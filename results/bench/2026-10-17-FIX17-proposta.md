# FIX 17 — proposta di regole dal giro 5, da installare prima del giro 6

Scritta il 2026-10-17 da un subagent della sessione principale, **a giro 5 chiuso** (riga di sintesi in
`registro.md`, riga 61). È una **proposta**: nessun file del laboratorio è stato toccato, nulla è
committato. La decide e la installa la sessione principale (pre-registrazione del giro 5, §6: «FIX 17 =
le lezioni dei quattro punteggi del giro 5, scritte come regole nel `CLAUDE.md` del lab (e, se serve,
nelle definizioni), dopo la chiusura del giro 5 nel registro»).

## Che cosa ho letto, e che cosa no

- **Sistema**: `<workspace>/laboratorio/CLAUDE.md` (236 righe, regole 1-17), `.claude/agents/lab-{analista,
  critic,validatore}.md`, `.claude/skills/laboratorio/SKILL.md`.
- **Banco**: `registro.md` (righe 41-61), i quattro punteggi del giro 5 per intero, la pre-registrazione
  del giro 5 per intero, `punteggio.md`, `giri/2026-08-04-analisi-a-freddo.md` §6-§10, la voce `<domanda aperta 7>`
  in `<open-questions file>`, `PROSSIMO-PASSO.md` righe 1-40.
- **Run**: `laboratorio-giro5-E1/run/20261017-premio-di-tappa/{00_problema,03_criteri,03b_critica}.md` e
  una riga di `02_metodo.md`; `laboratorio-giro5-D/run/20261017-ucb1-vs-egreedy/{00_problema,03_criteri,
  03b_critica}.md`.
- **Non aperti**: `verita/`, `casi/`, i verdetti e i controverdetti dei run (le cifre di misura che cito
  vengono dai punteggi, che le hanno ricalcolate dai grezzi).

**Contaminazione dichiarata.** Un `grep -rn "FIX 16"` lanciato sull'intero banco per trovare come fu
scritto il FIX 16 ha stampato, senza che li aprissi, frammenti di una riga ciascuno di `verita/E-primo.md`
(righe 108, 151, 157, 167, 179), `verita/A-primo.md` (304, 395) e `verita/B-primo.md` (361). Nessuna
regola qui sotto li usa: ogni motivazione viene dai file dei run o dai punteggi. Ai fini della regola del
cieco questo agente non coordina nulla; lo scrivo perché chi legge lo pesi.

