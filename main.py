import os.path
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def main():
  




  creds = None
  
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "client_secret.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId="", range="Planilha1!A1:AC33")
        .execute()
    )
    
   
    valores = result['values']
    
  

  except HttpError as err:
    print(err)

def formatarGenero(valores,sheet):
    for i, linha in enumerate (valores):
      
      if i > 0:
        genero = linha[1]
        genero = sheet.values().get(spreadsheetId="1frYwEuHv6_oqoojpUicCYLSuutQLAR_kQJSAzvsAW3k", range="Planilha1!E2")  

        #Verificações e correções da coluna gênero baseado no que já foi apurado até hoje (10/12/2024)
        genero = genero.replace("Masc.", "M").replace("Masculino", "M").replace('MASCULINO', "M").replace("masculino", "M").replace("m", "M")

        #Verificações e correções da coluna gênero baseado no que já foi apurado até hoje (10/12/2024)
        genero = genero.replace("Fem.", "F").replace("Feminino", "F").replace('FEMININO', "F").replace("feminino", "F").replace("f", "F")

        print(genero)

if __name__ == "__main__":
  main()
  
  
  