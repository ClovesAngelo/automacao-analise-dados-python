from pathlib import Path
import argparse
import sys
import pandas as pd

from src.leitura import ler_csv
from src.validacao import validar_colunas
from src.tratamento import tratar_dados
from src.relatorio import gerar_resumo, salvar_saidas
from src.metricas import calcular_metricas, formatar_metricas


COLUNAS_OBRIGATORIAS = ["nome", "produto", "valor", "quantidade", "data_compra"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--outdir", default="data")
    args = parser.parse_args()

    entrada = Path(args.input)
    saida = Path(args.outdir)

    if not entrada.exists():
        print("Arquivo não encontrado")
        sys.exit(1)

    arquivos = [entrada] if entrada.is_file() else list(entrada.glob("*.csv"))

    frames = []

    for arquivo in arquivos:
        df = ler_csv(arquivo)
        validacao = validar_colunas(df, COLUNAS_OBRIGATORIAS)

        if not validacao.ok:
            print(f"Ignorado {arquivo.name}: {validacao.mensagem}")
            continue

        df_tratado = tratar_dados(df)
        df_tratado["arquivo_origem"] = arquivo.name
        frames.append(df_tratado)

    if not frames:
        print("Nenhum dado válido encontrado.")
        return

    df_final = pd.concat(frames)
    resumo = gerar_resumo(df_final)
    metricas = calcular_metricas(df_final)

    print(formatar_metricas(metricas))
    salvar_saidas(df_final, resumo, saida)


if __name__ == "__main__":
    main()
