# Punteggio del giro 5 — caso D (due strategie logaritmiche a orizzonte finito)

Run punteggiato: `<workspace>/laboratorio-giro5-D/run/20261017-ucb1-vs-egreedy` (repo seminato
`f24f29e`, 7 commit del run da `0918403` a `70a07b1`). Mandato:
`giri/MANDATO-PUNTEGGIO-GIRO5.md` con l'Emendamento 1. Regole di accettazione:
`giri/2026-10-17-preregistrazione-giro5.md` §3 (per D: §3.2 punto 4). Metro: `punteggio.md` con
E-P1, E-P1b, E-P1c. Denominatori del caso: verdetto n/1, percorso n/4.

**Ruolo pubblico di D** (pre-registrazione §2): deve dare `INCONCLUSIVO`, **per la ragione prevista
dalla verità**. `verita/D.md` è l'unica verità del banco rimasta sigillata dal 2026-08-11: questa
sessione è la prima che la apre.

## Chi punteggia, e che cosa sapeva prima di aprire alcunché

Subagent fresco della sessione principale, 2026-10-17. Non ha coordinato il run, non ha osservato
il lancio né la sorveglianza, non ha aperto la nota di progetto nelle <note dell'autore> né le verità degli altri
casi (`verita/A-primo.md`, `B-primo.md`, `E-primo.md`).

**Contaminazioni, dichiarate tutte:**

1. **Il titolo del verdetto l'ho letto in `00_problema.md`, prima del commit di questa parte.** Il
   mandato elenca `00_problema.md` fra i file da leggere nel tempo 1; il coordinatore vi ha scritto,
   al CHECKPOINT 4, il titolo del verdetto e le tre riserve del controverdetto. Non era evitabile
   senza violare il mandato, e l'Emendamento 1 non lo copre (chiude `stato-`, `log-`, `console-`,
   non i file del run). Effetto su questa parte: **nessuno sui numeri**, tutti ricalcolati da me dai
   grezzi prima di guardare qualunque cifra del verdetto (§1, §2-bis). P1-P3 punteggiano
   `02`/`03`/`03b`, che sono congelati prima della misura. **Proposta per il mandato** (non applicata,
   non tocca a me): nel tempo 1 di `00_problema.md` si legge solo fino a «Registro dei checkpoint».
2. Il grep d'invalidazione su `verita/D.md` ha mostrato anche la riga 49 (fuori dalla sezione):
   «La condizione di invalidazione sopra (divario reale sopra il rumore): ricalibrare c e
   rilanciare». Non aggiunge nulla alla sezione 28-32.
3. `git log` del banco mostra il titolo del commit `ea21c87` (esito di E′, non di D) e `de5a165`
   (cronaca di quota e rilanci di D, nessun esito).
4. Di `giro-auto/stato-D-orizzonte-finito.txt` ho letto solo le righe 1-6 e le righe «modelli che
   hanno committato» / «sistema sotto test» (Emendamento 1). `log-` e `console-D-orizzonte-finito.txt`
   **non** aperti prima del commit di questa parte. `05_verdetto.md` e `05b_controverdetto.md` **non**
   aperti (ne ho visto solo il `wc -l` e il `grep -c` del terminatore).

---

# Parte 1 — scritta a verità chiusa

## 1. Controllo di invalidazione — primo gesto (<domanda aperta 1>)

Della verità ho letto solo la sezione 28-32 («Condizione di invalidazione (stile <domanda aperta 1>)»):

> Se il run misura un divario medio |UCB1 − ε-decrescente| **> 3 · SE** (errore standard dai suoi
> log, appaiato se il run è appaiato), **e** la direzione è la stessa su entrambe le metà dei semi
> (1–15 e 16–30), la premessa di parità è falsa, la verità è invalidata e il caso non punteggia il
> verdetto.

**Il run è appaiato** [misurato]: `rewards_sha256` coincide fra `ucb1` ed `egreedy` a parità di
seme su 30/30 righe di `per_seed.csv` (common random numbers, S10 di `02_metodo.md`). Quindi vale
l'SE appaiato.

**Misura, con codice mio** (`evidenze/2026-10-17-punteggio-D/invalidazione.py`): rimpianto per seme
ricalcolato da `actions.npz` come $\sum_t k_{a_t}/20$ con $k=20\,\Delta$ dai letterali del caso, poi
$D_s=R_U(s)-R_\varepsilon(s)$.

| grandezza | valore | fonte |
|---|---|---|
| scarto fra il mio $R(s)$ e `regret_T` di `per_seed.csv` | **0** su 60 righe | `actions.npz`, `per_seed.csv` |
| media $R_U$ · sd | 547,433 · 39,80 | idem |
| media $R_\varepsilon$ · sd | 555,685 · 12,74 | idem |
| $\bar D$ (UCB1 − ε) | **−8,252** | idem |
| SE appaiato $s_D/\sqrt{30}$ | **7,808** (soglia 3·SE = 23,42) | idem |
| $\lvert\bar D\rvert$/SE | **1,06** | idem |
| SE non appaiato (riscontro) | 7,630 ($\lvert\bar D\rvert$/SE = 1,08) | idem |
| $\bar D$ semi 0-14 (i «1-15») | **+8,84** | idem |
| $\bar D$ semi 15-29 (i «16-30») | **−25,34** | idem |
| segni $D_s>0$ / $<0$ | 14 / 16 | idem |

