import datos
import pygame
import random
from datetime import datetime 
import os

 #---------- FUNCION PARA GENERAR MATRIZ 10*10 DE AGUA(0)---------------
def matriz_agua(): 
    return [[datos.agua for _ in range(datos.columnas)] for _ in range(datos.filas)] #Usando comprension de lista para generar la matriz con agua(0) y retornar el valor a main


 #---------- FUNCION PARA GENERAR MATRIZ 10*10 DE DISPAROS---------------
def matriz_disparos():
    # Creamos la matriz igual que la del agua, más corto y limpio
    return [[datos.agua for _ in range(datos.columnas)] for _ in range(datos.filas)]


#---------- FUNCION PARA VALIDAR LAS COORDENADAS DEL USUARIO ---------------
def coordenada_valida(f, c):
    # Verificamos que f y c estén entre 0 y el máximo permitido
    if 0 <= f < datos.filas and 0 <= c < datos.columnas: #Se verifica si esta entre 0 y 10, dependiendo retorna True o False
        return True
    else:
        print("¡Coordenada fuera del mapa! Intenta de nuevo.")#Mensaje por si ingreso coordenada invalida
        return False #Aunque tambien se podria hacer usando los eventos de pygame y que en vez de ser introduciendo coordenadas, que el usuario con el mouse haga click en la matriz para disparar
    
#------------- FUNCION PARA ESCANEAR EL ESPACIO DISPONIBLE PARA LAS FLOTAS ---------------
def posicion_valida(tablero, f, c, orientacion, tamaño):
    # CASO HORIZONTAL
    if orientacion == "H":
        if c + tamaño > datos.columnas: # 1. Verificamos borde
            return False
        for i in range(tamaño):         # 2. Verificamos si choca con otro barco
            if tablero[f][c + i] != datos.agua:
                return False
                
    # CASO VERTICAL
    else:
        if f + tamaño > datos.filas:    # 1. Verificamos borde
            return False
        for i in range(tamaño):         # 2. Verificamos si choca con otro barco
            if tablero[f + i][c] != datos.agua:
                return False
                
    return True
    #Retoraria True siempre, porque si cumple todas las viladaciones, las condiciones de esta funcion "posicion_valida()" no reotrnarian False.
    #En cambio, si no cumple una, retornaria minimo un False Y(AND) un True, lo que resultaria en que la funcion "posicion_valida()" por logica es igual a False
    
#------------- FUNCION DE ORIENTACION Y COLOCACION ---------------
def colocar_barco(tablero, f, c, orientacion, barco):
    tamaño = barco["tamaño"]
    simbolo = barco["simbolo"] # Usamos el símbolo (P, A, S, D)
    for i in range(tamaño):
        if orientacion == "H":
            tablero[f][c + i] = simbolo
        else:
            tablero[f + i][c] = simbolo
            
#------------- FUNCION DE GENERACION DE FLOTA RANDOM ---------------
def generar_flota_random(tablero, flota):
    for barco in flota: # Iteramos sobre tu nueva lista de diccionarios
        colocado = False
        while not colocado:
            f = random.randint(0, datos.filas - 1)
            c = random.randint(0, datos.columnas - 1)
            orientacion = random.choice(["H", "V"])
            
            # Pasamos barco["tamaño"] a la validación
            if posicion_valida(tablero, f, c, orientacion, barco["tamaño"]):
                colocar_barco(tablero, f, c, orientacion, barco)
                colocado = True

#------------- FUNCION DE VERFIFICACION DE BARCO HUNDIDO ---------------           
def barco_hundido(hundido,flota):
    if hundido == 0:
        print(f"!Excelente! Has hundido un {flota['nombre']}")
        
#------------- FUNCION DE VERFIFICACION DE TABLERO SIN BARCOS ---------------           
def tablero_sin_barcos(sin_flota):
    if sin_flota == 0:
        print("¡Felicidades! Has hundido toda la flota enemiga.")
        game_over = True
        return game_over
        
# --- GUARDAR HISTORIAL ---
def guardar_historial(nombre, intentos, resultado):
    try:
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Formato exigido por el PDF: Nombre, Fecha, Intentos, Resultado
        linea = f"JUGADOR: {nombre} | FECHA: {fecha} | INTENTOS: {intentos} | RESULTADO: {resultado}\n"
        
        with open("historial.txt", "a") as archivo:
            archivo.write(linea)
        print(f"--- Registro guardado: {resultado} ---")
    except Exception as e:
        print(f"Error guardando archivo: {e}")

# ---------- FUNCION DE FILTRO PARA MEJORES PUNTAJES -------------
def guardar_mejor_puntaje(nombre_jugador, intentos_realizados):
    nombre_archivo = "mejores_puntajes.txt"
    lista_puntajes = []
    
    # Obtenemos la fecha y hora actual
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. LEER LOS PUNTAJES ANTERIORES (Parsing complejo)
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "r", encoding="utf-8") as f:
            lineas = f.readlines()
            
            for linea in lineas:
                # Saltamos las líneas que no sean de datos (como el título)
                if "TOP" not in linea:
                    continue
                
                try:
                    # El formato es: TOP 1. JUGADOR: Albert | FECHA: ... | INTENTOS: 46 | ...
                    # Usamos split('|') para separar por las barras
                    partes = linea.split("|")
                    
                    # Extraemos el nombre (limpiando el "TOP X. JUGADOR: ")
                    parte_nombre = partes[0].split(":")[1].strip()
                    
                    # Extraemos la fecha
                    parte_fecha = partes[1].split("FECHA:")[1].strip()
                    
                    # Extraemos los intentos (limpiando " INTENTOS: ")
                    parte_intentos = int(partes[2].split(":")[1].strip())
                    
                    # Guardamos en nuestra lista temporal
                    lista_puntajes.append({
                        "nombre": parte_nombre,
                        "fecha": parte_fecha,
                        "intentos": parte_intentos
                    })
                except:
                    pass # Si alguna línea está mal escrita, la ignoramos

    # 2. AGREGAR EL NUEVO JUGADOR A LA LISTA
    lista_puntajes.append({
        "nombre": nombre_jugador,
        "fecha": fecha_actual,
        "intentos": intentos_realizados
    })

    # 3. ORDENAR POR INTENTOS (Menor es mejor)
    lista_puntajes.sort(key=lambda x: x['intentos'])

    # 4. QUEDARSE SOLO CON LOS 3 MEJORES
    top_3 = lista_puntajes[:3]

    # 5. GUARDAR CON EL FORMATO BONITO Y TÍTULO
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(" ========================= 🏆 MEJORES PUNTAJES 🏆 ========================= \n")
        
        # Escribimos cada jugador con su número de TOP (indice + 1)
        for i, puntaje in enumerate(top_3):
            # Aquí creamos la cadena exacta que pediste
            linea_formateada = (
                f"TOP {i+1}. JUGADOR: {puntaje['nombre']} | "
                f"FECHA: {puntaje['fecha']} | "
                f"INTENTOS: {puntaje['intentos']} | \n"
            )
            f.write(linea_formateada)
            
    print("¡Top 3 actualizado correctamente!")

    
if __name__ == "__main__":
    main()

print()
