# Análise de Liquidações e Empenhos das Obras de Vargem Alta - ES  

Este projeto é uma ferramenta de análise de liquidações e empenhos das obras de Vargem Alta - ES, com georreferenciamento. Foi desenvolvido pela equipe do **Laboratório de Dados Municipais do LabCidades - UFES**.  

A aplicação foi desenvolvido utilizando **Shiny para Python** na versão **Python 3.13.0**.  

## Configuração do Ambiente  

Antes de instalar as dependências, recomenda-se a criação de um ambiente virtual para garantir a organização e compatibilidade das bibliotecas.  

### Criando um Ambiente Virtual  

Execute os seguintes comandos no terminal:  

```bash
# Criar o ambiente virtual
python -m venv venv  

# Ativar o ambiente virtual (Windows)
venv\Scripts\activate  

# Ativar o ambiente virtual (Linux/Mac)
source venv/bin/activate  
```

## Instalação das Dependências  

Com o ambiente virtual ativado, instale as bibliotecas necessárias executando:  

```bash
pip install -r requirements.txt
```  

## Executando a Aplicação  

Para rodar a aplicação, basta executar o seguinte comando:  

```bash
python app.py
```  

O download, tratamento e processamento dos dados são realizados automaticamente ao iniciar a aplicação.  

---  