Prima condizione ($\lvert\bar D\rvert>3\,$SE): **falsa** (1,06 SE). Seconda (stessa direzione sulle
due metà): **falsa** (segni opposti). Basta una delle due per non invalidare.

**Esito: l'oracolo di D REGGE. Il caso punteggia sia il verdetto sia il percorso.** La premessa di
parità è sostenuta dai log: il divario misurato è dentro il rumore di 30 semi.

### 1.1 Replay indipendente dei 60 run (per non fidarmi di `actions.npz`)

Il controllo sopra legge `actions.npz`; se il banco avesse implementato altre strategie, la parità
misurata sarebbe di altri algoritmi. Ho scritto un replay mio
(`evidenze/2026-10-17-punteggio-D/replay.py`) **dalla specifica S1-S12 di `02_metodo.md` e dai
letterali del caso** ($K$, $\mu$, $T$, $c=236$), senza leggere `04_impl/banco.py`:

- azioni identiche ad `actions.npz`: **30/30 semi UCB1, 30/30 semi ε-greedy** (60 × 10⁵ giocate);
- `actions_sha256` 60/60, `rewards_sha256` 60/60, `egreedy_explore` identico;
- tempo del replay 3,3 s.

Conformità della specifica al caso [derivato]: UCB1 «forma standard» con `ln(t−1)` (giocate già
fatte, F1 Fig. 1 alla lettera) invece di `ln t` del testo del caso — differenza relativa
$\le10^{-4}$ dopo $t=10^4$, dichiarata in S2; ε-greedy con $\varepsilon_t=\min(1,236/t)$ alla lettera,
esplorazione uniforme sui 10 bracci (S6). **I log misurano le due strategie del caso.**

## 2. Controlli di processo e d'ambiente

