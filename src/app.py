# app.py

from app import create_app  # Certifique-se de que o caminho está correto

# Cria o app e o expõe como variável global
app = create_app()

if __name__ == "__main__":
    # Para testes locais, podemos iniciar o servidor ASGI
    from asgiref.wsgi import WsgiToAsgi
    import uvicorn
    uvicorn.run(WsgiToAsgi(app), host="127.0.0.1", port=8000)
