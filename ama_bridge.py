import os
import subprocess
import json
import sys
import datetime
from colorama import init, Fore, Style
import pyfiglet

# Inicializar Colorama
init(autoreset=True)

def imprimir_ascii_art():
    """
    Imprime el título del proyecto en ASCII art con colores.
    """
    ascii_art = pyfiglet.figlet_format("AmaBridge", font="slant")
    print(Fore.CYAN + ascii_art)

def obtener_wordlist():
    """
    Pregunta al usuario si desea usar una wordlist.
    Si es así, solicita la ruta local o la URL y retorna la ruta local de la wordlist.
    Si no, retorna None.
    """
    while True:
        respuesta = input(Fore.YELLOW + "Do you have a wordlist? (yes/no): ").strip().lower()
        if respuesta in ['yes', 'y']:
            ruta_wordlist = input(Fore.YELLOW + "Please enter the local path or URL of your wordlist: ").strip()
            if ruta_wordlist.startswith("http://") or ruta_wordlist.startswith("https://"):
                # Descargar la wordlist desde la URL
                nombre_archivo = os.path.basename(ruta_wordlist)
                ruta_local = os.path.join(os.getcwd(), nombre_archivo)
                try:
                    print(Fore.GREEN + f"Downloading wordlist from {ruta_wordlist}...")
                    subprocess.run(["powershell", "-Command", f"Invoke-WebRequest -Uri {ruta_wordlist} -OutFile {ruta_local}"], check=True)
                    print(Fore.GREEN + f"Wordlist downloaded and saved to {ruta_local}")
                    return ruta_local
                except Exception as e:
                    print(Fore.RED + f"Failed to download wordlist from URL. Error: {e}")
                    return None
            else:
                # Verificar si la ruta local existe
                if os.path.exists(ruta_wordlist):
                    return ruta_wordlist
                else:
                    print(Fore.RED + f"The specified wordlist path does not exist: {ruta_wordlist}")
                    return None
        elif respuesta in ['no', 'n']:
            return None
        else:
            print(Fore.RED + "Invalid input. Please enter 'yes' or 'no'.")

def crear_carpeta_resultados():
    """
    Crea la carpeta 'Result' si no existe.
    """
    ruta_result = os.path.join(os.getcwd(), "Result")
    if not os.path.exists(ruta_result):
        os.makedirs(ruta_result)
        print(Fore.GREEN + f"Created the output directory: {ruta_result}")
    else:
        print(Fore.GREEN + f"The output directory already exists: {ruta_result}")
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
        print(Fore.GREEN + f"Using wordlist: {wordlist}")
    
    print(Fore.CYAN + f"\n[+]{Fore.WHITE} Executing Amass for domain: {Fore.YELLOW}{dominio}")
    try:
        proceso = subprocess.run(comando, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(Fore.GREEN + "[+]" + Fore.WHITE + " Amass enumeration completed successfully.")
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"[-] Error executing Amass for {dominio}: {e.stderr}")
        return False
    return True

def procesar_txt(ruta_txt):
    """
    Procesa el archivo .txt generado por Amass y muestra los subdominios únicos.
    Añade un separador para diferenciar múltiples escaneos.
    """
    if os.path.exists(ruta_txt):
        print(Fore.CYAN + "\n[+]" + Fore.WHITE + " List of found subdomains:")
        with open(ruta_txt, "r", encoding='utf-8') as file:
            subdominios = set()
            for line in file:
                if "node -->" in line:
                    partes = line.strip().split(" --> ")
                    if len(partes) >= 3:
                        subdominio = partes[2].split(" (FQDN)")[0].strip()
                        subdominios.add(subdominio)
        if subdominios:
            for sub in sorted(subdominios):
                print(Fore.GREEN + f" - {sub}")
        else:
            print(Fore.YELLOW + "No subdomains found through passive enumeration.")
    else:
        print(Fore.RED + f"[-] Subdomain list file not found: {ruta_txt}")

def procesar_json(ruta_json):
    """
    Procesa el archivo .json generado por Amass y muestra detalles adicionales.
    """
    if os.path.exists(ruta_json):
        print(Fore.CYAN + "\n[+]" + Fore.WHITE + " Subdomain Details (IPs):")
        with open(ruta_json, "r", encoding='utf-8') as file:
            try:
                datos_json = json.load(file)
                if datos_json:
                    for item in datos_json:
                        nombre = item.get("name", "N/A")
                        direcciones = item.get("addresses", [])
                        ips = ", ".join(addr.get("ip", "") for addr in direcciones)
                        ip_display = Fore.YELLOW + ips if ips else Fore.RED + "No IPs found"
                        print(Fore.GREEN + f" - {nombre}: {ip_display}")
                else:
                    print(Fore.YELLOW + "No data found in the JSON file.")
            except json.JSONDecodeError:
                print(Fore.RED + f"[-] Error decoding JSON file: {ruta_json}")
    else:
        print(Fore.RED + f"[-] JSON results file not found: {ruta_json}")

def agregar_separador(ruta_txt):
    """
    Agrega un separador con la fecha y hora actual al archivo .txt para diferenciar escaneos.
    """
    separador = f"\n\n----- Scan on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -----\n\n"
    with open(ruta_txt, "a", encoding='utf-8') as file:
        file.write(separador)

def main():
    imprimir_ascii_art()
    print(Fore.MAGENTA + "Welcome to AmaBridge - Your Bridge to Powerful DNS Enumeration with Amass\n")
    
    # Obtener dominios del usuario
    dominios_input = input(Fore.YELLOW + "Enter domain(s) to scan, separated by commas: " + Fore.WHITE).strip()
    dominios = [dom.strip() for dom in dominios_input.split(",") if dom.strip()]
    
    if not dominios:
        print(Fore.RED + "No valid domains entered. Exiting.")
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
            print(Fore.RED + f"Skipping processing for {dominio} due to Amass execution failure.")
    
    print(Fore.MAGENTA + f"\nAll scans completed. Results are stored in the '{ruta_result}' directory.")
    print(Fore.CYAN + "Stay secure and keep hacking responsibly!\n")

if __name__ == "__main__":
    main()
