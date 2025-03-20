from coleta.download_dados import *
from tratamento.tratamento import *
from processamento.processamento import *
from utils import download_planilhas_obras_google_sheets

def ask_for_download():
    while True:
        answer = input("Deseja fazer o download dos dados? (sim/nao): ").lower()
        if answer == 'sim':
            return True
        elif answer == 'nao':
            return False
        else:
            print("Por favor, responda com 'sim' ou 'não'.")


def ask_for_tratamento():
    while True:
        answer = input("Deseja fazer o tratamento dos dados? (sim/nao): ").lower()
        if answer == 'sim':
            return True
        elif answer == 'nao':
            return False
        else:
            print("Por favor, responda com 'sim' ou 'não'.")


def ask_for_process():
    while True:
        answer = input("Deseja fazer o processamento dos dados? (sim/nao): ").lower()
        if answer == 'sim':
            return True
        if answer == 'nao':
            return False
        else:
            print("Por favor, responda com 'sim' ou 'não'.")


def main():
    print("Iniciando...")

    # Baixa planilhas direto do google sheets
    download_planilhas_obras_google_sheets()

    if ask_for_download():
        print("Iniciando downloads...")
        
        download_limites_municipios()
        download_distritos_ES()
        download_bairros_ES()
    else:
        print("Download ignorado.")

    if ask_for_tratamento():
        print("Iniciando tratamento dos dados...")

        obter_limite_municipio_vargem_alta()
        obter_distritos_vargem_alta()
        obter_bairros_vargem_alta()
    else:
        print("Tratamento dos dados ignorado.")

    if ask_for_process():
        print("Iniciando processamento dos dados...")

        obter_gdf_contratos()
        obter_percentual_pagamento_contratos()
        obter_empenhos_liquidacoes()
    else:
        print("Processamento ignorado.")

# Bloco principal
if __name__ == "__main__":
    main()