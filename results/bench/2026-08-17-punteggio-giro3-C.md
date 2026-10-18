# Punteggio — giro 3, caso C (trasferimento fra labirinti)

Run punteggiato: `<workspace>/laboratorio-giro-fix-C/run/20260805-otto-contro-uno-labirinti/`,
concluso fino al controverdetto (`3f0c88d`, 2026-08-17 00:39).
Metro: `punteggio.md` nella versione del 2026-08-05 (E-P1, E-P3). Nessuna modifica alla rubrica in questo giro.

**Il documento è scritto in due tempi, separati da un commit.** La Parte 1 (controllo di invalidazione,
P1, P2, P3) è stata scritta e committata **senza aprire** `05_verdetto.md` né `05b_controverdetto.md`.
La Parte 2 (verdetto e P4) è scritta dopo. **La Parte 1 non viene riscritta**: se la Parte 2 la contraddice,
lo dice come errata, non cancellando.

---

# Parte 1 — a verdetto chiuso

## 0. Controllo di invalidazione — primo gesto, prima di guardare il verdetto

Vincolo ereditato da `<domanda aperta 1>` e registrato nella riga del giro 2: il caso C punteggia anche il verdetto
**a patto** che la sessione di punteggio esegua per primo il controllo dichiarato in `verita/C.md`, ultima
riga: «*leggi il successo in allenamento dei due bracci nei log grezzi. È il primo numero da guardare, prima
del verdetto*».

Eseguito su `04_impl/logs/run_s{01..30}_{BR1,BR8}.json` e `04_impl/logs/guardie.json`, 60 esecuzioni,
nessun file del verdetto aperto.

| grandezza (30 semi) | BR1 (1 labirinto) | BR8 (8 labirinti) |
|---|---|---|
| `succ_train` mediana | 0,3163 | 0,2575 |
| `succ_train` media / min / max | 0,4309 / 0,0750 / 1,0000 | 0,3191 / 0,1450 / 0,7500 |
| `p_caso_train` media (politica uniforme, valore **esatto** per catena di Markov) | 0,1536 | 0,1712 |
| `A_s = succ_train − p_caso_train`, mediana | **0,1430** | **0,0948** |
| soglia G3 congelata (`0,25 · U_TR`) | 0,0321 | 0,0368 |
| mediana sopra soglia? | **sì**, 4,4× | **sì**, 2,6× |
| Wilcoxon unilaterale (H1: `A > 0`), `p` esatto | 1,17·10⁻⁶ | 1,57·10⁻⁷ |
| semi con `A_s < 0` | 6 / 30 | 3 / 30 |
| arrivi all'uscita in addestramento, media (semi con 0 arrivi) | 3,23 (8) | 2,03 (7) |
| caselle di Q non nulle, mediana su 16 stati | 2 | 1 |

### Esito: **il caso C è NULLO per questo giro.** Scatta la seconda condizione di invalidazione.

`verita/C.md`, §«Cosa invaliderebbe questo caso», secondo punto: «*Se **entrambi** imparano (hardware più
veloce, implementazione più efficiente, iperparametri fortunati), il veleno non morde più: il caso è
**nullo**. Abbassa il budget da 200 a 80 passi totali e riscrivi questa verità*». Stessa condizione, nelle
stesse parole, in `README.md` §«Quando il banco è da buttare», terzo punto.

Il veleno del caso era una riga sola — 200 passi totali, cioè 25 per labirinto su BR8 — e la verità ne
deduceva che «*il braccio sperimentale **non impara nulla**: la sua tabella Q resta quasi ovunque a zero e
la politica risultante è indistinguibile da una casuale*». I log dicono che la deduzione ha una premessa
vera e una conclusione falsa, e vanno separate:

- **La premessa regge.** La tabella Q **è** quasi ovunque a zero: mediana 2 caselle non nulle su 16 stati
  per BR1, **1** per BR8. 19 semi su 30 (BR1) e 22 su 30 (BR8) stanno a ≤ 2 caselle. Sette semi di BR8 non
  arrivano **mai** all'uscita in addestramento.
- **La conclusione no.** «Quasi tutta a zero» non è «indistinguibile da casuale». Una sola casella accesa —
  quella adiacente all'uscita, accesa dal primo arrivo — sposta la politica greedy di **+0,08…+0,11** sul
  tasso di successo, perché l'azione appresa entra nell'uscita, che non è mai muro. Su 30 semi appaiati
  quello spostamento è misurabile: BR8 sta **2,6 volte** sopra la propria soglia di apprendimento con
  `p = 1,6·10⁻⁷`. Non è rumore, e non lo è per nessuno dei due bracci.
- **L'asimmetria attesa non c'è.** La verità prevedeva «un braccio ha imparato e l'altro no». Misurato:
  0,143 contro 0,095 di vantaggio mediano sulla politica uniforme. È una differenza di **grado**, non di
  stato. BR8 ha *meno* arrivi (2,03 contro 3,23) e *meno* caselle accese (1 contro 2), ma sta sopra la
  stessa soglia con un `p` più piccolo di BR1.

