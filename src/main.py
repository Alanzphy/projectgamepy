import random # Importamos la librería random para seleccionar preguntas aleatorias
import pandas as pd # Importamos la librería pandas para trabajar con datos tabulares
import gspread # Importamos la librería gspread para interactuar con Google Sheets
from oauth2client.service_account import ServiceAccountCredentials # Importamos ServiceAccountCredentials para autenticación
import os  # Importamos os para verificar si el archivo existe
import sys  # Importamos sys para limpiar la terminal
import time  # Importamos time para pausar la ejecución

# Preguntas por nivel de dificultad
preguntas_niveles = {
    'fácil': [
        {"pregunta": "¿Cómo listar archivos en un directorio?", "respuesta_correcta": "ls"},
        {"pregunta": "¿Cómo crear un nuevo directorio?", "respuesta_correcta": "mkdir"},
        {"pregunta": "¿Cómo cambiar el directorio actual?", "respuesta_correcta": "cd"},
        {"pregunta": "¿Cómo copiar un archivo?", "respuesta_correcta": "cp"},
        {"pregunta": "¿Cómo mover un archivo?", "respuesta_correcta": "mv"}
    ],
    'medio': [
        {"pregunta": "¿Cómo mostrar el contenido de un archivo?", "respuesta_correcta": "cat"},
        {"pregunta": "¿Cómo buscar un archivo por su nombre?", "respuesta_correcta": "find"},
        {"pregunta": "¿Cómo mostrar el uso del disco?", "respuesta_correcta": "df"},
        {"pregunta": "¿Cómo ver los procesos actuales en ejecución?", "respuesta_correcta": "ps"},
        {"pregunta": "¿Cómo eliminar un archivo?", "respuesta_correcta": "rm"}
    ],
    'difícil': [
        {"pregunta": "¿Cómo redirigir la salida de un comando a un archivo?", "respuesta_correcta": ">"},
        {"pregunta": "¿Cómo cambiar los permisos de un archivo?", "respuesta_correcta": "chmod"},
        {"pregunta": "¿Cómo agregar permisos de ejecución a un archivo?", "respuesta_correcta": "chmod +x"},
        {"pregunta": "¿Cómo ver el historial de comandos ejecutados?", "respuesta_correcta": "history"},
        {"pregunta": "¿Cómo ver el espacio en disco de un archivo o directorio?", "respuesta_correcta": "du"}
    ]
}

def animacion_procesando():
    """Simula una animación de procesamiento en la terminal."""
    animacion = ["[=     ]", "[==    ]", "[===   ]", "[====  ]", "[===== ]", "[======]"]
    for i in range(1):  # Repetir la animación 1 veces
        for frame in animacion:
            sys.stdout.write(f"\r{frame} Procesando...")
            sys.stdout.flush()
            time.sleep(0.2)  # Pausar por 0.2 segundos entre cada frame
    print("\n")

def animacion_escribir(texto, velocidad=0.029):
    """Simula la escritura de texto en la terminal, con un pequeño retraso entre cada carácter."""
    for char in texto:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(velocidad)
    print()  # Para ir a la siguiente línea al terminar de escribir

def jugar_nivel(nombre, nivel, preguntas):
    """Lógica para jugar un nivel y registrar respuestas."""
    nombre = nombre.capitalize()
    respuestas = []
    puntaje = 0
    preguntas_nivel = random.sample(preguntas, 5)  # Seleccionar 5 preguntas aleatorias

    for pregunta in preguntas_nivel:
      os.system('clear' if os.name == 'posix' else 'cls')  # Limpiar la terminal

      print(f"Nivel {nivel.upper()}")
      print(pregunta["pregunta"])

      respuesta = input("Ingresa el comando (o escribe 'rendirse' para pasar): ")
      # Mostrar animación de procesamiento despues de ingresar la respuesta
      animacion_procesando()


      if respuesta.lower() == 'rendirse':
          animacion_escribir(f"Te rendiste. La respuesta correcta es: {pregunta['respuesta_correcta']}")
          respuestas.append({"Pregunta": pregunta["pregunta"], "Respuesta": "Rendirse", "Resultado": "Incorrecto"})
      elif respuesta == pregunta["respuesta_correcta"]:
          animacion_escribir(f"Correcto!")
          respuestas.append({"Pregunta": pregunta["pregunta"], "Respuesta": respuesta, "Resultado": "Correcto"})
          puntaje += 1
      else:
          animacion_escribir(f"Incorrecto. La respuesta correcta es: {pregunta['respuesta_correcta']}")
          respuestas.append({"Pregunta": pregunta["pregunta"], "Respuesta": respuesta, "Resultado": "Incorrecto"})

      # Esperar unos segundos para que el jugador vea el resultado
      input("\nPresiona Enter para continuar...")


    print(f"Puntaje en nivel {nivel}: {puntaje}/5\n")
    return puntaje, respuestas

