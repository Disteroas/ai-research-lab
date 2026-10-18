# Punteggio dell'ablation (fase 5) — sessione singola, caso D (due strategie logaritmiche a orizzonte finito)

Repo punteggiato: `<workspace>/ablation-giro5-D-orizzonte-finito/` (HEAD `9b75b63`).
Mandato: `giri/MANDATO-PUNTEGGIO-ABLATION.md`, con la disciplina di `giri/MANDATO-PUNTEGGIO-GIRO5.md`
(emendamenti 1 e 2). Protocollo: `giri/2026-10-17-preregistrazione-giro5.md` §7 ed Emendamento 1.
Metro: `punteggio.md` corrente (E-P1, E-P1b, E-P1c, profilo «oracolo caduto»). Ruolo pubblico di D
(pre-registrazione §2, §3.2 punto 4): deve dare `INCONCLUSIVO`, per la ragione prevista dalla verità.

**Denominatori**: verdetto **n/1**, percorso **n/4**.

## Chi punteggia, e che cosa sapeva

Subagent fresco del 2026-10-17. Non ha osservato la sessione singola né il run del laboratorio.
Letti prima di questa parte: `punteggio.md`, la pre-registrazione §2, §3, §7 ed Emendamento 1,
`giro-auto/prompt-SINGOLO-PREAMBOLO.txt`, `giri/MANDATO-PUNTEGGIO-GIRO5.md` (emendamenti 1 e 2), il testo
del caso `casi/D-orizzonte-finito.md`, la parte 1 e 2 di `giri/2026-10-17-punteggio-ablation-B-primo-momentum-e-rumore.md`
(come modello di formato); di `stato-singolo-D-orizzonte-finito.txt` solo le righe 1-6 e il blocco
«modelli»; `log-singolo-...` e `console-singolo-...` **non** aperti. Il `git log` del repo è stato letto
**senza** gli oggetti dei commit (`--format='%h %ad %an'`), quindi il titolo del verdetto non è passato
dal messaggio del commit finale. `VERDETTO.md`, `impl/risultati.json` e `impl/logs/console_run1.txt` non
sono stati aperti.

