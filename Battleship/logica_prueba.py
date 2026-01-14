import logica, datos, pygame, random

#Esta es una version beta de nuestro juego en en terminal que se uso como guia para hacer el fronted y la interfaz del juego =)
print("--------------------- BIENVENIDO A !BATALLA NAVAL! ---------------------\n!Ataca los barcos enemigos con coordenadas!\n")
name = input("Con que nombre deseas registarte? ")#Bienvenida al Usuario y Registro

#Programa Principal importando las funciones del modulo "logica"
def main():
    #Tablero del Usuario lleno de agua
    mi_tablero = logica.matriz_agua()
    
    #Tablero de la CPU lleno de agua
    cpu_tablero = logica.matriz_agua()
    
    #Tablero del Usuario para sus disparos
    tablero_disparos = logica.matriz_disparos()
    
    #Tablero de la CPU para sus disparos
    cpu_tablero_disparos = logica.matriz_disparos()#NECESARIO?(SOS)
    
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
        while not valido: #Condicionales para que el juego se mantenga y la validacion de los inputs
            try:
                print("!Ataca la flota rival!")
                f = int(input(" - Fila (0-9): "))
                c = int(input(" - Columna (0-9): "))
            
                if logica.coordenada_valida(f, c):
                    tablero_disparos[f][c] = 2 #Registramos el disparo
                    if cpu_tablero[f][c] != "🌊":
                        print("\n¡BOOM! Le diste a un barco. 💥")#Como le dio, se modifican los valores en el tablero de disparos del ususario 
                        tablero_disparos[f][c] = "💥"
                        cpu_tablero[f][c] = "💥"
                        simbolo = cpu_tablero[f][c]
                        for barco in datos.flota:
                            if barco["simbolo"] == simbolo:
                                barco["hundido"] -= 1#Se modifica el valor de hundido para el barco especifico
                                datos.sin_flota -= 1#Se modifica el valor de hundido para todos los barcos
                                logica.barco_hundido(barco["hundido"], barco)#Verfificando que el barco no este hundido
                                break
                    else:
                        print("\n¡FALLIDO! Diste con el agua. 🌊✖️")#Si fallo, se modifican tambien los valores en el tablero de disparos del ususario
                        tablero_disparos[f][c] = "✖️"
                        cpu_tablero[f][c] = "✖️"
                    valido = True#Esto rompe el bucle while de validacion de inputs
                    
                    if logica.tablero_sin_barcos(datos.sin_flota):
                            print("\n!GAME OVER!, !YOU WIN!\n")#Veridicacion de Victoria del Usuario
                    else:
                        #Mostrando los disparos del Usuario
                        print(f"\nAsi va tu escaner de disparos, {name}:\n")
                        for fila in tablero_disparos:
                            print(fila)
                        print()
                        #Mostrando el tablero de la CPU modificado para verificar mas rapido(haciendo trampa)
                        print(f"\nAsi va el tablero de la CPU:\n")
                        for fila in cpu_tablero:
                            print(fila)
                        print()
                        
                    print("\n!Cuidado! Ahora es el turno de la CPU.\n")
                    f = random.randint(0, datos.filas - 1)
                    c = random.randint(0, datos.columnas - 1)#La Cpu ataca a lo random(Facil)
                    if mi_tablero[f][c] != "🌊":
                        simbolo = mi_tablero[f][c]
                        print(f"La CPU ha atacado la posición ({f}, {c}) y te ha dado. 💥\n")
                        cpu_tablero_disparos[f][c] = "💥"
                        for barco in datos.flota:
                            if barco["simbolo"] == simbolo:
                                barco["hundido"] -= 1
                                logica.barco_hundido(barco["hundido"], barco)
                                break
                    else:
                        print(f"La CPU ha atacado la posición ({f}, {c}) y ha fallado. 🌊✖️\n")
                        cpu_tablero_disparos[f][c] = "✖️"
                                #Hasta aca la CPU indica que coordenada ataco y si le dio o no
                    if logica.tablero_sin_barcos(datos.sin_flota):
                        print("\n!GAME OVER!, !YOU LOST!\n")#Veridicacion de Victoria de la CPU
            except ValueError:
                print("Error: ¡Debes ingresar un número entero!")#Error que daria si el usuario ingresa al que no sea un entero, y como valido es igual a False aun, se seguiria pidiendo una coordenada valida
    
if __name__ == "__main__":
    main()