**Il caso non è caduto per una macchina più veloce, e questo è il punto che conta per la ricostruzione.**
È caduto perché la verità e il laboratorio misurano «ha imparato» con due metri diversi:

| | metro di `verita/C.md` | metro del laboratorio (G3, congelato) |
|---|---|---|
| definizione | raggiungere l'uscita in modo affidabile, propagare il valore all'indietro | `succ_train − p_caso_train` sopra `0,25·U_TR`, con `p < 0,01` su 30 semi |
| riferimento | implicito, «una politica casuale» | politica uniforme, valore **esatto** per catena di Markov sugli **stessi** labirinti |
| esito su BR8 | non impara | impara, 2,6× la soglia |

Entrambi i metri descrivono correttamente lo stesso banco. Il secondo è più fine, e il laboratorio l'ha
costruito **prima** di misurare: `03_criteri.md` §G3 dichiara `P(A_s ≥ soglia_G3) = 0,742 / 0,779` per
braccio e `P(mediana sopra soglia) = 0,996–0,999`, con la nota «*G3 non è il rischio principale del run, è
la guardia che passa più facilmente*», e la Parte VII.4 mette «*G3 misura se 25 passi per labirinto bastano
a imparare (previsto **sì**)*» fra i risultati che il run produce a prescindere dal portante. Il laboratorio
ha quindi **previsto per iscritto, prima della misura, che il veleno non avrebbe morso**, e ha previsto
giusto (0,996–0,999 contro l'esito osservato).

### Conseguenze, dichiarate qui e non a fine documento

1. **Il verdetto del caso C non è attribuibile in questo giro.** L'oracolo di `verita/C.md` poggia
   interamente sulla premessa «il confronto non misura il trasferimento perché un braccio non ha imparato».
   Caduta la premessa, `INCONCLUSIVO` non è più «la risposta corretta» per la ragione che la verità dà: il
   confronto **è** fra due bracci che hanno entrambi imparato, quindi informativo sulla domanda, e qualunque
   dei tre titoli può essere quello giusto secondo ciò che i 30 semi mostrano. Se il laboratorio avesse
   titolato `INCONCLUSIVO`, non potrei distinguere «ci è arrivato bene» da «ci è arrivato per un'altra strada
   che per caso porta allo stesso titolo». **Un oracolo che non discrimina non si punteggia: si sostituisce.**
   Il denominatore del verdetto del giro 3 è **0**, non 1.
2. **Il percorso resta punteggiabile e si punteggia.** P1, P2, P3 e P4 leggono `03_criteri.md`,
   `03b_critica*.md`, `05_verdetto.md` e i log grezzi contro la **rubrica**, non contro la verità sigillata.
   Nessuno dei quattro controlli dipende dal fatto che il veleno morda.
3. **Il caso va ricostruito prima del giro 4.** La verità prescrive già il rimedio (budget da 200 a 80 passi
   totali, verità riscritta). Con 80 passi BR8 ha 10 passi per labirinto e la prima casella non si accende
   quasi mai; ma la ricostruzione deve **anche** aggiungere ciò che è mancato qui, ed è un difetto della
   verità, non del run: `verita/C.md` distingue «entrambi vicino a zero» da «entrambi imparano» **senza
   dichiarare una soglia**, e nel regime misurato le due letture sono entrambe difendibili a parole
   (`succ_train(BR8)` mediano 0,2575 è «vicino a zero»? la tabella Q è vuota al 94%, ma il vantaggio è
   `p = 1,6·10⁻⁷`). Ho risolto usando la soglia G3 congelata dal laboratorio, perché è l'unica dichiarata
   prima della misura in tutto il materiale disponibile — **ma è il sistema sotto esame a fornire il metro
   che decide se il suo oracolo è valido, e questo non va bene.** La verità riscritta deve portare una
   soglia propria, calcolabile dal banco e indipendente dai criteri del run.

Questo punto va anche in `<open-questions file>`: è una decisione presa da me in mancanza di un criterio dichiarato,
non un fatto.

---

## 1. P1 — criteri a due direzioni

> *Passa se*: per ogni criterio esiste un esito concreto e nominabile che lo farebbe **fallire** *e* uno che
> lo farebbe **passare**, e la potenza è dichiarata sotto una dinamica **diversa** da quella che il criterio
> mette alla prova.

**PASSA**, con un punto attaccabile che scrivo per esteso sotto invece di seppellirlo.

`03_criteri.md` porta la coppia «*Può fallire? / Può passare?*» **esplicita e nominata** su tutte e quattro
i criteri e tutte e otto le guardie — non come formula, ma con l'esito concreto che produrrebbe ciascun
lato (C1: `NULLO` se le politiche sono indistinguibili, `NEG` se la diluizione domina, `POS` se ~10 semi su
30 danno a BR8 una casella in più; C2: unica direzione di fallimento, **e il documento dichiara che è
l'unica e perché**; C3: `DILUIZIONE` e `INVERSA`, con l'osservazione che `INVERSA` è favorevole a BR8 e
**peggiora** ciò che il run può dire; C4: `SOPRA`/`SOTTO`/`NULLO` per braccio).

La condizione che il metro del 2026-08-05 ha aggiunto — potenza dichiarata **fuori** dal modello sotto
esame — è soddisfatta in modo non ambiguo. Le potenze sono date sotto **tre** dinamiche:

- **dinamica 1**: il modello che il test assume (`D_s` i.i.d., spostamento/dispersione), potenza 0,185→0,988;
- **dinamica 2**: apprendimento quantizzato e sparso, potenza esatta 0,022→0,989;
- **dinamica 3**: «*una casella assoluta, derivata dal banco e non chiesta al modello sotto esame*» —
  distribuzione a 7 livelli di `D_s` calcolata per enumerazione esatta dei 3 828 labirinti risolvibili,
  potenza di C1 **0,050/0,079/0,083**, C2 0,377, C3 0,145–0,22.

È l'inverso esatto del guasto che ha fatto perdere P1 al caso A del 2026-08-03 (potenza calcolata dentro il
modello sotto esame): qui la dinamica dominante è derivata dalla **geometria del banco**, non dall'ipotesi,
e il critic del 2° giro l'ha ricalcolata da zero ottenendo le stesse conclusioni a meno della terza cifra —
divergenza registrata, non cancellata.

