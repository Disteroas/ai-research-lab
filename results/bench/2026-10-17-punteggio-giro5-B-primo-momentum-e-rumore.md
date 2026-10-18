# Punteggio del giro 5 — caso B′ (il momentum e il rumore del gradiente)

Run punteggiato: `<workspace>/laboratorio-giro5-B1/run/20261017-momentum-sgd-regime` (HEAD del repo
`53428ee`, commit seminato `307fc85`, autore `banco`). Mandato: `giri/MANDATO-PUNTEGGIO-GIRO5.md`
compreso l'Emendamento 1. Regola di accettazione: `giri/2026-10-17-preregistrazione-giro5.md` §3.
Metro: `punteggio.md` con E-P1, E-P1b, E-P1c (nessun emendamento dopo il 2026-08-18).

Denominatori di questo file: verdetto **n/1**, percorso **n/4** (riga di caso; la sintesi n/4 e n/16 la
scrive la sessione principale).

## Chi punteggia, e che cosa sapeva prima di aprire alcunché

Subagent fresco del 2026-10-17: non ha coordinato il run, non ha partecipato al lancio, non ha aperto la
nota di progetto nelle <note dell'autore> né le verità degli altri casi. Prima della parte 1 sapeva: la
pre-registrazione (che dichiara pubblicamente il ruolo di B′, «deve dare `NON PASSA`»), il metro, il
modello di punteggio del giro 4 (caso E), il registro.

**Contaminazioni dichiarate, tutte minori:**

1. **Titoli delle sezioni della verità.** Per localizzare la sezione dell'invalidazione ho eseguito
   `grep -n -i "invalidaz"` e anche `grep -n '^#'` su `verita/B-primo.md`. Il secondo ha mostrato i
   titoli, fra cui quello dell'esito atteso («`NON PASSA` — il momentum moltiplica per ~10 l'errore a
   regime»); il primo ha mostrato le righe 221 e 384, che citano la forma chiusa 9,976 e la soglia di
   calibrazione 9,31. Nessuna delle due cose è nuova: il ruolo `NON PASSA` è pubblico nella
   pre-registrazione §2, e il fattore ~10 (9,976) il run lo deriva da sé in `02_metodo.md` riga 106. Non
   ho letto altro della verità prima del commit di questa parte.
2. **Riga di A′ nel registro.** Per il formato ho stampato le righe del registro, compresa quella di A′
   (che contiene il punteggio di A′). Non tocca B′.
3. `stato-B-primo-momentum-e-rumore.txt`: letto solo come da Emendamento 1 (righe 1-6, «modelli che
   hanno committato», «sistema sotto test»). `log-` e `console-B-primo-…` **non aperti** prima del
   commit di questa parte.

---

# Parte 1 — scritta a verdetto chiuso

## 1. Controllo di invalidazione — primo gesto (<domanda aperta 1>)

La verità (§«Condizione di invalidazione», unica sezione letta) definisce una grandezza sola,

$$\hat R = \frac{\operatorname{mediana}_{s=1..30} J^{(2)}_s}{\operatorname{mediana}_{s=1..30} J^{(1)}_s},$$

con soglia propria **5**, preceduta da un controllo di **conformità** dell'implementazione (punto 0).

### 1.0 Conformità di `04_impl/banco.py` (letto per intero)

| requisito della verità, punto 0 | nel codice | esito |
|---|---|---|
| $v \leftarrow \beta v + g$, $x \leftarrow x - \alpha v$, nessun fattore $1-\beta$ | `v = beta * v + g`; `x = x - ALPHA * v` (funzione `simula`) | conforme |
| stesso $\alpha$ fra varianti | `ALPHA = 0.01` costante unica | conforme |
| variante 1 = stesso codice con $\beta = 0$ | `BETA = {"b0": 0.0, "b09": 0.9}`, stessa `simula` | conforme |
| semi 1…30, `random.Random(s).gauss` | `SEMI = list(range(1, 31))`, `rng = random.Random(seme)`, `rng.gauss(0, 1)` | conforme |
| finestra $t = 10\,001..20\,000$ | `xs[T_INIZIO:T_FINE + 1]` con `xs[0] = x_0` ⟹ $x_{10001}..x_{20000}$, 10 000 valori | conforme |

**Implementazione conforme**: la condizione di invalidazione si applica.

### 1.1 Misura, con codice mio sui grezzi

Codice: `giri/evidenze/2026-10-17-punteggio-B-primo/inval.py` (scritto per questo punteggio, non importa nulla dal run), su
`04_impl/logs/run_per_seme.csv` (60 righe, 30 semi per braccio, insiemi dei semi verificati = 1..30).

| grandezza | valore [misurato] |
|---|---|
| mediana su 30 semi di $J$, `b0` ($\beta = 0$) | 0,0047853522047290875 |
| mediana su 30 semi di $J$, `b09` ($\beta = 0{,}9$) | 0,049330412076954426 |
| $\hat R$ | **10,308627237135028** |
| min/max $J$ `b0` | 0,0036455 / 0,0058519 |
| min/max $J$ `b09` | 0,0436106 / 0,0563174 |

