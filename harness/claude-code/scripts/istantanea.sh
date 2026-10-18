#!/bin/bash
# Istantanea COMPLETA del sistema sotto test: definizioni + sha256 + AMBIENTE.
#
# Uso:  bash istantanea.sh <nome>            es.  bash istantanea.sh 2026-08-09-pre-giro3
#       bash istantanea.sh <nome> --forza    sovrascrive un'istantanea gia' esistente
#
# Crea  istantanee/<nome>/  con:
#   - le 7 definizioni vive copiate da <workspace>/laboratorio
#     (CLAUDE.md, .claude/agents/lab-*.md, .claude/skills/laboratorio/SKILL.md: dal
#     2026-09-30, commit 4615d0f, le definizioni vivono nel repo a scope progetto,
#     non piu' in ~/.claude; un run le legge dalla copia dentro il proprio repo)
#   - SHA256SUMS.txt   nel formato letto da giro-auto/verifica-sistema.sh
#   - AMBIENTE.txt     versione di Claude Code, modelli dichiarati, data/ora, HEAD del laboratorio
#   - README.md        bozza con i dati d'ambiente gia' compilati; il "cosa e' cambiato" si scrive a mano
#
# PERCHE' AMBIENTE.txt. Fino al 2026-08-09 l'istantanea registrava solo i file e i loro
# sha256: la versione di Claude Code e il modello finivano nel README a mano, quando ci si
# pensava. L'istantanea 2026-08-04-8d27db5 non li ha, e il modello del run del 2026-08-03
# non e' piu' ricostruibile - il sistema sotto test non e' solo il testo degli agenti, e'
# quel testo interpretato da quella versione del CLI con quel modello.
#
# Il modello DICHIARATO non e' il modello effettivo: il 2026-08-05 settings.json diceva
# "opus" e il processo staccato ha committato come Fable 5. Qui si registra cosa e'
# dichiarato e dove; la prova di cosa ha davvero risposto resta il pre-volo di stacca.sh
# e i trailer Co-Authored-By dei commit del run.
#
# Sola lettura su tutto cio' che sta fuori dal banco: copia, shasum, claude --version,
# lettura di settings.json e git rev-parse. Non lancia mai una sessione Claude.

set -euo pipefail

BANCO="$(cd "$(dirname "$0")" && pwd)"
LABORATORIO="<workspace>/laboratorio"

NOME="${1:?serve un nome per la istantanea, es. 2026-08-09-pre-giro3}"
FORZA="${2:-}"
DEST="$BANCO/istantanee/$NOME"

if [ -d "$DEST" ] && [ "$FORZA" != "--forza" ]; then
  echo "RIFIUTO: $DEST esiste gia'."
  echo "Un'istantanea si aggiunge, non si riscrive: e' il riferimento di run gia' misurati."
  echo "Se e' davvero da rifare:  bash $0 $NOME --forza"
  exit 1
fi

# I file che COMPONGONO il sistema sotto test, nome nell'istantanea -> file vivo.
# Stessa mappa di giro-auto/verifica-sistema.sh (funzione vivo_di): se qui si aggiunge
# un agente, aggiungerlo anche la'.
vivo_di() {
  case "$1" in
    laboratorio-CLAUDE.md)      echo "$LABORATORIO/CLAUDE.md" ;;
    skill-laboratorio-SKILL.md) echo "$LABORATORIO/.claude/skills/laboratorio/SKILL.md" ;;
    *)                          echo "$LABORATORIO/.claude/agents/$1" ;;
  esac
}

# Copie residue a livello utente: dal 30/09 non devono esistere. Una copia in
# ~/.claude verrebbe caricata da OGNI sessione della macchina, anche fuori dal
# repo del run: non e' deriva dei 7 file, e' un confondimento da registrare.
COPIE_UTENTE=""
for f in "$HOME"/.claude/agents/lab-*.md "$HOME/.claude/skills/laboratorio/SKILL.md"; do
  [ -f "$f" ] && COPIE_UTENTE="$COPIE_UTENTE $f"
done

FILE=(
  lab-analista.md
  lab-critic.md
  lab-implementatore.md
  lab-scout.md
  lab-validatore.md
  laboratorio-CLAUDE.md
  skill-laboratorio-SKILL.md
)

