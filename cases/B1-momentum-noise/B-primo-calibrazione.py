#!/usr/bin/env python3
"""Calibrazione del caso B' (il momentum e il rumore del gradiente).

Interprete: /Library/Frameworks/Python.framework/Versions/3.10/bin/python3 (serve numpy).

Verifica i numeri scritti in verita/B-primo.md:

  1. FORMA CHIUSA. Errore a regime (varianza stazionaria di x) per la regola
         v <- beta*v + g,  x <- x - alpha*v,  g = lambda*x + sigma*xi
     gamma0(beta) = alpha*sigma^2*(1+beta) / ((1-beta)*lambda*(2(1+beta) - alpha*lambda))
     e rapporto R = gamma0(0,9)/gamma0(0) = 9,9763. Controllata per una seconda
     via indipendente: equazione di Lyapunov discreta 2x2 risolta con numpy.
     Controllato anche che R > 1 per ogni beta in (0,1) su griglia (l'affermazione
     e' falsa per ogni beta, non solo per 0,9).
  2. PROTOCOLLO DEL CASO, alla lettera, in Python puro (stdlib): semi 1..30,
     random.Random(s).gauss(0,1), stesso seme per le due varianti. Misura:
     mediane su semi dell'errore a regime, rapporto delle mediane R_hat (la grandezza
     della condizione di invalidazione), tempo di esecuzione (< 60 s).
  3. DISTRIBUZIONE di R_hat su 200 lotti indipendenti da 30 semi (numpy): la
     condizione di invalidazione (R_hat < 5) non deve scattare in nessun lotto.
     Medie su 6000 semi contro la forma chiusa, tolleranza 2 %.
  4. TRAPPOLE documentate nella verita':
     T1 forma "media mobile" v <- beta*v + (1-beta)*g: R_EMA atteso 0,99526 (< 1:
        un laboratorio che rinegozia la forma "conferma" l'affermazione).
     T2 fase iniziale: tempo al primo |x_t| <= 1 partendo da x_0 = 10; il momentum
        deve essere piu' veloce (la fase transitoria "conferma" l'affermazione).

Ultima riga stampata: esattamente "CALIBRAZIONE OK", oppure
"CALIBRAZIONE NON OK — correggere: ..." con l'elenco di cosa correggere.
"""

import random
import time

import numpy as np

# --- Ambiente del caso B' (deve coincidere con casi/B-primo-momentum-e-rumore.md) ---
LAMBDA = 1.0
SIGMA = 1.0
ALPHA = 0.01
BETA = 0.9
X0 = 10.0
T = 20_000
INIZIO_FINESTRA = 10_001          # errore a regime = media di x_t^2, t = 10001..20000
SEMI = range(1, 31)

# --- Soglie della verita' ---
SOGLIA_INVALIDAZIONE = 5.0        # R_hat < 5  => verita' invalidata
TOL_FORMA_CHIUSA = 1e-12          # Lyapunov contro formula (relativa)
TOL_MEDIE = 0.02                  # medie su 6000 semi contro forma chiusa (relativa)
TOL_PROTOCOLLO = 0.15             # R_hat del protocollo (30 semi) contro R (relativa)
TOL_EMA = 0.01                    # R_EMA misurato contro forma chiusa (assoluta)
N_LOTTI = 200
SEME_NUMPY = 20261017


def gamma0(alpha, beta, lam=LAMBDA, sigma=SIGMA):
    """Varianza stazionaria di x per la regola heavy-ball (forma chiusa, derivata nella verita')."""
    return alpha * sigma**2 * (1 + beta) / ((1 - beta) * lam * (2 * (1 + beta) - alpha * lam))


def gamma0_lyapunov(alpha, beta, lam=LAMBDA, sigma=SIGMA):
    """Seconda via: stato z_t = (x_t, x_{t-1}) (2x1), z_{t+1} = A z_t + b e_t,
    covarianza stazionaria P (2x2) da P = A P A' + b b' s^2, risolta come sistema lineare 4x4."""
    a = 1 + beta - alpha * lam
    A = np.array([[a, -beta], [1.0, 0.0]])                  # 2x2
    b = np.array([[1.0], [0.0]])                            # 2x1
    Q = (alpha * sigma) ** 2 * (b @ b.T)                    # 2x2
    M = np.eye(4) - np.kron(A, A)                           # 4x4: vec(P) = (I - A(x)A)^-1 vec(Q)
    P = np.linalg.solve(M, Q.reshape(4)).reshape(2, 2)
    return P[0, 0]


