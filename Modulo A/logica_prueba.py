import logica
import datos
import random

print("--------------------- BIENVENIDO A !BATALLA NAVAL! ---------------------\n!Ataca los barcos enemigos con coordenadas!\n")
name = input("Con que nombre deseas registarte? ")

def main():
    #Tablero del Usuario lleno de agua
    mi_tablero = logica.matriz_agua()
    
    #Tablero de la CPU lleno de agua
    cpu_tablero = logica.matriz_agua()
    
    #Tablero del Usuario para sus disparos
    tablero_disparos = logica.matriz_disparos()
    
    #Flota en el Tablero del Usuario
    logica.generar_flota_random(mi_tablero, datos.flota)
    
    #Flota en el Tablero de la CPU
    logica.generar_flota_random(cpu_tablero, datos.flota)
    
    #Mostrando al usuario su tablero con su flota
    print(f"Este es tu tablero con barcos, {name}:")
    for fila in mi_tablero:
        print(fila)
    print()
    
    #Mostrando al usuario su tablero de disparos
    print("Y este es tu escaner de disparos:")
    for fila in tablero_disparos:
        print(fila)
    print()
    
    #---------- TRAMPA PARA VERFIFICAR TABLERO DEL CPU ----------
    print("!SHHHHHHH! Este es el tablero del CPU:")
    for fila in cpu_tablero:
        print(fila)
    print()
    
    valido = False
    while not valido:
        try:
            print("!Ataca la flota rival!")
            f = int(input(" - Fila (0-9): "))
            c = int(input(" - Columna (0-9): "))
            
            if logica.coordenada_valida(f, c):
                tablero_disparos[f][c] = 2 #Registramos el disparo
                if cpu_tablero[f][c] != "0":
                    print("\n¡BOOM! Le diste a un barco. 💥")
                    tablero_disparos[f][c] = "*"
                else:
                    print("\n¡FALLIDO! Diste con el agua. 🌊")
                    tablero_disparos[f][c] = "X"
                valido = True #Esto rompe el bucle while
                    
        except ValueError:
            print("Error: ¡Debes ingresar un número entero!")#Error que se daria si el usuario ingresa al que no sea un entero, y como valido es igual a False aun, se seguiria pidiendo una coordenada valida
    
    print()        
    # Imprimir el resultado final del tablaro de Disparos
    for fila in tablero_disparos:
        print(fila)
    print()
    
if __name__ == "__main__":
    main()
    
    