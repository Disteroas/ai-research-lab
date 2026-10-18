#!/bin/bash
# Lancia UN caso del banco come processo STACCATO e torna subito.
# Sopravvive alla chiusura del terminale e alla sessione che lo lancia.
#
# Uso:  bash stacca.sh A-giro2
#       bash stacca.sh B-politiche-senza-memoria
#       bash stacca.sh C-trasferimento-labirinti
#
# Torna subito. Casi DIVERSI possono girare in parallelo: ognuno ha il proprio
# repo, quindi nessun indice git condiviso. Lo STESSO caso due volte no - due
# coordinatori sullo stesso indice sono il guasto che il laboratorio vieta per
# primo, ed e' lo script a rifiutare.
#
# macOS non ha `setsid`. La versione precedente lo invocava e falliva subito:
# si forka in python3 e si chiama os.setsid() nel figlio, che non e' capogruppo
# e quindi puo' farlo. Stesso meccanismo di notte.sh.

#
# MODELLO APPUNTATO, obbligatorio. Il 2026-08-05 il caso A automatico ha cambiato
# modello a meta' run - Opus 5 fino alle 00:18, Fable 5 dal rilancio delle 10:11 -
# perche' questo script non passava --model ed ereditava il default della macchina.
# settings.json dichiarava "opus" e il processo ha committato come Fable 5: il
# default NON e' una garanzia. Un confondimento di modello dentro un run rende il
# run non interpretabile, e cade proprio sulla catena criteri -> verdetto.
# Sovrascrivibile con MODELLO=... solo dichiarandolo nel registro del giro.

set -euo pipefail
SP="$(cd "$(dirname "$0")" && pwd)"
# Istantanea di riferimento del giro CORRENTE. Senza, verifica-sistema.sh usa il
# suo default (giro 2) e dal giro 3 in poi ogni run parte "gia' derivato":
# misurato il 2026-08-16, primo lancio di C. Da aggiornare a ogni cambio giro,
# o sovrascrivere con ISTANTANEA=... dichiarandolo nel registro.
ISTANTANEA="${ISTANTANEA:-$SP/../istantanee/2026-10-17-giro5}"
# Un repo per caso: tre coordinatori non possono condividere un indice git.
# Giro 5 (2026-10-17): i casi nuovi hanno "primo" nel nome file e vanno PRIMA
# dei pattern a lettera sola, altrimenti E-primo-* cadrebbe su E-* (giro 4,
# archiviato). I repo dei giri chiusi restano mappati solo per ispezione.
case "${1:-}" in
  A-primo-*) REPO_DEF="<workspace>/laboratorio-giro5-A1" ;;
  B-primo-*) REPO_DEF="<workspace>/laboratorio-giro5-B1" ;;
  E-primo-*) REPO_DEF="<workspace>/laboratorio-giro5-E1" ;;
  D-*)       REPO_DEF="<workspace>/laboratorio-giro5-D"  ;;
  A-*) REPO_DEF="<workspace>/laboratorio-giro-fix-A" ;;
  B-*) REPO_DEF="<workspace>/laboratorio-giro-fix"   ;;
  C-*) REPO_DEF="<workspace>/laboratorio-giro-fix-C" ;;
  E-*) REPO_DEF="<workspace>/laboratorio-giro4-E"    ;;
  *)   REPO_DEF="<workspace>/laboratorio-giro-fix"   ;;
esac
REPO="${REPO:-$REPO_DEF}"
# Giro 5: Opus 5.5 (decisione utente 2026-10-17, dichiarata nella pre-registrazione).
# Giri 2-4: claude-opus-5.
MODELLO="${MODELLO:-claude-opus-5-5}"
CASO="${1:?serve il nome del caso}"
PROMPT="$SP/prompt-$CASO.txt"
LOG="$SP/log-$CASO.txt"
STATO="$SP/stato-$CASO.txt"

[ -f "$PROMPT" ] || { echo "prompt mancante: $PROMPT"; exit 1; }
[ -d "$REPO/.git" ] || { echo "repo del giro mancante: $REPO"; exit 1; }

