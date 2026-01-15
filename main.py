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


def parse_args():
    parser = argparse.ArgumentParser(
        description="Pipeline de processamento de CSVs: valida, trata, calcula métricas e gera saídas."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Arquivo CSV ou pasta contendo CSVs (ex.: data/raw ou data/raw/vendas.csv)",
    )

    parser.add_argument(
        "--outdir",
        default="data",
        help="Diretório base de saída. Dentro dele serão criadas pastas processed/ e reports/ (default: data)",
    )

    parser.add_argument(
        "--pattern",
        default="*.csv",
        help="Padrão de busca quando --input for pasta (default: *.csv)",
    )

    parser.add_argument(
        "--excel",
        action="store_true",
        help="Também gera CSV compatível com Excel PT-BR (sep=';' e encoding utf-8-sig).",
    )

    return parser.parse_args()


def coletar_arquivos(entrada: Path, pattern: str) -> list[Path]:
    if entrada.is_file():
        return [entrada]
    return sorted(list(entrada.glob(pattern)))


def main():
    args = parse_args()

    entrada = Path(args.input)
    outbase = Path(args.outdir)

    # Estrutura padrão
    saida_processed = outbase / "processed"
    saida_reports = outbase / "reports"

    # Cria diretórios automaticamente
    saida_processed.mkdir(parents=True, exist_ok=True)
    saida_reports.mkdir(parents=True, exist_ok=True)

    if not entrada.exists():
        print(f"Arquivo ou pasta não encontrado: {entrada}")
        sys.exit(1)

    arquivos = coletar_arquivos(entrada, args.pattern)

    if not arquivos:
        print(f"Nenhum arquivo encontrado em: {entrada} (pattern={args.pattern})")
        sys.exit(1)

    frames = []
    ignorados = 0

    for arquivo in arquivos:
        df = ler_csv(arquivo)
        validacao = validar_colunas(df, COLUNAS_OBRIGATORIAS)

        if not validacao.ok:
            ignorados += 1
            print(f"Ignorado {arquivo.name}: {validacao.mensagem}")
            continue

        df_tratado = tratar_dados(df)
        df_tratado["arquivo_origem"] = arquivo.name
        frames.append(df_tratado)

    if not frames:
        print("Nenhum dado válido encontrado após validação.")
        print(f"Arquivos analisados: {len(arquivos)} | Ignorados: {ignorados}")
        return

    df_final = pd.concat(frames, ignore_index=True)

    resumo = gerar_resumo(df_final)
    metricas = calcular_metricas(df_final)

    print(formatar_metricas(metricas))

    # Aqui a gente passa o local de saída de forma organizada:
    # processed: dados tratados
    # reports: resumos/métricas
    salvar_saidas(
        df_final=df_final,
        resumo=resumo,
        out_processed=saida_processed,
        out_reports=saida_reports,
        gerar_excel=args.excel
    )

    print("\nConcluído ✅")
    print(f"Arquivos analisados: {len(arquivos)} | Ignorados: {ignorados}")
    print(f"Saídas em:\n- {saida_processed}\n- {saida_reports}")


if __name__ == "__main__":
    main()
