import os
import csv
import gspread
from config import Config

def download_planilhas_obras_google_sheets():
    # Diretório para salvar os arquivos CSV
    output_path = os.path.join("..", "dados", "dados_baixados")
    os.makedirs(output_path, exist_ok=True)

    # Define os dados das planilhas: ID, nome (para log), arquivo de saída e delimitador
    sheets_info = [
        {
            "sheet_id": "1e9Eyk3qpREyBCHq2utwwZFNNbG4PmsxwQzQzUA_giEE",
            "sheet_name": "contratos_etapa4_v4",
            "output_file": os.path.join(output_path, "contratos_etapa4_v4.csv"),
            "delimiter": ","  # Essa planilha será salva com vírgula
        },
        {
            "sheet_id": "1qSNk9TKVifmzWEFlGZVnUVV-hf-CZsALdrIiam1-tqQ",
            "sheet_name": "empenhos",
            "output_file": os.path.join(output_path, "empenhos.csv"),
            "delimiter": ";"  # As demais serão salvas com ponto e vírgula
        },
        {
            "sheet_id": "1GNm2zeCm6XSd-hS5NPQs_EJCfp2hy_lmpsi_TVqc_lM",
            "sheet_name": "liquidacoes",
            "output_file": os.path.join(output_path, "liquidacoes.csv"),
            "delimiter": ";"
        }
    ]

    # Autenticação com a conta de serviço
    service_account_info = {
        "type": "service_account",
        "project_id": Config.SERVICE_ACCOUNT_PROJECT_ID,
        "private_key_id": Config.SERVICE_ACCOUNT_PRIVATE_KEY_ID,
        "private_key": str(Config.SERVICE_ACCOUNT_PRIVATE_KEY).replace('\\n', '\n'),
        "client_email": Config.SERVICE_ACCOUNT_CLIENT_EMAIL,
        "client_id": Config.SERVICE_ACCOUNT_CLIENT_ID,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": Config.SERVICE_ACCOUNT_CLIENT_CERT_URL
    }
    client = gspread.service_account_from_dict(service_account_info)

    # Função para baixar uma planilha e salvar em CSV com delimitador específico
    def download_google_sheet_para_csv(sheet_id, sheet_name, output_file, delimiter):
        try:
            # Abre a planilha pelo ID
            spreadsheet = client.open_by_key(sheet_id)
            # Acessa o primeiro worksheet (índice 0)
            worksheet = spreadsheet.get_worksheet(0)
            data = worksheet.get_all_values()
            
            # Salva os dados em arquivo CSV com o delimitador correto
            with open(output_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=delimiter)
                writer.writerows(data)
            print(f"Planilha '{sheet_name}' salva com sucesso em {output_file} (delimitador: '{delimiter}')")
        except Exception as e:
            print(f"Erro ao baixar a planilha '{sheet_name}': {e}")

    # Processa cada planilha definida em sheets_info
    for sheet in sheets_info:
        download_google_sheet_para_csv(
            sheet_id=sheet["sheet_id"],
            sheet_name=sheet["sheet_name"],
            output_file=sheet["output_file"],
            delimiter=sheet["delimiter"]
        )

    return 'Planilhas baixadas e salvas como CSV com sucesso!'
