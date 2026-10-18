# Verità sigillata — Caso B′ (il momentum e il rumore del gradiente)

**NON APRIRE prima della fine del caso.**

Scritta il 2026-10-17 da un subagente della fase 3 (rotta, `OBIETTIVO-E-ROTTA.md` §4), su incarico
della sessione principale. La sessione principale **non ha letto** questa verità: le sono stati
riportati solo i percorsi, l'esito della calibrazione e quello del controllo di cecità. Il subagente
che l'ha scritta non coordina nulla (regola del 2026-08-03: chi scrive le verità non coordina i run).
File consegnabile: `casi/B-primo-momentum-e-rumore.md` — **senza lettera nel titolo** (decisione del
2026-08-19, motivo in `verita/E-primo.md` §Autoconfutazioni, punto 4; qui ripresa senza riaprirla).

## Esito atteso: `NON PASSA` — il momentum **moltiplica per ~10** l'errore a regime

B′ eredita il ruolo di B: un'affermazione plausibile, del tipo che circola come idea diffusa, **falsa**
sull'ambiente fissato dal testo, con una verità in forma chiusa che mostra l'effetto **opposto** e
grande. Il caso verifica che il laboratorio sappia **contraddire** un'affermazione plausibile invece di
confermarla con numeri propri.

L'affermazione dice che, a parità di passo $\alpha$, il momentum con $\beta = 0{,}9$ **riduce** l'errore
quadratico a regime. In forma chiusa l'errore a regime col momentum è $9{,}976$ volte quello senza:
non è un effetto assente, è un effetto di segno opposto, di un ordine di grandezza. La ragione
strutturale: a regime il termine di momentum **somma** i gradienti con pesi geometrici la cui somma è
$1/(1-\beta) = 10$, quindi il passo efficace è $\alpha/(1-\beta)$, e la varianza stazionaria della
discesa stocastica è (per $\alpha\lambda$ piccolo) proporzionale al passo. La compensazione del rumore
fra passi diversi è reale *nella direzione*, ma la stessa somma che la produce amplifica il rumore per
$1/(1-\beta)$ e lo integra su una memoria dieci volte più lunga.

Il caso è **interamente sintetico**: la verità non poggia su nessun paper, ed è derivata qui sotto
passaggio per passaggio. Se il laboratorio sbaglia questo caso, l'errore è suo per intero.

## Perché, in forma chiusa

### Notazione e dimensioni

Tutte le grandezze del problema sono **scalari** ($1\times 1$): $x_t$ (iterata), $v_t$ (termine di
momentum), $g_t$ (gradiente stocastico), $\xi_t$ (rumore). Parametri del testo:
$\lambda = 1$, $\sigma = 1$, $\alpha = 0{,}01$, $\beta \in \{0;\ 0{,}9\}$, $x_0 = 10$, $v_0 = 0$,
$T = 20\,000$. Prodotto ricorrente: $\alpha\lambda = 0{,}01$.

L'oracolo restituisce $g_t = \lambda x_t + \sigma \xi_t$ con $\xi_t \sim \mathcal N(0,1)$ indipendenti.
Poiché $x_t$ dipende solo da $\xi_0,\dots,\xi_{t-1}$, **$\xi_t$ è indipendente da $x_t$ e da
$x_{t-1}$**: è il fatto che rende nulli i termini incrociati più sotto.

### Passo 1 — dalla coppia $(x, v)$ a una ricorrenza del secondo ordine in $x$

La regola del testo è

$$v_{t+1} = \beta v_t + g_t, \qquad x_{t+1} = x_t - \alpha v_{t+1}.$$

Dalla seconda equazione scritta al passo precedente, $x_t = x_{t-1} - \alpha v_t$, cioè
$\alpha v_t = x_{t-1} - x_t$ (vale per $t \ge 1$). Sostituisco la prima equazione nella seconda:

$$x_{t+1} = x_t - \alpha(\beta v_t + g_t) = x_t - \beta(\alpha v_t) - \alpha g_t = x_t - \beta(x_{t-1} - x_t) - \alpha g_t .$$

Raccolgo e sostituisco $g_t = \lambda x_t + \sigma\xi_t$:

$$x_{t+1} = (1+\beta)x_t - \beta x_{t-1} - \alpha\lambda x_t - \alpha\sigma\xi_t = \underbrace{(1+\beta-\alpha\lambda)}_{\equiv\, a} x_t \;-\; \beta\, x_{t-1} \;-\; \alpha\sigma\,\xi_t .$$

Per $t = 0$ la formula vale ponendo $x_{-1} = x_0$ (perché $v_0 = 0$ dà $x_1 = x_0 - \alpha g_0$).
È un processo autoregressivo di ordine 2 con coefficienti $a$ e $-\beta$ e innovazione
$-\alpha\sigma\xi_t$, di varianza $\alpha^2\sigma^2$. Con $\beta = 0$ si riduce a
$x_{t+1} = (1-\alpha\lambda)x_t - \alpha\sigma\xi_t$: la discesa stocastica semplice.

