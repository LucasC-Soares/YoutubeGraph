"""Tabela LaTeX: grafo real x modelos clássicos."""
from comum.saida import fmt, salvar_tex


def _c(x):
    """Clusterização: notação científica quando muito pequena."""
    if 0 < x < 1e-3:
        mant, exp = f"{x:.1e}".split("e")
        return f"\\ensuremath{{{mant.replace('.', '{,}')}\\times10^{{{int(exp)}}}}}"
    return fmt(x)


def tabela(linhas_dados, pasta):
    linhas = []
    for nome, d in linhas_dados.items():
        mle = d["mle"]
        g = f"{fmt(mle['gamma'], 2)} ({fmt(mle['ks'], 2)})" if mle else "---"
        linhas.append(f"    {nome} & {fmt(d['k_medio'], 2)} & {fmt(d['grau_max'])} & {_c(d['C'])} & "
                      f"{fmt(d['L'], 2)} & {d['diam_lb']} & {g} \\\\")
    salvar_tex(pasta, "tab_modelos.tex",
               "\\begin{tabular}{lrrrrrr}\n    \\toprule\n"
               "    Grafo & $\\langle k\\rangle$ & $k_{max}$ & $C$ & $L$ & Diâm.\\ ($\\geq$) & $\\gamma$ (KS) \\\\\n"
               "    \\midrule\n" + "\n".join(linhas) + "\n    \\bottomrule\n\\end{tabular}\n")
