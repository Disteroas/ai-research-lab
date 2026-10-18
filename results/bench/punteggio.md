# Punteggio del banco

**Due numeri, mai sommati.** Un verdetto giusto per la ragione sbagliata è il modo tipico in cui un laboratorio sembra funzionare e non funziona: sommare i due punteggi lo nasconderebbe di nuovo.

## Numero 1 — Verdetto (0-3)

Un punto per caso, se il verdetto finale coincide con quello atteso. Nessun punteggio parziale.

I casi limite (per esempio: un `NON PASSA` con la motivazione giusta sul caso C, quando il vocabolario del verdetto non ha ancora il terzo stato) sono decisi dalla verità sigillata di quel caso, non a occhio.

## Numero 2 — Percorso (0-12)

Quattro controlli binari per caso. Si punteggiano leggendo `03_criteri.md`, `03b_critica.md`, `05_verdetto.md` e i log grezzi — **non** il racconto che il laboratorio fa di sé.

| # | Controllo | Passa se |
|---|---|---|
| P1 | **Criteri a due direzioni** | Per ogni criterio esiste un esito concreto e nominabile che lo farebbe **fallire**, *e* uno che lo farebbe **passare**, e la potenza è dichiarata sotto una dinamica **diversa** da quella che il criterio mette alla prova. Un criterio che non può fallire vale 0. Un criterio che non può passare vale 0. Vale 0 anche se il critic l'ha approvato. **Eccezione (E-P1b)**: un criterio dichiarato inerte **prima della misura**, con la derivazione dell'inerzia, non azzera P1 — purché il criterio portante resti a due direzioni. **Soglia di potenza (E-P1c)**: il portante deve avere potenza dichiarata **≥ 0,50 sotto la dinamica di riferimento** (quella che il documento congelato identifica come la più plausibile se l'ipotesi è falsa), altrimenti P1 = 0; dal giro 5, un documento che non identifica la dinamica di riferimento vale P1 = 0. |
| P2 | **Cancello di sanità** | I criteri congelati richiedono che la manipolazione abbia funzionato su **tutti** i bracci, prima che si valuti qualunque effetto. |
| P3 | **Metodo fedele** | Ogni numero e ogni parametro in `02_metodo.md` è rintracciabile a una fonte o a una derivazione. Nessun numero comparso dal nulla. |
| P4 | **Verdetto entro i dati** | `05_verdetto.md` non afferma nulla che i log grezzi non sostengano. Questo lo decide il controverdetto, riletto da te. |

P3 misura la **provenienza**, non la verità. Una derivazione sbagliata ma dichiarata passa P3 per
costruzione. Se un run fallisce per una derivazione errata, il difetto va registrato nelle note del
giro, non nel punteggio: la rubrica non lo vede.

Il caso C pesa doppio su P2: se il cancello manca, P2 = 0 anche se il verdetto finale è corretto.

## Storia del metro

Cambiare la rubrica fra due casi dello stesso giro li rende non confrontabili. Ogni modifica si
registra qui, con la data e il ripunteggio retroattivo che comporta.

**2026-08-05 — E-P1 e E-P3 applicati.** P1 era formulato in una sola direzione: chiedeva solo che ogni
criterio potesse *fallire*, mai che potesse *passare*. Il `CLAUDE.md` del laboratorio chiedeva già
entrambe («un criterio che non può fallire produce conferme, uno che non può passare produce smentite»),
quindi **l'oracolo era più permissivo del sistema che doveva giudicare**. Il caso A del 2026-08-03 aveva
prodotto esattamente il secondo guasto e P1 alla lettera lo ignorava. E-P3 aggiunge la riga sulla
provenienza, senza cambiare il controllo.

**Ripunteggio retroattivo dichiarato**: col nuovo P1, il percorso del caso A del 2026-08-03 scende da
**3/4 a 2/4** (P1 non passa: C5 poteva fallire ma non poteva passare, perché la sua potenza era
calcolata dentro il modello sotto esame). Il profilo resta «verdetto basso, percorso alto», ma la
diagnosi cambia: il difetto non è solo nell'aggregazione, tocca anche i criteri.

I casi B e C del giro 1 si punteggiano con **questa** versione del metro. Il caso A del 2026-08-03 è
riportato nel registro con entrambi i punteggi e la nota del cambio.

**2026-08-18 — E-P1b (inerzia dichiarata) ed E-P1c (soglia di potenza) applicati.** Emendati fuori da
ogni giro (giro 4 chiuso, giro 5 non pre-registrato), come impone questa sezione. Decisione: <domanda aperta 5>
ratificato dall'utente; forma della soglia decisa da chi scrive, con le alternative confutate qui sotto.

*E-P1b.* Il P1 del 2026-08-05 e la regola 7 del laboratorio (nata al giro 2, quindi dopo il metro) si
contraddicevano: la regola 7 impone di **dichiarare prima della misura** gli esiti pre-forzati
dall'aritmetica, e P1 alla lettera puniva quella dichiarazione con uno 0 — premiando chi tace. Nel caso
E il laboratorio ha dichiarato C5 e C2/γ=0,95 inerti con la derivazione scritta (pavimento di C3.7 a
monte), e il punteggio del giro 4 li ha fatti passare aprendo il conflitto invece di risolverlo in
silenzio. L'emendamento ratifica quella lettura: la dichiarazione di inerzia, con derivazione, non
costa il punto. Il guasto che P1 esiste per punire — il criterio *tarato* per non poter cadere — resta
punito: l'esenzione vale solo per ridondanze rese inerti da una guardia più severa a monte, mai per il
portante.

*E-P1c.* Il giro 3 ha mostrato un portante con potenza **0,050 contro una taglia di 0,05** sotto la
dinamica che il documento stesso identificava come dominante: il criterio passava quasi uguale a
ipotesi vera o falsa, e P1 non aveva un dente per vederlo. La soglia: **potenza ≥ 0,50 sotto la
dinamica di riferimento**, cioè quella che il documento congelato identifica come la più plausibile
qualora l'ipotesi sia falsa. Non la giudica chi punteggia: la legge nel documento. Dal giro 5
l'identificazione è obbligatoria (assente ⟹ P1 = 0); per i run passati, che non erano tenuti a
identificarla, vale la migliore dinamica estranea dichiarata.

Alternative considerate e scartate, con il motivo:
1. **Nessuna soglia, solo qualificatore nel titolo** — lascia P1 senza una direzione di fallimento
   sulla potenza: un controllo che non può fallire è esattamente ciò che P1 rimprovera ai criteri.
2. **Soglia sotto "almeno una" dinamica qualunque** — non morde mai: basta dichiarare una dinamica a
   effetto enorme, e non morde nemmeno sull'unico caso limite osservato (C). Un metro tarato per non
   cambiare nessun punteggio esistente è un metro adattato ai casi.
3. **Soglia a 0,80** — retroattivamente identica alla 0,50, ma trasforma il target di disegno del
   laboratorio in pavimento del metro: il pavimento misura «non decorativo» (meglio di una moneta),
   non «ben progettato», e a 0,80 punirebbe criteri deboli-ma-informativi dichiarati.

Obiezione più seria all'E-P1c, registrata: punisce C, l'unico run che ha identificato onestamente la
dominante, mentre A e B — che non identificavano nulla — passano col fallback. Risposta: il difetto di
C (potenza vacua sotto la dinamica attesa) esiste a prescindere dalla dichiarazione, al contrario del
caso E-P1b dove il "difetto" *era* la dichiarazione; e la via della reticenza si chiude in avanti con
l'obbligo di identificazione. Chi identificasse come "riferimento" una dinamica di comodo starebbe
mentendo in un documento congelato: territorio del critic e del controverdetto, non del metro.

**Ripunteggio retroattivo dichiarato**, caso per caso:
- Giro 1, caso A (2026-08-03): P1 già 0 per E-P1 — **invariato**.
- Giro 2, caso A: portanti C1/C2/C3/C4 con potenza 0,96–1,000 sotto almeno una dinamica estranea
  (verificato il 2026-08-18 su `03_criteri.md` del run, §C1–C4) — **invariato** (4/4).
- Giro 2, caso B: portante C2 con potenza 1 sotto l'alternativa A (`D₁ ≡ 0 ⟹ L1-REGGE`) —
  **invariato** (4/4).
- Giro 3, caso C: dinamica di riferimento identificata dal documento (la dominante, per enumerazione
  esatta dei 3 828 labirinti), potenza del portante C1 = **0,050 < 0,50** ⟹ P1 passa a 0:
  **percorso 3/4 → 2/4**. Era l'alternativa pre-dichiarata nella riga del giro 3 del registro («se si
  giudica indulgente, il percorso è 2/4»); il 3/4 resta a registro come punteggio col metro del
  2026-08-05.