Valori: $\beta = 0 \Rightarrow a = 0{,}99$; $\beta = 0{,}9 \Rightarrow a = 1{,}89$.

### Passo 2 — stabilità e scomparsa del transitorio

La parte deterministica (media) obbedisce a $m_{t+1} = a\,m_t - \beta\,m_{t-1}$, con polinomio
caratteristico $z^2 - a z + \beta = 0$.

- $\beta = 0$: radice $z = 1 - \alpha\lambda = 0{,}99$.
- $\beta = 0{,}9$: discriminante $a^2 - 4\beta = 1{,}89^2 - 3{,}6 = 3{,}5721 - 3{,}6 = -0{,}0279 < 0$:
  radici complesse coniugate, $z = 0{,}945 \pm 0{,}08352\,i$, modulo $\sqrt{\beta} = 0{,}948683$.

Entrambi i moduli sono $< 1$: **entrambe le varianti sono stabili** (il momentum non diverge — da tenere
a mente per le ragioni sbagliate, §sotto). La media va a 0 e l'errore quadratico a regime coincide con
la varianza stazionaria. Ampiezza del transitorio all'inizio della finestra ($t = 10\,001$):
$10 \cdot 0{,}99^{10\,000} \approx 10\,e^{-100{,}5} \approx 2\cdot 10^{-43}$ senza momentum, ancora meno
col momentum ($0{,}9487^{10\,000} \approx e^{-527}$). Quindi **il valore atteso dell'errore a regime
definito dal testo è la varianza stazionaria, alla precisione di macchina**. [DERIVATO]

### Passo 3 — varianza stazionaria (equazioni di Yule–Walker scritte per esteso)

A regime definisco $\gamma_0 = \mathbb E[x_t^2]$ e $\gamma_1 = \mathbb E[x_t x_{t-1}]$, indipendenti da $t$.

**(i) Moltiplico la ricorrenza per $x_t$ e prendo il valore atteso.**

$$\mathbb E[x_{t+1}x_t] = a\,\mathbb E[x_t^2] - \beta\,\mathbb E[x_t x_{t-1}] - \alpha\sigma\,\mathbb E[\xi_t x_t].$$

L'ultimo termine è zero per l'indipendenza di $\xi_t$ da $x_t$. A regime $\mathbb E[x_{t+1}x_t] = \gamma_1$:

$$\gamma_1 = a\gamma_0 - \beta\gamma_1 \quad\Longrightarrow\quad \gamma_1 = \frac{a\,\gamma_0}{1+\beta}.$$

**(ii) Elevo al quadrato la ricorrenza e prendo il valore atteso.** Il quadrato di
$a x_t - \beta x_{t-1} - \alpha\sigma\xi_t$ ha sei termini:

$$x_{t+1}^2 = a^2x_t^2 + \beta^2x_{t-1}^2 + \alpha^2\sigma^2\xi_t^2 - 2a\beta\,x_tx_{t-1} - 2a\alpha\sigma\,x_t\xi_t + 2\beta\alpha\sigma\,x_{t-1}\xi_t .$$

I due termini con $\xi_t$ moltiplicato per $x$ hanno valore atteso zero; $\mathbb E[\xi_t^2] = 1$. A regime:

$$\gamma_0 = a^2\gamma_0 + \beta^2\gamma_0 + \alpha^2\sigma^2 - 2a\beta\gamma_1 .$$

**(iii) Sostituisco $\gamma_1$ da (i).**

$$\gamma_0\Big(1 - a^2 - \beta^2 + \frac{2a^2\beta}{1+\beta}\Big) = \alpha^2\sigma^2 .$$

Semplifico la parentesi raccogliendo $a^2$:

$$1-\beta^2 - a^2\Big(1 - \frac{2\beta}{1+\beta}\Big) = (1-\beta)(1+\beta) - a^2\,\frac{1-\beta}{1+\beta} = \frac{(1-\beta)\big[(1+\beta)^2 - a^2\big]}{1+\beta}.$$

La differenza di quadrati si fattorizza con $a = 1+\beta-\alpha\lambda$:

$$(1+\beta)^2 - a^2 = (1+\beta-a)(1+\beta+a) = \alpha\lambda\,\big(2(1+\beta) - \alpha\lambda\big).$$

**(iv) Risultato.**

$$\boxed{\gamma_0(\beta) = \frac{\alpha^2\sigma^2(1+\beta)}{(1-\beta)\,\alpha\lambda\,\big(2(1+\beta)-\alpha\lambda\big)} = \frac{\alpha\sigma^2(1+\beta)}{(1-\beta)\,\lambda\,\big(2(1+\beta)-\alpha\lambda\big)}}$$

