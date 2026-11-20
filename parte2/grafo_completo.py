"""Execução dos algoritmos lineares no grafo inteiro (opção --completo)."""
import time

from comum.estatistica import ic95
from comum.grafo import arestas
from parte2 import algoritmos as al


def rodar_completo(ip, ind, R, rng):
    """Algoritmos lineares no grafo inteiro (pontos de dados em R < 30 -> t-Student)."""
    n = len(ip) - 1
    print("[completo] montando listas de adjacência ...", flush=True)
    adj = [ind[ip[i]:ip[i + 1]].tolist() for i in range(n)]
    u, v = arestas(ip, ind)
    ar = list(zip(u.tolist(), v.tolist(), [1] * len(u)))
    res = []
    for nome, fn in [("BFS", lambda s: al.bfs(adj, s)), ("DFS", lambda s: al.dfs(adj, s)),
                     ("Eulerianidade", lambda s: al.eulerianidade(adj)),
                     ("Tarjan (pontes/art.)", lambda s: al.tarjan_pontes_articulacoes(adj)),
                     ("Kruskal", lambda s: al.kruskal(n, ar))]:
        ts = []
        for _ in range(R):
            s = int(rng.integers(n))
            t0 = time.perf_counter()
            r = fn(s)
            ts.append(time.perf_counter() - t0)
        media, desv, ic, dist = ic95(ts)
        extra = None
        if nome == "Eulerianidade":
            extra = r[0] + f" ({r[1]} vértices de grau ímpar)"
        if nome.startswith("Tarjan"):
            extra = f"{len(r[0])} pontes, {len(r[1])} pontos de articulação"
        if nome == "Kruskal":
            extra = f"{r[1]} arestas na árvore geradora (peso unitário)"
        res.append({"algoritmo": nome, "R": R, "media_s": media, "desvio_s": desv, "ic95_s": ic,
                    "dist": dist, "resultado": extra})
        print(f"[completo] {nome}: {media:.2f}s ± {ic:.2f} ({dist})", flush=True)
    return res
