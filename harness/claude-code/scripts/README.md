# Scripts (Claude Code harness)

Sanitized copies (see [SANITIZATION.md](../../../SANITIZATION.md)) of the scripts of the author's bench, comments in Italian. They are shown as they were used to
measure the benchmark, **not** as a portable tool: read them before running anything.

| Script | Purpose |
|---|---|
| `stacca.sh <case>` | detached launch of one case: model pre-flight, `claude -p` with pinned `--model` (`MODELLO=...` to override), confinement prompt, system check at start and end, status file |
| `sorveglia.sh` | watcher: relaunches stopped cases (`CASI="..." TETTO_ORE=6 bash sorveglia.sh`), exits on drift, relaunch cap, completion or time cap |
| `verifica-sistema.sh <snapshot> [repo]` | sha256 of the seven definitions vs a snapshot; prints the live environment. Exit 0 = unchanged |
| `istantanea.sh <name>` | takes a snapshot: copies of the definitions, `SHA256SUMS.txt`, `AMBIENTE.txt` (CLI version, models, plugins, hooks, lab HEAD) |
| `genera-prompt.sh <case.md>` | builds `prompt-<case>.txt`: `/laboratorio ` + case text + the unattended note |
| `prompt-NOTA-NON-PRESIDIATA.txt` | the unattended-mode note appended to every bench prompt |

**Paths must be adapted.** The scripts contained absolute paths of the author's machine, replaced here by the
placeholder `<workspace>/...` (lab repository, per-case run repositories, archive) and assume the
bench layout they came from:

```
<bench>/istantanea.sh
<bench>/istantanee/<snapshot>/          snapshots
<bench>/giro-auto/stacca.sh, sorveglia.sh, verifica-sistema.sh, genera-prompt.sh,
                  prompt-NOTA-NON-PRESIDIATA.txt, prompt-<case>.txt
```

They also use macOS tools (`caffeinate`, BSD `stat`, `shasum`). Apart from the sanitization, the files are
left as they were measured; adapt a copy, not these.