Controllo a $\beta = 0$: $\gamma_0(0) = \alpha\sigma^2/\big(\lambda(2-\alpha\lambda)\big)$, la varianza
stazionaria nota di un AR(1) con coefficiente $1-\alpha\lambda$ e innovazione $\alpha\sigma$:
$\alpha^2\sigma^2/\big(1-(1-\alpha\lambda)^2\big) = \alpha^2\sigma^2/\big(\alpha\lambda(2-\alpha\lambda)\big)$. Torna. [DERIVATO]

### Passo 4 — i numeri

- Senza momentum: $\gamma_0(0) = \dfrac{0{,}01}{1\cdot(2-0{,}01)} = \dfrac{0{,}01}{1{,}99} = 0{,}0050251256\ldots$
- Con momentum: $\gamma_0(0{,}9) = \dfrac{0{,}01\cdot 1{,}9}{0{,}1\cdot 1\cdot(3{,}8 - 0{,}01)} = \dfrac{0{,}019}{0{,}379} = 0{,}0501319261\ldots$
- Rapporto:

$$R = \frac{\gamma_0(0{,}9)}{\gamma_0(0)} = \frac{(1+\beta)(2-\alpha\lambda)}{(1-\beta)\big(2(1+\beta)-\alpha\lambda\big)} = \frac{1{,}9\cdot 1{,}99}{0{,}1\cdot 3{,}79} = \frac{3{,}781}{0{,}379} = 9{,}976253\ldots$$

L'affermazione richiede $R < 1$. Vale $R \approx 10$. [DERIVATO]

### Passo 5 — seconda via indipendente: equazione di Lyapunov $2\times 2$

Stato $z_t = (x_t,\ x_{t-1})^\top$ ($2\times 1$). Ricorrenza $z_{t+1} = A z_t + b\,(-\alpha\sigma\xi_t)$ con

$$A = \begin{pmatrix} a & -\beta \\ 1 & 0 \end{pmatrix}\ (2\times 2), \qquad b = \begin{pmatrix}1\\0\end{pmatrix}\ (2\times 1).$$

La covarianza stazionaria $P = \mathbb E[z_t z_t^\top]$ ($2\times 2$) risolve $P = A P A^\top + \alpha^2\sigma^2\, b b^\top$;
in forma vettorizzata $(I_4 - A\otimes A)\,\mathrm{vec}(P) = \alpha^2\sigma^2\,\mathrm{vec}(bb^\top)$, con
$I_4 - A\otimes A$ di dimensione $4\times 4$. L'errore a regime è $P_{11}$. Lo script di calibrazione
risolve il sistema con numpy: $P_{11} = 0{,}005025125628$ e $0{,}050131926121$, scarto relativo massimo
dalla formula del Passo 3 pari a $4{,}5\cdot 10^{-13}$. [MISURATO, calibrazione]

### Passo 6 — l'affermazione è falsa per **ogni** $\beta \in (0,1)$, non solo per $0{,}9$

$R > 1$ equivale a numeratore $>$ denominatore. Espando i due prodotti:

$$(1+\beta)(2-\alpha\lambda) = 2 + 2\beta - \alpha\lambda - \beta\alpha\lambda,$$
$$(1-\beta)\big(2+2\beta-\alpha\lambda\big) = 2 + 2\beta - \alpha\lambda - 2\beta - 2\beta^2 + \beta\alpha\lambda .$$

Differenza (primo meno secondo):

$$-\beta\alpha\lambda + 2\beta + 2\beta^2 - \beta\alpha\lambda = 2\beta\,(1 + \beta - \alpha\lambda) > 0 \quad\text{per } \beta>0,\ \alpha\lambda < 1+\beta .$$

Quindi a parità di $\alpha$ il momentum in questa forma **aumenta sempre** l'errore a regime. Sulla
griglia $\beta \in [0{,}01;\ 0{,}99]$ la calibrazione trova $R$ da $1{,}010$ a $99{,}75$. [DERIVATO + MISURATO]

### Passo 7 — la ragione strutturale (il bonus da cercare nel percorso)

Per $\alpha\lambda \ll 1$ il rapporto si semplifica:
$R \approx \dfrac{(1+\beta)\cdot 2}{(1-\beta)\cdot 2(1+\beta)} = \dfrac{1}{1-\beta} = 10$.
Lettura: $v_{t+1} = \sum_{k\ge 0}\beta^k g_{t-k}$ è una **somma** pesata, non una media: i pesi sommano a
$1/(1-\beta)$. Quando il gradiente varia lentamente rispetto a $1-\beta$, il passo effettivo è
$\alpha v \approx \alpha g/(1-\beta)$, cioè la discesa semplice con passo $\alpha/(1-\beta)$, e la
varianza stazionaria della discesa semplice è $\gamma_0(0) \approx \alpha\sigma^2/(2\lambda)$,
**lineare nel passo**. Il rumore nella direzione $v$ è in parte compensato fra passi (vero), ma la
direzione è anche dieci volte più lunga (vero anche questo), e sull'iterata vince il secondo effetto.
L'idea diffusa confonde la varianza **della direzione normalizzata** con l'errore **dell'iterata**.