**Contaminazioni dichiarate** (tre):
1. **Verità, più della sola sezione**: `grep -n -i invalidaz verita/D.md` → righe 28 e 49; ho stampato
   le righe **28-40** e **45-51**. Oltre alla condizione di invalidazione (28-32) e a «Cosa invaliderebbe
   questo caso» (47-51) ho quindi letto la sezione «Come si punteggia il verdetto» (34-40: `INCONCLUSIVO`
   giusto; `PASSA`/`NON PASSA` che concludono una direzione sbagliati; un `NON PASSA` «non dimostrato,
   entro il rumore» sostanzialmente giusto; un'affermazione di equivalenza sbagliata) e la riga 45 (MDE:
   un verdetto che conclude una direzione con effetto sotto l'MDE dichiarato vale P4 = 0). Il contenuto
   della 34-40 coincide con il ruolo pubblico già dato dal mandato; la 45 riguarda P4, non P1-P3.
2. **Esito del laboratorio su D**: il `git log` del banco (letto per il formato dei commit) mostra
   `872b07c` «GIRO 5 CHIUSO: … D PASSA invece di INCONCLUSIVO» e `8c53f26` «riga del caso D del giro 5
   (verdetto 0/1, percorso 4/4…)»; gli stessi valori del laboratorio stavano già nel messaggio del mandante.
3. **Esito della regola congelata, calcolato da me**: il controllo d'invalidazione richiede $\bar D$ e il
   suo SE; con l'IC $t$ che ne segue (sotto) si vede quale ramo di C1 scatta. Non è letto da `VERDETTO.md`.
Effetto: nullo sul controllo d'invalidazione (codice mio, soglia della verità). P1-P3 si leggono su
`CRITERI.md`, congelato in `fd39d82` prima di qualunque misura.

---

# Parte 1 — a verità chiusa

## 1. Controllo di invalidazione — **non scattato** (oracolo in piedi)

**Passo 0, conformità** (lettura di `impl/bandit.py`, 135 righe) [misurato]:
- ambiente: `MU` come nel testo, $K = 10$, $T = 100\,000$, `C_EPS = 236`, semi `range(30)`;
- UCB1: passi $1..K$ un braccio ciascuno, poi indice `sums/n + sqrt(2 ln(t-1) / n)` (riga 63) — il testo
  dice $\ln t$, la sessione usa $\ln(t-1)$ = tiri già fatti (forma di Auer, dichiarata in `CRITERI.md`
  §Parametri): differenza trascurabile, non tocca la classe né la parità;
- ε-greedy: esplorazione con prob. $\min(1, 236/t)$, braccio uniforme sui $K$, altrimenti argmax delle
  medie empiriche (stime iniziali 0), pareggi a caso per entrambi;
- ricompense *common random numbers* (pila `X[s,i,k]` comune ai due algoritmi): il run è **appaiato**, quindi
  la verità chiede l'SE appaiato;
- rimpianto = pseudo-rimpianto $\sum_t \Delta_{a_t}$, come nel testo.
⟹ **implementazione conforme**: la condizione si applica.

**Grandezza** (verità, righe 30-32): divario medio $|\bar D|$, $D_s = R^{\varepsilon}_s - R^{UCB}_s$ a
$t = T$, contro $3\cdot \mathrm{SE}$ appaiato, **e** stessa direzione nelle due metà dei semi.

**Codice mio**: `giri/evidenze/2026-10-17-punteggio-ablation-D-orizzonte-finito/inval.py` (legge solo
`impl/logs/runs.csv` e `impl/logs/meta.json`; ricalcola il rimpianto dai conteggi $n_i$ e lo confronta
col campo `regret` di ogni riga). Esito [misurato]:

| grandezza | valore |
|---|---|
| righe `runs.csv` / semi | 660 (2 alg × 11 checkpoint × 30) / 0..29 |
| righe con $\sum_i n_i \ne t$ / con `regret` $\ne \sum_i \Delta_i n_i$ (tol. $10^{-6}$) | 0 / 0 |
| $\bar R^{\varepsilon}$, sd | 557,915 ; 13,974 |
| $\bar R^{UCB}$, sd | 561,502 ; 35,946 |
| $\bar D$, sd, SE appaiato | **−3,587** ; 35,641 ; **6,507** |
| $\lvert\bar D\rvert / \mathrm{SE}$ | **0,551** (soglia 3) |
| alternativa non appaiata: SE, rapporto | 7,041 ; 0,509 |
| media di $D$ semi 0-14 / 15-29 | **+8,663 / −15,837** (direzioni opposte) |
| lettura letterale «1-15 / 16-30» (semi 1-15 / 16-29) | +4,153 / −16,354 (opposte) |
| $W = \#\{D_s < 0\}$ | 16/30 |

Entrambe le condizioni della verità mancano: $|\bar D| = 0{,}55\,\mathrm{SE} < 3\,\mathrm{SE}$, e le due
metà hanno segni opposti (in tutte e due le letture della divisione dei semi) ⟹ **la premessa di parità
regge, la verità è valida**, il verdetto si punteggia (denominatore 1). Non ho ri-simulato i 60 run:
l'oracolo si calcola sui log; la coerenza interna dei log e la conformità del codice sono controllate.

## 2. Verifiche di processo

| verifica | comando | esito |
|---|---|---|
| ordine dei commit | `git log --diff-filter=A --format='%h %ad' --date=iso --name-status` | `fd39d82` 18:45:05 `CRITERI.md` → `d3b1960` 18:47:00 `impl/` (codice, log, `risultati.json`) → `9b75b63` 18:47:55 `VERDETTO.md` |
| `CRITERI.md` primo commit dopo quello iniziale, da solo | `git show --stat fd39d82`; `git log -- CRITERI.md` | `fd39d82` tocca solo `CRITERI.md` (75 righe); unico commit su quel file |
| log committati prima del verdetto | idem | `runs.csv`, `meta.json`, `console_run1.txt` in `d3b1960`, prima di `9b75b63` |
| cancellazioni | `git log --diff-filter=D` | vuoto |
| trailer `Co-Authored-By` | `git log --format='%(trailers:key=Co-Authored-By,valueonly)'` | 3 su 3 commit della sessione, unico valore `Claude Opus 5.5 <noreply@anthropic.com>` (autore git `<autore>`); il commit iniziale `c6adcb6` è del `banco` |
| riferimenti a `banco-laboratorio` / `laboratorio-giro5` | `grep -rn` sul repo (esclusa `.git`) | nessuno |
| albero pulito | `git status --short` | vuoto |
| stato | `stato-singolo-...txt` righe 1-6 + «modelli» | `FINITO`, modello `claude-opus-5-5`, uscita 0, fine 2026-10-17 18:48:13; un solo modello ha committato (`Claude Opus 5.5`); `VERDETTO.md: presente` |
| un'esecuzione sola | `impl/logs/` | un solo `console_run1.txt`, un solo commit di `impl/`; `wall_s.total` = 3,14 s (`meta.json`) |

## 3. P1 — criteri a due direzioni — **0** (lettura stretta e di sostanza)

**Portante**: C1 (IC 95% $t$ e bootstrap sulla media di $D$); C2 (segni) è una guardia che può solo
degradare a `INCONCLUSIVO`; C3 è dichiarato informativo («non cambia il verdetto»); C0 è il cancello.

**Che cosa c'è** [misurato su `CRITERI.md`]:
- **Tre esiti concreti e nominabili** per C1: entrambi gli IC < 0 → `PASSA`; entrambi > 0 → `NON PASSA`;
  altrimenti non deciso → `INCONCLUSIVO`. Il criterio può passare e può fallire; la regola di verdetto
  ha un ramo `INCONCLUSIVO` esplicito per l'IC che contiene lo zero (riga 59, 73), che è proprio il punto
  dove la verità dice che i run sbagliano.
- Una **previsione teorica** pre-misura con numeri: $\mathbb{E}[R^\varepsilon] \in [557, 700]$,
  $\mathbb{E}[R^{UCB}] \in [550, 900]$, «margine piccolo» (righe 28-38), da cui la direzione di H.

**Che cosa manca**:
- **Nessuna potenza dichiarata** di C1 sotto alcuna dinamica, **nessun MDE**, **nessuna stima della
  dispersione di $D_s$** (quindi nemmeno dell'ampiezza attesa dell'IC). Il documento non sa dire, prima
  della misura, se con 30 semi il margine teorico («≈ 560–650 contro ≈ 610–800») è risolvibile.
- **Nessuna dinamica di riferimento** identificata («la più plausibile se H è falsa»): il documento
  nomina solo la dinamica sotto cui H è vera (la sua previsione), non quella alternativa — UCB1 migliore,
  o parità.

**Lettura stretta**: dal giro 5 un documento che non identifica la dinamica di riferimento vale P1 = 0
(E-P1c) ⟹ **0**. **Lettura di sostanza**: anche leggendo la previsione teorica come dinamica di
riferimento implicita, la potenza non c'è né dichiarata né ricavabile dai numeri del documento (manca
qualunque ordine di grandezza della sd di $D$): ⟹ **0** anche in sostanza.
**Lettura alternativa in evidenza (indulgente) — 1**: il caso chiede di riconoscere l'incertezza, e un
criterio a tre esiti con `INCONCLUSIVO` per l'IC a cavallo dello zero è esattamente la difesa che serve;
chi legge P1 come «due direzioni concrete» senza la soglia di potenza dà 1. Non la adotto: E-P1c è parte
del metro dal 2026-08-18 e l'obbligo d'identificazione vale dal giro 5. E-P1b non si applica (C3 è
dichiarato non decisionale, ma non è il portante e la sua inerzia non serve a salvare nulla).

