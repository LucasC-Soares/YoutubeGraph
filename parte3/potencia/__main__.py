"""Parte III.2 / Apêndice B — A distribuição de graus sugere uma lei de potência?

Passos (conforme o apêndice):
 1. distribuição de graus P(k) e CCDF;
 2. gráficos em escala log-log (P(k) e CCDF);
 3. ajuste: (a) regressão linear de log CCDF x log k e (b) MLE de γ com k_min por mínima
    distância KS (detalhes e limitações em parte3/potencia/ajuste.py).

Uso (na raiz do repositório):  python -m parte3.potencia [--kmin-max 200]
Saídas em parte3/resultados/: parte3_potencia.json, tab_potencia.tex, fig/potencia.pdf
"""
import argparse
import json

import numpy as np

from comum.config import pasta_saida
from comum.dados import carregar_grafo
from comum.saida import salvar_json
from parte3.potencia.ajuste import melhor_kmin, regressao_ccdf
from parte3.potencia.distribuicao import distribuicao
from parte3.potencia.grafico import grafico
from parte3.potencia.tabela import tabela


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kmin-max", type=int, default=200)
    args = ap.parse_args()

    pasta = pasta_saida("parte3")
    ip, ind, _, _ = carregar_grafo()
    deg = np.diff(ip)
    graus, ks, pk, ccdf = distribuicao(deg)

    ols = regressao_ccdf(ks, ccdf)
    melhor = melhor_kmin(graus, args.kmin_max)
    saida = {"n_vertices": int(len(deg)), "grau_max": int(graus.max()), "grau_medio": float(graus.mean()),
             "ols_ccdf": ols, "mle": melhor}
    salvar_json(pasta, "parte3_potencia.json", saida)
    grafico(ks, pk, ccdf, melhor, pasta)
    tabela(ols, melhor, pasta)
    print(json.dumps(saida, indent=2, default=float))


if __name__ == "__main__":
    main()
