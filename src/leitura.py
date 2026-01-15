from pathlib import Path
import pandas as pd


def ler_csv(caminho: str | Path) -> pd.DataFrame:
    caminho = Path(caminho)
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    try:
        return pd.read_csv(caminho, encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv(caminho, encoding="latin-1")
