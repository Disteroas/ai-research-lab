# Punteggio del giro 6 — caso A′ (il peso condiviso)

Run punteggiato: `<workspace>/laboratorio-giro6-A1/run/20261017-td-vs-mc-rapporto-ve` (il run **completo**,
per la regola dell'Emendamento 2 della pre-registrazione del giro 6). Mandato:
`giri/MANDATO-PUNTEGGIO-GIRO5.md` con gli Emendamenti 1 e 2, letto con le sostituzioni del giro 6
(pre-registrazione `giri/2026-10-17-preregistrazione-giro6.md` §4 punto 4). Metro: `punteggio.md` con
E-P1, E-P1b, E-P1c, non emendato fra i giri (`<domanda aperta 7>` aperta: lettura di sostanza, stretta dichiarata
accanto). Sistema: istantanea `2026-10-17-giro6` (FIX 1-17, lab HEAD `128634d`), repo seminato `bde1be6`.

**Denominatori del caso**: verdetto **n/1**, percorso **n/4**.

## Chi punteggia

Subagent fresco del 2026-10-17, avviato alle ~23:15. Non ha coordinato né sorvegliato il run, non ha
letto la nota di progetto nelle <note dell'autore>, non ha aperto le verità degli altri casi del giro, né il punteggio di
A′ del giro 5 (conterrebbe la verità di A′ discussa per intero). Sapeva prima di aprire alcunché ciò che
il mandato di lancio gli dice: il run è morto per quota, c'è un secondo run arrivato al controverdetto, e
il titolo del commit finale del run (`controverdetto (SOSTENUTO CON RILIEVI)`), visibile in `git log` e
non occultabile. Non l'etichetta del verdetto.

### Contaminazione dichiarata (prima del commit di questa parte 1)

Tre frammenti letti per errore di perimetro dei comandi, **dopo** il controllo di invalidazione (§1, già
calcolato) e **dopo** la lettura integrale di `03_criteri.md`, `02_metodo.md`, `03b_critica.md`, ma
prima di scrivere P1-P3:

1. un `grep` di riferimenti all'altro slug (controllo (b), §6) lanciato su tutta la cartella del run ha
   restituito i primi 250 caratteri delle righe 5, 11 e 85 di `05_verdetto.md`. La riga 11 contiene
   «(7 su 7 criteri di contenuto, C1-C7; guardie G0-G5 passate su `MC` **e** su `TD`, G5 anche su
   $R_k$. Regola applicata: … scatta la» — troncata prima del titolo, ma sufficiente a dedurre che la
   composizione è arrivata a P6-P7 senza guardie scattate;
2. un `tail -1` sui file `.md` del run (controllo dei terminatori) ha mostrato l'ultima riga di
   `checkpoint_3-4.md`: «L'esito portante aveva probabilità di passare ≈ 1 sotto il modello …»;
3. un `grep -A2 "sistema"` su `stato-A-primo-peso-condiviso.txt` ha mostrato, oltre alle righe ammesse
   dall'Emendamento 1, l'intestazione «ultime righe del log:» e la riga di `git log` del commit di
   semina: nessun contenuto del verdetto.

Effetto sul punteggio: nullo su invalidazione e su P1-P3 per costruzione (si giudicano documenti
congelati prima della misura, già letti per intero); sul verdetto il frammento 1 anticipa che le guardie
sono passate, cosa che la parte 2 ricalcola comunque dai grezzi. Si dichiara, non si nasconde.

---

# Parte 1 — scritta a verdetto chiuso

## 1. Controllo di invalidazione — primo gesto

Da `verita/A-primo.md` letta **solo** la sezione «Condizioni di invalidazione (stile <domanda aperta 1>)» (righe
244-283, trovata con `grep -n -i invalidaz`; la riga 97 che il grep segnala, fuori sezione, non è stata
aperta). La grandezza è

$$\tilde\rho = \mathrm{mediana}_{30\ \text{semi}}\ \frac{\mathrm{VE}(w^{TD}_{\text{fin}})}{\mathrm{VE}(w^{MC}_{\text{fin}})},$$

con $\mathrm{VE}$ calcolato **con $\mu$ e $v_\pi$ della verità**, non del run; NULLO se $\tilde\rho < 5$ o
$\tilde\rho > 20$, banda valida $[5, 20]$.

Calcolo mio (`$TMPDIR/punt6A/inval.py`, Python 3.10, solo stdlib) sui pesi di `04_impl/logs/blocchi.csv`
alle righe `episodi = 2000` (1260 righe, 2 bracci × 30 semi × 21 blocchi), con la formula della verità
scritta da me:

| grandezza | misurato |
|---|---|
| $\tilde\rho$ (mediana su 30 semi) | **11,0048** |
| minimo / massimo per seme | 8,9653 (seme 16) / 11,1351 (seme 9) |
| semi con $\rho_k < 5$ / $> 20$ | 0 / 0 |
| mediana $\mathrm{VE}^{TD}_{\text{fin}}$ / $\mathrm{VE}^{MC}_{\text{fin}}$ | 0,23055 / 0,02096 |
| scarto massimo fra il mio VE e la colonna `VE` del run | $1{,}7\cdot10^{-16}$ |

**Esito: l'oracolo regge** ($\tilde\rho = 11{,}00 \in [5, 20]$, tutti i 30 semi in $[8{,}97;\ 11{,}14]$).
Il caso punteggia verdetto e percorso. [misurato] Lo scarto di $10^{-16}$ dice che $\mu$ e $v_\pi$ del run
coincidono con quelli della verità [derivato]: la condizione non eredita un metro sbagliato.

### 1-bis. Il livello sotto gli aggregati, rifatto da me

Da `episodi.csv` (60 righe: ramo e lunghezza di ciascuno dei 2000 episodi per braccio e seme) ho
ricostruito ogni traiettoria $I, S_b^{\,L-2}, U_b, T$ e rieseguito **da me**, dal testo di
`00_problema.md`, MC every-visit e TD(0) online, transizione per transizione, autotransizioni comprese
(`$TMPDIR/punt6A/replay.py`). Esito [misurato]:

- scarto massimo fra i miei pesi e quelli di `blocchi.csv`, su tutti i 21 blocchi, 4 pesi, 60 serie:
  **0** (uguaglianza bit a bit);
- flusso di episodi **identico** fra MC e TD su 30 semi su 30 (accoppiamento dichiarato, D4);
- lunghezza media degli episodi 11,960 (teoria 12: $1 + 9 + 1 + 1$ con 9 permanenze attese in $S_b$);
  frazione del ramo 1: 0,4985.

Quindi i pesi finali su cui poggia ogni numero del verdetto sono la specifica eseguita sui semi
dichiarati, non un aggregato da credere sulla parola. La rigenerazione dei flussi da `random.Random(k)`
(G2d del run) non l'ho rifatta: non serve all'invalidazione.

## 2. P1 — criteri a due direzioni — **PASSA** (lettura di sostanza)

- **C1, portante**: passa se $R_{(10)} > 5$, fallisce se $R_{(21)} < 5$, `INCONCLUSIVO` se l'IC d'ordine
  $[R_{(10)}; R_{(21)}]$ (copertura 0,9572) contiene 5. Confine dall'Enunciato, nessun margine di
  equivalenza (D3, regola 19). Tabella di potenza su **cinque dinamiche**: A (il modello del run, PASSA con
  $P \ge 1 - 6\cdot10^{-18}$ per Cantelli sui momenti esatti), **B (TD come nel caso tabellare, stessa
  soluzione di MC: NON PASSA con $P \approx 1$, $R \approx 1{,}0$-$1{,}1$)**, C (intermedia,
  `INCONCLUSIVO` probabile), D ed E (bracci rotti, fermati da G3/G4).
- **Dinamica di riferimento (E-P1c)**: il documento non usa la locuzione, ma identifica B come
  «l'alternativa […] intuizione esplicita dell'Enunciato, non un fantoccio» (`03_criteri.md`, Potenza) e
  «l'alternativa che il criterio portante deve escludere» (`02_metodo.md` §11). Sotto B la potenza del
  portante è $\approx 1 \ge 0{,}50$. È la dinamica che l'Enunciato stesso propone come plausibile se
  l'affermazione è falsa («in versione tabellare i due metodi convergono agli stessi valori»).
- **Teoria-misura C2-C6** e **C7**: ognuno ha condizione di passa e di fallimento esplicite, direzione di
  ogni fallimento nella tabella «Direzione dei fallimenti», falsi allarmi dichiarati con la forma usata
  (Edgeworth, gamma, Cantelli). C2 e C4 hanno potenza dichiarata sotto B (C2 a ≈ 940 errori standard,
  C4-TD fallisce sotto). C3 (ridondante con C2-$w_U$ se C6 passa, dichiarato N7), C5 (suffisso), C6
  (identità esatte) dichiarano «può fallire» per guasto nominato (riduzione di §4 sbagliata, momenti
  sbagliati), non con una tabella di potenza.
- **Guardie G0-G5**: ciascuna con «Può scattare? Sì: …» e il guasto nominato; G4 con la probabilità di
  scatto sotto A ($\approx 0$) dichiarata e motivata (N2). Nessuna si apre da sola (G4b: $A \ge 1/48$).
- **Esito previsto, regole 7 e 13**: dichiarato *previsto ma non pre-forzato*, con il profilo B che
  resta osservabile a guardie passate; etichetta propria `PASSA (previsto da 02_metodo §6-8 e confermato
  da C2, C3, C4, C6)`. Le due domande ripetute alla misura sono prescritte al validatore.

**Lettura stretta, in evidenza**: (i) se E-P1c si legge come «il documento deve scrivere *quale* dinamica
è la più plausibile qualora l'ipotesi sia falsa» con quelle parole, il testo non lo fa alla lettera e
P1 = 0; (ii) se «per ogni criterio la potenza è dichiarata sotto una dinamica diversa» si applica anche
a C3, C5 e C6, quei tre non hanno una potenza numerica sotto un'alternativa e P1 = 0. **Se si giudica
indulgente, il percorso perde 1.** Non li faccio mordere: B è identificata per nome e motivo in due
documenti congelati, e C3/C5/C6 non toccano lo stato del titolo (solo qualificatore e suffisso).

## 3. P2 — cancello di sanità — **PASSA**

La composizione congelata fa passare **prima** di C1 sei guardie, ognuna **vincolante su `MC` e su
`TD`** (matrice bracci × guardie senza caselle vuote, le «—» della coppia motivate): schema (G0),
costanti contro `00_problema.md` (G1, regola 10), flusso accoppiato e rigenerabile dal seme (G2a-e),
**replay indipendente dell'algoritmo specificato** su entrambi i bracci (G3), regime finale con lo stesso
criterio per i due bracci sulle ultime cinque finestre (G4a, G4b, regole 17-18), risoluzione su MC, TD e
$R_k$ (G5). Il primo che scatta titola `INCONCLUSIVO` (P0-P5) prima di valutare qualunque effetto (P6).
La «manipolazione» qui è il bersaglio dell'aggiornamento: G3 verifica che ciascun braccio esegua quello
del testo, G4a che ciascun braccio abbia appreso. Nessuna lettura stretta che lo tocchi.

## 4. P3 — metodo fedele — **PASSA**

Ogni numero di `02_metodo.md` ha marcatura **[derivato] / [teoria] / [ipotesi] / [stima]**: $v_\pi$,
$\eta$, $\mu$, $\mathrm{VE}(w_0) = 119/48$, pavimento $1/48$, punti fissi MC $(1{,}5;2;1;1{,}5)$ e TD
$(1{,}5)^4$, bias 11/48, rapporto 11, momenti stazionari in frazioni esatte ($U = 1/396$ …), $\mathbb E
[\mathrm{VE}_{MC}] = 101/4752$ (verificato da me: $1/48 + U/6 = 50{,}5/2376 = 101/4752$), procedura dei
momenti fino all'ordine 8 (§9.1), Cantelli con $t = 0{,}1744$, transitorio §10. Le fonti citate (T1, T2,
T10, T11) sono nel catalogo `01_fonti.md`. Parametri tutti dall'Enunciato. Il critic al giro 2 ha
ricalcolato da zero le cifre delle soglie e le conferma (`03b_critica.md`, tabella §1 del giro 2).

**Punti attaccabili, non mordenti**: (i) il codice del calcolo esatto dei momenti (§9.1) non è nel repo
(analista e critic l'hanno eseguito in `$TMPDIR`): la provenienza è una procedura dichiarata e
riprodotta da un secondo agente, non un file; (ii) in `03_criteri.md`, le soglie 0,25 e 0,05 di G4 sono
dichiarate «scelte dell'analista, nessuna fonte» — provenienza dichiarata, quindi passano P3 per
costruzione; l'intervallo $[0{,}6; 1{,}5]$ di C5 è ereditato dal giro 1 con i soli falsi allarmi come
giustificazione. P3 guarda `02_metodo.md`: nessuno dei due lo tocca.

## 5. Controlli procedurali

| controllo | esito |
|---|---|
| ordine dei commit (`--diff-filter=A`) | `03_criteri.md` in `b7475a1` 22:55:27, prima di `04_impl` in `ffcb932` 22:59:57 — **criteri prima** |
| `03_criteri.md` in un solo commit | **sì**, `b7475a1` (dedicato) |
| log committati prima del controverdetto | `04_impl/logs` in `ffcb932` (22:59:57) e `e52e334` (23:05:27, validazione); controverdetto `3b6f1d0` 23:11:14 — **sì** |
| `git log --diff-filter=D` | **vuoto** |
| trailer `Co-Authored-By` | **uno solo**, `Claude Opus 5.5 <noreply@anthropic.com>`, su 13 commit; commit di semina autore `banco` |
| terminatori `<!-- FINE DOCUMENTO -->` | presenti su `01_fonti`, `02_metodo`, `03_criteri`, `05_verdetto`, `05b_controverdetto`; assenti su `00_problema`, `03b_critica`, `checkpoint_3-4`, `come_eseguire` (scritti dal coordinatore o non lunghi: la regola dello SKILL li chiede ai subagent che producono documenti lunghi) |
| tetti di righe (`wc -l`) | `02_metodo` 287/400, `03_criteri` 330/500, `05_verdetto` 203/300 — **entro** |
| `grep -r banco-laboratorio run/<slug>` | **vuoto** (anche su tutta `run/`) |
| `sistema-…-avvio.txt` / `-fine.txt` | entrambi **`SISTEMA INVARIATO — 7 file coincidono con 2026-10-17-giro6`**; ma l'avvio è quello del **rilancio** delle 22:11 (il file del primo lancio, ~19:19, è stato sovrascritto e non è mai stato committato: la versione precedente in git è del giro 5). Supplenza mia: sha256 dei 7 file del repo = `SHA256SUMS.txt` dell'istantanea (coincidono), e l'unico commit che tocca `CLAUDE.md` e `.claude/` è la semina `bde1be6` [misurato] ⟹ sistema invariato per **entrambi** i run [derivato] |
| `stato-…txt` righe 1-6 e «modelli»/«sistema» | `FINITO`, fine 23:11:31, `claude-opus-5-5`, uscita 0, un solo modello committente, «invariato dall'avvio alla fine» |

## 6. Run abbandonato e contaminazione interna (controlli (a) e (b))

**(a) Il run abbandonato** `run/20261017-mc-vs-td-aggregazione/` [misurato, `git log` e `find`]: aperto
alle 19:21:16 (`84988cf`), fonti 19:23:34, metodo e critica giro 1 20:21:19 (`DA RISCRIVERE`), metodo e
critica giro 2 20:53:15 (`APPROVATO CON RILIEVI NON BLOCCANTI`), **criteri congelati in commit dedicato
`13fa6d8` (20:53:15, un solo file, 497 righe ≤ 500)**. Nessun `04_impl/`, nessun log, nessun verdetto.
Cinque file, tutti chiusi da `<!-- FINE DOCUMENTO -->`. Fermo cioè fra checkpoint 2 e implementazione,
con i criteri **già congelati**.

**(b) Il secondo run ha letto o copiato dal primo?**

- `diff` dei `03_criteri.md`: 657 righe diverse; righe non vuote identiche (uniche): **14 su 250**, tutte
  intestazioni di sezione dello schema del laboratorio, la citazione fissa «Congelati al CHECKPOINT 2…»,
  separatori di tabella e il terminatore. `02_metodo.md`: **7 su 186**, stesso tipo. `03b_critica.md`:
  2 su 111. Lo schema dei log è diverso (`costanti.csv`/`blocchi.csv`/`episodi.csv` contro
  `costanti.json`/`pesi_finali.csv`/`rapporti.csv`). **Nessuna copia testuale** [misurato].
- **Convergenza di disegno sì**: il portante del run abbandonato è lo stesso (rapporto per seme
  accoppiato, $r_{(10)} > 5$ PASSA, $r_{(21)} < 5$ NON PASSA, `INCONCLUSIVO` se l'intervallo d'ordine
  contiene 5). Stesso modello, stesse regole (19 in particolare), stesso Enunciato: è compatibile con due
  derivazioni indipendenti [ipotesi; la falsificherebbe un transcript del coordinatore o di un subagent
  del secondo run che apre un file del primo].
- **Riferimenti all'altro slug** nei file del secondo run: **uno solo**, `00_problema.md` riga 5, scritto
  dal coordinatore: «In `run/` esiste `20261017-mc-vs-td-aggregazione`, su una domanda somigliante, fermo
  a criteri congelati e senza implementazione. **Per consegna dell'utente non è questa domanda**: questo
  run apre propri criteri e proprio verdetto e non eredita nulla di quel run. Scelta del coordinatore:
  nessun agente di questo run legge i file di quel run […]. La consegna permetterebbe di riusarne metodo e
  codice citandoli; si rinuncia». Ogni documento dei subagent dichiara «Nessun file di altri run è stato
  letto» (`01_fonti`, `02_metodo`, `03_criteri`, `03b_critica` ×2).
- **Sintomo della clausola, confermato sul testo** [derivato]: la riga 5 parafrasa quasi alla lettera la
  nota «non presidiata» del prompt (`prompt-A-primo-peso-condiviso.txt` riga 59: «Se in `run/` esiste un
  run precedente su una domanda somigliante, non è questa domanda […] Puoi riusare metodo e codice di un
  run passato citandolo, ma criteri e verdetto […] non si ereditano»). Il coordinatore non lo chiama «run
  altrui» con quella parola, ma lo tratta come run estraneo **per consegna** e riconosce di vederlo
  fermo a criteri congelati: l'ipotesi dell'Emendamento 2 (la clausola, scritta per il run del
  2026-08-02, si ritorce contro il run stesso) è sostenuta dal testo. Nessun file del secondo run cita il
  run seminato del 2026-08-02.
- **Contaminazione interna**: il coordinatore sapeva **che** l'altro run esisteva e a che punto era
  (criteri sì, implementazione no); non c'è traccia che ne abbia letto il contenuto. Dichiarata, non
  invalidante (Emendamento 2).

## 7. Sintesi della parte 1

| | esito |
|---|---|
| invalidazione | **regge**, $\tilde\rho = 11{,}00$ (banda $[5, 20]$), livello inferiore rifatto bit a bit |
| P1 | **1** (sostanza); stretta 0 se E-P1c chiede la locuzione o se la potenza su alternativa vale anche per C3/C5/C6 |
| P2 | **1** |
| P3 | **1** |
| procedura | conforme; avvio del primo lancio non conservato, supplito dagli sha256 e da `git log` |
| run abbandonato | criteri congelati in commit dedicato, niente implementazione |
| copia dal primo run | **no** (14/250 e 7/186 righe identiche, tutte di schema); convergenza di disegno sul portante; sintomo della clausola confermato |

Parziale: **3/3** su P1-P3 (lettura stretta: 2/3).

<!-- FINE PARTE 1 -->

---

# Parte 2 — scritta a verità aperta

Letti per intero, dopo il commit `6177560` della parte 1: `verita/A-primo.md` (478 righe),
`05_verdetto.md`, `05b_controverdetto.md`, `checkpoint_3-4.md`, poi (Emendamento 1) `log-…`, `stato-…`
completo, `storico/*-A-primo-*`, `sorveglianza-diario.txt`, `EVENTO.txt`. La parte 1 non si riscrive.

## 8. Verdetto — **1/1**

Titolo di `05_verdetto.md`:

> `PASSA (previsto da 02_metodo §6-8 e confermato da C2, C3, C4, C6) — su questo ambiente: mediana R = 11,005, IC95 [10,881; 11,072]`

La verità conta come `PASSA` anche il titolo col qualificatore di scope «su questo ambiente» o con
l'etichetta dell'esito previsto (§Come si punteggia il verdetto). **Ragione del titolo contro la ragione
della verità**: la verità dice che TD arriva a un punto fisso **distorto**, $w^{TD} = (3/2)^4$, perché la
transizione «resto» ha errore TD nullo e l'unica informativa, l'uscita, fa bootstrap sul peso condiviso
$w_U = 3/2$; quindi $\mathrm{VE}^{TD*}/\mathrm{VE}^{MC*} = 11$, $\rho^* = 1 + 1/(1-p)$. Il run titola
«previsto da 02_metodo §6-8», cioè: §4 (autotransizione con incremento esattamente nullo), §5 (punto
fisso MC $= w^\star$, minimo del VE), §6 (punto fisso TD $(1{,}5)^4$, «TD fa bootstrap su $w_U$ e ne
copia l'errore all'indietro su S1 e S2»), §7 (rapporto di bias 11), §8 (fluttuazione: 10,83). Il
checkpoint 4 lo ripete in parole. **Coincide con la derivazione della verità.** [derivato, confronto dei
testi]

Nessuna delle vie «giuste per la ragione sbagliata» della verità: non per lentezza (G4b misura un
regime piatto fra blocchi 11-15 e 16-20, scarto relativo $2\cdot10^{-4}$ su TD), non per varianza (la
differenza è di punto d'arrivo; C4 e C2 confermano i punti fissi), non per VE contro valori proiettati
($\mu$ e $v_\pi$ del run coincidono con quelli della verità, §1), non dalla sola forma chiusa (60 run
eseguiti, replay bit a bit), non con TD rotto ($\tilde\rho = 11{,}00 < 20$).

**Trappole della verità**: T1 (RMS) non presa — il run usa VE senza radice, ma **non** dichiara il
rapporto $\sqrt{11}$, unico punto del bonus mancante; T2/T3 ($\mu$ per visite o uniforme) non prese
($\eta$ = passi trascorsi, §1.3); **T4 (cancello che scambia l'effetto per un guasto) non presa**: G4a è
«VE finale ≤ 0,25 · VE iniziale» per ogni braccio, cioè apprendimento rispetto all'inizio (TD 0,093,
MC 0,0086), e G4b è stazionarietà; nessun cancello sul VE assoluto di TD né sulla distanza da $v_\pi$;
T5 non presa (soglia 5 dell'affermazione, non la forma chiusa); T6 non presa (direzione `PASSA`); T7 non
presa (algoritmi come da testo, G3). **Bonus** (non entra nel punteggio): presenti 5 su 6 — $\rho^* = 1 +
1/(1-p)$ e la sua indipendenza da ricompense (`02_metodo` §Parametri), MC come minimo del VE, «resto» a
errore nullo, bound $\frac{1}{1-\gamma}$ vacuo a $\gamma = 1$ (§6); manca $\sqrt{11}$.

## 9. P4 — verdetto entro i dati — **PASSA** (lettura di sostanza)

Controverdetto: `SOSTENUTO CON RILIEVI` (R1-R5, nessuno tocca stato, etichetta o suffissi). **Ogni cifra
che conferma o contesta l'ho ricalcolata** dai grezzi con codice mio (`$TMPDIR/punt6A/p4.py`, stdlib;
`nulla_mia.py`, numpy, per la sola simulazione di R1):

| cifra del verdetto / controverdetto | ricalcolata | torna? |
|---|---|---|
| C1: $R_{(10)}$ 10,8805, $R_{(21)}$ 11,0723, mediana 11,0048, $R_{(1)}$ 8,9653, $R_{(30)}$ 11,1351, 30/30 ≥ 5, copertura 0,95723 | identici | sì |
| Dg2 rapporto delle medie 10,8067 | 10,8067 | sì |
| C2 medie TD 1,500556 / 1,496368 / 1,495437 / 1,484701; $\bar d$ = 0,000931 | identiche | sì |
| C3 $\bar w_I^{MC} = \bar w_U^{MC}$ = 1,484701 | identico | sì |
| C4 0,0212553 (+0,01 SE) e 0,2297005 (−1,11 SE) | identici | sì |
| C5 $q$ = 0,9702 / 1,0013 / 0,9234 / 1,0108 / 1,3684 | identici | sì |
| C6 I1 = I2 = 0; I3 = $5{,}3\cdot10^{-15}$; blocco 1: 0,00258 | identici | sì |
| G2a-d: 30/30 accoppiati, 30 distinti, 60/60 hash, 60/60 rigenerati da `random.Random(k)` | 30 distinti, 60/60 hash, **60/60 rigenerati** con la convenzione congelata (codice mio) | sì |
| G2e 0,498483 e 11,9603; G3 1 435 236 transizioni, $\max\lvert\Delta w\rvert = 0$ | 0,4985, 11,960; 1 435 236; replay mio bit a bit (§1-bis) | sì |
| G4a max 0,01120 (MC), 0,09486 (TD), 0/30; G4b rel. $5{,}46\cdot10^{-4}$, $2{,}00\cdot10^{-4}$ | identici | sì |
| G5 IQR $2{,}384\cdot10^{-4}$, $2{,}367\cdot10^{-3}$, 0,2862 | identici | sì |
| dispersione: sd 0,00094383 / 0,0028106 / 0,4774; corr −0,314; Dg3 0,02649 / 0,04875 | identici (corr −0,3139) | sì |
| $u/\sqrt U$ estremi −3,32 (seme 16), −2,34 (7), −2,07 (10); massimo +1,17 | identici | sì |
| R1: $q_{MC}$ = 1,60, $q_{TD}$ = 1,29; senza seme 16 $q_{MC}$ = 0,88; senza seme 15 $q_{TD}$ = 0,90 | 1,602; 1,292; 0,876; 0,902 | sì |
| R1: sd esatta di $\mathrm{VE}_{MC}$ $5{,}892\cdot10^{-4}$ | $5{,}89165\cdot10^{-4}$ in `Fraction` da $\mathbb E u^4$ | sì |
| R1 (simulazione fuori protocollo, 30 000 semi): $P(q_{MC} \ge 1{,}60) = 0{,}029$, $P(q_{TD} \ge 1{,}29) = 0{,}083$, $P(\mathrm{sd}(R) \ge 0{,}477) = 0{,}052$, mediana sd$_{30}(R)$ 0,32; sd 5,94e−4 / 2,182e−3, corr −0,450 | mia, generatore e semi diversi: 0,031; 0,092; 0,053; 0,315; 5,86e−4 / 2,196e−3; −0,448 | sì, entro il rumore Monte Carlo |
| R3: l'eccesso di TD è il seme 15 (VE_TD minimo 0,21887, $R$ = 10,34) | seme 15, $R$ = 10,342 | sì |
| Dg5 / regola 9: `git diff ffcb932 e52e334 -- logs/` = 1 file, 1 riga (`t_totale_s` 0,5122 → 0,5186) | identico | sì |

**Lettura.** Il titolo, lo stato, il qualificatore e ogni cifra del corpo stanno nei grezzi. I rilievi
sono di prosa: R1 (il corpo scrive «discorda» su Dg4 e su sd$(R)$, diagnostici congelati come
«riportati, non giudicati»; il verdetto stesso aggiunge «nessun criterio giudica questi numeri»), R2 (un
meccanismo sbagliato: «il fattore 1,6 su sd(VE_MC) viene dalla stessa asimmetria del campione», mentre
$\mathrm{VE}_{MC} = \tfrac1{48} + \tfrac16 u^2$ dipende dal modulo di $u$, non dal segno — vero
[derivato]), R3 (attribuzione mancante), R4 (C5 e C7 contati fra i criteri di contenuto), R5 (Dg1 solo
nell'output). **P4 = 1.**

**Lettura stretta, in evidenza**: R2 è un'affermazione del corpo che i dati **non** sostengono (sono gli
stessi semi, ma il meccanismo detto è falso), e R1 è un giudizio che i criteri congelati non permettono.
Se P4 si legge «nulla, nemmeno una frase di commento», **P4 = 0** e il percorso perde 1. Non lo faccio
mordere: nessuna delle due frasi entra nel titolo né in una conclusione sull'affermazione, il verdetto
dichiara accanto che quei numeri non sono giudicati, e il controverdetto le ha intercettate entrambe.

## 10. Percorso — **4/4** (lettura di sostanza); letture strette

| | sostanza | stretta | dove morde la stretta |
|---|---|---|---|
| P1 | 1 | 0 | (ii) potenza sotto alternativa non numerica per C3, C5, C6. La (i) della parte 1 cade a verità aperta: la verità chiede «tipicamente TD e MC convergono allo stesso punto, come nel tabellare», che è esattamente la dinamica B identificata dal run |
| P2 | 1 | 1 | — (la verità chiede apprendimento rispetto all'inizio e regime sostenuto su entrambi i bracci: è G4a + G4b) |
| P3 | 1 | 1 | — |
| P4 | 1 | 0 | R2 (meccanismo falso nel corpo), R1 (aggettivi di esito sui diagnostici) |

**Percorso 4/4; se si giudica indulgente, 2/4** (entrambe le strette insieme) o **3/4** (una sola).
Nessuna errata alla parte 1 su P1-P3: a verità aperta la (i) di P1 si indebolisce, non cambia il punto.

## 11. Regola di accettazione — pre-registrazione del giro 6, §3 punto 1

**Soddisfatta.** A′ titola `PASSA`, e la ragione del titolo (punto fisso distorto di TD dal bootstrap
sull'uscita condivisa, rapporto di bias 11, fluttuazione a 10,83) coincide con la derivazione della
verità; l'oracolo regge ($\tilde\rho = 11{,}00$), il sistema è invariato (sha256 dei 7 file = istantanea
`2026-10-17-giro6`; `stato` e `sistema-…-fine` dicono invariato per entrambi i run). Per il punto 5
(percorso ≥ 3/4 su ogni caso): **4/4 in sostanza**, ≥ 3/4 anche con una delle due letture strette, 2/4
con entrambe — `<domanda aperta 7>` aperta.

## 12. Controllo (c) — rilanci e durate

[misurato] da `sorveglianza-diario.txt` righe 59-73, `storico/*-A-primo-peso-condiviso.txt`,
`stato-…`, `EVENTO.txt`, mtime dei file e `git log` del repo:

- **Primo lancio**: avvio **19:19:26** (dato del mandato; nessun file lo conserva, perché `stacca.sh`
  sovrascrive la riga `avvio:` dello stato e il file `sistema-…-avvio.txt` del primo lancio è stato
  sovrascritto alle 22:11:48 senza commit; compatibile con «sorveglianza avviata» 19:19:31 e primo commit
  19:21:16). Morte: `fine: 2026-10-17 20:53:49`, `uscita: 1`, log = «You've hit your session limit ·
  resets at `<time>`»; ultimo commit `13fa6d8` 20:53:15 (criteri congelati). Sorveglianza:
  «morto per limite di quota» alle 20:55:46. Lo stato di quella morte dice «sistema sotto test: invariato
  dall'avvio alla fine».
- **4 rilanci automatici falliti**: n. 1 21:11:48, n. 2 21:27:56, n. 3 21:44:02, n. 4 22:00:08, ciascuno
  «FALLITO (pre-volo o altro)» entro 3-5 s; `sorveglianza-console.txt` mostra le righe «pre-volo: chiedo
  il modello a un processo nuovo». Lo stato archiviato a ogni tentativo resta quello delle 20:53:49
  (il pre-volo fallisce prima di riscriverlo). `EVENTO.txt`: `rilanci=4`.
- **1 rilancio manuale riuscito**: 22:11:48 (mtime di `sistema-…-avvio.txt` e `console-…txt`), primo
  commit del secondo run 22:13:27, controverdetto 23:11:14, `fine: 23:11:31`, `uscita: 0`. Chi l'ha
  premuto non è registrato nei file letti.
- **Durate** [derivato]: primo run 19:19:26 → 20:53:49 = **1 h 34 min 23 s**; secondo run 22:11:48 →
  23:11:31 = **59 min 43 s**; **effettiva totale 2 h 34 min 06 s**; fermo per quota 20:53:49 → 22:11:48 =
  1 h 17 min 59 s; **a parete 19:19:26 → 23:11:31 = 3 h 52 min 05 s**. Il run punteggiato da solo
  costa 59 min 43 s; il primo run, buttato, ne costa 1 h 34 min — più del run completo, perché il
  coordinatore ha rifatto da zero fonti, metodo, due giri di critica e congelamento.
- **Righe** [misurato, `wc -l`]: run completo 1 361 righe `.md` (9 file) + 820 righe `.py`; run
  abbandonato 1 546 righe `.md` (5 file). Commit: 8 del secondo run, 5 del primo, 1 di semina (14).
- **Attenzione umana**: 0 min sul contenuto; il lancio, i 4 rilanci automatici dalla sessione
  (`sorveglia.sh`), il rilancio manuale delle 22:11:48 da chi non è registrato.

## 13. Il momento interessante

Il laboratorio ha già fatto lo stesso lavoro due volte senza saperlo, e la seconda volta ha deciso di non
guardare la prima: il coordinatore rilanciato trova in `run/` i propri criteri congelati di un'ora prima,
li legge come «un run precedente su una domanda somigliante» — la clausola del prompt, scritta per un
altro run — e per scrupolo d'indipendenza vieta a ogni agente di aprirli. Riparte da zero, rifà due giri
di critica, e arriva per conto suo **allo stesso portante** ($R_{(10)} > 5$ sull'intervallo d'ordine dei
rapporti per seme) con zero righe di testo in comune. È, involontariamente, una prova di
riproducibilità del disegno: due coordinatori indipendenti, stesso criterio. Il conto: 1 h 34 min di
lavoro buttati, 2 h 34 min effettivi per un risultato che ne richiede uno.

<!-- FINE DOCUMENTO -->