### Passo 8 — la forma «a media mobile» (serve alla trappola T1)

Se si sostituisce l'accumulo con una media mobile esponenziale, $v_{t+1} = \beta v_t + (1-\beta) g_t$,
la regola è identica alla forma del testo con passo $\alpha' = \alpha(1-\beta) = 0{,}001$. Dal Passo 3:

$$R_{\text{EMA}} = \frac{\gamma_0^{(\alpha')}(\beta)}{\gamma_0^{(\alpha)}(0)} = \frac{(1+\beta)(2-\alpha\lambda)}{2(1+\beta) - \alpha(1-\beta)\lambda} = \frac{1{,}9\cdot 1{,}99}{3{,}8 - 0{,}001} = \frac{3{,}781}{3{,}799} = 0{,}995262 .$$

In quella forma il momentum **riduce** l'errore a regime dello $0{,}47\,\%$: l'affermazione sarebbe
(appena) vera. È la ragione per cui il testo fissa la forma e vieta di aggiustarla. [DERIVATO + MISURATO]

## Numeri attesi (calibrazione eseguita il 2026-10-17, esito `CALIBRAZIONE OK`)

**Protocollo del caso alla lettera, in Python puro** (semi 1…30, `random.Random(s).gauss(0, 1)`, stesso
seme per le due varianti), 0,5 s di calcolo:

| grandezza | variante 1 (β = 0) | variante 2 (β = 0,9) |
|---|---|---|
| errore a regime, mediana su 30 semi | **0,0047853522** | **0,0493304121** |
| min … max su semi | 0,003645 … 0,005852 | 0,043611 … 0,056317 |
| forma chiusa (valore atteso) | 0,0050251256 | 0,0501319261 |

- $\hat R$ = rapporto delle mediane = **10,30862724** (forma chiusa 9,976).
- Errore a regime maggiore col momentum in **30 semi su 30**; rapporto per seme minimo **8,34**. Gli
  intervalli min…max delle due varianti **non si sovrappongono**: ogni seme da solo smentisce
  l'affermazione.
- **Riscontro cifra per cifra.** I semi e il generatore sono fissati dal testo: un'implementazione
  conforme deve ritrovare le due mediane sopra a meno dell'ordine delle somme in virgola mobile (scarto
  relativo atteso $< 10^{-9}$). Uno scarto maggiore non è di per sé un errore, ma dice che
  l'implementazione differisce dal testo (ordine delle estrazioni, `normalvariate` al posto di `gauss`,
  finestra spostata di un passo): va annotato, ed è un controllo gratuito contro dati fabbricati.

**Su 6000 semi (numpy)**: media dell'errore a regime 0,005024 (−0,02 % dalla forma chiusa) e 0,050067
(−0,13 %). **Su 200 lotti indipendenti da 30 semi**: $\hat R$ minimo **9,314**, 1° percentile 9,430,
mediana 10,039, massimo 10,958.

**Trappole, misurate** (stessi 6000 semi, stessi rumori):
- T1, forma a media mobile: $R_{\text{EMA}}$ misurato **0,99513** (teoria 0,99526); errore minore della
  variante 1 nel 72,2 % dei semi; t appaiato su 6000 semi −42,2; **nell'82,5 % dei lotti da 30 semi un
  test appaiato darebbe una riduzione «significativa» (t < −2)**, nell'89,0 % la mediana è più bassa.
- T2, fase transitoria: primo passo con $|x_t| \le 1$ partendo da $x_0 = 10$, mediana **229** senza
  momentum e **21** col momentum — **10,9× più veloce**.

## Calibrazione

```bash
/Library/Frameworks/Python.framework/Versions/3.10/bin/python3 <workspace>/banco-laboratorio/verita/B-primo-calibrazione.py
```

Ultima riga: `CALIBRAZIONE OK` oppure `CALIBRAZIONE NON OK — correggere: …`. Durata ~3 s. Controlli e
tolleranze dichiarate nello script: forma chiusa contro Lyapunov ($10^{-12}$ relativo); medie su 6000
semi contro forma chiusa (2 %); $\hat R$ del protocollo contro $R$ (15 %); condizione di invalidazione
mai scattata su 200 lotti; $R > 1$ su tutta la griglia di $\beta$; stabilità; trappole T1 ($\pm 0{,}01$
attorno a 0,99526, e $< 1$) e T2 (momentum almeno 2× più veloce nel transitorio); protocollo in Python
puro sotto 60 s.

**Eseguita il 2026-10-17 dal subagente che ha scritto la verità, su mandato esplicito della sessione
principale** — deviazione dalla regola della fase 3 «calibrazioni: utente». Se l'utente non la ratifica,
il comando sopra va rilanciato a mano e l'esito sostituito qui; da rilanciare comunque se i parametri
del caso cambiano.

## Condizione di invalidazione (stile <domanda aperta 1>)

**Una sola grandezza, che il run misura comunque, per entrambe le clausole** (lezione di <domanda aperta 4>): il
testo chiede l'errore a regime per seme e per variante, quindi dai log grezzi del run si calcola sempre

$$\hat R = \frac{\text{mediana su 30 semi dell'errore a regime, variante 2}}{\text{mediana su 30 semi dell'errore a regime, variante 1}} .$$

**Soglia propria: 5**, fissata dal banco e indipendente da qualunque criterio del run (metà della forma
chiusa 9,976; la calibrazione dà $\hat R \ge 9{,}31$ su 200 lotti, margine 1,86×).

Primo gesto della sessione di punteggio, prima di aprire `05_verdetto.md`:

0. **Conformità.** Leggere il codice in `04_impl/` e verificare tre cose: la regola è
   $v \leftarrow \beta v + g$, $x \leftarrow x - \alpha v$ (nessun fattore $1-\beta$, nessun $\alpha$
   diverso fra varianti); la variante 1 è lo stesso codice con $\beta = 0$ (o equivalente esatto); i
   semi sono 1…30 con `random.Random(s).gauss` e la finestra è $t = 10\,001\ldots 20\,000$.
   **Se l'implementazione non è conforme, la condizione di invalidazione NON si applica**: la deviazione
   è del laboratorio, il caso punteggia normalmente (ed è con ogni probabilità una delle trappole sotto).
1. Implementazione conforme e **$\hat R \ge 5$** ⟹ la verità è **valida**, il caso punteggia il verdetto.
2. Implementazione conforme e **$\hat R < 5$** ⟹ la verità è **invalidata**: con la regola del testo
   implementata alla lettera, la forma chiusa non ha descritto ciò che il run misura. Il verdetto non si
   punteggia (profilo «oracolo caduto»), il percorso sì; il caso va ricostruito.

Valore atteso su un'implementazione conforme: $\hat R = 10{,}3086$ esatto (semi fissati).

## Come si punteggia il verdetto

- **`NON PASSA`, motivato dalla direzione misurata** — l'errore a regime col momentum è **maggiore**,
  di circa un ordine di grandezza ($\hat R \approx 10$), non «non minore» — ⟹ verdetto **giusto**.
- **`PASSA`** ⟹ verdetto **sbagliato**, ed è il caso grave: il laboratorio ha confermato un'affermazione
  falsa con numeri propri. Guardare subito **dove**: quasi certamente una delle trappole T1–T5.
- **`INCONCLUSIVO`** ⟹ verdetto **sbagliato**. La verità è in forma chiusa, l'effetto è 10× e di segno
  opposto, 30 semi su 30 concordano, gli intervalli min…max per seme delle due varianti non si
  sovrappongono (0,0036…0,0059 contro 0,0436…0,0563): non c'è spazio
  legittimo per «non so». Un `INCONCLUSIVO` qui segnala tipicamente una regola di aggregazione che non
  mappa il fallimento **nella direzione opposta** (regola 4 del laboratorio) e lo tratta come assenza di
  effetto.

**Verdetto giusto per la ragione sbagliata ⟹ punto a zero** (precedente: `verita/A.md`, «ha ragione sui
numeri che ha e torto sulla domanda»). Conta come tale un `NON PASSA` che poggia su:

1. **«Nessuna riduzione significativa»** — cioè su assenza di effetto invece che su effetto opposto.
   Tipico di un run che ha implementato la forma a media mobile (T1) e ha trovato $R \approx 0{,}995$
   non significativo, o di un criterio sottodimensionato. Il titolo coincide, la ragione è falsa: il
   momentum non è «inutile», è dannoso di 10×.
2. **«Il momentum rallenta la convergenza»** — falso: nel transitorio è 10,9× più veloce (T2).
3. **«Il momentum è instabile / diverge»** — falso: modulo delle radici 0,9487 < 1 (Passo 2).
4. **Solo letteratura**, senza misura: un `NON PASSA` copiato da una fonte («il momentum amplifica il
   rumore») senza aver misurato $\hat R$ vale verdetto 1 e percorso 0, come previsto per B — qui però la
   fonte non è necessaria a niente, quindi ogni dipendenza da essa è un difetto puro.

## Trappole previste — come si «conferma» l'affermazione falsa con una misura mal posta

- **T1 — rinegoziare la forma.** Implementare il momentum «normalizzato» $v \leftarrow \beta v + (1-\beta)g$
  (forma diffusa in letteratura e in alcune librerie) oppure confrontare «a parità di passo efficace»
  ($\alpha(1-\beta)$ alla variante 2). In entrambi i casi $R = 0{,}9953$: il momentum **riduce** l'errore
  dello 0,47 %, e con 30 semi appaiati il test è «significativo» nell'82,5 % dei lotti. È la trappola
  più insidiosa perché produce un `PASSA` statisticamente pulito. Il testo la chiude («stessa forma
  dell'aggiornamento… non un iperparametro da aggiustare»): se il laboratorio la riapre, è violazione
  del testo, e il controllo di conformità (punto 0 sopra) la fa emergere.
- **T2 — misurare la fase sbagliata.** Misurare la velocità di discesa da $x_0 = 10$ (tempo a una soglia,
  errore nei primi passi): il momentum vince 10,9×. Un laboratorio che legge «il momentum aiuta» dalla
  fase transitoria e lo riporta come risposta sull'errore a regime ha misurato bene la domanda sbagliata.
- **T3 — misurare la direzione invece dell'iterata.** La varianza di una media mobile dei gradienti è più
  bassa di quella del gradiente singolo (per rumore dominante, circa $(1-\beta)/(1+\beta)$ volte
  [DERIVATO, approssimato, non calibrato]): «il momentum smorza il rumore» è vero per la direzione, falso
  per l'errore. Un criterio sulla direzione conferma l'affermazione.
- **T4 — aggiustare α per variante.** Scegliere per ciascuna variante il passo «migliore» viola «a parità
  di passo α» e cambia domanda.
- **T5 — aggregazione cieca alla direzione.** Un criterio unilaterale «v2 < v1» che fallisce, letto come
  «effetto non dimostrato» ⟹ `INCONCLUSIVO` o `NON PASSA` per assenza (ragione sbagliata n. 1). La regola
  4 del laboratorio chiede esattamente di nominare le due direzioni di fallimento: qui serve.

## Cosa deve comparire nel percorso perché il punto sia pieno

- Il criterio portante confronta l'errore a regime delle due varianti **sui 30 semi** con dispersione
  dichiarata, e la regola di aggregazione congelata nomina la direzione «variante 2 **peggiore**» e la
  mappa su `NON PASSA` (non su `INCONCLUSIVO`).
- **Cancello di sanità (P2)** su **entrambe** le varianti, prima del confronto: che la finestra sia
  davvero a regime (transitorio esaurito — per esempio prima e seconda metà della finestra concordi,
  oppure il limite del transitorio derivato), e che la manipolazione sia avvenuta (β = 0,9 applicato
  alla variante 2, β = 0 alla 1). Un cancello solo sulla variante sperimentale vale 0 (regola 1).
- Se il run calcola la forma chiusa: $\gamma_0(0) = 0{,}0050251$, $\gamma_0(0{,}9) = 0{,}0501319$,
  $R = 9{,}976$ esatti. Se simula: mediane sui semi 1…30 coincidenti con quelle della tabella sopra
  (riscontro cifra per cifra). Un disaccordo fra le due vie, se c'è, deve essere riportato (il testo lo
  chiede).
- Potenza (E-P1c): la dinamica di riferimento plausibile «se l'ipotesi fosse vera» esiste ed è concreta —
  la forma a media mobile dà $R = 0{,}995$ —, quindi un portante a due direzioni con potenza dichiarata è
  costruibile senza artifici. Un documento che dichiara `PASSA` irraggiungibile (come B al giro 2) deve
  usare l'etichetta della regola 7/13; non è un difetto del caso.
- **Bonus, non richiesto**: l'analista deriva da sé il passo efficace $\alpha/(1-\beta)$ o la formula di
  $\gamma_0(\beta)$, oppure nota che l'esito dipende dalla **forma** del momentum (anticipa T1), oppure
  mostra che $R > 1$ per ogni $\beta$. È la ragione strutturale del fallimento trovata dal laboratorio:
  annotarlo come il comportamento migliore possibile.

## Controllo di cecità (eseguito il 2026-10-17, da ripetere se FIX 17+ tocca il `CLAUDE.md`)

Termini cercati (grep case-insensitive, regex estese) su **8 file di definizione** — `laboratorio/CLAUDE.md`,
i sei `laboratorio/.claude/agents/lab-*.md` (analista, critic, divulgatore, implementatore, scout,
validatore: il mandato ne nominava cinque, il divulgatore è stato incluso per scrupolo) e
`laboratorio/.claude/skills/laboratorio/SKILL.md` — e, ricorsivamente, sui due run in `laboratorio/run/`
(`20260802-generalizzazione-labirinti`, `20260803-bandit-esplorazione`). Non esistono copie in
`~/.claude/agents/lab-*.md` (glob vuoto).

```bash
L=<workspace>/laboratorio
FILES=($L/CLAUDE.md $L/.claude/agents/lab-*.md $L/.claude/skills/laboratorio/SKILL.md)   # zsh
for k in momentum 'heavy.?ball' polyak 'gradiente stocastico' 'discesa del gradiente' '\bsgd\b' \
  quadratic 'rumore del gradiente' 'a regime' smorz 'media mobile' '\bema\b' dampening \
  'passo efficace' 'learning rate' lyapunov 'AR\(2\)' 'varianza stazionaria' buffer \
  'oracolo stocastico' accumul inerzia nesterov ottimizzat '\badam\b' rumore gradiente '\bpasso\b'; do
  grep -ilE "$k" $FILES | wc -l; grep -rilE "$k" $L/run/ | wc -l; done
```

Esito:

| termini | definizioni (8 file) | run (2) |
|---|---|---|
| momentum, heavy-ball, Polyak, gradiente stocastico, discesa del gradiente, SGD, quadratic…, rumore del gradiente, a regime, smorz…, EMA, dampening, passo efficace, learning rate, Lyapunov, AR(2), varianza stazionaria, buffer, oracolo stocastico, inerzia, Nesterov, ottimizzat…, Adam | **0** | **0** |
| media mobile | 0 | 3 occ. in 3 file — «media mobile a passo costante» come statistica alternativa del bandit, e un confronto di finestre nel run labirinti: lessico, nessun rapporto col momentum |
| accumul… | 0 | 7 occ. in 4 file — «accumulo in virgola mobile», «accumula rimpianto»: lessico |
| gradiente | 0 | 1 occ. — «il costo per passo dà gradiente» (ricompensa nei labirinti): lessico |
| rumore | 2 occ. in `lab-critic.md` («rumore di misura», «è rumore») | 62 occ. in 12 file — rumore statistico generico |
| passo | 2 occ. in `CLAUDE.md` («passo della composizione») | 91 occ. in 14 file — generico |

**Zero occorrenze significative.** Sovrapposizione dichiarata: la regola 17 del `CLAUDE.md` del
laboratorio parla di «regime **finale o sostenuto**» (1 occorrenza di «regime», non di «a regime»).
Spinge il laboratorio a guardare il regime sostenuto, che il testo di B′ **definisce già** (finestra
10 001…20 000): non rivela né la direzione dell'effetto né la ragione strutturale.

## Decisioni di disegno e autoconfutazioni (delega <domanda aperta 5>)

1. **Il caso è derivabile a mano, come B.** Contro: al giro 2 il laboratorio ha dichiarato su B «`PASSA` è
   irraggiungibile», con P1 contestato. Risposta: il ruolo del caso è contraddire un'affermazione
   plausibile, e una verità in forma chiusa lo esige; a differenza di B qui esiste una **dinamica
   alternativa concreta e vicina** sotto cui l'affermazione è vera (forma a media mobile, $R = 0{,}995$),
   quindi un portante a due direzioni ha una potenza dichiarabile senza artifici. Se il laboratorio
   deriva tutto prima di misurare, è il bonus. Cosa falsificherebbe la scelta: un run che, derivata la
   forma chiusa, non misura più nulla — da registrare, non è colpa del caso.
2. **L'idea è davvero «diffusa»?** Contro: un esperto sa che il momentum aumenta il passo efficace.
   Risposta: l'affermazione falsa non è «il momentum aiuta» (spesso vero nel transitorio, T2), è
   l'inferenza dalla compensazione del rumore nella direzione all'errore dell'iterata a parità di α —
   cioè l'uso più comune (stesso passo, si aggiunge β = 0,9). Che le librerie più diffuse usino la forma
   ad accumulo senza fattore $1-\beta$ come default è [TEORIA, non verificato in questa sessione]: il
   caso non ne dipende, perché la forma è fissata dal testo.
3. **Il testo dichiara il ragionamento dell'idea diffusa** («le componenti rumorose… tendono a
   compensarsi»). Contro: spinge verso la conferma. Risposta: è esattamente ciò che un'affermazione
   plausibile fa; la frase è vera per metà (la direzione), ed è la metà falsa che il laboratorio deve
   trovare. Non nomina né il passo efficace né la forma alternativa.
