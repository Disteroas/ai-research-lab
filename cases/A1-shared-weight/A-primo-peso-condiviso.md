# Monte Carlo e TD(0) con un peso condiviso

*Questo file si consegna al laboratorio così com'è, dal titolo in giù. Non aggiungere nulla.*

---

## Problema

Per valutare una politica fissata con un'approssimazione della funzione di valore, le due scelte di base sono **Monte Carlo a gradiente**, che aggiorna la stima verso il ritorno osservato, e **TD(0) semi-gradiente**, che la aggiorna verso la ricompensa più la stima corrente dello stato successivo. In versione tabellare i due metodi convergono agli stessi valori, e TD ha bersagli meno rumorosi: per questo è spesso la scelta predefinita anche quando la rappresentazione non è tabellare.

Affermazione da mettere alla prova: **sull'ambiente qui sotto, con la rappresentazione data, a fine addestramento l'errore di valore VE di TD(0) semi-gradiente è almeno 5 volte quello di Monte Carlo a gradiente.**

## Ambiente su cui lavorare

Fissato, non è oggetto di scelta. Un processo di Markov con ricompense — la politica è già dentro le probabilità di transizione, non ci sono azioni da scegliere — episodico e **senza sconto** ($\gamma = 1$):

- Stati non terminali `I`, `S1`, `S2`, `U1`, `U2`; stato terminale `T`. Ogni episodio parte da `I`.
- Da `I`: a `S1` o a `S2` con probabilità 1/2 ciascuna, ricompensa 0.
- Da `S1`: resta in `S1` con probabilità **0,9**, passa a `U1` con probabilità **0,1**; ricompensa 0 in entrambi i casi. Da `S2`, allo stesso modo: resta con probabilità 0,9, passa a `U2` con probabilità 0,1, ricompensa 0.
- Da `U1`: a `T` con ricompensa **+2**. Da `U2`: a `T` con ricompensa **+1**.

**Rappresentazione**: aggregazione di stati, quattro pesi $w = (w_I, w_{S1}, w_{S2}, w_U)$. La stima è $\hat v(I) = w_I$, $\hat v(S1) = w_{S1}$, $\hat v(S2) = w_{S2}$ e **$\hat v(U1) = \hat v(U2) = w_U$**: le due uscite condividono un peso. $\hat v(T) = 0$. Pesi iniziali tutti **0**. Sotto, $g(s)$ indica il peso usato dallo stato $s$.

I due algoritmi, identici in tutto tranne il bersaglio dell'aggiornamento:

- **Monte Carlo a gradiente, every-visit**: a fine episodio, per $t = 0, 1, \dots, L-1$ in quest'ordine ($L$ = lunghezza dell'episodio) e coi pesi correnti, $w_{g(S_t)} \leftarrow w_{g(S_t)} + \alpha\,[G_t - \hat v(S_t)]$, dove $G_t$ è la somma delle ricompense da $t+1$ alla fine dell'episodio.
- **TD(0) semi-gradiente, online**: dopo ogni transizione $S_t \to S_{t+1}$ con ricompensa $R_{t+1}$, $w_{g(S_t)} \leftarrow w_{g(S_t)} + \alpha\,[R_{t+1} + \hat v(S_{t+1}) - \hat v(S_t)]$.
- **$\alpha = 0{,}02$** costante per entrambi. **2000 episodi** per algoritmo e per seme.

I due algoritmi si implementano **esattamente come specificati**: il bersaglio è l'oggetto del confronto, non un iperparametro da aggiustare.

**Errore di valore**:

$$\mathrm{VE}(w) = \sum_{s \in \{I,\, S1,\, S2,\, U1,\, U2\}} \mu(s)\,\big[v_\pi(s) - \hat v(s, w)\big]^2$$

dove $v_\pi(s)$ è il valore vero dello stato e $\mu(s) = \eta(s) / \sum_{s'} \eta(s')$, con $\eta(s)$ il numero atteso di passi temporali trascorsi in $s$ in un episodio. VE si calcola sui pesi alla fine di ogni blocco di 100 episodi; «a fine addestramento» vuol dire dopo il 2000° episodio.

- **30 semi** indipendenti, dichiarati nei criteri.

## Vincoli operativi

- Solo Python 3 e la sua libreria standard. **Nessuna dipendenza esterna, `numpy` compreso: non è installato su questa macchina.**
- Il giro completo deve stare **sotto i 60 secondi** su un portatile.
- Ogni numero riportato deve essere ricalcolabile dai log grezzi salvati, **pesi finali per seme e per algoritmo compresi**.

## Cosa si vuole in uscita

Un criterio **falsificabile** sull'affermazione, misurato su tutti e 30 i semi, con la dispersione dichiarata e non solo la media. Se l'analisi teorica e la misura non concordano, è un risultato da riportare, non da nascondere.
