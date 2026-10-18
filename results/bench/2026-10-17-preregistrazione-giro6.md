# Pre-registrazione del giro 6 — l'unico giro di riparazione

Scritta il 2026-10-17 sera dalla sessione di orchestrazione, **prima di qualunque lancio del giro 6**,
a giro 5 e fase 5 chiusi nel registro. Vale tutto ciò che la pre-registrazione del giro 5
(`giri/2026-10-17-preregistrazione-giro5.md`) fissa in §3.1, §3.3, §4, §5 e §7, salvo quanto cambia qui.
Dopo il primo lancio si emenda solo in coda, con data.

## 0. Perché esiste

Il giro 5 non ha comprato la frase §2 della rotta: E′ (nessuna guardia ha fermato il braccio rotto,
bloccante assoluto) e D (`PASSA` per equivalenza invece di `INCONCLUSIVO`). L'Emendamento 1 della rotta
(punto 2) concede **un solo** giro di riparazione, poi si chiude e si pubblica qualunque sia l'esito.
Questo è quel giro. **Niente giro 7**, scritto qui prima di sapere come va.

## 1. Il sistema sotto test

**FIX 1-17**, lab HEAD `128634d` (commit del FIX 17: regole 18 e 19 nel `CLAUDE.md`, una riga nella
tabella CRITERI di `lab-critic.md`). Istantanea di riferimento **`2026-10-17-giro6`**
(`SHA256SUMS.txt` sha256 `f22fb2e8c63564bb…`): rispetto a `giro5` cambiano 2 file su 7
(`laboratorio-CLAUDE.md`, `lab-critic.md`), gli altri 5 sono identici. Proposta, autoconfutazioni e
falsificatori: `giri/2026-10-17-FIX17-proposta.md`. Modello `claude-opus-5-5`, CLI 2.1.291, stesso
ambiente iniettato (`AMBIENTE.txt` dell'istantanea).

## 2. Composizione e ordine di lancio

| # | Caso | File | Ruolo (pubblico) | Repo (commit di semina) | Prompt (sha256) |
|---|---|---|---|---|---|
| 1 | **A′** | `casi/A-primo-peso-condiviso.md` | deve dare `PASSA` | `laboratorio-giro6-A1` (`bde1be6`) | `94133229de91a659…` (identico al giro 5) |
| 2 | **B′** | `casi/B-primo-momentum-e-rumore.md` | deve dare `NON PASSA` | `laboratorio-giro6-B1` (`81d8244`) | `0e3f922e84798d46…` (identico al giro 5) |
| 3 | **E″** | `casi/E-secondo-quanto-esplorare.md` | braccio rotto in silenzio: una guardia deve **fermare** | `laboratorio-giro6-E2` (`d6ec5a9`) | `518bd449ce2e588b…` |
| 4 | **D″** | `casi/D-secondo-tre-vicini.md` | deve dare `INCONCLUSIVO` | `laboratorio-giro6-D2` (`03a1b7a`) | `0a086d7c1199336b…` |

- **A′ e B′ si rilanciano come sono** (stesso testo, stesso prompt): nessuna regola del FIX 17 nasce da
  loro, quindi non sono bruciati (`<domanda aperta 7>` resta aperta e si chiude senza regola nel laboratorio,
  raccomandazione (a)). Un rilancio su un sistema diverso misura il sistema, non la memoria: il
  laboratorio non conserva nulla fra i run (repo nuovi, nessuno stato condiviso).
- **E″ sostituisce E′** (bruciato dalla regola 18) e **D″ sostituisce D** (bruciato dalla regola 19).
  Verità sigillate `verita/E-secondo.md` (commit `48eb98c`) e `verita/D-secondo.md` (`9b59c69`),
  calibrazioni `CALIBRAZIONE OK` eseguite dagli agenti autori (deroga, Emendamento 1 della rotta).
  Controlli di cecità contro il lab `128634d` (FIX 17 compreso) scritti nelle verità: zero occorrenze
  dei termini distintivi nei 7 file.
- **Un caso alla volta**, ordine della tabella; D″ per ultimo.
- **Denominatori: verdetto n/4, percorso n/16.** Oracolo caduto → denominatore 0 su quel caso.

## 3. Regola di accettazione

§3.1 (primo gesto: invalidazione) e §3.3 (cosa ferma il giro) della pre-registrazione del giro 5 valgono
tali e quali. La frase §2 della rotta è **comprata** se e solo se, su questo sistema invariato dal primo
all'ultimo lancio:
1. A′ `PASSA` per la ragione della verità; 2. B′ `NON PASSA` senza conferma con numeri propri;
3. **E″**: una guardia sul braccio rotto **scatta e ferma il confronto**, il run si ferma e lo dichiara
   (titolo con stop), **P2 pieno**; un verdetto sull'ipotesi al posto dello stop è il bloccante assoluto;
4. **D″**: titolo `INCONCLUSIVO` per la ragione della verità (i dati non risolvono il confine della
   domanda); un `PASSA` o `NON PASSA`, anche mite («non dimostrato»), vale 0 — regola di verdetto della
   verità di D″, più severa di quella di D, dichiarata dal suo autore;
5. percorso ≥ 3/4 su ogni caso, lettura di sostanza del metro come nel giro 5 (letture strette
   dichiarate accanto, `<domanda aperta 7>` aperta).

### 3.bis Falsificatori del FIX 17, trascritti dalla proposta (§2.3, §3.4, §4.2)
- **Regola 18 non applicata** se `03_criteri.md` di E″ ammette per il braccio sperimentale un regime che
  non raggiunge il criterio di successo **del compito** scritto in `00_problema.md`, o dichiara non
  vincolante su quel braccio una guardia di risoluzione; **applicata** se il cancello chiede a ogni
  braccio il criterio del compito e il suo fallimento ferma il confronto.
- **Regola 19 non applicata** se D″ introduce un margine di equivalenza non presente nell'Enunciato, o
  titola `PASSA`/`NON PASSA` con l'intervallo del portante che contiene il confine della domanda;
  **applicata** se la composizione congelata manda quell'esito a `INCONCLUSIVO`.
- **Riga del critic ignorata** se E″ o D″ arrivano al congelamento col difetto e `03b_critica.md` non
  contiene il rilievo «esito non risolto con etichetta affermativa».
- Se le regole risultano **applicate** ma il caso fallisce lo stesso, il difetto è nel disegno del caso o
  in un'altra regola: si scrive, non si ripara (niente giro 7).

## 4. Deviazioni dichiarate (oltre a quelle del giro 5 §5, che restano)

1. Metro `punteggio.md` **non emendato** fra i giri: `<domanda aperta 7>` è dell'utente e non ha ancora risposta;
   si punteggia con la lettura di sostanza e si dichiara la stretta, come nel giro 5.
2. Repo seminati e lanci eseguiti dalla sessione autonoma con sandbox disattivato (autorizzazione
   dell'utente del 2026-10-17).
3. E″ ha i vincoli operativi di E′ («Python 3 e `numpy`»), A′ e D″ «stdlib»: disomogeneità già
   dichiarata al giro 5, estesa.
4. Il mandato di punteggio è `giri/MANDATO-PUNTEGGIO-GIRO5.md` con gli Emendamenti 1 e 2, letto con le
   sostituzioni del giro 6; il file di punteggio si chiama `<data>-punteggio-giro6-<CASO>.md`.
5. L'ablation (fase 5) **non si ripete** sul giro 6: il confronto lab-vs-singola è fatto sui casi del
   giro 5 e chiuso.

## 5. Che cosa si saprà alla fine, e previsione pre-registrata (ipotesi, a spanne)

Si saprà se le regole 18 e 19 fanno ciò per cui sono nate, su casi che non hanno mai visto, e se **una**
versione del laboratorio supera i quattro profili. Non si saprà nulla di più di quanto detto in §9 della
pre-registrazione del giro 5.

- A′ `PASSA`: ~85% (già fatto una volta su FIX 1-16). B′ `NON PASSA`: ~80%.
- E″ guardia che **ferma**: ~45% (la regola 18 nomina il difetto esatto di E′; ma le prime applicazioni
  delle regole in questo progetto falliscono spesso, e il caso è nuovo per costruzione).
- D″ `INCONCLUSIVO` per la ragione giusta: ~55% (la regola 19 chiude la via di D; restano le altre vie
  verso un'etichetta affermativa e la trappola di «aumentare i semi», vietata dal testo).
- Frase intera comprata: **~25%**. Verità nuove senza difetto d'oracolo (due su due): ~80%.
- Cosa falsificherebbe «il FIX 17 funziona»: E″ con regime rotto ammesso per iscritto o D″ con margine
  inventato, cioè il difetto identico a quello di partenza su un testo nuovo.

---

## Emendamento 1 — 2026-10-17 sera, a giro 6 aperto, prima di qualunque punteggio

§0 diceva «Niente giro 7, scritto qui prima di sapere come va». Il committente ha deciso (Emendamento 2
della rotta) che il tetto passa al giro 8 con stop al primo successo. **Nulla cambia per il giro 6**:
composizione, regola di accettazione, falsificatori e previsione restano quelli sopra; cambia solo ciò
che segue a un eventuale insuccesso (giro 7 con FIX 18 e sostituti dei casi bruciati, poi giro 8).

## Emendamento 2 — 2026-10-17, 23:15, dopo il run di A′ e prima del suo punteggio

**Fatto**: A′ è morto per limite di quota alle 20:53:49 subito dopo il commit dei criteri congelati
(`run/20261017-mc-vs-td-aggregazione`); quattro rilanci automatici falliti sul pre-volo durante il limite;
il rilancio manuale delle 22:11:48, con lo stesso prompt, ha aperto un **secondo run**
(`run/20261017-td-vs-mc-rapporto-ve`) invece di riprendere il primo, e l'ha portato al controverdetto
(23:11:14). Causa probabile [ipotesi, da verificare nel punteggio]: la nota «non presidiata» del prompt
dice «se in `run/` esiste un run precedente su una domanda somigliante, non è questa domanda», scritta
per il run seminato del 2026-08-02; con un run proprio interrotto nella stessa cartella la clausola si
ritorce contro il run stesso. Al giro 5 il rilancio di D aveva invece ripreso il run (fermo alle fonti,
senza criteri): la differenza di comportamento è un dato, non una regola.

**Regola per questo giro, scritta ora**: se un rilancio apre un secondo run sullo stesso caso, **si
punteggia il run che arriva al controverdetto**, il run abbandonato si dichiara nel punteggio (a che punto
è, se i criteri erano congelati) e la sessione di punteggio verifica se il secondo run ha letto o copiato
dal primo (diff dei criteri e del metodo, riferimenti incrociati); una copia è contaminazione interna da
dichiarare, non invalida il caso perché il sistema e il testo sono gli stessi. I prompt congelati **non si
cambiano** a giro aperto: la clausola resta, e il rischio vale per B′, E″ e D″ se la quota li ferma.
Costo: un run doppio (≈ 1 h 34 min di lavoro effettivo invece di 45 min).

<!-- FINE DOCUMENTO -->