| controllo | esito | prova |
|---|---|---|
| un solo run | **sì**: unica cartella `run/20261017-*` = `20261017-ucb1-vs-egreedy`; l'altra cartella, `run/20260802-generalizzazione-labirinti`, è l'esempio seminato (presente solo nel commit di semina `f24f29e`) | `ls run/`, `git log -- run/20260802-…` |
| criteri prima del codice | `03_criteri.md` aggiunto in `506f0db` 17:50:53; `04_impl` aggiunto in `e37ed82` 17:54:32 | `git log --diff-filter=A` |
| `03_criteri.md` in un solo commit | **sì** (`506f0db`) | `git log -- 03_criteri.md` |
| criteri scritti **dopo** la ripresa delle 17:12 | **sì**: commit 17:50:53; nascita su disco di `02_metodo.md` 17:44:33, `03b_critica.md` 17:40:37, `03_criteri.md` 17:50:01, `banco.py` 17:52:37. Della prima vita (15:19-15:34) restano solo `00_problema.md` (15:19:12) e le fonti (nate 15:20:17-15:21:20, commit `e762a52` 15:21:23) | `stat -f %SB`, `git log` |
| log committati prima del controverdetto | `e37ed82` (implementazione) e `c34b8b2` 18:02:28 (validazione), controverdetto `70a07b1` 18:10:49 | `git log` |
| regola 9 provata con git | `git diff e37ed82 c34b8b2 -- 04_impl/logs/`: 1 file (`run_info.json`), 2 righe (`wall_s`, `timestamp`) | `git diff --stat` |
| `git log --diff-filter=D` | **vuoto** | |
| trailer `Co-Authored-By` | **uno solo**, `Claude Opus 5.5`, su 7/7 commit del run; `stato-…txt` riga 7 concorda | `git log --format=%(trailers)` |
| terminatori `<!-- FINE DOCUMENTO -->` | presenti su `01`, `02`, `03`, `03b`, `05`, `05b`; assente su `00_problema.md` (non richiesto) | `grep -c` |
| tetti di righe (`CLAUDE.md` del lab, riga 225) | `02` = 330 ≤ 400 · `03` = 499 ≤ 500 · `05` = 273 ≤ 300 | `wc -l` |
| riferimenti a `banco-laboratorio` nel run | **nessuno** | `grep -r` |
| sistema sotto test | `sistema-D-orizzonte-finito-avvio.txt` e `-fine.txt`: **SISTEMA INVARIATO — 7 file coincidono con 2026-10-17-giro5**; CLI 2.1.291 = istantanea; `settings-model` utente `fable` → `opus` (informativo, come in E′); `stacca --model` = istantanea | file letti per intero |
| prompt | `prompt-D-orizzonte-finito.txt` sha256 `eb1c2f74165bffdb…` = pre-registrazione §2; `prompt-D-continua.txt` esiste ma è del 2026-08-17 (giro 4), non usato | `shasum`, `stat` |
| stato finale | `FINITO`, fine 18:11:06, modello `claude-opus-5-5`, uscita 0 | `stato-…txt` righe 1-6 |
| residuo non tracciato | `05_validazione/__pycache__/` (bytecode dell'esecuzione degli script del validatore) | `git status` |

### 2.1 Rilanci e durata

Dal diario della sorveglianza (`giro-auto/sorveglianza-diario.txt`, righe 40-57):

- 15:18:07 sorveglianza avviata; primo commit del run 15:19:12, fonti 15:21:23.
- 15:32:08 «fermo senza controverdetto, rilancio n. 1»; 15:34:16 «morto per limite di quota,
  riprovo fra 30 min».
- **Rilanci automatici n. 2-6** (16:04, 16:20, 16:36, 16:52, 17:08): tutti «rilancio FALLITO
  (pre-volo o altro)», durante il limite. Il diario finisce alle 17:08:50.
- **Rilancio a mano alle 17:12** dalla sessione principale, stesso prompt (dato del mandato; il
  diario non lo registra — da riscontrare nel tempo 2 su `log-D-…txt`). Il coordinatore ripreso ha
  ricominciato dall'analisi: primo commit nuovo `6cb891f` 17:50:53, ultimo `70a07b1` 18:10:49.
- **Totale: 6 rilanci automatici (1 partito e morto per quota, 5 falliti al pre-volo) + 1 manuale.**
- **Durata**: a parete 15:18 → 18:11:06 ≈ 2 h 53 min; **lavoro effettivo ≈ 75 min** (15:18 →
  15:34 ≈ 16 min, più 17:12 → 18:11:06 ≈ 59 min), al netto di 1 h 38 min di attesa quota.

### 2-bis. Applicazione mia della regola di composizione congelata, sui grezzi

Fatta qui perché servirà a P4 e alla domanda di §3.2 punto 4; è conto mio, non lettura del verdetto
(`evidenze/…/composizione.py`).

| passo | grandezza | misurato | esito |
|---|---|---|---|
| 0 | G1-G4 | G2 e G3 rifatti da me (§1, §1.1) | passano |
| 1 | G5: media `n_explore` · media $R_{\rm exp}$ | 1657,43 ∈ [1637,87; 1688,30] · 555,445 ∈ [547,55; 566,71] | passa |
| 1 | G6: inizializzazione · media $R_U\le2463{,}22$ | 30/30 semi `[0..9]` · 547,43 | passa |
| 1 | G7 `n_sub_last` ∈ [1; 500] | UCB1 min 5 max 77 · ε min 12 max 29 | passa su entrambe |
| 2 | G8 IQR | $R_U$ 41,98 · $R_\varepsilon$ 17,53 · $D$ 55,16 | passa |
| 3 | $\bar D$, $s_D$, $h$, IC | −8,252 · 42,767 · 15,969 · **[−24,22; 7,72]** | `F_eq` falso (h < δ = 27,857), `F_ris` falso (h ≥ δ/2) |
| 4 | leave-one-out $s^*$ | $s^*=1$ ($D_1=+92{,}75$), IC senza $s^*$ = **[−26,55; 3,08]** | dentro (−δ, δ) |
| 5 | regione | $0\in$ IC e IC ⊂ (−27,857; 27,857) | **Q** |

**La regola congelata, applicata alla lettera, dà Q** — `PASSA — risposta: equivalenti entro δ`.
Margine: Q regge per δ ≥ 24,22 sull'IC pieno e δ ≥ **26,55** col leave-one-out; δ congelata 27,857.
Diagnostici: C2a ρ = 0,985, C2b ρ = 0,963 (banda [0,85; 1,20]); C3 media $R_{\rm sfr}$ = 0,240
(max 3,2) ≤ 55,713; C4 = 0,000 ≤ 18,204. Test dei segni 14/16, p = 0,856.
corr($R_U$, $R_\varepsilon$) = −0,081 (S10 la ipotizzava ≥ 0: **falsificata in segno**, ma piccola).

## 3. P1 — criteri a due direzioni — **PASSA** (punto attaccabile: E-P1c alla lettera)

**Due direzioni, criterio per criterio** (`03_criteri.md`):

- **C1 (portante).** La domanda non ha ipotesi direzionale e il documento lo dichiara («Nessuna
  ipotesi titolata», riga congelata sugli stati): `NON PASSA` non è un esito di C1. Le sue direzioni
  sono le quattro regioni U, E, Q, N, esaustive e disgiunte (verificato dal critic, giro 2) e **tutte
  raggiungibili alla stesura** (§ Esito pre-forzato: Q solo se $s_D<74{,}60$, N solo se
  $s_D\ge37{,}30$), con verifica obbligatoria alla misura (`F_eq`, `F_ris`). Per ogni risposta
  esiste un esito nominabile che la esclude; «fallire» per C1 è N (`INCONCLUSIVO`), raggiungibile.
  Ricalcolato da me: 74,6016 e 37,3008. **Passa.**
- **C2** bilaterale, banda [0,85; 1,20], discrimina 2/Δ da 8/Δ (ρ ≈ 4) e da 1/(2Δ) (ρ ≈ 0,25).
- **C3** passa se ≤ 55,713, fallisce se sopra; ↓ impossibile e dichiarato; un seme da ≈1400-1700
  basta a farlo cadere.
- **C4** passa se ≤ 18,204, fallisce se sopra.
- C2-C4 sono diagnostici che non toccano lo stato: due direzioni ciascuno.

**Potenza sotto una dinamica diversa.** Tabella § Potenza di C1 (15 caselle, A con sd 43, sd 60, B
con sd 90) **riprodotta da me casella per casella** (`potenza.py`, approssimazione normale a sd
nota): es. A, |E[D]| = 30 → 0,96 / 0,01; B, |E[D]| = 30 → 0,41, |E[D]| = 50 → 0,84, P(Q) = 0,00
ovunque sotto B.

**E-P1c.** Il documento congelato non usa la parola «riferimento». Identifica però due dinamiche con
ruolo dichiarato: **A** «modello assunto» (02_metodo) e **B** «alternativa che il modello esclude»
(aggancio di ε-greedy, coda $x^{-2,47}$, F9). Se l'ipotesi che regge il disegno — la previsione
centrale del metodo, «la domanda sta esattamente dove le costanti si equivalgono» — è falsa, la
dinamica che il documento stesso nomina è B. Sotto B: P(Q falso) = **0,00** (l'equivalenza non può
passare a torto) e P(direzione giusta) = 0,41-0,84 su |E[D]| = 30-60 (≥ 0,50 da |E[D]| ≈ 33,6).
Lettura adottata: B è la dinamica di riferimento, e la potenza contro il titolo sbagliato (Q) è
1,00 ≥ 0,50 → **passa**.

**Punto attaccabile.** (a) Lettura stretta di E-P1c: «riferimento» non è nominato → **P1 = 0,
percorso −1**; è lo stesso conflitto già segnalato su A′, B′, E′, e va risolto nel metro, non qui.
(b) Se la potenza che conta sotto B è quella di **risolvere la direzione**, l'estremo inferiore
dichiarato (0,41 a |E[D]| = 30) sta sotto 0,50: anche così P1 = 0. Non l'adotto perché la domanda
di D non ha una direzione ipotizzata da confermare; ma lo scrivo.

**Rilievo per la parte 2 (non entra in P1).** Sotto A a $E[D]=0$ il documento prevede Q con
probabilità **0,87**, e lo dice: il portante è disegnato perché la parità vera esca come
`PASSA — equivalenti`, non come `INCONCLUSIVO`. Il critic (R3) ha scritto che «il confine Q/N
dipende da δ più che dai dati» e che δ = 5 % di `R_explore_th` è «scelta dell'analista, nessuna
fonte». È il punto in cui il caso D si decide, e lo deciderà la verità.

## 4. P2 — cancello di sanità — **PASSA, pieno**

La «manipulation» qui sono le due strategie stesse: la domanda è valida solo se il banco implementa
UCB1 ed ε-greedy come prescritti e se entrambe apprendono. I criteri congelati lo richiedono **su
entrambi i bracci, prima di qualunque effetto**:

- **Matrice strategie × guardie** (regola 1) con le due caselle vuote motivate e coperte: G5
  (ancora esatta) solo su ε-greedy perché UCB1 non ha un'aspettativa chiusa → controparte G6 + G3;
  G6 solo su UCB1 perché il Teorema 3 di F1 è vacuo per ε-greedy → controparte G5.
- **Passo 0** (G1-G4 su entrambe), **passo 1** (G5, G6, G7 su **entrambe**: «Nessuna strategia di
  questo protocollo è "diagnostica": una guardia fallita su una qualunque delle due ferma il
  confronto»), **passo 2** (G8): tutti **prima** del passo 3 che calcola l'IC di C1.
- **G7** (regola 17) guarda la finestra finale (giocate 90 001-100 000), ha entrambi i lati
  (≥ 1 tiro sub-ottimo: la strategia esplora ancora; ≤ 500: ha identificato il braccio 0), è
  sulle due strategie e ferma.
- **G3** replay dai letterali di `00_problema.md`, con il buco di R2 (pareggi a scarto 0) chiuso
  prima del congelamento.

Misurato (§2-bis): il cancello non scatta; G7 passa con margine (UCB1 5-77, ε 12-29 contro [1; 500]).
Nessun punto attaccabile che vedo: è il cancello che E′ non aveva.

## 5. P3 — metodo fedele — **PASSA** (punto attaccabile: «sd ≈ 10» senza derivazione)

Ricalcolate da me (`metodo.py`) tutte le costanti numeriche di `02_metodo.md`:

| grandezza | 02_metodo | ricalcolo |
|---|---|---|
| $S_\varepsilon$ · 236 + 236·(H_T−H_236) | 1663,0876 · 236 + 1427,09 | 1663,08764 · 236 + 1427,0876 |
| Var $N_{\rm exp}$ · sd | 1192,14 · 34,53 | 1192,144 · 34,527 |
| $\bar g$ · E[G²] · Var G | 0,335 · 0,13525 · 0,023025 | identici |
| E[$R_{\rm exp}$] · Var · sd | 557,1344 · 172,08 · 13,12 | 557,13436 · 172,081 · 13,118 |
| incremento 10⁴→10⁵ · $\bar g S_\varepsilon(10^4)$ | 182,039 · 375,1 | 182,0388 · 375,096 |
| $c_{F1}$ · $c/(5d^2)$ | 0,944 · 4,72 | 0,944 · 4,72 |
| 3° termine del Teor. 3 a $n$ = 237 · 10⁴ · 10⁵ | 214,7 · 36,6 · 12,35 | 214,68 · 36,63 · 12,354 |
| Lai-Robbins · × ln T | 10,817 · 124,5 | 10,8171 · 124,537 |
| `B_thm1` | 2463,22 | 2463,2185 |
| $b^*$, $n^{\rm fp}$, $R_{\rm fp}$ a 10⁵ | 0,0153126 · (496,7 … 72,1) · 555,608 | 0,01531264 · identici · 555,6084 |
| $b^*$, $R_{\rm fp}$ a 10⁴ · incremento | 0,04572 · 372,559 · 183,05 | 0,045717 · 372,5588 · 183,0496 |
| senza $b^*$ · rapporto | 612,21 · 1,10 | 612,212 · 1,1019 |
| convessità · sd($R_U$) delta | +17,1 · 39,4 | +17,143 · 39,386 |
| taratura F4 (N, b, senza b) | 368,7 · 0,0159 · 495 | 368,745 · 0,01588 · 495,17 |
| pendenze 53,18 · 79,06 · ≈79,5 | | 53,176 · 79,06 · 79,497 |
| $10\cdot0{,}9^{236}$ | 1,6·10⁻¹⁰ | 1,589·10⁻¹⁰ |
| sd medie a 23,6 campioni · P(braccio 1 in testa) | 0,082 · 0,10 · ≈0,06 | 0,0823 · 0,1008 · 0,0622 |
| esponente 23,6·kl(0,8‖0,6) · 236/e · 86,8^2,16 | 2,16 · 86,8 · 1,5·10⁴ | 2,1598 · 86,82 · 1,54·10⁴ |
| m(T) · p(10⁴) · integrale decade finale | 166,4 · 3,5·10⁻⁵ · 0,28 | 166,36 · 3,53·10⁻⁵ · 0,2834 |
| $e^{3/23,6}$ | 1,14 | 1,1356 |
| coda ε: 23,6·kl(0,6‖0,8) | 2,47 | 2,4697 |
| gap medio escludendo il braccio 0 (S6) | ≈ 0,372 | 0,3722 |

Provenienze non numeriche: F1 (Fig. 1, Fig. 3, Teor. 1 e 3, §4, c migliore 0,05-0,40, 100 run),
F4 (§5.1, Fig. 1, 50 000 run), F9 (code), tutte citate in `01_fonti.md`; seme 20261017 = data
d'apertura dichiarata; S1-S12 marcate [scelta] col motivo.

**Due numeri che non riproduco esattamente**, entrambi in passaggi marcati [ipotesi]:
1. «aggancio: $\hat\mu_0<\mu_1$, probabilità ≈ 0,0035 con 24 campioni». Normale: 0,0072; binomiale
   esatta $X\le14$ su Bin(24; 0,8): 0,0126; $X\le13$: 0,0038. È una derivazione dichiarata con una
   convenzione non scritta: per costruzione del metro **passa** P3 (il difetto, se c'è, va nelle note).
2. **«sd ≈ 10» dello sfruttamento di ε-greedy** (§ Dispersione per seme): marcato [ipotesi], **senza
   derivazione**. Entra in sd($R_\varepsilon$) ≈ 16 e quindi in $s_D$ ≈ 43 della colonna A di potenza.
   Attenuanti: è dentro una sezione titolata «stima di forma alternativa — il banco produrrà i
   valori veri», la decisione usa l'$h$ osservato, e la tabella copre già $s_D$ = 60 e l'intervallo
   R4.1 [23,4; 55,4]. **Se si giudica che un'ipotesi senza derivazione è «un numero dal nulla», P3 =
   0, percorso −1.** Non l'adotto: il valore non entra in nessuna soglia né nella decisione.

## 6. Sintesi della parte 1

- **Controllo di invalidazione: l'oracolo REGGE** ($\lvert\bar D\rvert$ = 1,06 SE appaiato, direzione
  opposta fra le due metà). Il verdetto si punteggia.
- **P1 passa** (attaccabile: E-P1c alla lettera, o potenza di direzione 0,41 sotto B → 0).
- **P2 passa, pieno.**
- **P3 passa** (attaccabile: «sd ≈ 10» senza derivazione → 0).
- Processo pulito: un run solo, criteri congelati dopo la ripresa e prima del codice, sistema
  invariato, un trailer, regola 9 provata con git, nessun riferimento al banco.
- **Fatto che decide la parte 2** (misurato da me, non letto): la regola congelata applicata ai
  grezzi dà **Q — `PASSA — risposta: equivalenti entro δ = 27,86`**, non N. Se la verità chiede
  `INCONCLUSIVO`, la domanda della parte 2 è se l'equivalenza entro un δ scelto senza fonte sia la
  ragione della verità detta con un altro nome, o un'altra via.

Script: `giri/evidenze/2026-10-17-punteggio-D/` (`invalidazione.py`, `replay.py`, `composizione.py`,
`metodo.py`, `potenza.py`), interprete `/Library/Frameworks/Python.framework/Versions/3.10/bin/python3 -I`.

<!-- FINE PARTE 1 -->

---

# Parte 2 — scritta a verità aperta

Letti dopo il commit `e0ec4ee` della parte 1: `verita/D.md` per intero, poi `05_verdetto.md`,
`05b_controverdetto.md`, `giro-auto/log-D-orizzonte-finito.txt` (riassunto finale del coordinatore)
e `console-D-orizzonte-finito.txt` (vuoto, 0 righe).

## 7. Che cosa chiede la verità

Riassunto per chi punteggia, senza ripeterne la calibrazione: il caso è costruito perché **concludere
sia l'errore**. `INCONCLUSIVO` (o l'equivalente nel vocabolario congelato del run, «i dati non
risolvono la differenza al budget dato») è giusto; concludere una direzione è sbagliato; e — clausola
esplicita — un esito che **affermi che le due strategie sono equivalenti** è «una conclusione (di
equivalenza) non sostenuta: sbagliato». Il guasto atteso «quasi certamente» era un intervallo che
straddla lo zero letto come se non lo facesse.