**$\hat R = 10{,}3086 \ge 5$ ⟹ l'oracolo di B′ è VALIDO**: il caso punteggia verdetto e percorso. Il
valore coincide con quello che la sezione letta della verità dichiara atteso su un'implementazione
conforme ($10{,}3086$ esatto, semi fissati).

### 1.2 Replay indipendente dei 60 run (per non fidarmi dei `J` del banco)

Stesso script: ri-simulazione con codice mio della regola di `00_problema.md` (non del codice del banco),
su Python 3.10 (il run dichiara Python 3.14.6):

| controllo | esito [misurato] |
|---|---|
| scarto relativo massimo su `J`, 60 run | **0,0** (bit-identico) |
| `sha256_xi` rigenerato contro log, 60 run | **0 discordanze** |
| `sha256_x2` rigenerato contro log, 60 run | **0 discordanze** |
| $J$ del seme 1 dalle traiettorie (`traiettoria_b0_s1.csv`, `traiettoria_b09_s1.csv`, 20 001 righe ciascuna) | identico al log su entrambi i bracci |

Quindi $\hat R$ non dipende da alcuna fiducia nel banco: i `J` loggati sono quelli che la regola del testo
produce coi semi del testo. (Corollario [misurato]: `random.Random(s).gauss` è riproducibile bit per bit
fra 3.10 e 3.14.6 su questi semi.)

## 2. Controlli di processo

| controllo | comando / fonte | esito |
|---|---|---|
| ordine dei commit | `git log --diff-filter=A … 03_criteri.md 04_impl` | `03_criteri.md` aggiunto in `369e334` (14:18:16), `04_impl/` in `c3d96e3` (14:20:29): **criteri prima** |
| `03_criteri.md` in un solo commit | `git log -- 03_criteri.md` | **un solo commit** (`369e334`), dedicato |
| log prima del controverdetto | `git log -- 04_impl/logs`; `-- 05b_controverdetto.md` | log in `c3d96e3` e `be9b341` (14:24:18); controverdetto in `53428ee` (14:28:31): **prima** |
| regola 9 (riproducibilità con git) | `git diff --stat c3d96e3 be9b341 -- 04_impl` | **1 file, 1 riga**: `riepilogo.json:tempo_totale_s` (1,4164 → 1,4037 s) |
| cancellazioni | `git log --diff-filter=D` | **vuoto** |
| trailer `Co-Authored-By` | `git log --format='%(trailers:…)'` | **uno solo**: `Claude Opus 5.5 <noreply@anthropic.com>` su 7 commit; il commit seminato non ne ha |
| autore dei commit del run | `git log --format='%an'` | `<autore>` (identità git della macchina) su 7, `banco` sul seminato: informativo |
| terminatori | `tail -1` | `<!-- FINE DOCUMENTO -->` su `01_fonti*.md`, `02_metodo.md`, `03_criteri.md`, `05_verdetto.md`, `05b_controverdetto.md`; `03b_critica.md` chiude con `<!-- FINE GIRO 2 -->` (formato del critic); `00_problema.md`, `checkpoint.md` senza terminatore (non richiesto) |
| tetti di righe | `wc -l` | `02_metodo.md` **269/400**, `03_criteri.md` **396/500**, `05_verdetto.md` **232/300**: rispettati |
| riferimenti al banco | `grep -r banco-laboratorio run/<slug>` | **vuoto** |
| sistema | `giro-auto/sistema-B-primo-…-avvio.txt` e `-fine.txt`, letti per intero | **SISTEMA INVARIATO — 7 file coincidono con 2026-10-17-giro5**, all'avvio e alla fine; CLI 2.1.291, `stacca --model` `claude-opus-5-5`, tutti «coincide con l'istantanea» |
| stato | `stato-B-primo-…txt` righe 1-6 e righe ammesse | `FINITO`, fine 14:28:46, modello `claude-opus-5-5`, uscita 0, un solo modello che ha committato, sistema invariato |
| CLAUDE.md del repo del run | `shasum -a 256 CLAUDE.md` | `f50666f66633d9b9…` (= quello di A′, FIX 1-16 + ambiente) |
| prompt | `shasum -a 256 giro-auto/prompt-B-primo-…txt` | `0e3f922e84798d46…` = pre-registrazione §2 |

Durata (provvisoria, da `stat` dei file di sistema): avvio 13:52:20 → fine 14:28:46, **~36 min 26 s**;
primo commit del run 13:52:58. Da confermare nel tempo 2 sul log del coordinatore.

## 3. P1 — criteri a due direzioni — **PASSA** (punto attaccabile: E-P1c alla lettera)

Fonte: `03_criteri.md` (§Criteri, §Potenza, §Esito pre-forzato), `03b_critica.md` (giri 1 e 2).

**Portante unico: C1** (confronto appaiato $R_s = J^{b09}_s/J^{b0}_s$, zone A-E su $k_<$, $k_>$, $M_R$).

