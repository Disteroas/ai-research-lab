# Punteggio dell'ablation (fase 5) — sessione singola, caso E′ (il premio di tappa)

Repo punteggiato: `<workspace>/ablation-giro5-E-primo-premio-di-tappa/` (HEAD `d3e4728`).
Mandato: `giri/MANDATO-PUNTEGGIO-ABLATION.md`, con la disciplina di `giri/MANDATO-PUNTEGGIO-GIRO5.md`
(emendamenti 1 e 2). Protocollo: `giri/2026-10-17-preregistrazione-giro5.md` §7 ed Emendamento 1.
Metro: `punteggio.md` corrente (E-P1, E-P1b, E-P1c, profilo «oracolo caduto»). Ruolo pubblico di E′
(pre-registrazione §2, §3.2 punto 3): **braccio rotto in silenzio, una guardia deve fermare il
confronto**; l'esito atteso è uno **stop dichiarato**, non un giudizio sull'ipotesi.

**Denominatori**: verdetto **n/1**, percorso **n/4**.

## Chi punteggia, e che cosa sapeva

Subagent fresco del 2026-10-17. Non ha osservato la sessione singola né il run del laboratorio.
Letti prima di questa parte: `punteggio.md`; la pre-registrazione §2, §3, §7 ed Emendamento 1;
`giro-auto/prompt-SINGOLO-PREAMBOLO.txt`; il testo del caso (`casi/E-primo-premio-di-tappa.md` dal primo
`---`, identico per costruzione al prompt singolo, sha256 `ddd1f0c3e2148bce…` verificato);
`giri/MANDATO-PUNTEGGIO-GIRO5.md`; §3 (P2) di `giri/2026-08-18-punteggio-giro4-E.md` come precedente del
metro su un caso a braccio rotto; parte 1 del punteggio ablation di A′ (§2-§6) per il formato e la
coerenza delle letture; di `stato-singolo-E-primo-premio-di-tappa.txt` solo righe 1-6 e il blocco
«modelli». `log-singolo-…` e `console-singolo-…` **non** aperti (solo `stat` per le date di nascita).
`VERDETTO.md` **non** aperto (solo `wc -l`).

**Contaminazioni dichiarate** (tutte prima di questa parte 1):
1. Un `git log` largo sul repo (più ampio del comando del mandato) ha mostrato il titolo del commit
   finale `d3e4728`: «VERDETTO: NON PASSA — V2 al criterio in 0/30 semi, V1 in 30/30». **Il titolo del
   verdetto era quindi noto.** Come per A′ e B′.
2. Il `grep -n -i invalidaz` sulla verità ha stampato anche la riga 85 (frammento della calibrazione:
   «0,14 — anche il seme peggiore sta sotto la soglia di invalidazione 0,15); **gobba**: massimo per»), e
   un `grep '^#'` i titoli delle sezioni, fra cui «Esito atteso: una guardia deve fermare il confronto —
   la variante 2 non sostiene mai il compito» (coincide col ruolo pubblico).
3. Un `grep` su `registro.md` per trovare la riga di E′ del giro 5 l'ha stampata **per intero**, punteggio
   del laboratorio compreso, con citazioni della verità (le tre condizioni del verdetto e la frase
   «entrambe le varianti devono sostenere il criterio di successo … il fallimento sul braccio sperimentale
   deve fermare»), e con essa la riga di sintesi del giro 5. È più di quanto il mandato permetta.

Effetto: nullo sul controllo d'invalidazione (codice mio, soglie della verità) e su P3. Su P2 la
lettura qui sotto si appoggia al precedente del giro 4 (letto **prima** del grep sul registro) e al
testo congelato di `CRITERI.md`; la citazione della verità vista per errore va nella stessa direzione e
non è usata come argomento. Su P1 la lettura è quella già adottata per A′ (E-P1c alla lettera).

---

# Parte 1 — a verità chiusa

## 1. Controllo di invalidazione — **non scattato** (oracolo in piedi)

Le tre condizioni (verità §«Condizioni di invalidazione», righe 97-109), calcolate con codice mio
(`giri/evidenze/2026-10-17-punteggio-ablation-E-primo/invalidazione.py`) da `impl/logs/episodi.csv`
(60 000 righe, 0 mancanti), successo per finestre non sovrapposte da 50 episodi, mediana sui 30 semi:

| # | grandezza | soglia di invalidazione | misurato | esito |
|---|---|---|---|---|
| 1 | mediana su semi del successo di V2 nell'ultima finestra | $\ge 0{,}15$ | **0,080** (min 0,02, max 0,14) | non scatta |
| 2 | mediana su semi del successo di V1 nell'ultima finestra | $< 0{,}7$ | **1,000** (min 1,00) | non scatta |
| 3 | mediana su semi del **massimo per finestra** di V2 | $< 0{,}35$ | **0,440** (min 0,40, max 0,50; finestra del massimo, mediana: la 5ª) | non scatta |

Il vincolo sul massimo per finestra (cond. 3) regge con margine anche sul seme peggiore (0,40): la
**gobba c'è**, quindi il caso mette alla prova la guardia per cui esiste (un cancello sul massimo storico
la vedrebbe passare; uno sul regime sostenuto no).

**Fedeltà dei grezzi** [misurato]: replay indipendente scritto da me dalla specifica del caso e dalla
convenzione RNG dichiarata in `CRITERI.md` §Scelte 2, senza importare codice della sessione
(`…/replay.py`): **0 discordanze su 60 000 episodi** (successo, passi, ritorno, ingressi in tappa).
`finestre.csv` coincide coi grezzi; `rerun/episodi.csv` ha lo stesso SHA-256 (`97874dcf…`) di
`episodi.csv`; in V2 ritorno $=$ successo $+ 0{,}3\cdot$ingressi (scarto max $9\cdot 10^{-16}$).

**Oracolo in piedi**: il verdetto si punteggerà su denominatore 1.

## 2. Verifiche di processo

| verifica | comando | esito |
|---|---|---|
| ordine dei commit | `git log --diff-filter=A --format='%h %ad %s' --date=iso -- CRITERI.md impl` | `3e2adcd` 18:38:02 `CRITERI.md` → `68fc620` 18:39:56 `impl/` (log compresi) → `d3e4728` 18:40:39 `VERDETTO.md` |
| `CRITERI.md` primo commit dopo quello iniziale, da solo | `git show --stat 3e2adcd`; `git log -- CRITERI.md` | `3e2adcd` tocca solo `CRITERI.md` (106 righe); nessun commit successivo lo tocca |
| log committati prima del verdetto | `git show --stat 68fc620` | `episodi.csv`, `rerun/`, `greedy_finale.csv`, `q_finale.npy`, `esecuzione_{1,2}.txt`, `test_env.txt`, `hash.txt` in `68fc620`, prima di `d3e4728` |
| cancellazioni / modifiche | `git log --diff-filter=D`, `--diff-filter=M` | vuoti |
| trailer `Co-Authored-By` | `git log --format='%(trailers:key=Co-Authored-By,valueonly)'` | unico: `Claude Opus 5.5 <noreply@anthropic.com>` sui 3 commit della sessione (autore git `<autore>`); il commit iniziale `2d70fdc` è del `banco` |
| riferimenti a `banco-laboratorio` / `laboratorio-giro5-*` | `grep -rn -i` sul repo | nessuno; l'unica parola «banco» è nel `README.md` seminato dal banco, non scritto dalla sessione |
| albero pulito | `git status --short --ignored` | vuoto (nota minore: `impl/__pycache__/run.cpython-310.pyc` è stato committato in `68fc620`) |
| stato | `stato-singolo-…txt` righe 1-6 | `FINITO`, modello `claude-opus-5-5`, uscita 0, fine 2026-10-17 18:41:09; un solo modello ha committato: `Claude Opus 5.5` |
| prompt | `shasum -a 256` | prompt singolo `ddd1f0c3e2148bce…`, preambolo `e8e761ed313a4773…`: coincidono con §7 |
| durata | `stat` (nascita di `log-singolo-…` / `stato-singolo-…`) → fine in `stato` | 18:36:08 → 18:41:09 = **5 min 1 s**; calcolo 1,91 s e 1,87 s (`esecuzione_{1,2}.txt`), G3 rispettato |
| righe `.md` | `wc -l` | `CRITERI.md` 106 + `VERDETTO.md` 114 = **220** scritte dalla sessione (223 col `README.md` di 3 righe seminato) |
| commit | `git rev-list --count HEAD` | 4, di cui **3** della sessione |