## 8. Verdetto — **0/1**

Titolo: **`PASSA — risposta: equivalenti entro δ = 27,86 (|E[R_U]−E[R_ε]| < δ, non «uguali») — …`**.
È la stringa che la regola congelata produce sui grezzi (ricalcolato da me nella parte 1, §2-bis,
prima di aprire il verdetto; il controverdetto concorda carattere per carattere). Non è
`INCONCLUSIVO` e afferma un'equivalenza: cade nella clausola di zero della verità. Il riassunto
consegnato dal coordinatore (`log-D-…txt`, prima riga) dice lo stesso: «le due strategie sono
equivalenti entro il margine di equivalenza δ congelato».

**Come ci è arrivato — non per la via che la verità prevedeva.** Il guasto atteso non c'è: l'IC
[−24,22; 7,72] straddla lo zero e **nessun documento lo legge come una direzione**; test dei segni
14/16 p = 0,86 riportato; dispersione su tutti i 30 semi. Il run sa che non sa *quale* delle due
paghi meno. Il guasto è un altro, ed è nel disegno congelato:

1. al CHECKPOINT 1 il coordinatore fissa tre risposte ammesse (D1 di `00_problema.md`), fra cui
   «non distinguibili», «esito legittimo, non un fallimento»;
2. l'analista dà alla risposta «non distinguibili» la forma di un **test di equivalenza con margine**
   δ = 5 % di `R_explore_th` = 27,857, «scelta dell'analista, nessuna fonte»;
