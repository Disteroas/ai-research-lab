# Laboratorio — CLAUDE.md

Laboratorio di ricerca simulato: un gruppo di agenti a cui si assegna un problema e che lo porta da "domanda" a "risultato validato". Lingua di lavoro: **italiano** (salvo termini tecnici e codice).

**Cosa NON è.** Non è un assistente per la ricerca vera dell'utente. Quella la conduce lui e resta sotto il suo controllo. Questo è un esperimento a sé: vedere fin dove arriva un laboratorio fatto di agenti.

**Deroga esplicita alla regola globale «i run li lancia solo l'utente»**: dentro `run/` gli agenti del laboratorio eseguono banco, implementazione e validazione da sé — è l'oggetto stesso dell'esperimento. La regola globale resta valida per tutto ciò che sta fuori da `run/`.

---

## Il problema che questo laboratorio esiste per non avere

I sistemi di questa famiglia hanno un failure mode **misurato, non ipotetico**. [Science](https://www.science.org/content/article/ai-agents-may-be-skilled-researchers-not-always-honest-ones) riporta che sia [Agent Laboratory](https://arxiv.org/pdf/2501.04227) sia AI Scientist v2 hanno compiuto atti non accettabili nella ricerca: **inventare dati** e fare **p-hacking**, cioè ripetere un esperimento e riportare solo il risultato migliore.

Sono due guasti distinti con due difese distinte:

| Guasto | Causa | Difesa strutturale |
|---|---|---|
| **p-hacking** | criteri scelti dopo aver visto i risultati, o criteri che non possono fallire | criteri **congelati prima**, con n. run e seed dichiarati, passati al vaglio del critic |
| **dati inventati** | chi produce il risultato è anche chi lo racconta | **validatore indipendente**, poi controverdetto che rilegge i log grezzi |

Agent Laboratory non ha un validatore indipendente: il *professor* scrive il report sui risultati dei propri colleghi. Qui quel ruolo è separato per costruzione.

**Regola che non si negozia:** se `03_criteri.md` non risulta committato **prima** del primo commit dentro `04_impl/`, il run è invalido. Non è una convenzione: è verificabile con `git log`.

---

## Forma del sistema

**Fan-out parallelo solo nella ricerca, poi catena sequenziale con checkpoint.**

Le <note dell'autore> documentano che il multi-agente vince sulla ricerca ampia a direzioni indipendenti (+90,2% vs singolo agente) e **perde** sui task a contesto condiviso e molte dipendenze — «come gran parte del coding». Analisi, implementazione e validazione sono il secondo caso: si fanno con **un agente alla volta**.

```
problema
   │
   ├── scout ×2-4  (paralleli — unica fase breadth-first)
   │      ↓ CHECKPOINT 1: l'utente sceglie le fonti
   ├── analista    → 02_metodo.md + 03_criteri.md
   ├── critic (1)  → 03b_critica.md   «questo criterio può fallire?»
   │      ↓ CHECKPOINT 2: l'utente CONGELA i criteri  ← commit dedicato
   ├── implementatore → 04_impl/
   │      ↓ CHECKPOINT 3
   ├── validatore  → 05_verdetto.md
   ├── critic (2)  → 05b_controverdetto.md  «i log reggono il verdetto?»
   │      ↓ CHECKPOINT 4
   └── l'agente che aggiorna le note (già esistente) → nota nelle <note dell'autore>
```

## Le figure

| Figura | Dove | Modello | Confine |
|---|---|---|---|
| Coordinatore | skill `laboratorio` | Opus | Parla con l'utente, delega, tiene i checkpoint. **Non fa mai fetch di contenuti** |
| `lab-scout` | subagent, 2-4 paralleli | Sonnet | Cerca e cataloga. **Non legge i full-text**, non giudica il metodo |
| `lab-analista` | subagent, uno | Opus | Legge in profondità. Produce metodo **e** criteri falsificabili |
| `lab-critic` | subagent, due invocazioni | Opus | Solo critica. **Non riscrive codice, non produce risultati** |
| `lab-implementatore` | subagent, uno | Opus | Scrive **solo** dentro `04_impl/`. Non tocca i criteri |
| `lab-validatore` | subagent, uno | Opus | Misura contro i criteri congelati. **Non legge i test dell'implementatore** |

**Allocazione dei modelli**: Opus dove c'è giudizio, Sonnet sugli scout che fanno estrazione in parallelo. È la configurazione a cui le <note dell'autore> attribuiscono +90,2%.

## Struttura di un run

`run/<AAAAMMGG>-<slug>/`

| File | Chi | Contenuto |
|---|---|---|
| `00_problema.md` | coordinatore | problema, domande poste, risposte, confini, criteri di stop |
| `01_fonti.md` | scout | candidati: riferimento, anno, DOI/URL, perché rilevante, qualità |
| `02_metodo.md` | analista | come funziona, ipotesi, parametri, cosa serve per riprodurlo |
| `03_criteri.md` | analista | criteri falsificabili con numeri, soglie, **n. run e seed** |
| `03b_critica.md` | critic | quali criteri non possono fallire, e come riscriverli |
| `04_impl/` | implementatore | codice + `come_eseguire.md` |
| `05_verdetto.md` | validatore | per criterio: atteso, misurato, esito. **TUTTI i run** |
| `05b_controverdetto.md` | critic | il verdetto è sostenuto dai log grezzi? |

I subagent **scrivono su filesystem e tornano al coordinatore solo riferimenti leggeri**, mai il contenuto: evita perdita di informazione e overhead di token. Ogni artefatto è anche il **checkpoint di ripresa**: un run interrotto riparte dall'ultimo file scritto.

## Il cancello di fattibilità

Fra analisi e implementazione il laboratorio deve rispondere da sé a: **«con cosa misuriamo il successo, e ce l'abbiamo su questa macchina?»**

Se i criteri richiedono un simulatore, un dataset o un hardware assenti, il run **si ferma qui e lo dichiara**. Fermarsi al cancello è un esito **riuscito**: è il laboratorio che riconosce di non poter misurare, invece di produrre codice non misurabile.

## Guardrail

- Massimo **4 scout** per run. Regola di scaling: fatto semplice → 1 scout; confronto → 2-4; oltre, si chiede all'utente. Senza regola esplicita gli agenti sovra-investono sulle domande facili: è il failure mode più comune.
- **Un solo committer: il coordinatore**, e solo ai checkpoint. I worker non ricevono permessi git e non toccano mai l'indice. Motivo: con più scout paralleli si avrebbero più scrittori sullo stesso indice — è il guasto già pagato sulle <note dell'autore> con `<plugin>`.
- `03_criteri.md` va in un **commit dedicato**, separato da tutto il resto, così l'ordine si legge a colpo d'occhio.
- L'implementatore scrive **solo** in `04_impl/`: mai nel codice di ricerca dell'utente, mai nelle <note dell'autore>.
- Nessun agente tocca gli indici delle <note dell'autore>.
- Euristiche, non regole rigide: partire da query brevi e ampie poi restringere; preferire fonti autorevoli (il bias verso contenuti SEO è documentato).

## Le tre regole del primo run vero

Dal run `20260802-generalizzazione-labirinti`, che è arrivato in fondo, è stato riprodotto tre volte e validato — e **non ha stabilito nulla sulla domanda che si era posto**. Sono le tre correzioni che sarebbero bastate.

### 1. Una guardia su un braccio si chiede su tutti i bracci

Verifica meccanica di fine stesura: bracci sulle righe, guardie sulle colonne, ogni casella vuota è una domanda.

Quel run aveva la guardia «il braccio di controllo deve aver imparato», aggiunta con la motivazione *un braccio rotto e uno che non trasferisce producono lo stesso numero*. La simmetrica sul braccio sperimentale non c'era. È successo esattamente lì.

Attenzione alle **guardie che si aprono da sole**: `a ≤ b + δ` è soddisfatta quando `a` e `b` valgono entrambi zero.

### 2. Le costanti congelate le produce il codice del banco

Mai uno script scritto per l'occasione. In quel run la baseline fu congelata a 0,6835 e il banco vero ne produce **0,72** — tutte le soglie derivate erano tarate su un banco inesistente, e l'errore è sopravvissuto a due giri di critica avversariale.

Costo della regola: zero.

### 3. «Può passare?» si chiede insieme a «può fallire?»

Un criterio che non può fallire produce conferme. **Uno che non può passare produce smentite** — e una smentita prodotta dalla taratura è p-hacking col segno rovesciato.

In quel run un criterio aveva probabilità **0,12** di passare con l'ipotesi vera, e 0,00 col soffitto della metrica. Nessuno se n'era accorto perché il documento dichiarava la *taglia* di quattro guardie e la *potenza* di nessun criterio.

La potenza va **dichiarata**, non solo esistere: «se l'effetto vero è X, questo criterio passa con probabilità Y». Dove Y è bassa, si cambia il protocollo o si scrive che il fallimento non sarà leggibile come assenza dell'effetto.

---

## Le tre regole del secondo run vero

Dal run `20260803-bandit-esplorazione`, che è arrivato in fondo, ha misurato bene, e ha titolato un verdetto che il proprio corpo contraddice.

### 4. Un elenco di criteri non è un verdetto

I criteri dicono se ciascuna soglia è superata. **Non dicono come si compongono**, e il conteggio è cieco alla direzione: una soglia unilaterale fallisce sia quando l'effetto è assente sia quando è più forte del previsto, e i due casi hanno verdetti opposti.

`03_criteri.md` deve contenere una **regola di aggregazione congelata**: per ogni criterio le due direzioni di fallimento e cosa implicano, quali criteri sono portanti, e cosa si titola quando un portante fallisce nella direzione che *rafforza* l'ipotesi. Se manca, il validatore riporta il conteggio e **non titola**.

In quel run la lettura corretta era congelata prima della misura, il verdetto l'ha scritta quattro righe sotto il titolo, e ha titolato lo stesso `NON PASSA` contando «7 su 8».

### 5. La potenza non si chiede al modello sotto esame

Dichiarare che un criterio «può passare» calcolandone la probabilità **dentro il modello che il criterio mette alla prova** non è una verifica: è un'eco. La potenza si dichiara sotto almeno **due** dinamiche — il modello assunto e un'alternativa concreta che esclude.

Attenzione in particolare all'**orologio**: quando un modello converte una velocità in una durata, la conversione ha un proprio parametro. Verificare la velocità non verifica l'orologio. In quel run l'orologio sbagliava di 1/ε = 200× e il criterio, di fatto, non poteva passare — sopravvissuto a due giri di critica avversariale perché entrambi lo chiesero alla stessa fonte.

### 6. Il verdetto ha tre stati

`PASSA`, `NON PASSA`, **`INCONCLUSIVO`**. Senza il terzo, «l'esperimento non decide» esce sempre come `NON PASSA` — che è un'affermazione sull'ipotesi, fatta senza sostegno. È già successo due run su due: il titolo più forte del corpo.

---

---

## Le cinque regole del giro 2 del banco

Dal caso B (`20260805-greedy-memoryless-pomdp`), che è arrivato in fondo con **zero rilievi bloccanti** e il cui critic ha scritto da sé le prime quattro; e dal punteggio del 2026-08-10, che ha prodotto la quinta. Nessuna di queste nasce da un guasto del verdetto: nascono tutte da **cose vere che il punteggio non vede**.

### 7. Un esito pre-forzato merita un'etichetta propria

Se `03_criteri.md` dichiara **prima della misura** che un esito del criterio portante è forzato dall'aritmetica — cioè che con le guardie passate non esiste profilo osservabile che dia l'altro esito — la regola di aggregazione **non deve mappare quell'esito su una delle tre etichette ordinarie**. O il passo che titola prevede un'etichetta distinta (`NON PASSA (forzato) — il run misura il banco, non l'ipotesi`), o il titolo porta il qualificatore di scope che la tabella congelata già contiene.

**Perché.** Il caso B l'ha fatto bene nel corpo e male nella riga del titolo. La qualificazione affidata al corpo **sopravvive fino alla prima sintesi e non oltre**: il titolo è l'unica riga che finisce nelle <note dell'autore>. Correzione di una parentesi, costo zero.

### 8. Un canale è indipendente solo fino al livello a cui esistono i log

«Ricalcolato dai grezzi» è vero solo se esiste un artefatto **sotto** gli aggregati che si stanno verificando. Il banco deve produrre almeno un livello inferiore: i ritorni per episodio di **una** coppia (parametro, seme), oppure un hash del vettore dei ritorni accanto alla media e alla deviazione standard.

**Perché.** Nel caso B il validatore ha scritto «ricalcolato riga per riga dal CSV grezzo, non dagli aggregati del banco», ma `Ĵ` e `σ̂` **sono** aggregati del banco: sotto non esiste nulla. Ciò che ha ricalcolato davvero sono ricombinazioni di quegli aggregati — verifica utile, di un livello sotto quello che la frase promette. Costo del rimedio: una riga di codice e ~200 kB.

### 9. La riproducibilità si prova con git, non con `/tmp`

Il coordinatore committa i log dopo l'implementazione e di nuovo dopo la validazione: `git diff <commit-impl> <commit-valid> -- logs/` è la prova, è permanente, ed è verificabile da chiunque a distanza di anni.

**Perché.** Nel caso B il validatore ha citato un backup in `/tmp/valid_backup_logs/`, evaporato **prima ancora del controverdetto**: il confronto byte per byte dichiarato non è più riverificabile da nessuno. La prova migliore esisteva già ed era gratuita — il diff mostra un solo file cambiato, e solo nelle righe di orario.

### 10. L'errore di modo comune fra metodo e banco va dichiarato

Il cancello di ancoraggio confronta il banco con l'algebra dell'analista. Se **entrambi** hanno trascritto lo stesso ambiente sbagliato da `00_problema.md`, ogni guardia passa e il canale «indipendente» meno che mai, perché legge le stesse costanti. Serve una riga in `03_criteri.md` che verifichi le costanti d'ambiente stampate **contro `00_problema.md`**, o almeno la dichiarazione esplicita che nessuno lo fa.

**Perché.** Nel caso B il buco è stato chiuso da un controllo a mano del critic, **non da un criterio**. Una difesa che dipende dalla diligenza di chi critica non è una difesa del sistema.

### 11. Una guardia fallita si qualifica per braccio, nella regola di composizione

Ogni riga della composizione che parla di guardie deve dire **su quali bracci**. «Guardie passate», senza qualificare, è ambiguo appena un braccio diagnostico fallisce una guardia che per lui è dichiarata non vincolante.

**Perché.** Nel caso A del giro 2 la riga che titola `PASSA` chiedeva «guardie passate» e il lato superiore di una guardia falliva su un braccio **non portante**, per un motivo previsto e pre-registrato. Presa alla lettera, nessuna riga scattava e il verdetto sarebbe uscito `INCONCLUSIVO`, cioè **sbagliato**. Il verdetto ha letto «sui portanti» — lettura corretta, perché la tabella dei profili di controllo pre-registrava quel profilo esatto — ma resta l'unico punto dell'intero giro in cui il titolo poggia su un atto interpretativo invece che sul testo. Costo della regola: due parole.

---

## Le sei regole del giro 4 del banco (FIX 16)

Dal caso E (`20260817-gamma-orizzonte-velocita`), il primo run su FIX 9-15: verdetto corretto con margine enorme, e insieme il **cancello di sanità passato 30/30 sul braccio costruito apposta per farlo scattare** — zero guardie mai scattate in quattro run veri. Le prime cinque le ha scritte il run stesso (L1-L5 del checkpoint 4); la sesta viene dal punteggio.

### 12. La clausola di potenza si condiziona alla risoluzione osservata della metrica

Non solo a `d` e `n`. Un `d = 1,00` ottenuto per **censura totale** di un braccio non è il `d = 1,00` che la formula modella: se la metrica non varia, il test non misura l'effetto, misura la censura. La guardia è `IQR > 0` sulla scala del portante, **sul braccio di controllo**, e va messa come **passo della composizione prima del titolo** — non come diagnostico: un diagnostico non ferma nulla.

**Perché.** Nel caso E il test dei segni non poteva restituire altro che `L` (`T_scorr(γ=0,95) = 50` su 30 semi su 30, il minimo della scala), e la clausola congelata sulla potenza è finita nel titolo come garanzia che i log smentivano. Il verdetto stesso l'ha scritto — «misura solo la censura» — ma nel corpo.

### 13. «Esito pre-forzato?» si verifica in entrambe le direzioni, e si rifà alla misura

Due domande, non una: «l'esito titolato era raggiungibile?» **e** «l'altro lo era?». E si ripetono **alla misura**, non solo alla stesura: un esito raggiungibile sulla carta può essere diventato forzato dai dati.

**Perché.** Nel caso E la risposta corretta esisteva, ma nel corpo, mentre la riga di intestazione verificava solo la direzione comoda. È la regola 7 completata: la 7 chiede l'etichetta, questa chiede il controllo che la fa scattare.

### 14. I testi di clausola congelati nominano la grandezza misurata, mai una metafora

«Abbandona il traguardo» è vero se «traguardo» è lo stato 10 e falso se è θ = 0,80: due letture, un titolo solo. `max_tasso_scorr` e `tasso 901–1000` non hanno questo problema. Una clausola che nomina la colonna del log si verifica leggendo il log; una che nomina una metafora si verifica interpretando — e l'interpretazione è il punto in cui il titolo si stacca dal corpo (successo tre volte su cinque casi).

### 15. `come_eseguire.md` contiene comandi e schemi di file, mai esiti

Nel caso E conteneva numeri di risultato (244 episodi con `=`, i 17 disallineamenti di C7). Impatto nullo — il critic li ha riprodotti da sé — ma è una via per cui l'esito dell'implementatore raggiunge il validatore **prima della misura**, cioè un canale che perfora l'indipendenza proprio dove serve.

### 16. Lo schema di ogni campo di log letto da un criterio si congela in `03_criteri.md`

Alfabeti, valori ammessi, unità. Nel caso E l'implementatore ha introdotto un terzo carattere `=` in `policy_greedy`, fuori dall'alfabeto `L/R` del metodo: deviazione conservativa e innocua, ma **nessun criterio prescriveva l'alfabeto** — non è una violazione trovata, è un buco di specifica trovato per fortuna dal critic. Ciò che un criterio legge dev'essere specificato al livello a cui lo legge.

### 17. Il cancello di apprendimento non può basarsi solo su un massimo storico

Serve una condizione sul regime **finale o sostenuto** (ultima finestra, o mediana delle ultime k), e il suo fallimento sul **braccio sperimentale** deve poter **fermare il confronto**, non solo qualificarlo.

**Perché.** Nel caso E la guardia C4 misurava il massimo su tutte le finestre, e l'ottimismo `Q₀ = 1` regala a un braccio che non impara una **gobba iniziale** che la soddisfa: passata 30/30 sul braccio sabotato (medie per finestra 0,41 · 0,52 · 0,18 · 0,04 — il massimo sta all'inizio, l'apprendimento no). Un massimo storico misura «è mai sembrato vivo», non «ha imparato»; l'esaurirsi dell'ottimismo iniziale li rende diversi per costruzione. È la difesa nata dal guasto del 2026-08-02, riscritta perché la sua prima forma verificata non vedeva il guasto per cui era nata.

---

## Le due regole del giro 5 del banco (FIX 17)

Da due run con misura pulita e diagnosi giusta nel corpo, e un titolo già scritto dai criteri congelati e approvati dal critic: **un esito non risolto con un'etichetta affermativa**, motivata dal fatto che quell'esito era previsto.

### 18. Il cancello chiede il criterio di successo del compito, uguale per ogni braccio

Quando la grandezza portante esiste solo per chi raggiunge il criterio di successo (tempo al criterio, prestazione dopo), il cancello della regola 17 chiede a **ogni** braccio il criterio **del compito** — la definizione di successo di `00_problema.md`, con soglia e tetto di censure uguali per tutti i bracci — mai l'obiettivo proprio di un braccio. Un regime che non raggiunge quel criterio non è ammesso, nemmeno se è l'ottimo della ricompensa di quel braccio o la previsione del metodo: lì la grandezza portante non ha un valore ma una censura, e il confronto si ferma (`INCONCLUSIVO — <braccio> non sostiene il criterio di successo del compito, k/N semi`). Per la stessa ragione la guardia di risoluzione (regola 12) vincola ogni braccio che entra nel portante: «non vincolante perché la censura è l'esito previsto» è il caso che deve fermare. Se il compito non fissa un criterio, o se il portante è il raggiungimento stesso, non raggiungerlo è la misura: vale la regola 17 com'è.

**Perché.** Nel caso E′ (`20261017-premio-di-tappa`) G3 era la regola 17 alla lettera — regime finale, bloccante — e ha visto V2 orbitare sulla tappa in 30 semi su 30. Ma ammetteva per V2 il regime `TAPPA`, perché «per V2 "imparare bene" il proprio MDP significa **non** raggiungere il traguardo»; e G4, che sull'IQR nullo di V2 sarebbe scattata, era non vincolante su V2, approvata dal critic come «non `INCONCLUSIVO` per costruzione». Zero guardie scattate, quinto run vero di fila, e un `NON PASSA — T_scorr di V2 maggiore di V1` su un braccio censurato 30/30. Il difetto è passato dalla misura alla regola.

### 19. «Non distinguibili» si titola `INCONCLUSIVO`, salvo che l'Enunciato chieda l'equivalenza

Se l'intervallo del portante contiene il confine che la domanda pone — la differenza nulla, o la soglia d'effetto dell'Enunciato — il titolo è `INCONCLUSIVO`, mai `PASSA` né `NON PASSA`, anche se l'intervallo sta dentro un margine di equivalenza. Unica eccezione: l'**Enunciato** di `00_problema.md` (le parole dell'utente, non le risposte del coordinatore in FASE 0) chiede l'equivalenza e ne fissa il margine o la fonte. Altrimenti il margine è una scelta di chi scrive i criteri, e spostarlo di poco cambia l'etichetta: il test di equivalenza si riporta come qualificatore dell'`INCONCLUSIVO` («IC ⊂ (−δ, δ), δ senza fonte»), non come risposta. «Non distinguibili» può essere un esito legittimo: il suo nome è il terzo stato. E la regola 6 non è soddisfatta perché `INCONCLUSIVO` è raggiungibile da qualche parte: lo è se lo prende l'esito che non decide.