# Prima si controlla che ci siano TUTTI: un'istantanea parziale e' peggio di nessuna,
# perche' verifica-sistema.sh la dichiarerebbe "invariata" sui soli file presenti.
manca=0
for n in "${FILE[@]}"; do
  v="$(vivo_di "$n")"
  [ -f "$v" ] || { echo "MANCANTE  $n  ($v)"; manca=$((manca+1)); }
done
[ "$manca" -eq 0 ] || { echo; echo "RIFIUTO: $manca file del sistema non esistono. Istantanea non creata."; exit 1; }

mkdir -p "$DEST"
for n in "${FILE[@]}"; do
  cp "$(vivo_di "$n")" "$DEST/$n"
done

( cd "$DEST" && shasum -a 256 "${FILE[@]}" > SHA256SUMS.txt )

# ---------------------------------------------------------------- ambiente
VERSIONE="$(claude --version 2>&1 | head -1)"
BINARIO="$(command -v claude || echo '(claude non nel PATH)')"

# settings.json in SOLA LETTURA. python3 c'e' gia' (lo usa stacca.sh per il fork).
SETTINGS="$HOME/.claude/settings.json"
MODELLO_SETTINGS="$(python3 -c '
import json, sys
try:
    with open(sys.argv[1]) as f:
        print(json.load(f).get("model", "(campo model assente)"))
except Exception as e:
    print("(illeggibile: %s)" % e)
' "$SETTINGS" 2>/dev/null || echo "(illeggibile)")"

# Il --model che gli script di lancio passano davvero.
MODELLO_STACCA="$(sed -n 's/^MODELLO="${MODELLO:-\(.*\)}"$/\1/p' "$BANCO/giro-auto/stacca.sh" | head -1)"
[ -n "$MODELLO_STACCA" ] || MODELLO_STACCA="(default MODELLO non trovato in stacca.sh)"

