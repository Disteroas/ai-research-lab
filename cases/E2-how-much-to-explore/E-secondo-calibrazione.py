#!/usr/bin/env python3
"""Calibrazione del caso E'' (quanto esplorare con epsilon-greedy).

Verifica, contro casi/E-secondo-quanto-esplorare.md, i numeri di verita/E-secondo.md:

  A. struttura in forma chiusa (programmazione dinamica esatta, nessuna simulazione):
     A1. Q* per value iteration: la politica greedy e' il cammino minimo (10 passi)
         ed e' LA STESSA per le due varianti (Q* non dipende da epsilon);
     A2. tetto assoluto c_max(eps) = max su QUALUNQUE politica (anche non stazionaria)
         di P(ingresso nell'uscita entro 13 passi) eseguendo epsilon-greedy:
         c_max(0,3) < 0,9 (la variante 1 non puo' soddisfare il criterio del compito),
         c(0,05) >= 0,9 sull'intera classe dei cammini minimi (la variante 2 puo');
     A3. probabilita' esatta che una finestra da 50 episodi arrivi a 45 successi
         con p = c_max(0,3): deve essere trascurabile;
     A4. baseline della politica uniforme (entro 13 e entro 40 passi);
  B. simulazione del protocollo del caso su 60 semi per variante:
     B1. variante 1 (eps = 0,3) rotta su TUTTI i semi: regime finale 901-1000 < 0,9
         e massimo per finestra < 0,9 (nessun transitorio che tocchi il criterio);
     B2. variante 1 "sembra viva": regime sostenuto ben sopra la baseline, curva che
         sale, arrivo all'uscita entro 40 passi ~1, politica greedy finale = cammino minimo;
     B3. variante 2 (eps = 0,05) raggiunge e sostiene il criterio del compito su tutti
         i semi, con risoluzione (episodi al criterio non al pavimento, IQR > 0);
     B4. condizioni di invalidazione I1-I4 della verita' NON scattate;
     B5. tempo: 30 semi x 2 varianti sotto i 60 s.

Ultima riga stampata: CALIBRAZIONE OK oppure CALIBRAZIONE NON OK + cosa correggere.
Interprete: /Library/Frameworks/Python.framework/Versions/3.10/bin/python3 (numpy).
"""

import math
import time
import numpy as np

# --- Ambiente del caso (deve coincidere con casi/E-secondo-quanto-esplorare.md) ---
LARGH, ALT = 7, 5                 # x in 0..6, y in 0..4
START = (0, 0)
USCITA = (6, 4)
COSTO = -1.0                      # ogni passo, compreso quello che entra nell'uscita
SCADENZA = 13                     # successo = ingresso nell'uscita al passo <= 13
T_MAX = 40                        # troncamento (non terminale: si fa bootstrap)
EPISODI = 1000
FINESTRA = 50
SOGLIA_SUCC = 45                  # criterio del compito: >= 45 successi su 50
THETA = SOGLIA_SUCC / FINESTRA    # 0,9
ALPHA = 0.1
GAMMA = 0.9
Q0 = 0.0
EPS_V1 = 0.3                      # variante 1 (soggetto dell'affermazione)
EPS_V2 = 0.05                     # variante 2
N_SEMI = 60
SEED_MASTER = 20261017

# soglie delle condizioni di invalidazione (verita/E-secondo.md)
I1_MAX_MED_FIN_V1 = 0.65          # mediana ultima finestra V1 >= 0,65 -> invalida
I2_MIN_MED_FIN_V1 = 0.25          # mediana ultima finestra V1 <  0,25 -> invalida
I3_MAX_WIN_V1 = THETA             # una finestra qualunque di V1 >= 0,9 -> invalida
I4_MIN_MED_FIN_V2 = THETA         # mediana ultima finestra V2 < 0,9 -> invalida
I4_MAX_MED_W1_V2 = THETA          # mediana prima finestra V2 >= 0,9 -> invalida (pavimento)

