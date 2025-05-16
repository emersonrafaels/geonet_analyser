from itertools import product
import pandas as pd
import numpy as np
from loguru import logger


def gerar_base_exemplo(
    n_agencias=10,
    max_distancia_km=3000,
    seed=42,
    nome_col_origem="agencia_origem",
    nome_col_destino="agencia_destino",
    nome_col_distancia="distancia_km",
):
    """
    Gera uma base simulada de distâncias entre agências.

    Parameters:
    - n_agencias: Quantidade de agências a simular (default 10)
    - max_distancia_km: Distância máxima aleatória simulada (default 3000 km)
    - seed: Semente para reprodutibilidade (default 42)
    - nome_col_origem: Nome da coluna de origem
    - nome_col_destino: Nome da coluna de destino
    - nome_col_distancia: Nome da coluna de distância

    Return:
    - DataFrame com as colunas personalizadas
    """
    np.random.seed(seed)
    agencias = list(range(1, n_agencias + 1))

    dados = []
    for origem, destino in product(agencias, repeat=2):
        distancia = np.random.uniform(1, max_distancia_km) if origem != destino else 0
        dados.append(
            {
                nome_col_origem: origem,
                nome_col_destino: destino,
                nome_col_distancia: round(distancia, 2),
            }
        )

    return pd.DataFrame(dados)


def filtrar_agencias_proximas(
    df,
    limite_km,
    nome_col_origem="agencia_origem",
    nome_col_destino="agencia_destino",
    nome_col_distancia="distancia_km",
    nome_col_proximas="agencias_proximas",
    nome_col_quantidade="quantidade",
):
    """
    Filtra agências dentro de um limite de distância por origem,
    garantindo que todas as origens estejam presentes, mesmo sem matches.

    Parameters:
    - df: DataFrame com as colunas de origem, destino e distância
    - limite_km: Limite de distância (em km) para filtrar
    - nome_col_origem: Nome da coluna de origem
    - nome_col_destino: Nome da coluna de destino
    - nome_col_distancia: Nome da coluna de distância
    - nome_col_proximas: Nome da coluna de agências próximas no resultado
    - nome_col_quantidade: Nome da coluna de quantidade no resultado

    Return:
    - DataFrame com colunas personalizadas
    """
    # Validação de colunas obrigatórias
    colunas_necessarias = {nome_col_origem, nome_col_destino, nome_col_distancia}
    colunas_ausentes = colunas_necessarias - set(df.columns)
    if colunas_ausentes:
        raise ValueError(
            f"Colunas ausentes no DataFrame: {', '.join(colunas_ausentes)}"
        )

    # Seleciona apenas as colunas relevantes
    df_reduzido = df[[nome_col_origem, nome_col_destino, nome_col_distancia]]

    # Lista completa de origens
    origens = df_reduzido[nome_col_origem].unique()

    # Filtra pela distância limite
    filtrado = df_reduzido[df_reduzido[nome_col_distancia] <= limite_km]

    # Agrupa por origem e agrega as agências destino em lista e conta a quantidade
    resultado = (
        filtrado.groupby(nome_col_origem)
        .agg(
            agencias_proximas=(nome_col_destino, lambda x: list(x)),
            quantidade=(nome_col_destino, "nunique"),
        )
        .reindex(origens, fill_value=pd.NA)
        .reset_index()
    )

    # Preenche os campos vazios com lista vazia e zero
    resultado["agencias_proximas"] = resultado["agencias_proximas"].apply(
        lambda x: x if isinstance(x, list) else []
    )
    resultado["quantidade"] = resultado["quantidade"].fillna(0).astype(int)

    # Renomeia as colunas conforme solicitado
    resultado = resultado.rename(
        columns={
            nome_col_origem: nome_col_origem,
            "agencias_proximas": nome_col_proximas,
            "quantidade": nome_col_quantidade,
        }
    )

    return resultado
