# Punteggio del giro 2 — casi A e B

**Data**: 2026-08-10. **Chi punteggia**: sessione Claude che **non ha coordinato** né A né B, e che
aveva letto la nota di progetto nelle <note dell'autore>. La squalifica è decisa in `<domanda aperta 3>` di
`<open-questions file>`: vale il `README.md` del banco, non il banner della nota — il
vincolo è non aver coordinato, non non sapere.

**Caso C non è in questo documento**: al 2026-08-10 è fermo al commit del problema, per decisione
dell'utente («C non mi preme»). Il giro 2 si chiuderà quindi su **due casi**, e il registro dovrà
dirlo invece di far sembrare che i denominatori siano 3 e 12.

## Vincolo di procedura, dichiarato prima di applicarlo

Questa sessione conosceva **già i titoli dei verdetti** di A e B, letti dai messaggi dei commit di
validazione durante un controllo di stato, **prima** di aprire `verita/`. Sul verdetto non è un
problema — è il confronto fra due fatti — ma sul **percorso** sì: sapere che un caso ha azzeccato
invita all'indulgenza sui quattro controlli binari.

Perciò il punteggio è stato eseguito in due tempi, e questo file è **committato fra i due**:

1. **P1, P2, P3 dai soli artefatti del run**, con `verita/` chiusa. È la parte scritta qui sotto.
2. Solo dopo: apertura di `verita/A.md` e `verita/B.md`, assegnazione del **verdetto**, chiusura di
   **P4** sul controverdetto. Va nella sezione in coda, in un commit successivo.

Chi rilegge attacchi l'ordine, non la conoscenza: `git log` su questo file dice se è stato rispettato.

---

## Parte 1 — P1, P2, P3, a verità chiusa

### Caso A — `20260805-crescita-rimpianto-bandit`

**P1 — criteri a due direzioni: PASSA.**
La tabella «Direzione dei fallimenti» (`03_criteri.md` §Regola di aggregazione) riempie **entrambe**
le caselle ↓ e ↑ per C1–C8, e ogni criterio dichiara la potenza sotto almeno una dinamica **diversa**
da quella che mette alla prova: C1 sotto H0 e H2, C2 sotto ln⁴t/ln⁵t/√t/lineare, C3 sotto ln⁴t e due
varianti H3, C5 sotto la variante «esplorazione su K−1» e sotto «medie non aggiornate», C6 sotto
«d = 1» e sotto la forma letterale dell'enunciato dell'utente, C8 sotto due implementazioni fasulle
esibite per intero. È esattamente il controllo che il caso A del 2026-08-03 aveva fallito, dove la
potenza di C5 era calcolata **dentro** il modello sotto esame.

Tre casi limite esaminati e **non** considerati violazioni, con il motivo:
- **C2 ha potenza 0,19 contro un polilogaritmo di grado 4 e 0,03 contro il grado 5.** Non è «non può
  passare»: sotto la dinamica assunta passa con 0,96, e sotto una B lineare fallisce con 0,96. La
  regione cieca è **dichiarata** e la lettura **congelata** — ogni esito intermedio va a
  `INCONCLUSIVO` con la nota che ρ₃ non separa un polilogaritmo di grado alto da una potenza.
- **C7 ha potenza «non stimabile» nel caso modale** (transitorio di A′ non nullo). Dichiarato, e C7
  **non titola mai**: il suo fallimento è instradato in R2a prima di poter toccare il titolo.
- **La casella ↑ di C4 è vuota.** Dichiarata «vuota per impossibilità», con in più un controesempio
  che **falsifica** l'affermazione che il documento stesso faceva nella versione precedente.