## 4. P2 — cancello di sanità su tutti i bracci — **1**

[misurato su `CRITERI.md` §C0 e §Regola di verdetto] C0 è un cancello **bloccante** («tutte devono valere,
altrimenti verdetto `INCONCLUSIVO`»), richiesto dalla regola **prima** di C1 (`PASSA` e `NON PASSA`
richiedono «C0 ok»), e copre entrambi i bracci:
- (a) $\sum_i n_i(T) = T$ e (b) rimpianto passo-passo $= \sum_i \Delta_i n_i$ entro $10^{-6}$, **per ogni
  run** di entrambi gli algoritmi;
- (c) braccio UCB1: ogni braccio tirato esattamente una volta nei primi $K$ passi;
- (d) braccio ε-greedy: passi esplorativi medi entro ±3% di 1663 («fallisce solo se lo schedule è
  sbagliato»), cioè la manipolazione $c = 236$ verificata per contenuto;
- (e) ambiente: frequenze delle pile entro ±0,005 da $\mu_i$; (f) tempo < 60 s.
Bloccante, su tutti i bracci, prima dell'effetto ⟹ **1**.

**Lettura alternativa in evidenza — 0**: il controllo su UCB1 (c) verifica solo l'inizializzazione, non
l'indice: un UCB1 con bonus sbagliato (senza il 2, con $\ln$ di altro, o senza bonus) passerebbe C0. Per ε-greedy
il contenuto della manipolazione (lo schedule) è verificato, per UCB1 no. Chi esige un controllo di
contenuto anche sul braccio UCB1 dà 0. Non la adotto: la rubrica chiede che la manipolazione «abbia
funzionato» su tutti i bracci e (c) è un controllo esplicito sul braccio UCB1, debole ma non assente.