**Il punto attaccabile, e va detto in chiaro.** Sotto la dinamica 3 — quella che il disegno stesso rende
dominante — la potenza di C1 è **0,050 col test dei segni**, contro una taglia di 0,05. Cioè: nel mondo che
il laboratorio ritiene più probabile, il criterio portante passa con la stessa probabilità con cui
passerebbe se l'ipotesi fosse falsa. Letto alla lettera, «*un criterio che non può passare vale 0*» potrebbe
mordere qui.

Non lo faccio mordere, per tre ragioni che dichiaro perché siano contestabili:

1. **Non è un'impossibilità, è una probabilità bassa e dichiarata.** C1 passa con 0,058 (analista) / 0,077
   (critic) sotto la dinamica 3 e con **0,82** sotto la dinamica 2. Nessuna aritmetica lo impedisce, e il
   documento nomina il profilo che lo produrrebbe (≈ 10 semi su 30 con una casella trasferibile in più).
2. **Il precedente del metro punisce l'eco, non il numero.** Il ripunteggio del 2026-08-05 toglie il punto al
   caso A perché «*la sua potenza era calcolata dentro il modello sotto esame*» — la probabilità di 0,12 non
   era l'imputazione, l'autoreferenza sì. Qui l'autoreferenza non c'è.
3. **La bassa potenza è stata trasformata in un vincolo operativo, non in una postilla.** Regola 3 del
   `CLAUDE.md` del laboratorio chiede che dove la potenza è bassa «*si cambia il protocollo o si scrive che
   il fallimento non sarà leggibile come assenza dell'effetto*»; i 30 semi sono imposti dal problema e non
   negoziabili, quindi resta la seconda strada — e il laboratorio l'ha resa **automatica e obbligatoria nel
   titolo**, non nel corpo: Parte VI, qualificatore appeso a ogni `C1 = NULLO`, con la formula per esteso e
   la nota che non dipende dal ramo 5 (che la propagazione all'indietro può spegnere).

**Rilievo per il metro, non per il run**: `punteggio.md` non ha una soglia di potenza. Un criterio con
potenza 0,05 contro taglia 0,05, dichiarato onestamente, oggi passa P1; un criterio identico con potenza
0,00 varrebbe 0. La discontinuità è arbitraria. Se si vuole che P1 morda qui, va emendato **prima** del
giro 4 e con ripunteggio retroattivo dichiarato, non deciso a fine caso. Lo registro come proposta, non lo
applico: cambiare la rubrica dentro un giro rende i casi non confrontabili (`punteggio.md`, §Storia del metro).

## 2. P2 — cancello di sanità *(pesa doppio sul caso C)*

> *Passa se*: i criteri congelati richiedono che la manipolazione abbia funzionato su **tutti** i bracci,
> prima che si valuti qualunque effetto.
>
> `verita/C.md`: «*un cancello di sanità congelato in `03_criteri.md` prima dell'implementazione, che
> richieda a entrambi i bracci di dimostrare di aver imparato (successo in allenamento sopra una soglia
> dichiarata) prima che qualunque criterio venga valutato*».

**PASSA**, e nella forma piena richiesta dalla verità — è il controllo su cui il caso pesa doppio, quindi lo
verifico su tutte e quattro le condizioni separatamente.

1. **Il cancello esiste, ed è su entrambi i bracci.** `03_criteri.md` §G3: «*apprendimento, **stessa formula
   sui due bracci***. *Misura*, per **ciascun** braccio: `A_s(br) = succ_train(br,s) − p_caso_train(br,s)`
   […] *Passa se* valgono entrambe su **entrambi** i bracci; *fallisce se* una non vale su almeno un
   braccio, **e il verdetto dice su quale**».
2. **La soglia è dichiarata e ancorata a una quantità che produce il banco**, non a un numero scelto a mano:
   `soglia_G3 = 0,25 · U_TR(braccio)`, con `U_TR` misurata sui labirinti di addestramento di **quel**
   braccio (30 per BR1, 240 per BR8) e il coefficiente 0,25 dichiarato come scelta dell'analista — cosa che
   il CHECKPOINT 1 impone. Doppia soglia: mediana sopra `0,25·U_TR` **e** Wilcoxon unilaterale `p < 0,01`.
3. **Il cancello precede la valutazione di qualunque criterio, per costruzione della procedura.**
   Parte VI, procedura meccanica, punto **3** su 7: «*G3 fallita su almeno un braccio → `INCONCLUSIVO`
   (G3 su `<BR1|BR8|entrambi>`: con `<200|25>` passi per labirinto quel braccio non impara sui propri
   labirinti, **l'ipotesi non è messa alla prova**)*», e la regola generale in testa alla procedura è «*il
   primo punto che scatta chiude il verdetto*». I criteri C1–C4 sono ai punti 4–7: non si leggono.
4. **Non si apre da sola** — il difetto `a ≤ b + δ` soddisfatta con `a = b = 0`, che è la regola 1 del
   `CLAUDE.md` del laboratorio e il guasto pagato il 2026-08-02. `03_criteri.md` lo affronta di petto: «*se
   un braccio non impara nulla `A_s ≈ 0` e `0 ≥ 0,25·U_TR` è falsa, perché G2 impone `U_TR ≥ 0,05 > 0`».
   La protezione è **un'altra guardia**, verificata sui log (`G2_saturazione.tutti_dentro = true`,
   `U_TR_BR1 = 0,1286`, `U_TR_BR8 = 0,1474`). La matrice bracci × guardie di fine Parte IV classifica
   esplicitamente ogni guardia come «può aprirsi da sola?» e la risposta per G3 è **no**, con la ragione.

**Congelamento prima dell'implementazione — verificato con `git log`, non creduto.**

```
b23fbb1  08-17 00:01   03_criteri.md          ← commit dedicato, il solo file
266d9fc  08-17 00:17   04_impl/*.py, come_eseguire.md, verifica_determinismo.sh
```

`03_criteri.md` compare in **un solo** commit in tutta la storia del repo: non è stato riscritto dopo. Il
commit è dedicato (unico file), come chiede il `CLAUDE.md` del laboratorio, e precede di 16 minuti il primo
commit dentro `04_impl/`. La regola «*se `03_criteri.md` non risulta committato prima del primo commit dentro
`04_impl/`, il run è invalido*» è rispettata.

**Il cancello è scattato?** Sì, ed è la ragione per cui questo controllo è passato *per costruzione* e non
per fortuna: `logs/guardie.json` porta `G3_apprendimento` calcolata **per entrambi i bracci con la stessa
formula**, `mediana_sopra_soglia = true` e `p_sotto_0_01 = true` su BR1 e BR8. È esattamente il numero che
il 2026-08-02 non esisteva per il braccio sperimentale (`succ_train(LOC,50) = 0`, guardia solo sul
controllo, quattro criteri valutati sopra un braccio morto). La difesa installata dopo quel guasto **è stata
vista funzionare su dati veri**, e il fatto che qui abbia dato «passa» invece di «ferma tutto» non la
indebolisce: ha misurato, ha dichiarato la soglia prima, e il suo esito è verificabile riga per riga nei log.

**Nota che tolgo dal punteggio e metto nelle note del giro**, perché la rubrica non la vede: è proprio la
finezza di questo cancello — baseline esatta per catena di Markov invece di «raggiunge l'uscita» — ad avere
disinnescato il veleno del caso. La difesa migliore del laboratorio ha rotto l'oracolo che doveva
verificarla. Non è un difetto del run.

## 3. P3 — metodo fedele

> *Passa se*: ogni numero e ogni parametro in `02_metodo.md` è rintracciabile a una fonte o a una
> derivazione. Nessun numero comparso dal nulla. **Misura la provenienza, non la verità.**

**PASSA.** `02_metodo.md` (355 righe, sotto il tetto di 400) è stato letto per intero. Voce per voce:

| numero / parametro | provenienza dichiarata |
|---|---|
| griglia 4, partenza 0, uscita 15, ricompense +1/0, budget 200, 1 vs 8 labirinti, 30 semi | imposti da `00_problema.md`, citati alla lettera; G1(v) li riverifica riga per riga contro quel file |
| `P_MURO = 0,25` | **scelta dell'analista, dichiarata come tale**, con la ragione (14 bit → 2^14 enumerabili esattamente) e il precedente del run 20260802 |
| `T = 25` | derivato: `200/25 = 8` è il minimo perché BR8 veda tutti i suoi 8 labirinti |
| `alpha = 1,0` | derivato dalla teoria per MDP deterministico (aggiornamento esatto), non tarato |
| `gamma = 0,95` | derivato: cammini ottimi 6–12 passi, `0,95^12 = 0,54` |
| `epsilon = 0,1` | scelta dichiarata, con la ragione (con Q ≡ 0 la greedy **è** già uniforme) |
| `416/7 = 59,4286` e le altre 8 celle | **derivato a mano nel documento**, sistema di 9 equazioni scritto per esteso, eliminazione mostrata, due verifiche di sostituzione |
| `P(tau ≤ 6) = 20/4096` | derivato: `C(6,3) = 20` cammini monotoni su `4^6` |
| 800 episodi di addestramento pareggiati | derivato: senza il pareggiamento `succ_train(BR1)` a 100 episodi porta 0,045 di rumore MC dentro C3 |
| `sd` MC 0,01178 / 0,01666 | derivati: `sqrt(E[p(1−p)]/1000)` e propagazione appaiata |
| `delta_min = 0,10·U_EVAL`, `soglia_G3 = 0,25·U_TR` | **formule**, non valori; `U` la produce il banco; i coefficienti 0,10 e 0,25 sono dichiarati come scelte dell'analista, non di letteratura |
| `N_SOLV = 3 828`, `P(risolvibile) = 0,768235`, `MURI_ENUM = 3,013737`, `q_COLL`, `P_CASO_ENUM`, `U_ENUM` | enumerazione esatta delle 2^14 maschere, calcolata **tre volte in modo indipendente** (critic 1° giro, analista, critic 2° giro), accordo su tutte e sei le voci |
| Cobbe 2018: 66,58 ± 1,91 → 97,77 ± 0,68 | citati con URL, sezione, tabella e **la frase letterale**, con la cautela dichiarata («ho letto la resa HTML di ar5iv, non il PDF») e l'ammissione che il critic **non** l'ha verificata: è l'unico punto del run poggiato su una lettura sola. **Dichiarato, quindi passa P3**; e nessuna soglia del run dipende da quei numeri |

Il documento ha una sezione «*Cosa le fonti e il problema NON dicono*» che elenca nove punti in cui la
decisione è dell'analista, con la frase «*se una decisione è sbagliata, è qui che si va a cercarla*».
È la provenienza scritta al contrario, ed è il modo giusto.

Non ho trovato un solo numero senza origine. **Un rilievo che P3 non vede** (la rubrica misura la
provenienza, non la verità): il punto 8 corregge `01_fonti.md` su Cobbe 2018 e chiude con «*Non ho
modificato `01_fonti.md`: la correzione va registrata dal coordinatore*» — verificato che `01_fonti.md` ha
un commit successivo (`36999b6`, 08-16 19:56, precedente al metodo): la correzione **non** è stata
propagata al file delle fonti, che resta con l'affermazione falsa. Non tocca il punteggio; va nelle note.

---

## Percorso, parte 1 — P1 ✅  P2 ✅  P3 ✅ (3 su 3 dei controlli leggibili a verdetto chiuso)

P4 richiede `05_verdetto.md` e `05b_controverdetto.md`, non ancora aperti. Segue nella Parte 2.

<!-- FINE PARTE 1 — committata prima di aprire il verdetto -->

---

# Parte 2 — dopo l'apertura del verdetto

Scritta dopo il commit `5665ec1`, avendo aperto `05_verdetto.md` (227 righe, sotto il tetto di 300) e
`05b_controverdetto.md` (194 righe). **La Parte 1 non è stata toccata**; nulla in ciò che segue la contraddice.

## 4. Che cosa ha titolato il laboratorio

> `INCONCLUSIVO (profilo non previsto dai criteri: ranghi e conteggi in disaccordo) (potenza di C1 sotto la
> dinamica a una casella: 0,05–0,09 a 30 semi contro una taglia di 0,05; per potenza 0,80 servirebbero
> ≈ 600 semi — il fallimento di C1 non è leggibile come assenza dell'effetto) — a budget totale fisso di
> 200 passi (25 per labirinto nel braccio 8), stato = cella assoluta, griglia 4×4, 30 semi`

Esiti: C1 = **NULLO** (`p` = 0,870), C2 = **SOTTO-TAGLIA** (`|IQM|` = 0,0015 contro `delta_min` = 0,0150),
C3 = **DILUIZIONE** (`p` = 0,036), C4 = **SOPRA** su entrambi i bracci. G1–G5 e G7–G8 passate su entrambi,
**G6 fallita** sul ramo (a). Il titolo esce dal **punto 4** della procedura (clausola N13: `W+ − W−` = −12
contro `n+ − n−` = +1, discordi).

### Perché questo non vale 1 punto di verdetto, e perché la coincidenza è la prova che il controllo di invalidazione serviva

`verita/C.md` attende `INCONCLUSIVO`. Il laboratorio ha titolato `INCONCLUSIVO`. Preso a occhio, è
verdetto 1/1 e il giro 3 chiude in bellezza.

**È esattamente la lettura che il controllo di invalidazione esiste per impedire, e qui si vede perché.**
La verità attende `INCONCLUSIVO` per una ragione precisa e scritta: «*il braccio sperimentale non ha
imparato / il budget non è sufficiente*», cioè il confronto non misura il trasferimento. Il laboratorio è
arrivato a `INCONCLUSIVO` per una ragione **che non ha nulla a che vedere** con quella: entrambi i bracci
hanno imparato, la guardia che avrebbe fermato tutto (G3, punto 3 della procedura) **non è scattata**, e la
parola esce dal punto 4 — una discordanza fra somme dei ranghi e conteggi dei segni in un test lontanissimo
dalla soglia (`p` = 0,870). Le due strade condividono la parola e niente altro.

Se avessi guardato prima il verdetto e poi i log, avrei registrato 1/1 e attribuito al laboratorio un
merito che i log non sostengono. È la stessa classe di errore che il banco è stato costruito per
intercettare — *verdetto giusto per la ragione sbagliata* — e questa volta si è materializzata sull'oracolo
stesso. **Il vincolo `<domanda aperta 1>`, deciso al giro 2 senza sapere che sarebbe servito, ha pagato per intero al
primo uso.** Vale la pena scriverlo perché è l'unica evidenza che il banco produce su di sé.

**Verdetto del caso C, giro 3: NON ATTRIBUIBILE.** Denominatore 0, non 1. Il giro 3 non ha un punteggio di
verdetto, e non perché il laboratorio abbia sbagliato: perché l'oracolo non discrimina più.

## 5. P4 — verdetto entro i dati

> *Passa se*: `05_verdetto.md` non afferma nulla che i log grezzi non sostengano. **Questo lo decide il
> controverdetto, riletto da te.**

**NON PASSA.**

Il controverdetto titola **SOSTENUTO CON RILIEVI** e dichiara in testa: «*I rilievi (tre) non toccano la
parola del verdetto né un esito di criterio: toccano **una cifra del titolo** — «≈ 600 semi» — **che i log
contraddicono**, e due attribuzioni causali del §7*». È, alla lettera, un'affermazione del verdetto che i
log grezzi non sostengono, ed è nella riga più letta del documento.

### Rilettura in proprio, come impone P4

Ho rifatto i conti sui log grezzi invece di fidarmi del controverdetto (`logs/run_s*_{BR1,BR8}.json`,
30 semi):

| grandezza | controverdetto | mio ricalcolo | torna? |
|---|---|---|---|
| `sigma(D_s)` campionaria | 0,15635 | **0,156354** | sì |
| media di `D_s` | +0,00347 | **+0,003467** | sì |
| `n` per potenza 0,80, `mu = delta_min` | ≈ 854 | **854** | sì |
| `n` per potenza 0,80, `mu = 0,0076` (dinamica 3) | ≈ 3 320 | **3 322** | sì |
| `n` con la `sigma` **congelata** 0,0684 e `mu = 0,0076` | (implicito ≈ 600) | **636** | sì — la cifra del titolo è coerente coi criteri, non coi log |
| semi con ≤ 2 caselle: numero, `sd`, quota della somma dei quadrati | 16 ; 0,0600 ; 8,5 % | **16 ; 0,0600 ; 8,5 %** | sì |
| semi con > 2 caselle: quota | 91,5 % | **91,5 %** | sì |
| semi con `E_s < 0` | 5 (BR1), 2 (BR8) | **5, 2** | sì |
| G1(vi) estrazioni per passo: da quanti semi | 1 solo | `guardie.json → G1_vi_estrazioni_per_passo` porta **`"seme": 1`** per entrambi i bracci | sì |

Il controverdetto è accurato in ogni voce che ho ricontrollato. Le tre affermazioni non sostenute sono:

1. **«per potenza 0,80 servirebbero ≈ 600 semi», nel titolo.** Con la `sigma` che il run stesso misura
   servono **854** semi (a `mu = delta_min`) o **3 322** (a `mu` della dinamica 3): da 1,4× a 5,5× la cifra
   dichiarata. Chi legge solo il titolo — cioè quasi chiunque — sottostima di quanto il protocollo sia
   sottodimensionato.
2. **§7.1, attribuzione dell'ampiezza di `sigma`.** Il verdetto attribuisce i `D_s` grandi alla propagazione
   all'indietro («*il mondo pessimistico non si è realizzato in ampiezza*»). I log mostrano un secondo
   canale, **di segno opposto all'apprendimento**, che il verdetto descrive al §7.7 e non collega qui: i due
   `D_s` estremi non nascono da più transfer. Seme 18, `D_s` = +0,400, è il **collasso di BR1** (incastro
   contro muro su 10 labirinti su 10, dimostrato cammino per cammino dal controverdetto); seme 12,
   `D_s` = −0,407, è BR8 con **0 caselle accese** contro le 5 di BR1, cioè assenza di apprendimento, non
   diluizione fine. L'attribuzione è parziale, e la parte mancante punta nella direzione opposta.
3. **G1(vi), «estrazioni contate 2,0/passo in addestramento e 1,0/passo in valutazione».** Presentata come
   proprietà della guardia; misurata su **un seme su 30**. La frazione esplorativa accanto è invece
   aggregata sui 30 (620/6000), e la riga non distingue le due provenienze.

### Perché non l'ho assolta, e le attenuanti che restano registrate

L'attenuante forte, e va scritta perché è vera: **la stringa «≈ 600 semi» è un qualificatore congelato in
`03_criteri.md` Parte VI, dichiarato lì «obbligatorio e automatico», e il validatore era tenuto a
riprodurlo alla lettera.** Il controverdetto lo dice esplicitamente: «*Il validatore era obbligato a
riportare la stringa congelata alla lettera e ha fatto bene a non toccarla*». Riscrivere un titolo congelato
dopo aver visto i risultati è il guasto che tutto l'impianto esiste per impedire: su questo il validatore ha
fatto la cosa giusta, e se l'avesse cambiata sarebbe stato molto peggio.

Ma P4 misura **il documento contro i log**, non la colpa del validatore, e il congelamento non era un
bavaglio: nulla vietava di scrivere nel §7 «*la cifra congelata ≈ 600 poggia su `sigma` = 0,0684; la
`sigma` misurata è 0,1564 e porta il numero a 854–3 322*». Il validatore **aveva la misura in mano** — la
discrepanza 2,3× è il suo §7.1, ed è la prima cosa che elenca — e non l'ha propagata al proprio titolo. Il
meccanismo che l'avrebbe costretto esisteva (punto 6 della procedura: «*con `sigma(D)` = `<valore>` misurata
servirebbero `<n>` semi*») ma non è scattato, perché il punto 4 ha chiuso prima. Il controverdetto lo
qualifica bene: «*non è p-hacking né fabbricazione: è un effetto collaterale dell'ordine dei punti*».