CON_MODEL=""
SENZA_MODEL=""
for s in "$BANCO"/giro-auto/*.sh; do
  b="$(basename "$s")"
  # Solo gli script che lanciano davvero una sessione: altrove "--model" e' testo.
  grep -q 'claude -p' "$s" || continue
  if grep -q -- '--model' "$s"; then
    CON_MODEL="$CON_MODEL $b"
  else
    SENZA_MODEL="$SENZA_MODEL $b"
  fi
done

HEAD_LAB="(repo laboratorio non trovato)"
if [ -d "$LABORATORIO/.git" ]; then
  # rev-parse e' lettura pura: non tocca l'indice del repo sotto test.
  HEAD_LAB="$(git -C "$LABORATORIO" rev-parse --short HEAD 2>/dev/null || echo '(HEAD illeggibile)')"
fi

# ------------------------------------------------- ambiente iniettato (FIX 16)
# Il giro 4 ha girato con due plugin a hook SessionStart e un CLAUDE.md globale
# modificato tre ore prima del lancio: variabili del sistema misurato che
# l'istantanea non catturava (giri/2026-08-17-ambiente-plugin-giro4.md, debito
# dichiarato). Da qui in poi si registrano. Sola lettura, come tutto il resto.
PLUGIN_ABILITATI="$(python3 -c '
import json, sys
try:
    with open(sys.argv[1]) as f:
        d = json.load(f).get("enabledPlugins", {})
    on = sorted(k for k, v in d.items() if v)
    print(" ".join(on) if on else "(nessuno)")
except Exception as e:
    print("(illeggibile: %s)" % e)
' "$SETTINGS" 2>/dev/null || echo "(illeggibile)")"

HOOK_SETTINGS="$(python3 -c '
import json, sys
try:
    with open(sys.argv[1]) as f:
        h = json.load(f).get("hooks", {})
    print(" ".join(sorted(h)) if h else "(nessuno)")
except Exception as e:
    print("(illeggibile: %s)" % e)
' "$SETTINGS" 2>/dev/null || echo "(illeggibile)")"

CLAUDEMD_GLOBALE="$HOME/.claude/CLAUDE.md"
if [ -f "$CLAUDEMD_GLOBALE" ]; then
  SHA_CLAUDEMD="$(shasum -a 256 "$CLAUDEMD_GLOBALE" | awk '{print $1}')"
  # Copia nell'istantanea: ~/.claude non e' sotto git, senza copia lo sha
  # prova solo CHE e' cambiato, mai COSA (lezione del 2026-08-17, diff
  # ricostruito dal contesto della sessione prima che sparisse).
  cp "$CLAUDEMD_GLOBALE" "$DEST/CLAUDE-md-globale.md"
else
  SHA_CLAUDEMD="(assente)"
fi

{
  echo "istantanea:        $NOME"
  echo "creata:            $(date '+%F %T %Z')"
  echo "host:              $(hostname -s)  $(uname -sr)"
  echo "claude-code:       $VERSIONE"
  echo "claude-bin:        $BINARIO"
  echo "settings-model:    $MODELLO_SETTINGS   (~/.claude/settings.json, campo \"model\")"
  echo "stacca-modello:    $MODELLO_STACCA   (giro-auto/stacca.sh, passato come --model)"
  echo "script-con-model: ${CON_MODEL:- (nessuno)}"
  echo "script-senza-model:${SENZA_MODEL:- (nessuno)}   <- ereditano il default della macchina"
  echo "laboratorio-HEAD:  $HEAD_LAB"
  echo "plugin-abilitati:  $PLUGIN_ABILITATI   (~/.claude/settings.json, enabledPlugins=true)"
  echo "hook-settings:     $HOOK_SETTINGS   (~/.claude/settings.json, chiavi di \"hooks\"; i plugin possono aggiungerne di propri)"
  echo "claudemd-globale:  $SHA_CLAUDEMD   (sha256 di ~/.claude/CLAUDE.md; copia in CLAUDE-md-globale.md)"
  echo "copie-utente:      ${COPIE_UTENTE:-(nessuna)}   (lab-* o skill laboratorio in ~/.claude: devono essere assenti)"
  echo
  echo "# Dichiarato != effettivo. Il 2026-08-05 settings.json diceva \"opus\" e il processo"
  echo "# staccato ha committato come Fable 5. Cosa ha DAVVERO risposto lo provano il"
  echo "# pre-volo di stacca.sh e i trailer Co-Authored-By dei commit del run, non queste righe."
} > "$DEST/AMBIENTE.txt"

# ---------------------------------------------------------------- README bozza
if [ ! -f "$DEST/README.md" ] || [ "$FORZA" = "--forza" ]; then
  {
    echo "# Istantanea $NOME"
    echo
    echo "TODO: perche' e' stata presa e cosa e' cambiato rispetto alla precedente."
    echo
    echo "Laboratorio a \`$HEAD_LAB\`."
    echo "Claude Code \`$VERSIONE\`."
    echo "Modello: settings.json \`$MODELLO_SETTINGS\`, appuntato per i run \`$MODELLO_STACCA\` (in \`giro-auto/stacca.sh\`)."
    echo
    echo "Per tornare a questo stato:"
    echo
    echo "    cp istantanee/$NOME/lab-*.md <workspace>/laboratorio/.claude/agents/"
    echo "    cp istantanee/$NOME/skill-laboratorio-SKILL.md <workspace>/laboratorio/.claude/skills/laboratorio/SKILL.md"
    echo "    cp istantanee/$NOME/laboratorio-CLAUDE.md <workspace>/laboratorio/CLAUDE.md"
    echo
    echo "## Ambiente"
    echo
    echo "In \`AMBIENTE.txt\` (generato da \`istantanea.sh\`, non a mano)."
    echo
    echo "## sha256"
    echo
    echo "In \`SHA256SUMS.txt\`, sui soli file di definizione."
    echo "Verifica contro il sistema vivo: \`bash giro-auto/verifica-sistema.sh istantanee/$NOME\`."
  } > "$DEST/README.md"
fi

echo "== istantanea creata: $DEST"
echo
cat "$DEST/AMBIENTE.txt"
echo
echo "== ${#FILE[@]} definizioni + SHA256SUMS.txt + AMBIENTE.txt + README.md (bozza: completa il TODO a mano)"
echo "== controllo: bash giro-auto/verifica-sistema.sh $DEST"
