import os
import geopandas as gpd


def obter_limite_municipio_vargem_alta():
    # Definir o caminho relativo
    caminho_municipios = os.path.join("..", "dados", "dados_baixados", "limites_municipios_ES.geojson")
    
    # Carregar os dados
    gdf_municipios = gpd.read_file(caminho_municipios)
    
    # Filtra o limite da cidade de Vargem Alta
    gdf_municipio_vargem_alta = gdf_municipios[gdf_municipios['nome'] == 'Vargem Alta']
    
    #salvar
    gdf_municipio_vargem_alta.to_file(os.path.join("..", "dados", "dados_tratados", "limite_municipio_vargem_alta.geojson"), driver='GeoJSON')
    print("Arquivo limite_municipio_vargem_alta.geojson criado.")


def obter_distritos_vargem_alta():
    # Definir o caminho relativo
    caminho = os.path.join("..", "dados", "dados_baixados", "distritos_ES.geojson")
    
    # Carregar os dados
    gdf = gpd.read_file(caminho)
    
    # Filtra o limite da cidade de Vargem Alta
    gdf = gdf[gdf['municipio'] == 'Vargem Alta']
    
    #salvar
    gdf.to_file(os.path.join("..", "dados", "dados_tratados", "distritos_vargem_alta.geojson"), driver='GeoJSON')
    print("Arquivo distritos_vargem_alta.geojson criado.")


def obter_bairros_vargem_alta():
    # Definir o caminho relativo
    caminho = os.path.join("..", "dados", "dados_baixados", "bairros_ES.geojson")
    
    # Carregar os dados
    gdf = gpd.read_file(caminho)
    
    # Filtra o limite da cidade de Vargem Alta
    gdf = gdf[gdf['municipio'] == 'Vargem Alta']
    
    #salvar
    gdf.to_file(os.path.join("..", "dados", "dados_tratados", "bairros_vargem_alta.geojson"), driver='GeoJSON')
    print("Arquivo bairros_vargem_alta.geojson criado.")