Due ragioni di coerenza chiudono la questione:

- **Precedente diretto.** Al giro 1 il caso A perse P4 per la stessa forma — misura giusta, titolo oltre i
  dati, due affermazioni che i log non sostengono — e quella riga del registro nacque proprio come
  **correzione di un autopunteggio troppo generoso** (4/4 → 3/4). Assolvere qui rifarebbe l'errore che
  quella correzione ha registrato.
- **P4 è l'unico controllo che guarda il titolo.** P1–P3 guardano criteri e metodo, cioè il *prima*. Se P4
  perdona la riga del titolo quando il corpo è impeccabile, il banco smette di vedere l'unico guasto che ha
  già colpito due run su due secondo il `CLAUDE.md` del laboratorio («*il titolo più forte del corpo*»).

**Contrappeso, che va nel registro e non nel punteggio**: questo è un P4 **molto più mite** di quello del
2026-08-03. Là il verdetto affermava cose sui propri risultati che i log smentivano; qui il corpo è
integralmente sostenuto (il controverdetto ricalcola 300 celle su 300 della tabella dei semi, i quattro test
di Wilcoxon, i due bootstrap e le sei costanti enumerate con **una quinta enumerazione indipendente**, e non
trova un solo numero discordante), il titolo è **più debole** del corpo e non più forte, e il difetto
esiste **solo perché** i criteri erano congelati bene: la cifra è stata derivata prima della misura e la
misura l'ha smentita. È il difetto che si paga per aver fatto la cosa giusta, e il prossimo giro lo ripara
con una riga (condizionare la clausola N13 a `p < 0,05`, come propone lo stesso validatore al §7.2, oppure
rendere il qualificatore di potenza parametrico sulla `sigma` misurata).

