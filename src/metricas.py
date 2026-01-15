import pandas as pd


def calcular_metricas(df: pd.DataFrame) -> dict:
    metricas = {
        "linhas": len(df),
        "total_vendas": round(df["valor_total"].sum(), 2),
        "ticket_medio": round(df["valor_total"].mean(), 2),
    }

    metricas["top_produtos"] = (
        df.groupby("produto")["valor_total"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .to_dict()
    )

    return metricas


def formatar_metricas(metricas: dict) -> str:
    linhas = [
        "=== RESUMO DA EXECUÇÃO ===",
        f"Registros finais: {metricas['linhas']}",
        f"Total de vendas: R$ {metricas['total_vendas']:.2f}",
        f"Ticket médio: R$ {metricas['ticket_medio']:.2f}",
        "",
        "Top 5 Produtos:",
    ]

    for produto, valor in metricas["top_produtos"].items():
        linhas.append(f"- {produto}: R$ {valor:.2f}")

    return "\n".join(linhas)
