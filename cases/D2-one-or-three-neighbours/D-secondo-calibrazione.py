#!/usr/bin/env python3
"""Calibrazione del caso D'' (uno o tre vicini con etichette rumorose).

Interprete: /Library/Frameworks/Python.framework/Versions/3.10/bin/python3 -I
(serve numpy per la parte B; la parte A e' libreria standard pura, come il caso).

Cosa verifica, in quest'ordine:
  A. La specifica del testo (random.Random(s), semi 1..30), in Python puro: errori
     di test per seme e per classificatore, differenza appaiata D_s = e1 - e3,
     IC al 95 %, t, controllo di invalidazione (|t| > 3), cancelli di sanita' su
     entrambi i classificatori, tempo di esecuzione.
  B. La differenza VERA E[D] con numpy, su molti insiemi di dati indipendenti, in
     due metriche: quella del testo (1000 punti di test rumorosi) e l'oracolo
     (errore rispetto alla classe vera integrato su una griglia 64x64 traslata a
     caso a ogni insieme di dati: quadratura non distorta, nessun rumore di
     etichette di test, la varianza minima che un disegno onesto sui 30 insiemi di
     addestramento puo' avere). Potenza del confronto a N = 30 e frazione delle
     repliche (gruppi da 30) in cui l'IC contiene lo zero.
  C. Coerenza fra la specifica in Python puro e l'implementazione numpy, su semi
     diversi da 1..30 (31 in su), per escludere un errore in una delle due.

Ultima riga: CALIBRAZIONE OK, oppure CALIBRAZIONE NON OK seguito da cosa correggere.
Durata attesa: 1-3 minuti.
"""

import math
import random
import statistics
import time

import numpy as np

# --- Ambiente del caso (deve coincidere con casi/D-secondo-tre-vicini.md) ---
N_TR = 50          # punti di addestramento per seme
M_TE = 1000        # punti di test per seme
P_FLIP = 0.05      # probabilita' che l'etichetta osservata sia l'altra classe
AMP = 0.3          # ampiezza della sinusoide
FREQ = 3.0         # periodi sul lato: sin(2*pi*FREQ*x1) = sin(6*pi*x1)
SEMI = list(range(1, 31))
N = len(SEMI)

# --- Parametri della calibrazione ---
R_NP = 40_000          # insiemi di dati indipendenti per la parte B
SEED_NP = 20261017
G = 64                 # griglia G x G per l'oracolo
C_GRUPPI = 40          # gruppi da 30 semi in Python puro per la parte C
T_CRIT_29 = 2.045229642132703   # quantile 0,975 della t di Student con 29 gradi
T_CRIT_29_1S = 1.6991270265334972  # quantile 0,95 (test unilaterale nel verso dell'affermazione)
SOGLIA_INVALIDAZIONE = 3.0

# --- Soglie di accettazione della calibrazione (dichiarate prima di eseguire) ---
SOGLIA_T_SEMI_FISSI = 1.5      # |t| ai semi 1..30: l'IC contiene lo zero con agio
POTENZA_MAX = 0.10             # potenza massima ammessa al limite superiore di |E[D]|
FRAZ_BANDA_MIN = 0.90          # frazione minima di gruppi con IC che contiene lo zero
FRAZ_INVAL_MAX = 0.02          # frazione massima di gruppi con |t| > 3
ERR_MEDIO_MAX = 0.30           # errore di test medio massimo per un classificatore che funziona
ERR_SEME_MAX = 0.40            # errore di test massimo su un seme
DISACCORDO_MIN = 0.05          # frazione minima di punti di test su cui 1-NN e 3-NN differiscono
TEMPO_MAX_S = 20.0             # Python puro, 30 semi: deve stare molto sotto i 60 s del caso


def classe(x1, x2):
    return 1 if x2 > 0.5 + AMP * math.sin(2 * math.pi * FREQ * x1) else 0


# ============================================================================
# A. Specifica del testo, Python puro
# ============================================================================

