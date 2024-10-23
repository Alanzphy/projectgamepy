from googleapiclient.discovery import build
from google.oauth2 import service_account

# Configura la autenticación
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'

# Crea las credenciales
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Construye el servicio
service = build('sheets', 'v4', credentials=credentials)

# ID de tu hoja de cálculo
SPREADSHEET_ID = '1y_IJGlUz6ZQRDXlWwtfXHVxzYDX2C8gIY-ZS8OF_LHc'
KEEP_SHEET_ID = None  # ID de la hoja que deseas mantener

# Obtener la lista de hojas
spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
sheets = spreadsheet.get('sheets', [])

# Encontrar la hoja que deseas mantener (por ejemplo, la primera hoja)
if sheets:
    KEEP_SHEET_ID = sheets[0]['properties']['sheetId']  # Mantiene la primera hoja

# Crear la lista de peticiones para eliminar las demás hojas
requests = []
for sheet in sheets:
    sheet_id = sheet['properties']['sheetId']
    if sheet_id != KEEP_SHEET_ID:
        requests.append({
            "deleteSheet": {
                "sheetId": sheet_id
            }
        })

# Si hay hojas para eliminar, realizar la petición de eliminación
if requests:
    body = {
        'requests': requests
    }

    response = service.spreadsheets().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body=body
    ).execute()

    print('Hojas eliminadas:', response)
else:
    print('No hay hojas adicionales para eliminar.')