def protocollo_stdlib():
    """Il protocollo del caso alla lettera, in Python puro. Ritorna (err_v1, err_v2, secondi)."""
    t0 = time.time()
    err = {0.0: [], BETA: []}
    for beta in (0.0, BETA):
        for s in SEMI:
            rng = random.Random(s)
            x, v, acc = X0, 0.0, 0.0
            for t in range(T):                              # passo t: da x_t a x_{t+1}
                g = LAMBDA * x + SIGMA * rng.gauss(0, 1)
                v = beta * v + g
                x = x - ALPHA * v
                if t + 1 >= INIZIO_FINESTRA:
                    acc += x * x
            err[beta].append(acc / (T - INIZIO_FINESTRA + 1))
    return err[0.0], err[BETA], time.time() - t0


def simula_numpy(rng, n, soglia_transitorio=1.0):
    """Tre varianti in parallelo sugli stessi rumori (n semi): senza momentum, heavy-ball,
    'media mobile'. Il rumore xi_t (n,) si genera passo per passo (niente matrice T x n).
    Ritorna errori a regime (3, n) e primo t con |x_t| <= soglia (3, n)."""
    beta = np.array([[0.0], [BETA], [BETA]])                # 3x1
    peso_g = np.array([[1.0], [1.0], [1 - BETA]])           # 3x1: la terza e' la forma smorzata
    x = np.full((3, n), X0)
    v = np.zeros((3, n))
    acc = np.zeros((3, n))
    primo = np.full((3, n), -1)
    for t in range(T):
        xi = rng.standard_normal(n)                         # stesso rumore per le tre varianti
        g = LAMBDA * x + SIGMA * xi
        v = beta * v + peso_g * g
        x = x - ALPHA * v
        if t + 1 >= INIZIO_FINESTRA:
            acc += x * x
        nuovi = (primo < 0) & (np.abs(x) <= soglia_transitorio)
        primo[nuovi] = t + 1
    return acc / (T - INIZIO_FINESTRA + 1), primo


