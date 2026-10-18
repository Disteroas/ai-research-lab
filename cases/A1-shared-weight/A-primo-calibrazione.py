#!/usr/bin/env python3
"""Calibrazione del caso A' (il peso condiviso) — verita' in verita/A-primo.md.

Esecuzione: dal 2026-10-17 la lancia anche la sessione autonoma (Emendamento 1 della rotta).
Solo libreria standard: la parte simulata e' anche la prova che un'implementazione in Python puro
sta nel budget di 60 s del testo del caso.

Verifica, nell'ordine:
  1. FORMA CHIUSA, in aritmetica razionale esatta (fractions):
     eta, mu, v_pi, punto fisso di Monte Carlo (proiezione mu-pesata), punto fisso di TD(0)
     (sistema Phi' D (I-P) Phi w = Phi' D rbar), VE_MC* = 1/48, VE_TD* = 11/48, rapporto = 11 =
     1 + 1/(1-p); VE iniziale = 119/48; rapporti-trappola (pesi uniformi, pesi per episodio) = 2;
     rapporto sulla radice (RMS) = sqrt(11).
  2. SIMULAZIONE del protocollo esatto del testo (60 semi, 2000 episodi, alpha = 0,02):
     - effetto grande: mediana su semi di rho = VE_TD/VE_MC finale >= 8 (1,6 x la soglia 5 del
       testo) e minimo su semi >= 6 (1,2 x la soglia);
     - condizione di invalidazione (verita' §Invalidazione): banda [5, 20] sulla mediana di rho —
       NON deve scattare, e ogni seme deve stare in [6, 16] (margine per seme);
     - media di VE_MC entro 5% della teoria stazionaria esatta 1/48 + (1/6) * alpha*0,25/(2-alpha);
       media di VE_TD entro 5% di 11/48;
     - punti fissi raggiunti: |w - w*|_inf <= 0,25 su ogni seme e braccio;
     - apprendimento evidente su entrambi i bracci: VE_finale / VE_iniziale <= 0,2 su ogni seme;
     - regime sostenuto: mediana su semi di VE nei blocchi 16-20 entro 10% del valore atteso.
  3. TEMPO: protocollo da 30 semi x 2 algoritmi in Python puro < 20 s (il testo concede 60 s).

Ultima riga: esattamente "CALIBRAZIONE OK", oppure "CALIBRAZIONE NON OK — correggere: ...".
"""

import random
import statistics
import time
from fractions import Fraction as F

# --- Ambiente del caso A' (deve coincidere con casi/A-primo-peso-condiviso.md) ---
P_RESTA = F(9, 10)          # probabilita' di restare nella sala
R_U1, R_U2 = 2, 1           # ricompense d'uscita
ALPHA = 0.02
EPISODI = 2000
BLOCCO = 100
N_SEMI = 60
SEED_MASTER = 20261017
SOGLIA_TESTO = 5            # "almeno 5 volte" nell'affermazione

# stati non terminali: 0=I, 1=S1, 2=S2, 3=U1, 4=U2 ; T = -1
NOMI = ["I", "S1", "S2", "U1", "U2"]
GRUPPO = [0, 1, 2, 3, 3]    # U1 e U2 condividono il peso w_U
N_S, N_G = 5, 4
T = -1


# ---------------------------------------------------------------- forma chiusa
def risolvi(A, b):
    """Eliminazione di Gauss in aritmetica razionale. A lista di liste, b lista."""
    n = len(A)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        piv = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[piv] = M[piv], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [M[r][k] - f * M[c][k] for k in range(n + 1)]
    return [M[i][n] / M[i][i] for i in range(n)]


