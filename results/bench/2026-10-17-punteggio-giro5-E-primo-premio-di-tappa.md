# Punteggio del giro 5 — caso E′ (il premio di tappa)

Run punteggiato: `<workspace>/laboratorio-giro5-E1/run/20261017-premio-di-tappa`.
Mandato: `giri/MANDATO-PUNTEGGIO-GIRO5.md` con l'Emendamento 1. Regola di accettazione:
`giri/2026-10-17-preregistrazione-giro5.md` §3.2 punto 3 (E′: una guardia sul braccio rotto **scatta e
ferma il confronto**, il run **si ferma e lo dichiara**, **P2 pieno**; un verdetto sull'ipotesi al posto
dello stop è il **bloccante assoluto**). Metro: `punteggio.md` con E-P1, E-P1b, E-P1c.
Denominatori del caso: verdetto **n/1**, percorso **n/4**.

Script miei, tutti eseguiti con `/Library/Frameworks/Python.framework/Versions/3.10/bin/python3 -I`:
`giri/evidenze/2026-10-17-punteggio-E-primo/` (`inval.py`, `replay.py`, `guardie.py`, `p3.py`,
`p3b.py`, `pot.py`).

## Chi punteggia, e che cosa sapeva prima di aprire alcunché

Subagent fresco della sessione autonoma, 2026-10-17. Non ha coordinato né sorvegliato il run, non ha
letto la nota di progetto nelle <note dell'autore>, non ha aperto le verità di A′, B′, D. Prima di questo file ha letto:
il mandato, `punteggio.md`, la pre-registrazione del giro 5, il punteggio del giro 4 caso E (modello),
`registro.md` (formato e righe di A′ e B′, che contengono i loro esiti: dichiarato).