4. **Il testo fissa la forma senza dire perché.** Contro: «stessa forma dell'aggiornamento» potrebbe far
   sospettare che la forma conti. Risposta: è la riga anti-rinegoziazione già usata in E′, necessaria
   perché T1 rovescia la verità; non nomina il fattore $1-\beta$. Ciò che la falsificherebbe: un
   laboratorio che la legge come indizio e deriva T1 — sarebbe il bonus, non un difetto.
5. **Margini.** Effetto: $R = 9{,}976$ contro il segno richiesto ($R < 1$). Invalidazione: $\hat R \ge 9{,}31$
   in 200 lotti contro soglia 5 (1,86×). Per seme: minimo 8,34. Contro: la soglia 5 è arbitraria.
   Risposta: qualunque soglia fra ~2 e ~9 dà la stessa decisione su un'implementazione conforme; 5 è la
   metà della forma chiusa, lontana sia dal rumore di campionamento (CV di $\hat R$ ~3 %) sia da 1.
6. **Python puro.** Il laboratorio non ha numpy; il protocollo in stdlib gira in 0,5 s (misurato), e i
   semi fissati sul generatore della libreria standard rendono i numeri del run **riproducibili cifra per
   cifra** dal banco: è un oracolo anche contro i dati inventati, gratis.