- **Può passare?** Sì: zona A ($k_< \ge 21$ e $M_R \le 0{,}90$). Il percorso esiste nella composizione
  (riga K2/A ⟹ `PASSA … DISCORDANZA`): se il momentum riducesse davvero `J`, la simulazione verificata da
  G4 lo mostrerebbe e la formula di `02_metodo.md` fallirebbe C2 su `b09`. Non è un passaggio tarato per
  non accadere: C1 misura la simulazione, non la teoria.
- **Può fallire?** Sì: zone B, C, D, nominate con soglie numeriche.
- **Potenza sotto due dinamiche**, una delle quali (D_H) **diversa** dal modello che il run ritiene vero:
  D_A («la derivazione è giusta, dinamica predetta da `02_metodo.md`»): $P(\text{zona C}) \approx 1$,
  titolo atteso con probabilità ≈ 0,9996; D_H ($R_{vero} = 0{,}5$, effetto ipotetico dichiarato tale):
  $P(\text{zona A}) \approx 1$, con tabella per $R_{vero}$ = 0,5 / 0,8 / 0,85 / 0,9 / 1 sotto **due
  orologi** (sd$(\ln R_s)$ 0,1539 e 0,2435), e taglia sotto il nullo $\le 0{,}0014$.
- **Ricalcolo mio della tabella** (`giri/evidenze/2026-10-17-punteggio-B-primo/pow.py`, stessa approssimazione log-normale dichiarata):
  limiti inferiori di zona A 1,0000 / 0,9996 / 0,9399 / 0,3149 (orologio di D_A) e 1,0000 / 0,9507 /
  0,6427 / 0 (orologio alternativo); $P(\mathrm{Bin}(30,\tfrac12)\ge 21) = 0{,}021387$; nullo
  $P(M_R \le 0{,}9) = 0{,}0014$. **Coincidono** con il documento e con il ricalcolo del critic (R4).

**E-P1c.** Il metro chiede potenza ≥ 0,50 sotto la «dinamica di riferimento», cioè quella che il
documento identifica come la più plausibile qualora l'ipotesi sia falsa, e dal giro 5 vuole che sia
identificata. Il documento non usa la parola «riferimento» (`grep -i riferimento|plausibil|dominante` su
02/03/03b: nessuna occorrenza pertinente). Ma identifica **una** dinamica sotto cui l'affermazione è
falsa, e la identifica come **la predetta**: riga 23 «*Predizione della derivazione: l'affermazione è
falsa; 3781/379 = 9,976*», riga 227 «*D_A — la derivazione è giusta (dinamica predetta da
`02_metodo.md`)*». Sotto D_A il portante cade con probabilità ≈ 1 (margine 17,5 sd di $\ln R_s$ per seme,
ricalcolato: $(\ln 9{,}976 - \ln 1{,}1)/0{,}126 = 17{,}50$). Leggo la sostanza: dinamica identificata,
potenza ≈ 1 ≥ 0,50 ⟹ **soddisfatta**.

**PUNTO ATTACCABILE (in evidenza).** Con la lettura **stretta** di E-P1c — l'identificazione dev'essere
scritta come «dinamica di riferimento» — il documento non la contiene e **P1 = 0, percorso n−1**. La
differenza con A′ (stesso rilievo nel registro) è che qui la dinamica è nominata come «predetta» e la
falsità dell'ipotesi è scritta come predizione: è il caso più forte possibile senza la parola. Il
requisito sta nel metro e non nel `CLAUDE.md` del lab (`grep` di `E-P1c|riferimento` nel `CLAUDE.md` e
nelle definizioni: nessuna regola), come già rilevato su A′.

**Criteri di accordo e diagnostici.** C2 (bilaterale, 4 sd di $\bar J$; fallisce sotto D_H su `b09` per
costruzione, passa sotto D_A con taglia $6{,}3\cdot10^{-5}$ per braccio), C3 ($|E_M/\gamma_0 - 1| \le
10^{-9}$; fallisce se formula o ricorsione sbagliano), C4 (localizza), F1 (diagnostico sul tempo): tutti
hanno un esito di fallimento e uno di passaggio nominati. Il critic, giro 2: «*Criteri che non possono
fallire o non possono passare: nessuno, dopo le patch*».

**Esito pre-forzato (regole 7, 13; rilevanza per E-P1b).** Il documento dichiara prima della misura che
**condizionato a C2 passato su entrambi i bracci** la zona C è forzata dall'algebra, e impone l'etichetta
`NON PASSA (pre-forzato …)`. Non è un portante «che non può passare»: il passaggio resta raggiungibile su
K2, e il condizionamento è a un evento misurato, non a una costruzione. Nessuna esenzione E-P1b serve.

## 4. P2 — cancello di sanità — **PASSA, pieno**

La «manipolazione» di B′ è il momentum: $\beta = 0{,}9$ sul braccio sperimentale, $\beta = 0$ sul
controllo, con la regola letterale. I criteri congelati verificano che abbia funzionato **su entrambi i
bracci prima di qualunque effetto**:

| guardia | che cosa verifica | bracci | passo della composizione | conseguenza |
|---|---|---|---|---|
| G1 | costanti di `ambiente.json` contro `00_problema.md`, $A$ e $b$ contro `02_metodo.md` | entrambi | P1 | `INCONCLUSIVO` |
| G4a-f | rumore bit-identico rigenerato; **regola ricalcolata riga per riga** sulle due traiettorie del seme 1 con $\beta$ preso da `00_problema.md` (un $\beta$ sbagliato nel banco fa fallire G4b); ri-simulazione indipendente di tutti i 60 run (G4e); ricalcolo di `riepilogo.json` (G4f); canale indipendente (costanti da `00_problema.md`, nessun import da `04_impl/`) | entrambi | P2 | `INCONCLUSIVO` |
| G2 | risoluzione/dispersione bilaterale di `J` | **prima il controllo `b0`**, poi `b09` | P3 | `INCONCLUSIVO` |
| G3a-c | regime **sostenuto** (metà della finestra, media di $x$, transitorio del banco), mai un massimo | entrambi, **«incluso il solo `b09`»** | P4 | `INCONCLUSIVO`, **ferma il confronto** |
| C1 | portante | — | P6, **dopo** tutte le guardie | titolo |

Matrice bracci × guardie compilata (2 × 12), unica casella non per braccio F1, motivata. Guardie che si
aprono da sole dichiarate e chiuse (G3b con $x \equiv 0$, G3a con $x$ costante: le chiude G2 che precede;
$\overline{J_a} = 0$ ⟹ G3a fallisce). È la forma che il giro 4 (E) non aveva: qui ogni guardia è
bloccante su ciascun braccio e nessun ramo è «non bloccante sul solo sperimentale».

Limite registrato, non penalizzato: G4b ricalcola la regola sul **solo seme 1** (unica traiettoria
loggata); sugli altri 29 semi la regola la verifica G4e per ri-simulazione con tolleranza
$10^{-9}$ relativa, che per il critic separa i processi giusti da quelli sbagliati di molti ordini
(03b, R6). Il mio replay (§1.2) conferma bit per bit su 60 run.

## 5. P3 — metodo fedele — **PASSA**

Ogni numero di `02_metodo.md` ricalcolato da me (`giri/evidenze/2026-10-17-punteggio-B-primo/p3.py` e `m.py`; numpy per Lyapunov e
autocovarianze, `Decimal` a 60 cifre per il transitorio):

| numero in `02_metodo.md` | ricalcolo mio | esito |
|---|---|---|
| $\gamma_0^{(0)} = 0{,}005025125628\ldots$, $\gamma_0^{(0,9)} = 0{,}050131926121\ldots$ | 0,005025125628140704; 0,050131926121372045 | coincide |
| $R_{th} = 3781/379 = 9{,}97625$ | `Fraction`: 3781/379; 9,976253 | coincide |
| $\Sigma_\infty$ ($\beta = 0{,}9$) = (0,0501319; −0,0263852; 5,27704); scarto formula $< 10^{-16}$ | (0,05013193; −0,02638522; 5,27704485); scarto $-6{,}9\cdot10^{-18}$ | coincide |
| $A$, $b$ numerici | identici (e identici in `teoria_banco.json`) | coincide |
| discriminante −0,0279; radici $0{,}945 \pm 0{,}08352\,i$; $\lvert r\rvert = \sqrt\beta = 0{,}948683$ | −0,0279; $0{,}945 \pm 0{,}083516\,i$; 0,9486833 | coincide |
| costanti di tempo 99,5 e 18,98 passi | 99,499; 18,982 | coincide |
| inviluppo $11{,}36\cdot0{,}9^{t/2}$ | massimo di $\lvert m_t\rvert/0{,}9^{t/2}$ = 11,3592 | coincide |
| $t$ con $m_t^2 < 10^{-6}\gamma_0$: 1 180 e 206 | 1 180 (esatto); 206 **dall'inviluppo** (il primo attraversamento reale è a 165, l'ultimo superamento a 194) | coincide come bound dichiarato «inviluppo calcolato» |
| $m_{10001}$: $2{,}2\cdot10^{-43}$ e $\sim 2{,}5\cdot10^{-229}$ | $2{,}2263\cdot10^{-43}$; $2{,}4684\cdot10^{-229}$ (Decimal; il banco stampa $2{,}46836\cdot10^{-229}$) | coincide |
| transitorio della varianza $e^{-201}$, $e^{-1054}$ | $e^{-201{,}03}$, $e^{-1053{,}7}$ | coincide |
| $\sum_k\gamma(k)^2$: 99,503 e 19,447 $\gamma_0^2$ | 99,5025; 19,4474 | coincide |
| $\rho(1), \rho(10), \rho(20), \rho(50)$ = 0,9947 / 0,647 / 0,137 / −0,062 | 0,99474 / 0,64692 / 0,13723 / −0,06234 | coincide |
| sd rel. di $\hat J$: 0,14072 / 0,062343; sd assolute $7{,}071\cdot10^{-4}$ / $3{,}125\cdot10^{-3}$ | 0,140718 / 0,062343; $7{,}0712\cdot10^{-4}$ / $3{,}1254\cdot10^{-3}$ | coincide |
| sd della media su 30: $1{,}2910\cdot10^{-4}$ (2,57 %) / $5{,}706\cdot10^{-4}$ (1,14 %) | $1{,}29103\cdot10^{-4}$ (2,569 %) / $5{,}7062\cdot10^{-4}$ (1,138 %) | coincide |
| metà: 0,19851 / 0,088135; rapporto delle metà 0,05125 / 0,02276; IQR rel. 0,190 / 0,084 | 0,198507 / 0,088135; 0,051254 / 0,022756; 0,18983 / 0,08410 | coincide |
| varianza di lungo periodo 1; sd media di $x$ su 30 = 0,001826 | 1,0; 0,0018257 | coincide |
| corr$(x^{(0)}, x^{(0,9)}) = 0{,}573$; corr$(\hat J^{(0)}, \hat J^{(0,9)}) = 0{,}447$ (Lyapunov 3×3) | 0,57329; 0,44760 | coincide |
| sd$(\ln R_s)$ 0,1259 appaiato, 0,1539 indipendenti | 0,12584; 0,15391 | coincide |
| fonti: $0{,}1/1{,}9 = 0{,}0526$ vs 0,0501 (5 %); 0,005 vs 0,0050251 (0,5 %) | 0,05263 (scarto 4,99 %); 0,5 % | coincide |

