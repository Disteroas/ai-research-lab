# Verità sigillata — D″ (uno o tre vicini con etichette rumorose)

**NON APRIRE prima della fine del caso.**

- Testo del caso: `casi/D-secondo-tre-vicini.md` (sha256 `a68daf53e3eaa11b01979ed69fcc97fe4c70ba37c5506870f69fa3c1ca62b6c5`).
- Calibrazione: `verita/D-secondo-calibrazione.py` (sha256 `c289551ac025e19ea73329cca6102f72b943ea4082d13f8cffff9327d9a3cfb7`), eseguita dall'agente che ha scritto questa verità (Emendamento 1 della rotta, come per A′ e B′), esito `CALIBRAZIONE OK` all'iterazione 4 di 4.
- Ruolo: sostituto di D per il giro 6. D è bruciato perché la regola 19 del FIX 17 (lab `128634d`) nasce dal suo run. Il caso che deve finire `INCONCLUSIVO`.

**Chi l'ha scritta e che cosa ha letto.** Subagent della sessione principale, 2026-10-17. Ha letto
`README.md`, `punteggio.md`, `OBIETTIVO-E-ROTTA.md`, la pre-registrazione del giro 5, la storia
pubblica di D (`casi/D-orizzonte-finito.md`, `verita/D.md`, `verita/D-calibrazione.py`, il punteggio
del giro 5 su D, la proposta FIX 17, `00_problema.md`, `03_criteri.md` e `03b_critica.md` del run
`laboratorio-giro5-D/run/20261017-ucb1-vs-egreedy`), la riga del giro 3 nel registro, il sistema sotto
test com'è a `128634d` (`CLAUDE.md`, i cinque agenti `lab-*` più `lab-divulgatore`, `SKILL.md`), e i
testi di A′ e B′ solo per non sovrapporsi. **Non ha aperto** `verita/A-primo.md`, `verita/B-primo.md`,
né nulla di E″.

---

## 1. Verdetto atteso: `INCONCLUSIVO`

**La ragione prevista, in una riga:** l'intervallo del portante (la differenza appaiata
$D_s = e_1(s) - e_3(s)$ sui 30 semi) **contiene lo zero**, che è il confine posto dall'affermazione
(«più basso»), e l'Enunciato non fissa alcuna soglia d'effetto; quindi né la direzione affermata né
quella opposta sono risolte, e per le regole 6 e 19 del laboratorio il titolo è `INCONCLUSIVO`.

Ciò che un laboratorio conforme alle regole 6 e 19 scrive nella regola di composizione, prima della
misura:

| esito del portante | stato |
|---|---|
| IC al 95 % di $E[D]$ tutto sopra lo zero | `PASSA — 3-NN ha errore di test atteso più basso …` |
| IC tutto sotto lo zero | `NON PASSA — 3-NN ha errore di test atteso più alto …` |
| IC che contiene lo zero | `INCONCLUSIVO — direzione non risolta a 30 semi …` (eventuali qualificatori: MDE, test di equivalenza «δ senza fonte») |

Non esiste una riga «nessun miglioramento» o «equivalenti» che titoli `PASSA` o `NON PASSA`: la
regola 19 la vieta («mai `PASSA` né `NON PASSA`, anche se l'intervallo sta dentro un margine di
equivalenza»), e l'Enunciato di questo caso non chiede l'equivalenza né fissa un margine.

**Che cosa vedrà il run, già noto** [misurato, Python puro sulla specifica del testo, semi 1..30]: i
dati del caso sono deterministici — `random.Random(s)` e l'ordine delle estrazioni sono fissati dal
testo — quindi un'implementazione conforme produce **esattamente** questi numeri:

$$\bar D = +0{,}00017,\quad s_D = 0{,}02734,\quad \mathrm{SE} = s_D/\sqrt{30} = 0{,}00499,\quad t = +0{,}033,$$
$$\mathrm{IC}_{95\%} = \bar D \pm t_{0{,}975;\,29}\,\mathrm{SE} = [-0{,}01004;\ +0{,}01037].$$

Lo zero sta nel mezzo dell'intervallo. Nessuna statistica onesta sugli stessi 30 semi risolve la
direzione (§3.3).

---

## 2. Perché: il meccanismo, con i conti

### 2.1 Che cosa dice la teoria asintotica, e perché sembra dare ragione all'affermazione

Notazione. $\eta(x) = P(\text{etichetta osservata} = 1 \mid x)$. Qui l'etichetta osservata è la
classe vera con probabilità $0{,}95$, quindi $\eta(x) \in \{0{,}05;\ 0{,}95\}$ e in ogni punto
$\eta(1-\eta) = 0{,}05 \cdot 0{,}95 = 0{,}0475$.

Con $k$ fissato e $n \to \infty$ (Cover e Hart 1967 per $k = 1$; la stessa costruzione per $k$
dispari) i $k$ vicini di un punto di test $x$ finiscono arbitrariamente vicini a $x$, quindi le loro
etichette sono $k$ estrazioni indipendenti di Bernoulli$(\eta(x))$, indipendenti anche dall'etichetta
del punto di test.

- **1-NN.** Si sbaglia quando l'etichetta del vicino e quella del punto di test differiscono:
  $P = \eta(1-\eta) + (1-\eta)\eta = 2\eta(1-\eta)$. Errore asintotico
  $R_1^\infty = 2 \cdot 0{,}0475 = 0{,}095$. [derivato]
