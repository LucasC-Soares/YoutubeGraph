"""Complexidade teórica de cada algoritmo e limites de tamanho do experimento."""
import numpy as np

TEORICA = {  # nome -> (rótulo em LaTeX, f(V,E))
    "BFS": (r"$O(V+E)$", lambda V, E: V + E),
    "DFS": (r"$O(V+E)$", lambda V, E: V + E),
    "Eulerianidade": (r"$O(V+E)$", lambda V, E: V + E),
    "Dijkstra": (r"$O((V+E)\log V)$", lambda V, E: (V + E) * np.log2(V)),
    "Bellman-Ford": (r"$O(VE)$", lambda V, E: V * E),
    "Floyd-Warshall": (r"$O(V^3)$", lambda V, E: V ** 3),
    "Tarjan (pontes/art.)": (r"$O(V+E)$", lambda V, E: V + E),
    "Kruskal": (r"$O(E\log E)$", lambda V, E: E * np.log2(max(E, 2))),
    "Prim": (r"$O(E\log V)$", lambda V, E: E * np.log2(V)),
}
# tamanho máximo por algoritmo (pior caso pesado em Python puro)
LIMITE = {"Bellman-Ford": 8000, "Floyd-Warshall": 400}