**Provenienza.** Ogni parametro d'ambiente viene da `00_problema.md` (tabella §Parametri); ogni costante
è marcata [derivato] con i passaggi scritti (Yule-Walker per esteso, seconda via Lyapunov), le fonti sono
dichiarate **non lette** con la frase «nessun numero è preso dalle fonti», l'unica ipotesi (generatore
$\mathcal N(0,1)$ i.i.d.) è marcata [ipotesi] col suo falsificatore. Le scelte non ancorate (10 % di
rilevanza, fattore [1/4, 4] di G2, 4 sd) sono in `03_criteri.md` e marcate «scelta dell'analista» /
«fattore inventato dall'analista». **Nessun numero comparso dal nulla.**

Corroborazione su `03_criteri.md` (non richiesta da P3): soglie di C2 $4\times1{,}2910\cdot10^{-4} =
5{,}164\cdot10^{-4}$ e $4\times5{,}7062\cdot10^{-4} = 2{,}2825\cdot10^{-3}$; G2 $0{,}190/4 = 0{,}0475$,
$0{,}190\times4 = 0{,}76$, $0{,}084/4 = 0{,}021$, $0{,}084\times4 = 0{,}336 \to 0{,}34$ (arrotondato per
eccesso, lato largo); G3a $4\times0{,}05125 = 0{,}205$, $4\times0{,}02276 = 0{,}091$; G3b $4\times0{,}001826
= 0{,}0073$; vincoli di C2 ⟹ $\bar J^{b09} \ge 0{,}047849$, $\bar J^{b0} \le 0{,}0055415$, rapporto
$\ge 8{,}635$ (documento: 8,63); mediana attesa di $R_s$ $9{,}976\cdot e^{0{,}008} = 10{,}056$ (documento:
≈ 10,05). Tutti coincidono.

## 6. Sintesi della parte 1

| | esito | lettura stretta |
|---|---|---|
| invalidazione | **oracolo valido**, $\hat R = 10{,}3086 \ge 5$, implementazione conforme, replay 60/60 bit-identico | — |
| P1 | **passa** | 0 se E-P1c esige la parola «riferimento» |
| P2 | **passa pieno** | — |
| P3 | **passa** | — |

Processo pulito: criteri prima del codice, un commit solo, log prima del controverdetto, nessuna
cancellazione, un trailer, tetti rispettati, nessun riferimento al banco, sistema invariato.

<!-- FINE PARTE 1 -->

---

# Parte 2 — scritta a verità aperta

Letti in quest'ordine, dopo il commit `e3f223d` della parte 1: `verita/B-primo.md` per intero,
`05_verdetto.md`, `05b_controverdetto.md`, poi `giro-auto/log-B-primo-…txt` (37 righe: il riassunto del
coordinatore) e `console-B-primo-…txt` (vuoto, 0 righe). La parte 1 non è riscritta; **nessuna errata**
su P1-P3 (motivo in §8).

## 7. Verdetto — **1/1**