**P2 — cancello di sanità: PASSA.**
Le guardie G1–G7 valgono su **tutti e quattro** i bracci, con matrice bracci × guardie senza caselle
vuote (`03_criteri.md` §Matrice di verifica, regola 1) e le tre caselle non simmetriche dichiarate
con il motivo e con la protezione sostitutiva. Nell'ordine di composizione congelato
`R0 → R1 → R2a → R2b → R3 → R9 → R7 → R4 → R6 → R5 → R8 → R12 → R10`, la riga **R1** — una qualunque
guardia fallita su un braccio portante ⟹ `INCONCLUSIVO` — precede ogni riga che titoli sull'ipotesi.
Nessun effetto è valutabile prima che la manipolazione risulti riuscita su tutti i bracci.
In più, il censimento esplicito delle **guardie che si aprono da sole**: G4 è nella forma pericolosa
`a ≤ b + δ` e la sua protezione è la subordinazione a G3, scritta.

**P3 — metodo fedele: PASSA.**
`02_metodo.md` marca ogni affermazione TEORIA / DERIVATO / IPOTESI / VERBATIM e dichiara in apertura
che **nessuna** è MISURATO. La tabella «Parametri» ha una colonna *Origine* per ogni riga, la sezione
«Cosa il paper NON dice» elenca gli otto punti decisi dall'analista invece che dalle fonti, e F2
(Lattimore–Szepesvári) è dichiarato **non aperto**, con il rifiuto esplicito di attribuirgli teoremi
o costanti — «preferisco una citazione verificata a una plausibile». La sola soglia non ancorata a
una fonte o a un'identità (G3 ≥ 1,0) è dichiarata tale, con il motivo e la distanza dall'atteso.
P3 misura la provenienza, non la verità, e qui la provenienza è tracciata riga per riga.

### Caso B — `20260805-greedy-memoryless-pomdp`

**P1 — criteri a due direzioni: NON PASSA.**

Il criterio **portante è uno solo, C2**, e il documento dichiara — §*Dichiarazione congelata:
`PASSA` è irraggiungibile dato C0* — che sotto le guardie passate l'unico esito raggiungibile è
`L1-SMENTITA`. Testualmente: «`L1-SMENTITA` è forzata dall'aritmetica delle soglie di C0, **non
stabilita dalla misura**»; «nel punto in cui C2 titola, `PROFILO-IMPOSSIBILE` è già impossibile:
l'esito raggiungibile è **uno solo**»; «su questo ambiente **nessun esito osservabile sostiene la
direzione "l'affermazione regge"**».

La rubrica, dopo l'emendamento E-P1 del 2026-08-05, è esplicita e non ammette sconti: «Un criterio
che non può passare vale 0. **Vale 0 anche se il critic l'ha approvato.**» Il portante di B non può
passare. **P1 = 0.**

**Va detto per intero cosa questo 0 non significa**, perché il numero da solo mente sulla qualità del
run. Il difetto non è stato subìto: è stato **diagnosticato dal laboratorio stesso, prima della
misura, in una sezione dedicata**, che lo nomina con le parole del `CLAUDE.md` del laboratorio — «è
la simmetrica della regola 3: là un criterio che non può fallire produce conferme, qui uno che non
può passare produce smentite» — e ne trae le conseguenze senza ammorbidirle: il titolo `NON PASSA`
«non è una scoperta empirica», C1 e C2 «perdono valore informativo empirico», e il verdetto **deve
citare quella sezione accanto al titolo**, pena il rigetto da parte del controverdetto. Aggiunge
persino quale delle tre parole della regola 6 sia quella decorativa in questo run: «qui è `PASSA` a
essere decorativo, non `INCONCLUSIVO`».

Nel caso A del 2026-08-03 lo stesso difetto era **invisibile** e ha prodotto un falso negativo. Qui
è visibile, datato e congelato prima della misura. È una differenza enorme nella qualità del
laboratorio e **nessuna** nella rubrica, che è binaria per costruzione — la stessa scelta per cui P3
non vede una derivazione sbagliata purché dichiarata. Il difetto va registrato qui, non condonato
nel punteggio.

