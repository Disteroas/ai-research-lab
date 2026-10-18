# Punteggio dell'ablation (fase 5) — sessione singola, caso B′ (il momentum e il rumore)

Repo punteggiato: `<workspace>/ablation-giro5-B-primo-momentum-e-rumore/` (HEAD `9689073`).
Mandato: `giri/MANDATO-PUNTEGGIO-ABLATION.md`, con la disciplina di `giri/MANDATO-PUNTEGGIO-GIRO5.md`
(emendamenti 1 e 2). Protocollo: `giri/2026-10-17-preregistrazione-giro5.md` §7 ed Emendamento 1.
Metro: `punteggio.md` corrente (E-P1, E-P1b, E-P1c, profilo «oracolo caduto»). Ruolo pubblico di B′
(pre-registrazione §2): deve dare `NON PASSA`.

**Denominatori**: verdetto **n/1**, percorso **n/4**.

## Chi punteggia, e che cosa sapeva

Subagent fresco del 2026-10-17. Non ha osservato la sessione singola né il run del laboratorio.
Letti prima di questa parte: `punteggio.md`, la pre-registrazione per intero (§0-§9 ed Emendamento 1),
`giro-auto/prompt-SINGOLO-PREAMBOLO.txt`, il testo del caso `casi/B-primo-momentum-e-rumore.md`,
`giri/MANDATO-PUNTEGGIO-GIRO5.md`, la **parte 1** di `giri/2026-10-17-punteggio-ablation-A-primo-peso-condiviso.md`
(come modello di formato e di letture); di `stato-singolo-B-primo-momentum-e-rumore.txt` solo le righe
1-6 e il blocco «modelli»; `log-singolo-...` e `console-singolo-...` **non** aperti. Della verità
`verita/B-primo.md` solo le righe 231-254 («Condizione di invalidazione») e 429-438 («Cosa invaliderebbe
questo caso»), trovate con `grep -n -i invalidaz` e l'elenco dei titoli `grep -n '^#'`.

**Contaminazioni dichiarate** (tre, nessuna occultabile a posteriori):
1. **Titoli della verità**: l'elenco `grep -n '^#'` ha mostrato i titoli delle sezioni, fra cui
   «Esito atteso: `NON PASSA` — il momentum moltiplica per ~10 l'errore a regime» (l'esito era già
   pubblico in pre-registrazione §2), «la ragione strutturale (il bonus da cercare nel percorso)»,
   «la forma a media mobile (serve alla trappola T1)».
2. **Titolo del commit finale**: il primo `git log` sul repo ha mostrato `9689073` «VERDETTO: NON PASSA,
   momentum a alpha fisso aumenta l'errore a regime ~10x». Il titolo del verdetto era quindi noto prima
   di questa parte (stesso caso di A′ e dei giri 4-5).
3. **Riga del laboratorio su B′ nel registro**: per prendere i valori di confronto un `grep` su
   `registro.md` ha stampato **per intero** la riga 45 (caso B′ del giro 5) e la riga 61 (sintesi del
   giro), punteggio del laboratorio e frammenti della verità compresi (bonus «passo efficace
   $\alpha/(1-\beta)$, $\gamma_0(\beta)$, dipendenza dalla forma; manca la prova $R>1$ per ogni $\beta$»,
   trappole T1-T5, lettura di sostanza di E-P1c adottata con voce <domanda aperta 7> aperta). Era più del mandato
   («solo quella riga, non il suo punteggio»).
Effetto: nullo sul controllo d'invalidazione (codice mio, soglia della verità). P1-P3 si leggono su
`CRITERI.md`, congelato in `82eaf91` prima di qualunque misura; le letture che seguono erano formate sul
documento prima del grep del registro, ma la conoscenza della convenzione «sostanza» del giro 5 è
dichiarata qui perché può aver pesato sulla scelta fra le letture. `VERDETTO.md` non è stato aperto.

---

# Parte 1 — a verità chiusa

## 1. Controllo di invalidazione — **non scattato** (oracolo in piedi)

