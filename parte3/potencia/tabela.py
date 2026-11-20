"""Tabela LaTeX do ajuste de lei de potência."""
from comum.saida import fmt, salvar_tex


def tabela(ols, melhor, pasta):
    f = fmt
    linhas = [f"    Regressão log-log da CCDF ($k\\geq {ols['k_min_regressao']}$) & $\\gamma={f(ols['gamma'], 2)}$ "
              f"& $R^2={f(ols['r2'], 3)}$ \\\\"]
    if melhor:
        linhas.append(f"    MLE (Clauset et al.), $k_{{min}}={melhor['kmin']}$ & $\\gamma={f(melhor['gamma'], 2)}"
                      f"\\pm{f(melhor['erro_padrao'], 3)}$ & KS$={f(melhor['ks'], 3)}$ \\\\")
    salvar_tex(pasta, "tab_potencia.tex",
               "\\begin{tabular}{lll}\n    \\toprule\n    Método & Expoente & Qualidade \\\\\n    \\midrule\n"
               + "\n".join(linhas) + "\n    \\bottomrule\n\\end{tabular}\n")
