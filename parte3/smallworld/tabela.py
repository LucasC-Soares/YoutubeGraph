"""Tabela LaTeX do teste de small-world."""
from comum.saida import fmt, salvar_tex


def tabela(saida, pasta):
    real, rnd, teo = saida["real"], saida["aleatorio"], saida["teorico"]
    f = fmt
    linhas = [
        f"    $L$ (caminho médio) & {f(real['L'])} & {f(rnd['L'])} & {f(teo['L_rand_teorico'])} \\\\",
        f"    $C$ (clusterização média) & {f(real['C'], 6)} & {f(rnd['C'], 6)} & {f(teo['C_rand_teorico'], 6)} \\\\",
        f"    $L/L_{{rand}}$ & \\multicolumn{{3}}{{c}}{{{f(saida['razao_L'])}}} \\\\",
        f"    $C/C_{{rand}}$ & \\multicolumn{{3}}{{c}}{{{f(saida['razao_C'], 1)}}} \\\\",
        f"    $\\sigma=(C/C_{{rand}})/(L/L_{{rand}})$ & \\multicolumn{{3}}{{c}}{{{f(saida['sigma'], 1)}}} \\\\",
    ]
    salvar_tex(pasta, "tab_smallworld.tex",
               "\\begin{tabular}{lrrr}\n    \\toprule\n    Medida & Grafo real & $G(n,m)$ simulado & $G(n,m)$ teórico \\\\\n"
               "    \\midrule\n" + "\n".join(linhas) + "\n    \\bottomrule\n\\end{tabular}\n")