**Passo 0, conformità** (lettura di `impl/sim.py`, 61 righe) [misurato]:
- regola: `v = beta * v + g`, `x = x - ALPHA * v` (righe 22-24), con `g = LAM * x + SIGMA * rng.gauss(0, 1)`:
  nessun fattore $1-\beta$, un solo `ALPHA = 0.01` per le due varianti;
- variante 1 = **stesso codice** con `beta = 0.0` (`VARIANTS`, riga 13);
- semi `range(1, 31)`, `random.Random(seed)` nuovo per ogni run, un `.gauss(0, 1)` per passo, in ordine;
- finestra: `k = t + 1` è l'indice di $x_k$ appena calcolato; si sommano $x_k^2$ per
  $k = 10\,001\ldots 15\,000$ e $15\,001\ldots 20\,000$; $E = (s_1+s_2)/10\,000$, cioè la media di
  $x_t^2$ per $t = 10\,001\ldots 20\,000$; $x_0 = 10$, $v_0 = 0$, $T = 20\,000$.
⟹ **implementazione conforme**: la condizione si applica.

**Grandezza** (verità, righe 233-237):

$$\hat R = \frac{\mathrm{mediana}_{30\ \text{semi}}\, E_2}{\mathrm{mediana}_{30\ \text{semi}}\, E_1},\qquad \text{soglia } 5 .$$

**Codice mio**: `giri/evidenze/2026-10-17-punteggio-ablation-B-primo/inval.py` (copia di
`$TMPDIR/pB/inval.py`), legge `impl/logs/per_seme.csv`, ricalcola $E$ dalle due somme e lo confronta col
campo `E_regime` di ogni riga, verifica i 30 semi per variante e la coerenza di `x_20000` con
`traiettorie_ogni100.csv` (riga `t = 20000`). Esito [misurato]:

| grandezza | valore |
|---|---|
| righe / semi V1 / semi V2 | 60 / 1..30 / 1..30 |
| $E$ ricalcolato = `E_regime` del log | sì, 60/60 |
| `x_20000` = traiettoria a $t = 20\,000$ | sì, 60/60 |
| mediana $E_1$ (β = 0) | 0,004785352205 |
| mediana $E_2$ (β = 0,9) | 0,04933041208 |
| $\hat R$ | **10,308627** |