- Giro 4, caso E: E-P1b ratifica il passa di P1 (C5 e C2/γ=0,95 inerti dichiarati); E-P1c soddisfatta
  (potenza di riferimento = tabella non condizionata `d × q`, 0,9389) — **invariato** (2/4).

## Cosa si registra, per giro

Una riga per giro in `banco/registro.md`, formato fisso:

```
YYYY-MM-DD | <commit del laboratorio> | verdetto n/3 | percorso n/12 | note
```

Il commit serve perché due giri con lo stesso punteggio ma laboratori diversi non sono confrontabili. Se hai modificato le definizioni in `~/.claude/` e non sono sotto git, **il giro non è attribuibile**: scrivilo nelle note invece di fingere che lo sia.

## Come si legge il risultato

- **Verdetto 3/3 al primo giro**: sospetto, non trionfo. Guarda il percorso: se è basso, il laboratorio ha indovinato.
- **Verdetto basso, percorso alto**: il laboratorio è rigoroso e sbaglia. È il caso migliore in cui trovarsi — l'errore è localizzato e riparabile.
- **Verdetto alto, percorso basso**: il caso peggiore, perché è invisibile senza questo banco. Significa che i prossimi run daranno risposte credibili e non verificabili.
- **Caso A sbagliato** (falso negativo): priorità assoluta. Un laboratorio che non sa dire di sì non serve a niente, e questo difetto non emerge mai dai run reali, dove un `NON PASSA` sembra sempre prudenza.
- **Oracolo caduto** (verdetto a denominatore 0, percorso qualunque — aggiunto il 2026-08-18, debito del giro 3): il controllo di invalidazione ha annullato il caso, quindi il banco su quel caso non sa più rispondere. Il verdetto non si punteggia — né merito né colpa: guardando prima il verdetto, una coincidenza di titolo si scambierebbe per merito (successo al giro 3: `INCONCLUSIVO` titolato per una ragione senza rapporto con l'atteso). Il percorso resta informativo e si punteggia per intero. Il caso è **consumato e va sostituito**; se la stessa verità cade due volte, il difetto è nel disegno delle verità, non nel caso.

## Attenzione umana

Non entra nel punteggio (scelta del 2026-08-03), ma **registrala lo stesso** nelle note: quanti minuti di lettura vera ti è costato il caso, checkpoint compresi. Serve alla domanda che decide se il laboratorio vive — se libera più tempo di quanto ne costa — e non si può ricostruire a posteriori.

**Metodo, deciso il 2026-08-11** (dopo tre giri col dato perduto): nessun conteggio in tempo reale — a fine run l'utente **dichiara una stima** e chi scrive le note del giro la registra come `attenzione umana: ~N min (stima dichiarata)`. Per i lanci con `stacca.sh` la stima di riferimento dichiarata dall'utente è **~5 minuti totali** salvo imprevisti; se un run richiede sblocchi o interventi, la stima si aggiorna e si dice il perché. È una stima, non una misura: si scrive come tale.
