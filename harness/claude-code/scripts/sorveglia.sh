#!/bin/bash
# Sorveglia i casi del banco, RILANCIA da sola quello che si ferma, ed esce
# solo su ciò che richiede un giudizio umano.
#
# Perche' rilancia invece di svegliare qualcuno: il harness uccide i job
# bloccanti di lunga durata (misurato due volte il 2026-08-05, dopo 2 minuti
# e dopo pochi minuti), quindi non esiste un modo affidabile di svegliare la
# sessione. Un rilancio a livello di shell costa zero token e copre il caso
# frequente - un run che chiude il turno prima del controverdetto.
#
# ESCE, scrivendo EVENTO.txt, solo su:
#   1. deriva di ~/.claude mentre i run girano        -> nessun rilancio
#   2. tetto di rilanci raggiunto per un caso          -> serve capire perche'
#   3. tutti i casi hanno raggiunto il controverdetto
#   4. scadenza TETTO_ORE
#
# Uso:  CASI="A-giro2-continua" TETTO_ORE=6 bash sorveglia.sh
#
# Nessun set -e: questo script deve sopravvivere a ogni comando che fallisce,
# ed e' proprio il fallimento di pgrep senza match che ha gia' ucciso in
# silenzio stacca.sh il 2026-08-05.

set -uo pipefail
SP="$(cd "$(dirname "$0")" && pwd)"
BASE="<workspace>"
EVENTO="$SP/EVENTO.txt"
DIARIO="$SP/sorveglianza-diario.txt"
STORICO="$SP/storico"
CONTATORI="$SP/.sorveglianza"
PASSO="${PASSO:-120}"
TETTO_ORE="${TETTO_ORE:-6}"
TETTO_RILANCI="${TETTO_RILANCI:-8}"
# Stessa istantanea di stacca.sh: senza argomento verifica-sistema.sh confronta
# col giro 2 e dal giro 3 ogni controllo direbbe DERIVA (exit 3 al primo giro).
ISTANTANEA="${ISTANTANEA:-$SP/../istantanee/2026-10-17-giro5}"

read -r -a CASI <<< "${CASI:-A-giro2-continua}"
mkdir -p "$STORICO" "$CONTATORI"

# Contatori su file, non array associativi: bash di macOS e' 3.2 e "declare -A"
# non esiste - lo script sarebbe morto al primo giro. Su file c'e' anche un
# guadagno: il conteggio dei rilanci sopravvive a un riavvio del sorvegliante,
# quindi il tetto non si azzera se qualcuno lo uccide.
leggi() { cat "$CONTATORI/$1.$2" 2>/dev/null || echo 0; }
scrivi() { echo "$3" > "$CONTATORI/$1.$2"; }

log() { echo "$(date '+%F %T')  $*" >> "$DIARIO"; }

repo_di() {
  # Stessa mappa di stacca.sh (giro 5, 2026-10-17): i casi "primo" prima delle lettere.
  case "$1" in
    A-primo-*) echo "$BASE/laboratorio-giro5-A1" ;;
    B-primo-*) echo "$BASE/laboratorio-giro5-B1" ;;
    E-primo-*) echo "$BASE/laboratorio-giro5-E1" ;;
    D-*)       echo "$BASE/laboratorio-giro5-D"  ;;
    A-*) echo "$BASE/laboratorio-giro-fix-A" ;;
    C-*) echo "$BASE/laboratorio-giro-fix-C" ;;
    E-*) echo "$BASE/laboratorio-giro4-E"    ;;
    *)   echo "$BASE/laboratorio-giro-fix"   ;;
  esac
}

# Non basta che un processo NOMINI il caso: deve esserlo. Il 2026-08-09 l'unico
# match di pgrep era una shell di sorveglianza di un'altra sessione, che conteneva
# "banco-auto-B-continua" perche' lo stava cercando: il sorvegliante ha letto il
# proprio osservatore come l'osservato e non ha rilanciato per 42 minuti, in
# silenzio. Il coordinatore vero e' sempre un processo `claude`.
vivo() {
  local p
  for p in $(pgrep -f "banco-auto-$1" 2>/dev/null); do
    case "$(ps -o command= -p "$p" 2>/dev/null)" in
      claude\ *) return 0 ;;
    esac
  done
  return 1
}

# Il run del 2026-08-02 e' copiato in ogni repo e ha gia' il proprio
# controverdetto: escluderlo, o ogni processo morto sembra concluso bene.
concluso() {
  local f
  f=$(find "$1/run" -mindepth 2 -maxdepth 2 -name '05b_controverdetto.md' 2>/dev/null \
      | grep -v '/20260802-' | head -1)
  [ -n "$f" ]
}

# Un run morto per quota non va rilanciato subito: la finestra non e' rientrata.
per_quota() {
  tail -5 "$SP/log-$1.txt" 2>/dev/null | grep -qi "session limit\|usage limit\|rate limit"
}

archivia() {
  local c="$1" t; t=$(date '+%H%M%S')
  for f in "log-$c.txt" "stato-$c.txt"; do
    [ -f "$SP/$f" ] && cp "$SP/$f" "$STORICO/${t}-$f"
  done
}

