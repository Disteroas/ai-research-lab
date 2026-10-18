# Uno o tre vicini con etichette rumorose

*Questo file si consegna al laboratorio così com'è, dal titolo in giù. Non aggiungere nulla.*

---

## Problema

Il classificatore a vicini più prossimi assegna a un punto l'etichetta dei punti di addestramento più vicini. Con un solo vicino (1-NN) copia l'etichetta di quell'unico esempio, anche quando l'esempio è etichettato male; con tre vicini (3-NN) decide a maggioranza, e un'etichetta sbagliata isolata viene messa in minoranza dalle due vicine. Per questo, quando una parte delle etichette è sbagliata, tre vicini sono la scelta abituale al posto di uno.

Affermazione da mettere alla prova: **sul problema qui sotto, il classificatore 3-NN ha errore di test atteso più basso del classificatore 1-NN.**

## Ambiente su cui lavorare

Fissato, non è oggetto di scelta.

- Punti $x = (x_1, x_2)$ nel quadrato unitario $[0, 1]^2$, estratti in modo uniforme.
- **Classe vera**: $c(x) = 1$ se $x_2 > 0{,}5 + 0{,}3\,\sin(6\pi x_1)$, altrimenti $c(x) = 0$. Il confine fra le due classi è una sinusoide con tre periodi interi sul lato del quadrato.
- **Etichetta osservata**: la classe vera con probabilità $0{,}95$, l'altra classe con probabilità $0{,}05$, indipendentemente da punto a punto. Vale per i punti di addestramento **e** per quelli di test.
- **Dati di un seme**: **50** punti di addestramento, poi **1000** punti di test. Il seme $s$ inizializza `random.Random(s)`; con quel generatore si estraggono, nell'ordine, i 50 punti di addestramento e poi i 1000 di test, e ogni punto usa tre chiamate a `.random()` in quest'ordine: $x_1$, poi $x_2$, poi $u$. L'etichetta osservata è $c(x)$ se $u \ge 0{,}05$, è $1 - c(x)$ se $u < 0{,}05$.
- **Distanza euclidea** fra i punti.
- **1-NN**: predice l'etichetta osservata del punto di addestramento più vicino.
- **3-NN**: predice l'etichetta osservata più frequente fra i tre punti di addestramento più vicini.
- Se due punti di addestramento stanno alla stessa distanza, precede quello estratto per primo.
- **Errore di test** di un classificatore su un seme: frazione dei 1000 punti di test la cui etichetta predetta è diversa dalla loro etichetta osservata. «Atteso» si intende rispetto all'estrazione dei dati.
- I due classificatori usano, a ogni seme, gli **stessi** 50 punti di addestramento e gli **stessi** 1000 punti di test.

I due classificatori si implementano **esattamente come specificati**: il numero di vicini è l'oggetto del confronto, non un iperparametro da aggiustare.

- **Semi: 1, 2, …, 30.** Il campione è fissato: **30 semi, non di più.** Non si aggiungono semi, non si allargano gli insiemi di addestramento o di test, e non si generano altri dati su cui far girare i due classificatori, nemmeno per una previsione teorica o un controllo. Rieseguire gli stessi 30 semi è ammesso.

## Vincoli operativi

- Solo Python 3 e la sua libreria standard. Nessuna dipendenza esterna, `numpy` compreso; nessun download, nessuna GPU.
- Il giro completo deve stare **sotto i 60 secondi** su un portatile.
- Ogni numero riportato deve essere ricalcolabile dai log grezzi salvati, **errori di test per seme e per classificatore compresi**.

## Cosa si vuole in uscita

Un criterio **falsificabile** sull'affermazione, misurato su tutti e 30 i semi, con la dispersione dichiarata e non solo la media. Se l'analisi teorica e la misura non concordano, è un risultato da riportare, non da nascondere.