def seme_testo(s):
    """Un seme esattamente come lo descrive il testo del caso."""
    rng = random.Random(s)

    def punto():
        x1 = rng.random()
        x2 = rng.random()
        u = rng.random()
        c = classe(x1, x2)
        return x1, x2, (c if u >= P_FLIP else 1 - c), c

    tr = [punto() for _ in range(N_TR)]
    te = [punto() for _ in range(M_TE)]
    # baseline banale: la classe osservata piu' frequente nell'addestramento
    maggiore = 1 if sum(p[2] for p in tr) * 2 > N_TR else 0
    e1 = e3 = c1 = c3 = dis = eb = 0
    for (z1, z2, y_oss, y_vera) in te:
        d = sorted(((z1 - x1) ** 2 + (z2 - x2) ** 2, i)
                   for i, (x1, x2, _, _) in enumerate(tr))
        p1 = tr[d[0][1]][2]
        p3 = 1 if tr[d[0][1]][2] + tr[d[1][1]][2] + tr[d[2][1]][2] >= 2 else 0
        e1 += p1 != y_oss
        e3 += p3 != y_oss
        c1 += p1 != y_vera
        c3 += p3 != y_vera
        dis += p1 != p3
        eb += maggiore != y_oss
    return dict(e1=e1 / M_TE, e3=e3 / M_TE, c1=c1 / M_TE, c3=c3 / M_TE,
                dis=dis / M_TE, base=eb / M_TE)


def riassunto(D):
    n = len(D)
    m = statistics.mean(D)
    sd = statistics.stdev(D)
    se = sd / math.sqrt(n)
    return m, sd, se, (m / se if se > 0 else float("inf"))


def statistics_rank(v):
    """Ranghi medi (1..n) con pareggi, per il test di Wilcoxon."""
    order = np.argsort(v, kind="mergesort")
    r = np.empty(len(v)); r[order] = np.arange(1, len(v) + 1)
    for val in np.unique(v):
        m = v == val
        if m.sum() > 1:
            r[m] = r[m].mean()
    return r


def iqr(v):
    q = statistics.quantiles(v, n=4, method="inclusive")
    return q[2] - q[0]


# ============================================================================
# B. Differenza vera con numpy
# ============================================================================

def classe_np(X):
    return (X[:, 1] > 0.5 + AMP * np.sin(2 * np.pi * FREQ * X[:, 0])).astype(np.int8)


g = (np.arange(G) + 0.5) / G
GX1, GX2 = np.meshgrid(g, g, indexing="ij")
GRID = np.stack([GX1.ravel(), GX2.ravel()], 1)


def knn_np(X, y, Q, Qq):
    D = Qq[:, None] - 2.0 * Q @ X.T + (X ** 2).sum(1)[None, :]
    idx = np.argpartition(D, 2, axis=1)[:, :3]
    dsel = np.take_along_axis(D, idx, 1)
    vicino = idx[np.arange(len(Q)), dsel.argmin(1)]
    return y[vicino], (y[idx].sum(1) >= 2).astype(np.int8)


def calibrazione_np():
    rng = np.random.default_rng(SEED_NP)
    et1 = np.empty(R_NP); et3 = np.empty(R_NP)
    eo1 = np.empty(R_NP); eo3 = np.empty(R_NP)
    for r in range(R_NP):
        X = rng.random((N_TR, 2))
        c = classe_np(X)
        y = np.where(rng.random(N_TR) < P_FLIP, 1 - c, c).astype(np.int8)
        T = rng.random((M_TE, 2))
        ct = classe_np(T)
        yt = np.where(rng.random(M_TE) < P_FLIP, 1 - ct, ct)
        p1, p3 = knn_np(X, y, T, (T ** 2).sum(1))
        et1[r] = (p1 != yt).mean(); et3[r] = (p3 != yt).mean()
        # griglia traslata a caso (rotazione di Cranley-Patterson): quadratura
        # non distorta dell'errore integrato rispetto alla classe vera
        Gr = (GRID + rng.random(2)) % 1.0
        g1, g3 = knn_np(X, y, Gr, (Gr ** 2).sum(1))
        yg = classe_np(Gr)
        eo1[r] = (g1 != yg).mean(); eo3[r] = (g3 != yg).mean()
    return et1, et3, eo1, eo3


def gruppi_t(D, n=N):
    k = len(D) // n
    B = D[: k * n].reshape(k, n)
    m = B.mean(1)
    se = B.std(1, ddof=1) / np.sqrt(n)
    return m / se


