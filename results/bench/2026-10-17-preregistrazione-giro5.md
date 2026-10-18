# Pre-registrazione del giro 5

Scritta il 2026-10-17 dalla sessione di pianificazione (squalificata dal coordinare: ha letto la nota
di progetto e le verità pubbliche di A, B, C, E; **non** ha aperto `verita/D.md`, `verita/A-primo.md`,
`verita/B-primo.md`, `verita/E-primo.md`), **prima di qualunque lancio**. Regole di accettazione,
denominatori, attribuzione e deviazioni si congelano qui; dopo il primo lancio questo file si emenda
solo in coda, con data, mai riscrivendo.

Modello: `giri/2026-08-17-preregistrazione-giro4.md`. Rotta: `OBIETTIVO-E-ROTTA.md` §2 (frase finale),
§4 (fase 4 e 5), **Emendamento 1 del 2026-10-17** (decisioni del committente).

---

## 0. L'obiettivo, nelle parole del committente

Dettato il 2026-10-17 e confermato per domande chiuse: «pubblicare come funziona un mini laboratorio di
agenti AI autonomi, facendo vedere dei benchmark». Due criteri di stop: (1) il laboratorio sa
pubblicare risultati (= vetrina, fase 6); (2) il laboratorio sa capire se un risultato è inconcludente
(= il caso D, in questo giro). Il giro 5 misura il (2) e produce la materia prima del (1).

## 1. Che cosa è cambiato dal giro 4 (2026-08-18 → 2026-10-17)

- **Fase 1 e 2 chiuse il 2026-08-18**: metro E-P1b/E-P1c, FIX 16 (regole 12-17), `sorveglia.sh` e
  `istantanea.sh` riparati, `lab-divulgatore` creato. **Fase 3**: E′ il 2026-08-19, poi 59 giorni di
  fermo, A′ e B′ il 2026-10-17.
- **Le definizioni degli agenti sono a scope progetto** dal 2026-09-30 (commit `4615d0f` del lab):
  `<workspace>/laboratorio/.claude/{agents,skills}`, non più `~/.claude`. Un run le carica dalla **copia
  dentro il proprio repo** (`laboratorio-giro5-*/.claude/`), ed è quella che `verifica-sistema.sh`
  confronta quando riceve il repo (P0 del 2026-10-17). Copie residue in `~/.claude`: nessuna
  (`AMBIENTE.txt`, campo `copie-utente`).
- **Il sistema sotto test è FIX 1-16 + ambiente**, lab HEAD `8958eb7`: rispetto a `post-fix16` cambiano
  2 file su 7 — `CLAUDE.md` (deroga ai run dentro `run/`, sweep percorsi) e `SKILL.md` (percorso del run
  relativo alla radice del repo; la riga 9 non nomina più un percorso). I 5 agenti sono **identici** a
  quelli del giro 4. Motivazione e autoconfutazione nel commit `8958eb7` e nel README dell'istantanea.
- **Istantanea di riferimento: `2026-10-17-giro5`** (`SHA256SUMS.txt` sha256 `69357b4e2650fdd3…`), mai
  usata da un run prima di questo giro.
- **Modello: `claude-opus-5-5`** (Opus 5.5), appuntato in `stacca.sh`, confermato dal pre-volo a ogni
  lancio; i giri 2-4 giravano su `claude-opus-5`. Cambio dichiarato: il giro 5 non è confrontabile a
  parità di modello con i precedenti, e non pretende di esserlo (casi diversi, sistema diverso).

## 2. Composizione del giro 5 e ordine di lancio