def main():
    problemi = []
    al = ALPHA * LAMBDA

    # ---------------- 1. forma chiusa ----------------
    g_v1, g_v2 = gamma0(ALPHA, 0.0), gamma0(ALPHA, BETA)
    R = g_v2 / g_v1
    R_ema = gamma0(ALPHA * (1 - BETA), BETA) / g_v1
    print(f"Ambiente: lambda={LAMBDA}, sigma={SIGMA}, alpha={ALPHA}, beta={BETA}, x0={X0}, T={T}, "
          f"finestra t={INIZIO_FINESTRA}..{T}")
    print(f"[1] forma chiusa: gamma0(beta=0) = {g_v1:.8f}   gamma0(beta=0,9) = {g_v2:.8f}   R = {R:.6f}")
    print(f"    forma 'media mobile' (T1): R_EMA = {R_ema:.6f}")
    l_v1, l_v2 = gamma0_lyapunov(ALPHA, 0.0), gamma0_lyapunov(ALPHA, BETA)
    err_ly = max(abs(l_v1 - g_v1) / g_v1, abs(l_v2 - g_v2) / g_v2)
    print(f"    Lyapunov 2x2: {l_v1:.12f}  {l_v2:.12f}   scarto relativo max {err_ly:.2e}")
    if err_ly > TOL_FORMA_CHIUSA:
        problemi.append(f"forma chiusa e Lyapunov discordano ({err_ly:.1e}): rivedere la derivazione")
    radici = np.roots([1, -(1 + BETA - al), BETA])
    modulo = np.abs(radici).max()
    print(f"    radici del polinomio caratteristico (beta=0,9): {radici}  modulo max {modulo:.6f} "
          f"(stabile se < 1)")
    if modulo >= 1:
        problemi.append("variante 2 instabile: rivedere alpha o beta")
    griglia = np.linspace(0.01, 0.99, 99)
    R_griglia = np.array([gamma0(ALPHA, b) / g_v1 for b in griglia])
    print(f"    R su beta in [0,01; 0,99]: min {R_griglia.min():.6f} (a beta=0,01), max {R_griglia.max():.2f}")
    if R_griglia.min() <= 1:
        problemi.append("esiste un beta con R <= 1: l'affermazione non e' falsa per ogni beta come scritto")

    # ---------------- 2. protocollo alla lettera, stdlib ----------------
    e1, e2, secondi = protocollo_stdlib()
    m1, m2 = float(np.median(e1)), float(np.median(e2))
    R_hat = m2 / m1
    print(f"[2] protocollo stdlib (semi 1..30): variante 1 mediana {m1:.10f} [min {min(e1):.6f}, max {max(e1):.6f}]")
    print(f"                                   variante 2 mediana {m2:.10f} [min {min(e2):.6f}, max {max(e2):.6f}]")
    peggiori = sum(1 for a, b in zip(e1, e2) if b > a)
    print(f"    R_hat = {R_hat:.8f} (forma chiusa {R:.4f}); semi con errore v2 > v1: {peggiori}/30; "
          f"min su semi di v2/v1 = {min(b / a for a, b in zip(e1, e2)):.3f}")
    print(f"    durata del protocollo in Python puro: {secondi:.1f} s")
    if R_hat < SOGLIA_INVALIDAZIONE:
        problemi.append(f"la condizione di invalidazione SCATTA sul protocollo (R_hat {R_hat:.2f} < 5)")
    if abs(R_hat - R) / R > TOL_PROTOCOLLO:
        problemi.append(f"R_hat del protocollo lontano dalla forma chiusa ({R_hat:.3f} contro {R:.3f})")
    if secondi >= 60:
        problemi.append(f"protocollo troppo lento in Python puro ({secondi:.0f} s >= 60)")

    # ---------------- 3. distribuzione di R_hat su lotti, numpy ----------------
    rng = np.random.default_rng(SEME_NUMPY)
    n = N_LOTTI * 30
    err3, primo3 = simula_numpy(rng, n)
    a1, a2, a3 = err3
    tr1, tr2 = primo3[0], primo3[1]
    r_lotti = np.median(a2.reshape(N_LOTTI, 30), axis=1) / np.median(a1.reshape(N_LOTTI, 30), axis=1)
    print(f"[3] {n} semi numpy: media errore v1 {a1.mean():.6f} (teoria {g_v1:.6f}, scarto "
          f"{(a1.mean() - g_v1) / g_v1:+.2%}); v2 {a2.mean():.6f} (teoria {g_v2:.6f}, scarto "
          f"{(a2.mean() - g_v2) / g_v2:+.2%})")
    print(f"    R_hat su {N_LOTTI} lotti da 30: min {r_lotti.min():.3f}, 1° percentile "
          f"{np.percentile(r_lotti, 1):.3f}, mediana {np.median(r_lotti):.3f}, max {r_lotti.max():.3f}")
    print(f"    margine della condizione di invalidazione: min R_hat / 5 = {r_lotti.min() / 5:.2f}x; "
          f"effetto contro il segno affermato: R = {R:.2f}x (l'affermazione richiede R < 1)")
    for nome, mis, teo in (("v1", a1.mean(), g_v1), ("v2", a2.mean(), g_v2)):
        if abs(mis - teo) / teo > TOL_MEDIE:
            problemi.append(f"media simulata {nome} discorda dalla forma chiusa oltre il 2 %")
    if r_lotti.min() < SOGLIA_INVALIDAZIONE:
        problemi.append(f"in {int((r_lotti < 5).sum())} lotti su {N_LOTTI} la condizione di invalidazione scatterebbe")

    # ---------------- 4. trappole ----------------
    R_ema_mis = a3.mean() / a1.mean()
    d = a3 - a1
    t_pair = d.mean() / (d.std(ddof=1) / np.sqrt(n))
    frac = (a3 < a1).mean()
    print(f"[4] T1 forma 'media mobile': R_EMA misurato {R_ema_mis:.5f} (teoria {R_ema:.5f}); "
          f"semi con errore minore della variante 1: {frac:.1%}; t appaiato su {n} semi {t_pair:+.1f}")
    d30 = (a3 - a1).reshape(N_LOTTI, 30)
    t30 = d30.mean(axis=1) / (d30.std(axis=1, ddof=1) / np.sqrt(30))
    print(f"    su lotti da 30 semi appaiati: frazione di lotti con t < -2 (\"riduce\", significativo): "
          f"{(t30 < -2).mean():.1%}; con mediana EMA < mediana v1: "
          f"{(np.median(a3.reshape(N_LOTTI, 30), axis=1) < np.median(a1.reshape(N_LOTTI, 30), axis=1)).mean():.1%}")
    if abs(R_ema_mis - R_ema) > TOL_EMA or R_ema_mis >= 1:
        problemi.append("trappola T1 non come descritta (R_EMA misurato non ~0,995 o non < 1)")
    tm1, tm2 = np.median(tr1), np.median(tr2)
    print(f"    T2 fase iniziale: primo t con |x_t| <= 1, mediana v1 {tm1:.0f}, v2 {tm2:.0f} "
          f"(rapporto {tm1 / tm2:.1f}x a favore del momentum)")
    if not tm2 < tm1 / 2:
        problemi.append("trappola T2 non come descritta (il momentum non e' almeno 2x piu' veloce nel transitorio)")

    print()
    if problemi:
        print("CALIBRAZIONE NON OK — correggere: " + "; ".join(problemi))
    else:
        print("CALIBRAZIONE OK")


if __name__ == "__main__":
    main()
