#!/bin/bash
# Il sistema sotto test e' ancora quello dell'istantanea?
#
# Fino al 2026-09-30 le definizioni vivevano in ~/.claude, globale e non sotto
# git; dal commit 4615d0f del laboratorio vivono nel repo, in .claude/agents e
# .claude/skills, e un run le legge dalla COPIA dentro il proprio repo (stessa
# logica gia' applicata al CLAUDE.md il 2026-08-17). Resta vero che un file
# modificato a run in corso cambia il sistema a meta' misura: i subagent le
# rileggono da disco a ogni invocazione. Le definizioni NON si caricano una volta all'avvio
# di un run: ogni subagent le rilegge da disco quando viene invocato. Una
# sessione qualsiasi che le modifichi mentre un caso gira cambia il sistema
# sotto test a meta' misura, e nessun lock lo impedisce - quello delle <note dell'autore>
# protegge le <note dell'autore>, non ~/.claude.
#
# Questo script non impedisce la deriva: la rende visibile. E' la differenza
# fra un verdetto che non vale e un verdetto che non vale senza che si sappia.
#
# Il sistema sotto test non e' solo il testo delle definizioni: e' quel testo
# interpretato da una certa versione di Claude Code con un certo modello. Se
# l'istantanea ha un AMBIENTE.txt (le crea istantanea.sh dal 2026-08-09), qui
# si confronta anche quello e si stampa comunque l'ambiente vivo, cosi' finisce
# nei file sistema-<caso>-avvio.txt / -fine.txt che stacca.sh archivia: il
# modello del run del 2026-08-03 non e' ricostruibile proprio perche' nessuno
# lo aveva scritto da nessuna parte.
#
# L'uscita resta decisa dai SOLI sha256 delle definizioni. Una versione diversa
# del CLI e' deriva da leggere, non un run da buttare a meta': far uscire 1 qui
# ribalterebbe il significato dei confronti avvio/fine di stacca.sh su cui i
# giri gia' misurati sono stati letti.
#
# Uso:  bash verifica-sistema.sh [istantanea]
# Esce 0 se tutti gli sha256 coincidono, 1 altrimenti.

set -uo pipefail
BANCO="$(cd "$(dirname "$0")/.." && pwd)"
SNAP="${1:-$BANCO/istantanee/2026-08-05-post-fix}"
# Repo del run. Un coordinatore gira con `cd $REPO`, quindi le regole che legge
# sono $REPO/CLAUDE.md - la COPIA dentro il repo del giro, non il file vivo di
# <workspace>/laboratorio, che il confine di stacca.sh gli vieta perfino di aprire.
# Senza questo argomento si confronta il file vivo, ed e' il buco misurato il
# 2026-08-17: giro 2 e giro 3 hanno girato entrambi sul CLAUDE.md di FIX 1-8
# (a7b22b1) mentre questo script diceva INVARIATO leggendo il file vivo, che nel
# frattempo portava FIX 9-15. Attribuzione giusta per caso, non per costruzione.
REPO="${2:-}"

[ -f "$SNAP/SHA256SUMS.txt" ] || { echo "istantanea senza SHA256SUMS.txt: $SNAP"; exit 1; }
[ -z "$REPO" ] || [ -f "$REPO/CLAUDE.md" ] || { echo "repo senza CLAUDE.md: $REPO"; exit 1; }

# I file vivi, nell'ordine dei nomi usati dentro l'istantanea.
vivo_di() {
  local base
  if [ -n "$REPO" ]; then base="$REPO"; else base="<workspace>/laboratorio"; fi
  case "$1" in
    laboratorio-CLAUDE.md)      echo "$base/CLAUDE.md" ;;
    skill-laboratorio-SKILL.md) echo "$base/.claude/skills/laboratorio/SKILL.md" ;;
    *)                          echo "$base/.claude/agents/$1" ;;
  esac
}

derive=0
while read -r atteso nome; do
  [ -n "$nome" ] || continue
  vivo="$(vivo_di "$nome")"
  if [ ! -f "$vivo" ]; then
    echo "MANCANTE  $nome  ($vivo)"; derive=$((derive+1)); continue
  fi
  ora="$(shasum -a 256 "$vivo" | cut -d' ' -f1)"
  if [ "$ora" != "$atteso" ]; then
    echo "DERIVATO  $nome"
    echo "          atteso $atteso"
    echo "          ora    $ora"
    echo "          file   $vivo  (mtime $(stat -f '%Sm' -t '%F %T' "$vivo"))"
    derive=$((derive+1))
  fi
done < "$SNAP/SHA256SUMS.txt"