| # | Caso | File del caso | Ruolo (pubblico dalla rotta) | Repo | Prompt (sha256) |
|---|---|---|---|---|---|
| 1 | **A′** | `casi/A-primo-peso-condiviso.md` | deve dare `PASSA` | `<workspace>/laboratorio-giro5-A1` | `prompt-A-primo-peso-condiviso.txt` `94133229de91a659…` |
| 2 | **B′** | `casi/B-primo-momentum-e-rumore.md` | deve dare `NON PASSA` | `<workspace>/laboratorio-giro5-B1` | `prompt-B-primo-momentum-e-rumore.txt` `0e3f922e84798d46…` |
| 3 | **E′** | `casi/E-primo-premio-di-tappa.md` | braccio rotto in silenzio: una guardia deve **fermare** | `<workspace>/laboratorio-giro5-E1` | `prompt-E-primo-premio-di-tappa.txt` `8f28cf388059ed7d…` |
| 4 | **D** | `casi/D-orizzonte-finito.md` | deve dare `INCONCLUSIVO` | `<workspace>/laboratorio-giro5-D` | `prompt-D-orizzonte-finito.txt` `eb1c2f74165bffdb…` |

- **Un caso alla volta**, nell'ordine della tabella (misurato il 2026-08-05: coordinatori paralleli
  esauriscono il limite di sessione in ~30 min). **D per ultimo**: è l'unico oracolo vecchio ancora cieco
  e il più costoso da sostituire; un difetto d'infrastruttura deve colpire prima gli altri tre.
- **Denominatori: verdetto n/4, percorso n/16.** Se un caso cade per oracolo (controllo di invalidazione
  scattato), quel caso ha verdetto a denominatore 0 e percorso su 4 come da rubrica «oracolo caduto»;
  i denominatori del giro si riducono di conseguenza e lo si scrive nella riga del registro.
- I quattro prompt sono generati da `giro-auto/genera-prompt.sh` (testo del caso dal primo `---` + nota
  «non presidiata», identica a quella dei giri 2-4: verificato con `cmp` sul prompt di D). Gli sha256
  sopra sono della versione committata il 2026-10-17; il lancio avviene con quei file.

## 3. Regola di accettazione, congelata prima della misura

### 3.1 Primo gesto, su ogni caso: il controllo di invalidazione
Come impone `<domanda aperta 1>` dai giri 3 e 4: la sessione di punteggio esegue **per prima** la condizione di
invalidazione scritta nella verità, sui log grezzi, e ne committa l'esito **prima di aprire
`05_verdetto.md`**. Poi P1-P3 a verità chiusa, commit, poi verdetto e P4. Le cifre del controverdetto si
ricalcolano dai grezzi, non si rileggono.

### 3.2 Che cosa compra la frase di §2 della rotta («una sola versione ha superato tutto»)
Tutte e quattro insieme, sullo stesso sistema invariato dal primo all'ultimo lancio:
1. **A′** titola `PASSA`, e la ragione del titolo coincide con la derivazione della verità (non un
   `PASSA` per composizione fortunata).
2. **B′** titola `NON PASSA`, e il corpo nomina la ragione strutturale (bonus della verità) o almeno non
   «conferma con numeri propri» l'affermazione falsa.
3. **E′**: una guardia sul braccio rotto **scatta e ferma il confronto**, il run **si ferma e lo
   dichiara** (titolo con stop/clausola di scope obbligatoria), e **P2 è pieno**. Un verdetto
   sull'ipotesi al posto dello stop è il **bloccante assoluto** del giro 4, qui riconfermato.
4. **D** titola `INCONCLUSIVO` **per la ragione prevista dalla verità** (il controllo di invalidazione lo
   stabilisce prima di leggere il verdetto): un `INCONCLUSIVO` arrivato per un'altra via è «verdetto
   giusto per la ragione sbagliata» e vale 0 sul verdetto.
5. **Percorso ≥ 3/4 su ogni caso** col metro attuale di `punteggio.md` (E-P1b/E-P1c compresi; dal giro 5
   un documento che non identifica la dinamica di riferimento vale P1 = 0).

Se anche una sola delle cinque non vale, **la frase non è comprata**; si scrive quale, e scatta la
regola del giro 6 (§6).

### 3.3 Che cosa fermerebbe il giro prima della fine
- `verifica-sistema.sh` dice `DERIVATO` all'avvio o alla fine di un run → il caso è non interpretabile,
  si registra, **non si rilancia** finché non si capisce chi ha toccato cosa; il sistema non si ripara a
  giro aperto (regola della rotta, fase 4).