CONFINE="Confine di questa sessione: lavori esclusivamente dentro $REPO. Non leggere e non scrivere nelle <note dell'autore>, non aprire <workspace>/laboratorio, non aprire <workspace>/banco-laboratorio, e non aprire alcun file fuori da $REPO per nessun motivo, nemmeno per orientarti o per cercare contesto. Non c'e' alcun utente a cui rivolgerti: porta il compito a termine da solo e fermati quando il run e' completo."

# ---------------------------------------------------------------- figlio
if [ "${STACCA_FIGLIO:-}" = "1" ]; then
  {
    echo "IN CORSO"
    echo "caso:    $CASO"
    echo "avvio:   $(date '+%F %T')"
    echo "modello: $MODELLO"
    echo "repo:    $REPO"
    echo "log:     $LOG"
  } > "$STATO"

  # Il sistema sotto test com'era all'avvio. Se una sessione qualsiasi tocca
  # ~/.claude mentre il run gira, i subagent invocati dopo leggono definizioni
  # diverse: il confronto di fine run lo rende visibile.
  # "|| SISTEMA_AVVIO=$?" e non assegnazione secca: con set -e un esito 1 qui
  # uccideva il figlio PRIMA di lanciare claude, in silenzio (misurato
  # 2026-08-16). L'intento e' registrare la deriva, non abortire.
  SISTEMA_AVVIO=0
  bash "$SP/verifica-sistema.sh" "$ISTANTANEA" "$REPO" > "$SP/sistema-$CASO-avvio.txt" 2>&1 || SISTEMA_AVVIO=$?

  cd "$REPO"
  set +e
  claude -p "$(cat "$PROMPT")" \
    --model "$MODELLO" \
    --permission-mode bypassPermissions \
    --name "banco-auto-$CASO" \
    --append-system-prompt "$CONFINE" \
    > "$LOG" 2>&1
  esito=$?
  set -e

  {
    echo "FINITO"
    echo "caso:    $CASO"
    echo "fine:    $(date '+%F %T')"
    echo "modello: $MODELLO"
    echo "uscita:  $esito"
    echo "modelli che hanno committato (deve essercene UNO):"
    git -C "$REPO" log --format='%(trailers:key=Co-Authored-By,valueonly)' | sort -u | grep . | sed 's/^/  /'
    echo "sistema sotto test:"
    if [ "$SISTEMA_AVVIO" -ne 0 ]; then
      echo "  ATTENZIONE: gia' derivato ALL'AVVIO — vedi sistema-$CASO-avvio.txt"
    fi
    if bash "$SP/verifica-sistema.sh" "$ISTANTANEA" "$REPO" > "$SP/sistema-$CASO-fine.txt" 2>&1; then
      echo "  invariato dall'avvio alla fine"
    else
      echo "  DERIVATO DURANTE IL RUN — il verdetto di questo caso NON e' interpretabile."
      sed 's/^/  /' "$SP/sistema-$CASO-fine.txt"
    fi
    echo "ultime righe del log:"
    tail -5 "$LOG" | sed 's/^/  /'
    echo "commit:"
    git -C "$REPO" log --oneline | head -15
  } > "$STATO"
  exit 0
fi

# ---------------------------------------------------------------- padre
# Casi diversi girano in parallelo: repo separati, nessun indice condiviso.
# Lo STESSO caso due volte no - due coordinatori sullo stesso indice git sono
# il guasto che il laboratorio vieta per primo.
# Il processo trovato deve ESSERE un coordinatore, non limitarsi a nominarlo:
# stessa correzione applicata a sorveglia.sh il 2026-08-09, dove pgrep aveva letto
# una shell di sorveglianza come il caso sorvegliato e lo stallo e' costato 42
# minuti in silenzio. Qui l'effetto sarebbe opposto e piu' subdolo: un RIFIUTO che
# impedisce di rilanciare un caso morto, proprio quando serve rilanciarlo.
GIA_IN_CORSO=""
for _p in $(pgrep -f "banco-auto-$CASO" 2>/dev/null); do
  case "$(ps -o command= -p "$_p" 2>/dev/null)" in
    claude\ *) GIA_IN_CORSO="$_p"; break ;;
  esac
