# app.py

from src import create_app

# Função principal para rodar o aplicativo
def main():
    # Cria o app usando a função create_app
    app = create_app()
    
    # Inicia o app
    app()

# Bloco principal
if __name__ == "__main__":
    main()