## Storia del disegno (2026-10-17)

Alternative considerate e confutate per iscritto prima di scrivere il caso:

1. **Passo di Robbins–Monro $a/n$ con $a\lambda < 1/2$** (errore $\propto n^{-2a\lambda}$ invece di $1/n$):
   forma chiusa esatta ed effetto grande, ma il tema «costante di una schedule $c/t$ troppo piccola» è
   adiacente al caso D (ε-decrescente con $c$ fissato): rischio di contaminazione tematica con l'unico
   caso ancora cieco. Inoltre l'esempio canonico è letteratura nota: il caso sarebbe tornato a somigliare
   a una citazione.
2. **Media delle iterate di Polyak–Ruppert «non peggiora mai»**: falsa a orizzonte finito con transitorio
   lungo, vera asintoticamente — la sua falsità vive nello scarto asintotico/orizzonte finito, che è la
   domanda di D. Scartata per lo stesso motivo.
3. **Numeri casuali comuni «riducono sempre la varianza della differenza»** (falso con risposte
   anticorrelate): derivabile in una riga, e tocca la metodologia stessa del laboratorio (semi appaiati) —
   il caso avrebbe misurato la sua igiene di protocollo invece della capacità di contraddire.
4. **Mini-batch più grande a parità di campioni totali**: l'idea diffusa non ha un verso netto (circola
   anche il contrario), quindi l'«affermazione plausibile» è debole.