# azioni: 0 nord (y+1), 1 sud (y-1), 2 est (x+1), 3 ovest (x-1); fuori griglia = fermo
DX = np.array([0, 0, 1, -1])
DY = np.array([1, -1, 0, 0])
N_ST = LARGH * ALT
S_START = START[1] * LARGH + START[0]
S_USCITA = USCITA[1] * LARGH + USCITA[0]
STATI = np.arange(N_ST)


def passo(s, a):
    x, y = s % LARGH, s // LARGH
    x2 = np.clip(x + DX[a], 0, LARGH - 1)
    y2 = np.clip(y + DY[a], 0, ALT - 1)
    return y2 * LARGH + x2


NEXT = np.stack([passo(STATI, np.full(N_ST, a)) for a in range(4)], axis=1)  # (N_ST, 4)
DIST = (USCITA[0] - STATI % LARGH) + (USCITA[1] - STATI // LARGH)              # Manhattan


# ---------------------------------------------------------------- A. forma chiusa
def value_iteration():
    Q = np.zeros((N_ST, 4))
    for _ in range(10000):
        V = Q.max(axis=1)
        V[S_USCITA] = 0.0
        Qn = COSTO + GAMMA * np.where(NEXT == S_USCITA, 0.0, V[NEXT])
        Qn[S_USCITA] = 0.0
        if np.abs(Qn - Q).max() < 1e-13:
            return Qn
        Q = Qn
    return Q


def p_entro(k, eps, scelta):
    """P(ingresso nell'uscita entro k passi) eseguendo eps-greedy sopra una selezione
    dell'azione greedy fatta, passo per passo, con 'scelta' (max o min) fra le azioni
    ammesse. Programmazione dinamica esatta a orizzonte finito."""
    ammesse, op = scelta
    ammesse = ammesse.copy()
    ammesse[S_USCITA] = True          # riga dell'uscita: irrilevante (assorbente), evita NaN
    V = np.zeros(N_ST)
    V[S_USCITA] = 1.0
    for _ in range(k):
        Vn_next = V[NEXT]                                  # (N_ST, 4)
        greedy_val = op(np.where(ammesse, Vn_next, np.nan), axis=1)
        Vn = (1 - eps) * greedy_val + eps / 4 * Vn_next.sum(axis=1)
        Vn[S_USCITA] = 1.0
        V = Vn
    return V[S_START]


def coda_binomiale(n, kmin, p):
    return sum(math.comb(n, k) * p**k * (1 - p)**(n - k) for k in range(kmin, n + 1))


# ---------------------------------------------------------------- B. simulazione
def simula(eps, n_semi, seed):
    """Q-learning tabellare vettorizzato sui semi. Ritorna (passo d'arrivo per episodio
    (EPISODI, n_semi), con T_MAX+1 se troncato; Q finale (n_semi, N_ST, 4); lunghezza del
    rollout greedy deterministico a fine di ogni episodio (EPISODI, n_semi), informativa)."""
    rng = np.random.default_rng(seed)
    Q = np.full((n_semi, N_ST, 4), Q0)
    arrivo = np.full((EPISODI, n_semi), T_MAX + 1)
    roll = np.full((EPISODI, n_semi), T_MAX + 1)
    idx = np.arange(n_semi)
    for ep in range(EPISODI):
        s = np.full(n_semi, S_START)
        vivo = np.ones(n_semi, dtype=bool)
        for t in range(T_MAX):
            if not vivo.any():
                break
            greedy = np.argmax(Q[idx, s] + rng.random((n_semi, 4)) * 1e-12, axis=1)
            esplora = rng.random(n_semi) < eps
            a = np.where(esplora, rng.integers(0, 4, n_semi), greedy)
            s2 = NEXT[s, a]
            term = s2 == S_USCITA
            target = np.where(term, COSTO, COSTO + GAMMA * Q[idx, s2].max(axis=1))
            u = vivo
            Q[idx[u], s[u], a[u]] += ALPHA * (target[u] - Q[idx[u], s[u], a[u]])
            arrivo[ep, vivo & term] = t + 1
            s = np.where(vivo & ~term, s2, s)
            vivo = vivo & ~term
        g = np.full(n_semi, S_START)                       # rollout greedy, pari merito: indice minimo
        fuori = np.ones(n_semi, dtype=bool)
        for t in range(T_MAX):
            g = NEXT[g, np.argmax(Q[idx, g], axis=1)]
            arrivato = fuori & (g == S_USCITA)
            roll[ep, arrivato] = t + 1
            fuori &= ~arrivato
    return arrivo, Q, roll


def finestre(x):
    n = EPISODI // FINESTRA
    return x[: n * FINESTRA].reshape(n, FINESTRA, -1).mean(axis=1)   # (20, semi)


def primo_passaggio(succ):
    """Primo episodio e (50..1000) con >= SOGLIA_SUCC successi negli episodi e-49..e;
    EPISODI+1 se non esiste (censura)."""
    cs = np.vstack([np.zeros((1, succ.shape[1])), np.cumsum(succ, axis=0)])
    scorr = cs[FINESTRA:] - cs[:-FINESTRA]
    out = []
    for j in range(succ.shape[1]):
        w = np.flatnonzero(scorr[:, j] >= SOGLIA_SUCC)
        out.append(w[0] + FINESTRA if len(w) else EPISODI + 1)
    return np.array(out)


def rollout_greedy(Q):
    """Lunghezza del rollout greedy deterministico (pari merito: indice minimo) da START,
    per seme; T_MAX+1 se non arriva."""
    out = []
    for q in Q:
        s, L = S_START, T_MAX + 1
        for t in range(T_MAX):
            s = NEXT[s, int(np.argmax(q[s]))]
            if s == S_USCITA:
                L = t + 1
                break
        out.append(L)
    return np.array(out)


def fmt(v):
    return f"{v:.3f}"


def main():
    problemi = []
    print(f"Griglia {LARGH}x{ALT}, start {START}, uscita {USCITA}, scadenza {SCADENZA} passi, "
          f"troncamento {T_MAX}, criterio {SOGLIA_SUCC}/{FINESTRA}, "
          f"alpha {ALPHA}, gamma {GAMMA}, Q0 {Q0}, eps {EPS_V1} / {EPS_V2}, {N_SEMI} semi.")

    # ---- A1: Q* e cammino minimo
    Qs = value_iteration()
    V = Qs.max(axis=1)
    teoria = -(1 - GAMMA ** DIST) / (1 - GAMMA)
    ok_v = np.allclose(V[STATI != S_USCITA], teoria[STATI != S_USCITA], atol=1e-10)
    minime = (DIST[NEXT] == DIST[:, None] - 1)                     # azioni che accorciano
    greedy_set = np.isclose(Qs, Qs.max(axis=1, keepdims=True), atol=1e-12)
    ok_set = bool(np.all(greedy_set[STATI != S_USCITA] == minime[STATI != S_USCITA]))
    print(f"A1  V*(start) = {V[S_START]:.10f} (teoria -(1-g^10)/(1-g) = {teoria[S_START]:.10f}); "
          f"azioni greedy di Q* = azioni di cammino minimo su tutte le celle: {ok_set}")
    if not (ok_v and ok_set):
        problemi.append("A1: Q* non coincide con la forma chiusa del cammino minimo")

    tutte = np.ones((N_ST, 4), dtype=bool)
    cmax1 = p_entro(SCADENZA, EPS_V1, (tutte, np.nanmax))
    cmax2 = p_entro(SCADENZA, EPS_V2, (tutte, np.nanmax))
    cmin_cls1 = p_entro(SCADENZA, EPS_V1, (minime, np.nanmin))
    cmax_cls1 = p_entro(SCADENZA, EPS_V1, (minime, np.nanmax))
    cmin_cls2 = p_entro(SCADENZA, EPS_V2, (minime, np.nanmin))
    cmax_cls2 = p_entro(SCADENZA, EPS_V2, (minime, np.nanmax))
    print(f"A2  tetto assoluto (qualunque politica) entro {SCADENZA} passi: "
          f"eps {EPS_V1} -> {cmax1:.4f};  eps {EPS_V2} -> {cmax2:.4f}")
    print(f"    classe dei cammini minimi (selezione min..max): "
          f"eps {EPS_V1} -> [{cmin_cls1:.4f}, {cmax_cls1:.4f}];  "
          f"eps {EPS_V2} -> [{cmin_cls2:.4f}, {cmax_cls2:.4f}]")
    if not cmax1 < THETA:
        problemi.append(f"A2: tetto assoluto della variante 1 {cmax1:.4f} >= {THETA}: non e' rotta")
    if not cmin_cls2 >= THETA:
        problemi.append(f"A2: la variante 2 su qualche cammino minimo sta sotto {THETA} ({cmin_cls2:.4f})")

    p_fin = coda_binomiale(FINESTRA, SOGLIA_SUCC, cmax1)
    p_fin2 = coda_binomiale(FINESTRA, SOGLIA_SUCC, cmin_cls2)
    print(f"A3  P(finestra >= {SOGLIA_SUCC}/{FINESTRA}) con p = tetto assoluto di V1 ({cmax1:.4f}): "
          f"{p_fin:.3e};  con p = minimo di classe di V2 ({cmin_cls2:.4f}): {p_fin2:.4f}")
    if p_fin > 1e-6:
        problemi.append(f"A3: una finestra di V1 puo' toccare il criterio per caso (p = {p_fin:.2e})")

    base13 = p_entro(SCADENZA, 1.0, (tutte, np.nanmax))
    base40 = p_entro(T_MAX, 1.0, (tutte, np.nanmax))
    print(f"A4  baseline uniforme: entro {SCADENZA} passi {base13:.4f}; entro {T_MAX} passi {base40:.4f}")

    # ---- B: simulazione
    t0 = time.time()
    arr1, Q1, roll1 = simula(EPS_V1, N_SEMI, SEED_MASTER)
    arr2, Q2, roll2 = simula(EPS_V2, N_SEMI, SEED_MASTER + 1)
    durata = time.time() - t0
    stima30 = durata * 30 / N_SEMI

    s1, s2 = (arr1 <= SCADENZA).astype(float), (arr2 <= SCADENZA).astype(float)
    d1, d2 = (arr1 <= T_MAX).astype(float), (arr2 <= T_MAX).astype(float)
    w1, w2 = finestre(s1), finestre(s2)
    fin1, fin2 = s1[900:].mean(axis=0), s2[900:].mean(axis=0)
    max1 = w1.max(axis=0)
    T1, T2 = primo_passaggio(s1), primo_passaggio(s2)
    Tw1, Tw2 = primo_passaggio(d1), primo_passaggio(d2)
    r1, r2 = rollout_greedy(Q1), rollout_greedy(Q2)

    print("B   variante 1 (eps 0,3), successo per finestra, mediana su semi:",
          " ".join(f"{v:.2f}" for v in np.median(w1, axis=1)))
    print("    variante 2 (eps 0,05), successo per finestra, mediana su semi:",
          " ".join(f"{v:.2f}" for v in np.median(w2, axis=1)))
    print(f"B1  V1 regime finale 901-1000: mediana {fmt(np.median(fin1))}, min {fin1.min():.2f}, "
          f"max {fin1.max():.2f}; semi con regime finale >= {THETA}: {(fin1 >= THETA).sum()}/{N_SEMI}")
    print(f"    V1 ultima finestra: mediana {fmt(np.median(w1[-1]))}, max {w1[-1].max():.2f}")
    print(f"    V1 massimo per finestra: mediana {fmt(np.median(max1))}, max su tutti i semi "
          f"{max1.max():.2f}; semi con una finestra >= {THETA}: {(max1 >= THETA).sum()}/{N_SEMI}")
    print(f"    V1 episodi al criterio (finestra scorrevole): censurati {(T1 > EPISODI).sum()}/{N_SEMI}")
    if (fin1 >= THETA).any() or (max1 >= THETA).any() or (T1 <= EPISODI).any():
        problemi.append("B1: la variante 1 tocca il criterio del compito su qualche seme")

    print(f"B2  V1 arrivo entro {T_MAX} passi negli episodi 901-1000: mediana "
          f"{fmt(np.median(d1[900:].mean(axis=0)))}; prima finestra mediana "
          f"{fmt(np.median(w1[0]))}; rollout greedy finale = 10 passi su "
          f"{(r1 == 10).sum()}/{N_SEMI} semi (V2: {(r2 == 10).sum()}/{N_SEMI})")
    print(f"    rapporto regime finale V1 / baseline entro {SCADENZA}: "
          f"{np.median(fin1) / base13:.0f}x")
    if not (np.median(fin1) > 10 * base13 and (r1 == 10).all() and (r2 == 10).all()
            and np.median(d1[900:].mean(axis=0)) >= 0.95):
        problemi.append("B2: la variante 1 non 'sembra viva' come previsto (o greedy non minimo)")

    q1, med, q3 = np.percentile(T2, [25, 50, 75])
    print(f"B3  V2 regime finale 901-1000: mediana {fmt(np.median(fin2))}, min {fin2.min():.2f}; "
          f"semi con regime finale >= {THETA}: {(fin2 >= THETA).sum()}/{N_SEMI}")
    print(f"    V2 episodi al criterio: mediana {med:.1f}, Q1 {q1:.1f}, Q3 {q3:.1f}, "
          f"min {T2.min()}, max {T2.max()}, censurati {(T2 > EPISODI).sum()}/{N_SEMI}")
    if not ((fin2 >= THETA).all() and (T2 <= EPISODI).all() and q3 - q1 > 0 and med > FINESTRA):
        problemi.append("B3: la variante 2 non raggiunge/sostiene il criterio su tutti i semi, "
                        "o la sua metrica non ha risoluzione")

    print(f"    [informativo] episodi al criterio con successo 'debole' (arrivo entro {T_MAX}): "
          f"V1 mediana {np.median(Tw1):.1f} (cens {(Tw1 > EPISODI).sum()}), "
          f"V2 mediana {np.median(Tw2):.1f} (cens {(Tw2 > EPISODI).sum()})")

    def da_quando_minimo(roll):
        """Primo episodio da cui il rollout greedy resta di 10 passi fino alla fine."""
        ok = roll == 10
        out = []
        for j in range(roll.shape[1]):
            cattivi = np.flatnonzero(~ok[:, j])
            out.append(1 if len(cattivi) == 0 else (cattivi[-1] + 2 if cattivi[-1] < EPISODI - 1
                                                     else EPISODI + 1))
        return np.array(out)
    G1, G2 = da_quando_minimo(roll1), da_quando_minimo(roll2)
    print(f"    [informativo] episodio da cui la politica greedy resta il cammino minimo: "
          f"V1 mediana {np.median(G1):.1f} (Q1 {np.percentile(G1, 25):.1f}, Q3 "
          f"{np.percentile(G1, 75):.1f}), V2 mediana {np.median(G2):.1f} (Q1 "
          f"{np.percentile(G2, 25):.1f}, Q3 {np.percentile(G2, 75):.1f}); "
          f"semi con V1 prima di V2 (stesso indice di seme): {(G1 < G2).sum()}/{N_SEMI}")

    # ---- B4: invalidazione (sulla sola grandezza 'successo per finestra da 50')
    i1 = np.median(w1[-1]) >= I1_MAX_MED_FIN_V1
    i2 = np.median(w1[-1]) < I2_MIN_MED_FIN_V1
    i3 = (w1 >= I3_MAX_WIN_V1).any()
    i4 = np.median(w2[-1]) < I4_MIN_MED_FIN_V2 or np.median(w2[0]) >= I4_MAX_MED_W1_V2
    print(f"B4  invalidazione: I1 {i1}  I2 {i2}  I3 {i3}  I4 {i4}  "
          f"(V2 ultima finestra mediana {fmt(np.median(w2[-1]))}, prima finestra mediana "
          f"{fmt(np.median(w2[0]))})")
    if i1 or i2 or i3 or i4:
        problemi.append("B4: una condizione di invalidazione scatta sulla calibrazione")

    print(f"B5  durata {durata:.1f} s ({N_SEMI} semi x 2); stima 30 semi x 2: {stima30:.1f} s")
    if stima30 >= 60:
        problemi.append(f"B5: troppo lento ({stima30:.0f} s)")

    print()
    if not problemi:
        print("CALIBRAZIONE OK")
    else:
        print("CALIBRAZIONE NON OK — da correggere: " + " | ".join(problemi))


if __name__ == "__main__":
    main()