3. il critic (giro 1, R1, bloccante) sposta Q da `NON PASSA` a **`PASSA`**: «D1 dice esplicitamente che
   "non distinguibili" non è un fallimento». La riga congelata sugli stati ne fa la regola;
4. i criteri dichiarano prima della misura che **a parità vera Q esce con probabilità 0,87**
   (tabella di potenza, colonna A, riprodotta da me). L'`INCONCLUSIVO` (N) restava raggiungibile, ma
   era l'esito di minoranza proprio nel caso che la verità aveva calibrato.

Quindi l'`INCONCLUSIVO` non manca per una lettura sbagliata dei dati: manca perché il laboratorio ha
**dato al «non lo so» il nome di una risposta** e l'ha titolata `PASSA`. A decidere fra Q e N è stato
un numero senza fonte: Q regge per δ ≥ **26,55** (estremo di IC₋₁, ricalcolato), con δ = 25 il titolo
sarebbe stato `INCONCLUSIVO — equivalenza sostenuta da un solo seme`, con δ = 20 `INCONCLUSIVO — né
direzione né equivalenza`. Il verdetto e il controverdetto lo scrivono entrambi, nel corpo.

**Punto attaccabile.** L'equivalenza qui **è** statisticamente sostenuta al margine dichiarato
(IC e IC₋₁ dentro ±δ, δ congelato prima della misura): la clausola della verità («conclusione di
equivalenza non sostenuta») presuppone un'equivalenza affermata senza margine, e non prevede un TOST
pre-registrato. In più D1 chiama la terza risposta «non distinguibili», che è vicino all'«equivalente
nel vocabolario del run» ammesso dalla verità. **Se si legge Q come quell'equivalente, il verdetto
vale 1/1.** Non l'adotto per tre ragioni: (a) il vocabolario congelato del run ha già il suo
equivalente di «non risolto», ed è N (`INCONCLUSIVO — né direzione né equivalenza risolte`), distinto
da Q; (b) il titolo di Q afferma una proprietà di $E[D]$ («|E[R_U]−E[R_ε]| < δ»), non l'impossibilità
di distinguerle, e il coordinatore la consegna come «equivalenti»; (c) la frase la compra solo un δ
che nessuna fonte giustifica e che il critic stesso dichiarava decidere il titolo «più dei dati».