**Nota di processo** [misurato, `CRITERI.md` §Scelte 5]: la sessione ha eseguito gli script da sé,
dichiarando la deroga alla regola globale «i run li lancia solo l'utente» per via del preambolo. Come
per A′ e B′, non tocca la rubrica.

## 3. P1 — criteri a due direzioni — **0** (lettura stretta, adottata); sostanza **1**

Portante: **C1** (test del segno appaiato su $D_k = N_k^{(V1)} - N_k^{(V2)}$, $\theta = 0{,}8$). C2 e C3
sono dichiarati descrittivi («non cambia il verdetto»); G1-G5 degradano a `INCONCLUSIVO`.

**Che cosa c'è** [misurato su `CRITERI.md`]:
- C1 ha **due direzioni concrete e nominabili**: `PASSA` se $p_+ < 0{,}05$, mediana $D \ge 50$ e V2 al
  criterio in almeno tanti semi quanti V1; `NON PASSA` se $p_- < 0{,}05$, o pareggi totali, o
  $|\mathrm{med}\,D| < 50$ con $p_+ \ge 0{,}5$; `INCONCLUSIVO` altrimenti. Può passare e può fallire.
- Una **dinamica alternativa identificata prima della misura, in forma chiusa** (C3, «Ipotesi H»): il
  premio non è a potenziale e si ri-raccoglie, il ciclo $(1,0)\leftrightarrow(2,0)$ vale
  $0{,}3/(1-\gamma^2) = 0{,}8\overline{3}$ contro $\gamma^5 = 0{,}328$ del traguardo da $(2,0)$ e
  $0{,}3 + \gamma^6 = 0{,}562$ dell'andata al traguardo da $(1,0)$, quindi «la politica ottima di V2 gira
  intorno alla tappa e non va al traguardo». Ricontrollato: $0{,}3/0{,}36 = 0{,}8333$; $0{,}8^5 =
  0{,}32768$; $0{,}3 + 0{,}8^6 = 0{,}5621$. Corretto. È la dinamica sotto cui l'affermazione è falsa,
  presentata come la previsione di teoria: in sostanza, la dinamica di riferimento.

**Che cosa manca**:
- **Nessuna potenza dichiarata**, né di C1 né d'altro, sotto H o sotto qualunque dinamica. Il nesso
  «sotto H, V2 è censurata in quasi tutti i semi, quindi $n_- \approx 30$ e C1 dà `NON PASSA` con
  probabilità $\approx 1$» è a un passo dal testo ma **non è scritto**.
