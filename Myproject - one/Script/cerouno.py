import subprocess
import re
import requests
import os
import platform

def validar_ips_en_archivo():
    archivo = input("Ingrese la ruta del archivo de texto: ")
    with open(archivo, 'r') as file:
        contenido = file.read()
    ips = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', contenido)

    ips_activas = []

    ping_cmd = 'ping' if platform.system().lower() == 'windows' else 'ping -c 1'
    for direccion_ip in ips:
        validador = subprocess.run([ping_cmd, '-n', '1', direccion_ip], capture_output=True, text=True)     
        if validador.returncode == 0:
            ips_activas.append(direccion_ip)
    if not ips_activas:
        print("No se encontraron direcciones IP activas en el archivo.")
        return []

    nombre_archivo = input("Ingrese el nombre del archivo de salida: ")
    nombre_archivo += '.txt'  
    ruta_archivo = os.path.join(r'C:\Users\nl748\OneDrive\Escritorio\Myproject - one\Results', nombre_archivo)


    with open(ruta_archivo, 'w') as file:
        for ip in ips_activas:
            file.write(ip + '\n')   
    return ips_activas
       
def info_ip(ips_activas):
    if not ips_activas:
        print("No hay direcciones IP activas para consultar.")
        return

    api_key = '529712a193074f918508f95832b5c829' 
 
    url = "https://api.ipgeolocation.io/ipgeo?apiKey={}&ip={}"
    for ip in ips_activas:
        response = requests.get(url.format(api_key, ip))
        if response.status_code == 200:
            data = response.json()
            print(f"Información para la IP {ip}:")
            print("País:", data["country_name"])
            print("Ciudad:", data["city"])
            print("C. postal:", data["zipcode"])
            print("Latitud:", data["latitude"])
            print("Longitud:", data["longitude"])
        else:
            print(f"Error al consultar IPGeolocation para la IP {ip}. Código de estado:", response.status_code)


if __name__ == "__main__":
    ips_activas = validar_ips_en_archivo()
    if ips_activas:
        info_ip(ips_activas)






