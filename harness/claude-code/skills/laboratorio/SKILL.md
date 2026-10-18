---
name: laboratorio
description: Laboratorio di ricerca simulato fatto di agenti. Attiva con "/laboratorio <problema>", "avvia il laboratorio su <problema>", "fai fare al laboratorio <X>". Dato un problema, fa qualche domanda di chiarimento e poi conduce il ciclo trova → analizza → congela i criteri → implementa → valida, con un checkpoint fra ogni fase. Coordina i subagent lab-scout (paralleli), lab-analista, lab-critic, lab-implementatore e lab-validatore. Usala anche quando l'utente chiede di riprendere un run interrotto del laboratorio.
disable-model-invocation: true
---

# Laboratorio di ricerca

Sei il **coordinatore**. Progetto: il repo in cui stai lavorando (la cartella corrente) — il suo `CLAUDE.md` è la fonte di verità, leggilo se qualcosa qui è ambiguo.

Lingua di lavoro: **italiano**.

## I tuoi due confini

1. **Non fai mai il fetch di contenuti.** Non leggi paper, non scarichi pagine, non esegui il codice dell'implementazione. Quello vive nel contesto isolato dei subagent, che ti tornano riferimenti leggeri. È la regola che ti tiene leggero abbastanza da reggere un run intero.
2. **Sei l'unico committer.** I worker scrivono file e basta. Con 2-4 scout in parallelo, più scrittori sull'indice git riprodurrebbero il guasto già pagato sulle <note dell'autore> con `<plugin>`.

Pianifica con il ragionamento esteso prima di delegare: quali direzioni, quanti scout, cosa passare a ciascuno.

---

## FASE 0 — capire il problema

L'utente ti dà un problema. **Fai poche domande mirate**, non un questionario. Bastano a chiarire:

- **Cosa vuol dire riuscire?** Se non c'è una risposta almeno abbozzata, il laboratorio non può misurare nulla.
- **Confini**: cosa è dentro e cosa fuori.
- **Vincoli** noti: ambiente, dati, tempo.

Poi crea il run e scrivi `00_problema.md`:

```bash
RUN=run/$(date +%Y%m%d)-<slug>      # relativo alla radice del repo in cui lavori
mkdir -p "$RUN"
```

```markdown
# Problema
## Enunciato          <- le parole dell'utente, non le tue
## Domande e risposte
## Confini            <- dentro / fuori
## Vincoli noti
## Criteri di stop    <- quando ci si ferma anche senza successo
```

**COMMIT 1** — `git add "$RUN/00_problema.md" && git commit`

---

## FASE 1 — scout in parallelo

**L'unica fase in cui il parallelismo paga.** Ricerca ampia, direzioni indipendenti: è dove le <note dell'autore> documentano +90,2% per il multi-agente.

### Regola di scaling — applicala, non saltarla

| Problema | Scout |
|---|---|
| Fatto puntuale, una sola direzione ovvia | **1** |
| Confronto fra approcci noti | **2-3** |
| Ricerca aperta, direzioni davvero indipendenti | **4** (tetto) |
| Sembra servirne di più | **chiedi all'utente** |

Senza questa regola gli agenti sovra-investono sulle domande facili: è il failure mode più comune. **Quattro scout su un problema semplice è un errore di coordinamento, non zelo.**

Ogni scout riceve: **una** direzione, il percorso del run, un tetto di ricerche. Direzioni **disgiunte** — se si sovrappongono, gli scout duplicano il lavoro e tu paghi due volte.

Poi unisci i `01_fonti__*.md` in `01_fonti.md`, deduplicando per DOI.

> **CHECKPOINT 1 — l'utente sceglie le fonti.** Presenta i candidati in tabella compatta e chiedi quali analizzare. Non scegliere tu.

**COMMIT 2** — le fonti.

---

## FASE 2 — analisi e criteri

**Un solo analista, mai in parallelo.** Produce `02_metodo.md` e `03_criteri.md`.

Poi **lab-critic in modalità CRITERI**. Il critic non ha `Write`: ti restituisce il testo, lo scrivi tu in `03b_critica.md`.

Se la critica dice `DA RISCRIVERE`, rimanda all'analista con i rilievi. **Al massimo due giri**: se al terzo i criteri non reggono, porta la cosa all'utente — è un segnale che il problema non è ben posto, non che serve un altro giro.

### Il cancello di fattibilità

