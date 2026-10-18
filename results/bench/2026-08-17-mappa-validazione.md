# Mappa di validazione del laboratorio

Scritta il 2026-08-17, dopo il punteggio del giro 3. Risponde a una domanda sola:
**che cosa manca perché ci si possa fidare del laboratorio su una domanda di cui non si conosce la risposta.**

Non è un punteggio. È l'inventario di quali capacità sono state **viste funzionare**, con quale prova, su quale
versione del sistema — e quali sono solo **installate**.

---

## 1. La distinzione che regge tutto

Il `CLAUDE.md` del laboratorio la enuncia in una riga: «*Ogni difesa va vista fallire almeno una volta,
altrimenti non è stata verificata, è stata installata*». E, più avanti: «*Un documento che nessuno rilegge è
una difesa installata, non verificata*».

Il banco esiste per convertire *installata* in *verificata*. Una capacità è verificata quando l'abbiamo vista
esercitata su dati veri, in un regime in cui avrebbe potuto sbagliare, con la risposta giusta nota in anticipo.
Tutto il resto è previsione — e il giro 3 ha appena dimostrato quanto vale una previsione.

---

## 2. Il rilievo che cambia la lettura del giro 3

**Al primo passaggio ho sottovalutato ciò che il giro 3 ha dimostrato.** Il punteggio non cambia — il verdetto
resta non attribuibile, perché un oracolo caduto non può assegnare punti — ma l'**evidenza sul laboratorio**,
ricostruita dagli interni del run invece che dall'oracolo, è più forte di «coincidenza».

Ecco il fatto, verificabile riga per riga in `05_verdetto.md` §4 e nella tabella di Parte VI di `03_criteri.md`:

- Il run è finito con **C1 = NULLO** (nessuna differenza rilevabile, `p` = 0,870) e **C2 = SOTTO-TAGLIA**.
- Quella combinazione **è letteralmente la riga `NON PASSA`** della tabella congelata: «*`NON PASSA` — nessuna
  differenza rilevabile fra 8 e 1 labirinti*».
- L'unica cosa che ha impedito quel titolo è stata **G6 che ha fallito**: l'intervallo bootstrap della mediana
  è risultato 3,1 volte più largo di `delta_min` per lato, quindi il run non poteva *escludere* l'effetto.
- Con G6 fallita e C1 = NULLO, la procedura instrada a `INCONCLUSIVO` invece che a `NON PASSA` — ed è
  esattamente la regola scritta per non ripetere il 2026-08-02.

**Cioè: il profilo che il 2026-08-02 produsse un `NON PASSA` sbagliato si è ripresentato tale e quale, e la
difesa nuova l'ha intercettato.** Non per fortuna: G6 ha fallito per la ragione sostanziale (dispersione troppo
grande per risolvere) e la sua rete anti-degenerazione, il ramo (b), correttamente **non** è scattata
(23 semi non nulli su una soglia di 10). Se fosse scattata quella, sarebbe stato il difetto `a ≤ b + δ` con
entrambi a zero — il guasto originale.

E `INCONCLUSIVO` è la risposta **giusta nel merito**, indipendentemente da cosa si aspettasse la verità
sigillata: il run non ha rilevato un effetto e non è riuscito a escluderlo. Non rilevato e non escluso è la
definizione di inconcludente.

**Conclusione onesta: il terzo stato del verdetto è verificato.** Non nel modo che il caso C prevedeva, e non
sulla difesa che il caso C voleva far scattare — ma verificato. Questo è il singolo risultato più importante
del giro 3, e nel punteggio non si vedeva perché il punteggio guarda l'oracolo.

---

## 3. Inventario: che cosa è verificato, con quale prova, su quale sistema

Il sistema non è solo il testo delle definizioni: è quel testo su una certa versione del laboratorio. Le
colonne «quando» e «su quale sistema» non sono burocrazia — sono la ragione per cui la riga finale di questa
tabella è quella che conta.

