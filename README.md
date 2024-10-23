# Gamepy - Cuestionario linea de comandos

## Descripción

Juego interactivo para aprender linea de comandos

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/Alanzphy/projectgamepy && cd ./projectgamepy
   ```

Crea un entorno virtual:

  ```bash
python -m venv venv
  ```

## Activa el entorno virtual

En Windows:

  ```bash
venv\Scripts\activate
  ```

En macOS/Linux:

  ```bash
source venv/bin/activate
  ```

Instala las dependencias:

  ```bash
pip install -r requirements.txt
  ```

Crea una account service en GCP con Google Sheets, y el archivo .json, lo remplazas con el nombre 'keys' en el directorio del
proyecto, y la variable sheet_id la remplazas por el id de tu google sheets

## Ejecuta el proyecto

  ```bash
python src/main.py
  ```