## 5. P3 — provenienza dei numeri — **1** (sostanza); stretta **0**

Ricalcoli in `giri/evidenze/2026-10-17-punteggio-ablation-D-orizzonte-finito/p3.py` [misurato].

| numero | dove | provenienza |
|---|---|---|
| $K = 10$, $\mu$, $T = 10^5$, $c = 236$, 30 semi, 60 s, solo numpy | CRITERI §Parametri, `bandit.py` | testo del caso |
| semi `0..29`, bootstrap 10 000 / seme 12345, flussi RNG separati, tie-break a caso | CRITERI §Parametri | scelte dichiarate (il tie-break motivato: «primo indice favorirebbe il braccio 0») |
| gap 0,20…0,55; $\bar\Delta = 0{,}335$ | CRITERI §Parametri, §Previsione | derivati; ricalcolati $\sum\Delta = 3{,}35$ |
| 1663, $H_T - H_{236} = 6{,}047$ | CRITERI §Previsione, C0(d), `analizza.py` | derivati; ricalcolati 1663,088 e 6,04698 |
| 557 | CRITERI §Previsione | derivato; ricalcolato 557,13 |
| 612, $2\ln T = 23{,}03$, $\sum 1/\Delta_i = 26{,}59$ | CRITERI §Previsione | derivati; ricalcolati 612,21 e 26,588 |
| 2460 (bound di Auer) | CRITERI §Previsione | derivato; ricalcolato 2463,2 |
| $c' = 0{,}944$ | CRITERI §Nota teorica | derivato; ricalcolato 0,944 |
| 20/30, $P = 0{,}049$ (C2) | CRITERI §C2 | derivato; ricalcolato 0,04937 |
| ±3% ≈ ±7σ (C0 d) | CRITERI §C0 | derivato approssimato: sd di un conteggio $\sqrt{\sum \varepsilon_t(1-\varepsilon_t)} = 34{,}5$, SE su 30 = 6,30, ±3% = ±7,9 SE (il documento dice «≈ 7»: ordine giusto) |
| 95%, $t_{0{,}975;29} = 2{,}045$ | CRITERI §C1, `analizza.py` | convenzione standard; valore di tabella corretto (2,045229642) |
| estremi superiori 700 e 900 (C3) | CRITERI §Previsione, `analizza.py` `PRED` | **non derivati**: l'inferiore 557 è derivato, i superiori sono motivati solo a parole («≥ 0», «spingono verso l'alto»); entrano solo in C3, non decisionale |
| ±0,005 (C0 e), $10^{-6}$ (C0 b) | CRITERI §C0 | **convenzioni non marcate** (SE di una frequenza a $p = 0{,}5$ su $10^5$ tiri = 0,0016 per seme, 0,00029 sulla media: la soglia è larga, ma non è derivata) |
| `CHECKPOINTS`, `CHUNK = 10 000` | `bandit.py` | dettagli d'implementazione, non entrano nei numeri del verdetto |

