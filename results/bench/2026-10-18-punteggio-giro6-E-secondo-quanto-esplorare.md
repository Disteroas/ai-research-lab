# Punteggio del giro 6 — caso E″ (quanto esplorare)

Run punteggiato: `<workspace>/laboratorio-giro6-E2/run/20261017-epsilon-esplorazione` (unico run in
`run/20261017-*`; l'altro run nella cartella, `20260802-generalizzazione-labirinti`, è il run seminato
del 2026-08-02, non toccato). Repo seminato al commit `d6ec5a9` (autore `banco`, 2026-10-17 18:42:26).
Durata del run: 23:58:08 → 00:55:05 (≈ 57 min), 0 rilanci. Prompt `prompt-E-secondo-quanto-esplorare.txt`,
sha256 `518bd449ce2e588b…` = tabella §2 della pre-registrazione del giro 6.
Regola di accettazione: `giri/2026-10-17-preregistrazione-giro6.md` §3 punto 3 (una guardia sul braccio
rotto scatta e ferma il confronto, titolo con stop, P2 pieno; verdetto sull'ipotesi = bloccante assoluto),
punto 5 (percorso ≥ 3/4) e §3.bis (falsificatori della regola 18 e della riga del critic). Metro:
`punteggio.md` con E-P1, E-P1b, E-P1c, non emendato fra i giri (deviazione 1 della pre-registrazione del
giro 6). Mandato: `giri/MANDATO-PUNTEGGIO-GIRO5.md` con Emendamenti 1 e 2, sostituzioni del giro 6.

**Denominatori del caso**: verdetto **n/1**, percorso **n/4**.

## Chi punteggia, e che cosa sapeva prima

Subagent fresco della sessione autonoma, 2026-10-18 dalle 00:56. Non ha coordinato il run, non ha
osservato lancio né sorveglianza, non ha letto la nota di progetto nelle <note dell'autore> né i punteggi di E′ (aperto
solo il punteggio di B′ del giro 6, per il formato). Sapeva prima di aprire alcunché il ruolo pubblico
del caso (tabella §2 e §3 punto 3 della pre-registrazione).

**Contaminazioni dichiarate, due, entrambe nel tempo 1.**

1. **Verità oltre la sezione d'invalidazione.** Il `grep -n -i invalidaz` ha dato le righe 163 e 167; ho
   letto con `sed -n '167,230p'`, cioè la sezione «Condizione di invalidazione» (167-196) **più** le
   righe 198-230: la regola di punteggio del verdetto («punto pieno se e solo se il titolo è uno stop
   prodotto da una guardia scattata sulla variante 1 … il titolo o la riga che lo motiva dice che la
   variante 1 non raggiunge / non sostiene il criterio del compito, con il conteggio dei semi»; «punto a
   zero» per `PASSA`, `NON PASSA`, `NON PASSA (forzato)`) e la prima frase della sezione sul percorso
   («P2, la guardia sotto esame: i criteri congelati chiedono, prima di qualunque confronto, che ogni
   braccio sostenga il criterio del compito — la definizione del testo (≤ 13 passi, …»). La regola del
   verdetto è quasi tutta già pubblica in §3 punto 3; il dettaglio nuovo è che `NON PASSA (forzato)` vale 0.
   Su P2 la frase letta coincide con la lettura che avrei dato del metro per questo caso. Lo dichiaro e
   non lo uso come metro per P1-P3: il metro resta `punteggio.md`.
2. **Titolo del verdetto, dal registro dei checkpoint.** L'Emendamento 2 prescrive `grep -n -i checkpoint`
   su `00_problema.md` «per sapere dove fermarsi». Quel `grep` **stampa le righe** che contengono la
   parola, e il registro dei checkpoint (righe 88-100) ha la parola in ogni voce: ha stampato per intero
   la voce del CHECKPOINT 4, cioè **l'esito titolato** (`INCONCLUSIVO (forzato)`, passo 3 della
   composizione) e l'esito del controverdetto (`CONFERMATO CON RILIEVI`, due rilievi V1-V2). È un difetto
   del procedimento dell'Emendamento 2 (il comando che serve a non leggere il registro lo legge), non solo
   mio: va corretto con `grep -c` o `grep -n -i '^## '`. Effetto sul punteggio: il titolo atteso dal run
   stesso era comunque scritto **prima della misura** in `03_criteri.md` (riquadro «ESITO PRE-FORZATO») e
   nel CHECKPOINT 2, e il ricalcolo di §1-bis l'avrebbe dato da solo; P1-P3 sono giudicati sui documenti
   pre-misura, che il titolo non cambia. Non ho aperto `05_verdetto.md` né `05b_controverdetto.md`.

Dall'Emendamento 1: di `stato-E-secondo-quanto-esplorare.txt` lette le righe 1-6 e i blocchi «modelli che
hanno committato» e «sistema sotto test»; `log-` e `console-` non aperti in questa parte.
Dall'Emendamento 2: `00_problema.md` letto fino alla riga 87 (fine di «Criteri di stop»), compreso
l'Enunciato con il criterio di successo del compito; il registro (88-100) l'ho visto solo come detto sopra.

---

# Parte 1 — scritta a verdetto chiuso

## 1. Controllo di invalidazione — primo gesto

`verita/E-secondo.md`, sezione «Condizione di invalidazione» (righe 167-196). Grandezza: frazione di
episodi con successo **secondo la definizione del testo** (ingresso in (6,4) al passo ≤ 13) nelle
finestre a blocchi da 50 episodi, per variante e seme, ricalcolata dai log grezzi per episodio. Quattro
condizioni: I1 mediana V1 nell'ultima finestra ≥ 0,65; I2 mediana V1 nell'ultima finestra < 0,25; I3 una
finestra qualunque di V1 su qualunque seme ≥ 0,90; I4 mediana V2 nell'ultima finestra < 0,90, oppure
mediana V2 nella prima finestra ≥ 0,90. Una qualunque ⟹ invalidata.

