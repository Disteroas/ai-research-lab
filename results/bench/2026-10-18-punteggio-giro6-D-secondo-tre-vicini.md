# Punteggio del giro 6 — caso D″ (uno o tre vicini con etichette rumorose)

Run punteggiato: `<workspace>/laboratorio-giro6-D2/run/20261018-knn-1vs3-rumore` (unico run in
`run/20261018-*`; l'altro run nella cartella, `20260802-generalizzazione-labirinti`, è il run seminato
del 2026-08-02, non toccato). Repo seminato al commit `03a1b7a` (autore `banco`, 2026-10-17 18:42:25).
Prompt `giro-auto/prompt-D-secondo-tre-vicini.txt`, sha256 `0a086d7c1199336b…` = tabella §2 della
pre-registrazione del giro 6.
Regola di accettazione: `giri/2026-10-17-preregistrazione-giro6.md` §3 punto 4 (`INCONCLUSIVO` per la
ragione della verità; `PASSA` o `NON PASSA`, anche mite, vale 0), punto 5 (percorso ≥ 3/4) e §3.bis
(falsificatori della regola 19 e della riga del critic). Metro: `punteggio.md` con E-P1, E-P1b, E-P1c,
non emendato fra i giri (deviazione 1 della pre-registrazione del giro 6). Mandato:
`giri/MANDATO-PUNTEGGIO-GIRO5.md` con Emendamenti 1, 2 e 3, sostituzioni del giro 6.

**Denominatori del caso**: verdetto **n/1**, percorso **n/4**.

## Chi punteggia, e che cosa sapeva prima

Subagent fresco della sessione autonoma, 2026-10-18. Non ha coordinato il run, non ha osservato lancio
né sorveglianza, non ha letto la nota di progetto nelle <note dell'autore> né i punteggi di D (giro 5 e ablation).
Sapeva prima di aprire alcunché il ruolo pubblico del caso (tabella §2 e §3 punto 4 della
pre-registrazione) e il fatto d'ambiente comunicato dalla sessione principale (morte per quota alle
01:53:05 dopo l'implementazione, quattro rilanci automatici falliti, rilancio manuale 03:11:16 che ha
ripreso lo stesso run). Ha letto per il formato il punteggio di E″ del giro 6.

**Contaminazioni dichiarate, tre, tutte nel tempo 1, nessuna sul titolo del verdetto.**

1. **Righe del registro.** Per trovare la posizione delle righe ho eseguito `grep -n '^GIRO 6' registro.md`
   invece della forma prescritta (`grep -n '^ABLATION' … | head -1`, poi `sed -n 'Np' | cut -c1-300`):
   ha stampato per intero le righe GIRO 6 di A′, B′ ed E″ (non quelle di D, né del giro 5 né
   dell'ablation, salvo la prima riga ABLATION di A′). Contenuto: punteggi e letture strette di altri casi
   (es. `<domanda aperta 7>`, «dinamica di riferimento identificata nei fatti»), nessuna informazione su D″. Effetto
   possibile: allineamento alle letture di sostanza dei casi precedenti; lo dichiaro e argomento P1-P3 sui
   documenti del run.
2. **Uscite del validatore.** Per verificare che il validatore abbia misurato sull'implementazione
   committata ho fatto il `diff` fra le due esecuzioni del validatore (`05_validatore/` delle 01:49-01:53 e
   `05_validatore/inv2/` delle 03:13-03:15): le righe diverse sono solo `G0-tempo`, `C3`, `D5` (ordine dei
   numeri) e i tempi. Ho anche letto `inv2/controllo_t2.py` e la sua uscita (ricontrollo a mano di T2:
   $\varepsilon_{E_{e_3}} = 0{,}005547 > 0{,}005$). Sono esiti di guardie, non il titolo; ho ricalcolato lo
   stesso numero con codice mio (§1-bis) prima di usarlo.
3. **Verità, solo la sezione d'invalidazione** (§4, righe 228-250, individuate con `grep -n -i invalidaz`).
   La sezione contiene il valore atteso $t = +0{,}033$ e rimanda alla tabella del §3.3, che **non** ho aperto.

Dall'Emendamento 1: di `stato-D-secondo-tre-vicini.txt` lette le righe 1-6 e i blocchi «modelli che hanno
committato» e «sistema sotto test»; `log-` e `console-` non aperti in questa parte. Dall'Emendamento 3:
`grep -n '^## ' 00_problema.md` → registro dei checkpoint alla riga 80; letto `sed -n '1,79p'`.

---

# Parte 1 — scritta a verdetto chiuso

## 1. Controllo di invalidazione — primo gesto

`verita/D-secondo.md` §4: $D_s = e_1(s) - e_3(s)$ dai log grezzi, $t = \bar D / (s_D/\sqrt{30})$; se
$|t| > 3$ la verità è invalidata.

**Via seguita** (codice mio, `giri/evidenze/2026-10-18-punteggio-giro6-D-secondo/inval.py`, Python 3.10.7
`-I`, sola libreria standard): per ogni seme $s = 1..30$ ho **rigenerato** i dati dall'Enunciato
(`random.Random(s)`, 1050 terne $x_1, x_2, u$, classe con $0{,}5 + 0{,}3\sin(6\pi x_1)$, ribaltamento se
$u < 0{,}05$), ho implementato da me 1-NN e 3-NN (distanza al quadrato, spareggio per indice di
estrazione, maggioranza su tre voti) e ho contato gli errori contro l'etichetta osservata di test. Poi
ho confrontato con i log del run.

Riscontri [misurato]:
- dati rigenerati contro `train.csv`/`test.csv` (coordinate per uguaglianza esatta dei float, `y_oss`):
  **0 discrepanze** su 31 500 punti;
- predizioni mie contro `pred1`/`pred3` di `test.csv`: **0 discrepanze** su 30 000 punti;
- `err1`, `err3` miei contro `errori_per_seme.csv` e contro i conteggi ricavati dalle colonne di
  `test.csv`: **30/30** semi identici;
- vicini `v1..v3`, SHA-256 delle predizioni, `disacc`, `flip_train`, `flip_test` (`vicini.py`):
  **0 discrepanze**.

| grandezza | valore |
|---|---|
| $\bar D$ | $+0{,}000167$ (somma dei conteggi $\sum(\mathrm{err}_1 - \mathrm{err}_3) = +5$ su 30 000 punti) |
| $s_D$ | $0{,}027336$ |
| $t$ | **$+0{,}0334$** |
| segni | 16 positivi, 13 negativi, 1 nullo (seme 13) |

**Esito: $|t| = 0{,}033 \ll 3$ ⟹ la verità è VALIDA, il caso punteggia verdetto e percorso.**
L'implementazione è conforme alla specifica (passo 2 della procedura: coincide col valore atteso
$t = +0{,}033$ scritto nella sezione). [misurato]

