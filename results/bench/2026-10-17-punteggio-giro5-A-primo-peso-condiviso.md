# Punteggio del giro 5 — caso A′ (il peso condiviso)

Run punteggiato: `<workspace>/laboratorio-giro5-A1/run/20261017-td-vs-mc-aggregazione` (repo seminato in
`43cf404`, chiusura in `1c8948f`). Regole di accettazione: `giri/2026-10-17-preregistrazione-giro5.md`
§3. Metro: `punteggio.md` con E-P1, E-P1b, E-P1c (dal giro 5: un documento che non identifica la
dinamica di riferimento vale P1 = 0). Mandato: `giri/MANDATO-PUNTEGGIO-GIRO5.md`.

## Chi punteggia, e che cosa sapeva prima di aprire il verdetto

Subagent fresco della sessione autonoma, 2026-10-17, contesto isolato. Non ha coordinato né sorvegliato
il run, non ha aperto la nota di progetto nelle <note dell'autore> né le verità degli altri casi del giro
(`verita/B-primo.md`, `verita/D.md`, `verita/E-primo.md`). Di `verita/A-primo.md` ha letto **solo** la
sezione «Condizioni di invalidazione» (righe 244-280), trovata con `grep -n -i invalidaz`.

**Contaminazione da dichiarare, prima della parte 1.** Il mandato della sessione principale indicava
come file di stato `giro-auto/stato-A-primo-peso-condiviso.txt` e `log-A-primo-peso-condiviso.txt`.
Li ho letti per ricavare durata ed esito del sistema **prima** di committare questa parte, e contengono
il riassunto finale del coordinatore: **titolo `PASSA`**, controverdetto «`VERDETTO SOSTENUTO`, nessun
rilievo bloccante», e quattro punti aperti (contaminazione del critic, R6 applicato senza terzo giro,
«due buchi di specifica» in G-ANCH e G-ENV/`w0`, una frase del verdetto che «dice più di quanto il
codice faccia»). Non ho aperto `05_verdetto.md` né `05b_controverdetto.md`. Il controllo di
invalidazione (§1) e il ricalcolo dei pesi erano già eseguiti quando ho letto quei file; i giudizi di
P2 e P3 erano formati, quello di P1 era formato nella sostanza (punto attaccabile compreso). Non posso
dimostrarlo da fuori: lo scrivo perché chi legge pesi questa parte sapendolo. È lo stesso tipo di fuga
del giro 4 (titoli dei commit visibili), più larga: lì non trapelava l'etichetta, qui sì.

---

# Parte 1 — scritta a verdetto chiuso

## 1. Controllo di invalidazione — primo gesto, come impone <domanda aperta 1>

La verità definisce una grandezza sola, calcolata **dal banco** sui pesi finali con $\mu$ e $v_\pi$
**della verità**:

$$\tilde\rho = \mathrm{mediana}_{30\ \text{semi}}\ \frac{\mathrm{VE}(w^{TD}_{\text{finale}})}{\mathrm{VE}(w^{MC}_{\text{finale}})},$$

con banda valida $[5, 20]$: sotto 5 il run ha implementato un oggetto diverso dal testo, sopra 20 il
braccio TD è rotto o MC non usa il peso condiviso. In entrambi i casi il verdetto non si punteggia.

**Che cosa ho fatto, con codice mio** (`$TMPDIR/puntA/inval.py`, Python 3.10, sola stdlib):

1. Letti i pesi finali dalle righe `blocco = 20` (`episodi = 2000`) di `04_impl/logs/blocchi.csv`,
   bracci `MC` e `TD`, 30 semi. Il VE l'ho ricalcolato con la formula della verità, non letto dalla
   colonna `VE` del run.