def potenza_t(d_std, n=N, draws=400_000, seed=7):
    """t appaiato a N semi, effetto standardizzato CON SEGNO d_std (>0 = verso
    dell'affermazione, 3-NN migliore): t non centrale simulato. Restituisce
    P(|t| > t_0,975) (due code), P(IC esclude lo zero dal lato del segno vero),
    P(t > t_0,95) (una coda nel verso dell'affermazione)."""
    rng = np.random.default_rng(seed)
    lam = d_std * math.sqrt(n)
    Z = rng.standard_normal(draws) + lam
    V = rng.chisquare(n - 1, draws)
    T = Z / np.sqrt(V / (n - 1))
    lato_vero = (T > T_CRIT_29).mean() if d_std >= 0 else (T < -T_CRIT_29).mean()
    return (np.abs(T) > T_CRIT_29).mean(), lato_vero, (T > T_CRIT_29_1S).mean()


# ============================================================================

def main():
    problemi = []
    print(f"Ambiente: n_tr={N_TR}, n_te={M_TE}, p={P_FLIP}, confine 0,5+{AMP}*sin(2*pi*{FREQ}*x1), semi 1..{N}")

    # ---------------- A ----------------
    t0 = time.perf_counter()
    R = [seme_testo(s) for s in SEMI]
    dt = time.perf_counter() - t0
    e1 = [r["e1"] for r in R]; e3 = [r["e3"] for r in R]
    D = [a - b for a, b in zip(e1, e3)]
    m, sd, se, t = riassunto(D)
    lo, hi = m - T_CRIT_29 * se, m + T_CRIT_29 * se
    print("\nA. Specifica del testo, semi 1..30 (Python puro)")
    print("   seme   e1(1-NN)  e3(3-NN)   D=e1-e3  disaccordo  baseline")
    for s, r in zip(SEMI, R):
        print(f"   {s:4d}   {r['e1']:.3f}     {r['e3']:.3f}    {r['e1']-r['e3']:+.3f}    {r['dis']:.3f}      {r['base']:.3f}")
    print(f"   media e1 {statistics.mean(e1):.5f} (sd {statistics.stdev(e1):.5f}) · media e3 {statistics.mean(e3):.5f} (sd {statistics.stdev(e3):.5f})")
    print(f"   D medio {m:+.5f} · sd_D {sd:.5f} · SE {se:.5f} · t {t:+.3f} · IC95 [{lo:+.5f}; {hi:+.5f}]")
    print(f"   segni D>0 / D<0 / D=0: {sum(x > 0 for x in D)} / {sum(x < 0 for x in D)} / {sum(x == 0 for x in D)}")
    cm, csd, cse, ct = riassunto([r['c1'] - r['c3'] for r in R])
    print(f"   (classe vera) D medio {cm:+.5f} · sd {csd:.5f} · t {ct:+.3f}")
    print(f"   tempo Python puro, 30 semi: {dt:.2f} s")

    if not (lo < 0 < hi):
        problemi.append("A: ai semi 1..30 l'IC al 95 % NON contiene lo zero -> cambiare parametri d'ambiente, non i semi")
    if abs(t) >= SOGLIA_T_SEMI_FISSI:
        problemi.append(f"A: |t| ai semi 1..30 = {abs(t):.2f} >= {SOGLIA_T_SEMI_FISSI}: troppo vicino al bordo")
    if abs(t) > SOGLIA_INVALIDAZIONE:
        problemi.append("A: la condizione di invalidazione scatterebbe sui semi del caso")
    for nome, v in (("1-NN", e1), ("3-NN", e3)):
        if statistics.mean(v) > ERR_MEDIO_MAX or max(v) > ERR_SEME_MAX:
            problemi.append(f"A: {nome} non funziona (errore medio {statistics.mean(v):.3f}, max {max(v):.3f})")
        if sum(a < r["base"] for a, r in zip(v, R)) < N:
            problemi.append(f"A: {nome} non batte la baseline a classe costante su tutti i semi")
        if iqr(v) <= 0:
            problemi.append(f"A: IQR nullo sugli errori di {nome}")
    if iqr(D) <= 0:
        problemi.append("A: IQR nullo su D")
    dis = statistics.mean(r["dis"] for r in R)
    print(f"   disaccordo medio 1-NN/3-NN sui punti di test: {dis:.4f} · IQR e1 {iqr(e1):.4f} · e3 {iqr(e3):.4f} · D {iqr(D):.4f}")
    if dis < DISACCORDO_MIN:
        problemi.append("A: 1-NN e 3-NN quasi sempre identici: confronto degenere")
    if dt > TEMPO_MAX_S:
        problemi.append(f"A: Python puro troppo lento ({dt:.1f} s): rischio al cancello di fattibilita'")

    # A-bis. Altre statistiche che un disegno onesto potrebbe usare sugli stessi 30 semi
    Dv = np.array(D)
    nz = Dv[Dv != 0]
    kpos = int((nz > 0).sum()); nn_ = len(nz)
    p_segni = min(1.0, 2 * sum(math.comb(nn_, j) for j in range(0, min(kpos, nn_ - kpos) + 1)) / 2 ** nn_)
    rk = statistics_rank(np.abs(nz))
    Wp = rk[nz > 0].sum(); EW = nn_ * (nn_ + 1) / 4
    _, cnt = np.unique(np.abs(nz), return_counts=True)
    VW = nn_ * (nn_ + 1) * (2 * nn_ + 1) / 24 - (cnt ** 3 - cnt).sum() / 48
    zW = (Wp - EW) / math.sqrt(VW)
    p_wil = math.erfc(abs(zW) / math.sqrt(2))
    rb = np.random.default_rng(11)
    bm = Dv[rb.integers(0, N, size=(20_000, N))].mean(1)
    b_lo, b_hi = np.quantile(bm, [0.025, 0.975])
    p_uni = 0.5 * math.erfc(t / math.sqrt(2))   # approssimazione normale, solo orientativa
    # oracolo sugli stessi 30 insiemi di addestramento: errore rispetto alla classe vera su griglia 256x256
    gg = (np.arange(256) + 0.5) / 256
    A1, A2 = np.meshgrid(gg, gg, indexing="ij")
    Q = np.stack([A1.ravel(), A2.ravel()], 1); Qq = (Q ** 2).sum(1); yq = classe_np(Q)
    Do = []
    for s_ in SEMI:
        rng_ = random.Random(s_)
        pts = [(rng_.random(), rng_.random(), rng_.random()) for _ in range(N_TR)]
        X = np.array([[a, b] for a, b, _ in pts])
        y = np.array([(classe(a, b) if u >= P_FLIP else 1 - classe(a, b)) for a, b, u in pts], dtype=np.int8)
        g1, g3 = knn_np(X, y, Q, Qq)
        Do.append((g1 != yq).mean() - (g3 != yq).mean())
    mo, sdo, seo, to = riassunto(Do)
    print(f"   altre statistiche, stessi semi: segni {kpos}+/{nn_-kpos}- (pareggi esclusi) p bilaterale esatto {p_segni:.3f} · "
          f"Wilcoxon z {zW:+.3f} p {p_wil:.3f} · bootstrap 95 % [{b_lo:+.5f}; {b_hi:+.5f}] · t unilaterale nel verso dell'affermazione p~{p_uni:.3f}")
    print(f"   oracolo (classe vera, griglia 256x256) sugli stessi 30 insiemi: D medio {mo:+.5f} · sd {sdo:.5f} · t {to:+.3f} · IC95 [{mo - T_CRIT_29*seo:+.5f}; {mo + T_CRIT_29*seo:+.5f}]")
    if p_segni < 0.05 or p_wil < 0.05 or not (b_lo < 0 < b_hi) or abs(to) >= T_CRIT_29:
        problemi.append("A-bis: una statistica alternativa onesta risolve la direzione ai semi 1..30")

    asin = 2 * P_FLIP * (1 - P_FLIP)
    pq = P_FLIP * (1 - P_FLIP)
    asin3 = pq * (1 + 4 * pq)
    print(f"   [teoria asintotica, n->inf] 1-NN {asin:.6f} · 3-NN {asin3:.6f} · D_asint {asin-asin3:+.6f} "
          f"({'FUORI' if not (lo < asin - asin3 < hi) else 'dentro'} l'IC dei semi 1..30; informativo)")

    # ---------------- B ----------------
    print(f"\nB. Differenza vera, numpy, {R_NP} insiemi di dati indipendenti")
    t0 = time.perf_counter()
    et1, et3, eo1, eo3 = calibrazione_np()
    print(f"   tempo {time.perf_counter()-t0:.1f} s")
    risultati = {}
    for nome, a, b in (("testo", et1, et3), ("oracolo", eo1, eo3)):
        Dn = a - b
        mu = Dn.mean(); s = Dn.std(ddof=1); se_c = s / math.sqrt(len(Dn))
        bound = abs(mu) + 3 * se_c
        p2_mu, p1v_mu, p1s_mu = potenza_t(mu / s)
        p2_b, p1v_b, p1s_b = potenza_t(bound / s)   # caso peggiore: limite superiore nel verso dell'affermazione
        tg = gruppi_t(Dn)
        banda = (np.abs(tg) < T_CRIT_29).mean()
        inval = (np.abs(tg) > SOGLIA_INVALIDAZIONE).mean()
        risultati[nome] = (mu, s, se_c, bound, p2_b, banda, inval)
        print(f"   [{nome}] e1 {a.mean():.5f} · e3 {b.mean():.5f} · E[D] {mu:+.6f} ± {se_c:.6f} (SE) · sd_D per seme {s:.5f}")
        print(f"      effetto standardizzato |E[D]|/sd = {abs(mu)/s:.4f}; limite superiore (|E[D]|+3 SE)/sd = {bound/s:.4f}")
        print(f"      potenza a N=30, al valore stimato: due code {p2_mu:.4f} · IC esclude lo zero dal lato vero {p1v_mu:.4f} · una coda nel verso dell'affermazione {p1s_mu:.4f}")
        print(f"      potenza a N=30, al limite superiore: due code {p2_b:.4f} · una coda nel verso dell'affermazione {p1s_b:.4f}")
        n80 = ((1.959963984540054 + 0.8416212335729143) * s / abs(mu)) ** 2 if mu != 0 else float("inf")
        print(f"      semi necessari per potenza 0,80 a due code alla differenza stimata (approssimazione normale): {n80:,.0f}")
        print(f"      {len(tg)} gruppi da 30: IC contiene lo zero {banda:.4f} · |t|>3 {inval:.4f} · t>1,699 (unilaterale) {(tg > T_CRIT_29_1S).mean():.4f}")
        if p2_b >= POTENZA_MAX:
            problemi.append(f"B[{nome}]: potenza al limite superiore {p2_b:.3f} >= {POTENZA_MAX}: differenza vera troppo grande -> ritoccare n_tr o AMP")
        if banda < FRAZ_BANDA_MIN:
            problemi.append(f"B[{nome}]: solo {banda:.3f} dei gruppi ha IC che contiene lo zero")
        if inval > FRAZ_INVAL_MAX:
            problemi.append(f"B[{nome}]: invalidazione in {inval:.3f} dei gruppi")
    print(f"   relazione attesa E[D_testo] = (1-2p)·E[D_classe vera]: (1-2p)·E[D_oracolo] = {(1-2*P_FLIP)*risultati['oracolo'][0]:+.6f} contro E[D_testo] {risultati['testo'][0]:+.6f}")

    # ---------------- C ----------------
    print(f"\nC. Coerenza Python puro / numpy: {C_GRUPPI} gruppi da 30 semi, semi 31..{30 + 30 * C_GRUPPI}")
    t0 = time.perf_counter()
    Dpy = []
    for s in range(31, 31 + 30 * C_GRUPPI):
        r = seme_testo(s)
        Dpy.append(r["e1"] - r["e3"])
    Dpy = np.array(Dpy)
    mu_np, s_np, se_np = risultati["testo"][0], risultati["testo"][1], risultati["testo"][2]
    se_py = Dpy.std(ddof=1) / math.sqrt(len(Dpy))
    zc = (Dpy.mean() - mu_np) / math.sqrt(se_py ** 2 + se_np ** 2)
    tg = gruppi_t(Dpy)
    print(f"   tempo {time.perf_counter()-t0:.1f} s · E[D] Python puro {Dpy.mean():+.6f} ± {se_py:.6f} · sd {Dpy.std(ddof=1):.5f} (numpy {s_np:.5f})")
    print(f"   scarto standardizzato dalla stima numpy: {zc:+.2f} · gruppi con IC che contiene lo zero {(np.abs(tg) < T_CRIT_29).mean():.3f} · |t|>3 {(np.abs(tg) > 3).mean():.3f}")
    if abs(zc) > 3:
        problemi.append("C: la specifica in Python puro e l'implementazione numpy non concordano su E[D]")

    print()
    if problemi:
        for p in problemi:
            print("  - " + p)
        print("CALIBRAZIONE NON OK — " + " | ".join(problemi))
    else:
        print("CALIBRAZIONE OK")


if __name__ == "__main__":
    main()