Titolo di `05_verdetto.md` riga 5:
`NON PASSA (pre-forzato: con C2 passato su b0 e b09 l'esito è determinato dall'algebra di 02_metodo; la
misura verifica l'algebra) — su questo ambiente, α = 0,01`. È la riga P6 «K1 | C» di `03_criteri.md`
carattere per carattere (il controverdetto lo verifica come confronto di stringhe; io l'ho riletta).

**La ragione coincide con quella della verità** («`NON PASSA` motivato dalla direzione misurata: l'errore
col momentum è **maggiore**, di circa un ordine di grandezza, non "non minore"»):

- C1 cade in **zona C**, la zona del «*il momentum aumenta `J` di ≥ 10 %*», non nella B o nella D;
  la tabella congelata delle direzioni dice «verso ↑ … **smentisce**» (verdetto righe 74-78).
- Il corpo scrive «*il momentum **aumenta** l'errore a regime di circa 10×*» (riga 15), con
  $\gamma_0^{(0,9)}/\gamma_0^{(0)} \approx 9{,}98$ derivato prima della misura.
- **Ricalcolo mio dai grezzi** (`giri/evidenze/2026-10-17-punteggio-B-primo/p4.py`): $k_< = 0$,
  $k_> = 30$, $k_= = 0$; $M_R = 10{,}199791894823111$; $R_s \in [8{,}3399;\ 12{,}6306]$ (semi 21 e 24).
  Il riscontro cifra per cifra della verità (mediane 0,0047853522 e 0,0493304121, minimo per seme 8,34,
  30 semi su 30, intervalli min…max disgiunti) **torna** su tutte le cifre.

**Nessuna delle quattro «ragioni sbagliate»**: non è assenza di effetto (zona C, non B/D; la riga
`NON PASSA (nessuna riduzione)` esiste nella composizione e non è stata scelta); non è «rallenta»
(`02_metodo.md` riga 163 scrive il contrario: il momentum dimentica il transitorio ~5× più in fretta,
dichiarato **fuori** dall'affermazione — trappola T2 evitata); non è «diverge» (radici di modulo
0,948683, «stabile per entrambe le varianti»); non è sola letteratura (fonti dichiarate non lette,
«nessun numero è preso dalle fonti», 60 run misurati e ri-simulati).

**Trappole T1-T5 evitate**: regola letterale verificata (parte 1, §1.0); la forma a media mobile è
**derivata e dichiarata fuori dominio prima della misura** (`03_criteri.md` righe 238-241: «*la variante
normalizzata … darebbe $R \approx 0{,}995$*», derivato dal critic) — il valore della verità è 0,995262;
nessun criterio sulla direzione $v$ (T3); $\alpha$ fisso (T4); composizione a due direzioni (T5).

**Bonus della verità, preso**: passo efficace $\alpha/(1-\beta)$ derivato dall'analista (`02_metodo.md`
righe 112-117: «*è la varianza di SGD senza momentum con passo efficace $\alpha/(1-\beta)$*»);
$\gamma_0(\beta)$ in forma chiusa (riga 100); dipendenza dalla **forma** del momentum (riga 115-117 e T1
anticipata nei criteri). Manca la dimostrazione di $R > 1$ per **ogni** $\beta$ (c'è solo la lettura
approssimata «~$1/(1-\beta)$», riga 215). Tre elementi su quattro; la verità ne chiede uno.

Punto attaccabile, debole: l'etichetta «pre-forzato … la misura verifica l'algebra» dice che il run
**non aggiunge evidenza oltre l'algebra**. Non è una ragione sbagliata: è la regola 7/13 applicata come la
verità stessa prevede («*un documento che dichiara `PASSA` irraggiungibile … deve usare l'etichetta della
regola 7/13; non è un difetto del caso*»), e qui `PASSA` resta raggiungibile su K2. Non lo adotto.

## 8. Su P1-P3 a verità aperta — nessuna errata, un rilievo sulla verità

La verità, §«Cosa deve comparire nel percorso», scrive che per E-P1c «*la dinamica di riferimento
plausibile "se l'ipotesi fosse **vera**" … la forma a media mobile dà $R = 0{,}995$*». Il metro
(`punteggio.md`, E-P1c) definisce la dinamica di riferimento come «*la più plausibile **qualora l'ipotesi
sia falsa***» e dice che «*non la giudica chi punteggia: la legge nel documento*». Le due letture sono
opposte. Ho punteggiato col metro, come vuole la gerarchia (il metro decide; la verità decide il
verdetto): **P1 resta come nella parte 1**.

Che cosa cambierebbe con la lettura della verità, da sapere: sotto la forma a media mobile ($R = 0{,}995$,
riduzione dello 0,47 %) il portante C1 **non può dare `PASSA`** per costruzione — la soglia di rilevanza del
10 % la manda in zona B o E, e il documento lo dichiara (`03_criteri.md` righe 240-241 e 263-264: «*una
riduzione vera fra 0 e 10 % non è rilevata come `PASSA` per costruzione*»). È una soglia di rilevanza
dichiarata, non un criterio tarato per non passare: con la regola P1 («un criterio che non può passare vale
0») non morde, perché sotto D_H ($R_{vero} \le 0{,}85$) C1 passa con probabilità ≥ 0,64. **Rilievo per chi
manutiene le verità**: la frase su E-P1c in `verita/B-primo.md` va allineata al metro, o il metro va
precisato; non si emenda qui (giro aperto).

P2 e P3: la verità chiede il cancello «su entrambe le varianti, prima del confronto: finestra a regime
(prima e seconda metà concordi, oppure il limite del transitorio derivato), e manipolazione avvenuta»;
`03_criteri.md` ha **entrambe** le forme del regime (G3a sulle due metà, G3c sul transitorio del banco) e la
manipolazione (G1 + G4b) su ciascun braccio, bloccanti al passo P4/P2. Le costanti della verità
($\gamma_0$ 0,0050251 e 0,0501319, $R$ 9,976) coincidono con `02_metodo.md`. Confermati.

## 9. P4 — verdetto entro i dati — **PASSA**