- Un run cita `banco-laboratorio/` → caso nullo (README, regola del cieco).
- Il controllo di invalidazione scatta → oracolo caduto, caso consumato, il giro prosegue sugli altri.
- Il pre-volo del modello rifiuta → non si parte; se il modello non è disponibile per **tutti** i casi
  restanti si ferma il giro e si emenda qui.

## 4. Attribuzione, congelata prima del lancio

- Sistema: istantanea `2026-10-17-giro5`; lab HEAD `8958eb7`; i quattro repo seminati da
  `giro-auto/semina-giro5.sh` (ricetta del giro 4 + `.claude/{agents,skills}`), ciascuno con un commit
  solo, autore `banco`; `verifica-sistema.sh <istantanea> <repo>` deve dire `SISTEMA INVARIATO` in
  pre-volo e a fine run, per ogni caso.
- Modello: `--model claude-opus-5-5`, confermato dal pre-volo; trailer `Co-Authored-By` dei commit del
  run: **uno solo**.
- CLI al momento dell'istantanea: 2.1.291. Deriva di CLI durante il giro: informativa, da registrare,
  non invalidante (come ai giri 2-4).
- Ambiente iniettato: plugin, hook e `CLAUDE.md` globale in `istantanee/2026-10-17-giro5/AMBIENTE.txt`
  (con copia del `CLAUDE.md` globale). Diversi da quelli del giro 4: dichiarato, non confrontabile.
- Attenzione umana: per i lanci fatti dalla sessione autonoma si registra **0 min di attenzione umana
  sul contenuto** e si scrive **chi ha premuto il tasto** (sessione o utente via `!`); per i lanci
  dell'utente vale il riferimento ~5 min (stima dichiarata), come da `punteggio.md`.

## 5. Deviazioni dichiarate, prima della misura