# --------------------------------------------------- quale CLAUDE.md e' stato letto
# Si stampa SEMPRE: senza questa riga non si distingue un INVARIATO sul file che il
# run legge davvero da uno sul file vivo che non legge nessuno (buco del 2026-08-17).
if [ -n "$REPO" ]; then
  echo
  echo "Definizioni confrontate: $REPO/{CLAUDE.md,.claude/agents,.claude/skills}  (copie del repo del run — quelle che il coordinatore carica)"
  VIVO="<workspace>/laboratorio/CLAUDE.md"
  if [ -f "$VIVO" ] && [ "$(shasum -a 256 "$REPO/CLAUDE.md" | cut -d' ' -f1)" != "$(shasum -a 256 "$VIVO" | cut -d' ' -f1)" ]; then
    echo "  NOTA: diverso dal CLAUDE.md vivo di <workspace>/laboratorio. Non e' un errore —"
    echo "        e' il repo del giro che resta fermo alla versione con cui e' stato seminato."
    echo "        Ma il giro va attribuito a QUESTA copia, non al HEAD del laboratorio."
  fi
else
  echo
  echo "Definizioni confrontate: <workspace>/laboratorio/{CLAUDE.md,.claude/...}  (file VIVI)"
  echo "  ATTENZIONE: nessun repo passato come 2o argomento. Se stai verificando un run,"
  echo "  questo NON e' il file che il run legge: passa il repo del giro."
fi

# Copie residue a livello utente (informativo, non cambia l'esito): una copia in
# ~/.claude e' caricata da ogni sessione della macchina, anche fuori dal repo del
# run, ed e' un confondimento che l'istantanea registra in "copie-utente".
for f in "$HOME"/.claude/agents/lab-*.md "$HOME/.claude/skills/laboratorio/SKILL.md"; do
  [ -f "$f" ] && echo "  ATTENZIONE: copia a livello utente presente: $f (dal 30/09 non deve esistere)"
done

# ---------------------------------------------------------------- ambiente
# Informativo: non tocca il codice di uscita (vedi intestazione).
VERSIONE_ORA="$(claude --version 2>&1 | head -1)"
MODELLO_ORA="$(python3 -c '
import json, sys
try:
    with open(sys.argv[1]) as f:
        print(json.load(f).get("model", "(campo model assente)"))
except Exception as e:
    print("(illeggibile: %s)" % e)
' "$HOME/.claude/settings.json" 2>/dev/null || echo "(illeggibile)")"
STACCA_ORA="$(sed -n 's/^MODELLO="${MODELLO:-\(.*\)}"$/\1/p' "$BANCO/giro-auto/stacca.sh" | head -1)"

echo
echo "AMBIENTE (informativo, non cambia l'esito)"
echo "  claude-code ora:    $VERSIONE_ORA"
echo "  settings-model ora: $MODELLO_ORA"
echo "  stacca --model ora: ${STACCA_ORA:-(non trovato)}"

if [ -f "$SNAP/AMBIENTE.txt" ]; then
  # I valori possono avere un commento in coda fra parentesi, staccato da almeno DUE
  # spazi: si taglia quello. Un solo spazio fa parte del valore - "2.1.226 (Claude Code)"
  # e' cio' che stampa `claude --version`, non un commento.
  campo() { sed -n "s/^$1: *//p" "$SNAP/AMBIENTE.txt" | head -1 | sed 's/   *(.*$//' | sed 's/ *$//'; }
  confronta() {
    if [ -z "$2" ]; then
      echo "  $1: non registrato nell'istantanea"
    elif [ "$2" = "$3" ]; then
      echo "  $1: coincide con l'istantanea"
    else
      echo "  $1: DIVERSO — istantanea '$2', ora '$3'"
    fi
  }
  confronta "claude-code"    "$(campo claude-code)"    "$VERSIONE_ORA"
  confronta "settings-model" "$(campo settings-model)" "$MODELLO_ORA"
  confronta "stacca --model" "$(campo stacca-modello)" "$STACCA_ORA"
else
  echo "  istantanea senza AMBIENTE.txt: versione e modello di allora non registrati."
  echo "  Le prossime istantanee prendile con  bash istantanea.sh <nome>."
fi
echo

n=$(grep -c . "$SNAP/SHA256SUMS.txt")
if [ "$derive" -eq 0 ]; then
  echo "SISTEMA INVARIATO — $n file coincidono con $(basename "$SNAP")"
  exit 0
fi
echo
echo "SISTEMA DERIVATO — $derive file su $n cambiati rispetto a $(basename "$SNAP")."
echo "Un run in corso su questo sistema non e' interpretabile: le definizioni"
echo "sono cambiate mentre i subagent le rileggevano. Registra quali e quando."
exit 1