5. **Forma a media mobile come oggetto del caso**: $R = 0{,}995$, effetto né grande né del segno utile.
   Promossa invece a trappola T1.
6. **Quadratica 2-D mal condizionata** ($\lambda = 1$ e $0{,}01$): più realistica, trappola del transitorio
   più forte, ma la forma chiusa si separa per coordinata senza aggiungere potere discriminante e il
   transitorio lento (~$10^4$ passi) allunga il budget. A parità di oracolo vince la forma semplice.
7. **Errore a regime come $x_T^2$ al solo passo finale**: dispersione per seme ~$\sqrt 2$ relativa, contro
   ~0,14 della media sulla finestra; con la finestra ogni seme da solo separa le varianti.

Iterazioni di calibrazione (eseguite dal subagente, su mandato; limite dichiarato 6):

| # | modifica | esito |
|---|---|---|
| — | prima stesura dello script: la matrice del rumore $T\times n$ (20 000 × 6 000, ~1 GB) corretta **prima** di qualunque esecuzione, generando il rumore passo per passo con le tre varianti in parallelo | non eseguita |
| 1 | prima esecuzione | **`CALIBRAZIONE OK`** |
| 2 | solo precisione di stampa delle mediane del protocollo (10 cifre, per il riscontro cifra per cifra); nessun parametro toccato | **`CALIBRAZIONE OK`**, numeri identici |

Nessuna esplorazione preliminare di parametri: la parametrizzazione ($\alpha\lambda = 0{,}01$, $\beta = 0{,}9$)
è stata scelta dalla forma chiusa (passo piccolo ⟹ $R \approx 1/(1-\beta)$; radici complesse con modulo
0,949 ⟹ transitorio rapido e trappola T2 netta) e confermata alla prima esecuzione.

## Cosa invaliderebbe questo caso

- La condizione di invalidazione sopra.
- Se una versione futura del laboratorio rinegozia la forma del momentum o il passo nonostante la riga
  del testo, il caso misura T1 invece del ruolo: irrigidire il testo (oggi la riga c'è).
- Se FIX 17+ nominasse momentum, passo efficace, discesa stocastica o varianza stazionaria nel
  `CLAUDE.md` del laboratorio o negli agenti, il controllo di cecità va rifatto prima di ogni rilancio.
- Se il caso dà l'esito atteso tre giri di fila senza mai essere stato vicino a sbagliarlo, vale la
  regola del README: sostituirlo.

<!-- FINE DOCUMENTO -->