**Rilievo sulla verità** (non cambia il punteggio, va nel disegno dei casi futuri): la verità di D è
scritta per un laboratorio che sbaglia la direzione; il laboratorio del giro 5 ha un esito di
equivalenza con margine, e la verità lo giudica solo attraverso una clausola pensata per `NON PASSA`.
Una verità che attende `INCONCLUSIVO` dovrebbe dire esplicitamente come tratta un'equivalenza con
margine pre-registrato (TOST): ammessa solo se il margine ha una fonte esterna, o mai. Inoltre il
comando di calibrazione cita il percorso vecchio `<workspace>/banco-laboratorio/verita/…` (oggi
`<workspace>/banco-laboratorio/verita/D-calibrazione.py`, che esiste).

**Coerenza dell'oracolo con il run** [derivato, dai numeri della verità e dai miei]: UCB1 della
calibrazione 558 ± 34 (60 semi) contro 547,43 ± 39,80 (30 semi), scarto ≈ 1,3 SE; divario di
calibrazione +0,0 con SE 7,4 contro −8,25 con SE 7,81; parte esplorativa derivata 557 contro
$\overline{R_{\rm exp}}$ = 555,445 misurato. La premessa di parità regge anche contro l'appaiamento
del run, come la verità si proponeva («la parità deve reggere anche contro di lui»).