def guardar_respuestas_y_puntaje_en_excel(nombre, puntaje_total, respuestas, nombre_archivo):
    """Guarda las respuestas y puntaje del jugador en un archivo Excel, creando una nueva hoja si es necesario."""
    df = pd.DataFrame(respuestas)

    # Crear el archivo Excel si no existe
    if not os.path.exists(nombre_archivo):
        with pd.ExcelWriter(nombre_archivo, engine='openpyxl') as writer:
            # Guardar las respuestas en la primera hoja
            df.to_excel(writer, sheet_name=f'{nombre}', index=False)
        print(f"Archivo {nombre_archivo} creado y guardado.")
    else:
        # Si el archivo ya existe, debemos agregar una nueva hoja
        with pd.ExcelWriter(nombre_archivo, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            # Abrir la hoja existente
            df.to_excel(writer, sheet_name=f'{nombre}', index=False, startrow=5)  # Inicia desde la fila 5 para las preguntas

            # Abrir la hoja para agregar el nombre y puntaje total
            worksheet = writer.sheets[f'{nombre}']

            # Guardar el nombre y el puntaje total en celdas específicas
            worksheet['A1'] = 'Nombre'
            worksheet['B1'] = nombre
            worksheet['A2'] = 'Puntaje Total'
            worksheet['B2'] = puntaje_total

            print(f"Respuestas guardadas en la hoja '{nombre}' del archivo {nombre_archivo}.")
    return puntaje_total  # Retornar el puntaje total

def leer_puntaje_total(nombre_archivo, nombre_hoja):
    """Lee el puntaje total del archivo Excel y lo muestra."""
    if os.path.exists(nombre_archivo):
        df = pd.read_excel(nombre_archivo, sheet_name=nombre_hoja)
        puntaje_total = df.iloc[0, 1]  # Asumiendo que el puntaje total está en la celda B2
        print(f"Tu puntaje total es: {puntaje_total}")
    else:
        print("El archivo no existe.")

def subir_a_google_sheets(nombre_archivo, sheet_id, credenciales_json, nombre_hoja, puntaje_total):
    """Sube un archivo Excel a una nueva hoja de Google Sheets con la misma estructura."""
    scope  = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds  = ServiceAccountCredentials.from_json_keyfile_name(credenciales_json, scope)
    client = gspread.authorize(creds)

    # Leer el archivo Excel especificando que los encabezados están en la fila 0
    df = pd.read_excel(nombre_archivo, sheet_name=nombre_hoja, header=5)

    # Reemplazar valores NaN por cadenas vacías
    df = df.fillna('')

    # Imprimir el contenido del DataFrame para depuración
    print(df.head())  # Imprime las primeras filas del DataFrame

    # Renombrar las columnas para que coincidan con los nombres esperados
    df.columns = ['Pregunta', 'Respuesta', 'Resultado']  # Renombrar columnas

    # Verificar si las columnas existen
    required_columns = ['Pregunta', 'Respuesta', 'Resultado']
    for col in required_columns:
        if col not in df.columns:
            #print(f"Columna '{col}' no encontrada en el DataFrame.")
            return  # Termina la función si alguna columna falta

    # Abrir la hoja de Google Sheets existente usando su ID
    spreadsheet = client.open_by_key(sheet_id)

    # Crear una nueva hoja en Google Sheets
    new_worksheet = spreadsheet.add_worksheet(title=nombre_hoja, rows="100", cols="20")

    # Subir el nombre y puntaje total en las celdas A1 y A2
    new_worksheet.update(range_name='A1', values=[['Nombre']])
    new_worksheet.update(range_name='B1', values=[[nombre]])
    new_worksheet.update(range_name='A2', values=[['Puntaje Total']])
    new_worksheet.update(range_name='B2', values=[[puntaje_total]])

    # Subir el encabezado de las preguntas en la fila 4
    new_worksheet.update(range_name='A4', values=[['Pregunta', 'Respuesta', 'Resultado']])

    # Convertir las preguntas, respuestas y resultados en lista de listas
    datos = df[required_columns].values.tolist()

    # Subir los datos a partir de la fila 5
    new_worksheet.update(range_name='A5', values=datos)

    print(f"Estructura de datos subida a la nueva hoja '{nombre_hoja}' en Google Sheets.")


if __name__ == "__main__":
    # Nombre del archivo Excel
    nombre_archivo = 'respuestas_y_puntaje_comandos.xlsx'

    # ID del archivo de Google Sheets donde se subirán los datos
    sheet_id = '1y_IJGlUz6ZQRDXlWwtfXHVxzYDX2C8gIY-ZS8OF_LHc'

    # Archivo de credenciales
    credenciales_json = 'keys.json'

    # Jugar el juego
    nombre             = input("Ingresa tu nombre: ")
    puntaje_total      = 0
    respuestas_totales = []

    niveles = ['fácil', 'medio', 'difícil']
    for nivel in niveles:
        puntaje, respuestas = jugar_nivel(nombre, nivel, preguntas_niveles[nivel])
        puntaje_total      += puntaje
        respuestas_totales.extend(respuestas)

        # Si no pasa el nivel, se termina el juego
        if puntaje < 3:
            print(f"No lograste pasar el nivel {nivel}. Fin del juego.")
            break
    else:

        print(f"¡Felicidades {nombre}! Completaste todos los niveles.")

    # Guardar las respuestas y puntaje en Excel con una nueva hoja
    guardar_respuestas_y_puntaje_en_excel(nombre, puntaje_total, respuestas_totales, nombre_archivo)

    # Subir el archivo Excel a una nueva hoja en Google Sheets
    subir_a_google_sheets(nombre_archivo, sheet_id, credenciales_json, nombre, puntaje_total)

    # Leer el puntaje total desde el archivo Excel
    leer_puntaje_total(nombre_archivo, nombre)
