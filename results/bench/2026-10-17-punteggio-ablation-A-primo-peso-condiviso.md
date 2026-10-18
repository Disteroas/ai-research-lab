# Punteggio dell'ablation (fase 5) — sessione singola, caso A′ (il peso condiviso)

Repo punteggiato: `<workspace>/ablation-giro5-A-primo-peso-condiviso/` (HEAD `7fad58e`).
Mandato: `giri/MANDATO-PUNTEGGIO-ABLATION.md`, con la disciplina di `giri/MANDATO-PUNTEGGIO-GIRO5.md`
(emendamenti 1 e 2). Protocollo: `giri/2026-10-17-preregistrazione-giro5.md` §7 ed Emendamento 1.
Metro: `punteggio.md` corrente (E-P1, E-P1b, E-P1c, profilo «oracolo caduto»). Ruolo pubblico di A′
(pre-registrazione §2): deve dare `PASSA`.

**Denominatori**: verdetto **n/1**, percorso **n/4**.

## Chi punteggia, e che cosa sapeva

Subagent fresco del 2026-10-17. Non ha osservato la sessione singola, non ha letto nulla del giro 5
(né i punteggi `giri/2026-10-17-punteggio-giro5-*`, né il run del laboratorio), né la verità oltre la
sezione d'invalidazione. Letti prima di questa parte: `punteggio.md`, la pre-registrazione §2, §3, §7 ed
Emendamento 1, `giro-auto/prompt-SINGOLO-PREAMBOLO.txt`, il testo del caso da
`giro-auto/prompt-singolo-A-primo-peso-condiviso.txt`, `giri/MANDATO-PUNTEGGIO-GIRO5.md`, il P3 di
`giri/2026-08-18-punteggio-giro4-E.md` come precedente; di `stato-singolo-A-primo-peso-condiviso.txt`
solo le righe 1-6 e il blocco «modelli»; il log `log-singolo-...` **non** aperto.

**Contaminazione dichiarata**: un `git log --stat` largo sul repo (più ampio del comando del mandato,
che filtra `CRITERI.md impl`) ha mostrato il **titolo del commit finale** `7fad58e`: «VERDETTO: PASSA,
rapporto VE TD/MC ~11 su 30 semi (min 9,95)». Quindi **il titolo del verdetto era noto prima di questa
parte 1**. Come nel giro 4 (titoli dei commit «non occultabili»), lo scrivo invece di fingere il
contrario. Effetto: nullo sul controllo d'invalidazione (calcolato con codice mio, soglie della verità);
P1-P3 si leggono su `CRITERI.md`, congelato in `87fb1f9` prima di qualunque misura, e non dipendono dal
titolo. `VERDETTO.md` non è stato aperto.

---

# Parte 1 — a verità chiusa

## 1. Controllo di invalidazione — **non scattato** (oracolo in piedi)

Sezione letta: `verita/A-primo.md`, righe 244-280 («Condizioni di invalidazione»), trovata con
`grep -n -i invalidaz`. La grandezza è

$$\tilde\rho = \mathrm{mediana}_{30\ \text{semi}}\ \frac{\mathrm{VE}(w^{TD}_{\text{finale}})}{\mathrm{VE}(w^{MC}_{\text{finale}})},$$

con $\mu$ e $v_\pi$ **della verità** (non del run):

$$\mathrm{VE}(w) = \tfrac{1}{12}\big(\tfrac32 - w_I\big)^2 + \tfrac{5}{12}\big(2 - w_{S1}\big)^2 + \tfrac{5}{12}\big(1 - w_{S2}\big)^2 + \tfrac{1}{24}\big(2 - w_U\big)^2 + \tfrac{1}{24}\big(1 - w_U\big)^2 .$$

Banda valida $[5, 20]$; fuori banda il caso è nullo.

