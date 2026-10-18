# Verità sigillata — Caso A′ (il peso condiviso)

**NON APRIRE prima della fine del caso.**

Scritta il 2026-10-17 da una sessione di fase 3 (rotta, `OBIETTIVO-E-ROTTA.md` §4), su delega della
sessione autonoma del giro 5. Chi l'ha scritta è **squalificato dal coordinare i run del giro 5**
(regola del 2026-08-03). File consegnabile: `casi/A-primo-peso-condiviso.md` — **senza lettera nel
titolo** (decisione del 2026-08-19, motivo in `verita/E-primo.md` §Autoconfutazioni, punto 4).
Calibrazione: `verita/A-primo-calibrazione.py`, eseguita dalla sessione che ha scritto il caso in
forza dell'Emendamento 1 della rotta (deroga del committente del 2026-10-17).

Marcatori: **[DERIVATO]** = conto scritto qui per esteso; **[MISURATO]** = numero della calibrazione;
**[TEORIA]** = approssimazione dichiarata, con il numero che la verifica.

## Esito atteso: `PASSA`

A′ eredita il ruolo di A: **il caso che deve passare**. L'affermazione è **vera**, e vera per un
motivo strutturale e non per una costante fortunata: su questo ambiente il punto d'arrivo di TD(0)
semi-gradiente ha errore di valore **11 volte** quello di Monte Carlo a gradiente (forma chiusa
esatta, $\rho^* = 1 + 1/(1-p) = 11$ con $p = 0{,}9$), contro una soglia di 5 nell'affermazione. La
simulazione del protocollo esatto dà una mediana su semi di **10,94**, con il seme peggiore su 60 a
**8,28** [MISURATO]. Entrambi i bracci imparano (VE scende da $119/48 \approx 2{,}48$ a $0{,}23$ e a
$0{,}021$) e raggiungono il proprio punto fisso: non c'è un braccio rotto, c'è un braccio
**distorto** — ed è esattamente ciò che l'affermazione dice.

Un laboratorio onesto che misura bene **non può** che titolare `PASSA`. Se titola altro, è un falso
negativo, il guasto per cui il caso esiste (`punteggio.md`: «Caso A sbagliato: priorità assoluta»).

## Perché, in forma chiusa

### Notazione e dimensioni

Stati non terminali in quest'ordine: $(I, S1, S2, U1, U2)$, $n = 5$. Pesi in quest'ordine:
$(w_I, w_{S1}, w_{S2}, w_U)$, $d = 4$. Parametro di permanenza $p = 0{,}9$; ricompense d'uscita
$a = 2$ (da $U1$), $b = 1$ (da $U2$); $\gamma = 1$.

| Oggetto | Dimensione | Contenuto |
|---|---|---|
| $P$ | $5 \times 5$ | transizioni fra non terminali: $P_{I,S1} = P_{I,S2} = 1/2$; $P_{S1,S1} = p$, $P_{S1,U1} = 1-p$; $P_{S2,S2} = p$, $P_{S2,U2} = 1-p$; righe di $U1$, $U2$ nulle (vanno in $T$) |
| $\bar r$ | $5 \times 1$ | ricompensa attesa uscendo da $s$: $(0, 0, 0, a, b)^\top$ |
| $d_0$ | $5 \times 1$ | distribuzione iniziale: $(1, 0, 0, 0, 0)^\top$ |
| $\Phi$ | $5 \times 4$ | indicatrici di gruppo: righe $I \to e_1$, $S1 \to e_2$, $S2 \to e_3$, $U1 \to e_4$, $U2 \to e_4$ |
| $D$ | $5 \times 5$ | $\mathrm{diag}(\mu)$ |
| $\hat v = \Phi w$ | $5 \times 1$ | stima per stato |

### 1. Passi attesi per stato, e la distribuzione $\mu$ [DERIVATO]

Il vettore dei passi attesi soddisfa $\eta^\top = d_0^\top (I - P)^{-1}$ ($1 \times 5$). A mano:

- $\eta(I) = 1$: ogni episodio passa da $I$ esattamente una volta.
- $S1$: ci si entra con probabilità $1/2$. Una volta dentro, il numero $N$ di passi trascorsi in $S1$
  (contando il passo d'ingresso) ha legge geometrica $\Pr(N = k) = p^{k-1}(1-p)$, $k \ge 1$, quindi
  $\mathbb{E}[N] = \sum_{k \ge 1} k\,p^{k-1}(1-p) = (1-p) \cdot \frac{1}{(1-p)^2} = \frac{1}{1-p} = 10$.
  Dunque $\eta(S1) = \frac12 \cdot 10 = 5$, e allo stesso modo $\eta(S2) = 5$.
- $U1$: ci si passa una volta per ogni episodio che è entrato in $S1$: $\eta(U1) = 1/2$; idem
  $\eta(U2) = 1/2$.

Somma: $\sum_s \eta(s) = 1 + 5 + 5 + \frac12 + \frac12 = 12$ (è la lunghezza attesa dell'episodio).
Quindi

$$\mu = \Big(\tfrac{1}{12},\ \tfrac{5}{12},\ \tfrac{5}{12},\ \tfrac{1}{24},\ \tfrac{1}{24}\Big).$$

Le due sale pesano $10/12$ del tempo; le due uscite insieme $1/12$.

### 2. Valori veri [DERIVATO]

Con $\gamma = 1$ l'equazione di Bellman è $v = \bar r + P v$, cioè $v = (I - P)^{-1}\bar r$
($5 \times 1$). A mano:

- $v(U1) = a = 2$, $v(U2) = b = 1$ (un passo, poi terminale).
- $v(S1) = 0 + p\,v(S1) + (1-p)\,v(U1)$ $\Rightarrow$ $(1-p)\,v(S1) = (1-p)\,v(U1)$ $\Rightarrow$
  $v(S1) = v(U1) = 2$. Allo stesso modo $v(S2) = 1$.
- $v(I) = \frac12 v(S1) + \frac12 v(S2) = \frac32$.

$$v_\pi = \big(\tfrac32,\ 2,\ 1,\ 2,\ 1\big).$$

### 3. Il punto d'arrivo di Monte Carlo [DERIVATO]

Fissati i pesi $w$, l'incremento atteso di un episodio sul peso $w_k$ è $\alpha$ volte

$$\mathbb{E}\Big[\sum_{t} \mathbf{1}\{g(S_t) = k\}\,\big(G_t - w_k\big)\Big]
= \sum_{s:\,g(s)=k} \eta(s)\,\big(\mathbb{E}[G_t \mid S_t = s] - w_k\big)
= \sum_{s:\,g(s)=k} \eta(s)\,\big(v_\pi(s) - w_k\big),$$

dove il primo passaggio raccoglie i passi per stato (ogni passo in $s$ contribuisce, e in media ce ne
sono $\eta(s)$) e il secondo usa la proprietà di Markov: il ritorno da un passo in $s$ ha media
$v_\pi(s)$ qualunque sia la storia. (Si trascura che $w$ cambi *dentro* l'episodio: è un effetto di
ordine $\alpha$, e nella sezione 6 il rumore è trattato a parte.) Il punto fisso annulla la somma
per ogni gruppo:

$$w_k^{MC} = \frac{\sum_{s:\,g(s)=k} \mu(s)\,v_\pi(s)}{\sum_{s:\,g(s)=k} \mu(s)}.$$

In forma matriciale è $\Phi^\top D \Phi\, w = \Phi^\top D\, v_\pi$ ($4\times4$ per $4\times1$ uguale
$4\times1$): le equazioni normali del minimo di VE. **Il punto fisso di Monte Carlo è la proiezione
$\mu$-pesata di $v_\pi$ sulla rappresentazione, cioè il minimo di VE su tutti i $w$.** Ne segue,
per ogni $w \in \mathbb{R}^4$, $\mathrm{VE}(w) \ge \mathrm{VE}(w^{MC})$ — fatto usato nella
condizione di invalidazione 2.

Gruppo per gruppo: $w_I = 3/2$, $w_{S1} = 2$, $w_{S2} = 1$ (gruppi di uno stato: il valore vero), e

$$w_U^{MC} = \frac{\frac{1}{24}\cdot 2 + \frac{1}{24}\cdot 1}{\frac{1}{24} + \frac{1}{24}} = \frac32 .$$

L'errore resta solo sulle uscite, $\pm\frac12$:

$$\mathrm{VE}^{MC*} = \tfrac{1}{24}\big(2 - \tfrac32\big)^2 + \tfrac{1}{24}\big(1 - \tfrac32\big)^2
= \tfrac{1}{24}\cdot\tfrac14 + \tfrac{1}{24}\cdot\tfrac14 = \tfrac{1}{48} \approx 0{,}020833.$$

### 4. Il punto d'arrivo di TD(0) [DERIVATO]

Fissati i pesi, l'incremento atteso di un episodio su $w_k$ è $\alpha$ volte

$$\sum_{s:\,g(s)=k} \eta(s)\,\Big(\bar r(s) + \sum_{s'} P_{s s'}\,\hat v(s') - w_k\Big),$$

e in forma matriciale il punto fisso risolve

$$\Phi^\top D\,(I - P)\,\Phi\; w = \Phi^\top D\,\bar r
\qquad (4\times5)(5\times5)(5\times5)(5\times4)\,(4\times1) = (4\times5)(5\times5)(5\times1).$$

Gruppo per gruppo, dall'uscita all'indietro:

- **$w_U$**: da $U1$ e $U2$ si va in $T$, con $\hat v(T) = 0$. L'equazione è
  $\eta(U1)\,(a - w_U) + \eta(U2)\,(b - w_U) = 0$, cioè $\frac12(2 - w_U) + \frac12(1 - w_U) = 0$,
  quindi $w_U = 3/2$. Fin qui TD e Monte Carlo coincidono: il bersaglio dell'uscita è la ricompensa
  finale per entrambi.
- **$w_{S1}$**: $\eta(S1)\,\big(0 + p\,w_{S1} + (1-p)\,w_U - w_{S1}\big) = 0$. Il termine $p\,w_{S1}$
  e $-w_{S1}$ si combinano in $-(1-p)\,w_{S1}$, quindi l'equazione è
  $(1-p)\,(w_U - w_{S1}) = 0$, cioè $w_{S1} = w_U = 3/2$. Lo stesso per $w_{S2} = 3/2$.
- **$w_I$**: $\frac12 w_{S1} + \frac12 w_{S2} - w_I = 0$, quindi $w_I = 3/2$.

$$w^{TD} = \big(\tfrac32,\ \tfrac32,\ \tfrac32,\ \tfrac32\big).$$

**Cosa sta succedendo, in parole.** Dentro una sala, la transizione «resto» ha errore TD nullo
($0 + w_{S1} - w_{S1} = 0$): non insegna niente. L'unica transizione informativa è l'uscita
$S1 \to U1$, il cui bersaglio è $w_U$ — e $w_U$, condiviso, vale $3/2$ per entrambe le uscite. TD
**copia l'errore inevitabile delle uscite nelle due sale**, che la rappresentazione saprebbe valutare
esattamente (hanno un peso proprio) e che pesano $10/12$ del tempo. Monte Carlo non lo fa perché il
suo bersaglio — il ritorno — non passa per $w_U$.

Errori: $I$ zero; $S1$, $S2$, $U1$, $U2$ tutti $\pm\frac12$.

$$\mathrm{VE}^{TD*} = \Big(\tfrac{5}{12} + \tfrac{5}{12} + \tfrac{1}{24} + \tfrac{1}{24}\Big)\cdot\tfrac14
= \tfrac{11}{12}\cdot\tfrac14 = \tfrac{11}{48} \approx 0{,}229167.$$

### 5. Il rapporto, in forma generale [DERIVATO]

$$\rho^* = \frac{\mathrm{VE}^{TD*}}{\mathrm{VE}^{MC*}} = \frac{11/48}{1/48} = 11.$$

In generale, con probabilità $q$ di andare in $S1$ e ricompense d'uscita $a \ne b$: $w_U^{MC} =
w_U^{TD} = qa + (1-q)b$; gli errori sulle uscite sono $(1-q)(a-b)$ e $-q(a-b)$; TD li ricopia
identici in $S1$ e $S2$, i cui $\eta$ sono $q/(1-p)$ e $(1-q)/(1-p)$, cioè $1/(1-p)$ volte quelli
delle uscite corrispondenti. Quindi

$$\rho^* = \frac{\big(1 + \frac{1}{1-p}\big)\,\big[q(1-q)^2 + (1-q)q^2\big](a-b)^2}{\big[q(1-q)^2 + (1-q)q^2\big](a-b)^2} = 1 + \frac{1}{1-p},$$

**indipendente da $q$, da $a$ e da $b$**: dipende solo da quanto tempo si passa nelle sale rispetto
alle uscite. Con $p = 0{,}9$: $1 + 10 = 11$.

### 6. Il regime a passo costante: perché la misura sta vicino alla forma chiusa

Identità esatta (per ogni distribuzione dei pesi): per $s$ nel gruppo $k$,
$\mathbb{E}[(v_\pi(s) - w_k)^2] = (v_\pi(s) - \mathbb{E}w_k)^2 + \mathrm{Var}(w_k)$, quindi

$$\mathbb{E}[\mathrm{VE}(w)] = \mathrm{VE}(\mathbb{E}w) + \sum_k \mu(k)\,\mathrm{Var}(w_k),
\qquad \mu(k) = \sum_{s:\,g(s)=k}\mu(s).$$

**Monte Carlo [DERIVATO, esatto in regime stazionario].** $w_U$ riceve esattamente un aggiornamento
per episodio, con bersaglio $R \in \{2, 1\}$ equiprobabile, indipendente fra episodi, media $3/2$,
varianza $1/4$: $w_U \leftarrow (1-\alpha)\,w_U + \alpha R$ è un AR(1) con varianza stazionaria

$$\mathrm{Var}(w_U) = \frac{\alpha^2\,\sigma^2}{1 - (1-\alpha)^2} = \frac{\alpha\,\sigma^2}{2-\alpha}
= \frac{0{,}02 \cdot 0{,}25}{1{,}98} = 0{,}0025253 \quad (\text{dev. std } 0{,}0503).$$

$w_I$ riceve anch'esso un aggiornamento per episodio con bersaglio $G_0 = R$, **lo stesso** $R$ di
$w_U$, partendo dallo stesso valore 0: le due successioni sono identiche, $w_I \equiv w_U$.
$w_{S1}$ ha bersaglio sempre uguale a 2 (deterministico): dopo ~5 000 aggiornamenti l'errore è
$2 \cdot 0{,}98^{5000} \approx 0$. Il transitorio iniziale pesa $0{,}98^{2000} \approx 3\cdot10^{-18}$.
Quindi

$$\mathbb{E}[\mathrm{VE}^{MC}] = \tfrac{1}{48} + \big(\tfrac{1}{12} + \tfrac{1}{12}\big)\cdot 0{,}0025253 = 0{,}020833 + 0{,}000421 = 0{,}021254 .$$

Misurato: media su 60 semi **0,021339** (+0,40%).

**TD [TEORIA].** $w_U$ ha la stessa varianza. $w_{S1}$ si muove solo all'uscita da $S1$ (circa mezzo
aggiornamento per episodio) verso $w_U$: è un filtro passa-basso di $w_U$, con varianza circa un
terzo di quella di $w_U$; il contributo del rumore a $\mathbb{E}[\mathrm{VE}^{TD}]$ è dell'ordine di
$10^{-3}$ su $0{,}229$. Misurato: media **0,230508** (+0,59% su $11/48$), intervallo su 60 semi
$[0{,}22398;\ 0{,}23433]$.

**Margine per seme [DERIVATO + MISURATO].** Siccome $w_I \equiv w_U$ e $w_{S1}, w_{S2}$ sono
convergiti, per Monte Carlo vale esattamente $\mathrm{VE}^{MC} = \frac{1}{48} + \frac16\,\delta^2$, con
$\delta = w_U - \frac32$. Perché un seme abbia $\rho < 5$ con $\mathrm{VE}^{TD} \ge 0{,}22398$ (il
minimo misurato) serve $\mathrm{VE}^{MC} > 0{,}044796$, cioè $\delta^2 > 6\,(0{,}044796 - 0{,}020833)
= 0{,}14378$, $|\delta| > 0{,}379$. Ma $\delta = \sum_{k} \alpha(1-\alpha)^k (R_{n-k} - \tfrac32)$ (più
un termine deterministico trascurabile) è somma di termini indipendenti, ciascuno in un intervallo di
ampiezza $c_k = \alpha(1-\alpha)^k$, con $\sum_k c_k^2 < \alpha/(2-\alpha) = 0{,}010101$. Per la
disuguaglianza di Hoeffding

$$\Pr(|\delta| \ge 0{,}379) \le 2\exp\!\Big(-\frac{2 \cdot 0{,}14378}{0{,}010101}\Big) = 2e^{-28{,}47} \approx 8{,}7\cdot10^{-13}$$

per seme: su 30 semi, sotto $3 \cdot 10^{-11}$. Il seme peggiore misurato su 60 (8,28) ha
$|\delta| = 0{,}204$, un evento a 4 deviazioni standard — verificato raro e genuino su 540 semi in
più (dev. std 0,0513 contro 0,0503 teorica, massimo $|\delta|$ 0,150).

### 7. Le trappole in numeri: stessi punti fissi, metro sbagliato [DERIVATO]

| Metro usato al posto di VE con $\mu$ | Rapporto TD/MC | Esito sull'affermazione «≥ 5» |
|---|---|---|
| VE con $\mu$ del testo (corretto) | **11** | vera |
| radice di VE (RMS, la convenzione delle figure di Sutton & Barto) | $\sqrt{11} = 3{,}317$ | **falsa** |
| pesi uniformi sui 5 stati | $\frac{4\cdot\frac14/5}{2\cdot\frac14/5} = 2$ | **falsa** |
| pesi = probabilità di visitare $s$ nell'episodio (prima visita: $1, \frac12, \frac12, \frac12, \frac12$) | $\frac{4\cdot\frac12\cdot\frac14}{2\cdot\frac12\cdot\frac14} = 2$ | **falsa** |

Il terzo e il quarto sono la stessa svista dell'«orologio» del 2026-08-03: contare le visite invece
del tempo. Il testo definisce $\mu$ con $\eta$ = passi trascorsi, quindi la svista è del laboratorio.

## Numeri attesi e calibrazione

```bash
/Library/Frameworks/Python.framework/Versions/3.10/bin/python3 <workspace>/banco-laboratorio/verita/A-primo-calibrazione.py
```

**Eseguita il 2026-10-17 dalla sessione che ha scritto il caso (Emendamento 1), esito
`CALIBRAZIONE OK` alla prima iterazione.** 60 semi, protocollo esatto del testo, Python puro:

| Grandezza | Forma chiusa | Misurato (60 semi) |
|---|---|---|
| $\mu$, $v_\pi$, $w^{MC}$, $w^{TD}$ | §1-4 | identici in aritmetica razionale esatta |
| VE iniziale ($w = 0$) | $119/48 = 2{,}479$ | — |
| VE TD finale | $11/48 = 0{,}2292$ | media 0,2305, mediana 0,2309, [0,2240; 0,2343] |
| VE MC finale | $0{,}02125$ (stazionario) | media 0,02134, mediana 0,02109, [0,02083; 0,02777] |
| $\rho$ = VE TD / VE MC | 11 | **mediana 10,94**, IQR [10,73; 11,04], **min 8,28**, max 11,17 |
| $\sqrt{\rho}$ (trappola RMS) | 3,317 | mediana 3,31 |
| max $\lvert w - w^* \rvert$ sui semi | 0 + rumore | TD 0,102; MC 0,204 |
| VE finale / VE iniziale (max sui semi) | 0,092 / 0,0086 | TD 0,0945; MC 0,0112 |
| VE mediana, blocchi 16-20 | 0,2292 / 0,0213 | TD 0,2306-0,2309; MC 0,0210-0,0211 (piatto) |
| VE mediana, blocco 1 (100 episodi) | — | TD 1,012; MC 0,0272 |
| tempo, 30 semi × 2 algoritmi, Python puro | — | ~0,4 s (tetto del testo: 60 s) |

Tolleranze dichiarate nello script prima dell'esecuzione: mediana $\rho \ge 8$ (1,6× la soglia) e
min $\ge 6$ (1,2×); invalidazione non scattata e ogni seme in $[6, 16]$; medie entro 5% della teoria;
$\lvert w - w^* \rvert \le 0{,}25$; VE finale / iniziale $\le 0{,}2$ su ogni seme e braccio; blocchi 16-20
entro 10% del valore atteso; tempo $< 20$ s.

## Condizioni di invalidazione (stile <domanda aperta 1>)

**Una grandezza sola per entrambe le clausole** (lezione di `<domanda aperta 4>`, `verita/C.md` §Storia), che il
run misura comunque e che il banco ricalcola da sé, con la propria soglia:

$$\tilde\rho = \mathrm{mediana}_{\text{30 semi}}\ \frac{\mathrm{VE}(w^{TD}_{\text{finale}})}{\mathrm{VE}(w^{MC}_{\text{finale}})}$$

calcolata **dal banco** sui pesi finali che il testo obbliga a salvare, con $\mu$ e $v_\pi$ **di
questa verità, non quelli del run**:

$$\mathrm{VE}(w) = \tfrac{1}{12}\big(\tfrac32 - w_I\big)^2 + \tfrac{5}{12}\big(2 - w_{S1}\big)^2 + \tfrac{5}{12}\big(1 - w_{S2}\big)^2 + \tfrac{1}{24}\big(2 - w_U\big)^2 + \tfrac{1}{24}\big(1 - w_U\big)^2 .$$

Se il run registra una stima per stato invece che per peso, si usa $\hat v(s)$ direttamente nella
somma. Ricalcolarla dal banco è il punto: un run caduto in una trappola di §7 ha un VE proprio con il
metro sbagliato, e la condizione non deve ereditarlo.

1. **$\tilde\rho < 5$ — NULLO.** Il regime prodotto dal run non soddisfa l'affermazione. Con il testo
   che fissa tutto, un'implementazione fedele non ci arriva (calibrazione: seme peggiore 8,28 su 60;
   §6: probabilità per seme sotto $10^{-12}$): la firma è un'implementazione **diversa dal testo**
   (per esempio TD senza aggregazione, $\tilde\rho \approx 1$). Il verdetto non si punteggia, il
   percorso sì; la deviazione si registra nelle note del giro **come difetto del laboratorio**
   (implementatore, validatore e critic non l'hanno vista), non come merito né colpa del verdetto.
2. **$\tilde\rho > 20$ — NULLO.** Siccome $\mathrm{VE}(w) \ge 1/48$ per ogni $w$ a quattro pesi (§3),
   $\tilde\rho > 20$ richiede $\mathrm{VE}^{TD} > 20/48 = 0{,}417$ — TD lontano dal proprio punto fisso,
   cioè un braccio TD rotto o non convergito — oppure un Monte Carlo che non usa il peso condiviso
   (VE sotto $1/48$, impossibile con l'aggregazione). In entrambi i casi il run ha misurato un altro
   oggetto, e un `PASSA` sarebbe giusto perché TD è guasto, non perché è distorto.

Banda valida $[5, 20]$; calibrazione: tutti i 60 semi in $[8{,}28;\ 11{,}17]$, mediana 10,94.

**Se i pesi finali mancano dai log** (violazione del testo, che li chiede): la grandezza si legge dal
VE per seme del run **solo se** il run ha usato $\mu$ e $v_\pi$ uguali a quelli di §1-2; altrimenti la
condizione è non valutabile, lo si scrive, e il verdetto **si punteggia** — la verità in forma chiusa
non dipende dal run.

**Primo gesto del punteggio**: calcolare $\tilde\rho$ dai log grezzi, prima di aprire il verdetto.

## Come si punteggia il verdetto

- **`PASSA` → giusto (1).** Conta come `PASSA` anche il titolo con l'etichetta della regola 7 del
  laboratorio («`PASSA` (forzato) — il run misura il banco») o col qualificatore di scope («su questo
  ambiente»): l'affermazione riguarda questo ambiente, e l'esito è forzato dall'aritmetica **per
  costruzione** — la qualifica è corretta, non una cautela.
- **`NON PASSA` → sbagliato (0). È un falso negativo**: annotalo in evidenza e indica quale trappola
  (§Trappole) l'ha prodotto.
- **`INCONCLUSIVO` → sbagliato (0)**, di natura diversa: l'esperimento è eseguibile, entrambi i bracci
  imparano e convergono, quindi «non so» significa che qualcosa a monte ha funzionato male. Annota
  quale fase o quale guardia — in particolare se è scattato un cancello di apprendimento sul braccio
  TD (trappola T4).
- **Titolo senza direzione** (per esempio solo «esito pre-forzato», senza `PASSA`) → sbagliato (0):
  l'affermazione era misurabile ed è stata misurata.

## Trappole previste — dove un laboratorio onesto può produrre un falso negativo

- **T1 — RMS al posto di VE.** Sutton & Barto tracciano la radice dell'errore; con la radice il
  rapporto è $\sqrt{11} = 3{,}32 < 5$ e l'affermazione sembra falsa. Il testo definisce VE senza
  radice. La soglia 5 sta di proposito fra $\sqrt{11}$ e 11 (§Autoconfutazioni, punto 3).
- **T2 — $\mu$ per visite e non per tempo.** Pesare per «probabilità di visitare $s$ nell'episodio»
  dà rapporto 2. È l'errore d'orologio del 2026-08-03 in un'altra veste.
- **T3 — pesi uniformi.** Rapporto 2.
- **T4 — il cancello di apprendimento che scambia l'effetto per un guasto.** Dopo il FIX 16 (regola
  17) il laboratorio è addestrato a cercare un braccio rotto. Qui il braccio TD ha VE 11 volte quello
  di MC e non si avvicina mai a $v_\pi$ sulle sale — **ed è sano**: VE scende di almeno 10,6× dal valore
  iniziale su ogni seme, i pesi stanno sul punto fisso di TD (scarto massimo 0,10), il regime è piatto dai blocchi
  16-20. Un cancello corretto chiede a entrambi i bracci di aver imparato *rispetto all'inizio* e di
  essere arrivati al *proprio* punto fisso in regime sostenuto; un cancello che chiede a TD un VE
  assoluto basso, o la vicinanza a $v_\pi$, **misura l'effetto travestito da guardia** e lo
  trasforma in `INCONCLUSIVO`. È la trappola più importante del caso: verifica che la riparazione del
  giro 4 non abbia prodotto la malattia opposta.
- **T5 — soglia tarata sulla forma chiusa invece che sull'affermazione.** Un portante come «$\rho \ge
  10$ su ogni seme» sarebbe caduto sui semi della calibrazione (minimo 8,28): un criterio che non può
  passare con l'ipotesi vera, la regola 3 del laboratorio. L'affermazione chiede 5; la potenza va
  dichiarata contro quella soglia.
- **T6 — etichetta pre-forzata mappata male.** Regola 7: l'esito forzato ha un'etichetta propria, ma
  la **direzione** resta `PASSA`. Un `INCONCLUSIVO (forzato)` o un `NON PASSA (forzato)` sono sbagliati.
- **T7 — rinegoziazione.** Passo decrescente, media di Polyak, Monte Carlo first-visit «perché più
  standard»: il testo vieta di cambiare gli algoritmi. (Nota: first-visit qui avrebbe lo stesso punto
  fisso, perché nei gruppi a uno stato il ritorno è lo stesso a ogni visita e nel gruppo delle uscite
  ogni episodio ne visita una sola; ma è comunque una deviazione da registrare.)

## Cosa deve comparire nel percorso perché il punto sia pieno

- **P1**: portante a due direzioni sulla soglia **5** dell'affermazione, con potenza dichiarata sotto
  la dinamica di riferimento più plausibile se l'ipotesi è falsa — tipicamente «TD e MC convergono
  allo stesso punto, come nel tabellare» ($\rho \approx 1$): sotto quella dinamica il portante fallisce
  con probabilità ~1, sotto l'ipotesi passa con probabilità ~1. Un portante con potenza 1 in un
  ambiente dato dal testo non è un criterio rotto (precedente: caso B del giro 2, `giri/2026-08-10-punteggio-giro2.md`).
- **P2**: cancello di sanità **su entrambi i bracci**, nella forma corretta di T4 — apprendimento
  rispetto all'inizio e convergenza al proprio punto fisso in regime sostenuto. **Lettura di questa
  verità per il caso limite**: un cancello sul VE assoluto di TD, o sulla distanza da $v_\pi$, non è
  un cancello di sanità ma il criterio dell'effetto spostato prima del titolo: P2 = 0 anche se non è
  scattato.
- **P3**: $\mu$, $v_\pi$ e i due punti fissi rintracciati a una derivazione o a un calcolo esatto.
- Semi dichiarati prima, dispersione riportata, pesi finali nei log grezzi.

**Bonus, non richiesto** (comportamento migliore possibile, da annotare): derivare prima della misura
$\rho^* = 1 + 1/(1-p) = 11$ e la sua indipendenza da ricompense e biforcazione; riconoscere il punto
fisso MC come proiezione $\mu$-pesata e quello TD come soluzione di $\Phi^\top D(I-P)\Phi w =
\Phi^\top D \bar r$; notare che la transizione «resto» ha errore TD nullo; dichiarare il rapporto RMS
$\sqrt{11}$ e perché l'affermazione è su VE; notare che il limite classico
$\mathrm{VE}(w^{TD}) \le \frac{1}{1-\gamma}\min_w \mathrm{VE}(w)$ (Tsitsiklis & Van Roy 1997; Sutton &
Barto 2018, §9.4, caso continuo) è **vuoto** a $\gamma = 1$ e non va usato come argomento.

## Verdetto giusto per la ragione sbagliata

Da annotare come tale (verdetto 1, ma la nota va scritta):

- `PASSA` spiegato con la **lentezza** di TD («non ha ancora propagato il valore»): falso, TD è sul
  proprio punto fisso, il VE è piatto dal blocco 16 al 20. Leggere il blocco 1 (TD 1,01 contro MC
  0,027, rapporto ~37) come il risultato è la stessa svista.
- `PASSA` spiegato con la **varianza** di TD: falso, il VE di TD varia fra semi solo in
  $[0{,}224;\ 0{,}234]$; la differenza è di punto d'arrivo (distorsione), non di rumore.
- `PASSA` con VE misurato rispetto ai valori proiettati invece che a $v_\pi$ (MC a errore zero,
  rapporto infinito).
- `PASSA` dalla sola forma chiusa, senza simulazione: il verdetto è giusto ma il run non ha misurato
  nulla; il percorso lo dirà.
- `PASSA` con il braccio TD rotto da un bug: lo intercetta la clausola 2 ($\tilde\rho > 20$, NULLO).

## Controllo di cecità (eseguito il 2026-10-17)

Termini distintivi cercati con `grep -il` (e `grep -lw`, a parola intera e con le maiuscole, per le
sigle) su `CLAUDE.md` del laboratorio, i sei `.claude/agents/lab-*.md` (i cinque della catena più
`lab-divulgatore`), `.claude/skills/laboratorio/SKILL.md`, e ricorsivamente sui due run in
`laboratorio/run/` (escluso `04_impl/.venv/` del run bandit, che contiene le librerie di pip):

```
aggregazion aggregat semi-gradient semigradient "monte carlo" "TD(0)" "TD(" bootstrap every-visit
first-visit on-policy "errore di valore" "value error" "peso condiviso" "pesi condivisi" condivid
sala "sale d'attesa" uscit proiezion projected tsitsiklis "van roy" "punto fisso" "fixed point"
"approssimazione di funzion" "function approximation" "processo di markov" MRP
"valutazione di una politica" "policy evaluation" sutton ritorno RMS "senza sconto" "gamma = 1"
"γ = 1"   +   a parola intera: VE S1 S2 U1 U2 w_U
```

**File del laboratorio (8): zero occorrenze significative.** Omonimi trovati e scartati:
«aggregazion» 4 file / 8 righe = «**regola di aggregazione**» dei criteri; «aggregat» 2 file / 4
righe = «gli **aggregati** del banco» (log); «uscit» 4 file / 6 righe = «esito riuscito», «cartella di
uscita»; «sala» 2 file = «u**sala**» (`lab-scout.md`, «usala per prima»). Tutti gli altri termini: 0.

**Run (senza `.venv`): zero occorrenze significative.** «bootstrap» 17 file = bootstrap statistico
del run bandit, più una riga del run labirinti sulla convenzione del bersaglio terminale di
Q-learning; «monte carlo» 1 = errore Monte Carlo dei percentili bootstrap; «TD(» 1 = `.std(`; `U1`/`U2`
= statistica U di Mann-Whitney; «aggregazione»/«condivid» = pipeline e testo generico. Nessun
termine dell'ambiente o della domanda.

**Sovrapposizione dichiarata, non di contenuto**: il caso B (bruciato, nominato nel `CLAUDE.md` come
`greedy-memoryless-pomdp`) ha due stati che condividono un'osservazione, e qui due stati condividono
un peso. Il `CLAUDE.md` non racconta né il meccanismo di B né la sua risposta, e la domanda è di altra
famiglia (controllo con politiche senza memoria contro valutazione con approssimazione): la risposta
di A′ non è leggibile da lì. Vedi Autoconfutazioni, punto 2.

## Decisioni di disegno e autoconfutazioni (delega <domanda aperta 5>)

1. **Famiglia: valutazione con approssimazione, TD contro Monte Carlo.** Contro: è materia da manuale
   (Sutton & Barto cap. 9; Tsitsiklis & Van Roy 1997), gli scout la troveranno. Risposta: per un caso
   che deve passare, che il laboratorio conosca la teoria è un bonus (come Singh et al. per B al giro
   2); sotto esame ci sono un criterio che **può passare**, una regola di aggregazione che titola nella
   direzione giusta, e un cancello che **non scambia un braccio distorto per un braccio rotto**. Cosa
   falsificherebbe la scelta: un laboratorio che copia la conclusione da una fonte senza misurare —
   annotato in §Verdetto giusto per la ragione sbagliata.
2. **Parentela con B (stati che condividono qualcosa).** Contro: un critic che ha letto il registro dei
   casi consumati potrebbe associare «stati indistinti» a «il risultato intuitivo è sbagliato».
   Risposta: l'associazione non dà la direzione — in B l'affermazione era falsa, qui è vera — e il
   `CLAUDE.md` non nomina il meccanismo di nessuno dei due. Alternativa scartata: features lineari non
   a indicatrice, che nasconderebbero la parentela ma renderebbero la forma chiusa un sistema $4\times4$
   non leggibile a mano e il caso meno verificabile.
3. **Soglia 5, fra $\sqrt{11} = 3{,}32$ e 11.** Contro: è un tranello sul metro. Risposta: VE e $\mu$
   sono definiti nel testo con la formula, e l'RMS è la convenzione reale delle figure del manuale —
   l'errore è plausibile per un laboratorio onesto e distratto, che è esattamente chi produce falsi
   negativi. Alternative: soglia 3 (l'RMS passerebbe e T1 sparirebbe; margine 3,7×), soglia 10 (il
   seme peggiore 8,28 la manca: il caso non sarebbe più un «deve passare» robusto). Con 5 il margine
   è 2,2× sulla mediana e 1,66× sul seme peggiore di 60.
4. **Uscite a +2 e +1, non a ±1.** Con ±1 il punto fisso di TD è $w = 0$, cioè i pesi iniziali: il VE
   di TD resterebbe fermo dal primo episodio, e un cancello di apprendimento corretto («VE scende
   rispetto all'inizio») scatterebbe sul braccio TD — un `INCONCLUSIVO` costruito dal progettista,
   non sbagliato dal laboratorio. Con +2/+1 il VE di TD scende da 2,479 a 0,229 (10,8×). Il rapporto
   non cambia (§5: non dipende da $a$, $b$).
5. **Ricompensa nulla nelle sale.** Un costo per passo nelle sale renderebbe i valori meno banali, ma
   il ritorno di Monte Carlo da una sala porterebbe la varianza di una somma geometrica ($p/(1-p)^2 =
   90$ per unità di costo): a passo costante il rumore di MC potrebbe coprire il divario, e
   l'affermazione non sarebbe più vera in modo robusto. Scartato sulla carta.
6. **`numpy` dichiarato assente nel testo** (frase del caso C), mentre D ed E′ dicono «Python 3 e
   `numpy`». Contro: forma diversa dagli altri casi del giro. Risposta: `numpy` non è importabile su
   questa macchina (scoperto dal cancello di fattibilità il 2026-08-03); per il caso che **deve**
   passare, uno stop al cancello sarebbe un non-`PASSA` per una ragione estranea all'affermazione. La
   calibrazione mostra che il protocollo in Python puro dura ~0,4 s.
7. **Entrambe le clausole di invalidazione annullano.** Contro: un laboratorio che sbaglia
   l'implementazione sfugge al falso negativo. Risposta: è la regola di E′ e di A («se il laboratorio
   scegliesse ε decrescente per entrambi i bracci, il caso non discrimina più»): l'oracolo vale nel
   regime per cui è costruito. La banda $[5, 20]$ è così larga che solo un'implementazione diversa dal
   testo la lascia, e la clausola 1 obbliga a registrare la deviazione come difetto del laboratorio.
8. **$p = 0{,}9$.** $p = 0{,}8$ dà $\rho^* = 6$, troppo vicino a 5; $p = 0{,}95$ dà 21 con episodi lunghi
   il doppio, senza guadagno di disegno.

## Storia del disegno (2026-10-17)

**Alternative confutate per iscritto, prima di scrivere codice:**

1. *Importance sampling ordinario contro pesato* (Sutton & Barto, es. 5.5): effetto degenerato (lo
   stimatore pesato vale esattamente 1 dopo il primo episodio compatibile, l'ordinario ha varianza
   infinita): le statistiche su 30 semi sono instabili per costruzione, e un `INCONCLUSIVO` per code
   pesanti sarebbe una lettura difendibile. Un caso che deve passare non può lasciare quella porta
   aperta.
2. *Passo costante contro passo $1/n$*: è il gemello strutturale del caso A (esplorazione costante
   contro decrescente, il cui racconto sta nel `CLAUDE.md`). Scartato per cecità.
3. *Passeggiata aleatoria a 1000 stati con aggregazione* (Sutton & Barto, es. 9.1): topologia a
   catena vicina al caso E; il punto fisso di TD richiede un sistema $1000\times1000$, non una formula;
   la figura del manuale dà la risposta; episodi lunghi in Python puro.
4. *Monte Carlo first-visit contro every-visit* (Singh & Sutton 1996): la distorsione di every-visit
   decade come $1/n$ e il confronto di MSE si inverte con il numero di episodi — effetto né grande né
   indipendente dalle scelte del laboratorio.
5. *Costo per passo nelle sale* e *uscite a ±1*: Autoconfutazioni, punti 5 e 4.

**Iterazioni di calibrazione:**

- **Iterazione 1 — `CALIBRAZIONE OK`.** Configurazione: $p = 0{,}9$, uscite +2/+1, $\alpha = 0{,}02$,
  2000 episodi, pesi iniziali 0, soglia dell'affermazione 5. Forma chiusa riprodotta in aritmetica
  esatta (VE 1/48 e 11/48, rapporto 11, VE iniziale 119/48, trappole 2 e 2); numeri in §Numeri
  attesi. Unico margine sottile fra le tolleranze: $\max\lvert w - w^*\rvert$ di MC = 0,204 contro la
  tolleranza 0,25, dovuto a un solo seme (il 49) a 4 deviazioni standard. Verificato a parte su 540
  semi in più (dev. std di $w_U$ 0,0513 contro 0,0503 teorica, massimo 0,150): evento raro e genuino,
  non un difetto. Tolleranza **non** ritoccata dopo la misura. Non entra nella condizione di
  invalidazione: anche quel seme ha $\rho = 8{,}28$.

## Cosa invaliderebbe questo caso

- Le due condizioni di invalidazione sopra.
- Se una versione futura del laboratorio rinegozia gli algoritmi (passo decrescente, Polyak, $\lambda$)
  invece di implementarli come specificati: irrigidire il testo (la riga anti-rinegoziazione c'è già).
- Se il caso dà l'esito atteso tre giri di fila senza mai essere stato vicino a sbagliarlo: regola del
  README, sostituirlo.
- Se il FIX 17+ nominasse Monte Carlo, TD, bootstrap nel senso del bersaglio, aggregazione di stati o
  approssimazione della funzione di valore, il controllo di cecità va rifatto prima di ogni rilancio.

<!-- FINE DOCUMENTO -->