def forma_chiusa():
    p = P_RESTA
    # P: transizioni fra stati non terminali (5x5); rbar: ricompensa attesa uscendo da s (5)
    P = [[F(0)] * N_S for _ in range(N_S)]
    P[0][1] = P[0][2] = F(1, 2)
    P[1][1], P[1][3] = p, 1 - p
    P[2][2], P[2][4] = p, 1 - p
    rbar = [F(0), F(0), F(0), F(R_U1), F(R_U2)]
    I_P = [[(1 if i == j else 0) - P[i][j] for j in range(N_S)] for i in range(N_S)]
    # v = (I-P)^-1 rbar   (gamma = 1)
    v = risolvi(I_P, rbar)
    # eta' = d0' (I-P)^-1  <=>  (I-P)' eta = d0
    d0 = [F(1), F(0), F(0), F(0), F(0)]
    I_P_T = [[I_P[j][i] for j in range(N_S)] for i in range(N_S)]
    eta = risolvi(I_P_T, d0)
    mu = [e / sum(eta) for e in eta]
    # Phi (5x4) one-hot per gruppo
    Phi = [[F(1) if GRUPPO[s] == g else F(0) for g in range(N_G)] for s in range(N_S)]
    # MC: minimizza VE -> (Phi' D Phi) w = Phi' D v
    A_mc = [[sum(Phi[s][g] * mu[s] * Phi[s][h] for s in range(N_S)) for h in range(N_G)]
            for g in range(N_G)]
    b_mc = [sum(Phi[s][g] * mu[s] * v[s] for s in range(N_S)) for g in range(N_G)]
    w_mc = risolvi(A_mc, b_mc)
    # TD: punto fisso di TD(0) semi-gradiente -> Phi' D (I-P) Phi w = Phi' D rbar
    IP_Phi = [[sum(I_P[s][t] * Phi[t][h] for t in range(N_S)) for h in range(N_G)]
              for s in range(N_S)]
    A_td = [[sum(Phi[s][g] * mu[s] * IP_Phi[s][h] for s in range(N_S)) for h in range(N_G)]
            for g in range(N_G)]
    b_td = [sum(Phi[s][g] * mu[s] * rbar[s] for s in range(N_S)) for g in range(N_G)]
    w_td = risolvi(A_td, b_td)
    return v, eta, mu, w_mc, w_td


def ve(w, v, pesi):
    return sum(pesi[s] * (v[s] - w[GRUPPO[s]]) ** 2 for s in range(N_S))


# ---------------------------------------------------------------- simulazione (stdlib)
def episodio(rng, p_resta):
    """Lista di transizioni (s, r, s2). Il processo non dipende dai pesi."""
    tr = []
    s = 0
    while s != T:
        if s == 0:
            s2, r = (1 if rng.random() < 0.5 else 2), 0.0
        elif s in (1, 2):
            s2, r = (s if rng.random() < p_resta else s + 2), 0.0
        else:
            s2, r = T, (float(R_U1) if s == 3 else float(R_U2))
        tr.append((s, r, s2))
        s = s2
    return tr


def run(algoritmo, seme, v, mu):
    """Un seme, un algoritmo. Ritorna (pesi finali, VE per blocco)."""
    rng = random.Random(seme)
    p_resta = float(P_RESTA)
    w = [0.0] * N_G
    ve_blocchi = []
    for ep in range(1, EPISODI + 1):
        tr = episodio(rng, p_resta)
        if algoritmo == "TD":
            # online: il processo non dipende da w, quindi applicare in ordine dopo aver
            # generato l'episodio e' identico all'aggiornamento passo per passo
            for s, r, s2 in tr:
                g = GRUPPO[s]
                bersaglio = r + (w[GRUPPO[s2]] if s2 != T else 0.0)
                w[g] += ALPHA * (bersaglio - w[g])
        else:
            # Monte Carlo every-visit a fine episodio, t = 0..T-1 in ordine, pesi correnti
            G = [0.0] * len(tr)
            acc = 0.0
            for t in range(len(tr) - 1, -1, -1):
                acc += tr[t][1]
                G[t] = acc
            for t, (s, _, _) in enumerate(tr):
                g = GRUPPO[s]
                w[g] += ALPHA * (G[t] - w[g])
        if ep % BLOCCO == 0:
            ve_blocchi.append(ve(w, v, mu))
    return w, ve_blocchi


