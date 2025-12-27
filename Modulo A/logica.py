import datos
import pygame
import random

#Responsable de este módulo: ALBERT

 #---------- FUNCION PARA GENERAR MATRIZ 10*10 DE AGUA(0)---------------
def matriz_agua(): 
    return [[datos.agua for _ in range(datos.columnas)] for _ in range(datos.filas)] #Usando comprension de lista para generar la matriz con agua(0) y retornar el valor a main


 #---------- FUNCION PARA GENERAR MATRIZ 10*10 DE DISPAROS---------------
def matriz_disparos():
    # El proceso es igual que la matriz_agua
    tablero_disparos = []
    for f in range(datos.filas):
        fila = []
        for c in range(datos.columnas):
            fila.append(datos.agua) 
        tablero_disparos.append(fila)
    return tablero_disparos


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
    #1. Verificar si se sale del tablero
    if orientacion == "H": #si la orientacion es igual a "H"
        if c + tamaño > datos.columnas:
            return False
    else: #si la orientacion es igual a "V"
        if f + tamaño > datos.filas:
            return False

    #2. Verificar si hay otros barcos en el camino
    for i in range(tamaño):
        if orientacion == "H":
            if tablero[f][c + i] != datos.agua:
                return False
        else:
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
        
    


#-------------- PROGRAMA PRINCIPAL ----------------- Lo continue en otro modulo por comodidad
def main():
    tablero_agua = matriz_agua()
    for filas in tablero_agua:
        print(filas)#Aca se llama a la funcion matriz_agua para recorrer sus filas y que se imprima en su formato, nose si se necesita que se imprima en la terminal pero por ciacaso =)
    print()
        
    tablero_disparos = matriz_disparos()
    
    valido = False
    while not valido:
        try:
            f = int(input("Fila (0-9): "))
            c = int(input("Columna (0-9): "))
            
            if coordenada_valida(f, c):
                tablero_disparos[f][c] = 2 #Registramos el disparo
                valido = True #Esto rompe el bucle while
        except ValueError:
            print("Error: ¡Debes ingresar un número entero!")#Error que se daria si el usuario ingresa al que no sea un entero, y como valido es igual a False aun, se seguiria pidiendo una coordenada valida
    
    print()        
    # Imprimir el resultado final del tablaro de Disparos
    for fila in tablero_disparos:
        print(fila)
    print()
    
    mi_tablero = matriz_agua() # Creamos el tablero del usuario "vacio"(lleno de pura agua[0])
    generar_flota_random(mi_tablero, datos.flota) #Llenamos el tablero con la flota
    
    print("Tu tablero con barcos:")
    for fila in mi_tablero:
        print(fila)

    
if __name__ == "__main__":
    main()

print()