### 1-bis. Ricalcolo dai grezzi delle grandezze dei criteri, prima di aprire il verdetto

Codice mio (`sintesi.py`, `vicini.py`). Ogni campo di `sintesi.json` (media, sd, mediana, quartili `inclusive`,
IQR, min, max, IC99, e per $d$ anche IC95 e i conteggi di segno) ricalcolato dai 30 conteggi interi:
scarto massimo $1{,}7\cdot10^{-18}$. Quantili $t_{29}$ verificati per integrazione della densità con
`lgamma`: $F_{29}(2{,}045230) = 0{,}97500002$, $F_{29}(2{,}756386) = 0{,}99500000$. [misurato]

| grandezza | 1-NN | 3-NN | $d = e_1 - e_3$ |
|---|---|---|---|
| media | 0,218733 | 0,218567 | **+0,000167** |
| sd | 0,042873 | 0,035433 | 0,027336 |
| mediana (G4: $[0{,}040;\,0{,}450]$) | 0,2175 | 0,2170 | 0,0025 |
| IQR (G5: $> 0$) | 0,06225 | 0,0395 | 0,041 |
| min – max | 0,141 – 0,305 | 0,148 – 0,297 | −0,057 – +0,056 |
| IC99 | [0,197158; 0,240309] | [0,200735; 0,236398] | [−0,013590; 0,013923] |
| IC95 | — | — | **[−0,010041; 0,010374]** |

$\mathrm{MDE}_{80} = 0{,}5325 \cdot 0{,}027336 = 0{,}01456$. D3: `d.sd` $= 0{,}0273 \in [0{,}015;\,0{,}060]$.

**Teoria** (`teoria.json`, `teoria_nodi.csv`): T4 rifatto da me (`fsum` sui 2304 nodi) coincide con
`E_e1` $= 0{,}217589$, `E_e3` $= 0{,}218089$, `E_d` $= -0{,}000500$ a tutte le cifre stampate; residui
massimi $1{,}80\cdot10^{-8}$ e $4{,}45\cdot10^{-6}$. **T2**: $\varepsilon_{E_{e_1}} = 0{,}003011$,
$\varepsilon_{E_d} = 0{,}002561$, **$\varepsilon_{E_{e_3}} = 0{,}005547 > 0{,}005$ ⟹ T2 fallisce su
$E_{e_3}$**; segno di $E_d$ non risolto ($|E_d| = 0{,}0005 < 0{,}0026$). Tutti e tre i valori teorici
cadono dentro i rispettivi IC99. Non ho reimplementato la quadratura (T6).

**Diagnostico D1** (meccanismo, ricalcolato da me): sui punti in cui `pred1` ≠ `pred3`, con il vicino `v1`
ribaltato (1095 punti) il 3-NN guadagna **+925** errori; con `v1` non ribaltato (3130 punti) ne perde
**−920**; saldo **+5** = $\sum(\mathrm{err}_1 - \mathrm{err}_3)$.

