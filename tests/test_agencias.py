import sys
from pathlib import Path

import pandas as pd
import pytest

# Adiciona o caminho do diretório raiz ao sys.path dinamicamente
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from distance_matrix_generator import gerar_base_exemplo, filtrar_agencias_proximas

# ========================
# Testes do Gerador de Base
# ========================

@pytest.mark.geracao_base
def test_gerar_base_colunas_personalizadas():
    """
    Testa se a função gerar_base_exemplo retorna as colunas personalizadas corretamente.
    """
    df = gerar_base_exemplo(
        n_agencias=5,
        max_distancia_km=100,
        nome_col_origem="origem",
        nome_col_destino="destino",
        nome_col_distancia="km",
    )
    assert set(df.columns) == {"origem", "destino", "km"}
    assert len(df) == 25


@pytest.mark.geracao_base
def test_gerar_base_distancia_zero_para_mesma_agencia():
    """
    Testa se a distância entre uma agência e ela mesma é zero.
    """
    df = gerar_base_exemplo(n_agencias=3, max_distancia_km=100)
    zeros = df[df["agencia_origem"] == df["agencia_destino"]]["distancia_km"]
    assert all(zeros == 0)


# ================================
# Testes do Filtro de Agências Próximas
# ================================

@pytest.mark.filtro_agencias
def test_filtrar_agencias_proximas_funciona_com_base_valida():
    """
    Testa o filtro com uma base válida, verificando se as colunas de saída e as quantidades estão corretas.
    """
    data = {
        "agencia_origem": [1, 1, 2, 2],
        "agencia_destino": [2, 3, 1, 3],
        "distancia_km": [4, 6, 3, 7],
    }
    df = pd.DataFrame(data)
    resultado = filtrar_agencias_proximas(df, limite_km=5)

    assert "agencia_origem" in resultado.columns
    assert "agencias_proximas" in resultado.columns
    assert "quantidade" in resultado.columns
    assert resultado.loc[resultado["agencia_origem"] == 1, "quantidade"].values[0] == 1
    assert resultado.loc[resultado["agencia_origem"] == 2, "quantidade"].values[0] == 1


@pytest.mark.filtro_agencias
def test_filtrar_agencias_proximas_colunas_personalizadas():
    """
    Testa o filtro com nomes personalizados de colunas, verificando se a saída é consistente.
    """
    data = {"origem": [1, 1, 2, 2], "destino": [2, 3, 1, 3], "km": [4, 6, 3, 7]}
    df = pd.DataFrame(data)
    resultado = filtrar_agencias_proximas(
        df,
        limite_km=5,
        nome_col_origem="origem",
        nome_col_destino="destino",
        nome_col_distancia="km",
        nome_col_proximas="proximas",
        nome_col_quantidade="total",
    )

    assert "origem" in resultado.columns
    assert "proximas" in resultado.columns
    assert "total" in resultado.columns


@pytest.mark.filtro_agencias
def test_filtrar_agencias_proximas_com_coluna_ausente():
    """
    Testa o comportamento quando o DataFrame não possui a coluna de distância esperada.
    Deve levantar uma exceção ValueError.
    """
    data = {
        "origem": [1, 1],
        "destino": [2, 3],
        # coluna 'km' ausente propositalmente
    }
    df = pd.DataFrame(data)
    with pytest.raises(ValueError) as excinfo:
        filtrar_agencias_proximas(
            df,
            5,
            nome_col_origem="origem",
            nome_col_destino="destino",
            nome_col_distancia="km",
        )
    assert "Colunas ausentes" in str(excinfo.value)