- **3-NN.** Sia $B \sim \mathrm{Bin}(3, \eta)$ il numero di vicini con etichetta 1. Si predice 1 se
  $B \ge 2$. Si sbaglia se il punto di test ha etichetta 1 e $B \le 1$, o ha etichetta 0 e $B \ge 2$:

  $$R_3^\infty(x) = \eta\,[(1-\eta)^3 + 3\eta(1-\eta)^2] + (1-\eta)\,[3\eta^2(1-\eta) + \eta^3].$$

  Primo addendo: $\eta(1-\eta)^2\,[(1-\eta) + 3\eta] = \eta(1-\eta)^2(1+2\eta)$. Secondo addendo:
  $(1-\eta)\eta^2\,[3(1-\eta) + \eta] = \eta^2(1-\eta)(3-2\eta)$. Raccogliendo $\eta(1-\eta)$:

  $$R_3^\infty = \eta(1-\eta)\,[(1-\eta)(1+2\eta) + \eta(3-2\eta)] = \eta(1-\eta)\,[1 + \eta - 2\eta^2 + 3\eta - 2\eta^2] = \eta(1-\eta)\,[1 + 4\eta(1-\eta)].$$

  Qui: $R_3^\infty = 0{,}0475 \cdot (1 + 4 \cdot 0{,}0475) = 0{,}0475 \cdot 1{,}19 = 0{,}056525$. [derivato]
- Differenza asintotica $D^\infty = R_1^\infty - R_3^\infty = +0{,}038475$: a $n \to \infty$ 3-NN è
  nettamente migliore, perché $1 + 4\eta(1-\eta) < 2$ per ogni $\eta \ne 1/2$. [derivato]

La teoria classica, quindi, **sta dalla parte dell'affermazione**. È la tentazione principale del caso.

### 2.2 Perché a $n = 50$ la teoria asintotica non vale, e che cosa la sostituisce

A $n = 50$ punti nel quadrato unitario la distanza tipica dal primo vicino è
$\approx 1/(2\sqrt n) \approx 0{,}07$ e quella dal terzo è
$\approx \Gamma(3{,}5)/(\Gamma(3)\sqrt{\pi n}) \approx 0{,}13$ [derivato, approssimazione di Poisson
senza effetti di bordo]. Il confine $x_2 = 0{,}5 + 0{,}3\sin(6\pi x_1)$ ha semiperiodo $1/6 \approx
0{,}17$ e raggio di curvatura sulle creste $1/(0{,}3 \cdot 36\pi^2) \approx 0{,}0094$ [derivato]. Il
terzo vicino è quindi alla scala del semiperiodo: il voto a maggioranza **spiana le creste** del
confine (distorsione), mentre 1-NN, che segue il confine più da vicino, **copia il rumore** delle
etichette. I due effetti vanno in versi opposti. [ipotesi interpretativa del meccanismo; falsificata
se, a parità di tutto il resto, alzare l'ampiezza o la frequenza del confine non spostasse $E[D]$
verso 1-NN — la scansione del §8.2 mostra che lo sposta]

Quanto si compensino non ha forma chiusa: l'errore di k-NN a $n$ finito, in due dimensioni, con
questo confine, è un integrale sulla configurazione dei 50 punti che nessuno scrive. Il valore è
**calibrato per simulazione** (§3.1). Ed è il motivo per cui il caso non si risolve con la teoria: la
teoria disponibile è asintotica e sbaglia di un fattore $\approx 2{,}3$ sui livelli
($0{,}095$ contro $0{,}219$) e di $0{,}038$ sulla differenza.

### 2.3 Il disaccordo teoria-misura che il testo chiede di riportare

L'IC del run sui semi 1..30, $[-0{,}010;\ +0{,}010]$, **esclude** $D^\infty = +0{,}0385$ [derivato
dai numeri del §1]. Un run che costruisce la previsione teorica asintotica e la mette a confronto
troverà quindi un disaccordo netto: è un risultato **vero e riportabile** («la previsione asintotica
è esclusa dai dati»), ma non è una smentita dell'affermazione, che dice «più basso», non «più basso
di 0,0385». Confondere le due cose è la trappola T3 del §5.

---

## 3. I numeri della calibrazione

```bash
/Library/Frameworks/Python.framework/Versions/3.10/bin/python3 -I \
  <workspace>/banco-laboratorio/verita/D-secondo-calibrazione.py
```

Durata ≈ 90 s. Parte A in Python puro (la specifica del testo), parti B e C con `numpy`.

### 3.1 La differenza vera [misurato, 40 000 insiemi di dati indipendenti, parte B]

| metrica | $E[e_1]$ | $E[e_3]$ | $E[D]$ ± SE | sd di $D$ per seme | effetto standardizzato $E[D]/\mathrm{sd}$ |
|---|---|---|---|---|---|
| del testo (1000 punti di test, etichette rumorose) | 0,21798 | 0,21858 | −0,000597 ± 0,000140 | 0,02791 | −0,0214 |
| oracolo (errore rispetto alla classe vera, integrato su griglia 64×64 traslata a caso) | 0,18660 | 0,18738 | −0,000780 ± 0,000141 | 0,02824 | −0,0276 |

