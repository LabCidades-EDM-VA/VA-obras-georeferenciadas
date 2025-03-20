import os

def deploy_app():
    # Comando para realizar o deploy no shinyapps.io
    os.system("rsconnect deploy shiny ./ --name edm-vargem-alta --title va-obras-georreferenciadas")

deploy_app()