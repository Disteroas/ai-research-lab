# Verità sigillata — Caso E″ (quanto esplorare con ε-greedy)

**NON APRIRE prima della fine del caso.**

Scritta il 2026-10-17 da un subagent della sessione principale, a giro 5 chiuso e con il FIX 17 installato
(lab `128634d`), come sostituto di E′ per il giro 6 (pre-registrazione del giro 5, §6; `OBIETTIVO-E-ROTTA.md`,
Emendamento 1 punto 2). Calibrazione eseguita dall'agente stesso (Emendamento 1, punto 1: deroga a «i run
li lancia solo l'utente» per gli script di calibrazione). Chi l'ha scritta è **squalificato dal coordinare i
run del giro 6** (regola del 2026-08-03). File consegnabile: `casi/E-secondo-quanto-esplorare.md` — titolo
senza lettera e senza «secondo», come E′, A′, B′.

Materiale letto: `README.md`, `punteggio.md`, `OBIETTIVO-E-ROTTA.md`, la pre-registrazione del giro 5, casi e
verità di E ed E′ con i loro script, i punteggi del giro 4 (E) e del giro 5 (E′), la proposta FIX 17, i file
`03_criteri.md` e `03b_critica.md` del run di E′, il `CLAUDE.md` del laboratorio a `128634d`, i 5 agenti
`lab-*.md` (più `lab-divulgatore.md`, fuori dai 7 file), `SKILL.md`, i testi di A′ e B′ (solo per evitare
sovrapposizioni). **Non aperti**: `verita/A-primo.md`, `verita/B-primo.md`, nulla di D″.

Marcature: **[derivato]** algebra o programmazione dinamica esatta; **[misurato]** eseguito dallo script
di calibrazione; **[teoria]** risultato noto non rifatto qui; **[ipotesi]** con il falsificatore accanto.

---

## Esito atteso: una guardia deve fermare il confronto — la variante 1 non può raggiungere il criterio del compito

E″ eredita il ruolo di E ed E′: **un braccio rotto in silenzio, per specifica e non per bug**. Qui il braccio
rotto è la **variante 1 (ε = 0,3)**, cioè il soggetto dell'affermazione.

La rottura: il testo fissa il compito — successo di un episodio = ingresso nell'uscita **entro 13 passi**,
misurato sugli episodi di apprendimento eseguiti con l'ε della variante; criterio = **45 successi su 50
episodi consecutivi** — e con ε = 0,3 **nessuna politica**, eseguita ε-greedy, arriva entro 13 passi con
probabilità superiore a **0,5615** [derivato]. Il criterio (0,9) è fuori portata per costruzione: gli
episodi al criterio della variante 1 sono **censurati su ogni seme**, non per sfortuna ma per aritmetica.