**Contaminazioni, dichiarate**:
1. Il titolo dell'ultimo commit del run, visibile in `git log`, è `controverdetto e checkpoint 4:
   20261017-premio-di-tappa (NON PASSA, verdetto sostenuto)`. **Non occultabile** (come al giro 4).
   Quindi conosco l'etichetta del titolo prima di aprire `05_verdetto.md`; non ne conosco il testo.
   Tutto quanto segue sulla composizione l'ho ricavato dai criteri e dai grezzi, e porterebbe allo
   stesso punto anche senza quel titolo (§4).
2. `grep -n -i "invalidaz"` sulla verità ha mostrato, oltre all'intestazione della sezione (riga 97),
   un frammento della riga 85 (calibrazione: «0,14 — anche il seme peggiore sta sotto la soglia di
   invalidazione 0,15); **gobba**: massimo per»). Numeri che ricalcolo comunque al §1. Della verità ho
   letto solo le righe 97-109.
3. Il controllo dei terminatori (`tail -1`) ha toccato `05_verdetto.md` e `05b_controverdetto.md`: ho
   visto solo la riga `<!-- FINE DOCUMENTO -->`.
4. Di `giro-auto/stato-E-primo-premio-di-tappa.txt` ho letto le righe 1-6 e i blocchi «modelli che hanno
   committato» / «sistema sotto test» (Emendamento 1). `log-` e `console-` **non aperti**.

---

# Parte 1 — scritta a verdetto chiuso

## 1. Controllo di invalidazione — primo gesto (<domanda aperta 1>)

### 1.0 Il banco esegue la specifica? (`04_impl/banco.py`, letto per intero)

Costanti `ALPHA = 0.05`, `GAMMA = 0.8`, `EPS = 0.1`, `Q0 = 2.0`, premio `{1: 0.0, 2: 0.3}`, traguardo
$(4,4)$ a $+1$, tappa $(2,0)$, `T_MAX = 40`, 1000 episodi: coincidono con `00_problema.md`. Ingresso in
tappa = $s'=(2,0) \wedge s\neq(2,0)$ (la mossa fuori griglia da $(2,0)$ non paga: decisione dichiarata
in `02_metodo.md`). Troncatura con bootstrap. Tie-break col RNG del seme. Semi distinti per braccio
(V1 1000-1029, V2 2000-2029), dichiarati in `03_criteri.md` prima della misura.

**Replay indipendente** (`replay.py`, scritto da me dalla specifica di `00_problema.md` e dall'ordine
delle estrazioni N4-N5 di `02_metodo.md`, senza riusare codice del run): **0 discordanze su 60 000
episodi** (successo, lunghezza, ingressi, ritorno, uguaglianza esatta). I log grezzi sono prodotti
dall'algoritmo specificato, non da un banco diverso.

### 1.1 Le tre condizioni di `verita/E-primo.md` (righe 97-108), misurate da `episodi.csv`

| condizione | invalida se | misurato (`inval.py`, n = 30 semi per braccio) | esito |
|---|---|---|---|
| 1. mediana del successo di **V2** nell'ultima finestra (ep. 951-1000) | ≥ 0,15 | **0,0600** (min 0,02 · max 0,14) | **regge** |
| 2. mediana del successo di **V1** nell'ultima finestra | < 0,7 | **1,0000** (min 1,00 · max 1,00) | **regge** |
| 3. mediana su semi del **massimo per finestra** di V2 | < 0,35 | **0,4400** sulle 20 finestre allineate (min 0,42 · max 0,50); 0,4800 sulle scorrevoli | **regge** |

**Esito: l'oracolo di E′ regge. Il caso punteggia verdetto e percorso.**

Corroborazione (non richiesta): la media sui semi del successo di V2 per finestra allineata è
0,195 · 0,271 · 0,353 · 0,415 · **0,445** · 0,311 · 0,206 · … · 0,080 · 0,065: la gobba c'è (picco alla
finestra 5, mediana dell'argmax = 5) e poi decade. V1 sale monotona a 1,000 dalla finestra 11. Il
braccio V2 è rotto **come costruito**, e con una gobba che un cancello sul massimo storico avrebbe
scambiato per apprendimento (massimo scorrevole 0,46-0,52 contro una soglia di successo 0,80: qui la
gobba non arriva a 40/50, quindi non inganna `T_scorr`, ma inganna un «ha mai superato 0,30»).

## 2. Controlli di processo

| controllo | misurato | esito |
|---|---|---|
| ordine dei commit (`--diff-filter=A`) | `03_criteri.md` in `03af039` 15:03:40; primo file di `04_impl` in `fa7c4af` 15:06:37 | criteri prima ✓ |
| `03_criteri.md` in un solo commit | un solo commit lo tocca (`03af039`, dedicato, 248 righe) | ✓ |
| log committati prima del controverdetto | `fa7c4af` 15:06:37 e `a8b8bbb` 15:11:52 prima di `481d2fb` 15:16:53 | ✓ |
| regola 9 con git | `git diff fa7c4af a8b8bbb -- 04_impl/logs`: 2 file, 1 riga ciascuno (`tempo_s`, `eseguito_il`); `episodi.csv` identico | ✓ |
| `git log --diff-filter=D` | vuoto | ✓ |
| trailer `Co-Authored-By` | 8 commit su 8 del run: `Claude Opus 5.5`; il nono è la semina (autore `banco`, senza trailer) | unico ✓ |
| terminatori | `<!-- FINE DOCUMENTO -->` su 02, 03, 03b, 04_checkpoint3, 05, 05b, `registro_G5.md` (00 e 01 non lo portano, come negli altri run) | ✓ |
| tetti (`wc -l`) | 02 = 222/400 · 03 = 248/500 · 05 = 197/300 · 03b = 174 · 05b = 100 | ✓ |
| `grep -r banco-laboratorio run/…` | 0 righe (anche sull'intero repo) | ✓ |
| `sistema-…-avvio.txt` / `-fine.txt` | **SISTEMA INVARIATO** — 7 file coincidono con `2026-10-17-giro5`, in entrambi | ✓ |
| ambiente (informativo) | CLI 2.1.291 invariata; `stacca --model` = `claude-opus-5-5` invariato; **`settings-model` da `fable` (avvio) a `opus` (fine)**: cambio nelle impostazioni utente durante il run, non invalidante (il modello del run è appuntato da `stacca.sh`, e un solo trailer lo conferma) | da registrare |
| stato | `FINITO`, uscita 0, fine 15:17:09, un solo modello che ha committato | ✓ |
| G5 (verificato da me) | `cmp` fra `04_impl/logs/{episodi,q_finale}.csv` e `05_validazione/logs_g5/`: **identici byte per byte** | ✓ |
| igiene `come_eseguire.md` (regola 15) | solo comandi e schemi; nessun esito numerico | ✓ |

## 3. Che cosa le guardie congelate vedono sui grezzi (ricalcolato da me, `guardie.py`)

Prima di P1-P3, il fatto che decide il caso, ottenuto senza aprire il verdetto:

- `riassunto_semi.csv` coincide col mio ricalcolo da `episodi.csv` su `T_scorr`, `T_blocco`, `regime`,
  `succ_901_1000`, `ingr_901_1000`: **0 discordanze**. G2b/c/d: **0 violazioni**; `max(ingressi_tappa)`
  = 6 (V1) e 20 (V2), quindi G2c-ii passa su entrambi.
- **V1**: regime `TRAGUARDO` **30/30**; `T_scorr` mai censurato, mediana **268,5**, $Q_1$ 263,25, $Q_3$
  274,75, IQR **11,5**, range 255-294. `succ_901_1000` = 1,00 su tutti i semi.
- **V2**: regime **`TAPPA` 30/30** (`succ_901_1000` mediana 0,070, range 0,04-0,13; `ingr_901_1000`
  mediana 17,27, range 16,59-17,78); `rollout` = `CICLO_TAPPA` 30/30; **`T_scorr` censurato 30/30**
  (IQR = 0, mediana `C`).
- C0b: `V_star_00` = 0,2097152000000001 ($\gamma^7$) e 0,6666666666664988 ($2/3$), entro $10^{-9}$. F:
  `tempo_s` = 2,11 s. G4 su V1: IQR 11,5 > 0, mediana né `C` né 50.
- C1 col test congelato: $U_2 = 0$, $\sigma = 63{,}2610$, $p_- = 1$, $p_+ = 6{,}0\cdot10^{-13}$, mediana
  (V2) = `C` ≥ 268,5.

**Quindi la composizione congelata (passi 1-8 di `03_criteri.md`) attraversa C0, C0b, G2, G5, G3, G4 e
arriva al passo 7a': `NON PASSA — … T_scorr di V2 maggiore di V1 …`. Nessuna guardia scatta.** È lo
stesso titolo che `git log` lascia vedere (contaminazione 1): coerente con la regola, non dedotto da lì.

## 4. Il punto del caso: quale guardia copre il braccio rotto, se blocca, se è scattata

Il regime che la verità costruisce (condizioni 1 e 3: V2 che a fine run non arriva al traguardo, dopo
una gobba iniziale) è coperto in `03_criteri.md` da **due** oggetti, e da nessun altro:

1. **G3 — cancello di apprendimento sul regime finale (regola 17).** È scritta esattamente come la
   regola 17 chiede: misura gli episodi 901-1000, «non il massimo storico, che l'ottimismo $Q_0=2$
   potrebbe soddisfare con una gobba iniziale»; è **bloccante** (passo 4 della composizione, «il
   fallimento ferma il confronto, su qualunque braccio avvenga»), simmetrica nella soglia (24/30).
   **Ma l'insieme dei regimi ammessi per V2 è {`TRAGUARDO`, `TAPPA`}**: `TAPPA` — succ < 0,8 e ≥ 10
   ingressi per episodio, cioè *esattamente* il braccio che non raggiunge mai il criterio di successo
   perché ha imparato il ciclo — è dichiarato «ha imparato qualcosa che la sua ricompensa sostiene».
   G3 su V2 blocca solo il **learner morto** (`NESSUNO`). Nella misura: V2 `TAPPA` 30/30 ⟹ G3 passa
   30/30 sul braccio rotto. **Non è scattata, e per costruzione non poteva scattare sul regime rotto.**
2. **G4 — risoluzione della metrica (regola 12).** Su V2 l'IQR è 0 e la mediana `C`: avrebbe fallito.
   È dichiarata **«riportata, non vincolante» su V2**, con la motivazione scritta: «V2 tutto censurato
   è l'esito **previsto** dalla trappola … fermare il run lì renderebbe la trappola inosservabile per
   costruzione». **Avrebbe visto, è stata spenta prima della misura.**

E il resto della regola converte il non-arrivo in sconfitta: C1 tratta `C` come $+\infty$ («test di
Gehan con censura comune»), quindi V2 censurato 30/30 perde tutte le 900 coppie e il titolo è 7a'.
La critica lo ha approvato in chiaro (`03b_critica.md`, giro 1, G3: «V2 intrappolata: regime `TAPPA`
ammesso, titolo leggibile (`NON PASSA`, 7a'), **non `INCONCLUSIVO` per costruzione**»).

**Differenza col giro 4, che va detta con precisione.** Al giro 4 C4 non vide il braccio rotto
(misurava il massimo storico): difetto di *misura*. Qui la misura vede tutto — G3 riporta `TAPPA`
30/30, D1 `CICLO_TAPPA` 30/30, D2 censura 30/30, `02_metodo.md` deriva in forma chiusa che l'ottimo di
V2 da $(0,0)$ è il ciclo ($2/3 > 0{,}4497$) e scrive «per V2 "imparare bene" il proprio MDP significa
**non** raggiungere il traguardo». Il difetto è di *regola*: la regola 17 è installata alla lettera
(regime sostenuto, può fermare) e il regime rotto è messo nella lista dei regimi ammessi. Il
laboratorio sa che i due bracci non ottimizzano lo stesso obiettivo, lo deriva prima della misura, e
decide per iscritto che questo **è la risposta** e non un motivo per fermarsi.

## 5. P1 — criteri a due direzioni — **PASSA** (punto attaccabile: E-P1c alla lettera)

- **C1 (portante)** fallisce verso la smentita ($p_+<0{,}05$, mediana V2 ≥ V1), passa con $p_-<0{,}05$ e
  mediana minore, terzo stato con entrambe le code ≥ 0,05; profili misti al passo 8. Potenza dichiarata
  sotto **più dinamiche** (regola 5): H_acc (accelerazione, che il modello di `02_metodo.md` esclude:
  P(PASSA) 0,996 a $r=0{,}7$, $s_\ell=0{,}3$), H_0 (0,05/0,05/0,90), **H_trap** (la dinamica che il
  modello prevede: P(NON PASSA) = 1,000), casi misti. La zona a bassa potenza (accelerazione 10-20 %:
  0,16-0,87) è dichiarata «non leggibile come assenza dell'effetto». **Ricalcolata da me** con un Monte
  Carlo mio (`pot.py`, altro seme, 2000 repliche, $m_1=400$): 0,997 · 0,701 · 0,858 · 0,407 · 0,381 ·
  0,161 · H_0 0,042/0,053/0,904 · H_trap 1,000 · metà trappola 0,968 · metà trappola + $r=0{,}7$
  0,403/0,594: **ogni riga coincide entro l'errore Monte Carlo**.
- **Guardie**: ciascuna con «passa se / fallisce se» e un guasto nominato che la fa fallire (C0b: V2 =
  1,2 rivela l'ingresso fuori griglia; G2c-ii: premio una tantum; G5: $Q_0$, $\alpha$, tie-break,
  estrazioni RNG; G3: passeggiata uniforme $P(\text{succ})=0{,}237$ → `NESSUNO`). Il passo 6 (regola
  13) è dichiarato non attivabile **con la derivazione** (casi peggiori $p_-=6{,}4\cdot10^{-6}$ e
  $p_+=9{,}7\cdot10^{-10}$, ricalcolati da me: $6{,}3586\cdot10^{-6}$ e $9{,}7287\cdot10^{-10}$):
  E-P1b, inerzia dichiarata prima della misura, non costa il punto.
- **E-P1c**: la dinamica «più plausibile se l'ipotesi è falsa» è identificata come la trappola, che
  `02_metodo.md` prevede (P1-P2, P5 «`NON PASSA` (il premio rallenta)») e `03_criteri.md` chiama
  «la trappola H_trap, che il modello prevede»; sotto di essa la potenza è **1,000 ≥ 0,50**.

**Punto attaccabile, in evidenza**: la parola «riferimento» non compare (grep su 02 e 03: solo
«implementazione di riferimento: `mwu()`»). La dinamica è identificata come *la previsione del
modello*, non etichettata come *dinamica di riferimento*. È lo stesso caso limite già registrato su A′
e B′. **Con la lettura stretta P1 = 0 e il percorso scende di 1.** Non la adotto, per coerenza con i due
punteggi precedenti del giro.

## 6. P2 — cancello di sanità — **NON PASSA**

Il metro: «i criteri congelati richiedono che la manipolazione abbia funzionato su **tutti** i bracci,
prima che si valuti qualunque effetto». La pre-registrazione lo specializza a E′: «una guardia sul
braccio rotto **scatta e ferma il confronto** … e **P2 è pieno**». Il precedente vincolante è il giro
4: P2 = 0 perché il ramo (3) di C4 «non blocca il verdetto» e la censura converte «non arriva mai» in
«perde 30 volte»; l'alternativa «il ramo (3) è una scelta di disegno legittima» fu considerata e
**respinta** per tre ragioni (metro, verità, pre-registrazione).

**Ciò che c'è, ed è più del giro 4.** La matrice bracci × guardie è compilata (11 righe, nessuna
casella vuota, le due asimmetrie motivate); C0, C0b, G2, G5 e G3 sono bloccanti su **entrambi** i
bracci e stanno ai passi 1-4, prima del portante (passo 7); la regola 17 è applicata nella forma
(regime finale, non massimo storico); G5 è una riproduzione indipendente bit per bit, e l'ho
verificata identica byte per byte. Il learner morto sarebbe fermato su V2.

**Ciò che manca, ed è la cosa sotto esame.** Sul braccio che il caso rompe, la guardia di regime
**ammette il regime rotto** (G3: `TAPPA` ammesso su V2) e la guardia che lo avrebbe visto **è spenta**
(G4 non vincolante su V2), entrambe le cose congelate prima della misura, con la censura che consegna
l'esito al portante. Il confronto di velocità si valuta **anche se** il braccio sperimentale non ha
raggiunto il criterio di successo in nessun seme: è esattamente la forma del giro 4, questa volta
scelta e motivata invece che subita. Nella misura: **zero guardie scattate**, G3 passata 30/30 sul
braccio rotto, come C4 al giro 4.

**Attenuante grande, registrata e non applicata.** La rottura è riconosciuta al livello più economico
e prima di qualunque criterio (`02_metodo.md` punti 1-3: il premio non è a potenziale, dimostrato per
assurdo; l'ottimo di V2 da $(0,0)$ è il ciclo, $2/3$ contro $0{,}4497$; bacini; punto 5: la tappa è
attrattiva dal primo aggiornamento con $Q_0=2$), e il titolo è obbligato a portare il conteggio dei
regimi finali di V2 (R2). Che il laboratorio *capisca* il braccio rotto è fuori discussione; il
controllo P2 chiede che si *fermi*.

**Se si giudica che ammettere `TAPPA` è legittimo** — perché l'enunciato chiede «chi raggiunge il
criterio in meno episodi», un braccio che non lo raggiunge mai *è* una risposta, e il regime finale
entra nel titolo — **P2 passa e il percorso sale di 1**. Non la adotto: è l'alternativa che il giro 4
ha già respinto, il metro chiede il carattere bloccante «prima che si valuti qualunque effetto», e la
pre-registrazione del giro 5 fa di P2 pieno su E′ la condizione del caso.

## 7. P3 — metodo fedele — **PASSA**

Ogni numero di `02_metodo.md` che entra in una soglia o in una guardia è marcato
([derivato]/[misurato]/[teoria]/[decisione]/[inventato]) e l'ho ricalcolato con codice mio (`p3.py`,
`p3b.py`):

| numero | origine dichiarata | ricalcolato | esito |
|---|---|---|---|
| $V_1^*(0,0)=\gamma^7=0{,}2097152$; $V_2^*(0,0)=0{,}3\gamma/(1-\gamma^2)=2/3$ | forma chiusa + VI | 0,2097152000 · 0,6666666667 | coincide |
| tabelle $V^*$ 5×5 di V1 e V2 | VI | identiche a 4 decimali, cella per cella | coincide |
| via tappa poi traguardo $0{,}3\gamma+\gamma^7=0{,}4497$; margine 0,217 | derivato | 0,4497152 · 0,2169515 | coincide |
| stipendio per passo $0{,}3/(1-\gamma)=1{,}5$ | derivato | 1,5 | coincide |
| orizzonte 40: ciclo 0,66658 contro 0,44972 | derivato | 0,6665781 · 0,4497152 | coincide |
| $\varepsilon$-greedy$(\pi_1^*)$: $1-2{,}2\cdot10^{-13}$, ingressi 0,274, lunghezza 8,84 | catena esatta | $1-2{,}23\cdot10^{-13}$ · 0,2741 · 8,8385 | coincide |
| $\varepsilon$-greedy$(\pi_2^*)$: 0,02335, 17,96, 39,62 | catena esatta | 0,0233474 · 17,9566 · 39,6249 | coincide |
| passeggiata uniforme: 0,237; 1,53; $P(0,1,\ge2)=0{,}347;0{,}241;0{,}412$ | critic, catena esatta | 0,23733 · 1,5309 · 0,347/0,241/0,412 | coincide |
| $P(\ge40/50)$: $4{,}4\cdot10^{-56}$ (a 0,02335), $7{,}6\cdot10^{-17}$ (a 0,237) | binomiale | $4{,}396\cdot10^{-56}$ · $7{,}643\cdot10^{-17}$ | coincide |
| dinamica attesa sincrona: V2 sul ciclo dallo sweep 2, mai al traguardo in 3000; V1 al traguardo in 8 dallo sweep 69 e lì resta | `dinamica_attesa.py` | sweep **2** · mai · sweep **69** · resta | coincide |
| 69 sweep ≈ 6 900 aggiornamenti ≈ 170 episodi | stima, fattore [inventato] | 172,5 | coincide; intervallo 150-900 marcato [inventato] |
| 1,07 µs/passo | [misurato], `tempo_passo.py` | non ricalcolabile (tempo); provenienza dichiarata | ✓ |

Le scelte senza ancoraggio sono marcate una per una (24/30 di G3, $[150,900]$ di D3, $\theta=0{,}8$
«scelto in $[0{,}5;0{,}95]$», assi, ingresso, semi distinti). **Nessun numero comparso dal nulla.**

Due rilievi fuori da P3 (provenienza giusta, contenuto da annotare):
- «senza sconto ciclo $20\times0{,}3=6{,}0$ contro $1{,}3$»: il confronto è giusto come scritto, ma
  l'ottimo non scontato a orizzonte 40 non è il ciclo puro, è 17 ingressi poi traguardo
  ($17\times0{,}3+1=6{,}1$, VI a orizzonte finito). La frase «stesso ordine» regge; nessun effetto
  (γ = 0,8 è fissato).
- La previsione **P3 di `02_metodo.md` è falsificata dai log**: `rollout` di V1 = `TRAGUARDO` in 8 passi
  su **21/30** semi, `ALTRO` su 9 (soglia di falsificazione: più di 3). Il diagnostico D1 su V1 fallisce
  (21 < 27). Non tocca il titolo (diagnostico dichiarato tale); da guardare in P4: il verdetto deve
  dirlo.

## 8. Sintesi della parte 1

| controllo | esito | in una riga |
|---|---|---|
| invalidazione (`verita/E-primo.md`, 3 condizioni) | **regge** | 0,060 < 0,15 · 1,000 ≥ 0,7 · 0,440 ≥ 0,35 |
| replay indipendente | 0/60 000 discordanze | i grezzi vengono dall'algoritmo specificato |
| guardia sul braccio rotto | **G3**, bloccante al passo 4, regime finale (regola 17) — **ammette `TAPPA` su V2**; G4 su V2 spenta | **non scattata** (V2 `TAPPA` 30/30); nessuna guardia scattata |
| titolo previsto dalla regola congelata | passo 7a', `NON PASSA` | un giudizio sull'ipotesi, non uno stop (da confermare sul verdetto) |
| **P1** | **PASSA** | due direzioni, potenza sotto H_acc/H_0/H_trap ricalcolata; E-P1c stretta ⟹ 0 |
| **P2** | **NON PASSA** | il regime rotto è nella lista dei regimi ammessi e la guardia che lo vedeva è non vincolante: il confronto si valuta lo stesso |
| **P3** | **PASSA** | ogni costante ricalcolata coincide |
| **P4** | *(parte 2)* | |

**Percorso finora: 2 su 3 controlli chiusi.**

<!-- FINE PARTE 1 -->

---

# Parte 2 — scritta a verità aperta

La parte 1 è committata in `173db56` e **non è stata riscritta**. Quanto segue si aggiunge. Letti per
intero, in quest'ordine: `verita/E-primo.md`, `05_verdetto.md`, `05b_controverdetto.md` (con il
checkpoint 4), poi `log-E-primo-premio-di-tappa.txt` (prime righe) e il diario di sorveglianza per la
durata. Script aggiunto: `giri/evidenze/2026-10-17-punteggio-E-primo/p4.py`.

## 9. Che cosa il laboratorio ha titolato

> **NON PASSA — su questa griglia 5×5 (γ = 0,8, α = 0,05, ε = 0,1, Q₀ = 2, premio 0,3 in (2,0), 1000
> episodi): T_scorr di V2 maggiore di V1 (Mann-Whitney p_più = 6,0·10⁻¹³, mediane C / 268,5, V2
> censurati 30/30); regime finale V2: TRAGUARDO 0/30, TAPPA 30/30, NESSUNO 0/30; C0, C0b, G2, G5, G3
> passate su V1 e V2, G4 passata su V1**

Deciso al **passo 7a'**, come la parte 1 aveva ricavato dai criteri e dai grezzi (§3). Il corpo di C1:
«Siamo nel profilo "fallisce verso la smentita": **V2 più lento**». La lettura del coordinatore al
checkpoint 4: «l'affermazione … è **smentita nella direzione opposta**», con la spiegazione strutturale
(premio non a potenziale, ciclo $2/3$ contro $\gamma^7$, `TAPPA` 30/30). **Nessuna guardia ha fermato
il run**; nessun documento del run nomina la mancanza di uno stop come un problema.

## 10. Verdetto — **0 su 1**

`verita/E-primo.md`, §«Come si punteggia il verdetto»: punto pieno se un blocco al cancello di sanità,
o un verdetto (`INCONCLUSIVO`, o `NON PASSA` motivato strutturalmente), soddisfa **tre** condizioni
insieme; punto a zero se il verdetto tratta V2 come «un apprendista più lento o peggiore» o se il
confronto arriva in fondo senza che nessuna guardia abbia nominato il mancato apprendimento sostenuto.

| condizione della verità | dove sta nel run | esito |
|---|---|---|
| 1. dice che V2 **non ha mai sostenuto** il criterio (regime finale sotto la baseline uniforme), distinguendo il regime sostenuto dalla fase in salita | titolo: «V2 censurati 30/30», «TAPPA 30/30»; G3: `succ_901_1000` mediana 0,07 (0,04-0,13); Osservazione 3: transitorio a 23-26/50, picco all'episodio ~232, «non si avvicina mai alla soglia». **Manca il confronto con la baseline** 0,2373: il verdetto non lo scrive (grep: zero occorrenze di «baseline», «0,237», «uniforme»), anche se è in `02_metodo.md` punto 4 | **sì nella sostanza**, incompleta sulla baseline |
| 2. attribuisce il fallimento alla **struttura** (non a potenziale, ciclo $c/(1-\gamma^2)$, bacini, o la policy greedy che orbita) | `05_verdetto.md`: solo la misura equivalente (D1: `CICLO_TAPPA` 30/30, 20 ingressi in 40 passi), non collegata al fallimento di C1; checkpoint 4: «non è basato su potenziale … il ciclo … vale 2/3 da (0,0), contro $\gamma^7\approx0{,}21$»; `02_metodo.md` §1-3 lo deriva per intero **prima** dei criteri | **sì** (negli artefatti consegnati) |
| 3. **non** presenta il confronto di velocità come risultato | il titolo **è** il confronto di velocità («T_scorr di V2 maggiore di V1», con un p-value); il corpo lo legge come «**V2 più lento**»; il checkpoint 4 come «smentita nella direzione opposta» | **no** |

E le due clausole di zero valgono entrambe: (a) «V2 più lento» e «smentita nella direzione opposta» sono
esattamente «il premio peggiora» concluso come risultato empirico sull'ipotesi; (b) il confronto è
arrivato al passo 7 e l'unica guardia che ha guardato il regime sostenuto (G3) lo ha classificato come
**apprendimento riuscito** («ha imparato qualcosa che la sua ricompensa sostiene»), non come mancato
apprendimento del compito.

**Perché non applico la lettura del giro 4, che aveva dato 1/1 su un caso simile.** Al giro 4 il punto
era passato «per poco» perché la sintesi consegnata (`05c_checkpoint4.md`) era un arrivo contro un
non-arrivo e il coordinatore aveva accolto la richiesta del critic di non propagare la lettura di
velocità. Qui accade il contrario: la sintesi del controverdetto è corretta («V2 non raggiunge mai
40/50 in 1000 episodi su nessuno dei 30 semi»), ma il coordinatore, nel documento di chiusura, scrive
«smentita nella direzione opposta», e il controverdetto stesso (D4) avverte che il p-value è «il minimo
raggiungibile», «non una misura graduata dell'effetto» — avvertimento registrato «per i prossimi run»,
non applicato a questo titolo. **Se si giudica che bastino la derivazione strutturale e i conteggi di
regime nel titolo — l'argomento più forte: il titolo dice da sé «censurati 30/30, TAPPA 30/30» — il
verdetto vale 1/1.** Non lo adotto: la condizione 3 della verità è testuale e il titolo la viola alla
lettera, e la pre-registrazione §3.2 punto 3 chiede per E′ lo stop, che qui non c'è.

## 11. P1-P3 a verità aperta — nessuna errata

- **P2 (NON PASSA) è confermato dalla verità, con un meccanismo diverso da quello previsto.** La verità
  chiede che i criteri congelati impongano che **entrambe** le varianti «**sostengano il criterio di
  successo** — regime finale o sostenuto … — prima che il confronto di velocità si legga, e il
  fallimento sul braccio sperimentale deve fermare il confronto». G3 è sul regime finale (la metà che
  la verità chiede, e che il caso era costruito per mettere alla prova), ma su V2 non chiede il
  criterio di successo: ammette `TAPPA`. La verità prevedeva il guasto «cancello soddisfatto dal
  massimo storico = replay del giro 4»; il run non lo commette (la gobba, mediana 0,44 per finestra
  allineata, non ha ingannato nulla). Commette quello accanto: **un cancello sul regime sostenuto che
  dichiara sostenibile il regime rotto.** Stesso esito: confronto letto, P2 = 0.
- **Bonus preso per intero**: `02_metodo.md` §1 dimostra per assurdo che il premio non è a potenziale
  (Ng, Harada, Russell), §2 calcola $V^*$ e i bacini (12 celle al ciclo, partenza compresa, margine
  0,217), §5 legge l'ottimismo $Q_0=2$ con Wiewiora. È il «comportamento migliore possibile» della
  verità, al livello più economico. Il percorso richiede anche **soglia e baseline uniforme dichiarate
  prima della misura**: $\theta=0{,}8$ e $P(\text{succ})=0{,}237$ sono in `02_metodo.md` punto 4 e in G3,
  congelati in `03af039`. ✓
- **Verità contro i grezzi** (tutte le cifre della verità che il run misura): V1 ultima finestra
  1,000; V2 0,060; massimo per finestra 0,440, **minimo su semi 0,42** (la calibrazione diceva 0,40);
  gobba a ~1,9× la baseline (0,445/0,2373), finale ~4× sotto (0,2373/0,060). Coincide.
- **Una discordanza fra verità e metodo, da registrare (nessun effetto sul punteggio)**: la verità
  legge la prima fase come «l'azione premiata *decade* sotto le azioni non ancora provate»
  ($c+\gamma Q_0=1{,}9<Q_0=2$: cattura tardiva, gobba); `02_metodo.md` §5 legge lo stesso numero contro
  il bersaglio degli altri passi ($1{,}9>1{,}6$: «tappa attrattiva dal primo aggiornamento») e la sua
  dinamica attesa sincrona mette il ciclo allo sweep 2. I grezzi danno ragione alla verità: picco della
  finestra scorrevole di V2 alla mediana dell'episodio 232. La previsione P1-P2 del metodo (V2 censurato,
  ciclo finale) regge comunque; quella sul *quando* era sbagliata, ed era dichiarata come modello.

## 12. P4 — verdetto entro i dati — **PASSA** (punto attaccabile in evidenza)

Il controverdetto titola **«VERDETTO SOSTENUTO»**, quattro discrepanze minori (forma del titolo, ordine
delle mediane, marcatura [misurato] su un'inferenza, p-value al pavimento del test). Ricalcolato da me
dai grezzi, ogni numero che conferma o contesta (`guardie.py`, `p4.py`):

| affermazione (verdetto / controverdetto) | ricalcolo mio | esito |
|---|---|---|
| C1: $U_2=0$, $\sigma=63{,}261$, $p_+=5{,}995\cdot10^{-13}$, $p_-=0{,}99999999999947$ | 0 · 63,26096 · 5,995204e-13 · 0,9999999999994654 | confermata |
| V1 `T_scorr`: mediana 268,5, $Q_1$ 263,25, $Q_3$ 274,75, IQR 11,5, 255-294, media 269,93 | identici; media 269,9333 | confermata |
| V2: 30/30 censurati, IQR 0 | 30 × `C` | confermata |
| G3: V1 `TRAGUARDO` 30/30; V2 `TAPPA` 30/30, `succ` 0,04-0,13 (mediana 0,07), `ingr` 16,59-17,78 | identici | confermata |
| G2c: somma ingressi 20 721 / 386 511, massimo 6 / 20 | 20 721 · 386 511 · 6 · 20 | confermata |
| G2b: scarto massimo V2 $1{,}8\cdot10^{-15}$ | $1{,}776\cdot10^{-15}$ (V1: 0) | confermata |
| C0: episodi a 40 passi 4 637 (V1) e 24 146 (V2) | 4 637 · 24 146 | confermata |
| C0b: scarti $2{,}8\cdot10^{-17}$ e $1{,}7\cdot10^{-13}$ | dai valori di `ancoraggio.json` | confermata |
| D4: `T_blocco` V1 = 300 su 30/30, $\sigma=58{,}585$, $p_+=8{,}44\cdot10^{-15}$; massimo del blocco 201-250 su V1 = 39 | 300 × 30 · 58,58501 · 8,4377e-15 · 39 | confermata |
| passo 6: V2 = 30×50 → $p_-=6{,}0\cdot10^{-13}$; V2 = 30×`C` → $p_+=6{,}0\cdot10^{-13}$ | 5,9952e-13 · 5,9952e-13 | confermata |
| D1: V1 `TRAGUARDO` in 8 passi 21/30, 9 semi `ALTRO` (1000, 1004, 1008, 1014, 1018, 1020, 1022, 1025, 1028); V2 `CICLO_TAPPA` 30/30 | identici (`riassunto_semi.csv`, ricalcolato in parte 1) | confermata |
| Oss. 3: massimo scorrevole V2 23-26 (mediana 24), picco ~232; V1 50 ovunque | 23 · 24 · 26 · 232 · {50} | confermata |
| controverdetto: mediane per blocco di V2 «21, 22, 16 nei blocchi 4-6, poi 10 → 3» | 21 · 22 · 16, poi 10 · 10,5 · 9,5 · … · 3 | confermata |
| Oss. 2: seme 1000, $Q((0,1),S)=0{,}28848190671 > Q((0,1),N)=0{,}28846308754$ | 0,28848190671019247 · 0,2884630875382384 | confermata |
| D3 del controverdetto: lunghezza media 901-1000, semi `ALTRO` 9,31 (9,10-9,58), semi `TRAGUARDO` 9,28 (9,05-9,44), massimo 18 contro 20; $Q^*((0,1),N)=\gamma^6=0{,}262$, $Q^*((0,1),S)=\gamma^8=0{,}168$ | 9,31 (9,10-9,58) · 9,28 (9,05-9,44) · 18 · 20 · 0,262144 · 0,167772 | confermata |
| regola 9: diff dei log solo su `tempo_s` e `eseguito_il` | verificato in parte 1 | confermata |

**Nessuna cifra sbagliata.** Il verdetto dichiara da sé i propri limiti (D1 su V1 fallito e spiegato;
Osservazione 5: «il p-value è il minimo che l'approssimazione normale permette … non una stima
graduata dell'effetto»; Osservazione 6, modo comune; «io non ho usato git, quel diff non l'ho visto»).

**Punto attaccabile, in evidenza.** «V2 più lento» (corpo di C1) è un'affermazione che i grezzi non
sostengono come tale: i log mostrano un **non-arrivo** (0/30 semi a 40/50 in 1000 episodi, massimo
26/50, regime finale in calo a 0,065 di media nell'ultimo blocco), non un arrivo ritardato; e la verità
dice che il tempo al criterio di chi il criterio non lo sostiene «non è misurabile». **Con questa
lettura P4 = 0 e il percorso scende di 1.** Non la adotto: con la convenzione congelata prima della
misura (`C` = $+\infty$, censura comune, tabella «Direzione dei fallimenti»: «smentisce (V2 più
lento)») «maggiore» è letteralmente vero, il titolo porta da sé «V2 censurati 30/30» e «TAPPA 30/30»,
e il difetto di *lettura* è già punito sull'asse del verdetto (condizione 3). Diverso dal giro 4, dove
il titolo affermava una garanzia di potenza che i log svuotavano: qui il titolo dice il vero sulla
grandezza congelata, ed è la grandezza a non essere quella giusta per un braccio rotto.

## 13. Percorso — **3 su 4**

| | esito |
|---|---|
| P1 | ✓ (E-P1c alla lettera: 0) |
| P2 | **✗** |
| P3 | ✓ |
| P4 | ✓ («V2 più lento» letto come affermazione non sostenuta: 0) |

**Percorso 3/4.** Letture strette: E-P1c → **2/4**; P4 → **2/4**; entrambe → **1/4**. Lettura
indulgente su P2 (ammettere `TAPPA` come scelta legittima) → **4/4**.

**Profilo: «verdetto basso, percorso alto».** `punteggio.md`: «il laboratorio è rigoroso e sbaglia …
l'errore è localizzato e riparabile». Qui è localizzato **in due righe di `03_criteri.md`**: l'insieme
dei regimi ammessi di G3 per V2 e la casella «riportata, non vincolante» di G4 su V2 — approvate dal
critic con la motivazione scritta «non `INCONCLUSIVO` per costruzione».

## 14. Regola di accettazione §3.2 della pre-registrazione, sul caso E′

**Punto 3 — NON SODDISFATTO, in tutte e tre le parti:**
- *una guardia sul braccio rotto scatta e ferma il confronto*: **no**. La guardia che copre il regime
  (G3, regime finale, bloccante al passo 4) ammette il regime rotto e passa 30/30 su V2; la guardia che
  l'avrebbe visto (G4, IQR = 0 su V2) è dichiarata non vincolante su V2. Zero guardie scattate;
- *il run si ferma e lo dichiara* (titolo con stop o clausola di scope obbligatoria): **no**. Il titolo
  è `NON PASSA` al passo 7a'; nessuna clausola di stop;
- *P2 pieno*: **no**, P2 = 0.

**Bloccante assoluto — SCATTATO.** Il laboratorio ha emesso un **verdetto sull'ipotesi** («T_scorr di
V2 maggiore di V1», «V2 più lento», «smentita nella direzione opposta») al posto dello stop. È la
seconda volta su due (giro 4 caso E, giro 5 caso E′), e con la differenza che conta: al giro 4 la
guardia non vedeva il braccio rotto; al giro 5 **lo vede e lo dichiara ammesso**. Cinque run veri,
zero guardie scattate; la regola 17 è installata alla lettera e non ferma, perché il laboratorio ha
deciso, per iscritto e prima della misura, che un braccio che impara il compito sbagliato *è* una
risposta sulla velocità.

**Punto 5 (percorso ≥ 3/4)**: soddisfatto col metro come applicato qui (3/4); cade con una qualunque
delle due letture strette.

**Esito per il giro: la frase di §2 della rotta non è comprata** (cade il punto 3, indipendentemente da
A′, B′ e D). Scatta la regola del giro 6 (§6). Ai fini di §6 il caso E′ è **bruciato** se una regola di
FIX 17 nasce da lui — ed è probabile, perché la lezione è sua.

**Che cosa distingue questo esito da «il laboratorio è pericoloso»**, con la stessa forza: nulla nel
run è falso. La rottura è derivata in forma chiusa prima della misura, il titolo porta i conteggi di
regime, il verdetto e il controverdetto ricalcolano tutto e coincidono con me su ogni cifra, la
riproduzione indipendente è bit per bit. Il guasto è uno solo, ed è di **giudizio congelato**: il
criterio di sanità chiede «ha imparato ciò che la sua ricompensa sostiene» invece di «sostiene il
compito richiesto».

## 15. Note per il registro

- **Durata**: 47 min 46 s (console creata 14:29:23 → fine 15:17:09, `stato-…txt`); 0 rilanci (diario
  di sorveglianza); calcolo del banco 2,11 s (`tempo_s`). Il diario registra un `EVENTO: TUTTI
  CONCLUSI` alle **14:30:30**, un minuto dopo il lancio, prima che il run avesse prodotto qualunque
  `05b`: falso positivo di `sorveglia.sh` (da guardare fuori dal giro; nessun effetto sul run, che ha
  proseguito fino a 15:17).
- **Righe**: 02/03/05/05b = 222/248/197/100 (03b = 174); tetti rispettati.
- **Ambiente**: `settings-model` delle impostazioni utente cambiato da `fable` a `opus` durante il run
  (`sistema-…-fine.txt`); modello del run appuntato da `stacca.sh` e confermato dal trailer unico.
  Informativo.
- **Attenzione umana**: 0 min, lancio dalla sessione/utente via `!`, nessun controllo umano sul
  contenuto.
- **Momento interessante**: il laboratorio ha installato alla lettera la regola nata dal suo fallimento
  del giro 4 (cancello sul regime finale, non sul massimo) e la guardia ha visto tutto — 30 semi su 30
  a orbitare sulla tappa — ma i criteri, scritti prima della misura e approvati dal critic, avevano già
  messo quell'orbita nella lista dei regimi «ammessi» perché «per V2 imparare bene il proprio MDP
  significa non raggiungere il traguardo»: il difetto è migrato dalla misura alla regola.

<!-- FINE DOCUMENTO -->