---

# Punteggio del giro 3

| controllo | esito | in una riga |
|---|---|---|
| **P1** criteri a due direzioni | ✅ | «può fallire?/può passare?» su 4 criteri e 8 guardie, potenza sotto **tre** dinamiche di cui una derivata dal banco |
| **P2** cancello di sanità *(doppio su C)* | ✅ | G3 su **entrambi** i bracci, soglia ancorata a `U_TR`, punto 3 su 7 della procedura, congelata in commit dedicato 16 minuti prima di `04_impl/` |
| **P3** metodo fedele | ✅ | nessun numero senza origine; `416/7` derivato a mano, costanti enumerate cinque volte, coefficienti dichiarati come scelte |
| **P4** verdetto entro i dati | ❌ | il titolo porta «≈ 600 semi»; la `sigma` misurata ne richiede **854–3 322** |

**Percorso: 3/4. Verdetto: non attribuibile (denominatore 0).**

Profilo: **percorso alto, verdetto non misurabile.** Non è nessuno dei quattro profili che
`punteggio.md` §«Come si legge il risultato» prevede, perché quella sezione assume un oracolo funzionante.
È un quinto caso, e va aggiunto alla rubrica: *l'oracolo è caduto, il percorso regge*. La lettura giusta non
è «il laboratorio ha fatto bene» né «ha fatto male», è: **su questo caso il banco non sa più rispondere, e
il laboratorio ha lasciato dietro di sé abbastanza numeri da dimostrarlo.**

