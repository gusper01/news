import certifi

# Imprimir la ubicación del archivo de certificados que está utilizando certifi


import requests
import certifi

print(f"Certifi CA bundle path: {certifi.where()}")

# Parámetros de la solicitud
id_variable = '1'
desde = '2023-01-01'
hasta = '2023-12-31'

# URL de la API
url = f"https://api.bcra.gob.ar/estadisticas/v2.0/DatosVariable/{id_variable}/{desde}/{hasta}"

# Hacer la solicitud GET a la API usando el archivo de certificado de certifi
#response = requests.get(url, verify=certifi.where())
response = requests.get(url, verify=False)
# Imprimir la URL y el estado de la respuesta
print(f"URL: {url}")
print(f"Response status code: {response.status_code}")

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    # Obtener los datos en formato JSON
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}")

# Imprimir la ubicación del archivo de certificados que está utilizando certifi
#print(f"Certifi CA bundle path: {certifi.where()}")

