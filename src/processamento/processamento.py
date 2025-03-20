import os
import geopandas as gpd
import osmnx as ox
import networkx as nx
from shapely.geometry import LineString
import math
import pandas as pd
from shapely.geometry import Point
import pandas as pd
import geopandas as gpd
import os


def obter_gdf_contratos():
    # Definir o caminho relativo
    caminho = os.path.join("..", "dados", "dados_baixados", "contratos_etapa4_v4.csv")

    # Carregar os dados
    df = pd.read_csv(caminho)

    def parse_coord(coord):
        # Verifica se a string é válida
        if not coord or coord.strip() == "" or coord.lower() == "nan":
            print(f"Coordenada inválida ou vazia: {coord}")
            return None
        
        # Remove espaços desnecessários e faz o split
        partes = [parte.strip() for parte in coord.split(',')]
        
        # Verifica se temos pelo menos dois elementos
        if len(partes) < 2:
            print(f"Coordenada com formato inesperado: {coord}")
            return None
        
        try:
            # Converter as partes para float; 
            # ajuste a ordem se necessário (aqui, assumindo que o formato é "latitude,longitude")
            lat, lon = map(float, partes[:2])
            # Caso precise inverter (por exemplo, se o shapely espera (lon, lat)):
            return Point(lon, lat)
        except Exception as e:
            print(f"Erro ao converter '{coord}': {e}")
            return None

    # Aplicando a função na coluna
    df['coordenadaGeografica'] = df['coordenadaGeografica'].astype(str)
    df['geometry'] = df['coordenadaGeografica'].apply(parse_coord)

    # Criar um GeoDataFrame com o CRS EPSG:4326 (WGS 84)
    gdf = gpd.GeoDataFrame(df, geometry=df['geometry'], crs="EPSG:4326")

    # Salva o arquivo
    gdf.to_file(os.path.join("..", "dados", "dados_processados", "contratos.geojson"), driver='GeoJSON')
    print("Contratos criados.")


def obter_percentual_pagamento_contratos():
    # Definir o caminho relativo
    caminho_contratos = os.path.join("..", "dados", "dados_processados", "contratos.geojson")
    caminho = os.path.join("..", "dados", "dados_baixados", "liquidacoes.csv")

    # Carregar os dados
    gdf_contratos = gpd.read_file(caminho_contratos)
    df = pd.read_csv(caminho, sep=';', encoding='latin1')

    print("Antes da limpeza:")
    print(df[["Valor"]].head())

    # Ajustar o formato de valores no CSV
    # Vamos garantir que todas as transformações sejam feitas corretamente na string
    df["Valor"] = df["Valor"].str.replace(r"R\$", "", regex=True)  # Remover "R$"
    df["Valor"] = df["Valor"].str.replace(r"\.", "", regex=True)   # Remover separadores de milhar
    df["Valor"] = df["Valor"].str.replace(r",", ".", regex=True)    # Substituir vírgula decimal por ponto

    print("Após ajustes de formato de valores:")
    print(df[["Valor"]].head())

    # Tratar valores inválidos ou vazios antes da conversão para float
    # Agora, vamos forçar a conversão para float, substituindo qualquer valor inválido por NaN
    df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")

    print("Após conversão para numérico:")
    print(df[["Valor"]].head())

    # Preencher NaN com 0
    df["Valor"] = df["Valor"].fillna(0)  # Preencher NaN com 0

    print("Após preencher NaN com 0:")
    print(df[["Valor"]].head())

    print(df["Processo"].head())

    # Remover apenas um zero à esquerda de "numeroProcesso"
    df['Processo'] = df['Processo'].str.replace(r"^0", "", regex=True)

    print(df[["Processo", "Valor"]].head(30))

    # Ajustar nomes de colunas para correspondência
    df.rename(columns={"Processo": "numeroProcesso", "Valor": "valorPago"}, inplace=True)

    # Calcular o totalPago para cada processo
    pagamentos_por_processo = df.groupby("numeroProcesso")["valorPago"].sum().reset_index()
    pagamentos_por_processo.rename(columns={"valorPago": "totalPago"}, inplace=True)

    # Mesclar totalPago com gdf_contratos
    gdf_contratos = gdf_contratos.merge(
        pagamentos_por_processo, 
        on="numeroProcesso", 
        how="left"
    )

    # Preencher valores NaN (se algum processo de gdf_contratos não estiver em df)
    gdf_contratos["totalPago"] = gdf_contratos["totalPago"].fillna(0)

    # Calcular percentualTotalPago
    gdf_contratos["percentualTotalPago"] = (gdf_contratos["totalPago"] / gdf_contratos["valor"]) * 100

    # Visualizar o resultado
    print("Resultado final após cálculos:")
    print(gdf_contratos[["numeroProcesso", "valor", "totalPago", "percentualTotalPago"]].head(30))

    #salva o arquivo
    gdf_contratos.to_file(os.path.join("..", "dados", "dados_processados", "contratos.geojson"), driver='GeoJSON')
    print("Contratos criados.")
    print(gdf_contratos['percentualTotalPago'].max())


