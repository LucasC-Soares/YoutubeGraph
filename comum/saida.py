"""Gravação de JSON/tabelas .tex, formatação numérica para LaTeX e acesso ao matplotlib."""
import json

import numpy as np


def salvar_json(pasta, nome: str, obj) -> None:
    with open(pasta / nome, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, default=float)


def salvar_tex(pasta, nome: str, texto: str) -> None:
    (pasta / nome).write_text(texto, encoding="utf-8")


def fmt(x, casas: int = 4) -> str:
    """Formata número para LaTeX (vírgula decimal, milhar com espaço fino)."""
    if isinstance(x, (int, np.integer)):
        return f"{int(x):,}".replace(",", "\\,")
    s = f"{float(x):.{casas}f}".replace(".", ",")
    return s


def plt():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as _plt
    return _plt