| Capacità | Prova | Quando | Sistema | Stato |
|---|---|---|---|---|
| Titola `PASSA` quando deve | caso A, giro 2 | 2026-08-09/10 | **FIX 1-8** (`a7b22b1`) | ✅ e ha chiuso il falso negativo del giro 1 |
| Titola `NON PASSA` quando deve | caso B, giro 2 | 2026-08-10 | **FIX 1-8** | ✅ |
| Titola `INCONCLUSIVO` quando deve | caso C, giro 3 — **per ricostruzione**, §2 | 2026-08-17 | **FIX 9-15** (`fc7f812`) | ✅ ma non dall'oracolo |
| Congela i criteri prima di implementare | `git log`, ogni run | sempre | tutti | ✅ 3 run su 3, verificabile meccanicamente |
| Il validatore si accorge di un'implementazione rotta | T2 | 2026-08-02 | **pre-FIX** | ⚠️ verificata su un sistema di 15 fix fa |
| Il controverdetto rileva il cherry-picking | T3 | 2026-08-02 | **pre-FIX** | ⚠️ idem |
| Il critic respinge criteri non falsificabili | T1 | 2026-08-02 | **pre-FIX** | ⚠️ idem — 3 difetti su 3 diagnosticati per nome |
| Il critic **non** respinge criteri validi | T1c | 2026-08-02 | **pre-FIX** | ⚠️ idem, e solo dopo un falso positivo accertato |
| **Una guardia ferma il run** | — | mai | — | ❌ **mai vista scattare** |
| Scaling degli scout (1 su problema banale) | — | mai | — | ❌ mai provato |

### Le due righe rosse, spiegate

**Una guardia che ferma il run.** In tre run veri nessuna guardia ha mai bloccato niente. Al giro 3 G3 è stata
calcolata su entrambi i bracci, con la soglia giusta, al punto giusto della procedura — e ha **passato**.
Sappiamo che la guardia esiste, che è congelata prima dell'implementazione e che produce il numero. Non
sappiamo se, quando il numero dice no, il laboratorio si ferma davvero invece di proseguire. È precisamente il
guasto del 2026-08-02, ed è ancora installato e non verificato.

**Lo scaling degli scout** è il quarto punto della lista «Verifica del laboratorio stesso» del `CLAUDE.md` del
laboratorio, e l'unico dei quattro mai eseguito. Vale poco per la correttezza e molto per il costo: un
laboratorio che lancia 4 scout su una domanda facile brucia quota inutilmente ogni volta che lo usi.

### La riga che conta più di tutte

**Nessuna singola versione del laboratorio ha mai superato tutti e tre gli stati del verdetto.**

- `PASSA` e `NON PASSA` sono verificati sul sistema **FIX 1-8**.
- `INCONCLUSIVO` è verificato sul sistema **FIX 9-15**, che è quello di oggi.
- FIX 9-15 ha aggiunto cinque regole. Sono additive e riguardano aggregazione, dichiarazione di potenza e
  guardie simmetriche: è **plausibile** che A e B passino ancora. Plausibile non è verificato, ed è la stessa
  parola che ha appena fatto cadere il caso C.

La regola è già scritta nel README del banco: «*Non modificare il laboratorio fra due casi dello stesso giro.
Se lo fai, i tre punteggi appartengono a tre sistemi diversi e non si sommano*». È esattamente la situazione
in cui siamo, un giro alla volta invece che dentro un giro.

---

## 4. Perché «correggo e non rilancio» non porta dove vuoi

L'alternativa era: *individuato il difetto, lo correggo, e non serve rieseguire perché so come andrebbe.*
Non regge, per tre ragioni, in ordine di forza.

**1. Il giro 3 è la confutazione, ed è appena successo.** La verità sigillata del caso C non era un'opinione:
era un ragionamento derivato, scritto in anticipo, sicuro di sé — «*il braccio sperimentale non impara nulla,
la sua tabella Q resta quasi ovunque a zero e la politica risultante è indistinguibile da una casuale*».
Era **sbagliata**, e l'ha stabilito la misura. Nel frattempo il laboratorio aveva scritto la previsione opposta
(0,996–0,999 che entrambi i bracci imparassero) e aveva ragione lui. Se «so come andrebbe» fosse un metodo
valido, avresti registrato 1/1 su un caso rotto e ti saresti fidato di un oracolo morto.

**2. Ciò che vuoi trasferire è proprio la parte non prevedibile.** Quando userai il laboratorio sulla tua
ricerca non avrai una verità sigillata: sarà il caso in cui *il laboratorio ha sbagliato* e *quella domanda era
difficile* si sentono identici da dentro. L'unica evidenza che si trasferisce è statistica: «questa macchina si
è comportata correttamente in N regimi indipendenti, compresi quelli costruiti per farla sbagliare». Una
correzione non rieseguita non aggiunge un solo N.

**3. La correzione più importante che il giro 3 ha prodotto non è nel laboratorio, è nel banco.** Il difetto
scoperto è dell'**oracolo**, non del sistema: la verità di C dipendeva da parametri che il caso lasciava
liberi (densità dei muri, orizzonte, iperparametri, codifica dello stato), quindi la sua premessa era vera solo
per certe scelte dell'analista. Correggere quello e non rilanciare significa correggere il metro e non
rimisurare niente.

