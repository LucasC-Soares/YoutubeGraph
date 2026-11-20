"""Ajuste da lei de potência: regressão log-log da CCDF e MLE com k_min por KS.

Estimador (Clauset, Shalizi & Newman, 2009), aproximação contínua com correção de 1/2
para dados discretos:  γ = 1 + n_cauda / Σ ln( k_i / (k_min - 1/2) ).
Limitação: não fazemos o teste de bondade de ajuste por bootstrap nem LR vs. outras
distribuições; reportar como tal.
"""
import numpy as np


def ajuste_mle(graus, kmin):
    cauda = graus[graus >= kmin].astype(float)
    nt = len(cauda)
    if nt < 50:
        return None
    gamma = 1.0 + nt / np.sum(np.log(cauda / (kmin - 0.5)))
    cauda_ord = np.sort(cauda)
    ks_vals = np.unique(cauda_ord)
    # CCDF empírica em cada valor distinto (P(K >= k))
    emp = 1.0 - np.searchsorted(cauda_ord, ks_vals, side="left") / nt
    mod = ((ks_vals - 0.5) / (kmin - 0.5)) ** (1.0 - gamma)
    ks = float(np.max(np.abs(emp - mod)))
    return {"kmin": int(kmin), "gamma": float(gamma), "ks": ks, "n_cauda": int(nt),
            "erro_padrao": float((gamma - 1.0) / np.sqrt(nt))}


def regressao_ccdf(ks, ccdf, k_min_regressao=5):
    """Regressão linear de log CCDF x log k na cauda (k >= k_min_regressao): CCDF ~ k^(1-γ)."""
    sel = ks >= k_min_regressao
    b, a = np.polyfit(np.log(ks[sel]), np.log(ccdf[sel]), 1)
    r2 = float(np.corrcoef(np.log(ks[sel]), np.log(ccdf[sel]))[0, 1] ** 2)
    return {"gamma": float(1.0 - b), "r2": r2, "k_min_regressao": k_min_regressao}


def melhor_kmin(graus, kmin_max):
    """MLE para cada k_min em [2, kmin_max]; devolve o de menor distância KS."""
    melhor = None
    for kmin in range(2, kmin_max + 1):
        r = ajuste_mle(graus, kmin)
        if r is None:
            break
        if melhor is None or r["ks"] < melhor["ks"]:
            melhor = r
    return melhor
