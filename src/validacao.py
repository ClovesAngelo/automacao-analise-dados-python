from dataclasses import dataclass
import pandas as pd


@dataclass(frozen=True)
class ResultadoValidacao:
    ok: bool
    faltando: list[str]
    mensagem: str


def validar_colunas(df: pd.DataFrame, obrigatorias: list[str]) -> ResultadoValidacao:
    colunas_existentes = {c.strip().lower() for c in df.columns}
    obrigatorias_norm = [c.strip().lower() for c in obrigatorias]

    faltando = [c for c in obrigatorias_norm if c not in colunas_existentes]

    if faltando:
        return ResultadoValidacao(
            ok=False,
            faltando=faltando,
            mensagem=f"Faltam colunas obrigatórias: {', '.join(faltando)}",
        )

    return ResultadoValidacao(ok=True, faltando=[], mensagem="OK")