---

## 5. Il piano

Tre passi. Il primo è l'unico che richiede quota; gli altri due sono lavoro a tavolino.

### Passo 1 — Giro 4: il banco intero su un sistema solo, senza toccare il laboratorio

Quattro casi, **nessuna modifica al laboratorio dal primo all'ultimo**, così i punteggi si sommano e il giro è
confrontabile.

| Caso | Che cosa chiude | Perché adesso |
|---|---|---|
| **E** | *«una guardia ferma il run»* — la riga rossa | La rottura è nella **specifica** (γ = 0,5 rende il compito non ottimale per la variante 2): il braccio è rotto in silenzio e le guardie simmetriche **devono** fermare il confronto. È la replica diretta del 2026-08-02, calibrata e pronta |
| **D** | Il terzo stato in regime di **parità genuina** | Verifica `INCONCLUSIVO` dove la tentazione è concludere una direzione, non dove il run è degenere. È il complemento di ciò che il giro 3 ha mostrato, non un doppione: calibrato a parità (`c = 236`, divario misurato +0,0) |
| **A** | Conferma `PASSA` sul sistema **attuale** | Verificato solo su FIX 1-8. È il caso che scopre i falsi negativi, e i falsi negativi non emergono mai dai run veri |
| **B** | Conferma `NON PASSA` sul sistema **attuale** | Stessa ragione |

**Se la quota non basta per quattro, l'ordine di priorità è E, D, A, B** — E e D coprono ciò che non è mai
stato verificato, A e B confermano ciò che è stato verificato su un sistema precedente.

D ed E hanno entrambi una **condizione di invalidazione dichiarata in anticipo** su grandezze che il run misura
comunque, nello stile `<domanda aperta 1>`. **Va eseguita come primo gesto anche per loro**, prima di guardare il
verdetto: è la disciplina che al giro 3 ha impedito di regalare un punto. Per D è «divario > 3·SE con la stessa
direzione su entrambe le metà dei semi»; per E la verità dichiara le proprie soglie attese.

### Passo 2 — Ricostruire il caso C, ma dopo, e diversamente da come dice la sua verità

La verità prescrive «abbassa il budget da 200 a 80 passi». **Non basta, e va detto perché.** Il caso non è
caduto perché 200 fosse troppo: è caduto perché **la sua verità dipendeva da parametri che il caso non fissa**.
Il testo consegnato al laboratorio dice «muri generati a caso» senza densità, non dice l'orizzonte
dell'episodio, non dice gli iperparametri e lascia libera la codifica dello stato. Con `P_MURO = 0,25`,
`T = 25` e stato = cella assoluta il veleno non morde; con altre scelte morderebbe. Abbassare il budget e
lasciare libero il resto ricostruisce lo stesso difetto a un'altra scala.

Ci sono due strade, e **la scelta è tua** perché cambia cosa si sta misurando:

- **(i) Fissare nel testo del caso** la densità dei muri e l'orizzonte, lasciando liberi solo gli iperparametri.
  Il veleno diventa calcolabile e la verità torna un oracolo. Costo: il laboratorio ha meno libertà, quindi il
  caso misura meno «sa progettare un esperimento» e più «sa riconoscere una domanda senza risposta».
- **(ii) Tenere il testo com'è** e riscrivere la verità in forma **condizionale**: «il veleno morde se e solo
  se [condizione misurabile sui log]», col controllo di invalidazione promosso da nota a strumento primario.
  Il caso resta realistico ma smette di essere un oracolo secco: punteggia il percorso sempre, il verdetto solo
  quando la condizione è soddisfatta.

Preparo io la ricostruzione e lo script di calibrazione — da eseguire **tu**, come per D ed E — appena mi dici
quale delle due.

### Passo 3 — Due riparazioni piccole, prima del lancio

- **Il rilevatore di completamento di `sorveglia.sh`**: al giro 3 ha rilanciato sei volte un run già finito e
  ha emesso un `TETTO RILANCI` falso. Non ha contaminato nulla (nessuno di quei rilanci ha prodotto commit) ma
  brucia quota, e con quattro casi la brucerebbe quattro volte.
- **La prova di scaling degli scout**, che è a costo quasi zero: una domanda banale, si guarda quanti scout
  lancia. Chiude l'ultima riga rossa senza consumare un giro.

---

## 6. Quando potrai fidarti, e di che cosa esattamente

Alla fine del giro 4, se va come deve, potrai dire questa frase e sostenerla con i file:

