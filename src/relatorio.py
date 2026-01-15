from pathlib import Path
import pandas as pd


def gerar_resumo(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["categoria", "forma_pagamento"], dropna=False)
        .agg(
            total_vendas=("valor_total", "sum"),
            quantidade=("quantidade", "sum"),
            ticket_medio=("valor_total", "mean"),
        )
        .reset_index()
    )


def salvar_saidas(df: pd.DataFrame, resumo: pd.DataFrame, pasta_saida: str | Path):
    pasta = Path(pasta_saida)
    pasta.mkdir(parents=True, exist_ok=True)

    csv_path = pasta / "saida_tratada.csv"
    excel_path = pasta / "relatorio.xlsx"

    df.to_csv(csv_path, index=False)

    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="dados_tratados", index=False)
        resumo.to_excel(writer, sheet_name="resumo", index=False)

    return csv_path, excel_path
