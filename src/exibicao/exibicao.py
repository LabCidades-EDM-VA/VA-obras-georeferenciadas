import folium
import os
from folium import Popup
import geopandas as gpd
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from shiny import App, ui, render
from folium.plugins import HeatMap
import pandas as pd

def criar_mapa():
    # Função para limpar e converter valores monetários
    def limpar_valor(valor_str):
        valor_str = valor_str.replace("R$", "").strip().replace(" ", "")
        valor_str = valor_str.replace(".", "").replace(",", ".")
        return float(valor_str)

    # Função para formatar valores no padrão brasileiro
    def formatar_valor_br(valor):
        return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def formatar_valor_br_sem_casas_decimais(valor):
        return f"{int(valor):,}".replace(",", ".")


    def build_listagem_liquidacoes(empenhos):
        html = "<ul class='empenho-list'>"
        for empenho in empenhos:
            empenho_valor = float(empenho['valor'])
            html += f"""
                <li class='empenho-item'>
                    <div class='empenho-header'>
                        <span class='empenho-number'>Empenho {empenho['empenho']}</span>
                        <span class='empenho-value'>R$ {formatar_valor_br(empenho_valor)}</span>
                    </div>
            """
            liquidacoes = empenho.get('liquidacoes', [])
            if not isinstance(liquidacoes, list):
                try:
                    liquidacoes = list(liquidacoes)
                except Exception:
                    liquidacoes = []
            
            if liquidacoes:
                html += "<ul class='liquidacao-list'>"
                for liquidacao in liquidacoes:
                    html += f"""
                        <li class='liquidacao-item'>
                            <span class='liquidacao-number'>Liquidação {liquidacao['Liquidação']}</span>
                            <span class='liquidacao-value'>R$ {formatar_valor_br(limpar_valor(liquidacao['Valor']))}</span>
                        </li>
                    """
                html += "</ul>"
            html += "</li>"
        html += "</ul>"
        return html

    def build_progress_bar(percentage, bar_width, bar_height):
        scale_factor = bar_width / 150.0
        green_percentage = min(percentage, 100)
        green_width = green_percentage * scale_factor

        yellow_percentage = 0
        if percentage > 100:
            yellow_percentage = min(percentage - 100, 50)
        yellow_width = yellow_percentage * scale_factor

        demarcation_position = 100 * scale_factor

        flag_div = ""
        if percentage > 150:
            flag_div = f"""
            <div class="progress-flag">
                <span class="flag-text">{percentage:.0f}%</span>
                <span class="flag-arrow"></span>
            </div>
            <div class="progress-overflow"></div>
            """
            text_inside = ""
        else:
            text_inside = f"{percentage:.0f}%"

        progress_html = f"""
        <div class="progress-container" style="width: {bar_width}px;">
            <div class="progress-bar" style="height: {bar_height}px;">
                <div class="progress-green" style="width: {green_width}px;"></div>
                <div class="progress-yellow" style="width: {yellow_width}px; left: {green_width}px;"></div>
                <div class="progress-demarcation" style="left: {demarcation_position}px;"></div>
                <div class="progress-text">{text_inside}</div>
                {flag_div}
            </div>
            <div class="progress-marks">
                <span>0%</span>
                <span style="left: {demarcation_position}px;">100%</span>
                <span style="right: 0;">150%</span>
            </div>
        </div>
        """
        return progress_html

    def build_popup_html(row):
        # --- Início: Geração do gráfico de barras com matplotlib ---
        import matplotlib
        matplotlib.use('Agg')  # Define um backend que não depende do Tkinter
        import matplotlib.pyplot as plt
        from io import BytesIO
        import base64

        fig, ax = plt.subplots(figsize=(4, 3))
        # Utilizando os valores da obra e do total pago
        valores = [float(row['valor']), float(row['totalPago'])]
        categorias = ['Valor da Obra', 'Total Liquidado']
        barras = ax.bar(categorias, valores, color=['#d292e2', '#8B008B'])
        ax.set_title('Comparação: Valor Total X Liquidado')
        ax.yaxis.set_visible(False)
        max_val = max(valores)
        # Remover as bordas do gráfico
        for spine in ax.spines.values():
            spine.set_visible(False)

        ax.set_ylim(0, max_val * 1.2)  # adiciona 20% de margem

        percentualPago = float(row['percentualTotalPago'])
        count = 0
        for barra in barras:
            altura = barra.get_height()
            if count != 1:
                # Valor total obra em cima da barra
                ax.annotate(f'R$ {formatar_valor_br_sem_casas_decimais(altura)}',
                            xy=(barra.get_x() + barra.get_width()/2, altura),
                            xytext=(0, 7),  # desloca 7 pontos para cima
                            textcoords='offset points',
                            ha='center', va='bottom', fontsize=10)
            else:
                # Valor Liquidado total em cima da barra
                ax.annotate(f'R$ {formatar_valor_br_sem_casas_decimais(altura)} ({percentualPago:.0f}%)',
                            xy=(barra.get_x() + barra.get_width()/2, altura),
                            xytext=(0, 7),  # desloca 7 pontos para cima
                            textcoords='offset points',
                            ha='center', va='bottom', fontsize=10)
                if percentualPago >= 30:
                    # Porcentagem dentro da barra
                    ax.annotate(f'{percentualPago:.0f}%',
                                xy=(barra.get_x() + barra.get_width()/2, altura),
                                xytext=(3, -35),  # desloca 3 pontos para direita e 35 pontos para baixo
                                textcoords='offset points',
                                ha='center', va='bottom', fontsize=20, color='#ffffff', fontweight='bold')
            count += 1

        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        imagem_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close(fig)

        grafico_img_tag = f'<img src="data:image/png;base64,{imagem_base64}" alt="Gráfico de Barras" style="width: 100%; height: auto;">'
        # --- Fim: Geração do gráfico de barras ---

        total_value = row['valor']
        total_liquidado = row['totalPago']
        percentage = (total_liquidado / total_value * 100) if total_value else 0

        bar_width = 360
        bar_height = 40

        progress_bar_html = build_progress_bar(percentage, bar_width, bar_height)
        listagem_html = build_listagem_liquidacoes(row['empenhos'])
            # <div class="progress-section">
            #     <h3 class="section-title">Progresso da Liquidação</h3>
            #     {progress_bar_html}
            # </div>
            # <div class="popup-summary">
            #     <div class="summary-item">
            #         <span class="summary-label">Valor Total da Obra:</span>
            #         <span class="summary-value">R$ {formatar_valor_br(total_value)}</span>
            #     </div>
            #     <div class="summary-item">
            #         <span class="summary-label">Valor Total Liquidado:</span>
            #         <span class="summary-value">R$ {formatar_valor_br(total_liquidado)}</span>
            #     </div>
            # </div>
        popup_html = f"""
        <div class="popup-container">
            <h2 class="popup-title" style= "text-align: left">{row['descricaoObra']}</h2>
            <div class="chart-section" style="margin-top:10px;">
                {grafico_img_tag}
            </div>

            <div class="popup-summary">
                <div class="summary-item">
                    <span class="summary-label">Valor Total da Obra:</span>
                    <span class="summary-value">R$ {formatar_valor_br(total_value)}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">Valor Total Liquidado:</span>
                    <span class="summary-value">R$ {formatar_valor_br(total_liquidado)}</span>
                </div>
            </div>

            <div class="empenhos-section">
                <h3 class="section-title">Empenhos e Liquidações</h3>
                <div class="empenhos-container">
                    {listagem_html}
                </div>
            </div>
        </div>
        <style>
            .popup-container {{
                width: 400px;
                font-family: 'Roboto', Arial, sans-serif;
                font-size: 14px;
                background: #ffffff;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                padding: 20px;
            }}
            .popup-title {{
                margin: 0 0 15px 0;
                text-align: center;
                color: #333;
                font-size: 18px;
                font-weight: bold;
            }}
            .popup-summary {{
                display: flex;
                justify-content: space-between;
                margin-top: 20px;
                margin-bottom: 30px;
            }}
            .summary-item {{
                display: flex;
                flex-direction: column;
                align-items: center;
            }}
            .summary-label {{
                font-size: 12px;
                color: #666;
            }}
            .summary-value {{
                font-size: 16px;
                font-weight: bold;
                color: #333;
            }}
            .section-title {{
                font-size: 16px;
                color: #444;
                margin-bottom: 10px;
            }}
            .progress-container {{
                position: relative;
                margin-bottom: 20px;
            }}
            .progress-bar {{
                position: relative;
                background-color: #ddd;
                border: 2px solid #000;
                overflow: hidden;
            }}
            .progress-green {{
                position: absolute;
                height: 100%;
                background-color: #4CAF50;
            }}
            .progress-yellow {{
                position: absolute;
                height: 100%;
                background-color: #FFD700;
            }}
            .progress-demarcation {{
                position: absolute;
                top: 0;
                width: 2px;
                height: 100%;
                background-color: #000;
            }}
            .progress-text {{
                position: absolute;
                width: 100%;
                height: 100%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                color: #000;
            }}
            .progress-flag {{
                position: absolute;
                right: 5px;
                top: 50%;
                transform: translateY(-50%);
                background-color: #FF0000;
                color: white;
                display: flex;
                align-items: center;
                padding: 2px 6px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 3px 0 0 3px;
                height: 70%;
            }}
            .flag-text {{
                margin-right: 3px;
            }}
            .flag-arrow {{
                width: 0;
                height: 0;
                border-top: 5px solid transparent;
                border-bottom: 5px solid transparent;
                border-left: 5px solid #FF0000;
                position: absolute;
                right: -5px;
            }}
            .progress-overflow {{
                position: absolute;
                right: 0;
                top: 0;
                width: 2px;
                height: 100%;
                background-color: #FF0000;
            }}
            .progress-marks {{
                display: flex;
                justify-content: space-between;
                font-size: 12px;
                color: #666;
                margin-top: 5px;
                position: relative;
            }}
            .progress-marks span {{
                position: absolute;
            }}
            .empenhos-container {{
                max-height: 200px;
                overflow-y: auto;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 10px;
            }}
            .empenho-list {{
                list-style: none;
                padding: 0;
                margin: 0;
            }}
            .empenho-item {{
                margin-bottom: 10px;
                padding: 10px;
                background: #f5f5f5;
                border-radius: 4px;
            }}
            .empenho-header {{
                display: flex;
                justify-content: space-between;
                font-weight: bold;
                margin-bottom: 5px;
            }}
            .liquidacao-list {{
                list-style: none;
                padding-left: 20px;
            }}
            .liquidacao-item {{
                display: flex;
                justify-content: space-between;
                margin-top: 5px;
                font-size: 12px;
            }}
        </style>
        """
        return popup_html

    # Localização inicial no mapa (Vargem Alta, ES)
    localizacao_inicial = [-20.6711, -41.0074]
    zoom_inicial = 10

    # Definir os caminhos relativos
    caminho_municipio = os.path.join("..", "dados", "dados_tratados", "limite_municipio_vargem_alta.geojson")
    caminho_distritos_vargem_alta = os.path.join("..", "dados", "dados_tratados", "distritos_vargem_alta.geojson")
    caminho_bairros_vargem_alta = os.path.join("..", "dados", "dados_tratados", "bairros_vargem_alta.geojson")
    caminho_contratos = os.path.join("..", "dados", "dados_processados", "contratos.parquet")

    # Carregar os dados
    gdf_municipio_vargem_alta = gpd.read_file(caminho_municipio)
    gdf_distritos_vargem_alta = gpd.read_file(caminho_distritos_vargem_alta)
    gdf_bairros_vargem_alta = gpd.read_file(caminho_bairros_vargem_alta)
    gdf_contratos = gpd.read_parquet(caminho_contratos)

    # Ajusta o CRS
    gdf_municipio_vargem_alta = gdf_municipio_vargem_alta.to_crs(epsg=4674)
    gdf_distritos_vargem_alta = gdf_distritos_vargem_alta.to_crs(epsg=4674)
    gdf_bairros_vargem_alta = gdf_bairros_vargem_alta.to_crs(epsg=4674)
    gdf_contratos = gdf_contratos.to_crs(epsg=4674)

    # Criar o mapa
    mapa = folium.Map(location=localizacao_inicial, zoom_start=zoom_inicial)

    # Adicionar camadas geográficas
    folium.GeoJson(
        gdf_municipio_vargem_alta.geometry,
        name='Limites da cidade de Vargem Alta',
        style_function=lambda x: {'color': 'green'}
    ).add_to(mapa)
    folium.GeoJson(
        gdf_distritos_vargem_alta.geometry,
        name='Distritos da cidade de Vargem Alta',
        style_function=lambda x: {'color': 'green'}
    ).add_to(mapa)
    folium.GeoJson(
        gdf_bairros_vargem_alta.geometry,
        name='Bairros da cidade de Vargem Alta',
        style_function=lambda x: {'color': 'green'}
    ).add_to(mapa)

    # Filtrar contratos com coordenadas nulas
    gdf_contratos = gdf_contratos[gdf_contratos['geometry'].notnull()]

    # Camada de obras
    obras_layer = folium.FeatureGroup(name='Obras', show=True)
    for _, row in gdf_contratos.iterrows():
        popup_html = build_popup_html(row)
        popup = folium.Popup(popup_html, max_width=420)
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            popup=popup,
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(obras_layer)
    obras_layer.add_to(mapa)

    # Camada de heatmap
    calor_layer = folium.FeatureGroup(name='mapa de calor', show=True)
    heat_data = [
        (point.y, point.x, row.valor)
        for point, row in zip(gdf_contratos.geometry, gdf_contratos.itertuples())
        if point.geom_type == "Point"
    ]
    HeatMap(heat_data, radius=30, blur=15, max_zoom=1).add_to(calor_layer)
    calor_layer.add_to(mapa)

    folium.LayerControl().add_to(mapa)
    return mapa

