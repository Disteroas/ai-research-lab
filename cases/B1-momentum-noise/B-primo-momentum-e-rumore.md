# Il momentum e il rumore del gradiente

*Questo file si consegna al laboratorio così com'è, dal titolo in giù. Non aggiungere nulla.*

---

## Problema

Nella discesa del gradiente stocastico ogni passo usa una stima rumorosa del gradiente, e il rumore impedisce all'iterata di fermarsi sul minimo: a regime l'iterata fluttua attorno ad esso. Un'idea diffusa è che il **momentum** attenui questo effetto: il termine di momentum accumula i gradienti dei passi precedenti, le componenti rumorose di passi diversi tendono a compensarsi, e l'iterata dovrebbe quindi assestarsi più vicino al minimo.

Affermazione da mettere alla prova: **a parità di passo α, aggiungere il momentum con β = 0,9 riduce l'errore quadratico a regime della discesa del gradiente stocastico, sul problema qui sotto.**

## Ambiente su cui lavorare

Fissato, non è oggetto di scelta.

- Funzione obiettivo scalare **f(x) = ½·λ·x²**, con **λ = 1**; minimo in x\* = 0.
- Oracolo stocastico del gradiente: al passo t restituisce **g_t = λ·x_t + σ·ξ_t**, con **σ = 1** e ξ_t normale standard, indipendente fra passi.
- Regola di aggiornamento, **la stessa per le due varianti**:

  ```
  v_{t+1} = β·v_t + g_t
  x_{t+1} = x_t − α·v_{t+1}
  ```

  con **x_0 = 10**, **v_0 = 0**, **α = 0,01**.
- **Variante 1: senza momentum**, β = 0 (la regola si riduce a x_{t+1} = x_t − α·g_t).
- **Variante 2: con momentum**, **β = 0,9**.
- **T = 20 000** passi per run (da x_0 a x_20000).
- **Errore a regime** di un run: media di x_t² per t = 10 001, …, 20 000 (diecimila valori).
- **Semi: 1, 2, …, 30.** Il seme s inizializza `random.Random(s)`, che genera ξ_0, ξ_1, … con `.gauss(0, 1)`, uno per passo, in ordine. Le due varianti usano lo **stesso** seme, cioè la stessa sequenza di rumore.

Le due varianti si implementano **esattamente come specificate**: stessa regola, stesso α, stessa forma dell'aggiornamento; il momentum è l'oggetto del confronto, non un iperparametro da aggiustare.

## Vincoli operativi

- Solo Python 3 con la **libreria standard**. Nessuna dipendenza esterna, nessun download, nessuna GPU.
- Il giro completo deve stare **sotto i 60 secondi** su un portatile.
- Ogni numero riportato deve essere ricalcolabile dai log grezzi salvati.
- Se usi sia la simulazione sia un'analisi teorica e le due vie non concordano, è un risultato da riportare, non da nascondere.

## Cosa si vuole in uscita

Un criterio **falsificabile** sull'affermazione in cima, misurato su tutti e 30 i semi per entrambe le varianti, con la dispersione dichiarata e non solo la media.
