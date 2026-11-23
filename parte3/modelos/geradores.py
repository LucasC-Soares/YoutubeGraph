"""Geradores de modelos clássicos (implementação própria): Barabási–Albert e Watts–Strogatz.
O Erdős–Rényi G(n, m) já existe em parte3/smallworld/grafo_aleatorio.py."""
import numpy as np

from comum.grafo import csr_from_edges


def barabasi_albert(n, p3, rng):
    """Ligação preferencial. Cada novo vértice se liga a m_t vértices DISTINTOS, com m_t = 3 com
    probabilidade p3 e 2 caso contrário (grau médio 2*(2+p3), para casar com o nº de arestas do grafo
    real). A probabilidade de escolha é proporcional ao grau, via lista de extremidades de arestas.
    Começa com um triângulo. Devolve o CSR."""
    mt = (2 + (rng.random(n) < p3)).tolist()
    total = 3 + sum(mt[3:])
    rep = [0] * (2 * total)           # cada aresta (a,b) contribui com a e b: sorteio uniforme = ∝ grau
    rep[:6] = [0, 1, 0, 2, 1, 2]
    u, v = [0, 0, 1], [1, 2, 2]
    ptr = 6
    sorteios, c = rng.random(1 << 20).tolist(), 0
    for t in range(3, n):
        escolhidos = []
        while len(escolhidos) < mt[t]:
            if c == len(sorteios):
                sorteios, c = rng.random(1 << 20).tolist(), 0
            x = rep[int(sorteios[c] * ptr)]
            c += 1
            if x not in escolhidos:
                escolhidos.append(x)
        for x in escolhidos:
            u.append(t)
            v.append(x)
            rep[ptr] = t
            rep[ptr + 1] = x
            ptr += 2
    return csr_from_edges(n, np.array(u, dtype=np.int64), np.array(v, dtype=np.int64))


def watts_strogatz(n, k, p, rng):
    """Anel regular com k vizinhos (k/2 de cada lado); cada aresta tem a 2ª extremidade religada a um
    vértice uniforme com probabilidade p. Laços e duplicatas resultantes são removidos."""
    base = np.arange(n, dtype=np.int64)
    u = np.concatenate([base] * (k // 2))
    v = np.concatenate([(base + j) % n for j in range(1, k // 2 + 1)])
    re = rng.random(len(u)) < p
    v[re] = rng.integers(0, n, int(re.sum()))
    ok = u != v
    a, b = np.minimum(u[ok], v[ok]), np.maximum(u[ok], v[ok])
    chave = np.unique(a * n + b)
    return csr_from_edges(n, chave // n, chave % n)
