import requests
import json
import sys

# Cambiar la codificación de la salida estándar a UTF-8
sys.stdout.reconfigure(encoding='utf-8')

class Ingestion:
    def __init__(self):
        self.ruta_static = "src/bigdata/static/"

    def obtener_datos(self):
        url = "https://randomuser.me/api/?results=5"
        respuesta = requests.get(url)
        
        if respuesta.status_code == 200:
            datos = respuesta.json()
            
            for usuario in datos['results']:
                print(f"Nombre: {usuario['name']['first']} {usuario['name']['last']}")
                print(f"Género: {usuario['gender']}")
                print(f"Correo: {usuario['email']}")
                print(f"País: {usuario['location']['country']}")
                print("-" * 40)
            return datos  # Retornar los datos para guardarlos
        else:
            print(f"Error al obtener los datos. Código de estado: {respuesta.status_code}")
            print("Respuesta del servidor:", respuesta.text)
            return None

    def guardar_datos(self, datos, nombre_archivo="ingestion.json"):
        ruta_completa = f"{self.ruta_static}db/{nombre_archivo}"  # Corregir formato y typos
        with open(ruta_completa, "w", encoding='utf-8') as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=2)

    def validar_autoria(self, datos, nombre_archivo="ingestion.json"):
        """
        Valida la cantidad de registros y columnas obtenidos, así como la salida en el archivo .json.
        """
        if not datos:
            print("Error: No hay datos para validar.")
            return False

        # Validar cantidad de registros
        cantidad_registros = len(datos['results'])
        print(f"Cantidad de registros obtenidos: {cantidad_registros}")

        # Validar cantidad de columnas (campos) por registro
        primer_registro = datos['results'][0]
        cantidad_columnas = len(primer_registro.keys())
        print(f"Cantidad de columnas por registro: {cantidad_columnas}")

        # Validar archivo guardado
        ruta_completa = f"{self.ruta_static}db/{nombre_archivo}"
        try:
            with open(ruta_completa, "r", encoding='utf-8') as archivo:
                datos_guardados = json.load(archivo)
                cantidad_registros_guardados = len(datos_guardados['results'])
                print(f"Cantidad de registros en el archivo guardado: {cantidad_registros_guardados}")

                if cantidad_registros == cantidad_registros_guardados:
                    print("Validación exitosa: La cantidad de registros coincide.")
                    return True
                else:
                    print("Error: La cantidad de registros no coincide.")
                    return False
        except FileNotFoundError:
            print(f"Error: El archivo {ruta_completa} no existe.")
            return False
        except json.JSONDecodeError:
            print(f"Error: El archivo {ruta_completa} no tiene un formato JSON válido.")
            return False

# Crear instancia y usar métodos
ingestion = Ingestion()
datos = ingestion.obtener_datos()  # Llamar al método desde la instancia

if datos:  # Solo guardar si hay datos
    ingestion.guardar_datos(datos=datos, nombre_archivo="ingestion.json")
    # Validar autoría
    ingestion.validar_autoria(datos, nombre_archivo="ingestion.json")