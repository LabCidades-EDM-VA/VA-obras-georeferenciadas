from src.exibicao.exibicao import roda_app
import subprocess

# A função que a plataforma Shiny espera
def app():
    # Executa o comando "python ../main.py < input.txt" para baixar os dados necessários antes de iniciar o app
    subprocess.run("python src/main.py < input.txt", shell=True)
    
    return roda_app()

# Não é necessário o bloco if __name__ == "__main__" no app Shiny