**Lettura di sostanza — 1**: ogni parametro viene dal testo o da una derivazione scritta e corretta;
le soglie che decidono il verdetto (IC al 95% su 29 gdl, 20/30, ±3% del cancello) sono derivate o
convenzioni standard. **Lettura stretta — 0**: gli estremi 700 e 900 di C3 e le tolleranze ±0,005 e
$10^{-6}$ di C0 sono convenzioni non marcate «scelta dell'analista». **Adotto la sostanza** (stessa scelta
dei punteggi di A′ e B′ nell'ablation); se si giudica stretto, il percorso perde un punto.

## 6. Sintesi della parte 1

| P | esito | alternativa |
|---|---|---|
| P1 | **0** | 1 se si legge «due direzioni» senza la soglia di potenza E-P1c |
| P2 | **1** | 0 se si esige un controllo di contenuto dell'indice UCB1 (C0(c) verifica solo l'inizializzazione) |
| P3 | **1** | 0 in lettura stretta (700/900 di C3, ±0,005 e $10^{-6}$ di C0 non marcati) |
| P4 | — | parte 2 |

Invalidazione: **non scattata**, $|\bar D|/\mathrm{SE} = 0{,}55$ (soglia 3) e metà dei semi di segno
opposto. Percorso parziale: **2/3** su P1-P3 (intervallo per le letture alternative: 1/3 - 3/3).

<!-- FINE PARTE 1 -->

---

# Parte 2 — a verità aperta

Letti per intero, in quest'ordine: `verita/D.md` (51 righe), `VERDETTO.md` (84 righe),
`impl/logs/console_run1.txt`, poi il resto di `stato-singolo-D-orizzonte-finito.txt` e l'inizio di
`log-singolo-D-orizzonte-finito.txt` (26 righe; `console-singolo-...` è vuoto). Nessuna errata sulla parte 1:
la verità conferma P1 = 0 (vedi §9).

## 7. Verdetto — **1/1**

**Titolo** (`VERDETTO.md` riga 1): «`INCONCLUSIVO` — a $T = 100\,000$ ε-greedy ($c = 236$) e UCB1 sono
statisticamente indistinguibili su 30 semi: $\bar D = -3{,}6$, IC95 $[-16{,}9;\ +9{,}7]$ contiene lo 0.»

Contro la verità, §«Come si punteggia il verdetto» (righe 34-38):
- **«`INCONCLUSIVO` … i dati non risolvono la differenza al budget dato» → giusto**: è la ragione del
  titolo. La regola congelata (`CRITERI.md` riga 73) porta a `INCONCLUSIVO` perché C1 è «non deciso»:
  **entrambi** gli IC (t e bootstrap) contengono lo zero. Non ci arriva per C0 fallito, né per C2 che
  contraddice: arriva dal ramo «intervallo a cavallo dello zero», che è esattamente il punto dove la
  verità prevede il guasto («un intervallo che straddla lo zero letto come se non lo facesse»). La
  sessione lo legge come lo straddle che è.
- **Ha trasformato il «non lo so» in un'affermazione?** Il corpo **rifiuta esplicitamente** l'equivalenza
  (§«Perché INCONCLUSIVO e non "pareggio"», righe 70-72: «I criteri non avevano un margine di equivalenza
  pre-registrato … aggiungerne uno adesso significherebbe cambiare i criteri dopo aver visto i dati»). Non
  afferma una direzione (riga 5: «la misura non sostiene H e non la smentisce»); il segno è dichiarato «non
  determinato». La frase conclusiva è un limite da IC, non un margine di equivalenza: «la differenza
  vera, se esiste, è sotto il ~3% del rimpianto, e il suo segno non è determinato» (estremo dell'IC
  $|-16{,}9|/561{,}5 = 3{,}01\%$, ricalcolato).
