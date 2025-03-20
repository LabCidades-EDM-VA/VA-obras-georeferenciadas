# src/__init__.py

import subprocess
from src.exibicao.exibicao import roda_app

def create_app():
    # Executa o comando "python src/main.py < input.txt" para baixar os dados necessários antes de iniciar o app
    subprocess.run("python src/main.py < input.txt", shell=True)
    
    # Retorna a função do app para rodar
    return roda_app