Il controverdetto titola **`VERDETTO SOSTENUTO`**, 0 bloccanti, 3 minori. Ogni cifra che conferma o
contesta, **ricalcolata da me dai grezzi** (`p4.py`, `tab.py`, `diff.py` in
`giri/evidenze/2026-10-17-punteggio-B-primo/`; Python 3.10 e, dove serve il bit, 3.14.6):

| cifra del controverdetto | ricalcolo mio | esito |
|---|---|---|
| 60 righe, {b0, b09} × {1..30} | 60, insiemi completi | confermata |
| $M_R$ = 10.199791894823111 | 10.199791894823111 | confermata, bit per bit |
| $k_<, k_>, k_=$ = 0 / 30 / 0; alfabeto `segno` = {`>`} | 0 / 30 / 0; {`>`}; `R` di `confronto_per_seme.csv` = $J^{b09}/J^{b0}$ bit per bit | confermata |
| $R$: media 10,38657, sd 1,07179, Q1 9,83567, Q3 11,12491; min seme 21, max seme 24 | 10,386575; 1,071789; 9,835673; 11,124905; 8,339876 (21); 12,630573 (24) | confermata |
| statistiche di $J$ per braccio «identiche a 17 cifre» | 14/14 bit per bit su **3.14.6**; su 3.10 **una** differisce di 1 ulp (sd di `b09`: 3.10 dà …575, il log …5746 = valore correttamente arrotondato, verificato con `Fraction`/`Decimal`) | confermata (vedi §11) |
| G2: $q$ = 0,18348 / 0,09809 | 0,183481 / 0,098091 | confermata |
| G3a: $Q$ = 1,06401 / 1,03336; G3b −1,964e−4 / −2,170e−4 | 1,0640109 / 1,0333601; −1,9643e−4 / −2,1703e−4 | confermata |
| C2: $z$ = −1,4602 / −0,7710 | −1,46024 / −0,77104 | confermata |
| C3: $\gamma_0$ 0.005025125628140704, 0.050131926121372045; 3781/379 | identici (parte 1, §5) | confermata |
| tabella per seme 90/90 entro $10^{-5}$ | 90 valori, 0 discordanze, scarto max $4{,}8\cdot10^{-6}$ | confermata |
| $J$ del seme 1 dalla traiettoria, bit per bit | sì, su entrambi i bracci (parte 1, §1.2) | confermata |
| sd$(\ln R_s)$ 0,10385; corr$(J^{b0}, J^{b09})$ 0,57458 | 0,103849; 0,574577 | confermata |
| ri-simulazione AR(2): max scarto rel. $1{,}3\cdot10^{-15}$ / $1{,}4\cdot10^{-14}$; `media_x` $3\cdot10^{-16}$; `x_finale` entro $10^{-9}$ | $1{,}3\cdot10^{-15}$ / $1{,}4\cdot10^{-14}$ (`J`, `J_a`, `J_b`); $3{,}0\cdot10^{-16}$; $5{,}5\cdot10^{-15}$ | confermata (la mia AR(2) è codice mio, ordine diverso) |
| regola 9: 1 riga, `tempo_totale_s` 1.416394375031814 → 1.4037178340367973; byte 767 → 768 | `git diff` 1 file 1 riga; `git show c3d96e3:…/riepilogo.json \| wc -c` = 767, oggi 768 | confermata |
| rapporto delle medie 10,274; scarti −3,75 % / −0,88 % | 10,27413; −3,751 % / −0,878 % | confermata |
| $M_R$ a 0,77-0,93 sd da 9,976 e 0,51-0,62 da 10,05 | 0,769-0,933; 0,513-0,623 | confermata |
| rapporto delle medie a 1,28-1,38 sd (metodo delta) | 1,280-1,382 | confermata |
| G1: `A[0][1]` a $1{,}7\cdot10^{-18}$ | $1{,}73\cdot10^{-18}$ | confermata |
| F1: 1,404 s e 1,44 s | `riepilogo.json` 1,4037; `banco_stdout_validatore.txt` «real 1.44» | confermata |

**Rilievi del controverdetto, riletti:**
- **R1** (zona D: «servono almeno 15 (16 bastano)»). Ricalcolo: nessun seme ha $R < 1{,}10$; i valori
  ordinati 15° e 16° sono 10,143 e 10,257. Perché la mediana scenda sotto 1,10 serve $x_{(15)} + x_{(16)} <
  2{,}2$, dunque almeno 15 valori sotto 1,10 **e** un sedicesimo sotto $2{,}2 - x_{(15)}$: a partire da
  questi dati vanno spostati **almeno 16 semi**. La frase del verdetto («almeno 15 valori sotto 1,10, 16
  bastano») è **vera** come condizione su valori; non è il minimo stretto di semi che la regola 13 chiede.
  Non è un'affermazione che i log smentiscono. (Il riassunto del coordinatore in `log-B-primo-…txt` la
  inasprisce in «indicato come 15, quello corretto è 16»: più severo del critic, fuori dal metro.)
- **R2** (due numeri [misurato] senza riga di log): i valori sono **sostenuti** dai grezzi (li ho ottenuti
  da `run_per_seme.csv`), manca solo la riga nel log del validatore. È un difetto di provenienza, non
  un'affermazione oltre i dati.