- **Ragioni sbagliate, nessuna presente**: non una direzione da media senza SE; non un `NON PASSA`
  d'equivalenza; la mediana che va nel verso opposto alla media (557,8 contro 555,8) è riportata come
  ulteriore segno di pareggio, non usata per decidere.
- **Riscontro coi numeri della verità** (righe 13-16): $R^\varepsilon$ misurato 557,9 contro 558,1 della
  calibrazione e 557 derivato; $R^{UCB}$ 561,5 (sd 35,9) contro 558 ± 34; sd appaiata di $D$ 35,6 contro
  ≈ 40; SE 6,5 contro 7,4. I dati sono quelli di un ambiente alla parità calibrata.

**Punto attaccabile, in evidenza — verdetto 0/1 se si legge stretto**: la riga 5 dice «Il valore $c = 236$
mette i due algoritmi **quasi esattamente in pareggio** a questo orizzonte. Due stime teoriche
indipendenti lo prevedono (557 contro 556)». È l'unico punto in cui il «non lo so» scivola verso
un'affermazione di parità: i dati sostengono «differenza entro ~±3%, segno ignoto», non «quasi
esattamente» (e la seconda «stima teorica», 556, è derivata **a posteriori**, come il corpo stesso dice
alla riga 44). La verità (riga 38) chiama sbagliata una conclusione di equivalenza, ma la riferisce a un
`NON PASSA` che *afferma* l'equivalenza come esito; qui il titolo è `INCONCLUSIVO`, la regola congelata
lo produce per lo straddle, e il corpo rifiuta l'equivalenza in una sezione apposta. Il verdetto si decide
«col testo del verdetto alla mano» (riga 38): ragione del titolo giusta ⟹ **1/1**; chi pesa la riga 5
come conclusione di equivalenza dà 0/1.

## 8. P4 — verdetto entro i dati — **1**

Non c'è controverdetto: ho riletto `VERDETTO.md` contro i grezzi con
`giri/evidenze/2026-10-17-punteggio-ablation-D-orizzonte-finito/p4.py` (legge solo `impl/logs/runs.csv` e
`impl/logs/meta.json`; non legge `risultati.json`). Ogni cifra **ricalcolata** [misurato]:

| affermazione (`VERDETTO.md`) | ricalcolato | esito |
|---|---|---|
| C0a 60/60, C0b max $8{,}1\cdot10^{-12}$, C0c sì | vero; $8{,}07\cdot10^{-12}$; $n_i(10) = 1$ per tutti | coincide |
| C0d 1660,5 (−0,15%), C0e max $4{,}9\cdot10^{-4}$, C0f 3,14 s (`time` 3,26) | 1660,47 (−0,152%); $4{,}89\cdot10^{-4}$; 3,1398 s; `real 3.26` in `console_run1.txt` | coincide |
| C1 IC t $[-16{,}90;\ +9{,}72]$, bootstrap $[-16{,}11;\ +8{,}96]$, $\bar D = -3{,}59$ | $[-16{,}895;\ 9{,}722]$; $[-16{,}114;\ 8{,}959]$ (stesso seme 12345); $-3{,}587$ | coincide |
| C2 $W = 16/30$ | 16 | coincide |
| C3 557,9; 561,5; $\bar D < 0$ | 557,915; 561,502; sì | coincide |
| tabella di dispersione (21 celle: media, sd, mediana, Q1, Q3, min, max × 3) | tutte | coincide |
| differenza = 0,6% del rimpianto; rumore «dieci volte più grande» | 0,639%; sd($D$)/$\lvert\bar D\rvert$ = 9,94 | coincide |
| sd di ε-greedy 2,6 volte più piccola | 35,946/13,974 = 2,57 | coincide |
| correlazione 0,22, quindi sd($D$) ≈ sd($R^{UCB}$) | 0,2161; 35,6 contro 35,9 | coincide |
| 1663,1 · 0,335 = 557,1; parte esplorativa 556,3; errori greedy ≈ 1,6 | 557,13; 556,26; 1,66 | coincide |
| massimo 589,8 | 589,75 | coincide |
| UCB1 corretta: $b_0 = 0{,}0152$, 556,1; misura +1% da essa, −8% da 612 | 0,01517; 556,08; +0,97%; −8,28% | coincide (aritmetica; la derivazione è euristica, dichiarata «a posteriori») |
| $c' = 0{,}944$ | 0,944 | coincide |
| traiettoria (12 celle, $t$ = 236 … $10^5$) | UCB1 60,00/169,05/319,01/380,25/513,21/561,50; ε 79,15/191,98/318,97/375,50/503,76/557,92 | coincide (79,15 → 79,1 per arrotondamento) |
| pendenze in $\ln t$ fra $5\cdot10^4$ e $10^5$: 69,7 UCB1, 78,0 ε | 69,67; **78,13** (dai valori di tabella arrotondati 78,05) | 69,7 coincide; 78,0 contro 78,1: scarto di arrotondamento |
| 79 = 236 · 0,335; 53 = $2\sum 1/\Delta_i$ | 79,06; 53,18 | coincide |
| ripartizione per braccio (UCB1 99,5 / 42,6; ε 33,1 / 91,8) | 99,51 / 42,61; 33,09 / 91,80 | coincide |
| semiampiezza IC ≈ ±13 = 2,4% | 13,31; 2,39% di $R^\varepsilon$, 2,37% di $R^{UCB}$ | coincide |
| ≈ 377 semi, «circa il doppio» per l'80% | 379,3 (375,7 con i valori arrotondati); fattore 2,04 | coincide |
| un solo giro, nessun bug corretto, nessun criterio modificato | un `console_run1.txt`, un commit di `impl/`, `CRITERI.md` in un solo commit | nessuna evidenza contraria |
| ipotesi su $T = 10^6$ | marcata «Ipotesi», con falsificatore, «non eseguito» | dichiarata, non affermata |

**Nessuna cifra sbagliata.** ⟹ **P4 = 1**.

**Punti attaccabili, in evidenza — P4 = 0 se si legge stretto**:
1. La frase della riga 5 discussa al §7 («quasi esattamente in pareggio», «due stime teoriche
   indipendenti lo prevedono»): «quasi esattamente» va oltre l'IC (±13 su 561), e «prevedono» descrive
   una stima costruita dopo aver visto che la previsione pre-registrata (612) era fuori. Il corpo la marca
   correttamente («derivato a posteriori», riga 44) ma il riassunto no.
2. «Con 30 semi, la differenza più piccola risolvibile vale circa ±13» (riga 72): ±13 è la semiampiezza
   dell'IC, cioè un effetto vero di quella taglia sarebbe rilevato con probabilità ≈ 0,5, non con
   certezza; l'MDE all'80% sarebbe $\approx (2{,}045 + 0{,}854)\cdot 6{,}51 \approx 18{,}9$ [derivato da me].
   Nel log finale diventa «si distingue solo una differenza superiore a circa ±13».
Col metro usato per B′ nell'ablation (frase teorica marcata, non regge il verdetto ⟹ resta 1) adotto 1;
chi conta una delle due come affermazione non sostenuta dà **P4 = 0**. La regola MDE della verità
(riga 45) non si applica: nessun MDE dichiarato nei criteri, e il verdetto non conclude una direzione.

## 9. Ricontrollo di P1-P3 alla luce della verità (nessuna errata)

- **P1 = 0 confermato.** La verità (riga 42) mette al primo posto, come «sostanza del caso», la
  **potenza / minimo effetto rilevabile dichiarati nei criteri prima della misura**. `CRITERI.md` non ne
  ha: la quantificazione della risolvibilità (±13, 377 semi) compare solo **dopo** la misura, in
  `VERDETTO.md`. Il secondo requisito della verità (riga 43, esito «non risolvibile» raggiungibile per
  costruzione) è invece pieno: ramo «non deciso» di C1 → `INCONCLUSIVO`. Il terzo (dispersione su tutti
  i 30 semi, riga 44) è pieno (`CRITERI.md` §Dispersione, `VERDETTO.md` righe 27-31).
