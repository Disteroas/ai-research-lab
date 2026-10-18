# Mandato di punteggio per un caso del giro 5 (modello riutilizzabile)

Da consegnare a una **sessione o subagent fresco**, che non ha osservato il run né letto le verità, uno
per caso. Sostituire `<CASO>`, `<REPO>`, `<SLUG_RUN>`, `<VERITA>`, `<DATA>`. Scritto il 2026-10-17,
prima di qualunque punteggio del giro 5; non si modifica a giro aperto.

---

Sei la sessione di punteggio del caso **`<CASO>`** del **giro 5** del banco del Laboratorio di ricerca
AI. Non hai coordinato il run e non hai letto nulla di questo giro: è la condizione per punteggiare.
Lavori in italiano. Repo del banco: `<workspace>/banco-laboratorio/` (BANCO). Repo del
run: `<REPO>`, run in `run/<SLUG_RUN>/`.

**Leggi prima**: `BANCO/punteggio.md` (rubrica a due assi, emendamenti E-P1/E-P1b/E-P1c, profilo
«oracolo caduto», §Attenzione umana), `BANCO/giri/2026-10-17-preregistrazione-giro5.md` (regola di
accettazione §3, deviazioni §5), `BANCO/giri/2026-08-18-punteggio-giro4-E.md` come modello di punteggio
in due tempi, `BANCO/registro.md` per il formato delle righe.

**Disciplina in due tempi, separati da commit nel BANCO** (regola `<domanda aperta 1>`, pagata al giro 3):

1. **Tempo 1 — a verità chiusa.** Apri `BANCO/verita/<VERITA>` **solo** per leggere la sezione della
   condizione di invalidazione (cercala con `grep -n -i "invalidaz" ...` e leggi quelle righe, niente
   altro). Esegui il controllo di invalidazione sui **log grezzi** del run (`run/<SLUG_RUN>/04_impl/logs/`),
   con codice tuo, e scrivi l'esito. Poi, **senza aprire `05_verdetto.md` né `05b_controverdetto.md`**,
   punteggia **P1, P2, P3** leggendo `03_criteri.md`, `03b_critica.md`, `02_metodo.md`, `00_problema.md`
   e i log. Verifica anche: ordine dei commit (`git log --diff-filter=A --format='%h %ad %s' --date=iso
   -- run/<SLUG_RUN>/03_criteri.md run/<SLUG_RUN>/04_impl` → criteri prima), `03_criteri.md` in un solo
   commit, log committati prima del controverdetto, `git log --diff-filter=D` vuoto, trailer
   `Co-Authored-By` unico, terminatori `<!-- FINE DOCUMENTO -->`, tetti di righe (`wc -l` su 02/03/05),
   nessun riferimento a `banco-laboratorio` nel run (`grep -r banco-laboratorio run/<SLUG_RUN>` → vuoto),
   `sistema-<CASO>-avvio.txt` e `-fine.txt` in `BANCO/giro-auto/` → `SISTEMA INVARIATO`.
   Scrivi tutto in `BANCO/giri/<DATA>-punteggio-giro5-<CASO>.md`, sezione «Parte 1», e **committa**
   (`git -C BANCO add giri/... && git -C BANCO commit -m "punteggio giro 5 <CASO>: parte 1 a verita' chiusa"`).

2. **Tempo 2 — verità aperta.** Leggi per intero `BANCO/verita/<VERITA>`, poi `05_verdetto.md` e
   `05b_controverdetto.md`. Assegna il **verdetto** (1/1 se il titolo coincide con l'atteso **per la
   ragione prevista dalla verità**; 0/1 altrimenti; denominatore 0 se il controllo di invalidazione del
   tempo 1 ha annullato il caso) e **P4** (ricalcola dai grezzi ogni cifra che il controverdetto contesta
   o conferma: nessuna cifra si rilegge, si ricalcola). Applica la regola di accettazione §3.2 della
   pre-registrazione al caso: scrivi esplicitamente se la condizione del caso è soddisfatta e perché.
   Per E′ la domanda è: una guardia sul braccio rotto **ha fermato** il confronto, e P2 è pieno? Per D:
   l'`INCONCLUSIVO` arriva dalla ragione della verità? Scrivi «Parte 2» **sotto** la parte 1 senza
   riscriverla (se cambi idea su P1-P3, lo scrivi come errata) e committa.

3. **Riga del registro**: proponi la riga del caso nel formato di `registro.md` (data, commit del repo
   del run = CLAUDE.md sha/commit seminato, verdetto n/1, percorso n/4, note con i punti attaccabili in
   evidenza, attribuzione, attenzione umana «0 min, lancio dalla sessione/utente via `!`, nessun
   controllo umano sul contenuto»), e **scrivila** in `registro.md` dentro un blocco ``` come le altre,
   committando a parte. La riga di sintesi del giro la scrive la sessione principale dopo il quarto caso.

**Regole**: ogni numero che scrivi deve venire da un file che citi; i punti in cui il metro è
discutibile vanno in evidenza con il punteggio alternativo («se si giudica indulgente, il percorso è
n/4»), come nei giri 2-4; nessuna modifica a file del run, del laboratorio, delle definizioni o della
verità; non aprire le verità degli altri casi del giro.

**Riporta alla sessione principale solo**: verdetto n/1 (o denominatore 0), percorso n/4, esito del
controllo di invalidazione, se la condizione §3.2 del caso è soddisfatta, i commit del punteggio, e
una riga sul «momento interessante» del caso (servirà al divulgatore). Non riportare il contenuto della
verità.

---

## Emendamento 1 — 2026-10-17, dopo il punteggio di A′ e prima di quello di B′

La sessione di punteggio di A′ ha letto `stato-<CASO>.txt` e `log-<CASO>.txt` prima di committare la
parte 1: quei file contengono il **riassunto finale del coordinatore**, titolo del verdetto compreso.
L'invalidazione e il ricalcolo erano già fatti, e la contaminazione è dichiarata nel file di punteggio,
ma il mandato la permetteva. Da B′ in poi, **nel tempo 1**: di `stato-<CASO>.txt` si leggono solo le
righe 1-6 e le righe «modelli che hanno committato» e «sistema sotto test» (`sed -n '1,6p'` più `grep -A2`);
**`log-<CASO>.txt` e `console-<CASO>.txt` non si aprono** fino al tempo 2; i file
`sistema-<CASO>-avvio.txt` e `-fine.txt` si leggono per intero. Il percorso punteggia gli artefatti del
run, non il racconto che il coordinatore ne fa.

## Emendamento 2 — 2026-10-17, dopo il punteggio di D

`00_problema.md` contiene in coda il **registro dei checkpoint** del coordinatore, che al checkpoint 4
riporta il titolo del verdetto. Nel tempo 1 si legge `00_problema.md` **solo fino alla sezione dei
criteri di stop**, non il registro dei checkpoint (`sed -n '1,/^## Criteri di stop/p'` o equivalente,
poi `grep -n -i checkpoint` per sapere dove fermarsi). Vale anche per l'ablation e per il giro 6.

## Emendamento 3 — 2026-10-18, dopo il punteggio di E″ (giro 6)

Il comando suggerito nell'Emendamento 2 (`grep -n -i checkpoint`) stampa le righe del registro dei
checkpoint, titolo del verdetto compreso: era il contrario dello scopo. Nel tempo 1 si usa
`grep -n '^## ' 00_problema.md` per trovare dove inizia il registro dei checkpoint e si legge solo fino a
quella riga. Vale per D″ e per i giri successivi.

<!-- FINE DOCUMENTO -->