## 9. Su P1-P3 a verità aperta — nessuna errata

- **P1.** La verità chiede (§ «Cosa deve comparire nel percorso») potenza o MDE dichiarati prima
  della misura sotto una dinamica diversa: ci sono (MDE all'80 % ≈ 23 sotto A; B dichiarata); un
  criterio con l'esito «non risolvibile» raggiungibile per costruzione: c'è (N, raggiungibile per
  $s_D\ge37{,}30$; misurato $s_D$ = 42,77, quindi raggiungibile anche alla misura); dispersione su
  tutti i semi: c'è. P1 resta **passa**. Il fatto che a parità N fosse l'esito di minoranza (0,1-0,2
  contro 0,87 di Q) è un difetto del **verdetto** che il disegno produce, non della bidirezionalità.
- **P2, P3**: invariati.

## 10. P4 — verdetto entro i dati — **PASSA** (punto attaccabile: C4 «garantito dalla censura»)

Il controverdetto titola **«IL VERDETTO REGGE»**, 8 rilievi non bloccanti. Ricalcolato da me ogni
numero che conferma o contesta (`p4.py`, `p4_tabella.py`, `replay_cf.py`, `replay_ties.py`, più gli
script della parte 1):

| affermazione (verdetto / controverdetto) | ricalcolo mio dai grezzi | esito |
|---|---|---|
| tabella dei 30 run, 6 colonne numeriche | **0 discrepanze su 180 celle** (`n_sub_last` compresa) | confermata |
| $\bar D$ −8,2517 · $s_D$ 42,7668 · h 15,9694 · IC [−24,2211; 7,7177] | identici | confermata |
| $s^*$ = 1, IC₋₁ [−26,5519; 3,0829] | [−26,5519; 3,0829] | confermata |
| δ minimo per Q = 26,552; δ = 25 → INCONCLUSIVO; δ = 20 → N | 26,552; con δ = 25 IC pieno dentro (−24,22), IC₋₁ fuori → passo 5 riga «solo un seme»; con δ = 20 IC esce → N | confermata |
| margine sul bordo Q/N 3,64 ($\delta-h$ = 11,887) | 11,887 − 8,252 = 3,635 | confermata |
| statistiche per strategia (media, sd, mediana, IQR, min/max, semi) | identiche (547,433 · 39,802 · 540,75 · 41,975 · 488,50 s15 · 652,70 s1; 555,685 · 12,739 · 555,975 · 17,525 · 530,05 s4 · 577,75 s16) | confermata |
| `n_explore` 1657,43 · sd 34,37 · med 1664,5 · IQR 44 · 1581 (s4) · 1720 (s25); G5 −0,90 / −0,70 e.s. | identici; −0,897 / −0,705 | confermata |
| C2 ρ_T 0,9853 · ρ_tardo 0,9630; `ucb1_tardo` 176,28 · sd 23,91 · IQR 40,88 · 137,80 (s15) · 221,80 (s19) | identici | confermata |
| C3 0,24, 5 semi (1: 3,2 · 8: 0,2 · 15: 1,6 · 18: 1,0 · 20: 1,2); C4 0 su 30/30 | identici | confermata |
| convessità 573 contro 547,43 = 3,5 e.s.; punto fisso −1,12 e.s.; ε 555,69 ± 2,33, −0,6 e.s., sotto la banda di 1,3 | 3,52 · 1,12 · 2,326 · −0,62 · 1,315 | confermata |
| bound/media 4,50; $s_D$ atteso senza appaiamento 41,79; corr −0,081, e.s. ≈ 0,19 | 4,4996 · 41,791 · −0,0814 · 0,192 | confermata |
| code: max ε 577,75 contro media + 5 sd = 619,4; UCB1 s1 +2,6 sd | 619,38 · 2,64 | confermata |
| meccanismo di 02_metodo sommato: 0,10·2 + 0,0035·7 ≈ 0,22 | 0,2245 | confermata |
| **(contestata dal controverdetto)** C4 «garantito dalla censura»: passi greedy sub-ottimi 35 (16+1+8+4+6 nei semi 1, 8, 15, 18, 20), l'ultimo a t = 351 | **35, stessi semi e conteggi, ultimo t = 351** | **il controverdetto ha ragione**: lo 0 tardo è un'assenza osservata |
| UCB1: pareggi esatti al massimo 2786, discriminanti S8/`argmax` 1665, su 30/30 semi | 2786 · 1665 · 30 | confermata |
| ε-greedy: 2 pareggi nel ramo greedy, seme 8 t = 273 {0,1} non discriminante, seme 18 t = 300 {0,2} discriminante | identici | confermata |
| controfattuale `argmax` nudo: UCB1 87-120 azioni diverse sui semi 0-3, `regret_T` identico 30/30; ε-greedy solo seme 18, −0,25 | 111 · 87 · 115 · 120; $n_i$ identici 30/30, ΔR = 0; ε: 1 seme, −0,25 | confermata (S8 senza effetto sul rimpianto: la sua motivazione è smentita) |

**Nessuna cifra del verdetto è sbagliata.** Il titolo è la stringa congelata e il corpo non lo
contraddice; δ e la sua fragilità sono nel corpo (punto 1), con i due valori controfattuali.

**Punto attaccabile 1.** Il punto 2 di «Cosa ho osservato» afferma che C4 «regge» per **censura,
non per un test**: i grezzi mostrano sfruttamento vivo fino a t = 351 e un pavimento dal lato del
«regge», non una metrica bloccata; C4 poteva fallire (seme agganciato dopo 10⁴ che passa G7). È
un'affermazione del verdetto che i log non sostengono, fuori dal titolo e dichiarata «non cambia il
verdetto», corretta dal controverdetto. **Se si giudica che ogni frase del corpo conta, P4 = 0.**
**Punto attaccabile 2.** «previsioni: UCB1 regge, ε-greedy regge/regge» nella riga del titolo: vero
come esito di C2/C3/C4 e delle bande dichiarate (UCB1 [472; 667], ε $E[R_{\rm sfr}]$ in [0; 40]), ma le
due previsioni puntuali (573; 5-15) sono mancate e il corpo lo dice. Il controverdetto lo segnala
(L1). Al giro 4 una riga del titolo che i log svuotavano è costata P4; qui la riga non afferma nulla
di falso sulle grandezze che nomina. Non l'adotto; **in lettura stretta P4 = 0**.

## 11. Percorso — **4/4**

| P | esito | lettura stretta |
|---|---|---|
| P1 | passa | 0 (E-P1c alla lettera: «riferimento» non nominato; o potenza di direzione 0,41 sotto B) |
| P2 | passa, pieno | — |
| P3 | passa | 0 («sd ≈ 10» dello sfruttamento senza derivazione) |
| P4 | passa | 0 (C4 «garantito dalla censura» nel corpo; o «previsioni … regge» nel titolo) |

Una sola lettura stretta: 3/4. Tutte: 1/4. Profilo: **verdetto basso, percorso alto** — «il
laboratorio è rigoroso e sbaglia»; l'errore è localizzato (Q → `PASSA` con δ senza fonte, deciso al
CHECKPOINT 1 e al rilievo R1 del critic) e riparabile.