done
if [ -n "$GIA_IN_CORSO" ]; then
  echo "RIFIUTO: il caso $CASO sta gia' girando (PID $GIA_IN_CORSO)."
  ps -o pid=,command= -p "$GIA_IN_CORSO" | cut -c1-200
  exit 1
fi
# pgrep -fl stampa l'INTERA riga di comando, e i prompt sono multiriga:
# contarne le righe dava "34 casi" per un solo coordinatore. Si contano i PID.
# pgrep senza match esce 1; con "set -o pipefail" l'intera pipeline esce 1, e
# l'assegnazione prende quel codice: "set -e" uccideva lo script in silenzio
# proprio nel caso normale, cioe' un lancio con nessun altro caso in corso.
ALTRI=$( { pgrep -f "banco-auto-" || true; } | wc -l | tr -d " " )
# Il "|| true" non e' cosmetico: con set -e un test falso in coda a un && e'
# un comando fallito, e lo script moriva in silenzio con exit 1 proprio quando
# NON c'era nessun altro caso in esecuzione - cioe' nel caso normale.
if [ "${ALTRI:-0}" -gt 0 ]; then
  echo "== nota: $ALTRI altri casi del banco stanno girando (repo separati, ok)"
fi

# Pre-volo: il modello chiesto e' davvero quello che risponde?
# Il 2026-08-05 settings.json dichiarava "opus" e il processo staccato ha
# committato come Fable 5. Il default non e' una garanzia e --model da solo
# non prova nulla: si chiede, e se non torna quello atteso non si parte.
# Costa una richiesta di due secondi contro un run lungo da buttare.
ATTESO="${MODELLO#claude-}"
echo "== pre-volo: chiedo il modello a un processo nuovo ($MODELLO)"
# < /dev/null: senza, claude aspetta stdin 3 s e antepone un avviso alla
# risposta. L'avviso finisce dentro la stringa confrontata e rende il pre-volo
# fragile - passa per caso, perche' il model ID resta in coda.
RISPOSTA="$(claude -p 'Rispondi solo con il tuo model ID esatto, nient altro.' \
             --model "$MODELLO" < /dev/null 2>&1 | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]')"
case "$RISPOSTA" in
  *"$ATTESO"*)
    echo "== modello confermato: $RISPOSTA" ;;
  *)
    echo "RIFIUTO: chiesto '$MODELLO', ha risposto '$RISPOSTA'."
    echo
    echo "Non lancio: un run che cambia modello a meta' non e' interpretabile,"
    echo "ed e' esattamente il guasto del caso A automatico del 2026-08-05."
    echo
    echo "Se il ripiego e' voluto, lancia con il modello disponibile per TUTTI i"
    echo "casi del giro e dichiaralo nel registro:"
    echo "    MODELLO=<id> bash $0 $CASO"
    exit 1 ;;
esac

export STACCA_FIGLIO=1
nohup python3 -c '
import os, sys
if os.fork() == 0:
    os.setsid()
    fd = os.open(sys.argv[3], os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
    os.dup2(fd, 1); os.dup2(fd, 2)
    os.dup2(os.open(os.devnull, os.O_RDONLY), 0)
    os.execvp("caffeinate", ["caffeinate", "-dims", "bash", sys.argv[1], sys.argv[2]])
' "$0" "$CASO" "$SP/console-$CASO.txt" < /dev/null > /dev/null 2>&1 &

sleep 3
echo "== $CASO staccato $(date '+%F %T')  modello: $MODELLO"
pgrep -fl "banco-auto-$CASO" | head -2 || echo "(processo non ancora visibile, ricontrolla fra poco)"
echo "== log:     $LOG"
echo "== stato:   $STATO"
echo "== console: $SP/console-$CASO.txt"
echo
echo "Il terminale e' libero. Il run continua anche se chiudi tutto."
echo "A che punto e':  cat $STATO"
echo "Fermarlo:        pkill -f 'banco-auto-$CASO'"
