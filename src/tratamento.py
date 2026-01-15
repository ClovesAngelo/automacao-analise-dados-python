import pandas as pd


def tratar_dados(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]

    textos = ["nome", "produto", "categoria", "cidade", "estado", "forma_pagamento"]
    for col in textos:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype("string")
                .str.strip()
                .str.lower()
                .str.title()
            )

    if "valor" in df.columns:
        df["valor"] = pd.to_numeric(df["valor"], errors="coerce")

    if "quantidade" in df.columns:
        df["quantidade"] = pd.to_numeric(df["quantidade"], errors="coerce")

    if "data_compra" in df.columns:
        df["data_compra"] = pd.to_datetime(df["data_compra"], errors="coerce")

    df = df.dropna(subset=["nome", "produto", "valor", "quantidade", "data_compra"])
    df = df[df["quantidade"] >= 1]

    df["valor_total"] = df["valor"] * df["quantidade"]
    df["mes_compra"] = df["data_compra"].dt.to_period("M").astype(str)

    return df
