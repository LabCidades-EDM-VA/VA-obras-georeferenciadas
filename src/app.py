# app.py

# Função principal para rodar o aplicativo
from app import create_app

def main():
    # Cria o app usando a função create_app
    app = create_app()
    
    # Inicia o app
    app()

# Bloco principal
if __name__ == "__main__":
    main()
