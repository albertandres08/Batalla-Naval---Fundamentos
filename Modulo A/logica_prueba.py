import logica
import datos
import pygame
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
    
    #Tablero de la CPU para sus disparos
    cpu_tablero_disparos = logica.matriz_disparos()
    
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
    
    #"Haciendo trampa" para mostrar el tablero de la CPU
    print("!SHHHHHHH! Este es el tablero del CPU:")
    for fila in cpu_tablero:
        print(fila)
    print()
    
    game_over = False
    
    while game_over == False:
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
                    simbolo = cpu_tablero[f][c]
                    cpu_tablero[f][c] = "*"
                    for barco in datos.flota:
                        if barco["simbolo"] == simbolo:
                            barco["hundido"] -= 1 #ERORESSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
                            datos.sin_flota -= 1
                            logica.barco_hundido(barco["hundido"], barco)
                            break
                    logica.tablero_sin_barcos(datos.sin_flota)
                else:
                    print("\n¡FALLIDO! Diste con el agua. 🌊")
                    tablero_disparos[f][c] = "X"
                valido = True #Esto rompe el bucle while
            
                print("\n!Cuidado! Ahora es el turno de la CPU.\n") 
                f = random.randint(0, datos.filas - 1)
                c = random.randint(0, datos.columnas - 1)
                if mi_tablero[f][c] != "0":
                    simbolo = mi_tablero[f][c]
                    print(f"La CPU ha atacado la posición ({f}, {c}) y te ha dado. 💥\n")
                    mi_tablero[f][c] = "*"
                    for barco in datos.flota:
                        if barco["simbolo"] == simbolo:
                            barco["hundido"] -= 1
                            logica.barco_hundido(barco["hundido"], barco)
                            break
                else:
                    print(f"La CPU ha atacado la posición ({f}, {c}) y ha fallado. 🌊\n")
                    mi_tablero[f][c] = "X"
                
            except ValueError:
                print("Error: ¡Debes ingresar un número entero!")#Error que se daria si el usuario ingresa al que no sea un entero, y como valido es igual a False aun, se seguiria pidiendo una coordenada valida
    
    print()        
    # Imprimir el resultado final del tablaro de Disparos
    for fila in tablero_disparos:
        print(fila)
    print()
    
if __name__ == "__main__":
    main()

    
