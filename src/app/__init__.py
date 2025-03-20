# src/__init__.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../exibicao')))
from exibicao import roda_app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from utils import obtem_dados

def create_app():

    # Executa o script de download e tratamento de dados
    obtem_dados()
    
    # Retorna a função do app para rodar
    return roda_app()
