"""Tabela LaTeX da robustez."""
from comum.saida import fmt, salvar_tex
from parte3.robustez.metricas import CHAVES

ROTULOS = {"A_S": "A: $S$", "B_componentes": "B: nº de componentes", "C_caminho_medio": "C: caminho médio",
           "C_diametro_lb": "C: diâmetro ($\\geq$)", "D_isolados": "D: fração de isolados"}


def tabela(base, resumo, cenarios, reps, pasta):
    f = fmt
    linhas = []
    for c in CHAVES:
        d = 4 if c in ("A_S", "D_isolados", "C_caminho_medio") else 0
        val = lambda x: f(x, d) if d else f(int(x))
        linhas.append(f"    {ROTULOS[c]} & {val(base[c])} & {val(resumo[c]['media'])} $\\pm$ {f(resumo[c]['desvio'], max(d, 2))} & "
                      f"{val(cenarios['grau'][c])} & {val(cenarios['PageRank'][c])} \\\\")
    salvar_tex(pasta, "tab_robustez.tex",
               "\\begin{tabular}{lrrrr}\n    \\toprule\n    Métrica & Original & Aleatória ($T=" + str(reps) +
               "$) & Ataque: grau & Ataque: PageRank \\\\\n    \\midrule\n" + "\n".join(linhas) +
               "\n    \\bottomrule\n\\end{tabular}\n")
