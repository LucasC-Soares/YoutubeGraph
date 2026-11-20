"""Parte I — Análise estrutural obrigatória.

Uso (na raiz do repositório):  python -m parte1 [--fontes 200] [--amostra-clust 20000]

Saídas em parte1/resultados/:
  parte1.json, tab_estrutural.tex, tab_componentes.tex, tab_computado.tex,
  distribuicao_graus.csv, fig/graus.pdf, fig/visualizacao.pdf
"""
import argparse

from comum.config import pasta_saida, rng_padrao
from comum.dados import carregar_grafo
from comum.saida import salvar_json
from parte1 import basicas, clusterizacao, componentes, distancias, grafico_graus, tabelas, visualizacao


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fontes", type=int, default=200,
                    help="nº de BFS aleatórias (caminho médio / diâmetro / raio)")
    ap.add_argument("--amostra-clust", type=int, default=20000,
                    help="nº de vértices amostrados p/ clusterização (0 = todos)")
    ap.add_argument("--visualizacao", type=int, default=200,
                    help="nº de vértices da visualização reduzida")
    ap.add_argument("--sem-igraph", action="store_true",
                    help="não usa igraph p/ triângulos exatos")
    args = ap.parse_args()

    pasta = pasta_saida("parte1")
    rng = rng_padrao(1)
    ip, ind, ids, rel = carregar_grafo()
    n = len(ip) - 1
    status = {}  # medida -> (valor, como foi obtida)

    ks, cont = basicas.medir(ip, ind, status, pasta)
    lcc, tam_ord = componentes.medir(ip, ind, status)
    diam_lb, raio_ub, caminho_medio = distancias.medir(ip, ind, lcc, args.fontes, rng, status)
    clusterizacao.medir(ip, ind, args.amostra_clust, rng, not args.sem_igraph, status)

    visualizacao.visualizar(ip, ind, args.visualizacao, pasta)
    status["Visualização do grafo"] = (f"subgrafo de {args.visualizacao} vértices", "versão reduzida")
    grafico_graus.grafico_graus(ks, cont, n, pasta)

    salvar_json(pasta, "parte1.json", {
        "limpeza": rel,
        "medidas": {k_: {"valor": v[0], "como": v[1]} for k_, v in status.items()},
        "componentes_top10": [int(x) for x in tam_ord[:10]],
        "diametro_lb": diam_lb, "raio_ub": raio_ub,
        "caminho_medio": caminho_medio,
    })
    tabelas.tabela_estrutural(status, pasta)
    tabelas.tabela_componentes(tam_ord, n, pasta)
    tabelas.tabela_computado(status, pasta)
    for k_, v in status.items():
        print(f"{k_:40s} {v[0]}   [{v[1]}]")


if __name__ == "__main__":
    main()