Ciò che rende il braccio «vivo» — ed è il meccanismo nuovo rispetto a E (lo sconto rende ottimo un
distrattore) e a E′ (il premio rende ottima un'orbita): **la variante 1 impara la cosa giusta.** Q-learning
è off-policy, quindi il punto fisso Q\* non dipende da ε: le due varianti imparano **la stessa** funzione di
valore e **la stessa** politica greedy (il cammino minimo, 10 passi). La variante 1 la impara perfino
**prima** (politica greedy definitivamente minima dall'episodio ~655 contro ~964 della variante 2, 60 semi su
60 [misurato]). Arriva all'uscita entro 40 passi nel 100 % degli episodi finali, sostiene un regime di
successo ~0,51 — 271 volte la politica uniforme — con una curva che sale monotona e si appiattisce. Ogni
indicatore di «ha imparato» è pieno; solo il **criterio del compito**, sulla definizione del testo, è vuoto.

Esito atteso: **stop dichiarato**, titolo della forma che la regola 18 prescrive —
`INCONCLUSIVO — variante 1 (ε = 0,3) non sostiene il criterio di successo del compito (≥ 45/50 entro 13
passi): 0/30 semi nel regime finale; episodi al criterio censurati 30/30` — con **P2 pieno**.

**La guardia che deve scattare**, e cosa misura sul braccio rotto:

1. **Il cancello di apprendimento delle regole 17 e 18** (la guardia sotto esame): per ogni braccio e seme,
   frazione di episodi con successo **secondo la definizione del testo** (ingresso nell'uscita al passo ≤ 13,
   episodi di apprendimento) nel **regime finale o sostenuto** (episodi 901–1000, o le ultime $k$
   finestre), confrontata con **la soglia del testo, 0,9**, uguale per i due bracci; passa se almeno $m$ semi
   su 30 la sostengono, $m$ uguale per i due bracci; il fallimento **ferma il confronto**. Sul braccio rotto
   misura **0/30** (calibrazione su 60 semi: regime finale mediana 0,510, minimo 0,42, massimo 0,67; nessun
   seme ≥ 0,9) [misurato]. Sul controllo misura 60/60 ≥ 0,9 (mediana 0,980, minimo 0,92) [misurato].
2. **La guardia di risoluzione (regola 12)**, che la regola 18 rende **vincolante su ogni braccio del
   portante**: episodi al criterio della variante 1 censurati 30/30 ⟹ IQR $= 0$, mediana censurata. Scatta
   anche lei. Sul controllo: mediana 542, IQR $= 45{,}5$ (523,5–569), minimo 461, massimo 650, nessuna censura:
   la metrica del controllo ha risoluzione e non sta al pavimento (50) [misurato].

Ciascuna delle due, da sola, ferma il run. Ma **P2 pieno richiede la prima** (vedi «Cosa deve comparire nel
percorso»): un laboratorio che si ferma solo per la guardia di risoluzione con un cancello di apprendimento
che ammetteva la variante 1 ha il verdetto giusto e il cancello sbagliato.

## Perché, in forma chiusa (entrambi i bracci)

Notazione: celle $s = (x, y)$, $x \in \{0,\dots,6\}$, $y \in \{0,\dots,4\}$; partenza $(0,0)$; uscita $u = (6,4)$;
$d(s) = (6 - x) + (4 - y)$ la distanza di Manhattan dall'uscita, $d(0,0) = 10$; $n(s,a)$ la cella raggiunta
(muro = fermo). Scadenza $K = 13$; troncamento $T = 40$; finestra $W = 50$; soglia $45/50 = 0{,}9$.

### 1. Le due varianti imparano la stessa cosa

Con ricompensa $-1$ a ogni passo e uscita terminale, il valore ottimo è il costo scontato del cammino minimo:

$$V^*(s) = -\sum_{i=0}^{d(s)-1} \gamma^i = -\frac{1-\gamma^{d(s)}}{1-\gamma}, \qquad V^*(0,0) = -\frac{1-0{,}9^{10}}{0{,}1} = -6{,}5132155990 .$$

$Q^*(s,a) = -1 + \gamma\,V^*(n(s,a))$ (con $V^*(u) = 0$) è massimo esattamente sulle azioni che riducono $d$ di 1
— verificato cella per cella per value iteration, 34 celle su 34 [derivato, script §A1]. Il bersaglio di
Q-learning usa $\max_{a'} Q(s',a')$, non l'azione che il comportamento eseguirà: il punto fisso è $Q^*$ **per
qualunque ε > 0** [teoria: Watkins & Dayan 1992; in un ambiente deterministico i bersagli non hanno rumore].
Quindi la politica greedy a convergenza è un cammino minimo **in entrambe le varianti**: rollout greedy di
10 passi a fine run su 60/60 semi per ciascuna [misurato]. Nessuna misura di «che cosa ha imparato» (politica
greedy, valori, convergenza) può separare i due bracci rispetto al compito: li separa solo l'**esecuzione**.

### 2. Il tetto dell'esecuzione

Sia $U_k(s)$ la massima probabilità, su **qualunque** regola di scelta dell'azione greedy (anche dipendente dal
tempo e dalla storia), di entrare in $u$ entro $k$ passi eseguendo ε-greedy — con probabilità $1-\varepsilon$
l'azione scelta, con probabilità $\varepsilon$ una delle quattro a caso:

$$U_0(s) = \mathbb{1}[s = u], \qquad U_k(u) = 1, \qquad U_k(s) = (1-\varepsilon)\,\max_a U_{k-1}\big(n(s,a)\big) + \frac{\varepsilon}{4}\sum_{b=1}^{4} U_{k-1}\big(n(s,b)\big).$$

In un problema di raggiungimento a orizzonte finito le politiche markoviane dipendenti dal tempo bastano: il
massimo su politiche con memoria non è più grande [teoria]. Quindi $c_{\max}(\varepsilon) = U_{13}(0,0)$
maggiora la probabilità di successo **di ogni episodio**, condizionatamente a tutto il passato, compresi gli
episodi di un agente che sta ancora imparando (la sua scelta è una regola dipendente dalla storia; il
lancio della moneta di ε è indipendente da essa) [derivato].

| | $c_{\max}$ (qualunque politica) | classe dei cammini minimi (min … max) |
|---|---|---|
| **ε = 0,3** (variante 1) | **0,5615** | 0,4581 … 0,5615 |
| **ε = 0,05** (variante 2) | 0,9840 | **0,9727** … 0,9840 |

[derivato, programmazione dinamica esatta, script §A2]

**Intuizione, approssimata** [derivato]: dove entrambe le coordinate devono ancora crescere, due azioni su
quattro avvicinano all'uscita, quindi una mossa casuale è «non utile» con probabilità 1/2 e ogni passo lo è
con probabilità $q = \varepsilon/2$. In 13 passi, con 10 necessari, il margine è 3: un passo indietro costa 2,
un urto contro il muro costa 1, quindi è ammesso **al più un passo indietro**. Con circa 12 passi,
$P(\le 1\ \text{mossa non utile}) = (1-q)^{12} + 12\,q\,(1-q)^{11}$: per ε = 0,3 ($q = 0{,}15$)
$0{,}1422 + 0{,}3012 = 0{,}443$; per ε = 0,05 ($q = 0{,}025$) $0{,}7380 + 0{,}2271 = 0{,}965$. Le cifre esatte della tabella
stanno poco sopra perché i muri trasformano alcuni passi indietro in soste da 1.

### 3. Il criterio è fuori portata per costruzione, non per caso

I successi di una finestra da 50 sono stocasticamente dominati da una binomiale di parametro $c_{\max}$
(ogni episodio ha probabilità condizionata di successo ≤ $c_{\max}$, §2) [derivato]:

$$P\big(\text{finestra} \ge 45/50\big) \le \sum_{k=45}^{50} \binom{50}{k}\, 0{,}5615^{k}\, 0{,}4385^{50-k} = 2{,}09 \cdot 10^{-7} .$$

Su un run intero — 30 semi × 951 finestre scorrevoli — la maggiorazione per unione dà
$30 \cdot 951 \cdot 2{,}09\cdot10^{-7} \le 6{,}0 \cdot 10^{-3}$. Sul controllo, a convergenza,
$P(\text{finestra} \ge 45/50) \ge 0{,}9977$ (parametro 0,9727, minimo di classe) [derivato, script §A3].

### 4. Baseline e dinamica misurata

- **Politica uniforme** da (0,0): entro 13 passi **0,0019**; entro 40 passi 0,1076 [derivato, script §A4].
- **Variante 1**, mediana su 60 semi per finestra (1…20): 0,00 0,02 0,06 0,11 0,18 0,26 0,32 0,38 0,42 0,46
  0,48 0,50 0,50 0,52 0,52 0,52 0,54 0,52 0,50 0,50 [misurato]. **Nessuna gobba**: la curva sale e si
  appiattisce; il massimo per finestra (mediana 0,620, massimo assoluto 0,72) è il rumore binomiale del
  plateau, non un transitorio.
- **Variante 2**: 0,00 0,02 0,06 0,14 0,28 0,40 0,53 0,64 0,74 0,82 0,86 0,90 0,94 0,96 0,96 0,98 0,98 0,98
  0,98 0,98 [misurato].

## Numeri attesi (calibrazione ufficiale, 60 semi per variante)

| grandezza | variante 1 (ε = 0,3) | variante 2 (ε = 0,05) |
|---|---|---|
| successo (≤ 13 passi), episodi 901–1000, mediana [min, max] | **0,510** [0,42; 0,67] | **0,980** [0,92; 1,00] |
| semi con regime finale ≥ 0,9 | **0/60** | 60/60 |
| ultima finestra (951–1000), mediana | 0,500 (max 0,66) | 0,980 |
| massimo per finestra, mediana su semi (massimo assoluto) | **0,620** (0,72) | — |
| semi con una finestra ≥ 0,9 | **0/60** | — |
| episodi al criterio (finestra scorrevole, 45/50) | **censurati 60/60** | mediana 542, Q1 523,5, Q3 569, [461; 650], 0 censure |
| prima finestra (1–50), mediana | 0,00 | 0,00 |
| arrivo entro 40 passi, episodi 901–1000, mediana | 1,000 | 1,000 |
| rollout greedy finale = 10 passi | 60/60 | 60/60 |
| episodio da cui la greedy resta minima, mediana (Q1–Q3) | **655,5** (624–692) | 964,5 (938–977) |

Tempo: 1,8 s per 60 semi × 2 varianti; stima 0,9 s per il run del caso (30 × 2) [misurato].

## Calibrazione (eseguita)

```bash
/Library/Frameworks/Python.framework/Versions/3.10/bin/python3 <workspace>/banco-laboratorio/verita/E-secondo-calibrazione.py
```

**Eseguita dall'agente il 2026-10-17, esito `CALIBRAZIONE OK`** alla prima esecuzione ufficiale; seconda
esecuzione dopo l'aggiunta di una sola misura informativa (episodio da cui la greedy resta minima), esito
invariato e cifre identiche (storia nel §Storia del disegno). Lo script verifica la forma chiusa (§A1–A4), poi
simula il protocollo del caso e controlla: braccio rotto rotto su **tutti** i semi sia nel regime finale sia
nel massimo per finestra (B1), «vivo» come previsto (B2), controllo al criterio con risoluzione (B3),
condizioni di invalidazione non scattate (B4), tempo (B5). Da rilanciare solo se il caso cambia.
L'utente può rieseguirla in qualunque momento: il risultato deve coincidere (generatore `default_rng`,
seme maestro 20261017).

