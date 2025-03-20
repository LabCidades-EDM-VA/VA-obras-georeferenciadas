import os
import requests
import geopandas as gpd
from urllib.parse import urlencode
import requests
import gzip
import shutil

def download_limites_municipios():
    # URL base do serviço WFS
    base_url = "https://ide.geobases.es.gov.br/geoserver/ows"

    # Definir os parâmetros WFS para a requisição
    params = {
        "service": "WFS",
        "version": "2.0.0",
        "request": "GetFeature",
        "typename": "geonode:idaf_limite_municipal_2018_11",  # Ajustar conforme necessário
        "outputFormat": "application/json"  # Usando GeoJSON como formato de saída
    }

    # Construir a URL completa para a requisição
    url = f"{base_url}?{urlencode(params)}"

    print("Baixando arquivo limites_municipios_ES.geojson")
    # Realizar a requisição para o servidor WFS
    response = requests.get(url)

    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Criar o diretório "data" se não existir
        #os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)

        caminho_arquivo = os.path.join("..", "dados", "dados_baixados", "limites_municipios_ES.geojson")
        
         # Salvar o resultado GeoJSON no arquivo
        total_tamanho = int(response.headers.get('content-length', 0))  # Tamanho total do arquivo
        tamanho_downloaded = 0

        with open(caminho_arquivo, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                tamanho_downloaded += len(chunk)
                progresso = (tamanho_downloaded / total_tamanho) * 100 if total_tamanho > 0 else 100
                print(f"Progresso do download: {progresso:.2f}%", end='\r')  # Atualiza a mesma linha

        print("\nArquivo limites_municipios_ES.geojson salvo.")
    else:
        print(f"Falha ao baixar os dados WFS. Status code: {response.status_code}")


def download_distritos_ES():
    # URL base do serviço WFS
    base_url = "https://ide.geobases.es.gov.br/geoserver/ows"

    # Definir os parâmetros WFS para a requisição
    params = {
        "service": "WFS",
        "version": "2.0.0",
        "request": "GetFeature",
        "typename": "geonode:limite_distrital_2018_alt_novembro",  # Ajustar conforme necessário
        "outputFormat": "application/json"  # Usando GeoJSON como formato de saída
    }

    # Construir a URL completa para a requisição
    url = f"{base_url}?{urlencode(params)}"

    print("Baixando arquivo distritos_ES.geojson ...")
    # Realizar a requisição para o servidor WFS
    response = requests.get(url)

    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Definir o caminho do arquivo para salvar
        caminho_arquivo = os.path.join("..", "dados", "dados_baixados", "distritos_ES.geojson")

        # Salvar o resultado GeoJSON no arquivo
        total_tamanho = int(response.headers.get('content-length', 0))  # Tamanho total do arquivo
        tamanho_downloaded = 0

        with open(caminho_arquivo, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                tamanho_downloaded += len(chunk)
                progresso = (tamanho_downloaded / total_tamanho) * 100 if total_tamanho > 0 else 100
                print(f"Progresso do download: {progresso:.2f}%", end='\r')  # Atualiza a mesma linha

        print("\nArquivo distritos_ES.geojson salvo.")
    else:
        print(f"Falha ao baixar os dados WFS. Status code: {response.status_code}")


def download_bairros_ES():
    # URL base do serviço WFS
    base_url = "https://ide.geobases.es.gov.br/geoserver/ows"

    # Definir os parâmetros WFS para a requisição
    params = {
        "service": "WFS",
        "version": "2.0.0",
        "request": "GetFeature",
        "typename": "geonode:ijsn_limite_bairro_2020_UTF8",  # Ajustar conforme necessário
        "outputFormat": "application/json"  # Usando GeoJSON como formato de saída
    }

    # Construir a URL completa para a requisição
    url = f"{base_url}?{urlencode(params)}"

    print("Baixando arquivo distritos_ES.geojson ...")
    # Realizar a requisição para o servidor WFS
    response = requests.get(url)

    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Definir o caminho do arquivo para salvar
        caminho_arquivo = os.path.join("..", "dados", "dados_baixados", "bairros_ES.geojson")

        # Salvar o resultado GeoJSON no arquivo
        total_tamanho = int(response.headers.get('content-length', 0))  # Tamanho total do arquivo
        tamanho_downloaded = 0

        with open(caminho_arquivo, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                tamanho_downloaded += len(chunk)
                progresso = (tamanho_downloaded / total_tamanho) * 100 if total_tamanho > 0 else 100
                print(f"Progresso do download: {progresso:.2f}%", end='\r')  # Atualiza a mesma linha

        print("\nArquivo bairros_ES.geojson salvo.")
    else:
        print(f"Falha ao baixar os dados WFS. Status code: {response.status_code}")