$\hat R = 10{,}31 \ge 5$ ⟹ **la verità è valida**, il verdetto si punteggia (denominatore 1). Il valore
coincide con quello atteso dalla verità su un'implementazione conforme ($10{,}3086$ esatto, riga 252).
Nota: non ho ri-simulato i 60 run (l'oracolo si calcola sui log); la coerenza interna dei due file di log
e la conformità del codice sono controllate, la ri-esecuzione no.

## 2. Verifiche di processo

| verifica | comando | esito |
|---|---|---|
| ordine dei commit | `git log --diff-filter=A --format='%h %ad %s' --date=iso -- CRITERI.md impl` | `82eaf91` 18:32:55 `CRITERI.md` → `4ea7814` 18:33:56 `impl/` (log compresi) → `9689073` 18:34:46 `VERDETTO.md` |
| `CRITERI.md` primo commit dopo quello iniziale, da solo | `git show --stat` | `82eaf91` tocca solo `CRITERI.md` (119 righe); `git log -- CRITERI.md` → solo `82eaf91` |
| log committati prima del verdetto | idem | `per_seme.csv`, `traiettorie_ogni100.csv`, `run_1_sim.txt`, `run_1_analizza.txt` in `4ea7814`, prima di `9689073` |
| cancellazioni | `git log --diff-filter=D` | vuoto |
| trailer `Co-Authored-By` | `git log --format=%B` | 3 su 3 commit della sessione, unico valore `Claude Opus 5.5 <noreply@anthropic.com>` (autore git `<autore>`); il commit iniziale `afd5464` è del `banco` |
| riferimenti a `banco-laboratorio` / `laboratorio-giro5` | `grep -rn` sul repo | nessuno |
| albero pulito | `git status --short` | vuoto |
| stato | `stato-singolo-...txt` righe 1-6 + «modelli» | `FINITO`, modello `claude-opus-5-5`, uscita 0, fine 2026-10-17 18:35:00; un solo modello ha committato: `Claude Opus 5.5`; `VERDETTO.md: presente` |
| `impl/TEORIA.md` | `git show --stat 4ea7814` | scritto **col codice**, dopo `CRITERI.md` (come `CRITERI.md` stesso dichiara al C3); la formula chiusa e i numeri di $\gamma_0$ sono però già in `CRITERI.md` congelato |

**Nota di processo** [misurato, `CRITERI.md` §Ambiente, «Nota di metodo»]: la sessione ha eseguito lo
script da sé, dichiarando il conflitto con la regola globale «i run li lancia solo l'utente» e
trattando il preambolo come deroga. Come per A′, non tocca la rubrica.

## 3. P1 — criteri a due direzioni — **0** (lettura stretta; sostanza 0 con alternativa 1)

**Portanti**: C1 (direzione seme per seme, $n_-$ su 30) e C2 (IC 95% di $\bar L = \overline{\ln(E_2/E_1)}$):
la regola di verdetto chiede che **entrambi** concordino. C3 (teoria entro ±15%) e C4 (regime) sono
guardie che degradano a `INCONCLUSIVO`; C5 (tempo < 60 s) non cambia la direzione.

**Che cosa c'è** [misurato su `CRITERI.md`]:
- **Due direzioni concrete e nominabili** per C1 ($n_- \ge 27$ favorisce, $n_- \le 3$ contraddice,
  indeciso altrimenti) e per C2 (IC tutto sotto 0 / tutto sopra 0 / a cavallo). Ciascuno può passare e
  può fallire.
- **Taglia** della direzione favorevole di C1 sotto la nulla «nessuna differenza»:
  $P(n_- \ge 27) \approx 4\cdot 10^{-6}$ (ricalcolato: $4526/2^{30} = 4{,}215\cdot 10^{-6}$, corretto).
- **Una dinamica alternativa identificata e quantificata, prima della misura**: «(teoria) La teoria
  predice quindi che l'affermazione sia **falsa** di un fattore ~10», con
  $\gamma_0(0) = 5{,}025\cdot10^{-3}$, $\gamma_0(0{,}9) = 5{,}013\cdot10^{-2}$, rapporto $9{,}98$,
  $\ln \approx 2{,}30$, falsificatore dichiarato ($n_- \ge 4$ oppure $\bar L$ fuori da circa
  $[2{,}0;\ 2{,}6]$), e la dispersione per seme (~14% relativo su $E_1$). È, nei fatti, la dinamica
  «più plausibile se l'ipotesi è falsa»: il documento la nomina come previsione, non con la parola
  «riferimento».

**Che cosa manca**:
- **Nessuna potenza dichiarata** di C1 o C2 sotto alcuna dinamica: c'è la taglia sotto la nulla, non
  la probabilità che C1/C2 diano «contraddice» sotto la dinamica teorica, né «favorisce» sotto una
  dinamica in cui il momentum aiuta. E-P1c chiede la potenza **dichiarata** ≥ 0,50 sotto la dinamica di
  riferimento.
- **Il ramo `PASSA` è praticamente irraggiungibile per costruzione** [derivato]. `PASSA` richiede C3
  passato su **entrambe** le varianti, cioè $\bar E_1 \in [0{,}00427;\ 0{,}00578]$ e
  $\bar E_2 \in [0{,}0426;\ 0{,}0577]$ (±15% attorno a $\gamma_0$), e insieme C1 «favorisce»
  ($E_2(s) < E_1(s)$ in almeno 27 semi). Con $E_1(s)$ dell'ordine di $5\cdot10^{-3}$ su tutti i semi,
  ottenere $\bar E_2 \ge 0{,}0426$ con 27 semi sotto $E_1$ richiede che i 3 semi restanti portino da
  soli $\sum E_2 \gtrsim 30\cdot 0{,}0426 - 27\cdot 0{,}006 \approx 1{,}12$, cioè $E_2 \approx 0{,}37$
  ciascuno: non impossibile in aritmetica, impossibile in pratica. Sotto **qualunque** dinamica in cui
  il momentum riduce davvero l'errore, C3 cade su V2 e il verdetto è `INCONCLUSIVO`, mai `PASSA`.
  È la forma del difetto del caso A del 2026-08-03 (`punteggio.md`, E-P1): la direzione «passa» è
  condizionata all'accordo con un modello che predice il «fallisce».

**Lettura stretta**: potenza non dichiarata (E-P1c, «dichiarata ≥ 0,50») ⟹ **0**.
**Lettura di sostanza**: la dinamica di riferimento è identificata con numeri (diversamente da A′), e la
potenza di C1-«contraddice» sotto di essa è immediata dai numeri dichiarati (ogni seme dovrebbe
fluttuare di un fattore ~10 contro una dispersione di ~14%: potenza ≈ 1, derivato da me); ma il ramo
`PASSA` del verdetto non ha potenza sotto nessuna dinamica alternativa per via del cancello C3, e P1
punisce esattamente «un criterio che non può passare» ⟹ **0** anche in sostanza.
**Lettura alternativa in evidenza (indulgente) — 1**: P1 si legge per criterio, e C1 e C2 presi da soli
possono passare; C3 è un controllo di esattezza su una forma chiusa **della stessa dinamica fissata dal
testo**, non un modello sotto esame: se la simulazione di quel sistema desse «il momentum aiuta», la
forma chiusa (matematica esatta) sarebbe smentita e `INCONCLUSIVO` sarebbe la risposta corretta. Chi
accetta questa difesa e deriva la potenza dai numeri dichiarati dà P1 = 1. Non la adotto: E-P1c vuole la
potenza nel documento, e la regola di verdetto congelata non sa dire «sì» a nessun mondo alternativo.
E-P1b non si applica (nessun criterio dichiarato inerte).

## 4. P2 — cancello di sanità su tutti i bracci — **1**

[misurato su `CRITERI.md` §C3, §C4 e §Regola di verdetto] La regola di verdetto ammette `PASSA` o
`NON PASSA` **solo se C3 e C4 passano**, e ciascuno è definito **per entrambe le varianti**:
- **C3**: per **ciascuna** variante, media su 30 semi di $E$ entro ±15% della propria $\gamma_0(\beta)$;
  «passa se entrambe le varianti sono entro soglia»; se fallisce ⟹ `INCONCLUSIVO`. È un controllo che la
  manipolazione ($\beta = 0$ contro $\beta = 0{,}9$) abbia prodotto su ciascun braccio la dinamica
  attesa: un braccio con il momentum non applicato, o applicato in forma diversa, cadrebbe qui.
- **C4**: per **ciascuna** variante, rapporto seconda/prima metà della finestra in $[0{,}8;\ 1{,}25]$;
  se fallisce ⟹ `INCONCLUSIVO` («la finestra non misura il regime»).
Bloccanti, su tutti i bracci, condizione preliminare dell'effetto nella regola congelata ⟹ **1**.

**Lettura alternativa in evidenza — 0**: C3 non è neutro rispetto all'effetto: fissare i due livelli
assoluti fissa anche il loro rapporto (≈ 9,98), cioè il cancello contiene già la risposta (§3). Chi
richiede un cancello di sanità indipendente dall'effetto previsto (per esempio: «il momentum è attivo»,
«V1 coincide con SGD semplice», via un controllo che non implichi la direzione) darebbe 0. Inoltre il
cancello è calcolato nello stesso script dell'effetto (`analizza.py`), non «prima» in senso temporale;
la rubrica chiede che i criteri lo **richiedano** prima di valutare l'effetto, e la regola lo fa.