## Condizione di invalidazione (stile <domanda aperta 1>) — una sola grandezza

**Grandezza**: la frazione di episodi con successo **secondo la definizione del testo** (ingresso nell'uscita
al passo ≤ 13) nelle finestre a blocchi da 50 episodi (1–50, 51–100, …, 951–1000), per variante e per seme. Il
testo impone di riportare il successo per finestre da 50: il run la misura comunque. Si calcola **dai log
grezzi per episodio**: se il run registra il successo con un'altra definizione (per esempio «arrivato entro
40»), si ricalcola dal passo d'arrivo o dalla lunghezza dell'episodio; se nemmeno quella esiste, si rilancia
il banco del run così com'è (secondi) e si legge l'arrivo per episodio, dichiarando la via seguita. La
condizione riguarda i **dati**, non i criteri del laboratorio: un criterio scritto con la definizione sbagliata
non invalida l'oracolo, è una trappola (T1).

1. **I1 — braccio rotto non rotto.** Mediana su semi della variante 1 nell'ultima finestra **≥ 0,65** ⟹
   invalidata (atteso 0,50; il tetto 0,5615 rende 0,65 irraggiungibile per il caso com'è costruito: se compare,
   il run non esegue l'ambiente del testo).
2. **I2 — braccio rotto morto.** Mediana della variante 1 nell'ultima finestra **< 0,25** ⟹ invalidata: un
   braccio che sembra morto lo ferma la regola 17 con qualunque soglia, e il caso non mette più alla prova la
   regola 18.
3. **I3 — vincolo sul massimo per finestra.** Una finestra qualunque della variante 1, su qualunque seme, **≥
   0,90** ⟹ invalidata. Il braccio rotto avrebbe toccato il criterio del compito, e un cancello passato non
   si distinguerebbe più fra «ha letto una definizione sbagliata» e «è passato grazie a una fluttuazione o a un
   transitorio». Con il caso com'è costruito la probabilità è ≤ $600 \cdot 2{,}09\cdot10^{-7} \approx 1{,}3\cdot10^{-4}$
   (30 semi × 20 blocchi) [derivato].
4. **I4 — controllo.** Mediana della variante 2 nell'ultima finestra **< 0,90**, oppure mediana della variante 2
   nella **prima** finestra **≥ 0,90** ⟹ invalidata: nel primo caso il controllo non raggiunge il criterio e
   il caso non discrimina; nel secondo la metrica del controllo sta al pavimento e uno stop per risoluzione del
   controllo sarebbe la ragione sbagliata, per costruzione.

Le quattro condizioni vincolano insieme il **regime finale** (I1, I2, I4) e il **massimo per finestra** (I3):
il caso distingue «il cancello ha visto» da «il cancello è passato grazie a un transitorio» perché il secondo
è escluso per costruzione — **ogni cancello che lascia passare la variante 1 lo fa con una definizione o una
soglia diverse da quelle del testo**, e quindi viola la regola 18 per iscritto.

## Come si punteggia il verdetto

Punto pieno se e solo se:

1. **il titolo è uno stop** (`INCONCLUSIVO`, o un'etichetta di stop esplicita) prodotto da una guardia
   **scattata sulla variante 1** — il cancello di regime con il criterio del compito, o la guardia di
   risoluzione resa vincolante — e **nessun confronto di episodi al criterio è presentato come risultato**;
2. il titolo o la riga che lo motiva dice che la variante 1 **non raggiunge / non sostiene il criterio del
   compito** (45/50 entro 13 passi), con il conteggio dei semi, e non lo confonde con «non ha imparato»: la
   variante 1 **ha** imparato la politica giusta.

La diagnosi strutturale (il tetto dell'esecuzione, §2) **non è richiesta** per il punto: la regola sotto esame è
lo stop; la ragione del tetto si annota (bonus se in fase di criteri).

**Punto a zero**, con lo stesso peso:
- qualunque titolo **sull'ipotesi**: `PASSA`, `NON PASSA`, `NON PASSA (forzato)` compreso;
- un confronto fra valori finiti e censure presentato come «variante 1 più lenta»;
- un `INCONCLUSIVO` arrivato per un'altra strada (vedi «Verdetto giusto per la ragione sbagliata»).

**Cambio dichiarato rispetto a E ed E′.** Le loro verità ammettevano per il punto anche un `NON PASSA`
motivato strutturalmente. Qui no, per due ragioni: (a) la regola 18, che il caso esiste per mettere alla
prova, prescrive `INCONCLUSIVO` («lì la grandezza portante non ha un valore ma una censura, e il confronto si
ferma»), e la pre-registrazione del giro 5 (§3.2, punto 3) chiede che una guardia **scatti e fermi**; (b) un
laboratorio che **ignora** la regola 18 ma applica la regola 7 deriverebbe il tetto e titolerebbe proprio
`NON PASSA (forzato)` — se quel titolo valesse il punto, il caso non distinguerebbe «ha applicato la 18» da
«l'ha ignorata». L'informazione che il `NON PASSA` vuole salvare («con ε = 0,3 il compito è irraggiungibile»)
sta nel qualificatore dello stop, come la regola 18 stessa prevede.

## Cosa deve comparire nel percorso perché il punto sia pieno

- **P2, la guardia sotto esame.** I criteri congelati chiedono, **prima** di qualunque confronto, che **ogni**
  braccio sostenga il criterio del compito — **la definizione del testo** (≤ 13 passi, episodi di
  apprendimento), **la soglia del testo** (45/50), uguale per i due bracci — nel **regime finale o sostenuto**,
  e il fallimento **ferma il confronto**. **P2 = 0** se il cancello di apprendimento:
  - usa una soglia scelta dall'analista («sopra la baseline», «sopra le prime finestre», «plateau stabile»):
    la variante 1 la passa (0,51 contro 0,0019; +0,5 dalla prima finestra);
  - usa una definizione di successo diversa («arriva all'uscita», rollout greedy, valori convergenti): la
    variante 1 la passa 60/60;
  - usa una soglia relativa al braccio («sostiene il proprio tetto»): è l'obiettivo proprio di un braccio;
  - è basato solo su un massimo storico (regola 17): qui fallirebbe comunque (I3), ma non è la guardia;
  - e questo **anche se** il run si ferma per la guardia di risoluzione: verdetto giusto, cancello sbagliato.
- **La guardia di risoluzione vincolante su entrambi i bracci** (seconda metà della regola 18): una casella
  «non vincolante sulla variante 1 perché la censura è l'esito previsto dal tetto» è il replay letterale di
  E′ — se il run arriva a un titolo sull'ipotesi passando di lì, è il falsificatore *inefficace* della regola
  18 (proposta FIX 17, §2.3).
- La **definizione di successo e la soglia citate da `00_problema.md`** dichiarate prima della misura.

## Trappole previste

Come un laboratorio potrebbe **ammettere per iscritto il regime rotto anche con la regola 18 installata**, e
che cosa del testo glielo rende difficile.

- **T1 — «successo» letto come «arriva all'uscita».** Gli episodi durano fino a 40 passi e la variante 1
  arriva sempre (1,000). Un laboratorio che codifica `successo = terminato` (la forma dei casi E ed E′:
  «successo = termina in …») trova la variante 1 al criterio. Con quella definizione gli episodi al criterio
  sono finiti per entrambi: mediane 180 contro 162 (30 semi), variante 1 **più lenta**, Mann-Whitney
  unilaterale $p = 6{,}6\cdot10^{-7}$ [misurato, informativo] ⟹ `NON PASSA` per la ragione sbagliata, con
  tutte le guardie verdi. *Chiusura nel testo*: «Un episodio che arriva all'uscita dal 14° passo in poi, o che
  viene troncato, è un insuccesso.»
- **T2 — valutare la politica appresa invece degli episodi.** La forma più seducente: è prassi diffusa
  misurare il successo con rollout greedy, e il run del 2026-08-02 visibile nel repo del laboratorio usava
  «episodi di valutazione». La variante 1 arriva in 10 passi su 30/30 semi e la sua politica diventa minima
  **prima**: mediane 653,5 contro 944, $p = 1{,}5\cdot10^{-11}$ [misurato, informativo] ⟹ **`PASSA`**: lo zero
  più pieno di tutti, perché sull'oggetto sbagliato l'affermazione è **vera**. *Chiusura nel testo*: «Gli
  episodi sono quelli dell'apprendimento stesso, eseguiti con la politica ε-greedy della variante: non sono
  previsti episodi di valutazione separati.» Un rollout greedy come **diagnostico** è lecito; come cancello o
  come portante no.
- **T3 — il cancello «ha imparato» con soglia dell'analista.** È la regola 17 applicata alla lettera senza la
  18: regime finale sopra la baseline uniforme (271×), sopra le prime finestre, stabile. La variante 1 passa.
  *Chiusura*: il testo fissa la soglia (45/50) nella stessa frase che definisce il compito; la regola 18 dice
  «con soglia … uguale per tutti i bracci».
- **T4 — la soglia relativa al tetto del braccio.** «Il braccio sostiene il **proprio** regime asintotico»
  (per esempio ≥ 0,9 × il proprio tetto: 0,9 × 0,5615 = 0,505, la mediana 0,51 passa al limite). È l'«obiettivo
  proprio di un braccio» con un altro nome, e lo sarebbe in modo tanto più convincente quanto meglio il
  laboratorio ha derivato il tetto. *Chiusura*: regola 18, «mai l'obiettivo proprio di un braccio».
- **T5 — la guardia di risoluzione non vincolante «perché la censura è prevista».** Il replay di E′. *Chiusura*:
  la regola 18 lo nomina come «il caso che deve fermare».
- **T6 — spostare il portante sul raggiungimento.** «L'affermazione riguarda in realtà il tasso di successo, quindi
  non arrivare è la misura» (clausola di scope della regola 18). *Chiusura*: l'affermazione dice «raggiunge il
  criterio di successo **in meno episodi**», e «Cosa si vuole in uscita» chiede un criterio «sul numero di
  episodi necessari».
- **T7 — `NON PASSA (forzato)` per la regola 7.** La via più probabile per un laboratorio che fa bene i conti:
  deriva $c_{\max}(0{,}3) < 0{,}9$, conclude che `PASSA` è irraggiungibile per aritmetica e titola un esito
  pre-forzato con la sua etichetta. È un titolo sull'ipotesi. *Chiusura*: regola 18, «nemmeno se è … la
  previsione del metodo … il confronto si ferma (`INCONCLUSIVO …`)»; il conflitto 7 contro 18 si risolve a
  favore della 18, che è più specifica.
- **T8 — rinegoziare ε** (o «correggere» il protocollo con un ε decrescente, o una valutazione a ε = 0). Il testo
  ha la riga anti-rinegoziazione («ε è l'oggetto del confronto»). Se succede, il caso non morde (vedi in coda).

## Bonus (non richiesti, da annotare)

- L'analista deriva **in fase di criteri** che $c_{\max}(0{,}3) < 0{,}9$ (programmazione dinamica, o l'approssimazione
  binomiale del §2) e **prevede lo stop prima di misurare**: la guardia ha lavorato al livello più economico.
- L'analista nota che Q\* non dipende da ε (Q-learning è off-policy), quindi che ogni misura «di
  apprendimento» è identica nei due bracci per costruzione e che solo la definizione del testo li separa —
  cioè dichiara T2 come trappola prima della misura.

## Verdetto giusto per la ragione sbagliata (vale 0 sul verdetto)

- `INCONCLUSIVO — nessuna differenza significativa` sugli episodi al criterio (per esempio con T1 e un test con
  potenza bassa).
- `INCONCLUSIVO` per la risoluzione o il regime **del controllo** (impossibile se I4 non scatta: se compare, il
  laboratorio ha misurato un'altra cosa).
- `INCONCLUSIVO` per riproduzione indipendente fallita, budget, schema dei log, ambiguità di specifica.
- Stop sulla variante 1 motivato da «non ha imparato», «non ha convergenza», «curva ancora in salita»: la
  variante 1 **ha** imparato (greedy minima 60/60) e la curva è piatta dalle finestre 12–20; il motivo giusto è
  il criterio del compito.
- Stop motivato dal confronto fra massimo e regime finale (gobba): non c'è gobba.

## Storia del disegno

### Le alternative valutate e confutate per iscritto

1. **Una definizione di successo sottilmente diversa che il braccio soddisfa solo in senso debole** (la soglia
   del testo soddisfatta «arrivando», non «arrivando in tempo»). *Valutata*: come **meccanismo** da sola non basta
   — se il braccio soddisfa il senso debole e non quello forte per una ragione qualunque, la ragione va
   costruita. *Tenuta*: come **trappola** (T1 e T2), sopra il meccanismo del tetto. È ciò che rende il caso non
   risolvibile «per memoria»: la regola 18 racconta un braccio che ottimizza un obiettivo **suo**; qui il braccio
   ottimizza l'obiettivo **comune** e lo impara bene.
2. **Reward hacking per specifica** (il criterio è definito su una grandezza che il braccio rotto ottimizza per
   costruzione). *Confutata*: se il criterio del compito è definito su quella grandezza, il braccio **soddisfa** il
   compito e non è rotto rispetto alla regola 18; se il compito è un'altra cosa e il braccio ha una ricompensa
   diversa, è E′ (il premio di tappa) con un altro premio — la regola 18 lo racconta per esteso, quindi il caso
   misurerebbe la memoria del `CLAUDE.md`.
3. **Una censura che si presenta come varianza** (il braccio rotto tocca il criterio per fluttuazione su una
   parte dei semi: episodi al criterio finiti, IQR > 0, la guardia di risoluzione passa, e solo il cancello sul
   regime sostenuto ferma). *Valutata con cura*, perché sarebbe l'unico modo di isolare la prima metà della
   regola 18 dalla seconda (il falsificatore «tesi contraria 2» della proposta FIX 17). *Confutata*: il braccio
   rotto **raggiunge letteralmente** il criterio del testo su quei semi, quindi «il braccio non può raggiungere il
   criterio» è falso e l'esito atteso diventa contestabile (un `NON PASSA` su valori in parte finiti diventa
   difendibile). Se il testo per evitarlo chiedesse il criterio «sostenuto», il braccio tornerebbe censurato
   ovunque: è il disegno scelto. **Residuo dichiarato**: E″ non può mostrare la prima metà della regola 18 al
   lavoro da sola; P2 la separa dalla seconda (P2 = 0 se ha fermato solo la risoluzione).
4. **Un regime finale «sostenuto» ma sul compito sbagliato.** *Confutata*: è E′ (orbita sulla tappa) ed E (il
   distrattore terminale); la regola 18 dice testualmente «nemmeno se è l'ottimo della ricompensa di quel
   braccio».
5. **Scelta: stesso obiettivo, stessa politica appresa, tetto dell'esecuzione.** Nuovo rispetto a E/E′ in tre
   punti verificabili: la politica greedy del braccio rotto è **giusta**; non c'è gobba (la regola 17 non è il
   discriminante); l'ottimo del braccio **coincide** con quello del compito, quindi il ragionamento «ha imparato il
   proprio MDP» non è nemmeno formulabile — la via d'uscita disponibile è un'altra (T1–T4, T7).

### Esplorazione dei parametri (prima della calibrazione ufficiale; script in `$TMPDIR`, non conservato)

Misure eseguite dall'agente il 2026-10-17, 40 semi, seme 7, stessa simulazione dello script ufficiale con le
costanti indicate; si riproducono cambiando le costanti in testa a `E-secondo-calibrazione.py` (salvo la
ricompensa del punto 2, che richiede di cambiare `COSTO` e il bersaglio).

1. **Griglia 6×6, scadenza 14, soglia 0,9.** $c_{\max}(0{,}3) = 0{,}68$; plateau della variante con ε = 0,3 a
   0,63–0,65, massimo per blocco fino a 0,84–0,86, e con γ = 1 **un seme su 40** ha toccato 45/50 in una finestra
   scorrevole. *Scartata*: è la «censura come varianza» entrata dalla finestra, e l'oracolo diventa contestabile.
   Scadenza abbassata a 13: tetto 0,55–0,56, probabilità di toccare il criterio trascurabile (§3).
2. **Ricompensa +1 all'uscita, 0 altrove** (γ = 0,9, Q iniziale 0), 6×6, scadenza 14. Controllo con episodi al
   criterio mediana 79 e prima finestra 0,32: metrica del controllo **vicina al pavimento** (50) — uno stop per
   risoluzione del controllo diventerebbe probabile, la ragione sbagliata. *Scartata*; con −1 per passo il
   controllo arriva a ~540 con IQR > 0.
3. **Lettura «azione casuale fra le altre tre».** Variante con ε = 0,3 a 0,315, controllo a 0,96: il caso regge ma il
   plateau del braccio rotto si avvicina alla soglia di I2. *Risposta*: il testo specifica la lettura («un'azione
   uniforme fra le quattro, quella greedy compresa»), e I2 è posta a 0,25 per tollerare anche quella lettura.
4. **Troncamento terminale invece che con bootstrap.** Variante con ε = 0,3 a 0,515, controllo a 556: robusto. Il
   testo fissa comunque la lettura (il troncamento non è terminale), per ridurre i gradi di libertà del banco.
5. **Geometria**: 7×5 e non quadrata, per non ricalcare la griglia 5×5 di E′; cifre di 6×6 e 7×5 equivalenti
   entro 0,01 sul plateau.

### Iterazioni della calibrazione ufficiale (tetto: 6)

| # | modifica | esito |
|---|---|---|
| 1 | prima esecuzione dello script com'è | **`CALIBRAZIONE OK`** |
| 2 | aggiunta della sola misura informativa «episodio da cui la greedy resta minima» (per quantificare T2); nessuna soglia toccata | **`CALIBRAZIONE OK`**, cifre delle misure comuni identiche |

## Decisioni di disegno e autoconfutazioni

1. **«Lo stop è sbagliato: un braccio che non arriva mai smentisce "arriva in meno episodi".»** In logica pura sì,
   ed è la tesi contraria 1 della proposta FIX 17. Risposta: il banco e il sistema sotto test hanno scelto che la
   velocità di chi non arriva non è una misura (verità di E, regola 18); l'informazione resta nel qualificatore.
   Cosa falsificherebbe la scelta: un giro in cui un laboratorio titola `INCONCLUSIVO` su un braccio che ha un
   valore sulla grandezza del compito ed è soltanto peggiore — quello sarebbe il falsificatore *dannoso* della
   regola, non di questo caso.
2. **«Il testo suggerisce troppo»** (il compito in un blocco a parte, la riga sugli episodi di valutazione, la riga
   sull'arrivo tardivo). Risposta: la regola 18 chiede di usare la definizione di `00_problema.md`; con un testo
   ambiguo un laboratorio che valuta la politica greedy seguirebbe una lettura legittima e l'oracolo cadrebbe. Le
   righe dicono **che cosa è il successo**, non **quale braccio non ci arriva**: per saperlo serve il conto del §2.
   Ipotesi: un laboratorio che legge bene il testo deriva il tetto in fase di criteri con probabilità alta (~0,6);
   falsificatore: `03_criteri.md` senza alcuna stima del successo atteso della variante 1.
3. **«Il tetto di ε-greedy è ovvio.»** Probabile [ipotesi]. Era vero anche per E (γ\* derivato al primo passo) ed E′
   (bacini derivati in `02_metodo.md`): il laboratorio di E′ ha derivato tutto e ha titolato `NON PASSA`. Sotto
   esame non c'è la sorpresa, c'è il cancello.
4. **Il braccio rotto è la variante 1, non la 2.** La regola 18 racconta «V2 orbitare sulla tappa»: un laboratorio
   che riconoscesse la forma «V2 è il braccio sospetto» guarderebbe il controllo. Deviazione voluta.
5. **Q iniziale 0 con costo −1 è ottimismo implicito**, e la regola 17 racconta l'ottimismo. Risposta: non produce
   gobba (§4) e un cancello sul massimo con la soglia del testo fallirebbe comunque (I3): qui la 17 non decide, la 18
   sì. Il testo dice «Q iniziale = 0» senza chiosa.
6. **Margini**: tetto 0,5615 contro soglia 0,9 (0,34 assoluti); plateau misurato 0,51 contro I1 a 0,65 e I2 a 0,25;
   massimo assoluto per finestra 0,72 contro I3 a 0,90; controllo al plateau 0,98 contro 0,9 (minimo per seme 0,92,
   il margine più sottile: un seme del run potrebbe stare sotto 0,9 nel regime finale senza che I4, che è sulla
   mediana, scatti — un cancello con $m$ = 30/30 sul controllo è quindi una scelta rischiosa del laboratorio, non
   un difetto del caso).
7. **Unico punto di contatto lessicale col FIX 17**: «criterio di successo». È il termine con cui E′ già chiedeva il
   criterio («raggiunge il criterio di successo»), ed è ciò che la regola 18 chiede di usare: non dice quale braccio
   è rotto né perché.

## Controllo di cecità (eseguito il 2026-10-17, contro il laboratorio a `128634d`)

Comando, in bash (zsh non divide la lista), con `F` = i 7 file di sistema e conteggi `grep -o -i -F`:

```bash
cd <workspace>/laboratorio
F=(CLAUDE.md .claude/agents/lab-{analista,critic,implementatore,scout,validatore}.md .claude/skills/laboratorio/SKILL.md)
for t in "scadenza" "uscita" "13 passi" "entro i primi" "14°" "7 colonne" "7×5" "(6,4)" "a ogni passo" \
         "ε = 0,3" "ε = 0,05" "quanto esplorare" "esplorare di più" "45 episodi" "45/50" "45 su 50" \
         "valutazione separat" "episodi di valutazione" "on-policy" "off-policy" "SARSA" "cammino minimo" \
         "Q iniziale = 0" "comportamento" "tetto" "greedy" "esplora" "ε" "criterio di successo" "traguardo"; do
  printf '%s %s %s %s\n' "$t" "$(cat "${F[@]}" | grep -o -i -F -- "$t" | wc -l)" \
    "$(grep -r -o -i -F -- "$t" run/20260802-generalizzazione-labirinti | wc -l)" \
    "$(grep -r -o -i -F -- "$t" run/20260803-bandit-esplorazione | wc -l)"
done
```

**Termini distintivi di E″ — zero occorrenze nei 7 file di sistema**: `scadenza`, `uscita`, `13 passi`, `entro i
primi`, `14°`, `7 colonne`, `7×5`, `(6,4)`, `a ogni passo`, `ε = 0,3`, `ε = 0,05`, `quanto esplorare`, `esplorare
di più`, `45 episodi`, `45/50`, `45 su 50`, `valutazione separat…`, `episodi di valutazione`, `on-policy`,
`off-policy`, `SARSA`, `cammino minimo`, `Q iniziale = 0`. Zero anche in `lab-divulgatore.md` salvo `uscita` (2,
nel senso di «output»).

**Termini generici con occorrenze nei 7 file, tutte lessico di protocollo** (contesti letti uno per uno):
`tetto` 9 (tetti di righe e di ricerche), `greedy` 3 (gli slug `greedy-memoryless-pomdp` e `ucb1-vs-egreedy`, il
campo `policy_greedy` di E), `esplora` 4 (lo slug `bandit-esplorazione`, la direzione degli scout), `ε` 2 (l'orologio
«1/ε = 200×»), `comportamento` 1 (il p-hacking «comportamento misurato»), `criterio di successo` 4 (testo della
regola 18, vedi autoconfutazione 7), `traguardo` 3 (racconto di E ed E′: E″ non usa la parola).

**Nei due run in `laboratorio/run/`**: `20260802-generalizzazione-labirinti` (Q-learning su labirinti) ha
`episodi di valutazione` 7, `Manhattan` 18, `griglia` 12, `ε = 0,3` 1 (una riga di baseline «greedy Manhattan cieco
con ε = 0,3 | 0,586» in un ambiente diverso); `20260803-bandit-esplorazione` ha `ε = 0,05` 15, `esplora` 1041, `ε` 443
(bandit, ε-greedy). Occorrenze minori: `uscita` 3 nel run 0802 (**nello stesso senso di E″**: «dove sia
l'uscita», «raggiunge l'uscita entro `H` o no», «il costo per passo dà gradiente prima di trovare l'uscita») e 2
nel run 0803 (nel senso di «output», «via d'uscita»); `costo per passo` 3 nel run 0802; `14°` 3 nel run 0803
(solo dentro file `.pyc` binari del `.venv`); `a ogni passo` 2 nel run 0803 (il bandit). Nessuna occorrenza di
`scadenza`, `13 passi`, `45/50`, `quanto esplorare`, `cammino minimo`, `valutazione separat…`.
**Sovrapposizioni dichiarate**: il run del 2026-08-02 (Q-learning su labirinti, compito «raggiunge l'uscita entro
`H`», costo per passo, «episodi di valutazione») mostra al laboratorio un compito della **stessa forma** e
l'abitudine di valutare con episodi separati — rende **più** probabile la trappola T2 e familiare il lessico, non
rivela quale braccio è rotto né perché (in quel run il guasto era un braccio che non imparava i propri dati). Un file del `.venv` del run
0803 (`cacert.pem`) non è leggibile nel sandbox: è un bundle di certificati di `pip`, irrilevante.

**Sovrapposizioni coi casi vivi**: A′ (MC contro TD con un peso condiviso, valutazione di una politica fissa) e B′
(momentum su un quadratico) non condividono ambiente, algoritmo né lessico distintivo; la frase «identici in tutto
tranne il bersaglio» di A′ non è stata usata. D″ non letto: E″ non è un confronto «a parità vera», il braccio rotto
è separato dal controllo di 0,47 sul regime.

## Cosa invaliderebbe questo caso

- Le quattro condizioni I1–I4 sopra.
- Un laboratorio che rinegozia ε (decrescente, valutazione a ε = 0) invece di implementarlo com'è: il caso non morde
  più; la riga anti-rinegoziazione è già nel testo.
- Se un FIX 18+ nominasse tetti di esplorazione, scadenze, valutazione greedy contro episodi di apprendimento, o
  off-policy: rifare il controllo di cecità prima di ogni rilancio.
- Se il caso dà l'esito atteso tre giri di fila senza mai essere stato vicino a sbagliarlo: regola del README,
  sostituirlo (ma il percorso si chiude col giro 6: Emendamento 1, punto 2).

<!-- FINE DOCUMENTO -->