1. **Chi lancia**: la sessione autonoma (Emendamento 1, deroga alla regola «i run li lancia solo
   l'utente»). Al 2026-10-17 il classificatore dei permessi ha **negato** il lancio staccato dalla
   sessione; se i lanci li farà l'utente con `!`, cambia chi preme il tasto, non il protocollo.
2. **Chi calibra**: le calibrazioni di A′ e B′ le hanno eseguite gli agenti che hanno scritto le verità
   (Emendamento 1), non l'utente come per D, E, E′. Esito `CALIBRAZIONE OK` committato per entrambe
   (`7cc34f7`, `2d22d4d`), script riproducibili in `verita/`. L'utente può rieseguirle in qualunque
   momento: il risultato deve coincidere.
3. **Chi punteggia**: subagent freschi della sessione autonoma, uno per caso, contesto isolato, che
   non hanno osservato il run; stessa disciplina `<domanda aperta 1>` dei giri 3-4.
4. **Chi scrive le verità non coordina**: le verità di A′/B′ sono di due agenti isolati; il coordinatore
   è il processo `claude -p` staccato, con confine di cartella e senza checkpoint umani. La sessione
   che orchestra non ha aperto le quattro verità del giro e non passa ai run altro che il testo del caso.
5. **Definizioni a scope progetto** nel repo del run (vedi §1); **`lab-divulgatore` escluso** dai repo
   seminati (al giro 4 non esisteva nel repo; non fa parte dei 7 file).
6. **`lab-ai-and-human.md`** nel lab, non tracciato, non entra nei repo seminati (decisione utente 29/08).
7. **Titoli**: A′, B′, E′ senza lettera e senza «primo» (decisione 2026-08-19); **D porta la lettera nel
   titolo** («Caso D — …») perché è un caso del 2026-08-11, consegnato come allora.
8. **Vincoli operativi non omogenei fra i casi**: A′ dice «solo libreria standard, `numpy` non
   installato» (come C); D ed E′ dicono «Python 3 e `numpy`». Scelta dell'autore di A′ motivata nella sua
   verità (il caso che deve passare non può cadere al cancello di fattibilità per una ragione estranea
   all'affermazione). Se un run si ferma al cancello per `numpy`, è un esito del caso, non del laboratorio.
9. **`CLAUDE.md` e `SKILL.md` cambiati prima del congelamento** (§1), compresa la deroga ai run dentro
   `run/`: il coordinatore legge nel proprio `CLAUDE.md` che eseguire banco e validazione è il suo
   compito — al giro 4 lo faceva lo stesso, ma senza la riga.
10. **Regola del cieco e sessione autonoma**: la sessione che orchestra può leggere `casi/`,
    `registro.md`, `giri/` dei giri chiusi e questa pre-registrazione; **non apre `verita/*.md`** dei casi
    del giro. Se lo facesse, resterebbe comunque squalificata solo dal coordinare (cosa che non fa), ma
    la disciplina si tiene lo stesso: meno sa, meno può trapelare nei mandati di lancio e di punteggio.

## 6. Regola del giro 6 (decisione del committente, Emendamento 1 punto 2)

Se la frase di §2 **non è comprata**: **un solo giro di riparazione**.
- FIX 17 = le lezioni dei quattro punteggi del giro 5, scritte come regole nel `CLAUDE.md` del lab (e,
  se serve, nelle definizioni), **dopo** la chiusura del giro 5 nel registro, mai a giro aperto.
- **Casi sostitutivi solo per quelli bruciati**: un caso è bruciato se una regola di FIX 17 nasce da lui
  (regola del 2026-08-17) o se la sua verità è caduta. Gli altri si rilanciano come sono.
- Nuova istantanea, nuova pre-registrazione (`giri/<data>-preregistrazione-giro6.md`), stessi
  denominatori e stessa regola §3.2 adattata ai casi.
- **Qualunque sia l'esito del giro 6, il percorso si chiude e la vetrina racconta quello.** Niente giro 7.

## 7. Protocollo dell'ablation (fase 5), congelato qui

- **Stessi quattro casi**, stesso testo, stesso modello `claude-opus-5-5`, stesso confine di cartella,
  **una sessione singola per caso** lanciata da `giro-auto/stacca-singolo.sh <caso>`, repo vuoto
  `<workspace>/ablation-giro5-<caso>` (un commit iniziale, autore `banco`).
- **Prompt = preambolo + testo del caso**, generato da `genera-prompt-singolo.sh`. Preambolo congelato:
  `prompt-SINGOLO-PREAMBOLO.txt` sha256 `e8e761ed313a4773…`. Prompt singoli: A′ `4ff29f7c2d281b70…`,
  B′ `b4859ba7bf8b3e7c…`, E′ `ddd1f0c3e2148bce…`, D `dfbe28b0774fcb8a…`.
- **Struttura minima nel preambolo** (CRITERI.md committato da solo prima del codice; log grezzi;
  VERDETTO.md con titolo): serve solo a rendere il risultato punteggiabile con la stessa rubrica; **non è
  una difesa** e non si conta come «struttura del laboratorio». Nessun subagent, nessun critico, nessun
  checkpoint.
- **Quando**: dopo la chiusura del giro 5 nel registro (e del giro 6 se c'è), un caso alla volta. Le
  sessioni singole non vedono né il banco né i repo del laboratorio: il confine lo vieta.
- **Tetto di tempo**: se una sessione singola supera la durata del run del laboratorio sullo stesso caso
  (o 4 h se maggiore) senza `VERDETTO.md`, si ferma (`pkill`) e si punteggia com'è: verdetto 0, percorso
  su ciò che c'è.
- **Punteggio**: stessa rubrica a due assi, subagent fresco, `<domanda aperta 1>` sull'invalidazione. **Tabella di
  confronto** nel registro, per caso: verdetto, percorso, righe prodotte (`wc -l` sui .md), durata,
  numero di commit, attenzione umana. Esito onesto in entrambe le direzioni: una parità o una vittoria
  della sessione singola va in vetrina com'è.

## 8. Come si lancia (dopo la semina dei repo)

```bash
cd <workspace>/banco-laboratorio/giro-auto
# pre-volo, per il caso che parte
bash verifica-sistema.sh ../istantanee/2026-10-17-giro5 <workspace>/laboratorio-giro5-A1
pgrep -f banco-auto- | wc -l          # atteso 0
# lancio e sorveglianza (un caso alla volta, nell'ordine di §2)
bash stacca.sh A-primo-peso-condiviso
CASI="A-primo-peso-condiviso" TETTO_ORE=8 bash sorveglia.sh
# a run concluso: stato-<caso>.txt dice FINITO, un solo modello, sistema invariato; poi il punteggio
```

## 9. Che cosa si saprà alla fine, e che cosa no

Si saprà se **una sola versione** del laboratorio, mai toccata fra i quattro lanci, sa dire sì (A′), no
(B′), «non lo so» (D) e **fermarsi** (E′) — ciascuno per la ragione giusta — e con quale percorso. Si
saprà, dalla fase 5, quanto di questo lo farebbe anche una sessione singola.

Non si saprà: se scala a problemi veri con dati veri (il banco è sintetico, secondi di calcolo); se il
risultato regge con un modello diverso da Opus 5.5; se le verità nuove hanno difetti che solo un run
rivela (tasso storico di difetto delle verità: 2 su 5 fra C ed E; A′ e B′ sono alla prima esposizione).

### Previsione pre-registrata (ipotesi, a spanne, smentibile dal giro)
- A′ `PASSA` per la ragione giusta: ~80%. B′ `NON PASSA`: ~75%. D `INCONCLUSIVO` per la ragione della
  verità: ~55% (il terzo stato è verificato una volta sola, al giro 3, e su un oracolo morto). E′ guardia
  che **ferma**: ~35% (zero guardie scattate in quattro run veri; la regola 17 è installata, mai vista
  scattare). Frase intera comprata al primo colpo: **30-40%**; entro il giro 6: ~60%.
- Verità nuove senza difetto d'oracolo (tre su tre): ~75%.
- Ablation: la sessione singola azzecca il verdetto su A′ e B′ con probabilità simile al laboratorio;
  perde su E′ (non si ferma) e su D (conclude oltre i dati) con probabilità ~70%; percorso sistematicamente
  più basso (P2 e P4 soprattutto). Cosa falsificherebbe la tesi «la struttura aggiunge»: parità sui
  quattro verdetti e percorso ≥ 3/4 anche per la sessione singola.

---

# Emendamento 1 — 2026-10-17, dopo i punteggi di A′, B′, E′ e prima di qualunque lancio dell'ablation

**Che cosa cambia**: §7 diceva che l'ablation parte «dopo la chiusura del giro 5 nel registro (e del giro 6
se c'è)». Ora: **dopo la riga di sintesi del giro 5 e prima del giro 6**, un caso alla volta, nell'ordine
A′ → B′ → E′ → D, sugli stessi quattro casi e con i prompt singoli congelati in §7 (sha256 invariati).

**Perché**: l'ablation confronta la sessione singola con i run del laboratorio del **giro 5**, non del
giro 6; il giro 6 richiede un caso sostitutivo E″ con calibrazione e il FIX 17, lavoro senza run che
lascerebbe la macchina ferma per ore. Le sessioni singole non leggono il laboratorio né il banco (confine
di cartella), quindi il FIX 17 può essere installato nel laboratorio mentre girano senza toccare ciò che
misurano.

**Autoconfutazione**: (1) «anticipare l'ablation espone i casi a un'altra sessione prima del giro 6» — no:
le sessioni singole vedono solo il testo del caso, come il laboratorio, e i casi del giro 5 sono già stati
consegnati quattro volte; (2) «la quota»: oggi il limite di sessione ha fermato D per 97 minuti; una
sessione singola costa meno di un run del laboratorio, e `stacca-singolo.sh` fa il pre-volo del modello,
quindi un lancio durante un limite viene rifiutato e non parte a metà; (3) «cambiare l'ordine delle fasi è
una deviazione dalla rotta»: la rotta §4 mette la fase 5 dopo la fase 4, e il giro 6 è un'estensione della
fase 4 decisa dall'Emendamento 1 della rotta, non una fase a sé — l'ordine fase 4 → fase 5 è rispettato.
Nulla dell'ablation cambia nel merito: protocollo, prompt, tetto di tempo, rubrica e tabella restano §7.

<!-- FINE DOCUMENTO -->