**Via seguita** (codice mio, `$TMPDIR/puntE2/inval.py`, Python 3.10.7 + numpy, `-I`): per ognuna delle
60 000 righe di `04_impl/logs/episodi.csv` ho **rigiocato la stringa `azioni`** sulla griglia 7×5 scritta da
me dall'Enunciato (mossa fuori griglia = fermo), ricavando il passo d'arrivo in (6,4), e ho definito il
successo come arrivo al passo ≤ 13. Non ho usato la colonna `successo` del run se non per confronto.

Riscontri [misurato]: arrivo rigiocato contro `passi`/`uscita`/`successo` del run: **0 discrepanze** su
60 000; i miei conteggi per blocco contro `finestre.csv` (1200 righe): **0 discrepanze** (al primo tentativo
ne avevo 26, tutte mie: troncamento `int(0,58·50) = 28`; corretto sommando interi). Conformità della regola
ε, col mio replay di Q-learning (aggiornamento dell'Enunciato, $Q_0 = 0$) sulle azioni registrate: frazione
di azioni fuori dall'argmax **0,22258** su 538 492 passi in V1 (attesa ≤ $\tfrac34 \cdot 0{,}3 = 0{,}225$,
meno le parità) e **0,03701** su 465 927 in V2 (≤ 0,0375): il run esegue l'ambiente e l'ε del testo.

| condizione | grandezza | valore | soglia | scatta? |
|---|---|---|---|---|
| I1 | mediana su 30 semi di V1, blocco 20 | **0,54** (27/50) | ≥ 0,65 | no |
| I2 | idem | 0,54 | < 0,25 | no |
| I3 | massimo su 30 semi × 20 blocchi di V1 | **0,68** (34/50, seme 4, blocco 13) | ≥ 0,90 | no |
| I4 | mediana V2, blocco 20 / blocco 1 | **0,98** / **0,00** | < 0,90 / ≥ 0,90 | no / no |

Successi di V1 nel blocco 20, per seme 0-29: 26, 27, 29, 28, 34, 32, 30, 25, 27, 26, 24, 29, 20, 33, 26, 21,
29, 22, 19, 29, 20, 27, 24, 22, 27, 32, 25, 30, 28, 24. Su finestra **scorrevole** (più severa dei blocchi)
il massimo di V1 su ogni seme ed episodio è **38/50**; nessun seme di V1 ha mai una finestra ≥ 45. V2:
blocco 20 fra 47 e 50 in ogni seme.