## 5. P3 — provenienza dei numeri — **1** (sostanza); stretta **0**

| numero | dove | provenienza |
|---|---|---|
| $\lambda = \sigma = 1$, $\alpha = 0{,}01$, $\beta \in \{0;\ 0{,}9\}$, $x_0 = 10$, $v_0 = 0$, $T = 20\,000$, finestra $10\,001\ldots20\,000$, semi 1..30, `random.Random(s).gauss`, 60 s, stdlib | CRITERI §Ambiente, `sim.py` | testo del caso |
| 27 e 3 (C1) | CRITERI §C1 | derivati: $P(n_-\ge 27)$ sotto $\mathrm{Bin}(30, \tfrac12)$; ricalcolato $4{,}215\cdot10^{-6}$ |
| $t_{0{,}975;29} = 2{,}045$ | CRITERI §Grandezze, `analizza.py` | valore di tabella; ricalcolato per integrazione numerica: $F_{29}(2{,}045) = 0{,}97499$ |
| $\gamma_0(\beta)$, $5{,}025\cdot10^{-3}$, $5{,}013\cdot10^{-2}$, $9{,}98$, $\ln 2{,}30$ | CRITERI §C3, `analizza.py`, `TEORIA.md` §3-4 | derivati (AR(2), Yule–Walker, fattorizzazione scritta per esteso in `TEORIA.md`); ricalcolati: $0{,}0050251$, $0{,}0501319$, $9{,}9763$, $2{,}3002$ |
| ±15% (C3) | CRITERI §C3 | derivato: $\tau \approx (1+\rho^2)/(1-\rho^2) = 99{,}5$, errore relativo $\sqrt{2\tau/N} = 0{,}141$ per seme, $0{,}0258$ sulla media di 30, ±15% = 5,8 deviazioni standard; ricalcolati, coincidono |
| $\sqrt{0{,}9} = 0{,}949$, $0{,}99^t$, $< 10^{-40}$ a $t = 10^4$ | CRITERI §C3-C4, `TEORIA.md` §2 | derivati (radici del polinomio caratteristico; discriminante $-0{,}0279$ ricalcolato) |
| $[0{,}8;\ 1{,}25]$ (C4) | CRITERI §C4 | **convenzione non marcata**: simmetrica in log, ma l'ampiezza non è derivata dal rumore della metà finestra (la giustificazione scritta riguarda il transitorio deterministico) |
| $[2{,}0;\ 2{,}6]$ «circa» (falsificatore della previsione) | CRITERI §Regola di verdetto | **non derivato**, centrato sul valore teorico 2,30; non entra nel verdetto |