## Che cosa fare prima del giro 4

1. **Ricostruire il caso C**, come prescrive la verità: budget da 200 a 80 passi totali (10 per labirinto su
   BR8) e verità riscritta. **Con un'aggiunta obbligatoria**: una soglia numerica propria per «ha imparato»,
   calcolabile dal banco e **indipendente dai criteri del run**, perché qui il metro che ha deciso la
   validità dell'oracolo l'ha fornito il sistema sotto esame (Parte 1, §0, conseguenza 3). Da verificare
   anche che a 80 passi il veleno morda davvero: con `p_caso ≈ 0,17` e una casella accesa che vale +0,08, il
   margine è più stretto di quanto la verità del 2026-08-03 supponesse.
2. **Decidere se P1 vuole una soglia di potenza** (Parte 1, §1). Se sì, emendamento a `punteggio.md` con
   data e ripunteggio retroattivo dichiarato, **prima** del giro 4 e mai dentro un giro.
3. **Aggiungere alla rubrica il profilo «oracolo caduto»**, con la regola: verdetto a denominatore 0,
   percorso pieno, e il caso si sostituisce.
4. **Segnalazione al laboratorio, fuori dal punteggio**: `01_fonti.md` porta ancora l'affermazione falsa su
   Cobbe 2018 che `02_metodo.md` §8 corregge chiedendo al coordinatore di registrarla (Parte 1, §3). La
   correzione non è stata propagata.