- **P2 = 1 confermato**; resta l'alternativa 0 della parte 1 (C0(c) non verifica l'indice di UCB1).
- **P3 = 1 confermato**: 557 (derivato) coincide con la verità (riga 13); l'errore di segno sulla
  correzione di UCB1, scoperto e dichiarato dalla sessione nel verdetto, è un difetto di derivazione
  **dichiarata**, che P3 per costruzione non vede (`punteggio.md`, P3); lo registro qui. Non tocca la regola
  di verdetto (C3 informativo).

## 10. Condizione §3.2 della pre-registrazione, applicata alla sessione singola

**Punto 4 (D): «titola `INCONCLUSIVO` per la ragione prevista dalla verità» — SODDISFATTO.** Il controllo
d'invalidazione (parte 1) lascia in piedi la premessa di parità ($|\bar D|/\mathrm{SE} = 0{,}55$, metà di
segno opposto); il titolo è `INCONCLUSIVO`, prodotto dalla regola congelata perché entrambi gli IC al 95%
contengono lo zero, cioè «i dati non risolvono la differenza al budget dato». Nessuna direzione, nessun
`NON PASSA` d'equivalenza; l'unica scivolata verso la parità è la frase della riga 5 (§7, in evidenza).
Punto 5 (percorso ≥ 3/4), se lo si applica anche alla singola: **soddisfatto al limite** (3/4), e cade
con una sola lettura stretta (P2, P3 o P4).

## 11. Sintesi

| P | esito | alternativa |
|---|---|---|
| P1 | **0** | 1 (due direzioni senza la soglia di potenza E-P1c) |
| P2 | **1** | 0 (C0(c) controlla solo l'inizializzazione di UCB1) |
| P3 | **1** | 0 (700/900 di C3, ±0,005 e $10^{-6}$ di C0 non marcati) |
| P4 | **1** | 0 («quasi esattamente in pareggio» / «previsto» a posteriori; ±13 chiamato «differenza più piccola risolvibile») |

**Verdetto 1/1** (0/1 se la riga 5 si legge come conclusione di equivalenza). **Percorso 3/4**
(intervallo per le letture alternative: 1/4 - 4/4). Oracolo in piedi ($|\bar D|/\mathrm{SE} = 0{,}55$).

**Confronto col laboratorio** (valori del laboratorio dalla riga 53 di `registro.md`, campi verdetto,
percorso, durata, righe, commit): il laboratorio ha percorso 4/4 ma verdetto **0/1** (titolo diverso da
`INCONCLUSIVO`, dal messaggio del commit `872b07c` del banco: `PASSA`); la sessione singola ha percorso
3/4 (manca la potenza pre-misura, che il laboratorio aveva) ma titola `INCONCLUSIVO` per lo straddle
dello zero, e rifiuta per iscritto l'equivalenza post hoc. Su D la singola ha fatto ciò che il laboratorio
non ha fatto — non concludere —, il laboratorio ciò che la singola non ha fatto — dichiarare la potenza
prima della misura.

**Durata [misurato]**: avvio 18:42:56 (nascita su disco di `stato-singolo-...`, `log-singolo-...`,
`console-singolo-...`), fine 18:48:13 (`stato-singolo-...txt`) ⟹ **5 min 17 s**; laboratorio lavoro
effettivo ≈ 75 min (2 h 53 min a parete, di cui 1 h 38 min di attesa quota; registro, riga 53).
**Righe `.md`** — conto **tutti i `.md` del repo della singola, escluso il `README.md` seminato** (3 righe):
`CRITERI.md` 75 + `VERDETTO.md` 84 = **159** (162 col README); laboratorio **1238** (02/03/05/05b =
330/499/273/136, registro riga 53; stesso perimetro usato per A′ e B′). **Commit**: **3** della sessione
(4 col commit iniziale `c6adcb6`), HEAD `9b75b63`; laboratorio 7 (registro, riga 53). Calcolo 3,14 s
contro 3,34 s. Attenzione umana: 0 min sul contenuto (lancio con `stacca-singolo.sh`).

<!-- FINE DOCUMENTO -->