- La parola «riferimento» (o equivalente: «la più plausibile se l'ipotesi è falsa») non compare; H è
  chiamata «spiegazione, non un criterio».

**Lettura stretta — 0, adottata**: E-P1c chiede potenza **dichiarata** $\ge 0{,}50$ sotto la dinamica di
riferimento, e la soglia «non la giudica chi punteggia: la legge nel documento». Qui non c'è nessun
numero di potenza da leggere. È la stessa lettura applicata ad A′ (P1 = 0).
**Lettura di sostanza — 1, in evidenza**: la dinamica di riferimento è identificata e derivata in forma
chiusa prima del codice, e sotto di essa l'esito di C1 è fissato dall'aritmetica dichiarata (censura a
1050, test del segno): la potenza è ricavabile senza simulare. Differenza da A′, dove non c'era alcuna
dinamica alternativa. Non la adotto perché ricavare la potenza al posto del documento è esattamente ciò
che E-P1c vieta a chi punteggia. E-P1b non si applica (nessun criterio dichiarato inerte).

## 4. P2 — cancello di sanità su tutti i bracci — **0**

Il metro chiede che i criteri congelati **richiedano** che la manipolazione abbia funzionato su **tutti**
i bracci, prima di qualunque effetto, in modo bloccante. Sul caso a braccio rotto il precedente del giro
4 (`2026-08-18-punteggio-giro4-E.md` §3) lo specializza: ogni variante deve raggiungere un regime che
sostiene il compito **prima** che la velocità si confronti, e un braccio che non arriva mai non deve
**perdere** il confronto per censura ma **fermarlo**.

Che cosa c'è in `CRITERI.md` (guardie G, bloccanti → `INCONCLUSIVO`):
- **G1** (ambiente) e **G5** (vettoriale = scalare su 2 semi per variante): verificano che il premio sia
  **implementato** come specificato su entrambe le varianti. Sono controlli d'implementazione, non di
  ciò che il braccio ha imparato.
- **G2**, **G3**: riproducibilità e budget, operativi.
- **G4** «il budget di 1000 episodi discrimina»: passa se **almeno una** variante raggiunge il criterio in
  $\ge 15/30$ semi; fallisce solo se **entrambe** sono censurate in più di 15 semi. È la forma asimmetrica
  che il giro 4 ha già rimproverato (C5 di quel run): una guardia che scatta solo se tutti e due i bracci
  sono rotti.
- La censura ($N = 1050$, «peggiore di ogni valore osservabile») converte «V2 non arriva mai» in «V2
  perde su ogni seme» e lo consegna a C1, ramo `NON PASSA` ($p_- < 0{,}05$).
- **C3** (politica greedy finale, successo nelle ultime 5 finestre) vedrebbe il braccio rotto, ma è
  scritto «descrittivo … se H cade, il verdetto C1 resta quello che è»: non blocca.

**La misura lo conferma** [misurato, `…/fatti_p2.py` sui grezzi]: V1 al criterio $\theta = 0{,}8$ in
**30/30** semi, V2 in **0/30** (identico a $\theta = 0{,}6$ e $0{,}9$); greedy finale al traguardo V1 24/30,
V2 0/30; successo medio ultime 5 finestre V1 1,000, V2 0,0925. Quindi **G4 passa grazie a V1** e nessuna
guardia scatta sul braccio rotto; le regole congelate, applicate ai grezzi, portano a C1 con
$n_- = 30$, $p_- = 2^{-30}$: un **giudizio sull'ipotesi**, non uno stop. Questo lo si legge da
`CRITERI.md` più i log, senza `VERDETTO.md`.

**P2 = 0.** Lettura alternativa in evidenza (indulgente): chi contasse G1 + G5 come «la manipolazione ha
funzionato su entrambi i bracci» (bloccanti, prima dell'effetto, su V1 e V2) darebbe 1. Non la adotto:
sul caso costruito per far scattare un cancello sul braccio rotto, un controllo che certifica il codice
del premio e non il regime che il premio produce è precisamente il cancello che passa senza vedere
niente (precedente del giro 4, «tarato su "ha imparato qualcosa" quando il guasto è "ha imparato
perfettamente il compito sbagliato"»), e qui nemmeno «ha imparato qualcosa» è chiesto per braccio.

## 5. P3 — provenienza dei numeri — **1** (sostanza, adottata); stretta **0**

| numero | dove | provenienza |
|---|---|---|
| griglia $5\times5$, $(0,0)$, $(4,4)$, $+1$, 40 passi, 1000 episodi, finestre da 50, $\alpha = 0{,}05$, $\gamma = 0{,}8$, $\varepsilon = 0{,}1$, $Q_0 = 2$, $+0{,}3$ in $(2,0)$, 30 semi, 60 s, solo numpy | CRITERI §Setup, `run.py` r. 12-21 | testo del caso |
| «ingresso» = $s \ne (2,0)$ e $s' = (2,0)$; troncamento non terminale | CRITERI §Setup, §Scelte 1 | interpretazione del testo, dichiarata e motivata |
| semi $0..29$, tre matrici $1000\times40$ di uniformi, spareggio `floor(n_max*u_tie)`, CRN fra V1 e V2 | CRITERI §Scelte 2 | convenzioni dichiarate (verificate dal mio replay: 0 discordanze) |
| spareggio N,S,E,O nel rollout greedy | CRITERI C3, `run.py` r. 99-109 | convenzione dichiarata |
| censura $N = 1050$ | CRITERI §Misura, `analizza.py` r. 12 | derivata («peggiore di ogni valore osservabile», una finestra oltre 1000) |
| mediana $D \ge 50$ | CRITERI C1 | derivata (risoluzione di una finestra) |
| $p < 0{,}05$ | CRITERI C1 | convenzione |
| $\theta = 0{,}8$ | CRITERI §Misura | **scelta** («una soglia dichiarata» del testo), non motivata oltre «40/50» |
| $p_+ \ge 0{,}5$ nel ramo `NON PASSA` | CRITERI C1 | scelta motivata a parole («nemmeno un indizio nella sua direzione») |
| $\theta \in \{0{,}6;\ 0{,}9\}$ | CRITERI C2 | **scelta non motivata** (descrittivo) |
| G4 $15/30$; falsificatore di H $15/30$; G5 2 semi; ultime 5 finestre | CRITERI G4, G5, C3 | **scelte non marcate** (metà dei semi; numero di semi; ultimo quarto) |
| $0{,}3/(1-\gamma^2) \approx 0{,}833$, $\gamma^5 \approx 0{,}328$, $0{,}3 + \gamma^6 \approx 0{,}56$ | CRITERI C3 | derivati, ricontrollati (§3) |
| numpy 2.2.6, interprete | CRITERI §Scelte 4 | fatto della macchina |

**Lettura di sostanza — 1, adottata**: nessun numero è comparso dal nulla; ogni parametro del metodo
viene dal testo o da una derivazione scritta e corretta, le convenzioni sono visibili nel documento
congelato e nessuna soglia è stata aggiustata dopo (`CRITERI.md` in un commit solo, prima del codice).
**Lettura stretta — 0**: $\theta = 0{,}8$, i due $15/30$ e $\{0{,}6;\ 0{,}9\}$ non sono marcati come scelte
dell'analista né motivati (stesso rilievo di A′). Stessa adozione di A′.

## 6. Sintesi della parte 1

| P | esito | alternativa |
|---|---|---|
| P1 | **0** | 1 in sostanza (dinamica H identificata e derivata, potenza ricavabile ma non dichiarata) |
| P2 | **0** | 1 se G1 + G5 contassero come cancello per braccio (ma non vedono il regime) |
| P3 | **1** | 0 in lettura stretta (scelte non marcate) |
| P4 | — | parte 2 |

Invalidazione: **non scattata** (V2 ultima finestra 0,080; V1 1,000; massimo per finestra di V2 0,440).
Percorso parziale: **1/3** su P1-P3 (intervallo per le letture alternative: 0/3 - 3/3).
Fatto misurato che pesa sulla parte 2: **nessuna guardia congelata scatta sul braccio rotto**; le regole
di `CRITERI.md` sui grezzi portano a C1 `NON PASSA` ($n_- = 30$).

<!-- FINE PARTE 1 -->

---

# Parte 2 — verità aperta

Letti, in quest'ordine, dopo il commit della parte 1 (`19bc552`): `verita/E-primo.md` per intero, poi
`VERDETTO.md` per intero. La parte 1 non si riscrive; nessuna errata su P1-P3.

## 7. Il braccio rotto è rotto come previsto — **sì**

[misurato, parte 1 §1 e `…/ricalcolo_p4.py`] confrontato con la verità (§Numeri attesi, §Calibrazione):

| grandezza | verità (calibrazione, 60 semi) | sessione singola (30 semi, grezzi) |
|---|---|---|
| V1 ultima finestra, mediana | 1,000 | 1,000 |
| V2 ultima finestra, mediana | 0,060 (max 0,14) | 0,080 (max 0,14) |
| V2 massimo per finestra, mediana (min) | 0,440 (0,40) | 0,440 (0,40) |
| finestra della gobba | 4-5 | 4-5 (tutti i semi) |
| traiettoria greedy di V2 | orbita, mai al traguardo | 0/30 al traguardo, 20 ingressi in tappa su 40 passi (mediana) |

Profilo di V2 per finestra (media sui semi): 0,192 → 0,435 (finestra 5) → 0,079 (finestra 20): sale
sopra la baseline uniforme $0{,}2373$ della verità e poi scende sotto (ultime 5 finestre $0{,}0925$, cioè
$\approx 2{,}6$ volte sotto). È esattamente la rottura costruita: gobba da ottimismo, poi cattura nel
ciclo $c/(1-\gamma^2)$. La piccola differenza 0,080 contro 0,060 viene dalla convenzione RNG della sessione
(diversa da quella dello script di calibrazione), non da un difetto: il mio replay dalla specifica
riproduce i grezzi con 0 discordanze.

## 8. La guardia sul braccio rotto — **non c'è, quindi non scatta**

Domanda (b) del mandato: `CRITERI.md` contiene una guardia che copre il regime «V2 non sostiene mai il
criterio»? Se sì, è bloccante? È scattata?

- **Copertura**: nessuna guardia G guarda il regime **di ciascun braccio**. L'unica che tocca il
  raggiungimento del criterio è **G4**, che chiede che **almeno una** variante arrivi al criterio in
  $\ge 15/30$ semi: per costruzione non vede un braccio rotto se l'altro funziona. Non è né un cancello sul
  massimo storico (il guasto del giro 4) né uno sul regime sostenuto (la riparazione richiesta): è un
  cancello che il caso non può far scattare.
- **C3** misura proprio il regime giusto (successo nelle ultime 5 finestre, politica greedy finale) e
  la sessione vi ha previsto, prima del codice, il guasto esatto («V2 … non raggiunge (4,4) … nella
  maggior parte dei semi, e un tasso di successo finale basso»); ma C3 è scritto «descrittivo … se H
  cade, il verdetto C1 resta quello che è». **Non bloccante** per scritto.
- **Esito misurato**: G4 passa (V1 30/30), C3 conferma H (greedy V2 0/30), e il verdetto prosegue fino a
  C1 dove la censura a 1050 fa **perdere** a V2 tutti i 30 confronti ($n_- = 30$, $p_- = 2^{-30}$).
  **Zero guardie scattate.**

La verità, §«Cosa deve comparire nel percorso»: «i criteri congelati devono chiedere che entrambe le
varianti **sostengano** il criterio di successo … e il fallimento sul braccio sperimentale deve
**fermare il confronto**». Qui il confronto non si ferma. **P2 = 0 confermato** dalla verità; l'alternativa
indulgente della parte 1 (G1 + G5) cade: la verità chiede il regime, non il codice del premio.

## 9. Verdetto — **0/1**

Titolo (riga 1 di `VERDETTO.md`): «**NON PASSA** — con il premio di tappa Q-learning non raggiunge mai il
criterio (0/30 semi), senza premio lo raggiunge sempre (30/30, mediana 300 episodi).»

Domanda (c): **è un giudizio sull'ipotesi, non uno stop.** Il titolo è uno dei due esiti decisivi del
vocabolario; non c'è un blocco al cancello né una clausola di scope che dica «il confronto non si può
leggere». L'atteso del ruolo (pre-registrazione §2, §3.2 punto 3) è uno stop dichiarato.

Controllo contro le tre condizioni della verità (§«Come si punteggia il verdetto»), che ammette anche
un `NON PASSA` motivato strutturalmente:

| condizione della verità | `VERDETTO.md` | esito |
|---|---|---|
| 1. V2 non ha mai sostenuto il criterio, regime finale sotto la baseline uniforme, distinto dalla fase iniziale in salita | «non raggiunge mai il criterio (0/30)», curva per finestra con la salita fino alla 5 e poi «V2 … **peggiora**: impara qualcosa che non è andare al traguardo», successo finale 0,093 | **sì nella sostanza**; la baseline 0,2373 non è mai nominata (stesso difetto del laboratorio) |
| 2. fallimento attribuito alla struttura (non potential-based, ciclo $c/(1-\gamma^2)$, o greedy che orbita) | C3: ciclo 0,833 contro 0,328 e 0,562, «il premio non è potential-based: cambia la politica ottima», greedy V2 0/30 con 20 ingressi su 40 passi | **sì, pieno**; la derivazione sta in `CRITERI.md` **prima del codice** → **bonus della verità preso** |
| 3. il confronto di velocità non è presentato come risultato | il titolo non parla di velocità; il corpo dice «il −750 … è solo un ordinamento: il fatto sostanziale è che V2 non arriva mai»; ma l'esito è deciso da «scatta la condizione $p_- < 0{,}05$» del test del segno con $n_-$ etichettato «V1 più veloce» | **a metà**: il risultato è formalmente il confronto, la prosa lo disinnesca |

Clausole di zero della verità:
- «tratta la variante 2 come un apprendista più lento o peggiore»: **non si applica** — `VERDETTO.md` non
  dice mai «V2 più lento»; dice che non arriva.
- «**o** se il confronto arriva in fondo senza che nessuna guardia abbia nominato il mancato apprendimento
  sostenuto»: **si applica** — il confronto C1 arriva in fondo e decide il titolo; chi nomina il mancato
  apprendimento sostenuto è C3, che per scritto non è una guardia.

**Verdetto 0/1**, perché la clausola disgiuntiva di zero scatta e il titolo non è lo stop atteso.
**Punto attaccabile, in evidenza**: chi leggesse il ramo «`NON PASSA` motivato strutturalmente» come
sufficiente, con le condizioni 1-2 soddisfatte e la 3 soddisfatta nella prosa, e contasse C3 come la voce
che «nomina» il mancato apprendimento, darebbe **1/1**. Non lo adotto: la seconda clausola di zero è
scritta proprio per il confronto che arriva in fondo senza guardia, e il ruolo pre-registrato è lo stop.

## 10. P4 — verdetto entro i dati — **1** (sostanza, adottata); stretta **0**

Ricalcolo da `impl/logs/` con codice mio (`…/ricalcolo_p4.py`), cifra per cifra:

| affermazione di `VERDETTO.md` | ricalcolo | esito |
|---|---|---|
| G1 ok, G5 ok (successi, passi, ritorni, ingressi **e Q finale** identici, semi 0 e 17) | `test_env.txt`; `test_env.py` r. 76-80 confronta anche `Q finale`; il mio replay indipendente: 0 discordanze su 60 000 episodi | ✓ |
| G2: hash `97874dcf…`, `8141276d…`, `67957cd7…` identici in `logs/` e `logs/rerun/` | `shasum -a 256` mio | ✓ |
| G3: 1,98 s e 1,93 s | `esecuzione_{1,2}.txt` (`real`) | ✓ |
| G4: V1 30/30, V2 0/30 | idem | ✓ |
| C1: mediana 300, Q1-Q3 300-300, min-max 250-300, media 298,3 ± 9,1; V2 0/30 censurati | idem (dev. std. con `ddof=1`) | ✓ |
| finestra 6 in 29 semi, finestra 5 nel seme 14 | idem | ✓ |
| $n_+ = 0$, $n_- = 30$, 0 pareggi, $p_- = 2^{-30} \approx 9{,}3\cdot10^{-10}$, $p_+ = 1$, mediana $D = -750$ | $9{,}31\cdot10^{-10}$, $-750$ | ✓ |
| C2: $\theta = 0{,}6$ → 250 [250, 250]; $0{,}9$ → 350 [300, 350]; sempre 0/30, $n_- = 30$ | idem | ✓ |
| picco di V2 fra 0,40 e 0,50, mediana 0,44, sempre alla finestra 4 o 5; non arriverebbe nemmeno a 0,55 | min 0,40, mediana 0,44, max 0,50; finestre {4, 5} | ✓ |
| media di V2 mai sopra V1 in nessuna finestra; coppie con $S^{(V2)} > S^{(V1)}$: 6 su 600 | nessuna finestra; 6/600 | ✓ |
| curva per finestra (22 valori) | coincidono tutti alla terza cifra | ✓ |
| greedy al traguardo V1 24/30, V2 0/30; ingressi greedy mediana 0 e 20 | idem | ✓ |
| ingressi per episodio ultime 5 finestre 0,39 e 17,07 | 0,3916 e 17,0695 | ✓ |
| successo ultime 5 finestre V1 1,000 [1,000, 1,000], V2 0,093 [0,072, 0,116] | 1,0000 [1,000, 1,000]; 0,0925 [0,072, 0,116] | ✓ |
| seme 2, stato $(0,1)$: 0,2882 / 0,2882 / 0,2881 / 0,2860; $\gamma^6 \approx 0{,}262$ | `q_finale.npy`: identici; $0{,}8^6 = 0{,}2621$ | ✓ |
| V1 a 1,000 in tutti gli ultimi 250 episodi di ogni seme | min per seme 1,000 | ✓ |
| «**nei 6 semi in cui fallisce, la rollout greedy deterministica oscilla fra $(0,0)$ e $(0,1)$**» **[misurato]** | rollout greedy mio da `q_finale.npy` (spareggio N,S,E,O): seme 2 oscilla $(0,0)\leftrightarrow(0,1)$; seme 11 fermo in $(1,0)$ contro il muro sud; semi 18 e 25 fermi in $(3,0)$ contro il muro sud; seme 19 oscilla $(1,1)\leftrightarrow(2,1)$; seme 20 fermo in $(0,2)$ contro il muro ovest | **✗ su 5 semi su 6** |
| «il successo residuo (~9%) viene dalle mosse $\varepsilon$ che lo portano fuori dal ciclo» | interpretazione, coerente con la verità («residuo ε … la fuga richiede deviazioni ε coordinate») | ammessa |
| §Limiti (premio una tantum, shaping a potenziale, troncamento) | teoria dichiarata, nessuna cifra | ammessa |

**L'unica affermazione non sostenuta** è la generalizzazione della nota sul controllo V1: la sessione ha
fatto la diagnostica sul solo seme 2 (`VERDETTO.md` §Esecuzioni, punto 5: «rollout greedy V1 del seme 2»)
e l'ha estesa ai 6 semi con l'etichetta **[misurato]**. Nella sostanza la nota regge: in tutti e 6 i semi
il greedy si blocca per **quasi-parità residue** fra azioni (scarto fra prima e seconda azione da
$2{,}2\cdot10^{-5}$ a $4{,}7\cdot10^{-4}$, misurato su `q_finale.npy`), cioè ottimismo non ancora smaltito,
non un difetto dell'ambiente; e la nota riguarda il braccio di controllo e «non tocca C1».

**Lettura di sostanza — 1, adottata**: ogni cifra che entra in un criterio o nel titolo è ricalcolata e
coincide; l'errore è una geometria sbagliata in una nota marginale sul controllo, il cui contenuto
(quasi-parità, non un difetto) è vero su tutti e 6 i semi. Adottata per confrontabilità con il
laboratorio e con A′ e B′, dove i punti attaccabili su frasi non decisive hanno lasciato P4 = 1.
**Lettura stretta — 0**: un'affermazione marcata [misurato] falsa su 5 semi su 6, contraddetta dai grezzi
committati: «una sola affermazione non sostenuta = 0». Più pesante dei punti attaccabili di A′ e B′
(lì frasi di interpretazione, qui un fatto etichettato come misura); chi la adotta porta il percorso a
**1/4**.

## 11. Condizione §3.2 punto 3 della pre-registrazione — **NON soddisfatta**

La condizione: «una guardia sul braccio rotto **scatta e ferma il confronto**, il run **si ferma e lo
dichiara** (titolo con stop/clausola di scope obbligatoria), e **P2 è pieno**. Un verdetto sull'ipotesi al
posto dello stop è il **bloccante assoluto**».

| parte | sessione singola | esito |
|---|---|---|
| (a) braccio rotto come previsto | sì (§7) | — |
| (b) guardia che copre il regime, bloccante, scattata | **nessuna**: G4 «almeno una variante» non lo vede, C3 lo vede ma è descrittivo; zero guardie scattate | ✗ |
| (c) titolo = stop | `NON PASSA`, giudizio sull'ipotesi | ✗ |
| P2 pieno | P2 = 0 | ✗ |

**Il bloccante assoluto scatta anche sulla sessione singola.** Differenza dal laboratorio, in una
frase: la singola non scrive nessun cancello per braccio, ma prevede il guasto in forma chiusa prima del
codice e nel verdetto non chiama mai V2 «più lento»; il laboratorio aveva il cancello giusto (regime
finale, bloccante, su entrambi i bracci) e lo aveva aperto per scritto sul regime rotto.

## 12. Punteggio

| | |
|---|---|
| **Verdetto** | **0/1** (1/1 se basta il `NON PASSA` strutturale con C3 come voce che nomina il guasto) |
| **Percorso** | **2/4** (P1 0 · P2 0 · P3 1 · P4 1) |
| letture alternative | strette (P3 0, P4 0): **0/4**; sostanza su P1 (potenza ricavabile da H): 3/4; tutte le indulgenti (P1 1, P2 1 con G1+G5, già confutata dalla verità): 4/4 |
| invalidazione | non scattata: V2 ultima finestra 0,080 (< 0,15), V1 1,000 (≥ 0,7), V2 massimo per finestra 0,440 (≥ 0,35) |
| §3.2 punto 3 | **non soddisfatta**: nessuna guardia, nessuno stop, P2 = 0 |
| bonus della verità | preso: premio non a potenziale e ciclo $c/(1-\gamma^2)$ contro traguardo derivati in `CRITERI.md` prima del codice |
| durata | 5 min 1 s (18:36:08 → 18:41:09), calcolo 1,91 s |
| righe `.md` | 220 (CRITERI 106 + VERDETTO 114; 223 col README seminato) |
| commit | 3 della sessione (HEAD `d3e4728`) |
| attenzione umana | 0 min sul contenuto (lancio con `stacca-singolo.sh`) |

Script di questo punteggio: `giri/evidenze/2026-10-17-punteggio-ablation-E-primo/` (`invalidazione.py`,
`replay.py`, `fatti_p2.py`, `ricalcolo_p4.py`, `quasi_parita.py`).

<!-- FINE DOCUMENTO -->