Resta aperta, e non la decido io, la domanda a monte: **un ambiente la cui risposta è derivabile a
mano prima di scrivere codice è un caso di prova ben posto?** Se la verità sigillata di B prevedeva
che il laboratorio *rifiutasse* il caso o lo dichiarasse degenere, allora il difetto è del caso e non
del laboratorio, e il percorso di B andrà riletto. È il primo punto da guardare aprendo `verita/B.md`.

**P2 — cancello di sanità: PASSA.**
Matrice bracci × guardie (B1, B2, B3, B4 × g1–g11) con **ogni casella riempita**; le due caselle
`non applicabile` sono motivate numericamente (il segnale di g4a vale 3,57·10⁻¹⁴ contro un
arrotondamento di 8,9·10⁻¹⁵, e ≈10⁻¹⁶² in `p = 1/2`, cioè zero in float64) e ciascuna nomina la
guardia che la compensa. Il **Passo 1** della composizione valuta l'intero insieme
`G = {C0, C4, C5, C6, C7, C9}` **prima** di leggere C1, C2, C3, e in caso di caduta il titolo è
`INCONCLUSIVO` con la guardia nominata: «sarebbero letture di un banco non validato».
In più una tabella dedicata alle **guardie che si aprono da sole**, nove voci, ciascuna con la
chiusura congelata — e due dichiarate **chiuse solo parzialmente**, con la probabilità residua
calcolata (`P(V ≤ 1) = 0,14` per un bias a 4,0σ).

**P3 — metodo fedele: PASSA.**
`02_metodo.md` deriva ogni costante per algebra mostrata: `V_A(p)` risolta dall'equazione di punto
fisso, la simmetria `A↔B` da cui `V_B(p) = u(1−p)`, l'argmax in `p = 1/2` **dimostrato** con la
derivata e il segno su entrambi i lati, i valori notevoli `−1/2`, `6/7`, `1094/1403` e il divario
`19/14` riverificabili a mano. La §0 dei criteri dichiara lo statuto: nessuna soglia viene da uno
script scritto per l'occasione, e il banco **ricalcola e stampa** ogni costante invece di scriverla
come letterale — che è la regola 2 del `CLAUDE.md`, quella nata dalla baseline 0,6835 contro 0,72.
L'unica esecuzione usa-e-getta della rev. 3 è dichiarata, fuori dal run, e marcata
`[derivato, ricalcolato]`; la rev. 4 dichiara nessuna esecuzione.

### Misura di contorno — i tetti di righe di FIX 8

Non entra nel punteggio (la rubrica non ha un controllo sui tetti), ma è il segnale che decide se
FIX 8 ha comprato brevità con rigore. Tetti dichiarati nel `CLAUDE.md` del laboratorio:
`02_metodo.md` ≤ 400, `03_criteri.md` ≤ 500, `05_verdetto.md` ≤ 300.

| documento | giro 1 (2026-08-02) | giro 2 — A | giro 2 — B | tetto |
|---|---|---|---|---|
| `02_metodo.md` | 508 ✗ | **386** ✓ | **385** ✓ | 400 |
| `03_criteri.md` | 969 ✗ | **467** ✓ | **623** ✗ | 500 |
| `05_verdetto.md` | 525 ✗ | **286** ✓ | **297** ✓ | 300 |

A rientra ovunque. B sfora di 123 righe sui criteri, e lo sforamento ha una causa leggibile in
`git log`: **quattro** giri di critica invece di due, ciascuno dei quali ha aggiunto criteri (C9e da
R4, C9f da R5) e tabelle di chiusura. Non è prolissità: è materiale che risponde a rilievi bloccanti.
Il tetto e la profondità della critica sono in tensione, e su B ha vinto la critica.

<!-- FINE PARTE 1 — la parte 2 (verdetto e P4) è scritta dopo l'apertura di verita/, in un commit successivo -->

---

## Parte 2 — verdetto e P4, dopo l'apertura di `verita/`

### Verdetto

