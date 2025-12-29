#Importando todas las librerias necesarias
import pygame
import sys
import datos  
import logica
import copy
import random 

#Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL_MAR = (50, 150, 200)
ROJO_OSCURO = (100, 0, 0) 
AZUL_OSCURO = (4, 80, 165)

#Medidas
TAMANO_CELDA = 40 #el tamaño de las celdas (cuadrillas) en la matriz 10*10
MARGEN = 5 #la distancia entra cada celda en pixeles

#Calculamos la altura de UN solo tablero
ALTO_TABLERO = (TAMANO_CELDA + MARGEN) * datos.filas + MARGEN
#Con dicha formula se toma en cuenta el espacio ncesario para mostrar las celdas por filas del tablero

#Espacio en el medio para el texto (La "zona neutral")
ESPACIO_MEDIO = 100 

#Pantalla el doble de alta + espacio medio
ANCHO_PANTALLA = (TAMANO_CELDA + MARGEN) * datos.columnas + MARGEN #Aca se usa la formula para definir el ancho tomando las medidas, por ahora es casi del mismo ancho que la matriz 10*10, pero con la implemnetacion de los personajes y etxto seguro aumentara

ALTO_PANTALLA = (ALTO_TABLERO * 2) + ESPACIO_MEDIO #Con dicha formula se toma en cuenta el espacio ncesario para mostrar las celdas por filas del tablero por los 2 tablero en pantalla

# Calculamos dónde empieza a dibujarse el tablero de abajo
INICIO_Y_JUGADOR = ALTO_TABLERO + ESPACIO_MEDIO

# --- CARGAR IMÁGENES ---
#NOTA: los achivos e imagenes .AVIF no se ejecutan bien en PYGAME
#fondo_img = pygame.image.load("fondo_playa.jpg") 
#fondo_img = pygame.transform.scale(fondo_img, (ANCHO_PANTALLA, ALTO_PANTALLA))

