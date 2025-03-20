# app.py

from app import create_app

# Cria o app e expõe-o para o deploy
app = create_app()

if __name__ == "__main__":
    # Para testes locais, inicia o app.
    # OBS.: app.run() (ou app()) internamente chama uvicorn.run, que usa asyncio.run,
    # o que pode dar erro se já houver um loop de eventos. Para testes locais, isso normalmente funciona.
    app.run()
