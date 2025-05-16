🛰️ GeoNet Analyzer

Simulador e Analisador de Proximidade entre Unidades (Agências, Lojas, Pontos de Venda)

📖 Descrição

O GeoNet Analyzer é uma ferramenta Python que simula e analisa distâncias entre unidades geográficas (ex: agências bancárias, lojas, filiais).

Você pode:
- Gerar uma matriz simulada de distâncias entre N unidades.
- Filtrar quais unidades estão próximas de cada origem dentro de um limite de distância.
- Personalizar os nomes das colunas de entrada e saída.
- Garantir que todas as unidades sejam consideradas, mesmo as sem vizinhos próximos.

🛠️ Funcionalidades

✅ Geração de matriz simulada de distâncias com base em quantidade de unidades e distância máxima.

✅ Filtro de unidades próximas dentro de um raio personalizado (ex: até 5 km).

✅ Personalização de nomes de colunas.

✅ Compatível com Pandas DataFrames.

✅ Coberto por testes automatizados com pytest.

🚀 Instalação

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

🧑‍💻 Exemplo de Uso

```python
from distance_matrix_generator import gerar_base_exemplo, filtrar_agencias_proximas

# Gerar matriz simulada de 10 agências
df = gerar_base_exemplo(n_agencias=10, max_distancia_km=3000)

# Filtrar agências próximas até 500 km
resultado = filtrar_agencias_proximas(df, limite_km=500)

print(resultado)
```

✅ Testes

Os testes estão localizados em tests/test_agencias.py. Para rodar:

Rodar apenas uma categoria de teste: 

1. Geração de Base

```
pytest -m geracao_base
```

2. Filtro de Agências

```
pytest -m filtro_agencias
```

## 🗂️ Estrutura do Projeto

```text
📦 geonet_analyzer
 ┣ 📜 distance_matrix_generator.py
 ┣ 📂 tests
 ┃ ┗ 📜 test_agencias.py
 ┣ 📜 .gitignore
 ┣ 📜 README.md
 ┣ 📜 requirements.txt
```

📝 Licença

Este projeto é licenciado sob a MIT License. Consulte o arquivo LICENSE para mais informações.