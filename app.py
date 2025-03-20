from src.exibicao.exibicao import roda_app
import subprocess

def main():
    # Executa o comando "python ../main.py < input.txt" para baixar os dados necessários antes de iniciar o app
    subprocess.run("python src/main.py < input.txt", shell=True)
    
    roda_app()

# Bloco principal
if __name__ == "__main__":
    main()