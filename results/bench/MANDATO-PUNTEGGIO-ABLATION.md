# Mandato di punteggio per una sessione singola dell'ablation (fase 5, giro 5)

Variante di `MANDATO-PUNTEGGIO-GIRO5.md` (emendamenti compresi) per i repo `ablation-giro5-<CASO>`:
stessa rubrica a due assi, stessa disciplina in due tempi, file diversi. Scritto il 2026-10-17 prima di
qualunque punteggio dell'ablation. Sostituire `<CASO>`, `<VERITA>`, `<DATA>`.

---

Sei la sessione di punteggio della **sessione singola** (ablation, fase 5) sul caso **`<CASO>`**. Non hai
osservato quella sessione né letto nulla del giro 5: è la condizione per punteggiare. Lavori in italiano.
Repo del banco: `<workspace>/banco-laboratorio/` (BANCO). Repo della sessione singola:
`<workspace>/ablation-giro5-<CASO>/`.

**Leggi prima**: `BANCO/punteggio.md`; `BANCO/giri/2026-10-17-preregistrazione-giro5.md` §7 (protocollo
dell'ablation) e il suo Emendamento 1; `BANCO/giro-auto/prompt-SINGOLO-PREAMBOLO.txt` (ciò che la sessione
singola ha ricevuto oltre al testo del caso); `BANCO/giri/MANDATO-PUNTEGGIO-GIRO5.md` per la disciplina.

**File della sessione singola** (al posto di `00..05b`): `CRITERI.md` (criteri, soglie, semi: deve
essere il **primo commit** dopo quello iniziale del repo, da solo), `impl/` con `impl/logs/` (log grezzi),
`VERDETTO.md` (prima riga = titolo `PASSA` / `NON PASSA` / `INCONCLUSIVO`). Non esiste un controverdetto:
**P4 lo decidi tu** rileggendo `VERDETTO.md` contro i log grezzi con codice tuo, come farebbe il critic.

**Tempo 1 — a verità chiusa**: controllo di invalidazione di `BANCO/verita/<VERITA>` (solo la sezione,
via grep) sui log grezzi, con codice tuo; se i log non permettono il controllo (mancano i campi), scrivilo:
è un dato sul percorso. Poi, **senza aprire `VERDETTO.md`**, P1 (criteri a due direzioni, potenza sotto
una dinamica diversa da quella in prova; E-P1b/E-P1c come nel giro 5, lettura di sostanza e stretta
dichiarate entrambe), P2 (cancello di sanità su tutti i bracci, prima dell'effetto, bloccante), P3
(provenienza di ogni numero di `CRITERI.md` e del codice: fonte o derivazione). Verifica: ordine dei
commit (`git log --diff-filter=A --format='%h %ad %s' --date=iso -- CRITERI.md impl`), `CRITERI.md` in un
commit solo, log committati, trailer `Co-Authored-By` unico, nessun riferimento a `banco-laboratorio` o a
`laboratorio-giro5-*` nel repo, `BANCO/giro-auto/stato-singolo-<CASO>.txt` (righe 1-6 e «modelli»; non il
log). Scrivi «Parte 1» in `BANCO/giri/<DATA>-punteggio-ablation-<CASO>.md` e **committa** (file specifico).

**Tempo 2 — verità aperta**: leggi `BANCO/verita/<VERITA>` per intero, poi `VERDETTO.md`. Verdetto 1/1
se il titolo coincide con l'atteso **per la ragione prevista dalla verità**, 0/1 altrimenti, denominatore 0
se l'oracolo è caduto al tempo 1. P4: ogni cifra di `VERDETTO.md` ricalcolata dai grezzi; una sola
affermazione non sostenuta = 0 (stesso metro del laboratorio). Applica al caso la **stessa condizione §3.2**
del ruolo (PASSA / NON PASSA / stop con guardia / INCONCLUSIVO per la ragione giusta) e scrivi se la
sessione singola la soddisfa. «Parte 2» sotto la parte 1, committa.

**Tabella di confronto**: proponi e scrivi in `BANCO/registro.md`, in un blocco ```, la riga
`ABLATION <CASO> | <data> | verdetto n/1 | percorso n/4 | lab: verdetto n/1 · percorso n/4 | righe .md
singolo/lab | durata singolo/lab | commit singolo/lab | note`, prendendo i valori del laboratorio dalla riga
del caso già nel registro (solo quella riga, non il suo punteggio). Committa a parte.

**Regole**: ogni numero da un file citato; letture alternative in evidenza; nessuna modifica al repo della
sessione singola, al laboratorio, al banco oltre ai tuoi file; non aprire le verità degli altri casi.
**Riporta solo**: verdetto n/1, percorso n/4 con i P, invalidazione, condizione §3.2, commit, durata e
righe, e una riga sul confronto col laboratorio (chi ha fatto cosa che l'altro non ha fatto).

<!-- FINE DOCUMENTO -->