> Su **una sola versione del laboratorio**, il sistema ha titolato `PASSA` su un caso che doveva passare,
> `NON PASSA` su uno che doveva non passare, `INCONCLUSIVO` su uno in cui la risposta giusta è «non lo so»,
> e **si è fermato** su un caso in cui un braccio era rotto in silenzio. In tre casi su quattro conosceva la
> risposta solo l'oracolo, mai lui.

Questo è ciò che oggi non puoi dire, e la sola cosa che ti separa dal dirlo è eseguire quattro casi.

**Ciò che non potrai dire nemmeno allora**, e va scritto adesso perché non te lo racconti dopo:

- Il banco copre **problemi piccoli e sintetici**, secondi di calcolo, verità in forma chiusa o costruita. Non
  dice nulla su un problema di ricerca vero con dati veri e giorni di calcolo.
- Le quattro prove strutturali (T1–T3 più lo scaling) restano verificate su un sistema di 15 fix fa, salvo
  rieseguirle.
- Il banco misura il **processo**, non la fisica. `P3` misura la provenienza dei numeri, non la loro verità:
  una derivazione sbagliata ma dichiarata passa per costruzione, e il banco non la vede.
- Un caso «superato tre giri di fila senza mai essere vicino a sbagliare» smette di discriminare, e va
  sostituito. Vale già per A e B: al giro 4 sarebbero al secondo.

Fidarsi ciecamente non è lo stato finale. Lo stato finale è: **so su quali fronti è stato messo alla prova, su
quali no, e quanto è vecchia ogni prova.** Questa tabella è quel documento, e va aggiornata a ogni giro.

---

# Errata — 2026-08-17, stesso giorno, prima del giro 4

**La riga «Nessuna singola versione del laboratorio ha mai superato tutti e tre gli stati del verdetto»
(§3) è FALSA ed è ritirata.** Era la conclusione più pesante del documento e va corretta per prima.

L'errore nasceva da uno strumento, non da un ragionamento. Un coordinatore gira con `cd $REPO` e legge
`$REPO/CLAUDE.md`, la copia dentro il repo del giro; `stacca.sh` gli vieta esplicitamente di aprire
`<workspace>/laboratorio`. Ma `verifica-sistema.sh` confrontava proprio quel file vivo. Misurato:

| repo | caso | sha256 `CLAUDE.md` (16) | commit |
|---|---|---|---|
| `<workspace>/laboratorio-giro-fix-A` | A, giro 2 | `4077898048dfeb20` | `a7b22b1` — FIX 1-8 |
| `<workspace>/laboratorio-giro-fix` | B, giro 2 | `4077898048dfeb20` | FIX 1-8 |
| `<workspace>/laboratorio-giro-fix-C` | C, giro 3 | `4077898048dfeb20` | FIX 1-8 |
| `<workspace>/laboratorio` (vivo) | nessuno | `ae991de6c1c59a2c` | `fc7f812` — FIX 9-15 |

**A, B e C hanno girato sullo stesso identico sistema**, e le sei definizioni di `~/.claude` erano
invariate su entrambi i giri. Quindi una sola versione del laboratorio **ha** superato tutti e tre gli
stati: `PASSA` su A, `NON PASSA` su B, `INCONCLUSIVO` su C. Il laboratorio è più avanti di quanto §3
dicesse.

Il rovescio: **FIX 9-15 non è mai stato eseguito**. Le cinque regole nate dal giro 2 sono installate e
non verificate, e il giro 4 sarà il primo a eseguirle.

**Seconda correzione, sul piano di §5.** Il piano proponeva giro 4 = E, D, A, B. **A e B non si possono
rilanciare**: il `CLAUDE.md` attuale li nomina per slug e racconta cosa è andato storto in ciascuno
(righe 123, 149, 155, 161, 167, 173, 179). Non sarebbero test ciechi. D ed E non compaiono da nessuna
parte e restano gli unici due casi ancora ciechi.

**Regola nuova che ne segue**: quando una regola del laboratorio nasce da un caso, quel caso è consumato
e va sostituito. Vale per A e B, che servono rimpiazzati da A' e B' negli stessi ruoli.

**Riparazioni applicate** lo stesso giorno: `verifica-sistema.sh` accetta il repo del run come secondo
argomento e stampa sempre quale `CLAUDE.md` ha confrontato; `stacca.sh` glielo passa in pre-volo e a
fine run; `sorveglia.sh` controlla la deriva per caso. Controprova: `INVARIATO` sui repo del giro 4,
`DERIVATO` sul repo del giro 3 — la deriva che prima era invisibile.

Giro 4 pre-registrato, con le regole di accettazione congelate prima della misura:
`giri/2026-08-17-preregistrazione-giro4.md`.
