# src/__init__.py
from exibicao.exibicao import roda_app
from utils import obtem_dados

def create_app():

    # Executa o script de download e tratamento de dados
    obtem_dados()
    
    # Retorna a função do app para rodar
    return roda_app