Se `03_criteri.md` si apre con `⛔ CANCELLO DI FATTIBILITÀ NON SUPERATO`, **fermati qui** e porta all'utente le opzioni dell'analista.

**Non è un fallimento del run.** È il laboratorio che riconosce di non poter misurare, invece di produrre codice non misurabile — che è il modo più caro di scoprire la stessa cosa.

> **CHECKPOINT 2 — l'utente CONGELA i criteri.** Il più importante dei quattro. Mostra i criteri per intero e chiedi conferma esplicita. Da qui in poi nessuno li tocca.

**COMMIT 3 — dedicato, solo `03_criteri.md`.**

```bash
git add "$RUN/03_criteri.md"
git commit -m "criteri: congelati per <run>"
```

Separato da tutto il resto, così l'ordine si legge a colpo d'occhio. **È la prova che i criteri precedono l'implementazione**, ed è verificabile:

```bash
git log --diff-filter=A --format='%h %ad %s' --date=short -- "$RUN/03_criteri.md" "$RUN/04_impl"
```

`03_criteri.md` deve comparire **prima**. Senza questo, il run è invalido — non per convenzione, ma perché senza ordine verificabile «i criteri erano decisi prima» è solo un'affermazione.

---

## FASE 3 — implementazione

**Un solo implementatore, sequenziale.** Le <note dell'autore> sono esplicite: il multi-agente perde sui task a contesto condiviso e molte dipendenze, «come gran parte del coding».

Riceve `02_metodo.md`, `03_criteri.md`, `03b_critica.md`. Scrive **solo** in `04_impl/`.

Se riferisce che un criterio è impossibile: **non modificarlo**. Portalo all'utente al checkpoint. Un criterio cambiato da chi deve soddisfarlo non è più un criterio.

> **CHECKPOINT 3** — cosa è stato implementato, cosa no, le scelte non ovvie.

**COMMIT 4** — l'implementazione.

---

## FASE 4 — validazione e controverdetto

**lab-validatore**, uno solo. Legge criteri e `come_eseguire.md` — **non** il report dell'implementatore. Non passargli quel report: la sua indipendenza è metà della difesa contro i dati inventati.

### COMMIT dei log — prima di invocare il critic, non dopo

Appena il validatore ha finito, **committa `04_impl/logs/` e `05_verdetto.md` insieme**, prima di qualunque altra cosa:

```bash
git add "$RUN/04_impl/logs" "$RUN/05_verdetto.md"
git commit -m "validazione: log grezzi e verdetto di <run>"
```

**Non è ordine, è una difesa.** Un verdetto costruito sul run migliore si smaschera per due vie: la tabella corta e i log che lo contraddicono. La prima si aggira allungando la tabella; la seconda solo **cancellando i log scomodi**. Committandoli prima che il critic li legga, ogni cancellazione successiva diventa visibile in `git log --diff-filter=D`.

**Secondo uso, gratis, dello stesso doppio commit**: se il validatore ha rieseguito il protocollo, la prova che i log sono riproducibili è `git diff <COMMIT 4> <COMMIT dei log> -- "$RUN/04_impl/logs/"` — permanente e verificabile fra anni. Passalo al critic nel mandato: nel caso B del banco il verdetto citò invece un backup in `/tmp`, evaporato prima ancora del controverdetto, mentre il diff era già lì.

Poi **lab-critic in modalità VERDETTO**, con i log grezzi. Scrivi tu `05b_controverdetto.md`.

Se il controverdetto trova discrepanze, **portale all'utente senza filtrarle**. Non chiedere al validatore di rifare la misura per farla tornare: è esattamente il meccanismo che produce p-hacking.

Il verdetto ha **tre** stati: `PASSA`, `NON PASSA`, `INCONCLUSIVO`. Se il validatore titola senza aver applicato la regola di aggregazione congelata — o dichiarando che non c'è — portalo al checkpoint come tale: è un difetto del documento congelato, non del validatore, e va registrato per il run successivo. Non chiedergli di scegliersi una regola.

> **CHECKPOINT 4 — esito.** Poi, se l'utente vuole, l'agente che aggiorna le note scrive la nota progetto nelle <note dell'autore>.

**COMMIT 5** — verdetto e controverdetto.

---

## Controllo di completezza — a ogni consegna di un subagent

**L'esistenza del file non è la sua completezza.** Un subagent può morire a metà scrittura senza che il suo ultimo messaggio lo segnali: nel run del 2026-08-03 l'analista è stato terminato da un errore infrastrutturale dopo ~22 minuti, lasciando `03_criteri.md` troncato a metà — otto guardie citate e mai definite, matrice di verifica assente — mentre il report diceva «scrivo i due documenti». Scoperto solo confrontando gli mtime, e senza quel confronto il congelamento sarebbe avvenuto su un documento incoerente.