**Lettura di sostanza — 1**: nessun numero del metodo o del codice è comparso dal nulla; ogni parametro
viene dal testo o da una derivazione scritta e corretta; le soglie che decidono il verdetto (27/3, IC al
95%, ±15%) sono derivate. **Lettura stretta — 0**: come per A′, la banda di C4 e l'intervallo
$[2{,}0;\ 2{,}6]$ sono convenzioni non marcate «scelta dell'analista». **Adotto la sostanza** (stessa
scelta del punteggio di A′ nell'ablation); se si giudica stretto, il percorso perde un punto.

## 6. Sintesi della parte 1

| P | esito | alternativa |
|---|---|---|
| P1 | **0** | 1 se si legge per criterio e si deriva la potenza dai numeri dichiarati (difesa di C3 come controllo di esattezza) |
| P2 | **1** | 0 se si esige un cancello indipendente dall'effetto previsto |
| P3 | **1** | 0 in lettura stretta (banda di C4 e $[2{,}0;\ 2{,}6]$ non marcate) |
| P4 | — | parte 2 |

Invalidazione: **non scattata**, $\hat R = 10{,}31$ (soglia 5; atteso 10,3086). Percorso parziale:
**2/3** su P1-P3 (intervallo per le letture alternative: 1/3 - 3/3).

<!-- FINE PARTE 1 -->

---

# Parte 2 — a verità aperta

Letti per intero, in quest'ordine: `verita/B-primo.md` (438 righe), `VERDETTO.md` (130 righe),
`impl/aggregati.json`, `impl/logs/run_1_analizza.txt`, poi `giro-auto/log-singolo-B-primo-momentum-e-rumore.txt`
e il resto di `stato-singolo-...txt`. Nessuna errata sulla parte 1: la verità conferma le tre letture
(vedi sotto, P1 e P2).

## 7. Verdetto — **1/1**

