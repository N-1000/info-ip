import subprocess
import re
import requests
import os
import platform

def validar_ips_en_archivo():
    # Solicitar al usuario la ruta del archivo de texto
    archivo = input("Ingrese la ruta del archivo de texto: ")
    
    # Leer el contenido del archivo
    with open(archivo, 'r') as file:
        contenido = file.read()
    
    # Encontrar direcciones IP válidas en el contenido del archivo
    ips = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', contenido)

    # Lista para almacenar las direcciones IP activas
    ips_activas = []

    # Comando de ping dependiendo del sistema operativo
    ping_cmd = 'ping' if platform.system().lower() == 'windows' else 'ping -c 1'
    
    # Verificar la actividad de cada dirección IP utilizando ping
    for direccion_ip in ips:
        validador = subprocess.run([ping_cmd, '-n', '1', direccion_ip], capture_output=True, text=True)     
        if validador.returncode == 0:
            ips_activas.append(direccion_ip)
    
    # Si no se encontraron direcciones IP activas, imprimir un mensaje y retornar una lista vacía
    if not ips_activas:
        print("No se encontraron direcciones IP activas en el archivo.")
        return []

    # Solicitar al usuario el nombre del archivo de salida
    nombre_archivo = input("Ingrese el nombre del archivo de salida: ")
    nombre_archivo += '.txt'  
    
    # Construir la ruta completa del archivo de salida
    ruta_archivo = os.path.join(r'C:\Users\nl748\OneDrive\Escritorio\Myproject - one\Results', nombre_archivo)

    # Escribir las direcciones IP activas en el archivo de salida
    with open(ruta_archivo, 'w') as file:
        for ip in ips_activas:
            file.write(ip + '\n')   
    return ips_activas
       
def info_ip(ips_activas):
    # Si no hay direcciones IP activas para consultar, imprimir un mensaje y retornar
    if not ips_activas:
        print("No hay direcciones IP activas para consultar.")
        return

    # API key para acceder a la API de geolocalización
    api_key = '529712a193074f918508f95832b5c829' 
 
    # URL base para la consulta de información geográfica de una dirección IP
    url = "https://api.ipgeolocation.io/ipgeo?apiKey={}&ip={}"
    
    # Consultar información geográfica para cada dirección IP activa
    for ip in ips_activas:
        response = requests.get(url.format(api_key, ip))
        if response.status_code == 200:
            data = response.json()
            # Imprimir la información geográfica obtenida para la dirección IP
            print(f"Información para la IP {ip}:")
            print("País:", data["country_name"])
            print("Ciudad:", data["city"])
            print("Código postal:", data["zipcode"])
            print("Latitud:", data["latitude"])
            print("Longitud:", data["longitude"])
        else:
            # En caso de error al consultar la API de geolocalización, imprimir un mensaje de error
            print(f"Error al consultar IPGeolocation para la IP {ip}. Código de estado:", response.status_code)


if __name__ == "__main__":
    # Validar las direcciones IP en el archivo y obtener las activas
    ips_activas = validar_ips_en_archivo()
    
    # Si hay direcciones IP activas, obtener información geográfica de ellas
    if ips_activas:
        info_ip(ips_activas)