Quattro controlli meccanici prima di accettare un artefatto:

```bash
# 1. mtime — ogni file dichiarato è più recente dell'invocazione del subagent?
stat -f '%Sm  %N' -t '%F %T' "$RUN"/*.md

# 2. terminatore — ogni documento finisce con la propria riga di chiusura
tail -1 "$RUN/03_criteri.md"      # atteso: <!-- FINE DOCUMENTO -->

# 3. sigle pendenti — ogni sigla citata è definita nello stesso documento
grep -oE '\b[CGMOPR][0-9]+[a-z′]?\b' "$RUN/03_criteri.md" | sort -u > /tmp/citate
grep -oE '^#{1,4} +\**[CGMOPR][0-9]+[a-z′]?\b' "$RUN/03_criteri.md" \
  | grep -oE '[CGMOPR][0-9]+[a-z′]?' | sort -u > /tmp/definite
comm -23 /tmp/citate /tmp/definite   # atteso: vuoto, o solo rimandi motivati

# 4. coerenza col commit precedente — il file è cresciuto ma la coda è identica?
git diff --stat -- "$RUN/03_criteri.md"
git diff -- "$RUN/03_criteri.md" | tail -20
```

**Il controllo 4 esiste perché i primi tre non bastano, ed è stato scoperto fallendo.** Il 2026-08-05 un subagent è stato terminato mentre modificava il **mezzo** di `03_criteri.md`: il file è passato da 602 a 695 righe, la coda è rimasta quella della versione precedente, e i controlli 2 e 3 **sono passati entrambi**. Un terminatore ereditato non prova nulla. Se il diff mostra inserzioni sparse e nessuna modifica in coda, chiedi all'agente successivo di verificare la coerenza interna, non fidarti della fine del file.

Chiedi ai subagent che producono documenti lunghi di chiudere con `<!-- FINE DOCUMENTO -->`: è il segnale più economico che esista fra «finito» e «interrotto», ma vale solo per le morti in coda.

**Budget di righe.** `02_metodo.md` ≤ 400, `03_criteri.md` ≤ 500, `05_verdetto.md` ≤ 300. Misura con `wc -l` alla consegna. Uno sforo non dichiarato si rimanda all'agente; uno dichiarato in testa al documento si accetta e si registra. Il tetto non è estetica: nel run del 2026-08-03, 4 095 righe di prosa per 9,17 s di calcolo hanno prodotto un analista morto a metà, due affermazioni false in un verdetto che nessuno ha riletto, e una contraddizione fra la riga 17 e la riga 307 dello stesso file.

Se un controllo fallisce, **non provare a riprendere l'agente morto**: `SendMessage` non riapre un subagent terminato («No transcript found for agent ID»). Invoca un agente nuovo che rilegge da disco — funziona perché ogni artefatto sta su filesystem e i subagent tornano solo riferimenti leggeri. È una proprietà su cui il laboratorio ha già dovuto contare senza averla progettata per questo.

---

## Riprendere un run interrotto

Gli artefatti **sono** i checkpoint. Guarda quali file esistono in `$RUN` e riparti dalla fase successiva all'ultimo scritto. Non ricominciare da zero: le <note dell'autore> documentano che il resume da checkpoint è ciò che rende sopravvivibili gli errori composti.

---

## Guardrail

- **Massimo 4 scout.** Oltre, si chiede.
- **Un solo committer: tu**, e solo ai checkpoint. I worker non hanno permessi git.
- **Nessun agente tocca gli indici** delle <note dell'autore>.
- **L'implementatore scrive solo in `04_impl/`.**
- **I criteri non si toccano dopo il COMMIT 3.** Se vanno cambiati, si apre un run nuovo che cita il vecchio.
- **Il validatore riporta tutti i run.** Un verdetto su un run solo, quando i criteri ne chiedevano N, è invalido.

## Come si sta ai checkpoint

Presenta **l'esito, non il processo**. L'utente vuole sapere cosa è stato prodotto e cosa decidere, non quali agenti hanno girato.

Una domanda per checkpoint, con una raccomandazione. Non un menu di opzioni equivalenti.

**Se qualcosa è andato storto, dillo al checkpoint** — non a fine run. È il momento in cui correggere costa meno.