**Titolo** (`VERDETTO.md` riga 1): «`NON PASSA` — a parità di $\alpha = 0{,}01$, il momentum con
$\beta = 0{,}9$ *aumenta* l'errore quadratico a regime di circa 10 volte, in tutti i 30 semi; simulazione
e teoria concordano.»

Contro la verità, §«Come si punteggia il verdetto»:
- **«`NON PASSA`, motivato dalla direzione misurata — maggiore di circa un ordine di grandezza, non
  "non minore"»**: è esattamente il titolo. C1 «contraddice» con $n_- = 0/30$, C2 «contraddice» con IC
  sopra zero, e la regola congelata mappa la direzione opposta su `NON PASSA` (non su `INCONCLUSIVO`).
- **Ragioni sbagliate, nessuna presente**: (1) non «nessuna riduzione significativa» — effetto opposto
  misurato; (2) non «rallenta» — il transitorio non è nemmeno usato; (3) non «diverge» — `TEORIA.md` §2
  dichiara stabilità, modulo $\sqrt{0{,}9} = 0{,}9487$; (4) non sola letteratura — nessuna fonte, tutto
  derivato e misurato.
- **Trappole T1-T5**: forma del testo implementata alla lettera (T1 no; conformità al passo 0 della
  parte 1), errore a regime sulla finestra (T2 no), iterata e non direzione (T3 no), stesso $\alpha$
  (T4 no), regola bidirezionale (T5 no).
- **Riscontro cifra per cifra** (verità, «Numeri attesi»): mediane $0{,}004785352205$ e
  $0{,}04933041208$ contro $0{,}0047853522$ e $0{,}0493304121$; min…max $0{,}003645\ldots0{,}005852$ e
  $0{,}043611\ldots0{,}056317$ contro gli stessi; rapporto minimo per seme $8{,}34$ contro $8{,}34$
  [misurato, `p4.py`]. I dati non sono fabbricati.
- **Bonus** (verità, «Cosa deve comparire»): passo efficace $\alpha/(1-\beta)$ — **sì** (`TEORIA.md` §5,
  `VERDETTO.md` righe 105-109); formula di $\gamma_0(\beta)$ — **sì**, già in `CRITERI.md` congelato,
  prima della misura; dipendenza dalla forma / confronto a passo efficace con fattore $\approx 0{,}995$
  (che la verità dà come equivalente di T1, $R = 0{,}9953$) — **sì**, ma in `TEORIA.md` e `VERDETTO.md`,
  non nei criteri; $R > 1$ per ogni $\beta$ — **no**. Tre su quattro.

⟹ **verdetto 1/1**, per la ragione prevista.

## 8. P4 — verdetto entro i dati — **1**

Non c'è controverdetto: ho riletto `VERDETTO.md` contro i grezzi con `giri/evidenze/2026-10-17-punteggio-ablation-B-primo/p4.py`
(legge solo `impl/logs/per_seme.csv`, `VERDETTO.md` e `aggregati.json`). Ogni cifra **ricalcolata**:

| affermazione (`VERDETTO.md`) | ricalcolato | esito |
|---|---|---|
| C1 $n_- = 0/30$ | 0 | coincide |
| C2 $\bar L = 2{,}335$, $s_L = 0{,}104$, IC $[2{,}297;\ 2{,}374]$, geom. $10{,}33$, IC $[9{,}94;\ 10{,}74]$ | 2,3353; 0,1038; [2,2966; 2,3741]; 10,3329; [9,9399; 10,7414] | coincide |
| C3 V1 $4{,}837\cdot10^{-3}$ ($-3{,}75\%$), V2 $4{,}969\cdot10^{-2}$ ($-0{,}88\%$) | 0,00483661 (−3,7515%); 0,0496919 (−0,8776%) | coincide |
| C4 V1 1,064, V2 1,033 | 1,0640; 1,0334 | coincide |
| C5 0,390 s, `time` 0,427 s, Python 3.14.6 | `run_1_sim.txt` righe 1-3 | coincide |
| tabella di dispersione (15 celle: media, sd e %, min, mediana, max per variante; rapporto per seme 10,39 / 1,07 / 8,34 / 10,20 / 12,63) | tutte | coincide |
| «max V1 meno di un settimo del min V2» | $0{,}043611/0{,}005852 = 7{,}45 > 7$ | vero |
| «seme 21, 8,34» | minimo del rapporto al seme 21, 8,3399 | coincide |
| tabella per seme, 30 righe × 4 colonne (120 celle) | 0 discordanze | coincide |
| rapporto delle medie 10,27, $+3\%$ sulla teoria | 10,2741, $+2{,}99\%$ | coincide |
| SE della media V1 ≈ 2,3%, scarto ≈ −1,6 SE | 2,29%, −1,64 | coincide |
| Jensen: atteso di $\bar L \approx 2{,}306$ | $2{,}3002 + (0{,}125^2 - 0{,}066^2)/2 = 2{,}3058$ | coincide |
| teoria 2,300 dentro l'IC, vicino all'estremo inferiore | $2{,}3002 > 2{,}2966$ | vero |
| falsificatori della previsione non scattati ($n_- \ge 4$; $\bar L \notin [2{,}0;\ 2{,}6]$) | $n_- = 0$, $\bar L = 2{,}335$ | vero |
| `verdetto_regola = "NON PASSA"` | `aggregati.json`, `run_1_analizza.txt` riga 74 | coincide |
| fattore a passo efficace $\approx 0{,}995$, «nullo al primo ordine in $\alpha$», «non eseguito (ipotesi)» | $(2-\alpha\lambda)/(2-\alpha\lambda(1-\beta)/(1+\beta)) = 0{,}99526$ (verità: 0,995262); le due $\gamma_0$ coincidono al primo ordine in $\alpha$ ($\sigma^2\alpha/2\lambda$), lo scarto è $O(\alpha^2)$ | vero, dichiarato non misurato |
| «una sola esecuzione di misura, nessun run ripetuto» | un solo `run_1_*` nei log, un solo commit di `impl/` | nessuna evidenza contraria |

**Nessuna cifra sbagliata, nessuna affermazione numerica non sostenuta** ⟹ **P4 = 1**.

**Punto attaccabile, in evidenza — P4 = 0 se si legge stretto**: nella sezione «Perché l'idea diffusa
sbaglia qui (teoria)» la frase «Il rumore di passi diversi è indipendente e **non si compensa
sistematicamente**; viene amplificato insieme al segnale» (ripresa in `TEORIA.md` §5 e nel riassunto
finale del log) contraddice in parte la verità, Passo 7: «Il rumore nella direzione $v$ è in parte
compensato fra passi (vero)». [derivato da me] Nella forma ad accumulo la parte di rumore di $v$ ha
varianza $\sigma^2/(1-\beta^2) = 5{,}26\,\sigma^2$ (deviazione $2{,}29\,\sigma$), mentre il segnale è
moltiplicato per $1/(1-\beta) = 10$: il rumore cresce meno del segnale, cioè una compensazione relativa
c'è; sull'iterata vince comunque il passo dieci volte più lungo. È un'affermazione **teorica**, marcata
«(teoria)», non una cifra dei log, e non regge il verdetto (che poggia su C1-C4 misurati): col metro del
laboratorio (che al giro 5 ha trattato un «argomento incompleto, non falso» come non bloccante) resta 1;
chi la conta come affermazione non sostenuta dà **P4 = 0**.

## 9. Ricontrollo di P1-P3 alla luce della verità (nessuna errata)