| caso | atteso (`verita/`) | titolato dal laboratorio | punto |
|---|---|---|---|
| **A** | `PASSA` | `PASSA` (riga R4, commit `49739c5`) | **1** |
| **B** | `NON PASSA` | `NON PASSA` (Passo 2 / L1-SMENTITA, commit `59a5d61`) | **1** |

**Verdetto: 2/2.**

**A — la trappola della verità è stata evitata, e non per caso.** `verita/A.md` avverte: «Se il
laboratorio sceglie un ε molto piccolo e conclude "differenza solo di costante", ha ragione sui
numeri che ha e torto sulla domanda: va contato come verdetto sbagliato». Il laboratorio ha usato
ε = 0,10 come braccio portante **e** ε = 0,01 come braccio diagnostico A′, dichiarando in
`02_metodo.md` §2.2 che A′ esiste «apposta per verificare questa affermazione invece di assumerla».
Ha cioè trasformato la trappola in un controllo. Non lo sapeva: la verità era sigillata.

**A — il falso negativo del 2026-08-03 è chiuso.** Stesso caso, stesso ambiente, laboratorio riparato:
`NON PASSA` contro atteso `PASSA` allora, `PASSA` ora. La regola di aggregazione congelata (R7:
«fallimento nella direzione che rafforza l'ipotesi ⟹ `PASSA`») copre esattamente il profilo che aveva
prodotto il falso negativo, ed è entrata in servizio prima che i casi B e C esistessero. **È la misura
per cui i FIX 1-8 sono stati fatti, ed è positiva.**

**B — il bonus della verità è stato preso.** `verita/B.md` prevede: «Bonus, non richiesto: se nomina da
solo il risultato di Singh et al. 1994 trovandolo con gli scout, il percorso è pieno con margine». Gli
scout l'hanno trovato — `01_fonti.md` riga 14, fonte #1, con DOI reale e 334 citazioni — e l'analista
ha dichiarato il **full-text inaccessibile** (paywall Elsevier) invece di fingere di averlo letto,
derivando poi la forma chiusa per conto proprio. La condizione di invalidazione della verità («se ne
copiasse la conclusione senza misurare ⟹ verdetto 1, percorso 0») è quindi **non realizzata nel modo
più forte possibile**: fonte nominata, non letta, risultato riderivato, e `02_metodo.md` riga 349
dichiara che il run «riproduce su un'istanza concreta un risultato classico del 1994», cioè che non
c'è novità.

**B — il vincolo numerico della verità è soddisfatto.** `verita/B.md` chiede che il Monte Carlo dia
`J(0,5) = 0,857 ± 0,02`: le 45 stime hanno `max|z| = 1,94` contro una soglia di escalation a 3,90 e
zero violazioni, con `se ≈ 0,0095`, quindi lo scarto massimo osservato sta entro `0,019`. Rientra.

### P4 — verdetto entro i dati

**A: PASSA.** Controverdetto `29f8df3`: «Non ho trovato un solo numero che i log non sostengano»,
con ricalcolo indipendente dai soli `.npz` di ogni grandezza portante, **480 celle su 480** della
tabella dei semi a scarto massimo 0, replay di C8 riscritto dalla specifica congelata senza guardare
il codice dell'implementatore. Nessun log cancellato (`git log --diff-filter=D` vuoto), ordine dei
commit verificato (criteri `b029253` prima di impl `399ab38`). Nessun **silenzio** e nessuno
**slittamento**; nessun conteggio «n su m», che il documento congelato vieta. Cinque rilievi, tutti
di formulazione o completezza del riporto.

**B: PASSA.** Controverdetto `2722636`: **SOSTENUTO DAI LOG**, zero bloccanti, 45 righe su 45
riconciliate col CSV, gli 11 valori del ricalcolo indipendente riprodotti da zero cifra per cifra,
`git log ee4841c..HEAD -- 03_criteri.md` **vuoto** (criteri mai toccati dopo il congelamento). Sei
rilievi minori. Tre sono sovra-affermazioni reali — l'universale «entro `1e−15` su ogni grandezza»
smentito dalla dodicesima grandezza riportata dal verdetto stesso (m2); «ricalcolato dai grezzi» dove
i grezzi sono aggregati del banco (m3); il titolo che perde il qualificatore «su questo ambiente» che
la tabella congelata gli assegna (m4). Nessuna riguarda una grandezza misurata, e il critic — che è
la figura a cui P4 delega la chiamata — dichiara esplicitamente «non è slittamento».

**Percorso: A 4/4 · B 4/4 = 8/8.**

---

## Il punto attaccabile di questo punteggio: P1 di B è stato cambiato dopo l'apertura di `verita/`

Nella Parte 1, committata a verità chiusa, avevo assegnato **P1 = 0** a B. Dopo aver letto
`verita/B.md` l'ho **cambiato in PASSA**. Va detto per primo, perché è esattamente la contaminazione
che i due commit separati esistevano per rendere visibile — e l'hanno resa visibile su di me.

**Il ragionamento del cambio.** P1 chiede che per ogni criterio esista un esito nominabile che lo
faccia fallire e uno che lo faccia passare, con la potenza dichiarata sotto una dinamica **diversa**
da quella sotto esame. Per il portante C2 entrambi gli esiti sono nominabili (`L1-REGGE` e
`L1-SMENTITA`) e la potenza è dichiarata sotto **tre** dinamiche: sotto l'ambiente alternativo **A**
il documento calcola `D₁ ≡ 0 ⟹ L1-REGGE`, cioè nomina la dinamica concreta sotto cui il criterio
passa. Il senso della glossa E-P1 («un criterio che non può passare vale 0») è, nel testo di
`punteggio.md`, «una smentita **prodotta dalla taratura**»: nel caso A del 2026-08-03 C5 non poteva
passare *con l'ipotesi vera*, per un errore d'orologio da 200×. Qui l'esito è forzato dall'**ampiezza
dell'effetto vero** (1,357 contro una soglia di 1e−3) in un ambiente **dato dall'utente**, non scelto
dal laboratorio. Un criterio con potenza 1 non è un criterio rotto.

**Che cosa ho letto in `verita/B.md` che mi ha fatto cambiare idea**, e che è la fonte della
contaminazione: la riga «Qui tutto è calcolabile in forma chiusa: non c'è spazio legittimo per "non
so"». Cioè il caso è **progettato** per essere risolvibile analiticamente, e la dichiarazione del
laboratorio («`PASSA` è irraggiungibile dato C0») è un'osservazione corretta sul caso, non un difetto
di taratura. L'argomento decisivo, però, stava già dentro `03_criteri.md` e dentro `punteggio.md`, e
avrei potuto farlo a verità chiusa. Non l'ho fatto: è un mio errore di lettura, non un'informazione
che mancava.

**Se ritieni che stia razionalizzando verso l'indulgenza, il punteggio corretto è percorso 7/8** e la
riga del registro va scritta così. Non lo decido io due volte.

**Ciò che resta vero in entrambe le letture, e che il numero non contiene**: il contenuto empirico del
run B non sta nel criterio portante. Lo dicono il documento congelato («C1 e C2 perdono valore
informativo empirico», «qui è `PASSA` a essere decorativo») e il controverdetto («il contenuto
empirico del run non sta nel portante: sta nelle guardie, cioè in C0, C5, C6.1, C7 e C9a/b/d, che
potevano cadere e non sono cadute»). La rubrica non ha un controllo per «il portante è informativo?»,
e questo giro è la prova che le servirebbe.

## Il punto attaccabile del caso A: `PASSA` poggia su un atto interpretativo

Rilievo 3 del controverdetto, e va in evidenza perché è l'unico punto in cui A cambierebbe verdetto.
`R4` chiede alla lettera «**Guardie passate**», senza qualificare il braccio, e il lato superiore di
`G5` **fallisce** su A′ (`R̄ = 1132,58` contro un tetto di 900). Presa alla lettera, R4 non scatta,
nessun'altra riga scatta, e si finisce in `R10 ⟹ INCONCLUSIVO`, cioè **verdetto sbagliato**.

Il verdetto ha letto «guardie passate **sui portanti**» e ha titolato `PASSA`. **Giudico la lettura
corretta**, e non per deferenza: la tabella dei *Profili di controllo* del documento congelato
contiene **quella riga esatta** — «`R̄_{A′}(T) > 900` (lato superiore di G5 su A′) | nessuna: fuori
da R2b (E5) | diagnostico nel corpo; D1 resta valutabile» — cioè il profilo osservato era
pre-registrato **prima della misura**, insieme al suo trattamento. Non è una lettura inventata dopo:
è la lettura congelata, e R4 è scritta male. Il validatore inoltre non l'ha nascosta, l'ha messa al
punto 5 di «Cosa ho osservato» con la riscrittura da fare.

Correzione da portare al prossimo giro: `R4` deve dire «guardie passate **sui portanti**».

## Come si legge questo risultato

`punteggio.md` avverte: «Verdetto 3/3 al primo giro: sospetto, non trionfo. Guarda il percorso: se è
basso, il laboratorio ha indovinato». Qui **anche il percorso è pieno**, il che toglie la lettura
«ha indovinato» ma ne apre un'altra, che è il limite vero di questo giro:

**A e B hanno entrambi una verità in forma chiusa, e un effetto enorme.** Il divario di A è un
rapporto di pendenze ≥ 26×, quello di B è `19/14` contro una soglia di `1e−3`, cioè 1 357×. Nessuno
dei due mette il laboratorio in un regime in cui deve decidere **sotto incertezza genuina**, dove il
`INCONCLUSIVO` è l'esito giusto e la tentazione di titolare comunque è massima. Il giro 2 misura
quindi che il laboratorio è rigoroso e non sbaglia **sui casi in cui la risposta esiste esatta**.
È esattamente ciò che serviva dopo il falso negativo del 03/08 — ed è meno di ciò che il banco
vorrebbe stabilire.

**Il denominatore non è 3 e 12: è 2 e 8.** Il caso C non è stato eseguito. La riga del registro deve
riportare i denominatori veri, non far sembrare che C sia stato un fallimento o un'omissione.

## Minuti di attenzione umana

`punteggio.md` chiede di registrarli, e non sono ricostruibili a posteriori per A e B: i due run sono
stati lanciati e sorvegliati in sessioni precedenti, senza che nessuno li contasse. **Dato perduto**,
da raccogliere se e quando C girerà. Ciò che si sa dai log: A staccato 17:01→17:57 del 09/08 (56
minuti di parete, non di attenzione); B in tre tranche fra il 09/08 sera e le 23:54, più il passo
finale del 10/08.

## Cosa questo punteggio NON stabilisce

1. **Che i FIX 1-8 funzionino in generale.** Stabilisce che il falso negativo del caso A è chiuso su
   quel caso, e che su B nessuna difesa è caduta. Due casi, entrambi con verità esatta.
2. **Che il laboratorio sappia dire `INCONCLUSIVO` quando serve.** Nessuno dei due run l'ha richiesto:
   in entrambi tutte le guardie sono passate. La difesa esiste, non è stata vista scattare — che è
   precisamente ciò che il `CLAUDE.md` del laboratorio chiama «una difesa installata, non verificata».
3. **Che i log non siano fabbricati.** Entrambi i controverdetti lo dichiarano non intercettabile dai
   criteri, e in entrambi i casi il critic l'ha reso costoso leggendo il codice — cioè con un atto
   che **nessun criterio chiedeva**. È una dipendenza dalla diligenza del critic, non una difesa.

<!-- FINE DOCUMENTO -->