## 12. Regola di accettazione §3.2 della pre-registrazione, sul caso D

**Condizione §3.2 punto 4 — NON soddisfatta.** D **non** titola `INCONCLUSIVO`: titola `PASSA —
risposta: equivalenti entro δ`. Non è «verdetto giusto per la ragione sbagliata» (come al giro 3 su
C): è **etichetta sbagliata con la diagnosi quasi giusta nel corpo**. Il guasto previsto dalla
verità (IC che straddla lo zero letto come direzione) non si è verificato; il terzo stato era
raggiungibile ed è stato evitato da una regola congelata che chiama «risposta» la non distinguibilità,
con un margine senza fonte. Il terzo stato **resta mai verificato su un oracolo valido**: al giro 3
l'oracolo era morto, qui l'oracolo regge e il laboratorio non lo dice.

**Punto 5 (percorso ≥ 3/4) su D: soddisfatto** (4/4; 3/4 con E-P1c alla lettera).

La frase di §2 della rotta era già non comprata per E′ (bloccante assoluto); D aggiunge il punto 4.

## 13. Note per il registro

- **Rilanci**: 6 automatici della sorveglianza (n. 1 staccato 15:32:16 e morto per quota, rilevato
  15:34:16; n. 2-6 falliti al pre-volo durante il limite, 16:04-17:08) + **1 manuale** della sessione
  principale alle 17:12, stesso prompt: riscontrato da `sistema-D-orizzonte-finito-avvio.txt`
  modificato alle 17:12:00 e `console-…txt` alle 17:11:59 (il diario finisce alle 17:08:50). Il pre-volo
  della ripresa dice `SISTEMA INVARIATO`.
- **Un solo run**; criteri scritti dopo la ripresa (nascite su disco dalle 17:40:37, commit 17:50:53)
  e congelati prima di `04_impl/` (17:54:32).
- **Durata effettiva ≈ 75 min**: 15:18:01 → 15:34:16 (16 min 15 s) + 17:12:00 → 18:11:06 (59 min 06 s);
  a parete 2 h 53 min, di cui 1 h 38 min di attesa quota. Calcolo 3,34 s (`real`).
- **Righe** 02/03/05/05b = 330/499/273/136; tetti rispettati (03 a una riga dal tetto).
- **Momento interessante**: il laboratorio sapeva di non sapere — IC a cavallo dello zero, segni
  14/16, «la domanda sta esattamente dove le costanti si equivalgono» scritto **prima** della misura —
  ma il suo critic, per difendere il lettore da un `NON PASSA` fuorviante, aveva trasformato il «non lo
  so» in una risposta titolata `PASSA`; a decidere fra `PASSA` e `INCONCLUSIVO` è stato un margine
  senza fonte che reggeva per 1,30 su 27,86.

Script della parte 2 in `giri/evidenze/2026-10-17-punteggio-D/` (`p4.py`, `p4_tabella.py`,
`replay_cf.py`, `replay_ties.py`).

<!-- FINE DOCUMENTO -->