# ------- PROGRAMA PRINCIPAL -------- 
def main():
    # --- CONFIGURACIÓN INICIAL DEL PYGAME ---
    pygame.init()

    # -------- FUENTE(TIPOGRAFIA) ---------
    fuente = pygame.font.SysFont("Bodoni MT", 22, bold=True)

    ventana = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Batalla Naval - JUGADOR vs BOT") #Declarando la pantalla con las medidas y el titulo de la ventana

    # --- SONIDOS ---
    #pygame.mixer.init()#Se declaran los sonidos que vamos a usar
    #sonido_boom = pygame.mixer.Sound("bomba.mp3")
    #sonido_agua = pygame.mixer.Sound("splash.mp3")

    reloj = pygame.time.Clock()
    
    # --- SETUP DEL JUGADOR (ABAJO EN LA VENTANA) ---
    tablero_jugador = logica.matriz_agua() #Generando el tablero con agua 10*10 del usuario
    flota_jugador = copy.deepcopy(datos.flota) #Duplicando el valor de flota para no modificar el archivo original
    logica.generar_flota_random(tablero_jugador, flota_jugador) #Generando las flotas randoms para el usuario, falta hacer que el mismo elija sus posiciones de flota
    vidas_jugador = datos.sin_flota #Variable para la condicion de victoria

    # --- SETUP DEL BOT/ENEMIGO (ARRIBA EN LA VENTANA) ---
    #Se aplica lo mismo que el de arriba
    tablero_enemigo = logica.matriz_agua()
    flota_enemigo = copy.deepcopy(datos.flota)
    logica.generar_flota_random(tablero_enemigo, flota_enemigo)
    vidas_enemigo = datos.sin_flota

    mensaje = "TU TURNO - !Ataca el tablero de ARRIBA!" #Esta seria la variable mensaje que es la que se muestra en pantalla al final
    turno_jugador = True #Variable de control de turno
    corriendo = True #Variable para el loop del juego

    while corriendo:
        for evento in pygame.event.get(): #Funcion de Pygame que hace que el click del usuario de en que pixel se hizo
            if evento.type == pygame.QUIT: #Si es afuera en la X se cierra el loop y el juego
                corriendo = False
            
            # --- LÓGICA DE DISPARO DEL JUGADOR ---
            elif evento.type == pygame.MOUSEBUTTONDOWN and turno_jugador:
                x_mouse, y_mouse = pygame.mouse.get_pos()

                if y_mouse < ALTO_TABLERO: #Validar que el clic sea en el tablero de ARRIBA
                    fila = (y_mouse - MARGEN) // (TAMANO_CELDA + MARGEN)
                    col = (x_mouse - MARGEN) // (TAMANO_CELDA + MARGEN) #(SOS) Formula para pasar del pixel del click al una posicion especifica en una fila y columba de la matriz 10*10(0-9)

                    if logica.coordenada_valida(fila, col): #Con la funcion importada, se valida si la funcion esta en el rango perimitido
                        contenido = tablero_enemigo[fila][col] #Duplicando el valor del tablero enenemigo en la variable

                        if contenido in (datos.tocado, datos.fallo): #Si el contenido es igual a un fallo o barco tocado, dira que es repetido en vez de agua
                            mensaje = "¡Ya disparaste ahí!" #Esta se hace antes que ls demas porque sino se duplicaria o cambiaria el diseño de la celda
                        else:
                            #Procesar disparo al enemigo
                            if contenido == datos.agua: #Si el contenido es igual a Agua se toma en cuenta como fallo
                                tablero_enemigo[fila][col] = datos.fallo
                                #sonido_agua.play() #Se reporduce el sonido de agua
                                mensaje = "¡FALLASTE! Turno del Bot..."
                                #pygame.time.delay(1000) #Pequeña pausa para que se note que "piensa"
                                turno_jugador = False #Pasamos turno por el fallo
                            else:
                                tablero_enemigo[fila][col] = datos.tocado #Si no es ninguna de las anterirores entonces es un barco y se reproduce el sonido
                                mensaje = "¡IMPACTO! Sigue disparando."
                                #sonido_boom.play()
                                    
                                #Igualamos la variable simbolo para ver que habia en la celda
                                simbolo = contenido 
                                    
                                for barco in flota_enemigo:
                                    if barco["simbolo"] == simbolo: #Aqui, si el simbolo en la itracion es igual al que tenemos en la variable enonces se actualiza el valor de hundido para ese barco en el diccionario copido
                                        barco["hundido"] -= 1
                                        if barco["hundido"] == 0: #Al llegar a cero, indica que se undio un barco y se muestra en pantalla
                                                mensaje = f"¡HUNDISTE UN {barco['nombre'].upper()}!"
                                        break #(SOS)
                                #Restamos la vida global fuera del for(un impacto = una vida menos)
                                vidas_enemigo -= 1
                                if vidas_enemigo == 0: #Al llegar a cero, indica que el usuario gano por hundir toda la flota rival
                                    mensaje = "¡GANASTE LA GUERRA!"
                                    turno_jugador = False

        # --- LÓGICA DE DISPARO DEL BOT (Automática) ---
        if not turno_jugador and vidas_enemigo > 0 and vidas_jugador > 0: #Condicion para que al terminar el usuario su turno, siga el bot si el usraio no juega, ni las vidas llegan a 0
            pygame.time.delay(500) #Pequeña pausa para que se note que "piensa"
            
            #Disparo random simple (Se puede mejorar luego)
            f_bot = random.randint(0, datos.filas - 1)
            c_bot = random.randint(0, datos.columnas - 1) #funciones que perimiten que el bot elija una posicion random

            #Nos aseguramos que no repita tiro(loop while simple)
            while tablero_jugador[f_bot][c_bot] in (datos.tocado, datos.fallo): #Indica que si la elecion del bot esta dentro de esas opciones, lo repita(SOS)
                f_bot = random.randint(0, datos.filas - 1)
                c_bot = random.randint(0, datos.columnas - 1)
            
            #Verificamos qué golpeó el bot en el tablero usuario
            cont_jugador = tablero_jugador[f_bot][c_bot]
            
            if cont_jugador == datos.agua:
                tablero_jugador[f_bot][c_bot] = datos.fallo
                mensaje = "El Bot falló. TU TURNO."
                turno_jugador = True #devuelve el turno
            else:
                tablero_jugador[f_bot][c_bot] = datos.tocado
                mensaje = "¡TE DIERON! El Bot dispara de nuevo."
                vidas_jugador -= 1
                if vidas_jugador == 0:
                    mensaje = "PERDISTE... TU FLOTA FUE HUNDIDA 💀" #Aca se verifica que el bot ataco y si hundio la folta del usuario se termina el juego

        # --- DIBUJADO(FONDO) ---
        #ventana.fill(ROJO_OSCURO)#, (0, INICIO_Y_JUGADOR))
        #ventana.fill(NEGRO, (INICIO_Y_JUGADOR, INICIO_Y_JUGADOR + 100))
        #ventana.fill(BLANCO, (INICIO_Y_JUGADOR+100, ALTO_PANTALLA))
        ventana.fill(AZUL_OSCURO)


        # ------- DIBUJAR TABLERO ENEMIGO (ARRIBA) ----------
        for f in range(datos.filas):
            for c in range(datos.columnas):
                val = tablero_enemigo[f][c]
                color = AZUL_MAR
                if val == datos.tocado: color = datos.color_tocado
                elif val == datos.fallo: color = datos.color_fallo
                #Dependidendo de el valor de val se cambia si es tocado o fallido con sus colores
                
                x = (MARGEN + TAMANO_CELDA) * c + MARGEN
                y = (MARGEN + TAMANO_CELDA) * f + MARGEN #(SOS) Valores de x y y  que se vam actualizando segun se iteren los bucles como una matriz normal
                pygame.draw.rect(ventana, color, [x, y, TAMANO_CELDA, TAMANO_CELDA])#Aca es donde se dibuja en pantalla los cuadros segun los para metros

        # 2. DIBUJAR TABLERO JUGADOR (ABAJO)
        #Aquí si mostramos los barcos, para que el ususario vea su flota
        for f in range(datos.filas):
            for c in range(datos.columnas):
                val = tablero_jugador[f][c]
                color = AZUL_MAR
                if val == datos.tocado: color = datos.color_tocado
                elif val == datos.fallo: color = datos.color_fallo
                elif val != datos.agua: color = (100, 100, 100) #Se aplica similar a arriba, pero aca es Gris para ver los barcos vivos si es disntinto de agua y las otras 2
                
                x = (MARGEN + TAMANO_CELDA) * c + MARGEN
                y = ((MARGEN + TAMANO_CELDA) * f + MARGEN) + INICIO_Y_JUGADOR #Se le suma para tomar en cuenta el espacio verticual usado por el tabelro d ela cpu
                pygame.draw.rect(ventana, color, [x, y, TAMANO_CELDA, TAMANO_CELDA])

        # -------- TEXTO EN EL MEDIO ------
        texto = fuente.render(mensaje, True, BLANCO)
        ventana.blit(texto, (80, ALTO_TABLERO + 40)) #En la zona negra central se muetra el mensaje segun su valor

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
ventana = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Batalla Naval")

# --- BUCLE PRINCIPAL DEL JUEGO ---
def main():
    corriendo = True
    reloj = pygame.time.Clock()

    # Generamos el tablero lógico usando TU función
    tablero_logico = logica.matriz_agua()

    while corriendo:
        # 1. Manejo de eventos (Cerrar la ventana)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        # 2. Dibujar en pantalla
        ventana.fill(NEGRO) # Fondo negro

        # Dibujar la cuadrícula
        for f in range(datos.filas):
            for c in range(datos.columnas):
                color = AZUL_MAR
                
                # Coordenadas para dibujar el rectanguito
                x = (MARGEN + TAMANO_CELDA) * c + MARGEN
                y = (MARGEN + TAMANO_CELDA) * f + MARGEN

                pygame.draw.rect(ventana, color, [x, y, TAMANO_CELDA, TAMANO_CELDA])

        # 3. Actualizar la pantalla
        pygame.display.flip()
        
        # 60 cuadros por segundo
        reloj.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()