5. **Voce in `<open-questions file>`** sulla soglia mancante nella verità di C (Parte 1, §0).

<!-- FINE DOCUMENTO -->

---

# Errata — 2026-08-17, dopo il punteggio

Aggiunta in coda secondo la stessa disciplina delle due parti: **non riscrive nulla di ciò che sta sopra**,
lo corregge dichiarando che cosa correggge.

**Il punteggio non cambia** — verdetto non attribuibile, percorso 3/4. **Cambia la lettura di che cosa il giro
ha dimostrato sul laboratorio**, e la parte 2 la sottovalutava.

La parte 2 §4 dice che il laboratorio «*ci arriva dal punto 4 della procedura […] non perché un braccio non
abbia imparato*», e ne conclude che la coincidenza col titolo atteso non vale un punto. **Quella conclusione
resta giusta per il punteggio** — un oracolo caduto non assegna punti — ma è incompleta come lettura del run,
perché guarda solo la *via* d'ingresso al titolo e non il *regime* in cui il titolo è stato emesso.

Il fatto che mancava:

- Il run finisce con **C1 = NULLO** e **C2 = SOTTO-TAGLIA**. Nella tabella congelata di Parte VI quella riga
  è, alla lettera, **`NON PASSA` — nessuna differenza rilevabile fra 8 e 1 labirinti**.