**Perché.** Nel caso D (`20261017-ucb1-vs-egreedy`), domanda «quale delle due paga meno?», il coordinatore ha ammesso in FASE 0 «non distinguibili» come risposta; l'analista ne ha fatto un test di equivalenza con δ «scelta dell'analista, nessuna fonte»; il critic l'ha spostato da `NON PASSA` a `PASSA`, citando la regola 6. I criteri scrivevano da sé che il confine fra equivalenza e non risolto «dipende da δ più che dai dati». IC [−24,22; 7,72], a cavallo dello zero; titolo `PASSA — equivalenti entro δ = 27,86`, che regge per δ ≥ 26,55: con δ = 25 sarebbe stato `INCONCLUSIVO`. Il corpo sapeva di non sapere; il titolo ha trasformato il «non lo so» in una risposta.

---

E due regole di igiene, che non sono di metodo ma hanno lo stesso peso:

**L'esistenza di un artefatto non è la sua completezza.** Un subagent morto a metà scrittura lascia un documento che sembra finito e non lo è, e il suo ultimo messaggio non lo dice. Si controlla mtime, terminatore, sigle pendenti **e il diff contro l'ultimo commit** — un terminatore ereditato da una versione precedente non prova nulla quando la morte avviene a metà documento.

**Un documento che nessuno rilegge è una difesa installata, non verificata.** Tetti: `02_metodo.md` ≤ 400 righe, `03_criteri.md` ≤ 500, `05_verdetto.md` ≤ 300. Nel run del 2026-08-03: 4 095 righe di prosa per 9,17 s di calcolo.

---

## Verifica del laboratorio stesso

**Ogni difesa va vista fallire almeno una volta**, altrimenti non è stata verificata, è stata installata:

1. Si rompe di proposito l'implementazione → il validatore deve accorgersene.
2. Si sottopone un criterio non falsificabile (es. «il codice esegue senza errori») → il critic deve respingerlo.
3. Si produce un verdetto su un run solo quando i criteri ne chiedevano N → il controverdetto deve rilevarlo.
4. Su un problema banale il coordinatore deve lanciare 1 scout, non 4.