# App
def obter_app_ui():
    # Definir a interface do Shiny
    app_ui = ui.page_fluid(

        # Definir estilo global para o body para remover margens e paddings
        ui.tags.style("""
            body {
                margin: 0;
                padding: 0;
            }
            .container-fluid {
                padding: 0 !important;
            }
            .row {
                margin: 0 !important;
                padding: 0 !important;
            }
        """),

        # Cabeçalho estilizado (com logotipo e texto à direita)
        ui.tags.div(
            ui.tags.h1(
                ui.tags.span("Escritório", style="color: #7C019B; margin: 0; display: inline-block; float: left;"),
                ui.tags.span(
                    ui.tags.span("de Dados", style="color: #7C019B; margin: 0 8px 0 0; display: inline-block;"),
                    ui.tags.span("| Vargem Alta", style="color: #FEAA01; ; margin: 0; display: inline-block;")                
                ),
                style="float: left; margin-left: 50px; display: flex; flex-direction: column; align-items: flex-start; font-size: 1.5em;"
            ),
            ui.tags.h2("Visualização geolocalizada das obras da Cidade de Vargem Alta",
                style="color: #93319B; margin: 0 50px 0 0; padding: 0; float: right; font-size: 1.5em;"),
            style="height: 15vh; width: 100vw; padding: 10px; font-size: 3vh; display: flex; justify-content: space-between; align-items: center; background-color: white; font-family: 'Arial', sans-serif; font-weight: bold;"
        ),

        # Corpo do aplicativo (mapa, gráficos, etc.)
        ui.tags.div(
            ui.output_ui("mapa_output"),
            style="height: 80vh; width: 100vw; border: none; background-color: #f0f0f0; overflow: hidden; margin: 0; padding: 0;"
        ),

        # Rodapé estilizado
        ui.tags.div(
            ui.tags.p(
                "LabCidades Projetos Inteligentes - Universidade Federal do Espírito Santo (UFES), Goiabeiras, Vitória - ES, 29075-053",
                style="color: white; font-size: 0.9em; text-align: center; margin: 0; padding: 0;"
            ),
            style="height: 5vh; width: 100vw; background-color: #6D6E70; display: flex; justify-content: center; align-items: center; position: fixed; bottom: 0; margin: 0;"
        )
    )
    return app_ui

# Definir o servidor
def server(input, output, session):
    @output
    @render.ui
    def mapa_output():
        mapa = criar_mapa()
        mapa_html = mapa._repr_html_()
        return ui.HTML(mapa_html)
    
def roda_app():
    # Criar o app
    app = App(obter_app_ui(), server)

    # Rodar o app
    app.run()