2. **Replay indipendente dal livello inferiore.** Un episodio è determinato da `(ramo, L)` di
   `episodi.csv`: la sequenza degli stati è $I$, poi $L-2$ volte $S_k$, poi $U_k$, ricompensa $r_1 = 2$
   o $r_2 = 1$ solo sull'ultima transizione. Ho rigiocato i 2000 episodi di ogni seme con MC every-visit
   («coi pesi correnti», ritorni come somme all'indietro) e TD(0) online ($\hat v(T) = 0$),
   $\alpha = 0{,}02$, pesi iniziali 0, esattamente come in `00_problema.md`, e confrontato i pesi finali
   con `blocchi.csv`.

| grandezza | misurato | esito |
|---|---|---|
| $\tilde\rho$ (mediana su 30 semi) | **11,0048** | dentro $[5, 20]$ |
| $\min_s$ / $\max_s$ del rapporto | 8,9653 / 11,1351 | nessun seme fuori banda (0 su 30) |
| scarto massimo pesi replay − log, MC e TD (120 pesi) | **0** (uguaglianza esatta in float) | il log è l'uscita delle regole del testo |
| $\tilde\rho$ ricalcolato dai pesi del replay | 11,0048 | identico |
| scarto massimo VE della verità − colonna `VE` del run (1890 righe) | $2{,}2\cdot10^{-16}$ | il run usa $\mu$ e $v_\pi$ della verità |
| mediana $\mathrm{VE}_{TD}$ / mediana $\mathrm{VE}_{MC}$ finali | 0,230548 / 0,020964 | — |

**Esito: l'oracolo di A′ regge. Il caso punteggia sia il verdetto sia il percorso.** Il valore cade
vicino alla mediana della calibrazione dichiarata nella sezione letta (10,94), e il minimo per seme
(8,97) sta sopra il seme peggiore della calibrazione (8,28).

## 2. Controlli d'integrità del run

| controllo | comando / file | esito |
|---|---|---|
| criteri prima del codice | `git log --diff-filter=A … 03_criteri.md 04_impl` | `451a249` 13:35:49 (criteri) prima di `76fecec` 13:38:23 (impl) — **sì** |
| `03_criteri.md` in un solo commit | `git log -- 03_criteri.md` | solo `451a249` — **sì**, mai riscritto |
| log committati prima del controverdetto | `git log -- 04_impl/logs`, `-- 05b_controverdetto.md` | log in `76fecec` e `99ac42c` (13:43), controverdetto in `1c8948f` (13:49) — **sì** |
| riproducibilità (regola 9) | `git diff 76fecec 99ac42c -- 04_impl/logs` | cambia **un file** (`costanti.json`) e **una riga** (`tempo_s` 0,4295 → 0,4361); `blocchi.csv`, `episodi.csv`, `semi.csv` byte per byte uguali |
| nessuna cancellazione | `git log --diff-filter=D` | vuoto |
| trailer `Co-Authored-By` | `git log --format='%(trailers…)'` | un valore solo, `Claude Opus 5.5`, su 7 commit; il commit di semina `43cf404` (autore `banco`) non ne ha |
| terminatori | `tail` su ogni `.md` del run | presenti su 9 documenti su 9; manca solo su `04_impl/come_eseguire.md` (istruzioni dell'implementatore, non un documento della catena) |
| tetti (`CLAUDE.md` del lab, riga 225) | `wc -l` | `02_metodo.md` 258 ≤ 400; `03_criteri.md` 304 ≤ 500; `05_verdetto.md` 239 ≤ 300 — **tutti rispettati** |
| regola del cieco | `grep -r banco-laboratorio run/…` | vuoto (rc 1) |
| sistema sotto test | `giro-auto/sistema-A-primo-peso-condiviso-avvio.txt`, `-fine.txt` | `SISTEMA INVARIATO — 7 file coincidono con 2026-10-17-giro5` in entrambi |
| un modello, nessun rilancio | `stato-A-primo-peso-condiviso.txt`, `sorveglianza-diario.txt` | `claude-opus-5-5`, uscita 0, 0 rilanci |
| `git status` del repo del run | — | pulito (due cartelle `.claude/.cc-writes` dell'harness, non tracciate e non rilevanti) |

**Durata del run**: lancio 13:07:37 (mtime di `sistema-…-avvio.txt` e `console-…txt`), stato `FINITO`
13:50:05 → **42 min 28 s**, senza rilanci. Calcolo del banco: 0,44 s (`costanti.json`, `tempo_s`).

## 3. P1 — criteri a due direzioni — **PASSA** (punto attaccabile in evidenza)

**Le due direzioni ci sono, su ogni criterio e su ogni guardia.**

- **C1** (unico portante): passa con $k \ge 27$ semi su 30 con $R_s \ge 5$, fallisce con $k \le 15$,
  zona intermedia $16 \le k \le 26$ → `INCONCLUSIVO` (T4). La tabella «Direzione dei fallimenti»
  dichiara che C1 non può fallire verso ↑ e **dove** finisce quel caso (C2 ↑, titolo T2↑).
- **C2** (diagnostico che qualifica il titolo): passa con le 8 mediane dei pesi a $\le 0{,}05$ dal
  punto fisso e $\bar R \in [9{,}9;\ 12{,}1]$; fallisce ↑ o ↓ con precedenza congelata (R3 del critic).
  Sotto A1 ($\bar R \approx 1$) cade per costruzione.
- **Guardie**: ognuna ha un guasto nominato che la fa scattare e, cosa rara, un **braccio o una
  mutazione su cui deve scattare davvero** (G-CTRL): G-LEARN e G-CONV sul braccio K
  ($\alpha_K = 0{,}001$, l'orologio sbagliato di 20×), G-STREAM(f), G-REPLAY, G-INV sulle copie mutate
  M-STREAM, M-REPLAY, M-INV. Le «guardie che si aprono da sole» sono elencate e chiuse una per una
  (riga 195).

**La potenza è dichiarata sotto tre dinamiche, due diverse dal modello sotto esame** (`03_criteri.md`,
«Potenza del portante»): H (punto fisso di `02_metodo.md`), **A1** («TD = minimo di VE, l'intuizione
"tabellare" dell'enunciato»: $P(k \le 15) \approx 1$, $P(k \ge 27) = 0$) e A2 (famiglia a frazione
$\lambda$, soglia a $\lambda^* = 0{,}368$). La potenza contro A1 non usa il modello di rumore
dell'analista: usa solo $\mathrm{VE}(w) \ge 1/48$, che è aritmetica. Inerzie dichiarate: nessuna
(E-P1b non serve). La sezione «Esito pre-forzato?» risponde nelle due direzioni e, dopo R2, ammette che
`NON PASSA` è raggiungibile **solo se l'algebra è sbagliata**, e per questo assegna all'esito previsto
un titolo proprio (T1, «il run verifica l'algebra, non scopre un effetto nuovo»).

**Punto attaccabile: E-P1c, la dinamica di riferimento.** Dal giro 5 il metro chiede che il documento
congelato **identifichi** la dinamica «più plausibile qualora l'ipotesi sia falsa», e se non lo fa
P1 = 0; la pre-registrazione §3.2 punto 5 lo ripete. `03_criteri.md` e `02_metodo.md` **non usano mai**
le parole «riferimento», «più plausibile» o «dominante» (`grep -i` vuoto), e il `CLAUDE.md` del
laboratorio non lo chiede (regola 5: «il modello assunto e un'alternativa concreta che esclude»).

- **Lettura che adotto (passa).** Il documento identifica **un'alternativa sola**, al singolare,
  ancorata all'enunciato: A1 è l'unica riga etichettata «alternativa», è la premessa che l'utente
  stesso offre («in versione tabellare i due metodi convergono agli stessi valori»), ed è la dinamica
  con cui il documento traduce «l'affermazione è falsa» in «Come questo esperimento può fallire», punto 1
  («TD converge vicino al minimo di VE (A1) o oltre $\lambda^*$»). A2 non è una dinamica concorrente ma
  la parametrizzazione che localizza la soglia. Sotto A1 la potenza del portante è $\approx 1 \ge 0{,}50$.
  Il metro dice che la dinamica di riferimento non la sceglie chi punteggia ma «la legge nel documento»:
  qui la si legge, anche se senza l'etichetta.
- **Lettura stretta (non passa).** Il metro è nato per chiudere la «via della reticenza», e un documento
  che elenca tre dinamiche senza dire quale è la più plausibile sotto ipotesi falsa non ha
  **identificato** nulla per iscritto. Con questa lettura **P1 = 0 e il percorso scende di 1**, e la
  condizione 5 della §3.2 cade su A′ se il percorso finale risulta 3/4.
- **Perché non è un dettaglio.** Il requisito è stato introdotto nel metro il 2026-08-18 ma **non**
  nelle regole del laboratorio (FIX 16 è dello stesso giorno e non lo contiene): il sistema sotto test
  non sapeva di doverlo fare. È un conflitto fra metro e sistema, della stessa forma di <domanda aperta 5> al
  giro 4, e va deciso da chi possiede il metro, non da chi punteggia. Proposta: voce in `<open-questions file>`.

**Se si giudica indulgente, il percorso è più basso di 1.**

## 4. P2 — cancello di sanità — **PASSA**

Il metro chiede che i criteri congelati esigano che la manipolazione abbia funzionato su **tutti** i
bracci **prima** di valutare qualunque effetto. Qui la «manipolazione» è il bersaglio
dell'aggiornamento (ritorno contro bootstrap), e il cancello deve dire: entrambi i bracci eseguono la
regola del testo, hanno imparato e sono in regime.

- **Fedeltà della manipolazione, su tutti i bracci, al passo 0**: G-REPLAY ricostruisce con codice del
  validatore i $1890 \times 4$ pesi da `episodi.csv` con le regole di `00_problema.md` su MC, TD **e K**;
  G-STREAM(f) lega il flusso al generatore congelato; G-INV lega MC e TD sulla coppia. Fallimento →
  `INCONCLUSIVO — banco non conforme`.
- **Apprendimento e regime, su MC e TD, al passo 2, prima del portante (passo 3)**: G-LEARN bilaterale
  sul **regime finale** (media dei blocchi 16-20, non il massimo storico: è la lezione del caso E
  applicata), G-CONV bilaterale, G-RES sulla risoluzione della metrica. Una sola che fallisca su MC
  **o** su TD → `INCONCLUSIVO`, e C1 non si legge. La matrice bracci × guardie (riga 178) è piena,
  le N/A sono motivate una per una.
- **Il cancello è stato provato capace di chiudersi** (G-CTRL, passo 1): su K, addestrato a metà per
  costruzione, G-LEARN deve scattare su ≥ 25 semi e G-CONV deve scattare; se non accade il titolo è
  `INCONCLUSIVO — guardia non vista scattare`. Le stime di K le ho ricalcolate (§5).

È la forma piena chiesta dal metro: guardie simmetriche, bloccanti, anteposte all'effetto, e
verificate su un braccio rotto apposta. Rispetto al giro 4 il difetto di allora (cancello sul massimo
storico, non bloccante sul braccio sperimentale) non c'è.

## 5. P3 — metodo fedele — **PASSA**

Ho ricalcolato ogni costante di `02_metodo.md` che entra in una soglia o in una previsione
(`$TMPDIR/puntA/p3.py` e `inval.py`; le costanti esatte le ha anche il banco del run in
`costanti.json`, che coincidono):

| numero in `02_metodo.md` / `03_criteri.md` | origine dichiarata | ricalcolato | esito |
|---|---|---|---|
| $v_\pi$, $\eta$, $\mu$, $w^*_{MC}$, $w^*_{TD}$, $1/48$, $11/48$, $119/48$ | derivazione esatta | identici in `costanti.json` (Fraction) e nel mio VE | coincide |
| rapporto al punto fisso $1 + 1/(1-p) = 11$; soglia 5 ↔ $p = 0{,}75$ | derivazione | $11/48 \,/\, 1/48 = 11$ | coincide |
| $\lambda^* = 1 - \sqrt{0{,}4} \approx 0{,}368$ | derivazione | 0,36754 | coincide |
| $0{,}98^{2000} \approx 3\cdot10^{-18}$ | conto | $2{,}83\cdot10^{-18}$ | coincide |
| residuo ODE di TD $\approx 1{,}4\cdot10^{-4}$ a $n=1000$, $\approx 6\cdot10^{-9}$ a 2000 | [stima], forma scritta | $1{,}36\cdot10^{-4}$, $6{,}18\cdot10^{-9}$ | coincide |
| $\sigma_U^2 = 0{,}0025253$ | AR(1), esatta | 0,00252525 | coincide |
| fattore della cascata 0,3322 | formula scritta | 0,33223 | coincide |
| mediana $\mathrm{VE}_{MC} \approx 0{,}021025$ | [stima] $\chi^2_1$ | 0,021025 | coincide |
| Hoeffding $\approx 3\cdot10^{-13}$ | bound scritto | $2{,}64\cdot10^{-13}$ (Hoeffding corretto: proxy $= \sigma_U^2$ per bersagli $\pm 0{,}5$) | coincide |
| $\mathrm{VE}_K \approx 1{,}52$ a $n=1300$, $\approx 1{,}15$ a 1800 | [stima] campo medio | 1,517 / 1,151 | coincide |
| G-STREAM (d) dev. std. 0,002; (e) 0,039 | conto | 0,00204 / 0,0387 | coincide |
| soglia G-LEARN $119/192 \approx 0{,}620$ | $0{,}25 \cdot \mathrm{VE}_0$ | 0,61979 | coincide |

Le soglie non ancorate a un conto sono marcate «scelta mia, nessuna fonte» una per una (27/30 e 15/30
di C1, 0,25 di G-LEARN, 0,02 di G-CONV, $10^{-9}$ di G-RES, $\pm 10\%$ e 0,05 di C2). Le fonti non lette
sono dichiarate tali (Bertsekas 1995: «abstract verificato via Crossref, full text non letto», «non ne
riprendo numeri»). I bound delle fonti sono dichiarati **non informativi** a $\gamma = 1$, e il valore 11
«derivato qui, non preso da una fonte». Le costanti congelate le produce il banco in `Fraction` dalla
tabella delle transizioni (regola 2), e il confronto con l'algebra è una guardia (G-ANCH).

**Rilievo fuori da P3** (P3 misura la provenienza, non la verità): il «massimo atteso su 30 semi
$\approx 0{,}0240$» di $\mathrm{VE}_{MC}$ non segue dalla forma $\chi^2_1$ che il documento stesso dichiara:
con quella forma il massimo atteso di 30 estrazioni è $\approx 0{,}0232$ ($\mathbb E[\max] \approx 5{,}6$ in
unità $\chi^2_1$ su 20 000 repliche); 0,0240 richiede $\approx 7{,}5$. Non entra in nessuna soglia. Per la
stessa ragione, «minimo su 30 di $R_s \approx 9{,}5$» è una stima: la misura dà 8,97 (§1), il critic su
300 semi disgiunti 9,23. Nessun criterio legge questi due numeri.

## 6. Parte 1 — riepilogo

| controllo | esito | in una riga |
|---|---|---|
| invalidazione (`verita/A-primo.md`) | **regge** | $\tilde\rho = 11{,}005$ in $[5, 20]$; replay indipendente esatto (scarto 0 su 120 pesi finali) |
| **P1** criteri a due direzioni | **PASSA** (attaccabile) | due direzioni e potenza sotto H, A1, A2 e K; **la dinamica di riferimento non è etichettata come tale**: con E-P1c alla lettera P1 = 0 |
| **P2** cancello di sanità | **PASSA** | replay, apprendimento sul regime finale e convergenza bloccanti su MC e TD prima del portante, visti scattare su K e su tre mutazioni |
| **P3** metodo fedele | **PASSA** | ogni costante ricalcolata coincide; scelte marcate; una stima non usata in soglie è fuori di un fattore ~1,5 nell'eccesso |
| **P4** verdetto entro i dati | *(parte 2)* | — |

**Percorso finora: 3 su 3 controlli chiusi** (2 su 3 con la lettura stretta di E-P1c).

<!-- FINE PARTE 1 -->

---

# Parte 2 — scritta dopo aver aperto la verità, `05_verdetto.md` e `05b_controverdetto.md`

La parte 1 è committata in `2df29a8` e **non è stata riscritta**. Ordine di lettura: `verita/A-primo.md`
per intero, poi `05_verdetto.md`, `05b_controverdetto.md`, `checkpoint_3_4.md`.

## 7. Che cosa il laboratorio ha titolato

> **`PASSA (previsto in forma chiusa) — su questo ambiente (p = 0,9, γ = 1, α = 0,02, 2000 episodi,
> 30 semi) la misura conferma il punto fisso TD derivato in 02_metodo: il run verifica l'algebra, non
> scopre un effetto nuovo`**

Titolo T1, al passo 3 della regola congelata, con C1 a $k = 30/30$ e C2 passato (8 sotto-clausole (a)
più la (b)). Nessuna guardia è scattata sui bracci portanti; su K e sulle tre mutazioni M sono
scattate tutte quelle che dovevano. Il limite di contaminazione sta alla riga 9, accanto al titolo; il
coordinatore lo porta **dentro** la riga nella sintesi di `checkpoint_3_4.md` (rilievo 3 del critic).

## 8. Verdetto — **1 su 1**

La verità (§«Come si punteggia il verdetto») conta come `PASSA` anche il titolo con l'etichetta
dell'esito previsto e col qualificatore di scope: è il caso di T1. Resta da stabilire che la ragione
sia quella della verità e non una delle cinque «ragioni sbagliate» che la verità elenca.

| la verità vuole | dove sta nel run | esito |
|---|---|---|
| affermazione vera per un motivo **strutturale**: punto d'arrivo di TD distorto, $\rho^* = 1 + 1/(1-p) = 11$ | `02_metodo.md` deriva $w^*_{TD} = (3/2)^4$, $\mathrm{VE}^*_{TD} = 11/48$, rapporto 11, forma generale $1 + 1/(1-p)$ **prima** della misura; il titolo dice «conferma il punto fisso TD» | **sì** |
| meccanismo: TD copia l'errore inevitabile di $w_U$ nelle sale, che pesano $10/12$ | `02_metodo.md` §«Perché TD sbaglia qui»; `checkpoint_3_4.md` «l'errore di aggregazione sulle uscite ($\mu = 1/12$) viene propagato per bootstrap agli stati $S$, che pesano $\mu = 10/12$» | **sì**, con le stesse parole |
| non per **lentezza** di TD | G-CONV su TD: mediana di $D = -2{,}53\cdot10^{-4}$ contro tolleranza $4{,}61\cdot10^{-3}$ (ricalcolato); C2(a) TD a ≤ 0,0055 dal punto fisso; «Cosa NON viene misurato» esclude la velocità | **sì** |
| non per **varianza** di TD | il verdetto scrive che la dispersione di $R_s$ è **dominata da MC** (seme 16, $w_U = 1{,}333$); $\mathrm{Var}(\log \mathrm{VE}_{MC}) / \mathrm{Var}(\log \mathrm{VE}_{TD}) \approx 11$ (ricalcolato: $1{,}72\cdot10^{-3}$ e $1{,}54\cdot10^{-4}$ con $n-1$) | **sì** |
| VE rispetto a $v_\pi$, non ai valori proiettati | VE con $\mu$ e $v_\pi$ del testo: scarto contro la formula della verità $\le 4{,}4\cdot10^{-16}$ su 1890 righe (parte 1 e ricalcolo qui) | **sì** |
| non dalla sola forma chiusa | 90 addestramenti simulati, replay indipendente esatto | **sì** |
| non con TD rotto | $\tilde\rho = 11{,}005$ in $[5, 20]$ (§1) | **sì** |
| trappole T1-T3 (RMS, $\mu$ per visite, pesi uniformi) | $\mu$ per **passi** ($\eta$ dall'equazione di flusso, $Z = 12$), VE senza radice | **evitate** |
| **T4** — il cancello che scambia l'effetto per un guasto | G-LEARN ha soglia **relativa all'inizio** ($0{,}25 \cdot \mathrm{VE}_0$) sul regime finale, G-CONV sulla stazionarietà; **nessun** cancello sul VE assoluto di TD né sulla distanza da $v_\pi$; la distanza dal **proprio** punto fisso è in C2, che qualifica e non blocca | **evitata**, ed è la trappola che la verità dichiara «la più importante del caso» |

**Bonus della verità** (non richiesto): preso in **cinque elementi su sei** — $\rho^* = 1 + 1/(1-p)$ e
indipendenza dalle ricompense; punto fisso MC come $\arg\min$ di VE; punto fisso TD come
$\Phi w = \Pi_\mu(r + P\Phi w)$; errore TD nullo sulla transizione «resto»; bound di Tsitsiklis-Van Roy
e S&B (9.14) dichiarato **vuoto** a $\gamma = 1$. Manca solo il rapporto RMS $\sqrt{11}$ e la ragione per cui
l'affermazione è su VE (`grep -i "rms\|radice"` su 01-05 vuoto). L'indipendenza dalla biforcazione $q$
non è scritta (il documento tiene $q = 1/2$ fisso).

**Nessuna nota da «verdetto giusto per la ragione sbagliata»**, e nessun punto attaccabile sul
verdetto (al giro 4, sul caso E, ce n'era uno: la riga del titolo contro la sintesi).

## 9. P4 — verdetto entro i dati — **PASSA** (punto attaccabile in evidenza)

Il controverdetto titola **`VERDETTO SOSTENUTO`**, 0 bloccanti, 4 lievi, 2 informativi. **Ogni cifra
che conferma o contesta l'ho ricalcolata dai grezzi** (`$TMPDIR/puntA/p4.py`, `tab.py`, codice mio,
Python 3.10 stdlib, sui file di `04_impl/logs/`):

| cifra del verdetto / controverdetto | ricalcolata da me | esito |
|---|---|---|
| C1: $k = 30$ | 30 | confermata |
| $R_s$: mediana 11,0048; IQR 0,2862 (10,8020–11,0881); min 8,9653 (seme 16); max 11,1351 (seme 9); media $10{,}8264 \pm 0{,}4774$ | identici, `quantiles(method='inclusive')`, `stdev` | confermate |
| $\mathrm{VE}_{MC}$: mediana 0,020964; IQR $2{,}38\cdot10^{-4}$; min 0,0208335; max 0,025469; media $0{,}021255 \pm 0{,}000944$ | identici | confermate |
| $\mathrm{VE}_{TD}$: mediana 0,23055; IQR $2{,}37\cdot10^{-3}$; min 0,21887 (seme 15); max 0,23248; media $0{,}22970 \pm 0{,}00281$ | identici | confermate |
| tabella dei 30 semi (8 colonne numeriche, 240 celle) | confronto automatico alla precisione stampata | **0 discrepanze** |
| regola 13: $\min R_s - 5 = 3{,}965$; $\max \mathrm{VE}_{MC} = 0{,}025469$ contro $\min \mathrm{VE}_{TD}/5 = 0{,}043775$, fattore 1,72 | 3,9653; 0,0254693; 0,0437747; 1,7187 | confermate |
| C2(a) mediane MC (1,491599; 2; 1; 1,491599), TD (1,503555; 1,505056; 1,505504; 1,491599) | identiche | confermate |
| C2(b) $\bar R = 10{,}80675$, scarto $-0{,}1933$ | 10,806745; $-0{,}19325$ | confermata |
| G-LEARN MC $[0{,}020973;\ 0{,}022445]$, TD $[0{,}22389;\ 0{,}23191]$, 0 scatti; K $[1{,}117;\ 1{,}194]$, 30/30 | identici | confermate |
| G-CONV MC $5{,}15\cdot10^{-5} \le 4{,}23\cdot10^{-4}$; TD $\lvert -2{,}53\cdot10^{-4}\rvert \le 4{,}61\cdot10^{-3}$; K 0,3643 contro 0,0231 | identici | confermate |
| G-RES: 30 valori distinti su MC, TD; IQR(VE_K) $1{,}82\cdot10^{-2}$ | 30 e 30; 0,01825 | confermate |
| G-INV scarto massimo 0 | 0,0 su 630 righe per coppia | confermata |
| G-VE(b): minimo VE su 1890 righe 0,0208333336 > 1/48 | 0,0208333336 | confermata |
| G-STREAM (d) 0,498483; (e) 11,9603; (f) 60 000/60 000; sha e `passi` 30/30; 30 sha distinti | 0,4984833; 11,9603; flusso rigenerato con `random.Random(s)` = file su 30/30 semi; (b) 30/30, (c) 30/30, 30 distinti | confermate |
| M-REPLAY (MC batch): scarto massimo $1{,}47\cdot10^{-3}$, primo su `w_S1`, seme 1, blocco 1 | $1{,}475\cdot10^{-3}$; primo: seme 1, blocco 1, `w_S1` | confermata |
| M-INV ($\hat v(T) = w_U$): primo scostamento 1,599 (seme 1, blocco 1), massimo 59,45 | 1,59906 (1, 1); 59,4487 | confermata |
| MC `w_S1`, `w_S2` esatti a meno di $10^{-14}$ | massimo $5{,}3\cdot10^{-15}$ | confermata |
| quattro $R_s$ più bassi: semi 16, 7, 10, 15 | 16, 7, 10, 15 | confermata |
| eccesso di $\mathrm{VE}_{MC}$ +2,03 %, di $\mathrm{VE}_{TD}$ +0,23 %; $11 \cdot 1{,}0023 / 1{,}0203 = 10{,}807$ | +2,025 %; +0,233 %; 10,8067 | confermata |
| dev. std. per seme di $w_U^{MC}$ 0,0488 contro 0,0503 teorica | 0,0488 ($n-1$); teorica 0,05025 | confermata |
| riproducibilità: `git diff 76fecec 99ac42c -- logs` = 1 file, 1 riga (`tempo_s`) | idem (parte 1, §2) | confermata |

Non ricalcolata: $P(\mathrm{IQR} \le 2{,}38\cdot10^{-4}) \approx 0{,}03$ (Monte Carlo del critic su un modello
gaussiano; informativo, nessun criterio lo legge) e i tempi di parete (non registrati nei log).

**Nessuna cifra del verdetto né del controverdetto è risultata sbagliata.** Il titolo dice **meno** del
corpo (regola 14 rispettata) e non contiene nulla che i log smentiscano: a differenza dei giri 1, 3 e
4, qui P4 non si gioca sul titolo.

**Punto attaccabile: la riga 55 del verdetto.** Scrive che il validatore ha «ricalcolato in `Fraction`
direttamente da `00_problema.md`» le costanti derivate. Ho aperto `05_misura_validatore/misura.py`
(righe 283 e 290): $v_\pi$ e $w^*_{TD}$ sono **letterali** scritti a mano, quindi per due delle otto
costanti il «ricalcolo» è un confronto fra due trascrizioni. È il rilievo 4 del critic, ed è vero.

- **Lettura che adotto (passa).** Il metro chiede che `05_verdetto.md` non affermi nulla che i **log
  grezzi** non sostengano. La riga 55 non afferma nulla sui dati: descrive la forza di una verifica,
  ed esagera; i valori che quella verifica conferma sono giusti (li ha ricalcolati il critic, e la mia
  formula di VE con $\mu$ e $v_\pi$ della verità coincide con la colonna `VE` del run a $4{,}4\cdot10^{-16}$).
  Il difetto è stato trovato dal critic, è passato nelle riserve del checkpoint 4 e nel riassunto del
  coordinatore: la catena l'ha intercettato, che è ciò che P4 esiste per verificare.
- **Lettura stretta (non passa).** «Non afferma **nulla**»: una frase del verdetto che descrive una
  verifica più forte di quella eseguita, smentita da un file del run, è un'affermazione non sostenuta,
  e il precedente del giro 3 («assolvere qui rifarebbe quell'errore») non ammette attenuanti di
  impatto. Con questa lettura **P4 = 0 e il percorso scende di 1**.

**Rilievo 1 del critic (le due letture di G-ENV/`w0` e G-ANCH che cambierebbero il titolo)**: non tocca
P4. Il verdetto **dichiara** entrambe le ambiguità e la lettura scelta con il perché («Ambiguità di
lettura incontrate»); manca solo la frase «la lettura opposta cambia il titolo», che il coordinatore
aggiunge. Ho verificato i fatti: `costanti.json` ha `"w0": [0.0, 0.0, 0.0, 0.0]`, e `banco.py` contiene
`"1/2"` solo nelle righe 27-28, cioè nella tabella delle transizioni. La lettura letterale di G-ANCH
non è soddisfacibile da nessuna implementazione: è un buco della specifica congelata (regola 16), non
un'affermazione del verdetto. Va nelle note del giro come lezione per FIX 17.

## 10. Punteggio del caso A′

| | valore | denominatore |
|---|---|---|
| **Verdetto** | **1** | **/1** |
| **Percorso** | **4** | **/4** (P1 ✓ · P2 ✓ · P3 ✓ · P4 ✓) |

**Punti attaccabili, con il punteggio alternativo:**
- **P1, E-P1c alla lettera** (la dinamica di riferimento non è **etichettata** come tale): percorso
  **3/4**. Nota: la verità, nella sezione «Cosa deve comparire nel percorso», indica come dinamica di
  riferimento tipica proprio «TD e MC convergono allo stesso punto, come nel tabellare» — cioè A1 del
  run. Il contenuto c'è; manca la parola.
- **P4, riga 55 alla lettera**: percorso **3/4**.
- **Entrambe le letture strette insieme**: percorso **2/4**.

**Profilo: «verdetto alto, percorso alto»**, come A e B al giro 2 (entrambi 4/4); primo `PASSA` dopo il
giro 2, su un sistema e un modello diversi.

## 11. Regola di accettazione §3.2 della pre-registrazione, sul caso A′

| condizione congelata | misurato | esito |
|---|---|---|
| §3.2 punto 1: A′ titola `PASSA`, e la ragione del titolo coincide con la derivazione della verità (non un `PASSA` per composizione fortunata) | `PASSA` T1; $\rho^* = 11$ e meccanismo del peso condiviso derivati prima della misura, coincidenti con la verità parola per parola; misura sul punto fisso (C2) e in regime (G-CONV) | **soddisfatta** |
| §3.2 punto 5: percorso ≥ 3/4 col metro attuale (E-P1b/E-P1c compresi) | 4/4; 3/4 con una sola lettura stretta; 2/4 solo con entrambe | **soddisfatta** (cade solo se si adottano insieme le due letture strette) |
| §3.1: controllo di invalidazione primo gesto, committato prima del verdetto | $\tilde\rho = 11{,}005$, regge; committato in `2df29a8` | **soddisfatta** |
| §3.3: sistema invariato all'avvio e alla fine; nessun riferimento al banco nel run | `SISTEMA INVARIATO` ×2; `grep` vuoto | **soddisfatta** |

**La parte di §3.2 che riguarda A′ è comprata.** La frase intera di §2 della rotta dipende da B′, E′ e D.

## 12. Note per il giro

- **Il cancello non ha scambiato la distorsione per un guasto.** Era il rischio dichiarato della
  riparazione del giro 4 (regola 17): un laboratorio addestrato a cercare bracci rotti poteva fermarsi
  davanti a un TD con VE 11 volte quello di MC. Non l'ha fatto, e per la ragione giusta: il cancello
  misura l'apprendimento rispetto all'inizio e il regime, non la qualità assoluta, ed è stato visto
  chiudersi su K (orologio sbagliato di 20×).
- **Contaminazione dichiarata dal critic stesso** (simulazione sui semi congelati al giro 1 di critica).
  Il coordinatore ha tenuto i semi con una motivazione corretta, e il limite viaggia nella riga del
  titolo del checkpoint 4. Lezione proposta dal run: vietare per iscritto al critic in modalità CRITERI
  le simulazioni sui semi congelati.
- **Due buchi di specifica nei criteri congelati** (G-ANCH letterale insoddisfacibile; G-ENV senza
  dire se il confronto è numerico o testuale) che, letti nell'altro verso, avrebbero dato
  `INCONCLUSIVO`. Il validatore ha scelto la lettura difendibile e l'ha scritto; ma un falso negativo
  sul caso A′ sarebbe potuto nascere da lì, non dalla matematica. Candidato per FIX 17.
- **Stima del metodo fuori di un fattore ~1,5** sul massimo atteso di $\mathrm{VE}_{MC}$ (parte 1, §5) e
  IQR di $\mathrm{VE}_{MC}$ misurato metà della stima (rilievo informativo del critic): nessun criterio
  li legge.
- **Durata e volume**: 42 min 28 s dal lancio a `FINITO`, 0 rilanci, 7 commit del run; righe:
  `02_metodo.md` 258, `03_criteri.md` 304, `05_verdetto.md` 239, `05b_controverdetto.md` 81
  (totale dei `.md` del run 1239). Calcolo del banco 0,44 s.
- **Attenzione umana**: 0 min sul contenuto; lancio dalla sessione/utente via `!` (chi abbia premuto il
  tasto non risulta dai file che ho letto); nessun controllo umano sul contenuto.
- **Attribuzione**: repo seminato `43cf404`, `CLAUDE.md` del repo del run sha256 `f50666f66633d9b9`
  (FIX 1-16 + ambiente, lab HEAD `8958eb7`), istantanea `2026-10-17-giro5`, modello `claude-opus-5-5`.

<!-- FINE DOCUMENTO -->