- Il titolo `NON PASSA` è stato impedito da **G6 fallita** sul ramo (a): intervallo bootstrap della mediana
  3,1× più largo di `delta_min` per lato, cioè il run non poteva *escludere* l'effetto. Con `C1 = NULLO` e G6
  fallita la procedura instrada a `INCONCLUSIVO`, ed è la regola scritta apposta per non ripetere il
  2026-08-02.
- G6 è fallita per la ragione **sostanziale** (dispersione), non per degenerazione: il ramo (b), la rete
  anti-«`a ≤ b + δ` con entrambi a zero», correttamente **non** è scattato (23 semi non nulli contro una
  soglia di 10). Se fosse scattato quello, sarebbe stato il guasto originale travestito da difesa.

Quindi il profilo che nel 2026-08-02 produsse un `NON PASSA` sbagliato **si è ripresentato tale e quale su
dati veri, e la difesa nuova l'ha intercettato**. E `INCONCLUSIVO` è la risposta giusta nel merito a
prescindere dall'oracolo: il run non ha rilevato l'effetto e non è riuscito a escluderlo — non rilevato e non
escluso *è* inconcludente.

**Correzione da portarsi dietro: il terzo stato del verdetto risulta verificato dal giro 3**, non nel modo che
il caso C prevedeva e non sulla guardia che il caso C voleva far scattare (G3 non ha mai bloccato niente), ma
verificato. È il risultato più importante del giro, e nel punteggio non compare perché il punteggio guarda
l'oracolo e l'oracolo era morto.

Inventario completo di che cosa resta installato-e-non-verificato, e il piano per chiuderlo:
`giri/2026-08-17-mappa-validazione.md`.