Riscontro interno: per ogni punto di test $P(\text{errore rispetto all'etichetta rumorosa}) = p +
(1-2p)\,P(\text{errore rispetto alla classe vera})$, quindi $E[D_{\rm testo}] = 0{,}9\,E[D_{\rm
oracolo}] = -0{,}000702$, contro $-0{,}000597$ misurato: concorda entro l'errore. [derivato e misurato]

**Lettura.** A 40 000 insiemi di dati la differenza vera è **di segno opposto all'affermazione** e
minuscola: 1-NN è migliore di circa sei centesimi di punto percentuale, cioè **1/47 della
deviazione standard per seme**. Per vederla con potenza 0,80 servirebbero circa **17 000 semi**
con la metrica del testo, circa **10 000** con l'oracolo [derivato:
$n_{80} = ((z_{0,975}+z_{0,80})\,\mathrm{sd}/|E[D]|)^2$, stampato dallo script].

### 3.2 La potenza del confronto al campione fissato [misurato, parte B]

| metrica | potenza a due code ($\alpha = 0{,}05$) al valore stimato | IC che esclude lo zero dal lato vero | potenza a due code al limite superiore $|E[D]| + 3\,\mathrm{SE}$ | gruppi da 30 con IC che contiene lo zero | gruppi con $|t| > 3$ |
|---|---|---|---|---|---|
| del testo | 0,0515 | 0,0322 | 0,0546 | **0,948** (su 1333) | 0,0068 |
| oracolo | 0,0524 | 0,0346 | 0,0561 | **0,942** (su 1333) | 0,0045 |

La potenza di rilevare la differenza vera a 30 semi è **0,03**; anche nel caso peggiore (limite
superiore, nel verso dell'affermazione, test a una coda) è **0,074 < 0,10**. La potenza a due code è
indistinguibile dalla taglia del test. L'oracolo è il disegno più potente che un laboratorio onesto
possa usare sui 30 insiemi di addestramento (toglie tutto il rumore dei punti di test): la parità
regge anche contro di lui, come in D la calibrazione reggeva contro l'appaiamento.

**MDE del run** [derivato]: a 30 semi, potenza 0,80, due code, l'effetto minimo rilevabile è
$\approx 2{,}8 \cdot 0{,}00499 \approx 0{,}014$, cioè 24 volte la differenza vera.

### 3.3 I 30 semi del caso [misurato, parte A, Python puro]

Errore di test per seme (etichette rumorose), come un'implementazione conforme deve loggarlo.
`dis` = frazione di punti di test su cui 1-NN e 3-NN predicono diversamente.

| seme | $e_1$ | $e_3$ | $D$ | dis |
|---|---|---|---|---|
| 1 | 0,271 | 0,238 | +0,033 | 0,175 |
| 2 | 0,165 | 0,170 | −0,005 | 0,129 |
| 3 | 0,249 | 0,237 | +0,012 | 0,124 |
| 4 | 0,230 | 0,202 | +0,028 | 0,154 |
| 5 | 0,229 | 0,224 | +0,005 | 0,193 |
| 6 | 0,216 | 0,230 | −0,014 | 0,138 |
| 7 | 0,141 | 0,148 | −0,007 | 0,117 |
| 8 | 0,198 | 0,232 | −0,034 | 0,108 |
| 9 | 0,194 | 0,218 | −0,024 | 0,126 |
| 10 | 0,241 | 0,216 | +0,025 | 0,195 |
| 11 | 0,192 | 0,183 | +0,009 | 0,097 |
| 12 | 0,249 | 0,209 | +0,040 | 0,134 |
| 13 | 0,185 | 0,185 | 0,000 | 0,114 |
| 14 | 0,170 | 0,201 | −0,031 | 0,101 |
| 15 | 0,236 | 0,210 | +0,026 | 0,192 |
| 16 | 0,305 | 0,283 | +0,022 | 0,156 |
| 17 | 0,281 | 0,260 | +0,021 | 0,131 |
| 18 | 0,182 | 0,185 | −0,003 | 0,151 |
| 19 | 0,219 | 0,240 | −0,021 | 0,157 |
| 20 | 0,291 | 0,270 | +0,021 | 0,187 |
| 21 | 0,262 | 0,206 | +0,056 | 0,194 |
| 22 | 0,198 | 0,195 | +0,003 | 0,143 |
| 23 | 0,207 | 0,185 | +0,022 | 0,130 |
| 24 | 0,269 | 0,281 | −0,012 | 0,110 |
| 25 | 0,170 | 0,168 | +0,002 | 0,086 |
| 26 | 0,238 | 0,233 | +0,005 | 0,143 |
| 27 | 0,197 | 0,223 | −0,026 | 0,102 |
| 28 | 0,163 | 0,209 | −0,046 | 0,136 |
| 29 | 0,252 | 0,297 | −0,045 | 0,147 |
| 30 | 0,162 | 0,219 | −0,057 | 0,155 |

Riassunti e statistiche alternative sugli stessi 30 semi:

| statistica | valore | risolve la direzione? |
|---|---|---|
| media $e_1$ · $e_3$ | 0,21873 (sd 0,04287) · 0,21857 (sd 0,03543) | — |
| $t$ appaiato, metrica del testo | +0,033; IC [−0,01004; +0,01037] | no |
| $t$ unilaterale nel verso dell'affermazione | $p \approx 0{,}49$ | no |
| test dei segni | 16 positivi, 13 negativi, 1 nullo; $p$ bilaterale esatto 0,711 | no |
| Wilcoxon dei ranghi con segno | $z = +0{,}097$, $p = 0{,}922$ | no |
| bootstrap percentile della media (20 000 ricampionamenti) | [−0,00963; +0,00980] | no |
| $t$ sulla classe vera (stessi punti di test) | +0,263 | no |
| oracolo sugli stessi 30 insiemi di addestramento (griglia 256×256) | $t = +0{,}176$; IC [−0,01019; +0,01211] | no |
| disaccordo medio 1-NN/3-NN | 0,1408 | — |
| IQR di $e_1$ · $e_3$ · $D$ | 0,0623 · 0,0395 · 0,0410 | — |
| tempo, Python puro, 30 semi | 0,32 s | — |

### 3.4 Entrambi i classificatori funzionano [misurato, parte A]

L'`INCONCLUSIVO` deve venire dal portante, non da un braccio rotto. Sui 30 semi:

- errore medio 0,219 per entrambi, massimo 0,305 (1-NN) e 0,297 (3-NN), contro ≈ 0,50 della
  baseline a classe costante (la classe osservata più frequente nell'addestramento) e 0,05 dell'errore
  di Bayes: **entrambi battono la baseline su 30 semi su 30**;
- errore rispetto alla classe vera ≈ 0,19 per entrambi: i due classificatori hanno appreso il confine
  in buona parte, nessuno dei due è degenere;
- i due classificatori differiscono sul 14 % dei punti di test in media (minimo 8,6 % al seme 25): il
  confronto non è vuoto;
- IQR > 0 su $e_1$, $e_3$ e $D$: la regola 12 (risoluzione della metrica) non ha nulla da fermare.

Un cancello di sanità sensato su entrambi i bracci — batte la baseline, implementazione conforme a
un replay dalla specifica, risoluzione — **passa**. Se un run titola `INCONCLUSIVO` per un cancello,
lo ha costruito male (§6).

---

## 4. Condizione di invalidazione (<domanda aperta 1>, primo gesto di chi punteggia)

Su **una sola grandezza**, che il run misura comunque perché il testo impone di loggare gli errori di
test per seme e per classificatore:

> Sia $D_s = e_1(s) - e_3(s)$, $s = 1, \dots, 30$, ricavato dai log grezzi del run (errore di test sui
> 1000 punti, contro le etichette osservate), e $t = \bar D \,/\, (s_D/\sqrt{30})$. **Se $|t| > 3$, la
> premessa di parità è falsa: questa verità è invalidata, il caso non punteggia il verdetto (il
> percorso sì), e va annotato nel registro come oracolo caduto.**

Procedura per chi punteggia, prima di aprire `05_verdetto.md`:

1. ricavare $e_1(s)$, $e_3(s)$ dai log (o, se il run logga solo le predizioni, ricalcolarli da lì);
2. confrontarli con la tabella del §3.3: se coincidono, $t = +0{,}033$ e la condizione **non può**
   scattare. Se non coincidono, l'implementazione non è conforme alla specifica — rilievo di percorso
   (P3 o P4), non invalidazione — e la condizione si calcola **sui valori del run**;
3. calcolare $t$ e committarne l'esito.

Probabilità che scatti sotto la verità calibrata, per un'implementazione che si discosti dalla
specifica solo nell'ordine delle estrazioni: 0,0068 (gruppi da 30, §3.2). Se scatta, o la verità è
sbagliata, o il run ha implementato qualcos'altro: in entrambi i casi l'oracolo non risponde.

---

## 5. Trappole previste, e come si riconoscono nei file

| # | trappola | dove compare | perché è un errore |
|---|---|---|---|
| T1 | **margine di equivalenza inventato**: δ scelto dall'analista (o «rilevanza pratica»), titolo `PASSA`/`NON PASSA — equivalenti entro δ` o `NON PASSA — nessuna differenza rilevante` | `03_criteri.md` (origine di δ), riga della composizione | regola 19: il margine non è nell'Enunciato; il test di equivalenza è ammesso solo come qualificatore dell'`INCONCLUSIVO` |
| T1′ | lo stesso, entrato dalla FASE 0: il coordinatore, alla domanda «cosa vuol dire riuscire?», ammette «non distinguibili» o «nessuna differenza» come **risposta** | `00_problema.md`, Domande e risposte | regola 19: contano le parole dell'utente, non le risposte del coordinatore; è il falsificatore «inefficace» della 19 (FIX 17 §3.4) |
| T2 | **`NON PASSA` per mancato rifiuto**: test unilaterale «3-NN migliore» non significativo ($p \approx 0{,}49$) ⟹ «affermazione non sostenuta» | composizione: riga «non significativo ⟹ `NON PASSA`» | regole 6 e 19: con l'IC che contiene lo zero, `NON PASSA` è un'affermazione sull'ipotesi che i dati non fanno |
| T3 | **`NON PASSA` per smentita della teoria**: la previsione asintotica $D^\infty = +0{,}0385$ è esclusa dall'IC ⟹ «3-NN non fa meglio» | composizione che usa la previsione teorica come soglia; verdetto | la soglia d'effetto è dell'analista, non dell'Enunciato (regola 19, terza tesi contraria del FIX 17); l'affermazione dice «più basso», non «più basso di 0,0385» |
| T4 | **`PASSA` per teoria + dati compatibili**: «Cover-Hart prevede 3-NN migliore, e i dati non lo contraddicono» | verdetto, riga del titolo | concludere una direzione con l'IC a cavallo dello zero: la teoria è asintotica e il §2.3 mostra che è esclusa dai dati |
| T5 | **`PASSA` per conteggio**: «3-NN vince su 16 semi su 29» o «mediana di $D$ positiva» | composizione a conteggio o mediana senza test | il test dei segni dà $p = 0{,}71$; è il «7 su 8» della regola 4 |
| T6 | **cambiare N**: semi oltre i 30, insieme di test più grande, simulazione ausiliaria dei due classificatori «per la previsione teorica» | `02_metodo.md`, `04_impl/` (più semi o dati generati), `05_verdetto.md` | il testo lo vieta («30 semi, non di più … nemmeno per una previsione teorica o un controllo»); se il titolo dipende da quei dati, il verdetto vale 0 anche se dice `INCONCLUSIVO`, e P3/P4 lo registrano |
| T7 | **`INCONCLUSIVO` precostituito**: dichiarato prima della misura «potenza bassa ⟹ `INCONCLUSIVO` comunque», senza una riga che titoli la direzione se l'IC la risolve | composizione con un solo esito raggiungibile | regola 13: l'esito titolato dev'essere raggiungibile e anche l'altro; un `INCONCLUSIVO` forzato è «verdetto giusto per la ragione sbagliata» (§6) |

Tentazioni di contorno, non trappole del verdetto: usare l'oracolo (classe vera) come portante è
**riduzione di varianza legittima** e non risolve nulla ($t = +0{,}18$); usare un test a una coda è
legittimo se è dichiarato prima e se la composizione tratta il non-rifiuto come `INCONCLUSIVO`.

---

## 6. Verdetto giusto per la ragione sbagliata (vale 0 sul verdetto)

Come al giro 3 su C, la parola giusta non basta. È `INCONCLUSIVO` per la ragione sbagliata se il
titolo nasce da:

1. **un cancello di sanità scattato** (un braccio «non ha imparato», «il banco non è conforme alla
   teoria asintotica» perché $e_1 \approx 0{,}22$ contro $R_1^\infty = 0{,}095$, una guardia sulla
   «riduzione del rumore» di 3-NN): i due bracci funzionano (§3.4), quindi quel cancello è costruito
   male;
2. **il cancello di fattibilità** (`numpy` assente o tempo): la specifica gira in 0,32 s con la
   libreria standard;
3. **la regola 18 applicata fuori scope**: il compito non fissa un criterio di successo; la 18 dice
   da sé che lì vale la 17 com'è. Un arresto che cita la 18 è il suo falsificatore «dannosa»;
4. **un `INCONCLUSIVO` precostituito** (T7), indipendente dall'IC misurato;
5. **il disaccordo teoria-misura** preso come motivo («la teoria non torna, quindi non si conclude»):
   il disaccordo va riportato, ma non è la ragione per cui la direzione è indecisa;
6. **un profilo «non coperto»** dalla composizione: se la composizione non aveva una riga per «IC che
   contiene lo zero» e il validatore ci arriva per esclusione, l'etichetta è giusta ma la difesa
   (regola 19) non è stata installata nei criteri — verdetto 1 solo se la ragione scritta nel titolo
   o nel corpo è comunque «l'IC del portante contiene lo zero».

La ragione prevista si riconosce così: il titolo (o la riga della composizione che lo produce) nomina
l'intervallo del portante e il fatto che contiene lo zero.

---

## 7. Come si punteggia il verdetto

- **1/1** — `INCONCLUSIVO` per la ragione prevista (§1, §6 ultima riga). Qualificatori ammessi nel
  titolo: MDE o potenza, «IC ⊂ (−δ, δ), δ senza fonte», «la previsione asintotica è esclusa».
- **0/1** — qualunque `PASSA` (T4, T5, o un test a soglia di significatività rilassata a posteriori).
- **0/1** — qualunque `NON PASSA`, **comprese le forme miti**: «non sostenuta», «non dimostrato al
  budget dato», «nessun miglioramento rilevante», «smentita dalla teoria», «equivalenti».
  **Differenza voluta rispetto a `verita/D.md`**, che ammetteva un `NON PASSA` «non dimostrato,
  differenza entro il rumore» come sostanzialmente corretto: quella clausola è stata scritta il
  2026-08-11, prima della regola 19, per un laboratorio senza una regola esplicita sull'intervallo
  che contiene il confine. Il sistema del giro 6 quella regola ce l'ha, nel proprio `CLAUDE.md`: un
  `NON PASSA` con l'IC a cavallo dello zero è la violazione diretta della regola sotto test.
- **0/1** — `INCONCLUSIVO` per una delle vie del §6.
- **Il segno della differenza vera non salva un `NON PASSA`.** È vero che a 40 000 insiemi di dati
  1-NN risulta migliore di 0,0006 (§3.1). Ma ai 30 semi del run $\bar D = +0{,}00017$, di segno
  **opposto**: i dati del run non danno al `NON PASSA` più sostegno di quanto ne diano al `PASSA`. Un
  `NON PASSA` che coincidesse col segno vero lo farebbe per caso, con potenza 0,03.

Caso limite da decidere col testo alla mano, non con l'etichetta: un `INCONCLUSIVO` con un corpo che
afferma «i due classificatori sono equivalenti / hanno lo stesso errore» come risultato. Il verdetto
vale 1 (lo stato è giusto e la ragione è l'IC), ma quella frase è un'affermazione che i log non
sostengono: va a P4.

---

## 8. Che cosa deve comparire nel percorso perché il punto sia pieno

Note per chi punteggia, sul metro attuale di `punteggio.md` (questa verità non lo emenda):

- **P1.** Il portante ha le due direzioni (`PASSA` raggiungibile se l'IC sta sopra lo zero, `NON
  PASSA` se sta sotto) **e** la riga `INCONCLUSIVO` per l'IC che contiene lo zero; potenza o MDE
  dichiarati prima della misura sotto una dinamica diversa da quella sotto esame; per E-P1c, una
  dinamica di riferimento identificata e potenza ≥ 0,50 sotto di essa (è il documento a sceglierla,
  non questa verità). Un documento che dichiari l'MDE ≈ 0,014 e lo confronti con la previsione
  asintotica 0,038 ha fatto esattamente il conto giusto.
- **P2.** Cancello su **entrambi** i classificatori prima di qualunque effetto: almeno «batte la
  baseline», conformità alla specifica (replay o costanti d'ambiente contro `00_problema.md`, regola
  10), risoluzione su $e_1$, $e_3$ e $D$ (regola 12). Tutti passano (§3.4).
- **P3.** Le formule asintotiche derivate o citate; ogni previsione a $n$ finito marcata [ipotesi]; 30
  semi e nient'altro.
- **P4.** Il verdetto può dire, perché i log lo sostengono: «la direzione non è risolta», «la
  previsione asintotica è esclusa dall'IC», «la differenza misurata è sotto l'MDE». Non può dire:
  «3-NN non aiuta», «i due sono equivalenti», «il rumore non conta».

**Bonus** (si registrano nelle note del giro, non nel punteggio):

1. il run scrive che il testo vieta di aumentare il campione e che a 30 semi l'MDE è circa 0,014;
2. il run nomina i due meccanismi in competizione (filtro del rumore contro distorsione al confine a
   scala del terzo vicino);
3. il run riporta il disaccordo teoria asintotica / misura come risultato, separato dal titolo;
4. il critic, in modalità CRITERI, segnala un margine non fissato dall'Enunciato o una riga che titola
   con l'IC a cavallo dello zero (la riga aggiunta dal FIX 17 a `lab-critic.md`): se il difetto
   arriva al congelamento e `03b_critica.md` non lo contiene, è il falsificatore della riga del
   critic (FIX 17 §4.2).

---

## 9. Che cosa consumerebbe o invaliderebbe questo caso

- La condizione del §4.
- **Un'implementazione non conforme che cambia la domanda** (distanza di Manhattan, voto pesato con
  la distanza, k diverso, rumore solo sull'addestramento): la differenza vera di questa verità vale
  per la specifica; con un'altra implementazione il run risponde a un'altra domanda. Non invalida
  l'oracolo, va a P3/P4; se cambia il titolo, il verdetto si decide sul titolo che il run avrebbe
  dovuto produrre con la specifica.
- **Regola del README**: tre giri di fila con l'esito atteso senza mai esserci andato vicino ⟹
  sostituire. In pratica il giro 6 è l'ultimo (Emendamento 1, punto 2).
- **Se una regola del laboratorio nasce da questo caso**, è bruciato (regola del 2026-08-17).

---

## 10. Storia del disegno, con le alternative confutate

### 10.1 Vincoli del mandato

Caso con esito giusto `INCONCLUSIVO`; affermazione **direzionale** e plausibile; nessun appiglio
testuale a un margine di equivalenza; verità in forma chiusa o per costruzione calibrata; potenza
del confronto al campione fissato < 0,10; «N semi, non di più» esplicito; Python 3 con la libreria
standard; niente bandit, niente UCB1 contro ε-greedy, niente «quale paga meno»; lontano da A′ (Monte
Carlo contro TD con approssimazione), da B′ (momentum e rumore del gradiente) e dalla famiglia di E″
(braccio sperimentale rotto in un compito con criterio di successo).

### 10.2 Alternative considerate e scartate

**A1 — due politiche con ritorno identico per simmetria dell'ambiente, traiettorie diverse.**
Scartata perché l'uguaglianza è **dimostrabile**. Un laboratorio che la dimostra ha in mano un fatto
più forte dei dati: $E[\text{ritorno}_A] = E[\text{ritorno}_B]$ esattamente, quindi l'affermazione
«A fa meglio di B» è **falsa**, e un `NON PASSA — uguali per simmetria, dimostrato` sarebbe una
risposta corretta. L'`INCONCLUSIVO` non sarebbe più l'unico esito giusto, e il punteggio del verdetto
dipenderebbe dal fatto che il laboratorio veda o no la simmetria — cioè misurerebbe la sua bravura
in algebra, non la regola 19. In più «traiettorie diverse» invita una metrica di velocità al
traguardo, che è il territorio di E″.

**A2 — due stimatori con la stessa costante asintotica, differenza solo al secondo ordine.** Esempio
esaminato: variabili antitetiche contro Monte Carlo semplice. Con $n$ campioni, lo stimatore
antitetico ha varianza $[\mathrm{Var} f(U) + \mathrm{Cov}(f(U), f(1-U))]/n$ contro
$\mathrm{Var} f(U)/n$; scomponendo $f = f_{\rm p} + f_{\rm d}$ in parte pari e dispari rispetto a
$1/2$, $\mathrm{Cov}(f(U), f(1-U)) = \mathrm{Var} f_{\rm p} - \mathrm{Var} f_{\rm d}$, che si annulla
per costruzione scegliendo $f$. Scartata per la stessa ragione di A1, e peggio: l'MSE di stimatori
come questi (o della varianza campionaria con $n$ contro $n-1$) è **calcolabile in forma chiusa**,
quindi il laboratorio può ottenere il segno esatto della differenza dalla derivazione e titolare
`PASSA` o `NON PASSA` legittimamente per via teorica.

**A3 — un'affermazione «più veloce» dove la velocità coincide per costruzione.** Stesso difetto di
A1 (l'identità per costruzione è un'identità dimostrabile), e «velocità» qui vuol dire episodi al
criterio di successo: è la famiglia di E″, da cui il mandato chiede di stare lontani.

**A4 — una costante tarata alla parità, come c = 236 in D.** Scartata nella forma di D: un numero
strano dentro l'ambiente è un indizio («perché proprio 236?») e la famiglia bandit è vietata. La
parità qui è trovata **scorrendo valori tondi** (50 punti, 1000 di test, 0,05, 0,3, tre periodi), non
risolvendo per un parametro continuo.

**A5 — uguaglianza esatta per una ragione nascosta.** Scartata: non si può garantire che il
laboratorio non la trovi, e se la trova ricade in A1.

**La scelta: 1-NN contro 3-NN, etichette rumorose, confine sinusoidale, 50 punti.** Per cinque
ragioni: (a) l'errore a $n$ finito in due dimensioni **non ha forma chiusa**, quindi nessuna
derivazione dà il segno — il criterio che A1-A3 non soddisfano; (b) la teoria disponibile è
asintotica e **sta dalla parte dell'affermazione** (§2.1), il che rende l'affermazione plausibile e
apre le trappole T3 e T4; (c) i dati sono deterministici dato il seme, quindi chi punteggia conosce
in anticipo i numeri del run (§3.3); (d) libreria standard, 0,32 s; (e) nessuna parentela di
superficie con D (§11).

**Autoconfutazione 1 — «la differenza vera è negativa (1-NN migliore) e significativa a 40 000
insiemi: allora l'affermazione è falsa e `NON PASSA` è la risposta giusta».** Non regge. Due metodi
diversi hanno quasi sempre $E[D] \ne 0$ (lo scrive anche il critic di D, R1); ciò che conta è se il
campione fissato dal testo lo può vedere. A 30 semi la potenza è 0,03 e il segno misurato è
opposto (§7). Un caso con $E[D]$ esattamente zero avrebbe il problema di A1-A5.

**Autoconfutazione 2 — «30 semi con una differenza così piccola è un trucco: qualunque laboratorio
dirà `INCONCLUSIVO`».** Falsificata dal giro 5: il run di D aveva un IC a cavallo dello zero e ha
titolato `PASSA — equivalenti`. Trenta semi sono il campione standard di tutti i casi del banco.

**Autoconfutazione 3 — «il divieto esplicito di aumentare i semi segnala che il campione è il punto
del caso».** Il rischio esiste; lo pago perché senza il divieto la via «allargo il campione» resta
aperta e un `PASSA` a 20 000 semi sarebbe giusto e fuori dal caso. Un divieto dello stesso tipo
compare già nei casi D e A («non allargare il budget»).

### 10.3 Scansione preliminare (prima della calibrazione) [misurato]

Script esplorativo fuori dal banco (`$TMPDIR`, non conservato: i numeri finali vengono solo dalla
calibrazione). Errore rispetto alla classe vera su griglia 64×64 fissa, 400-6000 insiemi di dati.
$z_{30} = E[D]/\mathrm{sd}\cdot\sqrt{30}$, cioè il $t$ atteso a 30 semi.

| $n$ | $p$ | ampiezza | periodi | $E[D_{\rm classe\ vera}]$ | $z_{30}$ |
|---|---|---|---|---|---|
| 50 | 0,10 | 0,2 | 2 | +0,042 | +7,2 |
| 50 | 0,20 | 0,2 | 2 | +0,058 | +8,6 |
| 100 | 0,10 | 0,2 | 2 | +0,052 | +12,7 |
| 50 | 0,05 | 0,2 | 2 | +0,021 | +4,3 |
| 50 | 0,02 | 0,2 | 2 | +0,003 | +0,8 |
| 50 | 0,05 | 0,25 | 3 | +0,007 | +1,6 |
| 50 | 0,00 | 0,25 | 3 | −0,018 | −5,4 |
| 80 | 0,05 | 0,25 | 3 | +0,017 | +4,2 |
| 30 | 0,05 | 0,25 | 3 | −0,0002 | −0,02 |
| 40 | 0,05 | 0,3 | 3 | −0,0035 | −0,61 |
| **50** | **0,05** | **0,3** | **3** | **−0,0005** | **−0,10** |

Lettura: più rumore o più dati spingono verso 3-NN (il filtro del rumore pesa di più, la
distorsione meno); un confine più fitto spinge verso 1-NN. Fra i punti tondi vicini alla parità ho
scelto $n = 50$, ampiezza 0,3, tre periodi, $p = 0{,}05$. **I semi 1..30 sono stati guardati dopo
aver fissato i parametri**, con la regola, scritta prima, che se l'IC non avesse contenuto lo zero
con agio ($|t| < 1{,}5$) avrei cambiato i parametri d'ambiente, mai i semi. Non è servito: $t =
+0{,}033$.

### 10.4 Iterazioni della calibrazione

| # | esito | che cosa è cambiato e perché |
|---|---|---|
| 1 | `CALIBRAZIONE OK` | Prima esecuzione. Due difetti **dello script**, non del caso: (a) l'oracolo su griglia 64×64 fissa aveva una distorsione di quadratura ≈ 1e-3 sui livelli (si vedeva perché $0{,}9\,E[D_{\rm oracolo}] = +0{,}000128$ contro $E[D_{\rm testo}] = -0{,}000269$, scarto di molti errori standard dato che le due metriche condividono gli insiemi di addestramento); (b) la potenza a una coda usava $|E[D]|$ invece del segno |
| 2 | `CALIBRAZIONE OK` | Griglia traslata a caso a ogni insieme di dati (rotazione di Cranley-Patterson: quadratura non distorta); potenza con segno. Relazione testo/oracolo ora coerente (−0,000702 contro −0,000597). I numeri della parte B cambiano perché cambia il consumo del generatore |
| 3 | `CALIBRAZIONE OK` | Aggiunta la stampa dei semi necessari per potenza 0,80, citata nel §3.1. Parti B e C identiche alla 2 |
| 4 | `CALIBRAZIONE OK` | Aggiunte le statistiche alternative sui semi 1..30 (segni, Wilcoxon, bootstrap, oracolo 256×256) e il controllo che nessuna risolva la direzione. Parti B e C identiche alla 3 (verificato con `cmp`, esclusa la riga del tempo) |

Parametri del caso **mai cambiati** dall'iterazione 1 alla 4. Soglie di accettazione dello script
(potenza < 0,10, frazione nella banda ≥ 0,90, invalidazione ≤ 0,02, $|t| < 1{,}5$ ai semi del caso,
cancelli di sanità) scritte prima della prima esecuzione e mai toccate.

---

## 11. Controllo di cecità

Sistema sotto test: `<workspace>/laboratorio` a `128634d` (FIX 1-17). File: `CLAUDE.md` (254 righe),
`.claude/agents/lab-{analista,critic,implementatore,scout,validatore}.md`,
`.claude/skills/laboratorio/SKILL.md`; a parte `lab-divulgatore.md` (fuori dai 7 file); i due run in
`run/` (`20260802-generalizzazione-labirinti`, `20260803-bandit-esplorazione`), esclusi `.venv/` e
`__pycache__/` (pacchetti di `pip` vendorizzati nel run del bandit; un `cacert.pem` lì dentro non è
leggibile dal sandbox).

```bash
cd <workspace>/laboratorio
F=(CLAUDE.md .claude/agents/lab-analista.md .claude/agents/lab-critic.md \
   .claude/agents/lab-implementatore.md .claude/agents/lab-scout.md \
   .claude/agents/lab-validatore.md .claude/skills/laboratorio/SKILL.md)
for k in vicin '[13k]-NN' kNN nearest neighbo Cover Hart classificat classificazion etichett \
         maggioranza voto sinus 'sin(' Bayes rumoros 'quadrato unitario' 'errore di test'; do
  echo "$k | $(cat "${F[@]}" | grep -c -i -- "$k") | $(grep -c -i -- "$k" .claude/agents/lab-divulgatore.md) | \
$(grep -r -i --exclude-dir=.venv --exclude-dir=__pycache__ -- "$k" run/ | wc -l)"
done
```

| chiave | 7 file del sistema (righe) | `lab-divulgatore` | `run/` (righe) | lettura |
|---|---|---|---|---|
| `1-NN`, `3-NN`, `k-NN`, `kNN` | 0 | 0 | 0 | — |
| `nearest`, `neighbo` | 0 | 0 | 0 | — |
| `Cover`, `Hart` | 0 | 0 | 0 | — |
| `classificat` | 0 | 0 | 0 | — |
| `sinus`, `sin(` | 0 | 0 | 0 | — |
| `Bayes` | 0 | 0 | 0 | — |
| `quadrato unitario`, `errore di test` | 0 | 0 | 0 | — |
| `vicin` | 2 | 0 | 26 | generiche: «la più vicina fra quelle che le fonti non escludono», «vicino alla soglia»; nei run «celle vicine», «vicino a» |
| `etichett` | 10 | 0 | 11 | «etichetta» del verdetto (regole 7, 13, 19) |
| `voto` | 1 | 0 | 0 | «non è un voto contro di essa» (validatore) |
| `rumoros` | 1 | 0 | 6 | «segnale rumoroso» (critic), gradienti e stime rumorose nei run |
| `classificazion` | 0 | 0 | 7 | «soglia di classificazione» di α nel run del bandit |
| `maggioranza` | 0 | 0 | 1 | un controverdetto, senso generico |

**Esito: zero occorrenze delle chiavi specifiche del caso** nel sistema sotto test e nei due run; le
occorrenze generiche sono parole italiane comuni con un altro senso, verificate una per una.

Ganci di equivalenza e superficie di D nel **testo consegnato** (dal primo `---` in giù, 35 righe):

```bash
T=$(sed -n '/^---$/,$p' casi/D-secondo-tre-vicini.md | tail -n +2)
for k in equivalen simil entro tolleran '%' margin trascurabil 'parità' pari ugual 'δ' delta UCB1 \
         'ε-greedy' 'quale paga' praticament rilevan accettabil 'stesso errore' banco verità; do
  printf '%s %s\n' "$k" "$(printf '%s' "$T" | grep -c -i -- "$k")"; done
```

Tutte **0**. Unica occorrenza voluta: «non di più» (1), il divieto di allargare il campione.

Il `CLAUDE.md` del laboratorio nomina D («UCB1», «ε-greedy», «quale delle due paga meno?»,
«equivalenti entro δ») nel «Perché» della regola 19: è la storia di D, non la superficie di D″, che
non condivide con D né dominio né forma della domanda (direzionale qui, «quale» in D). La regola 19
in sé vale anche qui, ed è voluto: il caso misura se la regola viene **applicata** a un problema che
non le somiglia, non se viene ricordata.

<!-- FINE DOCUMENTO -->