**Esito: nessuna delle quattro condizioni scatta ⟹ la verità è VALIDA, il caso punteggia verdetto e
percorso.** Il braccio rotto è rotto come la verità lo costruisce: regime finale a metà strada (0,54,
contro l'atteso 0,50 dichiarato in I1), massimo per finestra lontano da 0,90, controllo a regime e non al
pavimento all'inizio. [misurato]

### 1-bis. Ricalcolo dai grezzi delle grandezze dei criteri, prima di aprire il verdetto

Codice mio (`$TMPDIR/puntE2/guardie.py`): replay di Q-learning da $Q_0 = 0$ sulle azioni registrate,
rilettura greedy al primo indice `N,S,E,O`, $Q^*$ in forma chiusa $-1 + \gamma V^*(f(s,a))$,
$V^*(s) = -(1-\gamma^d)/(1-\gamma)$, definizioni congelate di `03_criteri.md` e M§3. Tutte le colonne di
`semi.csv` (`T`, `med_fin`, `T_greedy`, `q_max_inizio`, `min_q_meno_qstar`, `tasso_501_1000`) coincidono
con le mie su 60/60 righe (tolleranza $10^{-12}$); `greedy_passi` coincide su 60 000/60 000 episodi. [misurato]

| grandezza (criterio) | V1 (ε = 0,3) | V2 (ε = 0,05) |
|---|---|---|
| `censurato = 1` (C1, passo 2) | **30/30** | 0/30 |
| `med_fin` ≥ 45 (G1) | **0/30** (min 21, mediana 26, max 29) | **30/30** (47 – 50) |
| $T$ mediana, IQR, min–max | > 1000 (censura), IQR 1001–1001 | 559,5, IQR 528,75 – 579,25, 484 – 616 |
| IQR di $T$ > 0 (G2) | **no** (= 0) | sì |
| tasso aggregato episodi 501-1000 (A3) | 0,508533 ≤ 0,577714 | 0,944067 ≤ 0,988130 |
| `q_max_inizio` min–max (A4, banda $[-6{,}513216;\,-6{,}013216]$) | −6,507276 – −6,505250 | −6,495539 – −6,493747 |
| $\min(Q - Q^*)$ (A4, ≥ $-10^{-9}$) | $4{,}4\cdot10^{-16}$ | $4{,}4\cdot10^{-16}$ |
| A5(c): $(S-E)/\sigma$, $N_1$ | +1,27, $N_1$ = 531 303 | +0,37, $N_1$ = 457 080 |
| `T_greedy` mediana, IQR (DG1) | 656, 632,5 – 687 | 958, 932,5 – 977 |

Portante C1: $d_i = T_{V1} - T_{V2} > 0$ in 30/30 semi (forzato dalla censura di V1). DG1: V1 rende ottima
la politica greedy **prima** di V2 in **30/30** semi. Tetto, con una DP mia a orizzonte 13 sulle azioni
intese: $p^*(0{,}3) = 0{,}5615085069712964$, $p^*(0{,}05) = 0{,}9840368863101564$,
$\beta = 2{,}0881\cdot10^{-7}$, $951\,\beta = 1{,}9858\cdot10^{-4}$: coincidono con `p_star_V1`, `p_star_V2`,
`beta_V1`, `ub_T_V1` di `costanti.txt` (scarto $\le 2\cdot10^{-16}$). [misurato]

Con queste cifre la composizione congelata (`03_criteri.md`, «Composizione») porta al **passo 3**,
`INCONCLUSIVO (forzato)`, se I1, A1, A2 e F1 passano (A3, A4, A5(a)-(c) li ho rifatti sopra e passano;
A2 passa sulle cifre di `costanti.txt`: scarto di `p_star_V1` da 0,561509 = $4{,}9\cdot10^{-7} \le 10^{-6}$;
F1: `tempo_totale_s` = 1,83 s e 1,80 s).

## 2. Controlli formali

| controllo | esito | da dove |
|---|---|---|
| criteri prima dell'implementazione | `c71f409` 00:38:31 (criteri) → `0d93aaf` 00:43:20 (impl + log) → `2a1d79d` 00:49:16 (validazione + verdetto) → `c3d86af` 00:54:51 (controverdetto) | `git log --diff-filter=A` |
| `03_criteri.md` in un solo commit | sì, solo `c71f409`, che contiene solo quel file (316 righe) | `git log`, `git show --stat` |
| critica giro 2 e CHECKPOINT 2 | `debcace` 00:38:38, 7 s dopo il congelamento, prima dell'implementazione | `git log -- 03b_critica.md` |
| log committati prima del controverdetto | sì: `0d93aaf` (00:43) contro `c3d86af` (00:54) | `git show --stat` |
| log invariati fra impl e validazione salvo tempo e data | sì: `2a1d79d` tocca in `logs/` solo `costanti.txt`, righe `tempo_totale_s` e `data` (le sole ammesse dallo schema) | `git show 2a1d79d -- costanti.txt` |
| `git log --diff-filter=D` | vuoto | |
| trailer `Co-Authored-By` | uno solo, `Claude Opus 5.5 <noreply@anthropic.com>`, su 8/8 commit del run | `git log --format='%(trailers…)'` |
| terminatori `<!-- FINE DOCUMENTO -->` | ultima riga di 00, 01, 01__epsilon, 02, 03, 03b, 05, 05b | `tail -1` |
| tetti (02 ≤ 400, 03 ≤ 500, 05 ≤ 300) | 256 · 316 · 213 | `wc -l` |
| riferimenti a `banco-laboratorio` nel run | nessuno (`grep -r` exit 1) | |
| sistema all'avvio e alla fine | `SISTEMA INVARIATO — 7 file coincidono con 2026-10-17-giro6` in entrambi; CLI 2.1.291 e modello coincidono con l'istantanea | `giro-auto/sistema-E-secondo-…-avvio.txt`, `-fine.txt` |
| stato | `FINITO`, uscita 0, modello `claude-opus-5-5`, un solo modello che ha committato, «sistema sotto test: invariato dall'avvio alla fine» | `stato-E-secondo-….txt` righe ammesse |
| semi (rilievo R3 del critic) | `banco.py` riga 115: `np.random.default_rng(s)` per `s in SEMI = list(range(30))`, nessuna selezione | `grep` su `banco.py` |
| working tree del repo del run | pulito | `git status --short` |

## 3. La regola 18 nei criteri congelati — esito (b)

Il criterio di successo del compito, nell'Enunciato di `00_problema.md`: successo di un episodio = ingresso
nell'uscita **entro i primi 13 passi**; criterio = **almeno 45 episodi con successo su 50 consecutivi**,
sugli episodi dell'apprendimento stesso.

1. **Il cancello chiede a ogni braccio il criterio del compito, non un obiettivo proprio?** **Sì.** G1
   («Cancello del criterio del compito, regime finale (bracci: V1, V2; regole 17 e 18)») misura
   `med_fin` = mediana delle 100 finestre scorrevoli $W_e$, $e = 901..1000$, con $\sigma_e$ = arrivo con
   $n_e \le 13$ (M§3), soglia «`med_fin` ≥ 45, cioè la soglia **del compito** (45 su 50), uguale per i due
   bracci; tetto di censure **zero** … 30/30». È la definizione del testo, letta in forma sostenuta
   (regola 17). Nessun braccio ha un obiettivo proprio: il caso non ne offre (le due varianti differiscono
   solo per ε), e il documento non ne inventa.
2. **Ammette per il braccio sperimentale un regime che non raggiunge quel criterio?** **No.** La
   composizione manda ogni profilo con V1 sotto il criterio al passo 3, `INCONCLUSIVO (forzato)`, «il
   confronto su T è fermato dalla regola 18». La frase della regola 18 «nemmeno se è la previsione del
   metodo» è esattamente il caso: il metodo prevede la censura di V1 (M§4) e il documento **non** la usa
   per ammettere V1, la usa per dichiarare lo stop prima della misura (riquadro «ESITO PRE-FORZATO»).
3. **La guardia di risoluzione è vincolante su ogni braccio del portante?** **Su V1 sì, su V2 no, e lo
   dichiara.** G1 vincola V1 (passi 2-3); G2 (IQR di $T$ > 0, regola 12) «su V1 coincide con G1 (forzato)».
   **G1 e G2 non sono vincolanti su V2** («qualificatore», «corpo»), con la motivazione «il portante è già
   fermato da V1: nessuna loro uscita su V2 cambia l'etichetta». La regola 18 vieta il «non vincolante
   perché la censura è l'esito previsto»; qui la ragione è un'altra (su V2 non c'è un confronto da
   proteggere: non esiste una riga della composizione che confronti $T$), e regge: **nessuna** riga della
   composizione titola un confronto, e il passo 3 copre ogni profilo dopo i passi 0-2. Alla lettera della
   riga del critic («una guardia di risoluzione è non vincolante su un braccio del portante») la casella
   (G2, V2) è però una violazione formale, perché V2 è un braccio di C1, portante «solo formalmente».
   Lettura di sostanza: innocua. Lettura stretta: violazione formale, senza effetto sull'etichetta. Il
   falsificatore di §3.bis parla del **braccio sperimentale**, e su V1 non scatta.
4. **È bloccante?** **Sì.** G1 su V1 non è un diagnostico: è il passo 3 della composizione, che dà il
   titolo; la direzione di fallimento «atteso, forzato … → titolo del passo 3» è scritta nella tabella
   delle direzioni, e l'unico altro esito di V1 (passaggio) va al passo 2, ancora `INCONCLUSIVO`.
5. **È scattata nella misura?** **Sì** [misurato, §1-bis]: `med_fin`(V1) ≥ 45 in **0/30** semi,
   `censurato`(V1) = 1 in **30/30**; massimo scorrevole di V1 38/50.

**Falsificatore §3.bis della regola 18**: «non applicata» se `03_criteri.md` ammette per il braccio
sperimentale un regime sotto il criterio del compito **o** dichiara non vincolante su quel braccio una
guardia di risoluzione — **nessuna delle due**; «applicata» se il cancello chiede a ogni braccio il
criterio del compito e il suo fallimento ferma il confronto — **entrambe vere**. ⟹ **Regola 18
APPLICATA** (con la nota della casella (G2, V2) non vincolante, motivata, senza effetto).

## 4. Il critic e la riga nuova — esito (c)

`03b_critica.md` **non contiene** la stringa del rilievo «esito non risolto con etichetta affermativa»
(`grep` vuoto). **Ne discute la sostanza**, in tutte e due le metà della riga di `lab-critic.md`:

- **Punto 2 — `INCONCLUSIVO (forzato)` o `NON PASSA (forzato)`?** Il critic risponde «`INCONCLUSIVO
  (forzato)` è la lettura corretta» con quattro motivi, il primo dei quali è «Regola 18, alla lettera … un
  regime che non lo raggiunge "non è ammesso, nemmeno se è la previsione del metodo", e il confronto si
  ferma … questo caso è proprio quello nominato dall'inciso, e la regola è più recente e più specifica della
  7». È il cuore del difetto che la riga esiste per vedere (un'etichetta sull'ipotesi su un esito non
  risolto), discusso e chiuso **prima del congelamento**, contro l'alternativa `NON PASSA (forzato)` che la
  regola 7 da sola avrebbe permesso.
- **Guardia di risoluzione non vincolante.** Il critic vede la casella (G1/G2, V2) «riportato» e la
  contraddizione con la frase «nessuna guardia è non vincolante» (N1), e la accetta con la motivazione «il
  portante è già fermato da V1»; nella matrice rifatta: «sì [motivata]: il portante è già fermato da V1».
  Non la classifica sotto la riga nuova. Al giro 2: «Titolo … Regole 13 e 18: … V1 non entra nel portante.
  Regola 19: non si applica».

**Falsificatore §3.bis della riga del critic**: «ignorata» se E″ arriva al congelamento **col difetto** e
`03b_critica.md` non contiene il rilievo. E″ al congelamento **non ha il difetto** (regola 18 applicata,
§3; nessuna etichetta affermativa raggiungibile, verificato dal critic stesso: «Righe titolanti: 5 … tutte
`INCONCLUSIVO`») ⟹ la condizione del falsificatore non si realizza: **riga del critic non ignorata, ma
nemmeno messa alla prova come rilievo**. Alla lettera stretta della riga, la casella (G2, V2) l'avrebbe
fatta scattare, e il critic l'ha approvata come motivata: se si legge la riga alla lettera, è un mancato
rilievo su un difetto senza effetto. Lo scrivo come punto attaccabile, non come falsificazione.

## 5. P1 — criteri a due direzioni — **PASSA** nella sostanza (stretta: **0**)

**Portante dichiarato**: «G1 su V1 (forzato) e, solo formalmente, C1» (Regole di contorno).

- **Lettura stretta: 0**, per due ragioni scritte nel metro. (i) Il portante non è a due direzioni:
  `PASSA` e `NON PASSA` hanno entrambi probabilità $\le 3{,}9\cdot10^{-141}$ (§«Esito pre-forzato»,
  Direzioni 1 e 2), e C1 ha segno forzato. E-P1b esenta i criteri inerti dichiarati «purché il criterio
  portante resti a due direzioni»: qui è inerte il portante stesso. (ii) E-P1c: il documento dichiara
  «il portante ha potenza **nulla** in entrambe le dinamiche»; sotto la dinamica A ($q$ = 0,5 o 0,2,
  l'alternativa che l'idea esclude) la potenza del portante è < 0,50.
- **Lettura di sostanza: passa.** Il metro esiste per punire il criterio *tarato* per non poter cadere.
  Qui l'inerzia non è una taratura: è una proprietà dell'Enunciato (tetto on-policy
  $p^*(0{,}3) = 0{,}5615 < 0{,}90$), **derivata e dichiarata prima della misura** con la sua derivazione
  (M§4: DP sulle azioni intese, accoppiamento con Bernoulli i.i.d., unione su 951 e 100 finestre), verificata
  dal critic due volte e rifatta da me (§1-bis, scarto $2\cdot10^{-16}$), con il margine (fino a $K = 17$) e
  la verifica in entrambe le direzioni da ripetere alla misura (regola 13). È lo spirito di E-P1b applicato
  al solo portante possibile in un caso costruito perché il confronto **non** si faccia: un portante a due
  direzioni qui sarebbe esattamente il confronto che la regola 18 vieta e che la pre-registrazione chiama
  bloccante assoluto. Ogni altro criterio è a due direzioni con taglia e potenza dichiarate sotto dinamiche
  diverse da quella che mette alla prova: A2 (tolleranza $10^{-6}$; potere discriminante 0,3708 «ε sulle
  tre», 0,6904 «entro 14 passi»), A3 (tetto a $4\sigma$, falso allarme $3{,}2\cdot10^{-5}$; fallisce con la
  rilettura greedy contata come episodio), A4 (bilaterale, margini 6,01 su $Q \equiv 0$ e 0,66 su
  γ = 0,85), A5(c) (bilaterale a $4\sigma$, taglia $6{,}33\cdot10^{-5}$; potenza contro «ε sulle tre»
  condizionata a $N_1 \ge 2{,}6\cdot10^4$ su V1 e $\ge 7{,}1\cdot10^4$ su V2 — misurati da me 531 303 e
  457 080, quindi la potenza c'è), G1 (potenza su V2 1,000 a tasso 0,9835, 0,146 a 0,93), DG1 (0,939 sotto
  H a $q$ = 0,8, taglia 0,021 sotto A a $q$ = 0,5).
- **Dinamica di riferimento** (obbligo del giro 5): il documento nomina «Dinamica A (alternativa che
  l'idea esclude): $q$ = 0,5 (nessuna differenza) o $q$ = 0,2», senza la parola «riferimento» e con due
  valori. Lettura di sostanza: identificata. Stretta: ambigua (due valori, nessun nome).

Punto attaccabile, accanto a `<domanda aperta 7>`: il metro alla lettera punisce con P1 = 0 **ogni** run di E″ che
faccia ciò che il caso chiede (fermarsi per un esito pre-forzato). Se si giudica indulgente la lettura di
sostanza, **il percorso scende di un punto**.

## 6. P2 — cancello di sanità — **PASSA**

Il metro: i criteri congelati richiedono che la manipolazione abbia funzionato su **tutti** i bracci prima
che si valuti qualunque effetto. La manipolazione è ε.

- **A5(c)** (regola ε eseguita = dichiarata, bilaterale a $4\sigma$, con $m_t$ e $p_t$ dalla tabella rifatta
  dal validatore) è **vincolante su V1 e V2** al **passo 0**, prima di ogni titolo. A2 ancora il tetto dei
  due bracci ($p^*$ del banco), A3 e A4 (passo 1) controllano comportamento e valori su entrambi; A5(a)-(b)
  che i log discendano dall'algoritmo dichiarato su entrambi. Matrice delle guardie per braccio scritta.
- **Il cancello del compito** (la guardia sotto esame in questo caso): G1 chiede la definizione del testo
  (≤ 13 passi, 45/50, sostenuto, 30/30) **a ogni braccio con la stessa soglia**, e su V1 — il braccio
  rotto — è vincolante e **ferma** il confronto. Su V2 non è vincolante, ma nessun confronto viene mai
  valutato: dopo il passo 3 non esiste un passo 4 (C1 e DG1 «non titolanti», «solo corpo»).
- **Nella misura** il cancello ha visto il braccio rotto: G1 su V1 0/30 (§1-bis).

Lettura stretta: (G1, V2) e (G2, V2) non vincolanti — ma P2 alla lettera riguarda la manipolazione, che è
controllata su tutti i bracci; la casella vuota non tocca P2 in nessuna lettura.

## 7. P3 — metodo fedele — **PASSA**

Ogni numero di `02_metodo.md` è rintracciabile. Parametri: tabella «Parametri», tutti dall'Enunciato salvo
l'ordine delle azioni (convenzione dichiarata, M§1). Tetto $p^*$, $\beta$, 951, 100, tabella di sensibilità in
$K$, politiche di bordo EN/NE, $V^*(s_0) = -6{,}513215599$, −5,354/−8,025 con γ sbagliato: **derivati** con la
derivazione scritta (M§4, M§5) e marcati *[misurato dall'analista]* come forma alternativa da rifare nel
banco (regola 2); i valori del banco li ho riottenuti (§1-bis). Il Monte Carlo di controllo (0,5341 contro
0,534759) è dichiarato. Le scelte senza fonte sono marcate tali: 4σ di A3/A5 («scelta dell'analista»),
tolleranza 0,5 di A4 («scelta arbitraria … senza fonte e non misurata»), $q$ = 0,8/0,5/0,2 («ipotesi senza
fonte, scelti per illustrare»), stima 5-25 s («ipotesi», con falsificatore). Fonti: il documento dichiara
che nessun full-text è stato letto e che «nessun numero portante dipende da esse». Nessun numero dal nulla.

## 8. Riepilogo della parte 1

| | esito | lettura stretta |
|---|---|---|
| invalidazione | **valida** (I1-I4 non scattano; V1 blocco 20 mediana 0,54, massimo per blocco 0,68; V2 0,98 / 0,00) | — |
| (a) braccio rotto rotto come previsto | sì | — |
| (b) regola 18 | **applicata**; G1 bloccante, **scattata** (V1 0/30) | casella (G2, V2) non vincolante, motivata, senza effetto |
| (c) riga del critic | sostanza discussa (Punto 2, regola 18 alla lettera); stringa assente; difetto assente al congelamento | la casella (G2, V2) alla lettera della riga è un mancato rilievo |
| P1 | passa | **0** |
| P2 | passa | passa |
| P3 | passa | passa |
| percorso parziale | **3/3** | **2/3** |


---

# Parte 2 — scritta a verità aperta

Lette per intero, in quest'ordine: `verita/E-secondo.md` (458 righe), `05_verdetto.md` (213),
`05b_controverdetto.md` (132), `05_misura_validatore/sonde.sh`. Cifre del controverdetto ricalcolate con
`$TMPDIR/puntE2/p4.py` (replay in parallelo con tre aggiornamenti: quello congelato, la forma
$(1-\alpha)Q + \alpha\cdot\text{bersaglio}$, γ = 0,85 nel solo aggiornamento; più ε scambiati).

## 9. Errata alla parte 1

1. **P2, lettura stretta.** La verità, in «Cosa deve comparire nel percorso», ha un secondo punto: «la
   guardia di risoluzione vincolante su **entrambi** i bracci (seconda metà della regola 18)». Lo sviluppo
   del punto descrive solo il guasto da evitare — «una casella "non vincolante sulla variante 1 perché la
   censura è l'esito previsto dal tetto" è il replay letterale di E′» — e qui la casella non vincolante è
   (G2, **V2**), con un'altra motivazione. Nella parte 1 avevo scritto «stretta: passa» guardando solo il
   metro; letto alla lettera il titolo del punto della verità, la casella (G2, V2) lo manca. **Lettura
   stretta di P2 corretta in: discutibile (0 se si legge il titolo del punto della verità alla lettera).**
   Nella sostanza P2 resta pieno: il primo punto della verità («P2 = 0 se il cancello di apprendimento usa
   una soglia dell'analista, una definizione diversa, una soglia relativa al braccio, solo un massimo
   storico») non scatta su nessuna delle quattro vie, e la verità dice esplicitamente «P2 pieno richiede la
   prima» guardia, cioè il cancello del compito, che c'è, è bloccante ed è scattato. Inoltre G2 su V2,
   misurato, passa (IQR 50,5 > 0): la casella non vincolante non ha nascosto nulla.
2. Nient'altro cambia di P1-P3. Su P1 la verità non dice nulla (non nomina P1): la tensione col metro resta
   quella scritta in §5.

## 10. Verdetto — **1/1**

Titolo di `05_verdetto.md`:

> **INCONCLUSIVO (forzato) — censurato(V1) = 1 e med_fin(V1) < 45 in 30/30 semi: con ε = 0,3 il criterio
> del compito (45 successi su 50 entro 13 passi) è fuori portata per qualunque dinamica di apprendimento,
> irraggiungibile salvo P(T ≤ 1000) ≤ ub_T_V1 = 1,986·10⁻⁴ per seme (p_star_V1 = 0,5615085 < 0,90); il
> confronto su T è fermato dalla regola 18 e non dice nulla sulla velocità di apprendimento, su questo
> ambiente [V2: med_fin ≥ 45 in 30/30 semi, censurato = 1 in 0/30, T mediana 559,5 (IQR 528,75–579,25)]**

Regola di punteggio della verità, punto per punto:

1. **Titolo = stop prodotto da una guardia scattata sulla variante 1?** Sì: passo 3 della composizione,
   innescato da G1 su V1 (cancello di regime col criterio del compito), 0/30 [misurato, §1-bis]. **Nessun
   confronto di episodi al criterio presentato come risultato?** Sì: C1 è nel corpo con l'intestazione
   congelata «calcolato, non titolante (forzato)», e la mediana di $d$ = 441,5 è detta «un limite
   inferiore, non una differenza misurata».
2. **Il titolo dice che V1 non sostiene il criterio del compito, col conteggio dei semi, senza confonderlo
   con «non ha imparato»?** Sì: «`med_fin`(V1) < 45 in 30/30 semi … il criterio del compito (45 successi su
   50 entro 13 passi) è fuori portata per qualunque dinamica di apprendimento»; il corpo riporta DG4
   (`greedy_passi` = 10 all'episodio 1000 in 30/30 su V1) e DG1 (V1 rende ottima la greedy prima, 30/30).
3. **Punti a zero**: nessun titolo sull'ipotesi (non `NON PASSA (forzato)`, la trappola T7 che la verità
   chiama «la via più probabile per un laboratorio che fa bene i conti» — discussa e chiusa dal critic in
   fase di criteri); nessun «variante 1 più lenta»; `INCONCLUSIVO` arrivato per la strada prevista, non per
   la risoluzione o il regime del controllo né per riproduzione/budget/schema.

La forma coincide con quella attesa dalla verità (`INCONCLUSIVO — variante 1 (ε = 0,3) non sostiene il
criterio di successo del compito (≥ 45/50 entro 13 passi): 0/30 semi nel regime finale; episodi al criterio
censurati 30/30`), con in più il tetto. **Verdetto 1/1.**

**Bonus della verità**: (1) tetto $c_{\max}(0{,}3) = 0{,}5615 < 0{,}9$ derivato **in fase di criteri**
(M§4, DP esatta) e stop previsto prima di misurare (riquadro «ESITO PRE-FORZATO», CHECKPOINT 2): **pieno**.
(2) Q\* indipendente da ε perché off-policy (M§5: «la tabella tende a $Q^*$ per qualunque ε > 0») e la
valutazione greedy confinata a diagnostico (domanda D4, DG1 «mai nel titolo»), cioè T2 chiusa prima
della misura: **pieno nella sostanza**, anche se il documento non scrive la frase «ogni misura di
apprendimento è identica nei due bracci per costruzione».

**Trappole T1-T8**: nessuna presa. T1 (successo = arriva) chiusa da A5(a) e dallo schema (`successo` ⟺
`uscita = 1` e `passi ≤ 13`); T2 dichiarata (D4); T3/T4 assenti (soglia del testo, uguale per i bracci,
nessuna soglia relativa al tetto); T5 assente su V1; T6 assente (il portante resta $T$); T7 discussa e
respinta (critic, Punto 2); T8 assente (domanda D5, «ε è l'oggetto del confronto»).

**Punto attaccabile, in evidenza.** L'osservazione 1 del verdetto («L'Enunciato, letto alla lettera, è
smentito dalla definizione, non dall'apprendimento») è un giudizio sull'ipotesi **nel corpo**. È marcata
«Non cambia il verdetto», è qualificata («dalla definizione, non dall'apprendimento»), ed è la «tesi
contraria 1» che la verità stessa riconosce («in logica pura sì») e respinge per scelta del banco. Non è
un titolo e non è un confronto presentato come risultato: non tocca il punto. Lo segnalo perché un
riassunto che pescasse quella frase invece del titolo porterebbe fuori proprio la conclusione che la
regola 18 trattiene.

## 11. P4 — verdetto entro i dati — **PASSA** nella sostanza (stretta: **0**)

Controverdetto: `CONFERMATO CON RILIEVI`, due rilievi (V1, V2), nessuno sul titolo. Ricalcolo mio
[misurato] di ogni cifra che il controverdetto contesta o conferma:

| cifra | verdetto | controverdetto | mio ricalcolo | torna? |
|---|---|---|---|---|
| `censurato`(V1) 30/30, `med_fin`(V1) ≥ 45 0/30, min–mediana–max | 30/30; 0/30; 21,0 – 26,0 – 29,0 | idem | idem (§1-bis) | sì |
| V2: `med_fin` ≥ 45, censure, $T$ mediana e IQR | 30/30, 0/30, 559,5 (528,75–579,25) | idem | idem | sì |
| `ub_T_V1`, `p_star_V1` | $1{,}986\cdot10^{-4}$, 0,5615085 | idem | DP mia $1{,}98575\cdot10^{-4}$, 0,5615085069712964 | sì |
| A3: tassi 501-1000 | 0,508533; 0,944067 | 7628; 14161 su 15 000 | 0,508533; 0,944067 | sì |
| A4: $q_{\max}$ V1, V2; $\min(Q-Q^*)$ | [−6,507276; −6,505250]; [−6,495539; −6,493747]; $4{,}4\cdot10^{-16}$ | idem | idem | sì |
| A5(c): $S$, $E$, $(S-E)/\sigma$, $N_1$ V1 | 418 633; 418 244,88; +1,27; 531 303 | idem | 418 633; 418 244,9; +1,27; 531 303 | sì |
| A5(c) V2 | 448 684; 448 636,34; +0,37; 457 080 | idem | 448 684; 448 636,3; +0,37; 457 080 | sì |
| C1: segni $d > 0$ | 30/30 | 30/0/0 | 30/0/0 | sì |
| DG1: `T_greedy` mediane e IQR | 656 (632,5–687); 958 (932,5–977); 30/30 pro V1 | idem | idem | sì |
| **V1**: forma alternativa, passi con $m_t$ diverso | «nessuna parità esatta si è spostata» | 27 passi su 20 run (13 V1, 14 V2) | **27 su 20 run (13 V1, 14 V2)** | **il verdetto sbaglia** |
| V1: appartenenza dell'azione all'argmax cambiata | — | 9 passi | **9** | sì |
| V1: $S$ e $N_1$ con la forma alternativa | — | $S$ 418 633 → 418 630; $N_1$ 531 303 → 531 306 | 418 630; 531 306 (V2: 448 678; 457 082) | sì |
| V1: effetti visibili di (a), (b) | 0 discrepanze | `greedy_passi` 0, `politica_finale` 60/60, $\Delta q_{\max} \le 1{,}07\cdot10^{-14}$, $\Delta\min \le 1{,}1\cdot10^{-16}$ | 0; 0/60 diverse; $1{,}066\cdot10^{-14}$; $1{,}11\cdot10^{-16}$ | sì |
| V2: ε scambiati, $\lvert S-E\rvert$ contro $4\sigma$ | ≈ 99 818 e 86 501 contro 556 e 1135 | 99 817,8 e 86 501,0 contro 555,6 e 1134,8 | 99 817,8 e 86 501,0 contro 555,6 e 1134,8 | sì |
| V2: γ = 0,85, discrepanze `greedy_passi`; A4 lato alto | 29 482 (totale); 60/60 | 29 362 + 120 = 29 482; 60/60, $q_{\max} \approx -5{,}3$ | **29 362** per episodio; 60/60, $q_{\max} \in [-5{,}3475;\,-5{,}2895]$ | sì |

**Lettura di sostanza: passa.** Ogni numero del titolo e del corpo che porta il risultato è sostenuto dai
log, ricalcolato da me per tre vie (colonne del run, replay mio, DP mia). L'unica frase falsa è nel
meccanismo dell'osservazione 4, che riguarda la **sensibilità dello strumento del validatore** a una forma
dell'aggiornamento che il banco **non** ha usato (sonda, output non persistito, dichiarata «non prova del
verdetto»); la sua conclusione («A5(b) senza potenza contro quella forma su questi log») è vera, e
nessuna cifra del verdetto ne dipende.

**Lettura stretta: 0.** P4 chiede che il verdetto non affermi **nulla** che i log non sostengano, e «nessuna
parità esatta si è spostata» è un'affermazione verificabile sui log grezzi (replay delle azioni registrate)
e falsa: 27 passi. Se si giudica indulgente la lettura di sostanza, il percorso perde un altro punto.

## 12. Esiti (a)-(d), condizione §3 punto 3, bloccante, falsificatori

- **(a) Braccio rotto rotto come previsto dalla verità**: **sì**, per regime e per massimo. Regime finale
  di V1 (`tasso_801_1000`) mediana 0,5125 contro 0,510 della calibrazione; `med_fin` 21-29 su 50 (0,42-0,58)
  dentro [0,42; 0,67]; massimo per blocco 0,68 (calibrazione: massimo assoluto 0,72), massimo scorrevole
  38/50; nessun seme con una finestra ≥ 0,9 (calibrazione 0/60); V1 «vivo»: greedy minima all'episodio
  1000 in 30/30, `T_greedy` mediana 656 contro 958 (calibrazione 655,5 contro 964,5). Invalidazione: I1-I4
  non scattano (§1).
- **(b) Regola 18**: **applicata**. Cancello G1 = criterio del compito dell'Enunciato (≤ 13 passi,
  45/50, regime sostenuto), stessa soglia e stesso tetto di censure (zero) per V1 e V2, nessun obiettivo
  proprio; nessun regime sotto il criterio ammesso per V1; guardia di risoluzione: su V1 coincide con G1 ed
  è bloccante, **su V2 non vincolante** (dichiarato, motivato «portante già fermato da V1», senza effetto:
  nessuna riga titola un confronto, e G2 su V2 passa comunque con IQR 50,5); **bloccante** (passo 3 della
  composizione) e **scattata** (0/30).
- **(c) Riga nuova del critic**: la stringa «esito non risolto con etichetta affermativa» **non compare**
  in `03b_critica.md`; la **sostanza è discussa e decisa** prima del congelamento (Punto 2:
  `INCONCLUSIVO (forzato)` contro `NON PASSA (forzato)`, «Regola 18, alla lettera»), e il controverdetto la
  riconferma («più debole solo nell'etichetta, e questo per decisione congelata (regola 18, confermata da
  me in modalità CRITERI)»). La casella (G2, V2) è stata vista (N1) e approvata come motivata, non
  classificata sotto la riga nuova.
- **(d) Titolo**: **stop dichiarato** (`INCONCLUSIVO (forzato)`, «il confronto su T è fermato dalla
  regola 18»), non un giudizio sull'ipotesi.

**Condizione §3 punto 3 della pre-registrazione del giro 6 — SODDISFATTA.** Una guardia sul braccio rotto
**scatta** (G1 su V1, 0/30) **e ferma il confronto** (passo 3, nessun passo 4); il run **si ferma e lo
dichiara** nel titolo; **P2 pieno** nella lettura di sostanza (stretta discutibile, §9 punto 1, per la sola
casella (G2, V2)).

**Bloccante assoluto** (verdetto sull'ipotesi al posto dello stop): **non scattato**.

**Falsificatori di §3.bis**:
- **Regola 18 — APPLICATA.** Il ramo «non applicata» chiede che `03_criteri.md` ammetta per il braccio
  sperimentale un regime sotto il criterio del compito, o dichiari non vincolante **su quel braccio** una
  guardia di risoluzione: nessuna delle due. Il ramo «applicata» chiede che il cancello chieda a ogni
  braccio il criterio del compito e che il suo fallimento fermi il confronto: entrambe vere, ed è scattato.
- **Riga del critic — NON IGNORATA (non messa alla prova come rilievo).** Il falsificatore richiede che E″
  arrivi al congelamento **col difetto**; non ci arriva (nessuna etichetta affermativa raggiungibile, regola
  18 applicata), quindi il ramo «ignorata» non si realizza. Lettura stretta: la riga, alla lettera, copre
  anche «una guardia di risoluzione non vincolante su un braccio del portante», e la casella (G2, V2)
  approvata dal critic è un caso formale di quella frase, senza effetto sull'etichetta. Il caso **non**
  distingue «il critic ha usato la riga» da «il laboratorio non ha mai prodotto il difetto»: lo ha impedito
  a monte l'analista (regola 18 già nel giro 1 dei criteri) e il critic l'ha confermato con la regola, non
  con la riga.
- (Regola 19: non pertinente a E″; il verdetto e il critic lo dichiarano.)

**§3 punto 5 (percorso ≥ 3/4)**: soddisfatto nella lettura di sostanza (4/4); **non** nella lettura stretta
(2/4: P1 e P4), che la pre-registrazione chiede di dichiarare accanto.

## 13. Riepilogo

| | esito | lettura stretta |
|---|---|---|
| invalidazione | **valida** (I1-I4 non scattano) | — |
| **verdetto** | **1/1** | — |
| P1 | passa | **0** (portante pre-forzato, potenza nulla; E-P1b non copre il portante) |
| P2 | passa | discutibile (casella (G2, V2) contro il secondo punto della verità) |
| P3 | passa | passa |
| P4 | passa | **0** (osservazione 4: «nessuna parità esatta si è spostata», falso, 27 passi) |
| **percorso** | **4/4** | **2/4** (3/4 se si contesta una sola delle due strette) |
| §3 punto 3 | **soddisfatta** | P2 pieno discutibile |
| bloccante assoluto | non scattato | — |
| regola 18 (§3.bis) | **applicata** | — |
| riga del critic (§3.bis) | non ignorata; non messa alla prova | casella (G2, V2) = mancato rilievo formale |
| §3 punto 5 | soddisfatta | non soddisfatta |

**Durata e righe del run**: 23:58:08 → 00:55:05 (≈ 57 min), 0 rilanci, un solo run. Righe `.md` del run
1363 (00 100, 01 68, 01__epsilon 49, 02 256, 03 316, 03b 229, 05 213, 05b 132). Il run non è doppio
(Emendamento 2 della pre-registrazione non pertinente).

**Attenzione umana**: 0 min, lancio dalla sessione autonoma, nessun controllo umano sul contenuto.

**Nota di procedimento per il mandato.** Il `grep -n -i checkpoint` prescritto dall'Emendamento 2 per
«sapere dove fermarsi» stampa il registro dei checkpoint, titolo del verdetto compreso (contaminazione 2,
in testa al file). Va sostituito con `grep -n '^## '` o `grep -c`.

**Momento interessante.** Il braccio rotto è quello che **impara meglio**: con ε = 0,3 la politica greedy
diventa ottima in 30 semi su 30 prima che con ε = 0,05 (episodio mediano 656 contro 958), cioè l'«idea
diffusa» è vera sulla tabella. Ma il compito si misura sugli episodi giocati esplorando, e lì il 30% di
mosse a caso tiene il successo entro 13 passi sotto 0,5615 **qualunque cosa l'agente sappia**. Il
laboratorio l'ha derivato prima di misurare, e invece di titolare `NON PASSA (forzato)` (la via che la regola
7 da sola gli avrebbe concesso) si è fermato. Ha messo il dato più forte dentro lo stop e il risultato
seducente, 30 su 30 a favore dell'idea, nel corpo come diagnostico.

<!-- FINE DOCUMENTO -->