def obter_empenhos_liquidacoes():
    # Definir o caminho relativo
    caminho_contratos = os.path.join("..", "dados", "dados_processados", "contratos.geojson")
    caminho_liquidacoes = os.path.join("..", "dados", "dados_baixados", "liquidacoes.csv")
    caminho_empenhos = os.path.join("..", "dados", "dados_baixados", "empenhos.csv")

    # Carregar os dados
    gdf_contratos = gpd.read_file(caminho_contratos)
    df_liquidacoes = pd.read_csv(caminho_liquidacoes, sep=';', encoding='utf-8')
    df_empenhos = pd.read_csv(caminho_empenhos, sep=';', encoding='utf-8')

    # 📌 Ajustar nomes de colunas problemáticas em liquidações (caso necessário)
    df_liquidacoes.columns = df_liquidacoes.columns.str.replace("Liquida��o", "Liquidacao", regex=True)

    # Remover apenas um zero à esquerda de "numeroProcesso"
    df_empenhos['processo'] = df_empenhos['processo'].str.replace(r"^0", "", regex=True)

    # 📌 Criar a estrutura de dados aninhada
    def obter_empenhos_por_contrato(numero_processo):
        """Retorna uma lista de empenhos associados a um contrato"""
        empenhos = df_empenhos[df_empenhos["processo"] == numero_processo].to_dict(orient="records")
        
        # Para cada empenho, adicionar suas liquidações
        for empenho in empenhos:
            empenho["liquidacoes"] = df_liquidacoes[df_liquidacoes["Empenho"] == empenho["empenho"]].to_dict(orient="records")
        
        return empenhos

    # Criar a nova coluna "empenhos" dentro do GeoDataFrame de contratos
    gdf_contratos["empenhos"] = gdf_contratos["numeroProcesso"].apply(obter_empenhos_por_contrato)

    pd.set_option("display.max_colwidth", None)

    # 🔍 Verificar um exemplo
    #print(gdf_contratos[["numeroProcesso", "empenhos"]].head())

    import json

    # Converter a coluna "empenhos" para JSON string
    #gdf_contratos["empenhos"] = gdf_contratos["empenhos"].apply(json.dumps)

    #salva o arquivo
    #gdf_contratos.to_file(os.path.join("..", "dados", "dados_processados", "contratos_teste.geojson"), driver='GeoJSON')

    gdf_contratos.to_parquet(os.path.join("..", "dados", "dados_processados", "contratos.parquet"), index=False)

    g = gpd.read_parquet(os.path.join("..", "dados", "dados_processados", "contratos.parquet"))

    print(g[["numeroProcesso", "empenhos"]].head())

    g.to_csv(os.path.join("..", "dados", "dados_processados", "contratos_parquet_csv.csv"), index=False)

    # output_path = os.path.join("..", "dados", "dados_processados", "contratos_parquet_json.json")
    # g.to_json(output_path, orient="records", lines=True)
