"""Média, desvio e IC95% (Z se n >= 30, t-Student caso contrário)."""
import numpy as np

_T975 = [12.706, 4.303, 3.182, 2.776, 2.571, 2.447, 2.365, 2.306, 2.262, 2.228,
         2.201, 2.179, 2.160, 2.145, 2.131, 2.120, 2.110, 2.101, 2.093, 2.086,
         2.080, 2.074, 2.069, 2.064, 2.060, 2.056, 2.052, 2.048, 2.045]  # gl = 1..29
Z975 = 1.959964


def ic95(x):
    """Retorna (média, desvio amostral, meia-largura do IC95%, 'Z'|'t')."""
    x = np.asarray(x, dtype=float)
    n = len(x)
    media = float(x.mean())
    if n < 2:
        return media, 0.0, 0.0, "-"
    s = float(x.std(ddof=1))
    if n >= 30:
        crit, dist = Z975, "Z"
    else:
        crit, dist = _T975[n - 2], "t"
    return media, s, crit * s / np.sqrt(n), dist
