import os
import subprocess
import json
import sys
import datetime
import shutil
import urllib.request

def obtener_wordlist():
    """
    Pregunta al usuario si desea usar una wordlist.
    Si es así, solicita la ruta local o la URL y retorna la ruta local de la wordlist.
    Si no, retorna None.
    """
    respuesta = input("Do you have a wordlist? (yes/no): ").strip().lower()
    if respuesta in ['yes', 'y']:
        ruta_wordlist = input("Please enter the local path or URL of your wordlist: ").strip()
        if ruta_wordlist.startswith("http://") or ruta_wordlist.startswith("https://"):
            # Descargar la wordlist desde la URL
            nombre_archivo = os.path.basename(ruta_wordlist)
            ruta_local = os.path.join(os.getcwd(), nombre_archivo)
            try:
                print(f"Downloading wordlist from {ruta_wordlist}...")
                urllib.request.urlretrieve(ruta_wordlist, ruta_local)
                print(f"Wordlist downloaded and saved to {ruta_local}")
                return ruta_local
            except Exception as e:
                print(f"Failed to download wordlist from URL. Error: {e}")
                return None
        else:
            # Verificar si la ruta local existe
            if os.path.exists(ruta_wordlist):
                return ruta_wordlist
            else:
                print(f"The specified wordlist path does not exist: {ruta_wordlist}")
                return None
    else:
        return None

def crear_carpeta_resultados():
    """
    Crea la carpeta 'Result' si no existe.
    """
    ruta_result = os.path.join(os.getcwd(), "Result")
    if not os.path.exists(ruta_result):
        os.makedirs(ruta_result)
        print(f"Created the output directory: {ruta_result}")
    return ruta_result

def ejecutar_amass(dominio, ruta_salida, wordlist, tiempo):
    """
    Ejecuta Amass para un dominio específico con las opciones proporcionadas.
    """
    nombre_archivo = dominio.replace('.', '_')
    output_prefix = os.path.join(ruta_salida, nombre_archivo)
    
    comando = [
        "amass",
        "enum",
        "-active",
        "-nocolor",
        "-d", dominio,
        "-oA", output_prefix,
        "-timeout", str(tiempo)
    ]
    
    if wordlist:
        comando.extend(["-w", wordlist])
    
    print(f"\nExecuting Amass for domain: {dominio}")
    try:
        subprocess.run(comando, check=True)
        print(f"Amass enumeration completed for {dominio}.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing Amass for {dominio}: {e}")
        return False
    return True

def procesar_txt(ruta_txt):
    """
    Procesa el archivo .txt generado por Amass y extrae los subdominios.
    Añade un separador para diferenciar múltiples escaneos.
    """
    if not os.path.exists(ruta_txt):
        print(f"Subdomain list file not found: {ruta_txt}")
        return
    
    with open(ruta_txt, "r", encoding='utf-8') as file:
        lines = file.readlines()
    
    subdominios = set()
    for line in lines:
        if "node -->" in line:
            partes = line.split(" --> ")
            if len(partes) >= 3:
                subdominio = partes[2].split(" (FQDN)")[0].strip()
                subdominios.add(subdominio)
    
    if subdominios:
        print("\nList of found subdomains:")
        for sub in sorted(subdominios):
            print(sub)
    else:
        print("No subdomains found through passive enumeration.")

def procesar_json(ruta_json):
    """
    Procesa el archivo .json generado por Amass y extrae detalles de los subdominios.
    """
    if not os.path.exists(ruta_json):
        print(f"JSON results file not found: {ruta_json}")
        return
    
    with open(ruta_json, "r", encoding='utf-8') as file:
        try:
            datos_json = json.load(file)
            if not datos_json:
                print("No data found in the JSON file.")
                return
            print("\nSubdomain Details (IPs):")
            for item in datos_json:
                nombre = item.get("name", "N/A")
                direcciones = item.get("addresses", [])
                ips = ", ".join(addr.get("ip", "") for addr in direcciones)
                print(f"{nombre}: {ips if ips else 'No IPs found'}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON file: {ruta_json}")

def agregar_separador(ruta_txt):
    """
    Agrega un separador con la fecha y hora actual al archivo .txt para diferenciar escaneos.
    """
    separador = f"\n\n----- Scan on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -----\n\n"
    with open(ruta_txt, "a", encoding='utf-8') as file:
        file.write(separador)

def main():
    print("=== Welcome to AmaBridge ===\n")
    
    # Obtener dominios del usuario
    dominios_input = input("Enter domain(s) to scan, separated by commas: ").strip()
    dominios = [dom.strip() for dom in dominios_input.split(",") if dom.strip()]
    
    if not dominios:
        print("No valid domains entered. Exiting.")
        sys.exit(1)
    
    # Preguntar por wordlist
    wordlist = obtener_wordlist()
    
    # Crear carpeta de resultados
    ruta_result = crear_carpeta_resultados()
    
    # Tiempo de ejecución en minutos
    tiempo_ejecucion = 60  # Puedes modificar este valor según tus necesidades
    
    for dominio in dominios:
        nombre_archivo = dominio.replace('.', '_')
        archivo_txt = os.path.join(ruta_result, f"{nombre_archivo}.txt")
        archivo_json = os.path.join(ruta_result, f"{nombre_archivo}.json")
        archivo_csv = os.path.join(ruta_result, f"{nombre_archivo}.csv")
        
        # Agregar separador si el archivo ya existe
        if os.path.exists(archivo_txt):
            agregar_separador(archivo_txt)
        
        exitoso = ejecutar_amass(dominio, ruta_result, wordlist, tiempo_ejecucion)
        if exitoso:
            procesar_txt(archivo_txt)
            procesar_json(archivo_json)
        else:
            print(f"Skipping processing for {dominio} due to Amass execution failure.")
    
    print(f"\nAll scans completed. Results are stored in the '{ruta_result}' directory.")

if __name__ == "__main__":
    main()