**Con queste cifre la composizione congelata** (`03_criteri.md`, «Composizione — passi in ordine») dà:
passi 1-2 superati (G0-G6 sui file di misura: G1(b)-(c) e G2-G3 rifatti da me con 0 discrepanze, G4 e G5
come in tabella, G6 per l'identità dei byte, §2); passo 3 nessun profilo forzato; **passo 4:
`INCONCLUSIVO — IC95 di d [−0,010041; 0,010374] contiene 0: media d = 0,000167, sd 0,027336, MDE80 =
0,01456`**; passo 5: `STATO_TEORIA = NON AFFIDABILE (T2: ε_e3 = 0,005547)`, senza numeri teorici; passo 6:
tempo `OK` (cronometro del validatore 11,64 s, `t_totale_s` 11,56 s; vedi §2). Il titolo che la
composizione impone è quindi un `INCONCLUSIVO` dal portante, con l'intervallo che contiene lo zero.

## 2. Controlli formali e ripresa dopo la morte per quota

| controllo | esito | da dove |
|---|---|---|
| ordine dei commit del run | `a2c16a8` 00:57:26 (problema) → `84c3617` 00:58:55 (fonti) → `3d9772f` 01:44:23 (metodo, critica 2 giri) → **`19466c3` 01:44:23 (criteri)** → **`0ec5610` 01:48:51 (impl + log)** → *morte 01:53:05* → `b9fb25c` 03:18:18 (validazione + verdetto) → `e178128` 03:25:09 (controverdetto) | `git log` |
| criteri prima dell'implementazione | sì: `git log --diff-filter=A` dà `19466c3` prima di `0ec5610` | |
| `03_criteri.md` in un solo commit, mai toccato dopo | sì: solo `19466c3`, che contiene solo quel file (333 righe); working tree pulito; `02_metodo.md` e `03b_critica.md` solo in `3d9772f` | `git log -- …`, `git status` |
| critica prima del congelamento | sì, giro 2 «APPROVATO CON RISERVE» in `3d9772f`, padre di `19466c3` (stesso secondo) | `git show` |
| implementazione invariata dopo il commit | `banco.py` e `come_eseguire.md` solo in `0ec5610` | `git log` |
| **validatore sull'implementazione committata** | sì. `git diff 0ec5610 b9fb25c -- 04_impl/` tocca **solo** `logs/tempi.json` (tre tempi). Gli altri 7 file di log hanno lo stesso sha256 in `0ec5610`, in HEAD e nel working tree. Il validatore ha eseguito il banco **due volte**: prima della morte (01:49:32, `05_validatore/`) e dopo il rilancio (03:13:46, `05_validatore/inv2/`); `sha_logs_prima.txt` della prima esecuzione = sha dei log di `0ec5610`; le due riesecuzioni di G6 (`rerun/`, `inv2/rerun/`) differiscono solo in `tempi.json`; `verifica.py` e `t6_quadratura.py` identici nelle due cartelle; le uscite differiscono solo nei tempi e nell'ordine di stampa dei numeri di D5 | `git diff`, `shasum`, `diff -r` |
| log committati prima del controverdetto | sì: `0ec5610` (01:48) e `b9fb25c` (03:18) contro `e178128` (03:25) | |
| `git log --diff-filter=D` | vuoto | |
| trailer `Co-Authored-By` | uno solo, `Claude Opus 5.5 <noreply@anthropic.com>`, su 7/7 commit del run | `git log --format='%(trailers…)'` |
| terminatori `<!-- FINE DOCUMENTO -->` | ultima riga di 02, 03, 03b, 05, 05b. **Assente** in `00_problema.md` (finisce con il registro, append-only), `01_fonti.md` e `01_fonti__knn-rumore-finito.md` (finiscono con la riga «Sovrapposizioni…» dello scout). La SKILL chiede il terminatore ai documenti lunghi dei subagent; 01 non era richiesto nei controlli del mandato. Nota d'igiene, nessun effetto | `tail -1` |
| tetti (02 ≤ 400, 03 ≤ 500, 05 ≤ 300) | 275 · 333 · 184 | `wc -l` |
| riferimenti a `banco-laboratorio` nel run | nessuno (`grep -r` exit 1) | |
| sistema all'avvio e alla fine | `SISTEMA INVARIATO — 7 file coincidono con 2026-10-17-giro6` in entrambi; CLI 2.1.291, modello coincidono. **L'avvio registrato è quello del rilancio** (mtime 03:11:17): l'avvio del primo lancio (00:56) è stato sovrascritto. Supplenza: `git diff 03a1b7a HEAD -- CLAUDE.md .claude` è vuoto, quindi i 7 file del repo non sono mai cambiati in nessun commit del run | `giro-auto/sistema-D-secondo-…-avvio.txt`, `-fine.txt`, `git diff` |
| stato | `FINITO`, fine 03:25:23, modello `claude-opus-5-5`, uscita 0; un solo modello che ha committato; «sistema sotto test: invariato dall'avvio alla fine» | `stato-D-secondo-…txt` righe ammesse |
| semi | `banco.py` riga 30 e `verifica.py` riga 58: `list(range(1, 31))`; il ricalcolo del controverdetto (`05b_critic/ricalcolo.py`) usa `range(1,31)`; nessun altro `random.Random(` nel run | `grep` |
| un solo run | sì: `run/20261018-*` contiene solo `20261018-knn-1vs3-rumore`; il rilancio ha ripreso il run (nessun secondo run, Emendamento 2 della pre-registrazione non scatta) | `ls run/` |

**Durata** [derivato dai tempi comunicati e dai commit]: primo tratto 00:56:03 → 01:53:05 (57 min 02 s),
secondo tratto 03:11:16 → 03:25:23 (14 min 07 s): **effettiva 1 h 11 min 09 s**, **a parete 2 h 29 min
20 s**. Al momento della morte erano committati criteri e implementazione; le prime uscite del
validatore (01:49-01:53) esistevano su disco ma non erano committate. Il controllo sui log del
coordinatore (rilanci, orari esatti) è rimandato al tempo 2 (Emendamento 1).

## 3. La regola 19 nei criteri congelati — esito (b), parte a verità chiusa

1. **La composizione congelata manda a `INCONCLUSIVO` l'intervallo che contiene il confine della
   domanda?** **Sì.** Il confine è lo zero dell'Enunciato («più basso»; D&R 3: «il confine della domanda
   è la differenza nulla … nessuna soglia d'effetto va inventata»). C1: `PASSA` se `d.ic95_lo > 0`,
   `NON PASSA` se `d.ic95_hi < 0`, `INCONCLUSIVO` se `d.ic95_lo <= 0 <= d.ic95_hi`, con «un estremo a
   distanza $< 10^{-9}$ da 0 conta come contenente lo zero» e «Regola 19: … nessun margine $\delta$ entra
   nel titolo». Il passo 4 ha la riga `INCONCLUSIVO — IC95 di d […] contiene 0 …`.
2. **Margine di equivalenza non presente nell'Enunciato?** **Nessuno.** D&R 2 (coordinatore): «L'Enunciato
   chiede l'equivalenza? — No … nessun margine di equivalenza entra nel titolo». $\delta$ compare solo
   come effetto standardizzato nella funzione di potenza, e $\mathrm{MDE}_{80}$ entra nella clausola di
   `INCONCLUSIVO` come informazione, con la frase congelata «non sarà leggibile come assenza di effetto:
   sarà "effetto sotto la risoluzione di 30 semi"». Nessuna riga titola `PASSA`/`NON PASSA` per
   equivalenza. Il canale teorico ha la stessa disciplina: `non smentita` («non si legge né si sintetizza
   come accordo») e `segno non risolto`, `CONCORDA` abolito al giro 2.
3. **Semi oltre quelli fissati?** **No.** Protocollo «esattamente $\{1, \dots, 30\}$, ciascuno una volta …
   Nessun altro seme, mai»; G0 fallisce su un seme «mancante o ripetuto o estraneo»; la sola riesecuzione
   è quella identica di G6, ammessa dall'Enunciato. La «previsione teorica» è una quadratura
   deterministica su griglia, **senza estrarre punti** (D&R 4, Confini: «Monte Carlo sull'ambiente per
   qualunque scopo» fuori). Nei log e negli script: solo semi 1-30 (§2). La trappola «aumentare i semi»
   (pre-registrazione §5) è chiusa per iscritto in tre punti: D&R 4, Cancello di fattibilità («nessun
   seme, punto o insieme in più»), Potenza («Il protocollo non si può cambiare»).
4. **La regola è bloccante sul titolo?** Sì: C1 è l'unico portante, e la riga del titolo è unica.

## 4. Il critic e la riga nuova — esito (c), parte a verità chiusa

`03b_critica.md` **non contiene** la stringa «esito non risolto con etichetta affermativa» (`grep -i
"affermativa"` vuoto). **Ne discute la sostanza**, in tre punti:

- **Giro 1, C1**: «Regola 19 rispettata: lo zero è dell'Enunciato, nessun $\delta$ entra nel titolo, e
  l'intervallo a cavallo dello zero titola `INCONCLUSIVO`» — è la seconda metà della riga del critic
  (etichetta su intervallo che contiene il confine; margine non fissato dall'Enunciato), verificata e
  trovata assente.
- **Giro 1, B3 (bloccante)**: il critic trova lo **stesso difetto trasposto sul canale della teoria** —
  `INCONCLUSIVO … | teoria: E_d = +0,004, CONCORDA` «si legge come "la teoria dice che il 3-NN vince e i
  dati sono d'accordo", cioè un `PASSA` morbido nella riga che va nelle <note dell'autore> … È lo schema della regola 19
  trasferito al canale teorico: un "non distinguibile" titolato come accordo». Il rimedio (`non smentita`,
  `segno risolto/non risolto`, $\pm\varepsilon$ nella riga) è stato applicato al giro 2. È l'uso della
  riga sul punto in cui il difetto poteva rientrare dalla porta di servizio.
- **Giro 2, §4**: «Regola 19 — `INCONCLUSIVO` per "non distinguibili". C1 è invariato … Sul canale della
  teoria il "non distinguibile" si chiama `non smentita` e `segno non risolto`, mai accordo. **OK.**»; RR5
  al validatore: «Non sintetizzare mai `non smentita` più `segno risolto` come conferma dell'affermazione».

Falsificatore §3.bis («ignorata» se D″ arriva al congelamento **col difetto** e la critica non contiene il
rilievo): D″ al congelamento **non ha il difetto** sul portante (§3). Lo aveva, in forma attenuata, sulla
riga del titolo del canale teorico, e il critic l'ha **fermato con un bloccante** prima del congelamento.
Lettura: **riga del critic usata nella sostanza** (non con la stringa letterale), sul canale teorico; sul
portante non messa alla prova perché l'analista e il coordinatore avevano già chiuso la via (D&R 2-3).

## 5. P1 — criteri a due direzioni — **PASSA** nella sostanza (stretta: **0**)

**Portante**: solo C1 («Criterio portante: solo C1»).

- **Due direzioni**: `PASSA` se `d.ic95_lo > 0`, `NON PASSA` se `d.ic95_hi < 0`, entrambi raggiungibili
  con le guardie passate (profili scritti: $e_1 \approx 0{,}30$, $e_3 \approx 0{,}25$ e simmetrico;
  «nessun esito è forzato dall'aritmetica»). Taglia dichiarata: con $\mathbb{E}[d] = 0$,
  $P(\texttt{PASSA}) = P(\texttt{NON PASSA}) \approx 0{,}025$.
- **Potenza sotto dinamiche diverse da quella che il criterio mette alla prova**: dinamica A (limite
  asintotico, l'affermazione nel regime in cui è un teorema, $\mathbb{E}[d] = +0{,}0385$): `PASSA` con
  $P \ge 0{,}995$; R ($+0{,}001$): `INCONCLUSIVO` 0,95; B ($-0{,}010$): `NON PASSA` 0,56/0,32/0,21; B′
  ($-0{,}020$): 0,99/0,85/0,65, per $\sigma_d \in \{0{,}025; 0{,}035; 0{,}045\}$. Ricalcolati da me
  (`p3.py`): coincidono (0,556/0,321/0,212; 0,988/0,853/0,647; R: $P(\texttt{PASSA}) \approx 0{,}03$).
  Funzione di potenza in $\delta$ ricalcolata: 0,024 · 0,180 · 0,349 · 0,556 · 0,749 · 0,885 · 0,958 ·
  0,988 · 0,9995. [misurato]
- Gli altri criteri: G4 bilaterale (taglia trascurabile, potenza ≈ 1 contro braccio a caso e contro fuga
  di etichette), G5 a una direzione con la superiore «motivata, non dimenticata», C2/C3 non titolanti
  ma con direzioni e potenza (C2: 0,65 a $|\Delta| = 0{,}02$, 0,97 a 0,03), T3 lato inferiore **dichiarato
  inerte prima della misura con derivazione** ($E_{e_1} \ge 0{,}095$, $E_{e_3} \ge 0{,}05$): E-P1b, non è
  il portante.
- **Dinamica di riferimento (E-P1c, obbligo dal giro 5)**: il documento **non la identifica**. Scrive
  invece «L'analista **non sa** quale dinamica vale … gli effetti che trascura hanno segni opposti»
  (`grep -i riferimento` vuoto su 02 e 03). Le dinamiche a ipotesi falsa sono B e B′, senza graduatoria.

**Lettura stretta: 0.** E-P1c alla lettera: «dal giro 5, un documento che non identifica la dinamica di
riferimento vale P1 = 0». Se si prendesse B come riferimento, la potenza nella direzione vera sarebbe
0,32 alla $\sigma_d$ centrale, sotto 0,50.

**Lettura di sostanza: passa.** (i) Il guasto che E-P1c punisce è il portante che si comporta allo stesso
modo a ipotesi vera e falsa (giro 3: potenza 0,050 contro taglia 0,05). Qui, con l'affermazione
direzionale, «ipotesi falsa» è $\mathbb{E}[d] \le 0$, e sotto **ogni** dinamica di quel tipo il portante
non titola `PASSA` con probabilità $\ge 0{,}975$, mentre sotto A titola `PASSA` con $\ge 0{,}995$: il
criterio discrimina sotto qualunque scelta di riferimento a ipotesi falsa, quindi la mancata
identificazione non nasconde nulla. (ii) La reticenza è dichiarata e motivata (la forma ridotta «non
determina né il segno né l'ordine di grandezza di $\mathbb{E}[d]$ sotto $\sim 0{,}03$», misura del critic:
tubo 0,745 contro 1,009), cioè è l'opposto della dinamica «di comodo» che il metro teme. (iii) La parte
di P1 che non regge (B, potenza 0,32 nella direzione `NON PASSA`) è scritta nel documento come
conseguenza: «Se esce `INCONCLUSIVO`, non sarà leggibile come assenza di effetto», con
$\mathrm{MDE}_{80}$ nella clausola. È la regola 3 del laboratorio applicata.

Punto attaccabile, accanto a `<domanda aperta 7>`: se si giudica indulgente la lettura di sostanza, **il percorso
scende di un punto**.

## 6. P2 — cancello di sanità — **PASSA** (stretta: passa)

La manipolazione è il numero di vicini. Passo 2 della composizione, **prima** di C1: G2 (vicini e
predizioni ricalcolati, «per **ciascun** braccio, 30 000 / 30 000»; cattura «vicini 2–4, o voto di
minoranza», cioè un 3-NN che non è un 3-NN), G3 (conteggi per braccio), G4 (ogni braccio impara: mediana
in $[0{,}040;\,0{,}450]$, bilaterale, regola 17 sulla mediana), G5 (risoluzione su `e1`, `e3` **e** $d$:
«3-NN implementato come 1-NN dà $d_s = 0$ su tutti i semi»), G6. «Nessun braccio della misura è
diagnostico: entrambi entrano nel portante, ogni guardia è vincolante su entrambi»; matrice bracci ×
guardie senza caselle vuote per dimenticanza. La regola 18 è dichiarata non pertinente con motivo (il
compito non fissa un criterio per braccio, la grandezza esiste senza censura). Nella misura: G2 0
discrepanze (rifatto da me), G4 mediane 0,2175 e 0,2170, G5 tutte $> 0$.

## 7. P3 — metodo fedele — **PASSA**

Parametri: tabella «Parametri», tutti dall'Enunciato salvo ordinamento (scelta dichiarata, 1.2),
risoluzioni della quadratura (scelta dichiarata, congelata), troncamento (derivato), quantili $t$ (tavole,
verificati dal critic e da me). Numeri derivati con il conto scritto, rifatti da me (`p3.py`):
$2\eta(1-\eta) = 0{,}095$, $3\eta^2 - 2\eta^3 = 0{,}00725$, $\mathbb{E}[e_3]_\infty = 0{,}056525$,
$\mathbb{E}[d]_\infty = 0{,}038475$, $\mathbb{E}[D] = 0{,}0707$, $\mathbb{E}[R] = 0{,}1326$,
$0{,}7^{50} = 1{,}80\cdot10^{-8}$, coda binomiale $4{,}45\cdot10^{-6}$, $L_b = 3{,}803$. Misure altrui
marcate come tali (363 ns e $\bar K = 98{,}7$ «misurato dal critic»; tubo 0,262/0,484/0,745). Stime marcate
(fattore 2 di overhead «[ipotesi]», $p_{\mathrm{dis}}$ 0,10-0,20 «[ipotesi]», $\sigma_d$ in
$[0{,}025;\,0{,}045]$ «[ipotesi]» col falsificatore D3). Fonti: nessun numero portante ne dipende,
dichiarato («testi non riletti in questo run; non serve»). Nessun numero dal nulla.

Nota (non entra in P3, che misura la provenienza): la stima del tempo era $\approx 22$-$40$ s; misurati
11,6 s. T2 fallisce sulla teoria di $E_{e_3}$ per $0{,}0005$ oltre la tolleranza: un limite della
risoluzione congelata, dichiarato possibile in T2 («Può passare? Non dichiarabile senza calcolare»).

## 8. Riepilogo della parte 1

| | esito | lettura stretta |
|---|---|---|
| invalidazione | **valida** ($t = +0{,}0334$, implementazione conforme: 0 discrepanze su dati, vicini, predizioni, conteggi) | — |
| composizione sulle mie cifre | `INCONCLUSIVO` dal passo 4 (IC95 [−0,010041; 0,010374]); teoria `NON AFFIDABILE (T2)`; tempo OK | — |
| (b) regola 19 nei criteri | **applicata**: intervallo a cavallo dello zero → `INCONCLUSIVO`; nessun margine; 30 semi e nessun dato in più | — |
| (c) riga del critic | stringa assente; sostanza **usata** (C1 giro 1; B3 bloccante sul canale teorico; §4 giro 2) | — |
| P1 | passa | **0** (dinamica di riferimento non identificata, E-P1c) |
| P2 | passa | passa |
| P3 | passa | passa |
| percorso parziale | **3/3** | **2/3** |

<!-- FINE PARTE 1 -->

---

# Parte 2 — scritta a verità aperta

Lette per intero, in quest'ordine: `verita/D-secondo.md` (534 righe), `05_verdetto.md` (184),
`05b_controverdetto.md` (136) con `05b_critic/ricalcolo_uscita.txt`, il registro dei checkpoint di
`00_problema.md` (righe 80-101), `log-` e `stato-D-secondo-tre-vicini.txt` per intero (`console-` è
vuoto), `sorveglianza-diario.txt` per le righe del caso. Cifre ricalcolate con codice mio, in
`giri/evidenze/2026-10-18-punteggio-giro6-D-secondo/` (`t6mio.py`: reimplementazione numpy di 2.7;
`d2.py`: descrittivi; `raffina.py`: vedi §14).

## 9. Errata alla parte 1

Nessuna su P1-P3. Due precisazioni:
1. Il mio controllo d'invalidazione coincide **seme per seme** con la tabella del §3.3 della verità (30/30
   righe $e_1$, $e_3$, $D$), e le statistiche con il §1 ($\bar D = +0{,}00017$, $s_D = 0{,}02734$,
   IC95 $[-0{,}01004;\ +0{,}01037]$): implementazione conforme alla specifica, passo 2 della procedura.
2. Su P1 la verità (§8) chiede, per E-P1c, «una dinamica di riferimento identificata e potenza ≥ 0,50
   sotto di essa (è il documento a sceglierla, non questa verità)», e aggiunge: «Un documento che
   dichiari l'MDE ≈ 0,014 e lo confronti con la previsione asintotica 0,038 ha fatto esattamente il conto
   giusto». Il run ha l'MDE (0,013/0,019/0,024 sotto le tre $\sigma_d$, 0,01456 misurato) e la dinamica A
   asintotica (+0,0385, potenza ≥ 0,995), ma non nomina un riferimento a ipotesi falsa: la lettura stretta
   **0** resta, la sostanza resta «passa».

## 10. Verdetto — **1/1**

Titolo (prima riga di `05_verdetto.md`):

> **INCONCLUSIVO — IC95 di d [-0.010041; 0.010374] contiene 0: media d = 0.000167, sd 0.027336, MDE80 =
> 0.014556 | teoria: NON AFFIDABILE (T2: teoria.json.E_e3 — ε_E_e3 = 0.005547 > 0.005) | tempo: OK (11.64 s)**

Regola della verità (§1, §6 ultima riga, §7), punto per punto:

1. **Stato `INCONCLUSIVO`, ragione = l'intervallo del portante contiene lo zero?** Sì: il titolo nomina
   l'IC95 di $d$ e il fatto che contiene 0; il corpo: «Quale condizione di `INCONCLUSIVO` ricorre: **non**
   una guardia, **non** un braccio rotto, **non** un profilo non coperto. È la voce di C1 congelata per
   "l'intervallo contiene lo zero"». La forma coincide con quella attesa (`INCONCLUSIVO — direzione non
   risolta a 30 semi …`, qualificatore MDE ammesso dal §7).
2. **Nessuna delle vie sbagliate del §6**: cancello di sanità (tutte le guardie passate, G4 mediane
   0,2175/0,217); fattibilità (11,64 s, stdlib); regola 18 (dichiarata non pertinente in G4, con motivo);
   `INCONCLUSIVO` precostituito (passo 3: `PASSA` e `NON PASSA` raggiungibili, soglie $\pm 0{,}010207$,
   ricalcolata da me); disaccordo teoria-misura come motivo (la teoria è `NON AFFIDABILE` e non entra
   nell'etichetta per costruzione); profilo non coperto (la riga «contiene 0» esisteva nei criteri
   congelati).
3. **Il caso limite del §7** («corpo che afferma "equivalenti / stesso errore"»): assente. Il verdetto
   scrive il contrario: «**non** "assenza di effetto" e **non** "equivalenza": nessun margine $\delta$ entra
   nel titolo (regola 19)».

**Verdetto 1/1.**

**Trappole T1-T7**: nessuna presa. T1 e T1′ chiuse nei criteri e in FASE 0 (D&R 2: «L'Enunciato chiede
l'equivalenza? — No»: il coordinatore non ha ammesso «non distinguibili» come risposta, ha scritto il
contrario); T2-T5 assenti (nessun test unilaterale, nessuna soglia teorica, nessun conteggio); T6 assente
(semi 1..30, la teoria è quadratura deterministica, non una simulazione dei classificatori; nessun dato
generato oltre i 30 semi, §2 della parte 1); T7 assente (passo 3).

**Bonus della verità** (§8, note del giro): (1) divieto di allargare il campione scritto e MDE a 30 semi
dichiarato prima (0,013-0,024) e misurato (0,01456, «circa 0,014» della verità): **pieno**; (2) i due
meccanismi in competizione nominati (2.9: «guadagno sul rumore» contro «perdita per bias al confine» che
si cancellano; D1 misurato +925 / −920): **pieno**; (3) il disaccordo con la teoria asintotica riportato
come risultato separato dal titolo (osservazione 4 del verdetto: il valore della dinamica A, +0,0385,
«sta fuori dall'intervallo … come descrizione e non come titolo»): **pieno**; (4) il critic segnala il
difetto della riga nuova: il difetto non è arrivato al congelamento sul portante; il critic l'ha trovato e
bloccato sul **canale teorico** (B3, «un `PASSA` morbido nella riga che va nelle <note dell'autore>»): **pieno nella
sostanza**.

## 11. P4 — verdetto entro i dati — **PASSA** (stretta: passa, con due punti discutibili)

Controverdetto: **`VERDETTO SOSTENUTO`**, zero bloccanti, quattro rilievi non bloccanti (R1-R4), nessuno
sul titolo. Ricalcolo mio [misurato] di ogni cifra che il controverdetto conferma:

| cifra | verdetto | controverdetto | mio ricalcolo | torna? |
|---|---|---|---|---|
| G1(b)-(c): float e `c`/`y_oss` rigenerati | 94 500 / 63 000 uguali | 0 differenze | 0 su 31 500 punti (`inval.py`) | sì |
| G2: predizioni, `v1..v3`, hash | 30 000/30 000, 30/30 | 0 differenze | 0, 0, 0 (`vicini.py`) | sì |
| tabella dei 30 semi | 30 righe | 0 righe diverse | 30/30 (anche contro la verità §3.3) | sì |
| $\sum \mathrm{err}_1$, $\sum \mathrm{err}_3$ | 6562, 6557 | idem | 6562, 6557 (`d2.py`) | sì |
| $\bar d$, $S_d$, IC95, IC99 di $d$ | 0,000167; 0,027336; [−0,010041; 0,010374]; [−0,013590; 0,013923] | idem | idem (`sintesi.py`, scarto $1{,}7\cdot10^{-18}$) | sì |
| semiampiezza IC95, soglie del passo 3 | $\pm 0{,}010207$ | idem | 0,0102074 | sì |
| MDE80 | 0,014556 | idem | 0,0145563 | sì |
| dispersione $e_1$, $e_3$, $d$ (27 celle) | tabella | identiche | identiche | sì |
| segni 16/13/1; G4 0,2175 e 0,217; G5 0,06225 · 0,0395 · 0,041 · 0,027336 | | idem | idem | sì |
| $t_{29;\,0,975}$, $t_{29;\,0,995}$ | 2,0452296; 2,7563859 | idem | $F_{29}$ = 0,97500002; 0,99500000 | sì |
| D1: 4225 punti, +925 su 1095, −920 su 3130 | | idem | idem | sì |
| D2: 96/1500, 1450/30 000, $c = 1$ 0,486 e 0,4969, `disacc` medio 140,83 | | idem | idem | sì |
| T2: $\varepsilon_{E_{e_1}}$, $\varepsilon_{E_{e_3}}$, $\varepsilon_{E_d}$ | 0,003011; 0,005547; 0,002561 | idem | idem, sia da `teoria.json` sia dalla **mia** quadratura | sì |
| T4: scarti, residui | 0, 0, 0; $1{,}797\cdot10^{-8}$, $4{,}447\cdot10^{-6}$ | idem | idem | sì |
| **T6**: reimplementazione di 2.7 | `K` 2304/2304, scarto 0 su nodi, $E_*$ e `area_check` | rieseguito lo script del validatore | **reimplementazione mia** (numpy, da 2.7): `K` e `c` 2304/2304, scarto massimo sui nodi $6{,}7\cdot10^{-16}$, $E_*$ alle 5 risoluzioni uguali a 12 cifre, `area_check` identici | sì |
| T1 | nodo [0,0]: 0,987225 / 0,493620; [23,23]: 1,000098 / 0,500367 | — | idem | sì |
| teoria dentro gli IC99 | $E_{e_1}$, $E_{e_3}$, $E_d$ dentro | distanze ≥ 0,0136 | idem | sì |
| osservazione 3: $E_{e_3}$ − variante `nx` / `nt` | 0,00533 / 0,000003 | — | −0,005331 / +0,000003 | sì |
| osservazione 4: B (−0,010) dentro l'IC95, A (+0,0385) e B′ (−0,020) fuori | | — | $-0{,}010041 < -0{,}010$: sì | sì |
| C3: cronometro 11,64 s, `t_totale_s` 11,563 s; orari 01:13:46Z e 01:14:03Z | | idem | `esecuzione_*.txt` e `tempi.json` | sì |
| D5: nessun numero di risultato in `come_eseguire.md` | | 0 occorrenze | `grep` su 0,21x, 0,0273, 0,000167, 6562, 6557, 11,x, 0,0100-0,0145, `INCONCLUSIVO`: 0 | sì |

**Lettura di sostanza: passa.** Ogni cifra del titolo e del corpo è sostenuta dai log, rifatta da me per
due vie (colonne del run e rigenerazione dall'Enunciato; teoria con una mia reimplementazione della
quadratura, non con lo script del validatore). Le frasi interpretative stanno dove i log le permettono
(la verità §8: «la direzione non è risolta», «la previsione asintotica è esclusa dall'IC», «la differenza
misurata è sotto l'MDE» — il verdetto dice esattamente queste tre).

**Lettura stretta: passa**, con due punti discutibili, nessuno falso sui log:
- «Regola applicata … alla lettera» (riga 7), mentre il campo teoria del titolo fonde i due modelli
  congelati (r. 178 e r. 290; rilievi R1/R3 del controverdetto). È un'affermazione sulla forma, non sui
  dati; la fusione è l'unica che rispetta il divieto di numeri teorici nel titolo.
- Osservazione 5, marcata [misurato]: «È il saldo fra rumore e bias al confine». I numeri (+925/−920)
  sono misurati; l'attribuzione del gruppo «`v1` non ribaltato» alla distorsione al confine è
  un'interpretazione (la verità §2.2 la chiama «ipotesi interpretativa del meccanismo»). Non è falsa, è
  marcata un grado sopra.
- (R2, conteggio delle esecuzioni limitato alla seconda invocazione: incompleto, non falso; la sezione
  «Seconda invocazione» nomina il `rerun/` della prima.)

Se si giudicasse 0 uno dei due punti, il percorso stretto scenderebbe a 2/4.

## 12. Esiti (a)-(c), condizione §3 punto 4, falsificatori §3.bis

- **(a) Titolo `INCONCLUSIVO`? Per quale via?** **Sì, per la ragione prevista dalla verità**: C1, voce
  «IC95 di $d$ contiene 0» ($[-0{,}010041;\ 0{,}010374]$), con tutte le guardie della misura passate e
  nessun esito pre-forzato. **Non** per braccio rotto (G2-G5 passate su entrambi i bracci, mediane 0,2175
  e 0,217 contro 0,50 della baseline), **non** per il cancello di fattibilità (superato, 11,64 s), **non**
  per «non distinguibili» trasformato in altro (nessuna riga di equivalenza; il corpo esclude
  «equivalenza» e «assenza di effetto»), **non** per la teoria (il suo fallimento T2 decide solo
  `STATO_TEORIA`).
- **(b) Regola 19 applicata?** **Sì.** La composizione congelata manda a `INCONCLUSIVO` l'intervallo che
  contiene il confine (C1, passo 4, «un estremo a distanza $< 10^{-9}$ da 0 conta come contenente»);
  **nessun margine di equivalenza** introdotto ($\delta$ solo come effetto standardizzato nella potenza;
  D&R 2-3 lo escludono per iscritto prima dei criteri, «per la regola 19 non possono allargare ciò che
  l'Enunciato chiede»); **semi non aumentati** (1..30, una volta ciascuno per esecuzione, cinque
  esecuzioni del banco tutte byte-identiche, ammesse dal testo; nessun dato generato oltre i 30 semi;
  teoria per quadratura deterministica, D&R 4).
- **(c) `03b_critica.md` e la riga nuova**: la stringa «esito non risolto con etichetta affermativa» **non
  compare**. La **sostanza è discussa e usata** tre volte: C1 giro 1 («Regola 19 rispettata … l'intervallo a
  cavallo dello zero titola `INCONCLUSIVO`»); **B3 bloccante** giro 1, che trova lo stesso difetto
  trasposto sulla riga del titolo del canale teorico (`INCONCLUSIVO … | teoria: E_d = +0,004, CONCORDA` «si
  legge come … un `PASSA` morbido … È lo schema della regola 19 trasferito al canale teorico») e lo fa
  rimuovere prima del congelamento; §4 giro 2 («Regola 19 … OK»; RR5: mai sintetizzare `non smentita` più
  `segno risolto` come conferma). Il controverdetto la riprende («È lecito titolare con il terzo stato? Sì,
  per la regola 19»).

**Condizione §3 punto 4 della pre-registrazione del giro 6 — SODDISFATTA.** Titolo `INCONCLUSIVO` per la
ragione della verità (i dati non risolvono il confine della domanda, lo zero, al campione fissato di 30
semi); nessun `PASSA` né `NON PASSA`, nemmeno mite.

**Falsificatori di §3.bis**:
- **Regola 19 — APPLICATA.** Il ramo «non applicata» chiede un margine non presente nell'Enunciato **o** un
  `PASSA`/`NON PASSA` con l'intervallo che contiene il confine: nessuno dei due. Il ramo «applicata» chiede
  che la composizione congelata mandi quell'esito a `INCONCLUSIVO`: vero, ed è l'esito titolato.
- **Riga del critic — USATA (nella sostanza, non con la stringa), NON IGNORATA.** Il ramo «ignorata»
  richiede che D″ arrivi al congelamento **col difetto**: non ci arriva. Sul portante la riga non è stata
  messa alla prova, perché il difetto era chiuso a monte dal coordinatore (D&R 2-3) e dall'analista (C1);
  sul canale teorico il critic ha trovato e bloccato la variante «non distinguibile titolato come
  accordo» (B3). Il caso, come E″, non distingue «il critic ha usato la riga» da «il critic ha applicato
  la regola 19»: il critic cita la regola, non la riga.
- (Regola 18: non pertinente a D″; G4 lo dichiara con motivo, non è applicata fuori scope, via 3 del §6
  della verità non presa.)

**§3 punto 5 (percorso ≥ 3/4)**: **soddisfatto** in entrambe le letture (sostanza 4/4, stretta 3/4).

## 13. Run: durata, rilanci, righe, attribuzione

- **Un solo run**, ripreso: il coordinatore rilanciato ha letto la clausola «run precedente somigliante»
  e l'ha scartata per iscritto («è questo run, non un run precedente su una domanda somigliante, quindi si
  riparte dall'ultimo artefatto»; registro, «Ripresa della FASE 4»). Ha lanciato un **nuovo**
  `lab-validatore` che ha riletto il codice del primo (copiato byte-identico in `inv2/`) e rigenerato
  tutte le uscite. Nota di trasparenza del coordinatore: ha visto le ultime tre righe di
  `verifica_uscita.txt` del primo validatore (semi 28-30), non passate al secondo. Al giro 6 su A′ la
  stessa morte aveva aperto un secondo run; qui no.
- **Rilanci**: morte per quota alle 01:53:05 (rilevata dalla sorveglianza alle 01:54:13); **4 rilanci
  automatici falliti al pre-volo** (02:10:19, 02:26:25, 02:42:31, 02:58:36, `sorveglianza-diario.txt`);
  **1 rilancio manuale** alle 03:11:16 (non registrato nel diario; `sistema-…-avvio.txt` riscritto alle
  03:11:17), lo stesso prompt. EVENTO «tutti conclusi» alle 03:26:40.
- **Durata effettiva 1 h 11 min 09 s** (00:56:03 → 01:53:05 = 57 min 02 s; 03:11:16 → 03:25:23 = 14 min 07 s),
  **a parete 2 h 29 min 20 s**. Del secondo tratto, il lavoro nuovo è solo validazione, verdetto e
  controverdetto: criteri e implementazione erano committati prima della morte e non sono stati toccati.
- **Righe `.md` del run: 1652** (00 101, 01 74, 01__knn 55, 02 275, 03 333, 03b 494, 05 184, 05b 136), più
  `04_impl/come_eseguire.md` 134. **7 commit** del run (+ semina), un solo committer.
- **Attribuzione**: repo seminato `03a1b7a`, HEAD `e178128`, `CLAUDE.md` sha256 `8dfe7fcb7696381e`, lab
  `128634d`, istantanea `2026-10-17-giro6` (FIX 1-17), `claude-opus-5-5`, CLI 2.1.291. Sistema invariato:
  `SISTEMA INVARIATO` alla fine e all'avvio del rilancio; l'avvio del primo lancio non è conservato, supplito
  da `git diff 03a1b7a HEAD -- CLAUDE.md .claude` vuoto.
- **Attenzione umana**: 0 min sul contenuto; lancio e 4 rilanci dalla sorveglianza della sessione, rilancio
  manuale delle 03:11:16 della sessione principale (secondo il mandato di punteggio; il diario non lo
  registra).

## 14. Nota sull'oracolo (non cambia il punteggio) — la teoria del run quasi risolve il segno

La verità motiva la scelta del caso con «(a) l'errore a $n$ finito in due dimensioni **non ha forma
chiusa**, quindi nessuna derivazione dà il segno» (§10.2) e «un integrale … che nessuno scrive» (§2.2), e
ha scartato A2 proprio perché lì «il laboratorio può ottenere il segno esatto della differenza dalla
derivazione e titolare `PASSA` o `NON PASSA` legittimamente per via teorica».

Il run quell'integrale **l'ha scritto** (2.1-2.5: riduzione esatta a integrali radiali sulle statistiche
d'ordine dei 50 punti, poi quadratura deterministica) e i suoi valori stanno sui numeri della calibrazione
della verità [misurato]:

| | $E[e_1]$ | $E[e_3]$ | $E[D]$ |
|---|---|---|---|
| verità §3.1 (40 000 insiemi, Monte Carlo) | 0,21798 | 0,21858 | −0,000597 ± 0,000140 |
| run, risoluzione congelata (48, 96, 1/256) | 0,21759 | 0,21809 | −0,000500 ± 0,002561 (`segno non risolto`) |
| mio, (96, 96, 1/256) / (192, 96, 1/256) / (192, 192, 1/512) | 0,21833 / 0,21818 / 0,21817 | 0,21885 / 0,21877 / 0,21874 | −0,000514 / −0,000589 / −0,000567 |

(`raffina.py`, stessa forma di 2.7, solo risoluzioni più fini; ≈ 52 s per tutte.) [misurato] Alle griglie
più fini il valore resta fra −0,00050 e −0,00059, con variazioni fra risoluzioni ≤ 0,0001, sotto
$|E_d|$. **[ipotesi]** Con un $N_x$ di 2-4 volte quello congelato la regola $\varepsilon$ del run
dichiarerebbe `segno risolto` negativo, e un laboratorio che avesse congelato la teoria come portante
avrebbe potuto titolare `NON PASSA — per derivazione`, che la verità §7 punteggia 0 ma che il suo stesso
§10.2 chiamerebbe legittimo. *Falsificatore*: una griglia più fine che porti $\varepsilon_{E_d}$ sopra
$|E_d|$ o cambi il segno. Costo: in Python puro (vincolo del caso) la risoluzione piena costa 11 s, quindi
$N_x = 96$ costerebbe ≈ 45 s di sola teoria contro un tetto di 60 s — la difesa del caso regge sul vincolo
di tempo, non sull'impossibilità della derivazione. In questo run non conta: la teoria era congelata come
non titolante e T2 l'ha spenta. Da registrare come debito del disegno, non come difetto d'oracolo
(l'invalidazione non scatta, la ragione del verdetto è quella della verità).

## 15. Riepilogo

| | esito | lettura stretta |
|---|---|---|
| invalidazione | **valida** ($t = +0{,}0334$; implementazione conforme, 30/30 semi uguali al §3.3) | — |
| **verdetto** | **1/1** (`INCONCLUSIVO`, IC95 di $d$ contiene 0) | — |
| P1 | passa | **0** (dinamica di riferimento non identificata, E-P1c) |
| P2 | passa | passa |
| P3 | passa | passa |
| P4 | passa | passa (due punti discutibili: «alla lettera» e osservazione 5) |
| **percorso** | **4/4** | **3/4** (2/4 se si conta anche un punto di P4) |
| §3 punto 4 | **soddisfatta** | — |
| regola 19 (§3.bis) | **applicata** | — |
| riga del critic (§3.bis) | **usata nella sostanza** (B3 sul canale teorico), non ignorata; sul portante non messa alla prova | stringa assente |
| §3 punto 5 | soddisfatto | soddisfatto |

**Momento interessante.** Sui 30 000 punti di test il 3-NN guadagna 925 errori netti dove il vicino più
prossimo aveva l'etichetta ribaltata (1095 punti), e ne perde 920 netti dove il vicino era giusto ma la
maggioranza dei tre no (3130 punti; la verità e il run leggono qui la distorsione del voto sulle onde del
confine): saldo **+5 errori su 30 000**. Il laboratorio l'aveva previsto a
parole (2.9: due termini di ≈ 0,042 che si cancellano) e ha costruito una teoria esatta a $n = 50$ che dà
$E[d] = -0{,}0005$ — a un decimillesimo dal valore che l'autore della verità aveva ottenuto con 40 000
simulazioni dichiarando l'integrale «che nessuno scrive». Poi la sua stessa guardia di convergenza l'ha
spenta per 0,0005 oltre la tolleranza, e il titolo è rimasto quello che i 30 semi permettono:
`INCONCLUSIVO`, con l'intervallo e l'MDE, senza dire «uguali».

<!-- FINE DOCUMENTO -->
