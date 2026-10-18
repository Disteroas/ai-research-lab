# Quanto esplorare con ε-greedy

*Questo file si consegna al laboratorio così com'è, dal titolo in giù. Non aggiungere nulla.*

---

## Problema

Con l'esplorazione ε-greedy l'agente, a ogni passo, sceglie con probabilità ε un'azione a caso invece di quella che ritiene migliore. Un ε piccolo sfrutta presto ciò che ha imparato ma prova poco; un ε grande prova tutto, e i valori di tutte le azioni vengono aggiornati più spesso. Un'idea diffusa: **esplorare di più fa imparare in meno episodi**, perché l'agente scopre prima i percorsi buoni e il valore si propaga più in fretta.

Affermazione da mettere alla prova: **a parità di tutto il resto, Q-learning con ε = 0,3 raggiunge il criterio di successo in meno episodi di Q-learning con ε = 0,05, sull'ambiente qui sotto.**

## Ambiente su cui lavorare

Fissato, non è oggetto di scelta. Una griglia di 7 colonne per 5 righe, celle `(x, y)` con `x ∈ {0, …, 6}` e `y ∈ {0, …, 4}`:

- Stato iniziale di ogni episodio: **(0,0)**. L'**uscita** è la cella **(6,4)**, terminale.
- Azioni: `nord` (y+1), `sud` (y−1), `est` (x+1), `ovest` (x−1), deterministiche, un passo. Una mossa fuori griglia lascia l'agente fermo.
- Ricompensa: **−1 a ogni passo**, compreso quello che entra nell'uscita. Nessun'altra ricompensa.
- Episodio troncato a **40 passi** se non termina prima. Il troncamento non è uno stato terminale: l'aggiornamento dell'ultimo passo usa il valore dello stato raggiunto, come ogni altro.
- **1000 episodi** per run.

**Il compito.**

- **Successo di un episodio** = l'agente entra nell'uscita **entro i primi 13 passi** dell'episodio. Un episodio che arriva all'uscita dal 14° passo in poi, o che viene troncato, è un **insuccesso**.
- Gli episodi sono quelli dell'apprendimento stesso, eseguiti con la politica ε-greedy della variante: non sono previsti episodi di valutazione separati.
- **Criterio di successo**: almeno **45 episodi con successo su 50 consecutivi**. Il successo si riporta per finestre di 50 episodi.

Le due varianti da confrontare, identiche in tutto tranne ε:

- Q-learning tabellare, **α = 0,1**, **γ = 0,9**, **Q iniziale = 0**. ε-greedy con ε costante: con probabilità ε un'azione uniforme fra le quattro (quella greedy compresa), altrimenti la greedy; a parità di valore l'azione si sceglie a caso col RNG del seme.
- **Variante 1: ε = 0,3. Variante 2: ε = 0,05.**

Le due varianti si implementano **esattamente come specificate**: ε è l'oggetto del confronto, non un iperparametro da aggiustare.

- **30 semi** indipendenti, dichiarati nei criteri.

## Vincoli operativi

- Solo Python 3 e `numpy`. Nessuna altra dipendenza, nessun download, nessuna GPU.
- Il giro completo deve stare **sotto i 60 secondi** su un portatile. Se la tua implementazione non ci sta, vettorizza sui semi: non allargare il budget.
- Ogni numero riportato deve essere ricalcolabile dai log grezzi salvati.

## Cosa si vuole in uscita

Un criterio **falsificabile** sul numero di episodi necessari a raggiungere il criterio di successo definito sopra, misurato su tutti e 30 i semi, con la dispersione dichiarata e non solo la media.
