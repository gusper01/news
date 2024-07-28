import requests

# Parámetros de la solicitud
id_variable = '1'  # Ejemplo de ID de variable
desde = '2023-01-01'     # Fecha de inicio (formato YYYY-MM-DD)
hasta = '2023-12-31'     # Fecha de fin (formato YYYY-MM-DD)

# URL de la API
url = f"https://api.bcra.gob.ar/estadisticas/v2.0/DatosVariable/{id_variable}/{desde}/{hasta}"

# Hacer la solicitud GET a la API
#response = requests.get(url)
response = requests.get(url, verify=False)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    # Obtener los datos en formato JSON
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}")
