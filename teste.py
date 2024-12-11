import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Arquivo JSON com credenciais do Google
filaname = "caminho_para_o_arquivo_de_credenciais.json"

# Escopos necessários para a autenticação
scopes = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Autenticando com o Google Sheets
cred = ServiceAccountCredentials.from_json_keyfile_name(filaname, scopes)
client = gspread.authorize(cred)

# Abrindo a planilha
planilhaCompleta = client.open(title="Planilha de alunos")
planilha = planilhaCompleta.get_worksheet(0)

# Função para mostrar os dados da planilha
def mostrar_planilha(planilha):
    dados = planilha.get_all_records()  # Pega todos os dados da planilha
    df = pd.DataFrame(dados)  # Converte os dados para um DataFrame do Pandas
    return df

# Função para encontrar o índice da coluna "Gênero"
def encontrar_coluna_genero(planilha):
    # Pega a primeira linha da planilha
    primeira_linha = planilha.row_values(1)
    
    # Procurando pela coluna "Gênero"
    for index, valor in enumerate(primeira_linha):
        if 'genero' in valor.lower():  # Verifica se 'genero' está na célula (case-insensitive)
            return index + 1  # O gspread usa indexação de 1, então somamos 1
    
    return None  # Retorna None se não encontrar a coluna

# Função para substituir "masculino" por "M" e "feminino" por "F"
def substituir_genero(planilha, coluna_genero):
    # Obtém todas as células da coluna de "Gênero", a partir da linha 2 até a última
    total_linhas = len(planilha.col_values(coluna_genero))
    
    # Percorre todas as células abaixo do cabeçalho
    for row in range(2, total_linhas + 1):
        valor = planilha.cell(row, coluna_genero).value
        
        # Substitui "masculino" por "M" e "feminino" por "F"
        if valor and valor.lower() == "masculino":
            planilha.update_cell(row, coluna_genero, "M")
        elif valor and valor.lower() == "feminino":
            planilha.update_cell(row, coluna_genero, "F")

# Exemplo de uso

# Exibir o DataFrame da planilha
df = mostrar_planilha(planilha)
print(df)

# Buscar o índice da coluna "Gênero"
coluna_genero = encontrar_coluna_genero(planilha)

if coluna_genero:
    print(f"A coluna 'Gênero' está na coluna {coluna_genero}")
    
    # Substitui "masculino" por "M" e "feminino" por "F"
    substituir_genero(planilha, coluna_genero)
    print("Substituições realizadas com sucesso.")
    
else:
    print("Coluna 'Gênero' não encontrada.")