**Vincolo seguito** (lo stesso dell'analisi a freddo, §6): il «Perché» di ogni regola cita **solo prove
interne ai run** — documenti congelati, titoli, cifre che il run stesso ha scritto — mai una verità
sigillata né un esito atteso dal banco. Come il FIX 16, nomina il caso e lo slug del run.

---

## 0. In una riga

**Due regole** nel `CLAUDE.md` (18: il cancello chiede il criterio di successo del compito; 19: «non
distinguibili» è `INCONCLUSIVO`), **una riga** nella tabella del critic, **nessuna** regola dalle lezioni
minori. Bruciati: **E′ e D**, già bruciati nel registro. A′ e B′ restano rilanciabili come sono.

---

## 1. Le due lezioni che decidono, verificate sui file

### 1.1 E′ — il regime rotto ammesso per iscritto [misurato sui file]

- `03_criteri.md:88-92` — G3 è la regola 17 alla lettera: misura il regime finale (episodi 901-1000), è
  bloccante («Il fallimento **ferma il confronto** … su qualunque braccio avvenga»), ma alla riga 90:
  «**Regimi ammessi**: V1 → solo `TRAGUARDO` … V2 → `TRAGUARDO` **o** `TAPPA` … Entrambi sono "ha
  imparato qualcosa che la sua ricompensa sostiene"».
- `02_metodo.md:165` — «Per V2 "imparare bene" il proprio MDP significa **non** raggiungere il traguardo:
  `03_criteri.md` lo tratta con una guardia di apprendimento che accetta due regimi per V2».
- `03_criteri.md:96-99` — G4 (regola 12) «vincolante su V1»; «**Su V2**: riportata, **non vincolante**.
  Motivo: V2 tutto censurato (IQR $=0$) è l'esito **previsto** dalla trappola».
- `03_criteri.md:135-136` — la matrice bracci × guardie registra le due asimmetrie come «motivate».
- `03b_critica.md:45-46` — il critic approva: «V2 intrappolata: regime `TAPPA` ammesso, titolo leggibile
  (`NON PASSA`, 7a'), non `INCONCLUSIVO` per costruzione»; «non vincolante su V2 motivato correttamente».
- Misura (punteggio E′, §3 righe 98-110, ricalcolata dai grezzi): V2 `TAPPA` 30/30, `T_scorr` censurato
  30/30, IQR $=0$; G3 passata su V2, G4 non vincolante; titolo al passo 7a' `NON PASSA — … T_scorr di V2
  maggiore di V1 …`. Zero guardie scattate (punteggio E′ §14, righe 407-413).

La lezione regge com'è scritta nel mandato: **la regola 17 è stata installata alla lettera e il difetto è
passato dalla misura alla regola** (punteggio E′, riga 446).

### 1.2 D — il «non lo so» rinominato risposta [misurato sui file]

- `00_problema.md:38` — D1, decisione del coordinatore (non dell'utente: riga 34, «Ogni risposta è una
  **decisione**, non un dato dell'utente»): «i tre esiti ammessi (UCB1 meno, ε-greedy meno, non
  distinguibili) … "non distinguibili" è un esito legittimo, non un fallimento».
- `00_problema.md:9` — l'Enunciato chiede solo «**quale delle due strategie ha rimpianto cumulativo atteso
  più basso?**»: nessun margine di equivalenza.
- `03_criteri.md:226-234` — regioni U/E/Q/N; «**Origine di δ**: **scelta dell'analista**, nessuna fonte. 5 %
  del rimpianto atteso di esplorazione».
- `03_criteri.md:235-238` — congelato da sé: «a effetto nullo, il confine Q/N dipende da δ più che dai
  dati»; $P(Q)$ a $E[D]=0$ vale 0,385 · 0,745 · **0,867** · 0,924 per $\delta$ = 20 · 25 · 27,86 · 30.
- `03b_critica.md:46-57` — R1 **bloccante**: titolare Q `NON PASSA` «è il guasto della regola 6»; «D1 dice
  esplicitamente che "non distinguibili" non è un fallimento»; riscrittura raccomandata Q ⟹ `PASSA`.
- `03_criteri.md:361-369` — la tabella congelata titola Q `PASSA — risposta: equivalenti entro δ = 27,86`;
  la «riga congelata sugli stati» legge la regola 6 così: «è soddisfatta perché `INCONCLUSIVO` esiste ed è
  raggiungibile».
- Misura (punteggio D, §2-bis e §8, righe 143-148 e 321-325): $\mathrm{IC}_{95\%} = [-24{,}22;\ 7{,}72]$,
  a cavallo dello zero; titolo Q; regge per $\delta \ge 26{,}55$ (leave-one-out); con $\delta = 25$ il
  titolo sarebbe stato `INCONCLUSIVO`. Il corpo del verdetto e il controverdetto lo scrivono (punteggio D,
  riga 325).

Anche questa regge com'è scritta nel mandato, con una precisazione che pesa sulla regola: **il primo
anello è del coordinatore** (D1, FASE 0), non dell'analista; e il critic ha usato la regola 6 **per**
spostare Q verso `PASSA`. Una regola che parli solo di analista e critic lascerebbe aperta la porta da cui
il guasto è entrato.

---

## 2. Regola 18 — il cancello chiede il criterio di successo del compito

### 2.1 Dove

Solo `CLAUDE.md`, in una sezione nuova «Le due regole del giro 5 del banco (FIX 17)» (testo completo
della sezione al §4.1). Più la riga del critic al §4.2, che copre insieme 18 e 19.

### 2.2 Testo pronto (è la parte 18 del blocco del §4.1)

```markdown
### 18. Il cancello chiede il criterio di successo del compito, uguale per ogni braccio

Quando la grandezza portante esiste solo per chi raggiunge il criterio di successo (tempo al criterio, prestazione dopo), il cancello della regola 17 chiede a **ogni** braccio il criterio **del compito** — la definizione di successo di `00_problema.md`, con soglia e tetto di censure uguali per tutti i bracci — mai l'obiettivo proprio di un braccio. Un regime che non raggiunge quel criterio non è ammesso, nemmeno se è l'ottimo della ricompensa di quel braccio o la previsione del metodo: lì la grandezza portante non ha un valore ma una censura, e il confronto si ferma (`INCONCLUSIVO — <braccio> non sostiene il criterio di successo del compito, k/N semi`). Per la stessa ragione la guardia di risoluzione (regola 12) vincola ogni braccio che entra nel portante: «non vincolante perché la censura è l'esito previsto» è il caso che deve fermare. Se il compito non fissa un criterio, o se il portante è il raggiungimento stesso, non raggiungerlo è la misura: vale la regola 17 com'è.

**Perché.** Nel caso E′ (`20261017-premio-di-tappa`) G3 era la regola 17 alla lettera — regime finale, bloccante — e ha visto V2 orbitare sulla tappa in 30 semi su 30. Ma ammetteva per V2 il regime `TAPPA`, perché «per V2 "imparare bene" il proprio MDP significa **non** raggiungere il traguardo»; e G4, che sull'IQR nullo di V2 sarebbe scattata, era non vincolante su V2, approvata dal critic come «non `INCONCLUSIVO` per costruzione». Zero guardie scattate, quinto run vero di fila, e un `NON PASSA — T_scorr di V2 maggiore di V1` su un braccio censurato 30/30. Il difetto è passato dalla misura alla regola.
```

**Che cosa avrebbe fatto su E′** [derivato dai criteri congelati e dalle cifre del punteggio]: G3 con
l'insieme ammesso {`TRAGUARDO`} anche su V2 fallisce (0/30 contro la soglia 24/30) al passo 4 della
composizione, e il titolo è uno stop; G4 vincolante su V2 fallisce comunque (IQR $=0$, mediana `C`).
Due guardie scattano sul braccio rotto, ciascuna da sola basterebbe.

### 2.3 Autoconfutazione

**Tesi contraria 1 — «vietare i regimi ammessi diversi dal successo rende impossibile ogni confronto in
cui il braccio sperimentale fallisce legittimamente».** Se l'affermazione è falsa *proprio perché* il
trattamento impedisce di arrivare, la regola trasforma una smentita in un `INCONCLUSIVO`.

*Perché non regge.* La distinzione fra «fallisce come previsto dall'ipotesi» e «è rotto» non sta nel
giudizio su che cosa il braccio ha imparato, sta nella **grandezza che il compito chiede**:
- *fallisce legittimamente* il braccio che ha un valore sulla grandezza del compito, ed è peggiore —
  arriva al criterio più tardi, o lo sostiene su meno semi entro il tetto di censure. Lì il confronto si
  fa, e `NON PASSA` è la risposta;
- *è rotto per questo confronto* il braccio che sulla grandezza del compito **non ha un valore**: se il
  portante è «episodi fino al criterio» e il braccio non sostiene il criterio, il suo valore è una
  censura, e un test fra un valore e una censura misura la censura (è la regola 12, che il giro 4 aveva
  scoperto sul braccio di controllo e che E′ ripete sul braccio sperimentale);
- se invece l'affermazione riguarda *il raggiungimento stesso* (portante = tasso di successo a regime),
  non arrivare **è** la misura e la regola dichiara di non applicarsi (ultima frase del testo).

L'argomento dell'«ottimo del proprio MDP» è esattamente quello che in E′ ha reso indistinguibili il
rotto e il previsto: un braccio che ottimizza un obiettivo diverso da quello del compito ha sempre
«imparato qualcosa». Per questo la regola ancora il cancello a `00_problema.md` e non a `02_metodo.md`.
L'informazione che la tesi contraria vuole salvare («il premio impedisce di arrivare») non va persa: è
il motivo dello stop, e la regola lo ammette nel titolo come qualificatore.

**Tesi contraria 2 — «basta la regola 12 estesa a tutti i bracci (G4 vincolante su V2 avrebbe fermato
E′)».** Vero su E′ [derivato: IQR $=0$ su V2]. Non basta in generale [ipotesi]: un braccio rotto su 20
semi e lento su 10 ha IQR $>0$ e passa la guardia di risoluzione, mentre l'insieme ammesso asimmetrico
resta un buco. Per questo la regola tiene entrambe le cose. *Falsificatore*: un caso del giro 6 in cui
il braccio rotto passa l'insieme ammesso ma la guardia di risoluzione lo ferma da sola mostrerebbe che
la prima metà della regola era superflua — non dannosa.

**Tesi contraria 3 — «un cancello sul criterio del compito diventa un cancello sulla qualità e scambia
un effetto per un guasto».** È il rischio che il punteggio di A′ registra come evitato al giro 5 (§12,
righe 347-351: «il cancello misura l'apprendimento rispetto all'inizio e il regime, non la qualità
assoluta»). La regola si applica solo quando il portante è condizionato al raggiungimento di un
criterio che `00_problema.md` fissa; fuori da lì lascia la regola 17 com'è. *Falsificatore*: nel giro 6
un run su un caso senza criterio di successo del compito (o con portante sulla qualità) si ferma al
cancello citando la regola 18 ⟹ la regola è letta oltre il suo scope e va ristretta.

**Tesi contraria 4 — «la soglia del criterio la sceglie comunque l'analista (in E′ $\theta = 0{,}8$ è
"[derivato + inventato]", `03_criteri.md:31`), quindi l'ancoraggio al compito è finto».** La soglia resta
dell'analista, ma la regola le toglie il grado di libertà che ha prodotto E′: deve essere **la stessa
su ogni braccio**, sulla stessa colonna del log. Un analista che abbassasse la soglia per tutti per far
passare il braccio rotto produrrebbe un criterio che il controllo passa per caso — territorio della
regola 3 e del critic. Buco residuo dichiarato, non chiuso da questa regola.

**Falsificatori nel giro 6** (da trascrivere nella pre-registrazione):
- *inefficace*: il caso sostitutivo E″ arriva a un verdetto sull'ipotesi con zero guardie scattate sul
  braccio che non sostiene il criterio del compito, per un'altra via (insieme ammesso ridefinito con
  altro nome, portante spostato sul raggiungimento senza che l'Enunciato lo chieda);
- *dannosa*: A′ o B′ titolano uno stop del cancello citando la regola 18.

### 2.4 Casi bruciati

**E′**, da cui nasce (già dichiarato bruciato nella riga di sintesi del registro, riga 61). Nessun altro:
la clausola di scope finale è il confine della regola, non una lezione presa da A′ (vedi §8, dubbio 2).

---

## 3. Regola 19 — «non distinguibili» si titola `INCONCLUSIVO`

### 3.1 Dove

Solo `CLAUDE.md` (stessa sezione), più la riga del critic al §4.2.

### 3.2 Testo pronto (è la parte 19 del blocco del §4.1)

```markdown
### 19. «Non distinguibili» si titola `INCONCLUSIVO`, salvo che l'Enunciato chieda l'equivalenza

Se l'intervallo del portante contiene il confine che la domanda pone — la differenza nulla, o la soglia d'effetto dell'Enunciato — il titolo è `INCONCLUSIVO`, mai `PASSA` né `NON PASSA`, anche se l'intervallo sta dentro un margine di equivalenza. Unica eccezione: l'**Enunciato** di `00_problema.md` (le parole dell'utente, non le risposte del coordinatore in FASE 0) chiede l'equivalenza e ne fissa il margine o la fonte. Altrimenti il margine è una scelta di chi scrive i criteri, e spostarlo di poco cambia l'etichetta: il test di equivalenza si riporta come qualificatore dell'`INCONCLUSIVO` («IC ⊂ (−δ, δ), δ senza fonte»), non come risposta. «Non distinguibili» può essere un esito legittimo: il suo nome è il terzo stato. E la regola 6 non è soddisfatta perché `INCONCLUSIVO` è raggiungibile da qualche parte: lo è se lo prende l'esito che non decide.

**Perché.** Nel caso D (`20261017-ucb1-vs-egreedy`), domanda «quale delle due paga meno?», il coordinatore ha ammesso in FASE 0 «non distinguibili» come risposta; l'analista ne ha fatto un test di equivalenza con δ «scelta dell'analista, nessuna fonte»; il critic l'ha spostato da `NON PASSA` a `PASSA`, citando la regola 6. I criteri scrivevano da sé che il confine fra equivalenza e non risolto «dipende da δ più che dai dati». IC [−24,22; 7,72], a cavallo dello zero; titolo `PASSA — equivalenti entro δ = 27,86`, che regge per δ ≥ 26,55: con δ = 25 sarebbe stato `INCONCLUSIVO`. Il corpo sapeva di non sapere; il titolo ha trasformato il «non lo so» in una risposta.
```

**Che cosa avrebbe fatto su D** [derivato]: la regione Q non può titolare `PASSA` (l'Enunciato non chiede
l'equivalenza né fissa $\delta$) né `NON PASSA`; con l'IC che contiene lo zero il titolo è
`INCONCLUSIVO — né direzione risolta …` con il qualificatore «IC ⊂ (−δ, δ), δ senza fonte». Il dato
dell'equivalenza resta nella riga del titolo; cambia lo stato.

### 3.3 Quando un margine è legittimo e quando no

| margine | legittimo per titolare l'equivalenza? | perché |
|---|---|---|
| fissato nell'**Enunciato** (parole dell'utente), o fonte nominata nell'Enunciato | **sì** | l'equivalenza è l'ipotesi del committente; il test la decide |
| scelto dall'analista, anche ancorato a una costante esatta (D: 5 % di `R_explore_th`) | **no** | decide il titolo al posto dei dati: in D $P(Q)$ passa da 0,385 a 0,867 fra $\delta = 20$ e $\delta = 27{,}86$ (`03_criteri.md:237`) |
| deciso dal coordinatore in FASE 0, modalità non presidiata | **no** | `00_problema.md:34` lo dice da sé: è una decisione, non un dato dell'utente; in D è da lì che il guasto è entrato |
| preso da una fonte che l'analista ha trovato | **no** | la scelta della fonte è lo stesso grado di libertà della scelta del numero |

In tutti i casi «no» il test di equivalenza **si può fare e si riporta**: nel titolo come qualificatore,
nel corpo per intero. La regola vieta solo che diventi lo stato.

### 3.4 Autoconfutazione

**Tesi contraria 1 — «un test di equivalenza con margine congelato prima della misura è statistica
standard, non p-hacking (lo scrive il critic, `03b_critica.md:105`); titolarlo `INCONCLUSIVO` butta via
un'informazione vera, $|E[D]| < \delta$».** *Perché non regge*: congelato non vuol dire fondato. Il
p-hacking col margine non sta nel scegliere $\delta$ dopo, sta nel fatto che **$\delta$, non i dati,
decide lo stato** — e il run lo ha misurato da sé (0,385 → 0,867). L'informazione non si butta: resta
nel qualificatore. Ciò che cambia è che lo stato risponde alla domanda posta («quale paga meno?»), e la
risposta a quella domanda, con un IC a cavallo dello zero, è «non lo so».

**Tesi contraria 2 — «un `INCONCLUSIVO` largo diventa la scappatoia che `lab-validatore.md` (righe
126-127) teme: evitare un `NON PASSA` scomodo».** La regola scatta solo quando l'intervallo contiene il
confine della domanda. Quando la direzione è risolta — anche di poco, anche sotto un margine di
rilevanza — si titola la direzione, e il qualificatore «stabilita ma < δ» che D già prevedeva al passo 6
resta lecito. *Falsificatore nel giro 6*: un run con direzione risolta (A′ o B′) titola `INCONCLUSIVO`
citando la regola 19.

**Tesi contraria 3 — «per un'ipotesi direzionale, un IC stretto attorno allo zero è una smentita
legittima: `NON PASSA (nessun effetto)`»**. Lo è solo se l'Enunciato fissa una soglia d'effetto e
l'intervallo la esclude: allora i dati separano gli esiti che la domanda distingue, e la regola non
scatta (il testo nomina «la soglia d'effetto dell'Enunciato» come confine). Se la soglia è dell'analista,
vale lo stesso argomento del margine. Conseguenza dichiarata: la regola cambia il **disegno** di
composizioni come la zona B di B′ (`NON PASSA (nessuna riduzione)` con soglia di rilevanza del 10 %
scelta dall'analista, punteggio B′ righe 269-270 e 302-306). Non brucia B′ (la regola non nasce da lui)
e non tocca il suo esito, che al giro 5 è a direzione risolta (zona C, $k_> = 30/30$).

**Tesi contraria 4 — «in modalità non presidiata nessun Enunciato fisserà mai un margine, quindi
l'eccezione è decorativa».** Probabile [ipotesi], e non è un difetto: è il modo in cui la regola dice
che decidere l'equivalenza spetta al committente. Se un caso futuro la chiede, la scrive nel testo.
*Falsificatore*: un caso con margine nell'Enunciato titolato `INCONCLUSIVO` invece che deciso dal test
⟹ l'eccezione non è stata letta.

**Falsificatori nel giro 6**:
- *inefficace*: D″ titola `PASSA` o `NON PASSA` con un intervallo che contiene il confine della domanda,
  per una via che la regola non nomina (margine scritto dal coordinatore nelle Domande e risposte come se
  fosse dell'utente; «fonte» trovata dall'analista);
- *dannosa*: un caso con direzione risolta titola `INCONCLUSIVO` citando la regola 19.

### 3.5 Casi bruciati

**D**, da cui nasce (già dichiarato bruciato nella riga 61 del registro). Nessun altro.

---

## 4. Il blocco da incollare, e l'unica riga fuori dal `CLAUDE.md`

### 4.1 `CLAUDE.md` del laboratorio

**Bersaglio**: `<workspace>/laboratorio/CLAUDE.md`, **dopo la riga 217** (ultima riga del «Perché» della
regola 17) e **prima della riga 218** (la riga vuota che precede il `---` delle «due regole di igiene»).
**Inserire** (la prima riga del blocco è vuota):

```markdown

---

## Le due regole del giro 5 del banco (FIX 17)

Da due run con misura pulita e diagnosi giusta nel corpo, e un titolo già scritto dai criteri congelati e approvati dal critic: **un esito non risolto con un'etichetta affermativa**, motivata dal fatto che quell'esito era previsto.

[blocco del §2.2 per intero: titolo ### 18, riga vuota, regola, riga vuota, «Perché»]

[blocco del §3.2 per intero: titolo ### 19, riga vuota, regola, riga vuota, «Perché»]
```

Ciascun segnaposto si sostituisce col blocco intero del §2.2 e del §3.2, che sono la versione unica del
testo; fra i due blocchi una riga vuota. Il risultato sono 18 righe: vuota, `---`, vuota, titolo di
sezione, vuota, paragrafo d'apertura, vuota, poi 5 righe per la 18, una vuota, 5 righe per la 19.

### 4.2 Una riga in `lab-critic.md` — raccomandata, e perché è l'unica

**Bersaglio**: `<workspace>/laboratorio/.claude/agents/lab-critic.md`, modalità CRITERI, tabella
«Verifica | Il criterio è difettoso se…», **dopo la riga 45** («Costanti scollegate»), come ultima riga
della tabella. **Inserire:**

```markdown
| **Esito non risolto con etichetta affermativa** | il cancello ammette per un braccio un regime che non raggiunge il criterio di successo del compito, o una guardia di risoluzione è non vincolante su un braccio del portante (regola 18); oppure una riga della composizione titola `PASSA` o `NON PASSA` quando l'intervallo contiene il confine della domanda, o con un margine che l'Enunciato non fissa (regola 19) |
```

**Perché è indispensabile** [misurato sui file]: in **entrambi** i casi l'ultimo controllo prima del
congelamento è stato un'approvazione scritta del critic che rendeva il difetto una virtù — E′
`03b_critica.md:45` («non `INCONCLUSIVO` per costruzione»), D `03b_critica.md:46-57` (R1, che usa la
regola 6 per spostare Q a `PASSA`). Il critic legge il `CLAUDE.md` (cita le regole 6, 12, 17 per numero),
quindi il testo delle regole lo raggiungerebbe comunque; ma la sua tabella di verifiche è dove cerca i
difetti, e oggi la tabella contiene «Potenza: non può **passare**» e nulla che gli chieda se un esito
non risolto è stato reso affermativo. L'asimmetria del suo mandato spinge esattamente nel verso dei due
guasti.

**Alternativa considerata e scartata: due domande meccaniche al CHECKPOINT 2 di `SKILL.md`.** Avrebbe
messo il controllo dove il coordinatore congela. Scartata per due ragioni: (1) in modalità non presidiata
il coordinatore è lo stesso che in D ha scritto D1, quindi il controllo lo farebbe chi ha aperto il
guasto; (2) un rinvio all'analista dopo il secondo giro di critica è un terzo giro, che `SKILL.md` riga 81
e il criterio di stop 2 dei run trasformano in un arresto prima del congelamento. La riga del critic
agisce dentro i due giri.

**Autoconfutazione della riga.** *Tesi*: «è ridondante con le regole 18-19, e il metodo vieta
l'auto-verifica generica». *Risposta*: non è generica — è una riga del controllo avversariale esistente,
con due condizioni nominate e verificabili leggendo `03_criteri.md`, ed è la stessa forma con cui il
FIX 2 mise la potenza nella tabella. *Falsificatore nel giro 6*: E″ o D″ arrivano al congelamento col
difetto e `03b_critica.md` non contiene il rilievo ⟹ la riga è ignorata, e la difesa resta affidata al
solo testo delle regole. Se la sessione principale vuole il minimo assoluto, la riga si omette e FIX 17
è solo `CLAUDE.md`: il conteggio del §7 lo dà in entrambe le forme.

**Nessuna modifica** a `lab-analista.md`, `lab-validatore.md`, `SKILL.md`. In particolare il validatore
**non** deve scavalcare una regola congelata che violi la 19: applica la regola congelata (regola 4) e
il difetto si ferma prima, al critic.

---

## 5. Le lezioni minori: regola o nota

Criterio: una lezione diventa regola solo se (a) è una lezione di sistema e non un rilievo di un run, e
(b) non brucia A′ o B′. Ogni riga sotto con «brucerebbe A′/B′» è **raccomandata come nota** (nei
punteggi esiste già, va ripresa nelle note del giro 6), perché A′ e B′ devono potersi rilanciare come
sono (pre-registrazione §6; riga 61 del registro).

| lezione | caso e fonte | regola esistente che la copre in parte | se diventasse regola | raccomandazione |
|---|---|---|---|---|
| **frasi del titolo più forti del corpo** («previsioni: UCB1 regge, ε-greedy regge/regge» con le due previsioni puntuali mancate) | D, punteggio D righe 396-400 | regole 7 e 14 (il titolo porta i qualificatori; nomina la grandezza misurata) | brucia solo D, già bruciato | **nota**: la 14 la copre se «regge» si legge come metafora di «dentro la banda»; una regola nuova allungherebbe il FIX senza un guasto di verdetto dietro |
| «V2 più lento» per un non-arrivo | E′, punteggio E′ righe 369-378 | regola 18 (il braccio censurato non ha un valore) | — | **assorbita dalla 18** |
| **«ricalcolato» per costanti scritte a mano** (riga 55 del verdetto di A′: $v_\pi$ e $w^*_{TD}$ letterali in `misura.py`) | A′, punteggio A′ righe 292-306 | regola 8 (un canale è indipendente solo fino al livello a cui esistono i log) | **brucerebbe A′** | **nota** |
| **stime laterali senza derivazione** («sd ≈ 10» dello sfruttamento in D; «massimo atteso 0,0240» in A′) | D righe 254-259; A′ righe 188-193 | nessuna; `lab-analista.md` chiede di marcare la stima di forma alternativa | **brucerebbe A′** se cita il suo caso; dal solo D è una regola su un punto che non entra in nessuna soglia | **nota** |
| **dipendenza dalla versione dell'interprete** (`statistics.stdev` differisce di 1 ulp fra 3.10 e 3.14.6) | B′, punteggio B′ righe 404-409 e 328 | nessuna | **brucerebbe B′** | **nota**; nessun effetto sul run (stesso interprete) |
| **costanti [misurato] senza riga di log** | B′, punteggio B′ righe 352-354 e 363-367 | regola 8, nello spirito | **brucerebbe B′** | **nota** |
| buchi di specifica nei criteri congelati (G-ANCH letterale insoddisfacibile; G-ENV numerico o testuale) | A′, punteggio A′ righe 308-314 e 356-359 | regola 16 (schema dei campi letti da un criterio) | **brucerebbe A′** | **nota** |
| divieto al critic di simulare sui semi congelati in modalità CRITERI | A′, punteggio A′ righe 352-355 | nessuna | **brucerebbe A′** | **nota**; è una lezione d'integrità vera, candidata per *dopo* il giro 6 (che chiude il percorso: andrebbe installata dichiarandola non verificata) |
| nominare la «dinamica di riferimento» (E-P1c) | A′, B′, E′, D (punti attaccabili di P1) | — | **brucerebbe A′ e B′** | **nessuna regola**: è la voce `<domanda aperta 7>`, conflitto fra metro e sistema; la raccomandazione (a) in `<open-questions file>` (ratificare la lettura di sostanza nel metro) evita la regola |
| baseline uniforme non citata nel verdetto di E′ | E′, punteggio E′ riga 290 | — | brucia solo E′ | **nota**; rilievo di un run, non di sistema |

**Fuori scope del FIX 17**, perché non sono regole del laboratorio: la proposta di Emendamento 2 al
mandato di punteggio (in tempo 1 leggere `00_problema.md` solo fino al registro dei checkpoint, punteggio
D righe 21-28); il falso positivo «TUTTI CONCLUSI» di `sorveglia.sh` (punteggio E′ righe 431-435); i
rilievi sulle verità (D: come trattare un'equivalenza con margine pre-registrato, percorso vecchio nel
comando di calibrazione; B′: lettura di E-P1c «se l'ipotesi fosse vera»), che vanno a chi manutiene le
verità.

---

## 6. Casi bruciati

| regola | nasce da | brucia | già nel registro? |
|---|---|---|---|
| 18 | E′ | **E′** | sì, riga 61 («E′ e D bruciati … sostituti E″ e D″») |
| 19 | D | **D** | sì, riga 61 |
| riga del critic (§4.2) | E′ e D | E′, D | — (nessun caso in più) |
| lezioni minori | — | **nessuno**, perché restano note | — |

**A′ e B′ non bruciati**, a due condizioni: nessuna delle note del §5 diventa regola, e `<domanda aperta 7>` si
chiude senza una regola nel laboratorio. Le regole 18 e 19 possono cambiare il **disegno** dei criteri di
A′ e B′ al giro 6 (§2.3 tesi 3, §3.4 tesi 3): è ciò che il giro 6 deve misurare, non un consumo del
caso.

---

## 7. Inventario: regola → lezione → caso → file e riga

| regola | lezione | caso | dove è documentata |
|---|---|---|---|
| 18 | il regime in cui il braccio sperimentale non raggiunge il criterio del compito era ammesso | E′ | `laboratorio-giro5-E1/run/20261017-premio-di-tappa/03_criteri.md:90-92`; `02_metodo.md:165`; `03b_critica.md:45`; punteggio E′ righe 112-143, 187-193, 407-413, 442-446; registro riga 49 (caso), 61 (sintesi) |
| 18 | la guardia di risoluzione che avrebbe visto era non vincolante sul braccio sperimentale | E′ | `03_criteri.md:96-99`, `:135-136`; `03b_critica.md:46`; punteggio E′ righe 126-129, 187-189 |
| 19 | «non distinguibili» ammesso come risposta dal coordinatore | D | `laboratorio-giro5-D/run/20261017-ucb1-vs-egreedy/00_problema.md:34`, `:38`; Enunciato `:9` |
| 19 | margine di equivalenza senza fonte che decide il titolo | D | `03_criteri.md:226-238`; punteggio D righe 143-148, 190-194, 321-325 |
| 19 | il critic sposta Q da `NON PASSA` a `PASSA`, con la regola 6 letta come «basta che esista» | D | `03b_critica.md:46-78`; `03_criteri.md:361-369`; punteggio D righe 311-319; registro riga 53 (caso), 61 (sintesi) |
| riga del critic | in entrambi i casi l'approvazione del critic ha reso il difetto una virtù | E′, D | E′ `03b_critica.md:45-46`; D `03b_critica.md:46-57` |

I percorsi dei run sono relativi a `<workspace>/`; i punteggi sono
`giri/2026-10-17-punteggio-giro5-{E-primo-premio-di-tappa,D-orizzonte-finito}.md`.

---

## 8. Conteggio righe [misurato con `wc` sul testo del §4]

| file | oggi | dopo FIX 17 | delta |
|---|---|---|---|
| `CLAUDE.md` del laboratorio | 236 righe · 3 100 parole | 254 righe · ~3 700 parole | **+18 righe, +596 parole (+19 % in parole)** |
| `lab-critic.md` (se si adotta il §4.2) | 181 righe | 182 righe | +1 riga (~80 parole) |

Le righe ingannano: nel `CLAUDE.md` ogni paragrafo è una riga sola. Il peso vero sono le parole: i due
testi valgono quasi quanto le sei regole del FIX 16 (659 parole, righe 185-217). Per questo il FIX 17
resta a **due regole**, sotto il tetto di tre o quattro del mandato, e tutto il resto va in nota (§5).
Se si vuole accorciare ancora, il primo taglio è l'ultima frase della 19 (la lettura della regola 6, −35
parole circa), che il «Perché» già racconta.

---

## 9. Che cosa NON si tocca qui: il metro

`punteggio.md` si emenda fuori dai giri e lo decide l'utente (voce `<domanda aperta 7>`, `RISPOSTA:` vuota al
2026-10-17). Il FIX 17 **non tocca**:

1. **P1** con E-P1, **E-P1b** (inerzia dichiarata) ed **E-P1c** (potenza ≥ 0,50 sotto la dinamica di
   riferimento, identificazione obbligatoria «dal giro 5») — è l'oggetto di `<domanda aperta 7>`;
2. **P2** (cancello su tutti i bracci prima di qualunque effetto) e la sua specializzazione per i casi a
   braccio rotto nelle pre-registrazioni;
3. **P3** e la riga «P3 misura la provenienza, non la verità»;
4. **P4** e le sue letture strette registrate nei punteggi (frasi del titolo, marcatura [misurato]);
5. «Il caso C pesa doppio su P2»;
6. la **Storia del metro** e i ripunteggi retroattivi;
7. «Come si legge il risultato», compreso il profilo **oracolo caduto**;
8. il metodo dell'**attenzione umana** e il formato della riga del registro.

Le regole 18-19 cambiano il sistema sotto test, non il metro: nessun ripunteggio retroattivo deriva da
questa proposta.

---

## 10. Installazione e «fatto quando»

1. La sessione principale decide il testo (due regole, con o senza la riga del critic) e lo incolla nei
   bersagli dei §4.1 e §4.2, in un commit del laboratorio dedicato e senza altro dentro.
2. **Fatto quando**: `grep -n '^### 1[89]\.' <workspace>/laboratorio/CLAUDE.md` restituisce due righe;
   `wc -l` dà 254 (e 182 su `lab-critic.md`, se adottata); `git diff --stat` del commit tocca solo quei
   file; la nuova istantanea `giro6` li contiene e `verifica-sistema.sh` la confronta.
3. I falsificatori dei §2.3, §3.4 e §4.2 si trascrivono nella pre-registrazione del giro 6 **prima** dei
   lanci, accanto alla regola §3.2 adattata.

---

## 11. Dubbi aperti

1. **Notazione.** Il mandato chiede lo stile delle regole 12-17, che nel `CLAUDE.md` del laboratorio
   usano Unicode e backtick (`IQR > 0`, `Q₀ = 1`), non LaTeX. I blocchi da incollare seguono il file di
   destinazione; la prosa di questa proposta usa LaTeX, come vuole la regola globale per i `.md`. Se la
   sessione principale preferisce LaTeX anche nel `CLAUDE.md`, va deciso per tutto il file, non per due
   regole.
2. **La clausola di scope della 18** («se il compito non fissa un criterio, o se il portante è il
   raggiungimento stesso … vale la regola 17 com'è») protegge un disegno come quello di A′ dal falso
   stop. L'ho scritta come confine logico della regola, non come lezione di A′, e per questo non conto
   A′ fra i bruciati. Se la sessione principale la legge come nata da A′, le strade sono due: toglierla
   (la regola resta corretta su E′ ma il rischio di falso stop cresce) o accettare A′ bruciato. Io
   raccomando di tenerla e non bruciare A′.
3. **Chi disegna E″ e D″** dovrebbe conoscere il testo del FIX 17, per non costruire casi che le regole
   risolvono alla lettera (un E″ con lo stesso insieme ammesso asimmetrico, un D″ con lo stesso margine
   dell'analista misurerebbero la memoria, non la regola). Non è materia del FIX, ma condiziona quanto il
   giro 6 dirà sulle regole 18-19.
4. **Il primo anello di D è del coordinatore** (D1 in FASE 0). La regola 19 lo nomina; la riga del
   critic lo coglie solo a valle, sui criteri. Se nel giro 6 il guasto rientrasse dalla FASE 0 in una
   forma che il critic non vede, l'unico rimedio rimasto sarebbe una riga in `SKILL.md` alla FASE 0 —
   scartata qui per tenere il FIX corto (§4.2).

<!-- FINE DOCUMENTO -->
