# app.py
from src.app import create_app  # ajuste o caminho conforme sua estrutura

# Cria o app e o expõe para o deploy
app = create_app()

if __name__ == "__main__":
    # Execução local para testes: inicia o app
    app.run()
