import requests
import json
import sys

# Cambiar la codificación de la salida estándar a UTF-8
sys.stdout.reconfigure(encoding='utf-8')

def obtener_datos():
    url = "https://randomuser.me/api/?results=5"
    respuesta = requests.get(url)
    
    if respuesta.status_code == 200:
        datos = respuesta.json()
        
        # Mostrar los primeros 5 usuarios de forma ordenada
        for usuario in datos['results']:
            print(f"Nombre: {usuario['name']['first']} {usuario['name']['last']}")
            print(f"Género: {usuario['gender']}")
            print(f"Correo: {usuario['email']}")
            print(f"País: {usuario['location']['country']}")
            print("-" * 40)
    else:
        print(f"Error al obtener los datos. Código de estado: {respuesta.status_code}")
        print("Respuesta del servidor:", respuesta.text)

obtener_datos()