rapporto() {
  {
    echo "EVENTO: $1"
    echo "quando: $(date '+%F %T')"
    echo
    echo "--- casi ---"
    for c in "${CASI[@]}"; do
      local r; r="$(repo_di "$c")"
      printf "%-26s vivo=%-3s rilanci=%-2s %s\n" "$c" \
        "$(vivo "$c" && echo si || echo no)" "$(leggi "$c" rilanci)" \
        "$(git -C "$r" log --oneline 2>/dev/null | head -1)"
      concluso "$r" && echo "    controverdetto PRESENTE" || echo "    controverdetto assente"
    done
    echo
    echo "--- sistema sotto test ---"
    bash "$SP/verifica-sistema.sh" "$ISTANTANEA" "$(repo_di "${CASI[0]}")" 2>&1 | tail -12
    echo
    echo "--- coda dei log ---"
    for c in "${CASI[@]}"; do
      echo "[$c]"; tail -4 "$SP/log-$c.txt" 2>/dev/null | sed 's/^/    /'
    done
    echo
    echo "--- diario recente ---"
    tail -12 "$DIARIO"
  } > "$EVENTO"
  log "EVENTO: $1"
}

log "sorveglianza avviata — casi: ${CASI[*]}, passo ${PASSO}s, tetto ${TETTO_ORE}h, max ${TETTO_RILANCI} rilanci"
SCADENZA=$(( $(date +%s) + TETTO_ORE * 3600 ))

while :; do
  sleep "$PASSO"
  ORA=$(date +%s)

  # 1. deriva: non si rilancia nulla, si chiama un umano.
  # Un controllo PER CASO, non uno globale: il CLAUDE.md che conta e' la copia
  # dentro il repo del caso, e due casi possono averne due diverse. Il controllo
  # globale del 2026-08-16 leggeva il file vivo, che nessun run apre (2026-08-17).
  for c in "${CASI[@]}"; do
    if ! bash "$SP/verifica-sistema.sh" "$ISTANTANEA" "$(repo_di "$c")" >/dev/null 2>&1; then
      rapporto "DERIVA — sistema cambiato mentre i run giravano (caso $c). Nessun rilancio."
      exit 3
    fi
  done

  aperti=0
  for c in "${CASI[@]}"; do
    r="$(repo_di "$c")"
    # Concluso = controverdetto presente E processo morto. Al giro 4 l'evento
    # TUTTI CONCLUSI e' stato scritto con vivo=si, 46 s prima che il coordinatore
    # finisse di scrivere: la presenza del controverdetto non e' la fine del run
    # (FIX 16, 2026-08-18). Chi punteggia aspetta comunque stato-<caso>.txt.
    if concluso "$r" && ! vivo "$c"; then continue; fi
    aperti=$((aperti+1))
    vivo "$c" && continue

    # fermo e non concluso: rilanciabile?
    n=$(leggi "$c" rilanci)
    if [ "$n" -ge "$TETTO_RILANCI" ]; then
      rapporto "TETTO RILANCI — $c fermo dopo $n rilanci senza arrivare al controverdetto"
      exit 2
    fi
    [ "$ORA" -lt "$(leggi "$c" attesa)" ] && continue

    if per_quota "$c"; then
      # Una sola attesa PER MORTE, ancorata al mtime del log: il log cambia solo
      # quando stacca.sh rilancia, quindi rileggerlo a ogni giro teneva il caso
      # in attesa perpetua — misurato il 2026-08-16, tre rinvii identici da 30
      # min senza mai riprovare. Ad attesa scaduta si TENTA il rilancio: se
      # muore di nuovo per quota il log ha un mtime nuovo e si attende di nuovo.
      MORTE="$(stat -f %m "$SP/log-$c.txt" 2>/dev/null || echo 0)"
      if [ "$(leggi "$c" quota_morte)" != "$MORTE" ]; then
        scrivi "$c" quota_morte "$MORTE"
        m=$(( (n + 1) * 15 )); [ "$m" -gt 60 ] && m=60
        scrivi "$c" attesa $(( ORA + m * 60 ))
        log "$c: morto per limite di quota, riprovo fra ${m} min"
        continue
      fi
      log "$c: attesa quota gia' fatta per questa morte, tento il rilancio"
    fi

    archivia "$c"
    n=$(( n + 1 )); scrivi "$c" rilanci "$n"
    log "$c: fermo senza controverdetto, rilancio n. $n"
    bash "$SP/stacca.sh" "$c" >> "$SP/sorveglianza-console.txt" 2>&1
    if [ $? -ne 0 ]; then
      scrivi "$c" attesa $(( ORA + 900 ))
      log "$c: rilancio FALLITO (pre-volo o altro), riprovo fra 15 min"
    fi
  done

  if [ "$aperti" -eq 0 ]; then
    rapporto "TUTTI CONCLUSI — ogni caso ha raggiunto il controverdetto"
    exit 0
  fi

  if [ "$ORA" -gt "$SCADENZA" ]; then
    rapporto "SCADENZA — ${TETTO_ORE}h senza conclusione, $aperti casi ancora aperti"
    exit 4
  fi
done