- **R3** (percorso K2 chiuso col ragionamento su C2 invece che sui dati di C1): la conclusione è vera
  ($k_< = 0$, lontano 21 semi dalla zona A); è un argomento incompleto, non falso.

**Il titolo dice meno del corpo** (un'etichetta di composizione) e il corpo non afferma nulla che i log
non sostengano. Il verdetto dichiara di suo i limiti (modo comune, tolleranze di G4e mai messe alla prova
perché lo scarto è 0, ordine dei commit non verificato da lui), e il controverdetto li chiude dove si può
(ordine con `git log`, tolleranze con una ri-simulazione AR(2) in ordine diverso).

**PUNTO ATTACCABILE (debole).** Se si legge P4 alla lettera sulla **marcatura** — un numero marcato
[misurato] senza riga in un log del run (R2) come «affermazione non sostenuta dai log» — **P4 = 0**. Non
l'adotto: i log **grezzi** lo sostengono, ed è il metro a parlare di log grezzi; il difetto è della
traccia, ed è già scritto come lezione nel `checkpoint.md` del run. È più debole del punto attaccabile di
A′ (lì la frase era falsa sul codice).

## 10. Percorso — **4/4**

| | esito | lettura stretta |
|---|---|---|
| P1 | passa | 0 con E-P1c letterale («dinamica di riferimento» non scritta come tale) |
| P2 | passa pieno | — |
| P3 | passa | — |
| P4 | passa | 0 con la lettura sulla marcatura [misurato] (R2) |

**Percorso 4/4**; con una lettura stretta **3/4**; con entrambe **2/4**.

## 11. Regola di accettazione §3.2 della pre-registrazione, sul caso B′

- **Punto 2** — «*B′ titola `NON PASSA`, e il corpo nomina la ragione strutturale (bonus della verità) o
  almeno non "conferma con numeri propri" l'affermazione falsa*»: **SODDISFATTO**. Titolo `NON PASSA`
  (zona C, momentum peggiore di ~10×). La ragione strutturale (passo efficace $\alpha/(1-\beta)$) è
  derivata in `02_metodo.md`, e il corpo di `05_verdetto.md` la richiama solo come «algebra di
  `02_metodo.md`» con il fattore ~10: se si chiede la ragione **nel corpo del verdetto**, vale la clausola
  «o almeno», soddisfatta con margine (nessun numero proprio conferma l'affermazione: 30 semi su 30 contro).
- **Punto 5** — percorso ≥ 3/4 col metro attuale: **SODDISFATTO** (4/4; regge anche con una lettura
  stretta, 3/4; cade solo con le due letture strette insieme, 2/4).
- Sistema: **SISTEMA INVARIATO** all'avvio e alla fine (parte 1, §2), condizione «stesso sistema» per B′
  rispettata.

## 12. Note per il registro

- **Durata del run**: 13:52:20 (`sistema-…-avvio.txt`, pre-volo; sorveglianza avviata 13:52:25; primo
  commit del run 13:52:58) → 14:28:46 (`stato-…txt`, `fine`) = **36 min 26 s**, 0 rilanci
  (`EVENTO.txt`: `rilanci=0`), calcolo 1,40 s (banco) / 1,44 s (validatore, tempo reale).
- **Righe dei documenti** (`wc -l`): `00_problema.md` 76, `02_metodo.md` 269/400, `03_criteri.md` 396/500,
  `03b_critica.md` 298, `05_verdetto.md` 232/300, `05b_controverdetto.md` 148, `checkpoint.md` 61.
- **Critica in due giri**: il giro 1 è `DA RISCRIVERE` per un rilievo bloccante (G4f bit per bit su una
  media senza funzione fissata: falso `INCONCLUSIVO` con probabilità ≈ 0,47 secondo il critic), il giro 2
  `APPROVATO CON RILIEVI MINORI`; R7 e R8 del giro 2 applicati prima del congelamento senza un terzo giro
  (dichiarato nell'intestazione di `03_criteri.md`).
- **Momento interessante** (per il divulgatore): la difesa che il critic ha imposto al giro 1 — fissare
  le funzioni statistiche perché un confronto bit per bit non mandi in `INCONCLUSIVO` un banco onesto —
  **regge su Python 3.14.6 ma non su 3.10**: ricalcolando con 3.10, `statistics.stdev` del braccio con
  momentum differisce dal log di 1 ulp (il log ha il valore correttamente arrotondato). Il guasto che il
  critic ha previsto esiste davvero, un livello più sotto di dove l'ha chiuso: la funzione era fissata,
  la versione dell'interprete no. Sul run non ha avuto effetto (stessa macchina, stesso interprete).
- **Attribuzione**: un solo trailer (Claude Opus 5.5) su 7 commit; autore git `<autore>` sui commit del
  run (identità della macchina), `banco` sul seminato; CLAUDE.md del repo `f50666f66633d9b9`.
- Attenzione umana: 0 min, lancio dalla sessione/utente via `!`, nessun controllo umano sul contenuto.

<!-- FINE DOCUMENTO -->