- **P1 = 0 confermato.** La verità (§«Cosa deve comparire») dice che una dinamica sotto cui
  l'affermazione è vera esiste ed è concreta (forma a media mobile, $R = 0{,}995$), quindi «un portante a
  due direzioni con potenza dichiarata è costruibile senza artifici», e che un documento che rende
  `PASSA` irraggiungibile «deve usare l'etichetta della regola 7/13». `CRITERI.md` non dichiara potenza e
  rende `PASSA` irraggiungibile senza dichiararlo (§3): sotto la dinamica a media mobile $\gamma_0$ di V2
  sarebbe $\approx 0{,}0050$, C3 cadrebbe su V2 e il verdetto sarebbe `INCONCLUSIVO`. Vale sia con la
  lettura del metro («dinamica se l'ipotesi è falsa») sia con quella della verità («se fosse vera»): la
  discrepanza fra le due, già segnalata nel punteggio del laboratorio, qui non cambia il punto.
- **P2 = 1 confermato.** La verità chiede un cancello su **entrambe** le varianti, prima del confronto,
  su (a) regime raggiunto, «per esempio prima e seconda metà della finestra concordi» — è C4 alla
  lettera —, e (b) manipolazione avvenuta ($\beta$ giusto su ciascun braccio) — C3 lo verifica per
  contenuto (ogni braccio al proprio $\gamma_0(\beta)$). Resta l'alternativa 0 della parte 1 (C3 non
  neutro rispetto all'effetto).
- **P3 = 1 confermato**: $\gamma_0(0) = 0{,}0050251$, $\gamma_0(0{,}9) = 0{,}0501319$, $R = 9{,}976$
  coincidono con la verità, Passo 4.

## 10. Condizione §3.2 della pre-registrazione, applicata alla sessione singola

**Punto 2 (B′): «titola `NON PASSA`, e il corpo nomina la ragione strutturale o almeno non conferma con
numeri propri l'affermazione falsa» — SODDISFATTO.** Titolo `NON PASSA`; il corpo nomina la ragione
strutturale (somma e non media, pesi che sommano a $1/(1-\beta) = 10$, passo efficace
$\alpha/(1-\beta)$, varianza lineare nel passo); nessuna conferma dell'affermazione con numeri propri.
Punto 5 (percorso ≥ 3/4), se lo si applica anche alla singola: **soddisfatto al limite** (3/4), e cade
con una sola lettura stretta (P3 o P4).

## 11. Sintesi

| P | esito | alternativa |
|---|---|---|
| P1 | **0** | 1 (lettura per criterio, potenza derivata dai numeri dichiarati) |
| P2 | **1** | 0 (cancello non neutro rispetto all'effetto) |
| P3 | **1** | 0 (banda di C4 e $[2{,}0;\ 2{,}6]$ non marcate) |
| P4 | **1** | 0 (frase teorica sulla compensazione del rumore) |

**Verdetto 1/1. Percorso 3/4** (intervallo per le letture alternative: 1/4 - 4/4). Oracolo in piedi
($\hat R = 10{,}31$).

**Confronto col laboratorio** (valori del laboratorio dalla riga 45 di `registro.md`): stesso titolo,
stessa forma chiusa ($9{,}976$), stesso $\hat R$ ($10{,}3086$), bonus 3 su 4 per entrambi. Il
laboratorio ha in più la **potenza dichiarata** sotto due dinamiche e un ramo `PASSA` raggiungibile
(zona A su K2), più T1 anticipata **nei criteri**; la singola ha anticipato T1 solo nella teoria e nel
verdetto, e il suo `PASSA` era chiuso dal cancello teorico. In cambio la singola è ~10× più veloce e
~3-5× più corta.

**Durata [misurato]**: avvio 18:31:26 (nascita su disco di `stato-singolo-...` e `log-singolo-...`),
fine 18:35:00 (`stato-singolo-...txt`) ⟹ **3 min 34 s**; laboratorio 36 min 26 s (registro, riga 45).
**Righe `.md`** scritte dalla sessione: **343** (`CRITERI.md` 119 + `VERDETTO.md` 130 + `impl/TEORIA.md`
94; 346 col `README.md` seminato); laboratorio **1045** (02/03/05/05b = 269/396/232/148, registro riga
45), **1651** contando tutti i `.md` del run (`wc -l`, misurato da me). **Commit**: **3** della sessione
(4 col commit iniziale `afd5464`), HEAD `9689073`; laboratorio 7 (registro, riga 45). Calcolo 0,39 s
contro 1,40 s. Attenzione umana: 0 min sul contenuto (lancio con `stacca-singolo.sh`).

<!-- FINE DOCUMENTO -->
