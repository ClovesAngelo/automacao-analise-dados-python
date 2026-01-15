from pathlib import Path

import pandas as pd


def gerar_resumo(df: pd.DataFrame) -> pd.DataFrame:
    """
    Gera um resumo simples das vendas:
    - total vendido por produto
    - quantidade total por produto
    """
    resumo = (
        df.groupby("produto", as_index=False)
        .agg(
            total_vendas=("valor", "sum"),
            quantidade_total=("quantidade", "sum"),
        )
        .sort_values("total_vendas", ascending=False)
    )

    return resumo


def salvar_saidas(df_final, resumo, out_processed: Path, out_reports: Path, gerar_excel: bool = False):
    out_processed.mkdir(parents=True, exist_ok=True)
    out_reports.mkdir(parents=True, exist_ok=True)

    # 1) Dados finais tratados (padrão mundial)
    df_path = out_processed / "dados_tratados.csv"
    df_final.to_csv(df_path, index=False, encoding="utf-8")

    # 2) Versão compatível com Excel BR (opcional)
    if gerar_excel:
        df_excel_path = out_processed / "dados_tratados_excel.csv"
        df_final.to_csv(df_excel_path, index=False, sep=";", encoding="utf-8-sig")

    # 3) Resumo/relatório
    # Se resumo for DataFrame:
    try:
        resumo_path = out_reports / "resumo.csv"
        resumo.to_csv(resumo_path, index=False, encoding="utf-8")
        if gerar_excel:
            resumo_excel_path = out_reports / "resumo_excel.csv"
            resumo.to_csv(resumo_excel_path, index=False, sep=";", encoding="utf-8-sig")
    except AttributeError:
        # Se resumo não for DataFrame, salva como texto simples
        resumo_path = out_reports / "resumo.txt"
        resumo_path.write_text(str(resumo), encoding="utf-8")