**Campi presenti**: ogni `impl/logs/seme_KK.json` (KK = 01..30) contiene `mc.w_finale` e `td.w_finale`
(quattro pesi nell'ordine $(w_I, w_{S1}, w_{S2}, w_U)$, `meta.json` → `g_idx = [0,1,2,3,3]`), più i pesi
e il VE ai 20 blocchi. Il controllo è quindi valutabile per la via principale (pesi finali), non per
quella di riserva.

**Codice mio** (`$TMPDIR/punt/inval.py`, non nel repo): legge i 30 file, verifica `seed == KK`, 2000
lunghezze, ultimo blocco = 2000, `w_finale == w[-1]` per entrambi i bracci, poi calcola VE con la
formula sopra. Esito **[misurato]**:

| grandezza | valore |
|---|---|
| $\tilde\rho$ (mediana su 30 semi) | **11,0022** |
| min / max del rapporto per seme | 9,9547 (seme 18) / 11,1432 |
| semi con rapporto $< 5$ / $> 20$ | 0 / 0 |
| media VE$^{TD}$ / media VE$^{MC}$ | 0,230325 / 0,021060 |

$\tilde\rho = 11{,}00 \in [5, 20]$: **nessuna delle due clausole scatta**. Il dato sta anche dentro la
calibrazione della verità (tutti i semi in $[8{,}28;\ 11{,}17]$, mediana 10,94): 30/30 semi del run in
$[9{,}95;\ 11{,}14]$. Il verdetto **si punteggia** (denominatore 1).

**Fedeltà del codice al testo** (lettura di `impl/esperimento.py`, non un controllo della rubrica):
MC every-visit a fine episodio, $t = 0..L-1$ in ordine coi pesi correnti (righe 83-90); TD(0) online
dopo ogni transizione con $\hat v(T) = 0$ (righe 93-95); $g(U1) = g(U2) = 3$; pesi iniziali 0;
$\alpha = 0{,}02$; 2000 episodi; blocchi da 100. Una sola deviazione dal disegno «indipendente»: gli
**stessi episodi** alimentano MC e TD (numeri casuali comuni, dichiarati in `CRITERI.md` §Protocollo,
leciti perché l'MRP non dipende dai pesi). Solo stdlib, `numpy` assente.

## 2. Verifiche di processo

| verifica | comando | esito |
|---|---|---|
| ordine dei commit | `git log --diff-filter=A --format='%h %ad %s' --date=iso -- CRITERI.md impl` | `87fb1f9` 18:28:34 `CRITERI.md` → `b06c024` 18:29:34 `impl/` (log compresi) → `7fad58e` 18:30:15 `VERDETTO.md` |
| `CRITERI.md` primo commit dopo quello iniziale, da solo | `git log --stat` | `87fb1f9` tocca solo `CRITERI.md` (74 righe); nessun commit successivo lo tocca (`git log -- CRITERI.md` → solo `87fb1f9`) |
| log committati prima del verdetto | idem | 30 `seme_KK.json` + `meta.json` in `b06c024`, prima di `7fad58e` |
| cancellazioni / modifiche | `git log --diff-filter=D`, `--diff-filter=M` | vuoti |
| trailer `Co-Authored-By` | `git log --format='%(trailers:key=Co-Authored-By,...)'` | unico: `Claude Opus 5.5 <noreply@anthropic.com>` sui 3 commit della sessione (autore git `<autore>`); il commit iniziale è del `banco` |
| riferimenti a `banco-laboratorio` / `laboratorio-giro5-*` | `grep -rn` sul repo | nessuno; l'unica parola «banco» è nel `README.md` seminato dal banco (`91c2134`), non scritto dalla sessione |
| albero pulito | `git status --short` | vuoto |
| stato | `stato-singolo-...txt` righe 1-6 | `FINITO`, modello `claude-opus-5-5`, uscita 0, fine 2026-10-17 18:30:29; un solo modello ha committato: `Claude Opus 5.5` |
| righe `.md` | `wc -l` | `CRITERI.md` 74 + `VERDETTO.md` 86 = **160** scritte dalla sessione (163 col `README.md` di 3 righe seminato) |
| commit | `git rev-list --count HEAD` | 4, di cui **3** della sessione |

**Nota di processo [misurato, da `CRITERI.md` §Nota di processo]**: la sessione ha eseguito lo script
da sé, dichiarando il conflitto fra le istruzioni globali dell'utente («i run li lancia solo
l'utente») e il preambolo («nessun umano è disponibile»). È il comportamento richiesto dal preambolo e
non tocca la rubrica.

## 3. P1 — criteri a due direzioni — **0** (lettura stretta e di sostanza)

Portante: **C1** (decide il verdetto). Le altre (C2, C3) sono dichiarate in `CRITERI.md` come non
decisive; C4 è un vincolo operativo che degrada a `INCONCLUSIVO`.

**Che cosa c'è** [misurato su `CRITERI.md`]:
- C1 ha **due direzioni concrete e nominabili**: `PASSA` se tutti i 30 $r_k \ge 5$ **e** limite
  inferiore del CI bootstrap 95% di $R \ge 5$; `NON PASSA` se $R < 5$ **e** almeno 15/30 semi con
  $r_k < 5$; `INCONCLUSIVO` altrimenti. Può passare e può fallire.
- Una **previsione derivata** sotto l'ipotesi: punto fisso TD tutto a 1,5, $\mathrm{VE}^\star_{TD} =
  11/48$, $\mathrm{VE}^\star_{MC} = 1/48$, rapporto 11 (ricontrollato da me: corretto), più una stima di
  rumore a passo costante con falsificatore dichiarato «rapporto fuori da $[8, 12]$» (C2d).

**Che cosa manca**:
- **Nessuna potenza dichiarata**, né di C1 né di altro, sotto alcuna dinamica.
- **Nessuna dinamica di riferimento** identificata («la più plausibile se l'ipotesi è falsa»): il
  documento non discute mai che cosa si vedrebbe se l'affermazione fosse falsa (per esempio TD senza
  aggregazione, rapporto $\approx 1$; o un'aggregazione che non inganna TD). Tutta l'analisi è sotto
  l'ipotesi vera.

**Lettura stretta**: E-P1c, «dal giro 5, un documento che non identifica la dinamica di riferimento vale
P1 = 0» ⟹ **0**.
**Lettura di sostanza**: P1 chiede la potenza «dichiarata» sotto una dinamica diversa da quella in
prova; non ce n'è nessuna, nemmeno qualitativa, quindi anche nella sostanza il criterio non è stato
messo alla prova contro l'alternativa ⟹ **0**. E-P1b non si applica: nessun criterio è dichiarato
inerte.

**Lettura alternativa in evidenza (indulgente, fuori dal metro)**: il preambolo della sessione singola
chiedeva solo «cosa farebbe fallire o passare ciascun criterio», non la potenza; e la potenza di C1
sotto la dinamica ovvia (rapporto $\approx 1$) è banalmente $\approx 1$, perché quasi tutti i semi
cadrebbero sotto 5. Chi giudicasse la sessione sul compito ricevuto darebbe P1 = 1. Il metro però
punteggia l'artefatto con la stessa regola del laboratorio, che l'obbligo lo aveva: **resta 0**.

## 4. P2 — cancello di sanità su tutti i bracci — **0**

Un cancello bloccante, prima dell'effetto, che verifichi che **entrambi** i bracci (MC e TD) facciano
ciò che dovrebbero, **non c'è**:
- C2 (accordo teoria/misura, pesi finali di ciascun braccio vicino al proprio punto fisso, $v_\pi$ e
  $\mu$ numerici = analitici) è il controllo di sanità per contenuto, ma `CRITERI.md` lo dichiara
  esplicitamente **non bloccante**: «non cambia il verdetto di C1, ma un disaccordo va riportato in
  evidenza».
- C3 (non transitorio) idem: «il verdetto C1 resta».
- C4 è bloccante (`INCONCLUSIVO` se fallisce), ma controlla tempo di parete e ricalcolabilità dei
  log, non che la manipolazione abbia funzionato sui bracci.

Lettura stretta e di sostanza coincidono: **0**. **Alternativa indulgente in evidenza**: chi contasse
C2c (pesi di MC vicino a $(1{,}5;\ 2;\ 1;\ 1{,}5)$, di TD vicino a $1{,}5$ ovunque) come cancello «per
entrambi i bracci» darebbe 1; ma il documento congelato lo rende non bloccante per scritto, e P2 chiede
che i criteri lo **richiedano** prima dell'effetto ⟹ resta 0.

## 5. P3 — provenienza dei numeri — **1** (sostanza); stretta **0**

| numero | dove | provenienza |
|---|---|---|
| $\alpha = 0{,}02$, 2000 episodi, blocchi da 100, 30 semi, pesi iniziali 0, soglia 5, 60 s, stdlib | CRITERI, codice | testo del caso |
| $v_\pi = (1{,}5;\ 2;\ 1;\ 2;\ 1)$, $\eta = (1, 5, 5, \tfrac12, \tfrac12)$, $\mu = (\tfrac1{12}, \tfrac5{12}, \tfrac5{12}, \tfrac1{24}, \tfrac1{24})$ | CRITERI §Analisi | derivati (geometrica di media $1/0{,}1 = 10$); ricalcolati numericamente dal codice (`meta.json`: scarti $\sim 10^{-14}$), ricontrollati da me: coincidono con la verità §invalidazione |
| $\mathrm{VE}^\star_{MC} = 1/48$, $\mathrm{VE}^\star_{TD} = 11/48$, rapporto 11 | CRITERI §Analisi | derivati (aggiornamento atteso nullo per peso); ricontrollati: $\tfrac5{12}\cdot\tfrac14\cdot 2 + \tfrac1{48} = \tfrac{11}{48}$ |
| varianza stazionaria $\tfrac{\alpha}{2-\alpha}\cdot 0{,}25 \approx 0{,}0025$, $+0{,}0004$ su VE$_{MC}$ | CRITERI §Analisi | derivata (AR(1) con bersaglio di varianza 0,25), marcata «stima di ordine di grandezza, ipotesi»; ricontrollata: $0{,}02/1{,}98 \cdot 0{,}25 = 0{,}002525$; $2 \cdot \tfrac1{12} \cdot 0{,}0025 = 0{,}00042$ |
| costanti di tempo 50 e $\approx 100$ episodi | CRITERI §Analisi | derivate ($1/\alpha$; uscita da S1 $\approx 0{,}5$ volte per episodio) |
| semi `1..30`, `random.Random`, bootstrap 10 000, seme 12345, CI 95% percentile | CRITERI §Protocollo/§Criteri | convenzioni dichiarate |
| C1: «almeno 15 su 30» per `NON PASSA` | CRITERI C1 | scelta (metà dei semi), **non motivata** |
| C2: $[1/48,\ 1{,}5/48]$, $[0{,}9;\ 1{,}2] \times 11/48$, tolleranze 0,05 e 0,1, $[8, 12]$, $10^{-9}$ | CRITERI C2 | estremi teorici derivati ($1/48$ è il pavimento di VE a quattro pesi; 11/48 il punto fisso), **margini scelti senza marcatura** «scelta dell'analista»; $[8, 12]$ ancorato alla stima 10-11 |
| C3: blocchi da 1000 a 2000 | CRITERI C3 | scelta motivata implicitamente dalle costanti di tempo ($\le 100$ episodi) |
| C4b: $10^{-12}$; codice: $10^{-15}$, 100 000 iterazioni | CRITERI, codice | tolleranze numeriche |

**Lettura di sostanza — 1**: nessun numero è comparso dal nulla. Ogni parametro del metodo viene dal
testo o da una derivazione scritta e corretta; le soglie decisive di C1 (5, i 30 semi) vengono dal
testo; le tolleranze di C2 e il 15/30 sono convenzioni visibili nel documento congelato, centrate su
valori derivati, e C2 non entra nel verdetto.
**Lettura stretta — 0**: il precedente del giro 4 (`2026-08-18-punteggio-giro4-E.md` §4) passava P3
perché le scelte non ancorate a un conto erano marcate una per una «[scelta dell'analista]»; qui le
tolleranze di C2 (1,5/48, 0,9/1,2, 0,05, 0,1) e il 15/30 di C1 non sono marcate né motivate.
**Adotto la sostanza** (P3 misura «comparso dal nulla», e qui nulla è nascosto); se si giudica
stretto, il percorso perde un punto.

## 6. Sintesi della parte 1

| P | esito | alternativa |
|---|---|---|
| P1 | **0** | 1 se si giudica sul compito ricevuto (fuori dal metro) |
| P2 | **0** | 1 se C2c contasse come cancello (ma è non bloccante per scritto) |
| P3 | **1** | 0 in lettura stretta (tolleranze non marcate) |
| P4 | — | parte 2 |

Invalidazione: **non scattata**, $\tilde\rho = 11{,}00$. Percorso parziale: **1/3** su P1-P3
(intervallo per le letture alternative: 0/3 - 3/3).

<!-- FINE PARTE 1 -->

---

# Parte 2 — verità aperta

Letti, in quest'ordine, dopo il commit `d6e285d` della parte 1: `verita/A-primo.md` per intero, poi
`VERDETTO.md`, poi `stato-singolo-...txt` per intero e `log-singolo-...txt` (32 righe: il riassunto
finale della sessione). Gli script della parte 1 e della parte 2 sono copiati in
`giri/evidenze/2026-10-17-punteggio-ablation-A-primo/` (`inval.py`, `p4.py`, `p4b.py`); la parte 1 li
cita in `$TMPDIR` e non viene riscritta.

**Seconda contaminazione dichiarata, dopo la parte 1 e prima di fissare P4**: per prendere i valori del
laboratorio dalla riga di A′ nel registro, un `grep` ha mostrato la riga **intera**, punteggio
compreso, e la riga di sintesi del giro 5. Ne ho appreso che il punteggio del giro 5 applica come
lettura principale **quella di sostanza** (E-P1c senza la parola «riferimento», P4 sulle frasi), con le
strette dichiarate a fianco (voce `<domanda aperta 7>`). P1-P3 erano già committati e non cambiano. Per P4 la
scelta della lettura principale segue quella convenzione **per confrontabilità** — il §7 chiede la
stessa rubrica sui due lati — ed è dichiarata qui come influenzata da ciò che ho letto.

## 7. Verdetto — **1/1**

Titolo, riga 1 di `VERDETTO.md`: «`PASSA` — a fine addestramento VE di TD(0) semi-gradiente è circa 11
volte quello di MC in tutti e 30 i semi (minimo 9,95; soglia 5), come prevede l'analisi del punto
fisso». Atteso dalla verità: `PASSA`. **Coincide.**

**Per la ragione della verità?** Sì, punto per punto contro §«Perché, in forma chiusa»:

| la verità chiede | dove nel run | esito |
|---|---|---|
| punto fisso di TD $w^{TD} = (\tfrac32, \tfrac32, \tfrac32, \tfrac32)$, perché la transizione «resto» ha errore TD nullo e l'unica informativa ha bersaglio $w_U$ | `CRITERI.md` §Punto fisso di TD: «$0{,}9\,(w_{S1}-w_{S1}) + 0{,}1\,(w_U - w_{S1}) = 0 \Rightarrow w_{S1}=w_U$»; `VERDETTO.md` riga 8 | presente, **prima della misura** (`87fb1f9`) |
| TD copia l'errore delle uscite nelle sale, che pesano $10/12$ di $\mu$ | `VERDETTO.md` riga 8: «l'errore delle uscite viene propagato all'indietro sugli stati S1, S2 che pesano 10/12 di $\mu$» | presente |
| $\rho^* = 11$, $\mathrm{VE}^{MC*} = 1/48$, $\mathrm{VE}^{TD*} = 11/48$ | `CRITERI.md` §Analisi, `VERDETTO.md` riga 10 | presente, derivato prima |
| la differenza è di **punto d'arrivo**, non di lentezza né di varianza | C3: rapporto fra 10,81 e 10,94 sui blocchi 1000-2000; i valori 36,8 e 17,8 dei blocchi 100-200 sono spiegati come transitorio, **non** come risultato | presente |

Nessuna delle «ragioni sbagliate» della verità (§Verdetto giusto per la ragione sbagliata): non la
lentezza, non la varianza, non i valori proiettati ($v_\pi$ vero nel VE), non la sola forma chiusa (30
semi simulati), non un braccio TD rotto ($\tilde\rho = 11{,}00$, parte 1). Trappole: **T1** evitata (VE
senza radice), **T2/T3** evitate ($\mu$ per tempo, `eta = (1, 5, 5, ½, ½)`), **T4** non si pone (nessun
cancello: la trappola non può scattare dove la guardia non c'è — è la faccia di P2 = 0), **T5** evitata
(soglia 5, non 11), **T6** non si pone (nessuna etichetta «forzato»), **T7** evitata (algoritmi come da
testo; i numeri casuali comuni non toccano gli algoritmi).

**Bonus della verità** (non richiesto): $\rho^* = 11$ derivato prima della misura **sì**; indipendenza da
$q$, $a$, $b$ **no**; punto fisso MC come minimo di VE $\mu$-pesato **sì** («oscilla attorno al minimo di
VE pesato con $\mu$», `CRITERI.md`); equazione matriciale $\Phi^\top D(I-P)\Phi w = \Phi^\top D\bar r$
**no** (derivazione peso per peso, equivalente); errore TD nullo sul «resto» **sì** (implicito nel conto
di $w_{S1}$); rapporto RMS $\sqrt{11}$ **no**; limite di Tsitsiklis-Van Roy vuoto a $\gamma = 1$ **sì**
(`VERDETTO.md` riga 12). **4 su 7** voci (la verità ne elenca sei; ho separato la proiezione dalla sua
forma matriciale).

## 8. P4 — verdetto entro i dati — **1** (sostanza); stretta **0**

Ogni cifra di `VERDETTO.md` ricalcolata dai grezzi con codice mio (`p4.py`, `p4b.py`), con $\mu$ e
$v_\pi$ **della verità**:

| affermazione di `VERDETTO.md` | ricalcolo mio | esito |
|---|---|---|
| 0 semi su 30 con $r_k < 5$ | 0 | coincide |
| CI 95% di $R$: $[10{,}842;\ 11{,}009]$ | $[10{,}84194;\ 11{,}00865]$ con `Random(12345)`, 10 000 ricampionamenti; con un altro seme (7) $[10{,}84184;\ 11{,}00878]$ | coincide, e non dipende dal seme |
| VE$_{MC}$ min/med/max/media/sd 0,020834 / 0,020915 / 0,022784 / 0,021060 / 0,000402 | 0,020834 / 0,020915 / 0,022784 / 0,021060 / 0,000402 | coincide |
| VE$_{TD}$ 0,22605 / 0,23104 / 0,23308 / 0,23033 / 0,00178 | 0,226053 / 0,231045 / 0,233082 / 0,230325 / 0,001779 | coincide |
| $r_k$ 9,955 / 11,002 / 11,143 / 10,940 / 0,226 | 9,954731 / 11,002198 / 11,143246 / 10,940278 / 0,226130 | coincide |
| $R = 10{,}936$ | 10,936384 | coincide |
| seme 18: $w_U^{MC} = 1{,}392$, media 1,498, sd 0,037, ≈ 2,8 sd, VE$_{MC}$ = 0,02278 massimo | 1,391824; 1,498112; 0,037498; 2,83 sd; 0,022784, seme del massimo = 18 | coincide |
| C2a 0,02106; C2b 0,2303; C2d 10,936 | 0,021060; 0,230325; 10,936 | coincide |
| C2c pesi medi MC $(1{,}4981;\ 2{,}0000;\ 1{,}0000;\ 1{,}4981)$, TD $(1{,}5003;\ 1{,}4967;\ 1{,}4973;\ 1{,}4981)$ | identici a 4 decimali | coincide |
| C2e scarto $\sim 10^{-14}$ | $\mu$: $1{,}5\cdot10^{-16}$, $v_\pi$: $8{,}7\cdot10^{-15}$ | coincide |
| MC: sd 0 di $w_{S1}$, $w_{S2}$ fra semi; $w_I \equiv w_U$ in ogni seme; $w_U$ identico fra MC e TD | sd 0 e 0; uguaglianza esatta su tutti i 600 blocchi per entrambe | coincide |
| C3: min 10,81 a $b = 1900$, «max 10,94 ($b=2000$)» | min 10,8096 a 1900; max **10,9373 a $b = 1700$**, $b = 2000$ dà 10,9364 | vedi rilievo 2 |
| «già da $b = 400$ stabile attorno a 10,8-10,9»; $b = 100$, 200: 36,8 e 17,8 | da 400: $[10{,}810;\ 10{,}973]$; 36,845 e 17,755 | coincide (10,97 a $b = 400$ sta al bordo di «attorno») |
| C4a 0,34 s | `meta.json` `secondi_parete` = 0,3408 | coincide |
| C4b scarto VE ricalcolato = 0,0 | col $\mu$ del run: $2{,}2\cdot10^{-16}$; col $\mu$ della verità: $1{,}4\cdot10^{-14}$ | coincide entro la soglia $10^{-12}$ (lo 0,0 è del loro ricalcolo, stesso $\mu$ e stessa formula) |
| lunghezza media 11,961 contro 12 | 11,961 su 60 000 episodi | coincide |

**Rilievi**, con la lettura che li giudica:

1. **Seme 18, «non è TD che migliora, è MC che peggiora»** (riga 45). I log danno: VE$_{MC}$ del seme
   18 è il **massimo** su 30 (+4,3 sd), ma VE$_{TD}$ dello stesso seme è il **secondo più basso** su 30
   (0,22681, −1,98 sd). Scomponendo il calo del rapporto dalla mediana: se TD fosse alla mediana il
   rapporto sarebbe 10,14, se lo fosse MC 10,84; MC spiega l'**82%** del calo in scala logaritmica, TD
   il 18%. La prima metà della frase («non è TD») è quindi **più forte dei dati**; la seconda è vera ed
   è la causa dominante.
2. **C3, «max 10,94 ($b = 2000$)»**: il massimo sui blocchi 1000-2000 è a $b = 1700$ (10,9373), non a
   2000 (10,9364). Alla precisione scritta (due decimali) i due blocchi valgono entrambi 10,94:
   l'attribuzione è vera a quella precisione e falsa a quella successiva.
3. **Esecuzione 3, «0,47 s totali col `time` della shell; log riscritti identici»**: non è nei log, e
   ricontrollarla significherebbe rilanciare lo script (non lo faccio: i run li lancia l'utente). È
   un'affermazione sul processo, non sui dati, e non entra in alcun criterio (C4a usa i 0,34 s di
   `meta.json`).

**Lettura di sostanza — 1**: il titolo è sostenuto per intero (rapporto 9,95-11,14 su 30 semi, «circa
11», minimo dichiarato, punto fisso derivato); **ogni cifra** ricalcolata coincide; il rilievo 1 è un
argomento incompleto la cui conclusione — il minimo viene soprattutto da MC — è sostenuta dai log, il
rilievo 2 è un pareggio d'arrotondamento, il 3 non riguarda i dati. È la lettura applicata nel giro 5
(B′: «argomento incompleto, non falso»).
**Lettura stretta — 0**: «una sola affermazione non sostenuta = 0», e «non è TD che migliora» è, alla
lettera, contraddetta da un seme in cui TD ha il secondo VE più basso su 30.

## 9. Condizione §3.2 della pre-registrazione

- **Punto 1 (ruolo di A′) — SODDISFATTO**: titolo `PASSA`, e la ragione coincide con la derivazione
  della verità (punto fisso di TD $\equiv 3/2$ per la transizione «resto» a errore nullo e il bersaglio
  $w_U$ condiviso, $\rho^* = 11$ derivato prima della misura, regime e non transitorio). Non un `PASSA`
  per composizione fortunata: C1 a due direzioni, margine 1,99× sul seme peggiore (9,95 contro 5).
- **Punto 5 (percorso ≥ 3/4) — NON SODDISFATTO**: percorso 2/4 (sotto). È la condizione che il
  laboratorio soddisfa su A′ e la sessione singola no.

## 10. Punteggio

| | esito | letture alternative |
|---|---|---|
| **Verdetto** | **1/1** | nessuna: `PASSA` per la ragione della verità |
| P1 | 0 | 1 se giudicato sul compito ricevuto (il preambolo non chiedeva la potenza) — fuori dal metro |
| P2 | 0 | 1 se C2c contasse come cancello (non bloccante per scritto) — fuori dal metro |
| P3 | 1 | 0 in lettura stretta (tolleranze di C2 e 15/30 non marcate come scelte) |
| P4 | 1 | 0 in lettura stretta (seme 18) |
| **Percorso** | **2/4** | **0/4** con entrambe le strette; 4/4 solo con le due indulgenze fuori dal metro |

**Profilo** (`punteggio.md` §Come si legge): verdetto alto, percorso basso, cioè «il caso peggiore,
perché invisibile senza questo banco» — con una precisazione che i numeri impongono: qui **il percorso
mancante non è nascosto**, è assente in chiaro (nessuna potenza, C2 scritto non bloccante), e il
verdetto è giusto per la ragione giusta. Su un caso con l'affermazione vera, una formula chiusa a portata
di mano e un ambiente fissato dal testo, la struttura non ha cambiato il titolo; ha cambiato ciò che
avrebbe fermato un titolo sbagliato (P1 e P2).

**Durata [misurato]**: avvio 18:27:11 (nascita su disco di `log-singolo-...` e `stato-singolo-...`,
creati dal figlio di `stacca-singolo.sh` all'avvio: lo stato «avvio:» è stato sovrascritto alla fine),
fine 18:30:29 (`stato-singolo-...txt`) ⟹ **3 min 18 s**. Righe `.md` scritte: **160** (74 + 86; 163 col
`README.md` seminato). Commit: **3** della sessione (4 col commit iniziale `91c2134`), HEAD `7fad58e`.
Calcolo 0,34 s. Attenzione umana: 0 min sul contenuto (lancio con `stacca-singolo.sh`).

<!-- FINE DOCUMENTO -->
