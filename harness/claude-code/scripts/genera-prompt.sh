#!/bin/bash
# Genera giro-auto/prompt-<caso>.txt dal file del caso in casi/.
#
# Uso:  bash genera-prompt.sh ../casi/D-orizzonte-finito.md
#
# Formato (identico ai prompt dei giri 2-4, verificato con cmp su D il 2026-10-17):
#   riga 1:  "/laboratorio "
#   corpo:   il testo del caso dal primo "---" in poi (titolo e nota di consegna esclusi)
#   coda:    due righe vuote + prompt-NOTA-NON-PRESIDIATA.txt (checkpoint decisi dal
#            coordinatore, run precedenti nel repo non sono questa domanda)
#
# Il nome del prompt e' il nome del file del caso: la lettera resta solo qui, mai nel
# testo consegnato (decisione del 2026-08-19).
set -euo pipefail
SP="$(cd "$(dirname "$0")" && pwd)"
CASO_FILE="${1:?serve il file del caso, es. ../casi/D-orizzonte-finito.md}"
[ -f "$CASO_FILE" ] || { echo "file del caso mancante: $CASO_FILE"; exit 1; }
NOME="$(basename "${CASO_FILE%.md}")"
OUT="$SP/prompt-$NOME.txt"
{
  printf '/laboratorio \n'
  sed -n '/^---$/,$p' "$CASO_FILE" | tail -n +2 | sed '1{/^$/d;}'
  printf '\n\n'
  cat "$SP/prompt-NOTA-NON-PRESIDIATA.txt"
} > "$OUT"
echo "scritto $OUT ($(wc -l < "$OUT" | tr -d ' ') righe)"
