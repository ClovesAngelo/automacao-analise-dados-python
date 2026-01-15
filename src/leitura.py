from pathlib import Path
import pandas as pd


def ler_csv(caminho: Path) -> pd.DataFrame:
    tentativas = [
        {"sep": ",", "encoding": "utf-8"},
        {"sep": ";", "encoding": "utf-8"},
        {"sep": ",", "encoding": "utf-8-sig"},
        {"sep": ";", "encoding": "utf-8-sig"},
    ]

    ultimo_erro = None

    for cfg in tentativas:
        try:
            return pd.read_csv(
                caminho,
                sep=cfg["sep"],
                encoding=cfg["encoding"],
            )
        except Exception as e:
            ultimo_erro = e

    # Fallback mais tolerante (lida melhor com CSV "sujo")
    try:
        return pd.read_csv(
            caminho,
            sep=None,              # tenta detectar separador
            engine="python",       # parser mais tolerante
            encoding="utf-8-sig",
            on_bad_lines="skip",   # pula linhas quebradas
        )
    except Exception as e:
        raise RuntimeError(
            f"Falha ao ler CSV: {caminho}\n"
            f"Erro original: {ultimo_erro}\n"
            f"Erro final: {e}"
        )