def main():
    problemi = []

    # ---------------- 1. forma chiusa esatta
    v, eta, mu, w_mc, w_td = forma_chiusa()
    p = P_RESTA
    ve_mc_star = ve(w_mc, v, mu)
    ve_td_star = ve(w_td, v, mu)
    ve_init = ve([F(0)] * N_G, v, mu)
    rapporto = ve_td_star / ve_mc_star
    print("FORMA CHIUSA (aritmetica razionale esatta)")
    print("  eta  =", [str(x) for x in eta], " somma", sum(eta))
    print("  mu   =", [str(x) for x in mu])
    print("  v_pi =", [str(x) for x in v])
    print("  w_MC* (I,S1,S2,U) =", [str(x) for x in w_mc])
    print("  w_TD* (I,S1,S2,U) =", [str(x) for x in w_td])
    print(f"  VE_MC* = {ve_mc_star} = {float(ve_mc_star):.6f}   (teoria 1/48)")
    print(f"  VE_TD* = {ve_td_star} = {float(ve_td_star):.6f}   (teoria 11/48)")
    print(f"  rapporto = {rapporto}   (teoria 1 + 1/(1-p) = {1 + 1 / (1 - p)})")
    print(f"  VE iniziale (w = 0) = {ve_init} = {float(ve_init):.6f}   (teoria 119/48)")
    if ve_mc_star != F(1, 48):
        problemi.append("VE_MC* != 1/48: rivedere la derivazione o l'ambiente")
    if ve_td_star != F(11, 48):
        problemi.append("VE_TD* != 11/48: rivedere la derivazione o l'ambiente")
    if rapporto != 1 + 1 / (1 - p) or rapporto != 11:
        problemi.append("rapporto di forma chiusa != 11")
    if ve_init != F(119, 48):
        problemi.append("VE iniziale != 119/48")

    # trappole: stessi punti fissi, metro sbagliato
    unif = [F(1, 5)] * N_S
    visita = [F(1), F(1, 2), F(1, 2), F(1, 2), F(1, 2)]     # P(visitare s in un episodio)
    visita = [x / sum(visita) for x in visita]
    r_unif = ve(w_td, v, unif) / ve(w_mc, v, unif)
    r_visita = ve(w_td, v, visita) / ve(w_mc, v, visita)
    print(f"  trappola pesi uniformi: rapporto = {r_unif}   (teoria 2)")
    print(f"  trappola pesi per episodio (prima visita): rapporto = {r_visita}   (teoria 2)")
    print(f"  trappola radice (RMS): rapporto = sqrt(11) = {float(rapporto) ** 0.5:.4f}")
    if r_unif != 2 or r_visita != 2:
        problemi.append("rapporti-trappola diversi da 2: aggiornare la verita'")

    # teoria stazionaria di VE_MC con alpha costante (esatta, verita' §Rumore)
    var_ar1 = ALPHA * 0.25 / (2 - ALPHA)
    ve_mc_teoria = float(ve_mc_star) + (1 / 6) * var_ar1
    print(f"  VE_MC stazionario atteso = 1/48 + (1/6)*{var_ar1:.6f} = {ve_mc_teoria:.6f}")

    # ---------------- 2. simulazione
    vf = [float(x) for x in v]
    muf = [float(x) for x in mu]
    w_mc_f = [float(x) for x in w_mc]
    w_td_f = [float(x) for x in w_td]
    ve_init_f = float(ve_init)

    t0 = time.time()
    ris = {"TD": [], "MC": []}
    for k in range(N_SEMI):
        ris["TD"].append(run("TD", SEED_MASTER + 2 * k, vf, muf))
        ris["MC"].append(run("MC", SEED_MASTER + 2 * k + 1, vf, muf))
    durata = time.time() - t0
    durata_30 = durata * 30 / N_SEMI

    ve_td_fin = [b[-1] for _, b in ris["TD"]]
    ve_mc_fin = [b[-1] for _, b in ris["MC"]]
    rho = [a / b for a, b in zip(ve_td_fin, ve_mc_fin)]
    med_rho = statistics.median(rho)
    q = statistics.quantiles(rho, n=4)
    print()
    print(f"SIMULAZIONE ({N_SEMI} semi, {EPISODI} episodi, alpha = {ALPHA})")
    print(f"  VE_TD finale: media {statistics.mean(ve_td_fin):.5f}  mediana "
          f"{statistics.median(ve_td_fin):.5f}  min {min(ve_td_fin):.5f}  max {max(ve_td_fin):.5f}")
    print(f"  VE_MC finale: media {statistics.mean(ve_mc_fin):.5f}  mediana "
          f"{statistics.median(ve_mc_fin):.5f}  min {min(ve_mc_fin):.5f}  max {max(ve_mc_fin):.5f}")
    print(f"  rho = VE_TD/VE_MC: mediana {med_rho:.3f}  IQR [{q[0]:.3f}, {q[2]:.3f}]  "
          f"min {min(rho):.3f}  max {max(rho):.3f}")
    rho_rms = [r ** 0.5 for r in rho]
    print(f"  (trappola RMS sul simulato: mediana sqrt(rho) = {statistics.median(rho_rms):.3f})")

    # effetto grande
    if med_rho < 1.6 * SOGLIA_TESTO:
        problemi.append(f"effetto non abbastanza grande: mediana rho {med_rho:.2f} < 8")
    if min(rho) < 1.2 * SOGLIA_TESTO:
        problemi.append(f"un seme ha rho {min(rho):.2f} < 6: margine per seme insufficiente")
    # invalidazione: banda [5, 20] sulla mediana, non deve scattare; ogni seme in [6, 16]
    invalida = med_rho < 5 or med_rho > 20
    print(f"  condizione di invalidazione (mediana rho fuori da [5, 20]): "
          f"{'SCATTA' if invalida else 'non scatta'}")
    if invalida:
        problemi.append("la condizione di invalidazione scatta sulla parametrizzazione scelta")
    if min(rho) < 6 or max(rho) > 16:
        problemi.append(f"semi fuori da [6, 16]: min {min(rho):.2f}, max {max(rho):.2f}")
    # medie contro teoria
    m_mc, m_td = statistics.mean(ve_mc_fin), statistics.mean(ve_td_fin)
    print(f"  media VE_MC {m_mc:.6f} vs teoria {ve_mc_teoria:.6f} "
          f"(scarto {100 * (m_mc / ve_mc_teoria - 1):+.2f}%)")
    print(f"  media VE_TD {m_td:.6f} vs 11/48 = {float(ve_td_star):.6f} "
          f"(scarto {100 * (m_td / float(ve_td_star) - 1):+.2f}%)")
    if abs(m_mc / ve_mc_teoria - 1) > 0.05:
        problemi.append("media di VE_MC fuori dal 5% della teoria stazionaria")
    if abs(m_td / float(ve_td_star) - 1) > 0.05:
        problemi.append("media di VE_TD fuori dal 5% di 11/48")
    # punti fissi raggiunti
    d_td = max(max(abs(a - b) for a, b in zip(w, w_td_f)) for w, _ in ris["TD"])
    d_mc = max(max(abs(a - b) for a, b in zip(w, w_mc_f)) for w, _ in ris["MC"])
    print(f"  max |w - w*| su semi: TD {d_td:.4f}, MC {d_mc:.4f}  (tolleranza 0,25)")
    if d_td > 0.25 or d_mc > 0.25:
        problemi.append("un braccio non ha raggiunto il proprio punto fisso")
    # apprendimento evidente
    fr_td = max(x / ve_init_f for x in ve_td_fin)
    fr_mc = max(x / ve_init_f for x in ve_mc_fin)
    print(f"  max VE_finale/VE_iniziale: TD {fr_td:.4f}, MC {fr_mc:.4f}  (tetto 0,2)")
    if fr_td > 0.2 or fr_mc > 0.2:
        problemi.append("apprendimento poco evidente su un braccio (VE_fin/VE_init > 0,2)")
    # regime sostenuto: blocchi 16-20
    for nome, atteso in (("TD", float(ve_td_star)), ("MC", ve_mc_teoria)):
        meds = [statistics.median(b[i] for _, b in ris[nome]) for i in range(15, 20)]
        print(f"  {nome}: mediana su semi di VE nei blocchi 16-20: "
              + " ".join(f"{m:.4f}" for m in meds))
        if any(abs(m / atteso - 1) > 0.10 for m in meds):
            problemi.append(f"{nome}: regime dei blocchi 16-20 non stabile entro 10%")
    meds1 = [statistics.median(b[0] for _, b in ris[n]) for n in ("TD", "MC")]
    print(f"  (blocco 1, dopo 100 episodi: mediana VE TD {meds1[0]:.4f}, MC {meds1[1]:.4f})")

    # ---------------- 3. tempo
    print(f"  durata: {durata:.1f} s per {N_SEMI} semi x 2; stima protocollo da 30 semi: "
          f"{durata_30:.1f} s (tetto 20 s, il testo concede 60)")
    if durata_30 > 20:
        problemi.append(f"protocollo in Python puro troppo lento ({durata_30:.0f} s stimati)")

    print()
    for x in problemi:
        print("  - " + x)
    if problemi:
        print("CALIBRAZIONE NON OK — correggere: " + "; ".join(problemi))
    else:
        print("CALIBRAZIONE OK")


if __name__ == "__main__":
    main()
