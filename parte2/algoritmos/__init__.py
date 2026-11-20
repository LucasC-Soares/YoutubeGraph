"""Algoritmos de grafos da disciplina, implementados do zero (um módulo por família).

Entrada: lista de adjacência (list[list[int]]) ou ponderada (list[list[tuple[int, float]]]).
Todas as versões são iterativas (sem recursão) para suportar grafos grandes.
"""
from .agm import DSU, kruskal, prim
from .busca import bfs, dfs
from .caminhos_minimos import INF, bellman_ford, dijkstra, floyd_warshall
from .euleriano import eulerianidade
from .tarjan import tarjan_pontes_articulacoes
