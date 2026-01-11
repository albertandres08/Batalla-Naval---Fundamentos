import pygame
import sys
import datos   
import logica
import copy
import datetime # <--- NUEVO: Para la fecha y hora

# --- CONFIGURACIÓN INICIAL ---
pygame.init()

# Colores RGB
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL_MAR = (50, 150, 200)

#Fuente definida al inicio para que no haya problema si se usa en cualquier parte del programa
fuente = pygame.font.SysFont("Arial", 22, bold=True)

#Tamaño de todas las pantallas del juego
ANCHO_PANTALLA = 960 #Cambio de resolución ---> Más espacio para texto y gráficos
ALTO_PANTALLA = 540
ventana = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))

# Tamaño de la celda y margen
TAMANO_CELDA = 40 
MARGEN = 5

# INICIAR EL MIXER Y CARGAR SONIDOS
pygame.mixer.init()
# Declarando los Sonidos
# (Nota: Asegúrate de que los archivos estén en la carpeta)
try:
    sonido_boom = pygame.mixer.Sound("Battleship/assets/explosion.mp3")
    sonido_agua = pygame.mixer.Sound("Battleship/assets/splash.mp3")
except:
    print("Advertencia: No se encontraron los audios. El juego seguirá sin sonido.")
    sonido_boom = None
    sonido_agua = None

# --- FUNCIÓN NUEVA: INGRESAR NOMBRE ---
def ingresar_nombre(ventana): #Función para pedir nombre en pantalla

    pygame.display.set_caption(f"Batalla Naval")

    nombre = ""
    escribiendo = True
    
    # Colores locales
    COLOR_FONDO = (20, 20, 20)
    COLOR_TEXTO = (0, 255, 200)

    while escribiendo:
        ventana.fill(COLOR_FONDO)
        
        # 1. Gestionar Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN: # ENTER para terminar
                    if len(nombre) > 0: # Solo salir si escribió algo
                        escribiendo = False
                elif evento.key == pygame.K_BACKSPACE: # Borrar
                    nombre = nombre[:-1]
                else:
                    # Limitar a 12 caracteres para que quepa bien
                    if len(nombre) < 12:
                        nombre += evento.unicode

        # 2. Renderizar Elementos
        txt_instruccion = fuente.render("INGRESA TU NOMBRE Y PULSA ENTER:", True, (150, 150, 150))
        txt_nombre = fuente.render(nombre, True, COLOR_TEXTO)
        
        # 3. Dibujar en la superficie
        # Centramos el texto horizontalmente
        rect_ins = txt_instruccion.get_rect(center=(ANCHO_PANTALLA//2, ALTO_PANTALLA//2 - 50))
        rect_nom = txt_nombre.get_rect(center=(ANCHO_PANTALLA//2, ALTO_PANTALLA//2 + 20))
        
        ventana.blit(txt_instruccion, rect_ins)
        ventana.blit(txt_nombre, rect_nom)

        # Dibujar un rectangulo decorativo para el nombre
        pygame.draw.rect(ventana, COLOR_TEXTO, (ANCHO_PANTALLA//2 - 150, ALTO_PANTALLA//2 - 10, 300, 60), 2)

        pygame.display.flip()
        
    return nombre

# --- FUNCIÓN NUEVA: GUARDAR HISTORIAL ---
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

# --- BUCLE PRINCIPAL DEL JUEGO ---
def main():
    # --- 1. PEDIR NOMBRE (Requerimiento PDF) --- EDITADO
    #print("\n" + "="*30) ### anterior
    #nombre_jugador = input(" INGRESA TU NOMBRE: ") ### anterior
    #print("="*30 + "\n") ### anterior
    
    nombre_jugador = ingresar_nombre(ventana)

    # 1. SETUP DE DATOS
    flota_viva = copy.deepcopy(datos.flota)
    vidas_restantes = datos.sin_flota 

    # Variable para contar disparos (Requerimiento PDF)
    intentos_realizados = 0

    # 2. SETUP DE VENTANA ### MOVIDO ARRIBA PARA MAYOR CONVENIENCIA + CAMBIAR RESOLUCIÓN
    #ANCHO_PANTALLA = (TAMANO_CELDA + MARGEN) * datos.columnas + MARGEN ### anterior
    #ALTO_PANTALLA = ((TAMANO_CELDA + MARGEN) * datos.filas + MARGEN) + 100 ### anterior

    #ventana = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))

    pygame.display.set_caption(f"Batalla Naval - Jugador: {nombre_jugador}") #Actualizar título
    
    reloj = pygame.time.Clock()

    #fuente = pygame.font.SysFont("Arial", 22, bold=True) <--- MOVIDO AL INICIO
    mensaje_juego = "¡Busca los barcos enemigos! Haz clic." 

    # Generamos el tablero lógico
    tablero_logico = logica.matriz_agua()
    logica.generar_flota_random(tablero_logico, flota_viva)
    
    corriendo = True
    juego_terminado = False # Para no guardar dos veces
    
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                # Si cierra antes de ganar, guardamos como ABANDONO
                if not juego_terminado:
                    guardar_historial(nombre_jugador, intentos_realizados, "ABANDONO")
                corriendo = False
            
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if juego_terminado: continue # Si terminó, bloqueamos clics

                posicion = pygame.mouse.get_pos()
                x_mouse = posicion[0]
                y_mouse = posicion[1]
        
                if y_mouse < (ALTO_PANTALLA - 100): 
                    fila_clic = (y_mouse - MARGEN) // (TAMANO_CELDA + MARGEN)
                    columna_clic =  (x_mouse - MARGEN) // (TAMANO_CELDA + MARGEN)
                    
                    if logica.coordenada_valida(fila_clic, columna_clic):
                        contenido = tablero_logico[fila_clic][columna_clic]

                        # A. ¿Repetido?
                        if contenido == datos.tocado or contenido == datos.fallo:
                            mensaje_juego = "¡Ya disparaste ahí! Busca otro sitio." 

                        # SI ES UN TIRO NUEVO (AGUA O BARCO)
                        else:
                            intentos_realizados += 1 # Sumamos intento

                            # B. ¿Agua?
                            if contenido == datos.agua:
                                mensaje_juego = "¡AGUA! No había nada." 
                                tablero_logico[fila_clic][columna_clic] = datos.fallo
                                if sonido_agua: sonido_agua.play()
                            
                            # C. ¡Barco!
                            else:
                                mensaje_juego = "¡IMPACTO CONFIRMADO! 💥"
                                if sonido_boom: sonido_boom.play()
                                
                                for barco in flota_viva:
                                    if barco["simbolo"] == contenido:
                                        barco["hundido"] -= 1
                                        if barco["hundido"] == 0:
                                            mensaje_juego = f"¡HUNDISTE UN {barco['nombre'].upper()}! 💀"
                                        break 

                                tablero_logico[fila_clic][columna_clic] = datos.tocado
                                vidas_restantes -= 1
                                
                                if vidas_restantes == 0:
                                    mensaje_juego = "¡VICTORIA! FLOTA HUNDIDA 🎉"
                                    # Guardamos la victoria
                                    guardar_historial(nombre_jugador, intentos_realizados, "GANO")
                                    juego_terminado = True
                    else:
                        pass 
                else:
                    pass 

        ventana.fill(NEGRO) 

        for f in range(datos.filas):
            for c in range(datos.columnas):
                valor = tablero_logico[f][c]

                if valor == datos.tocado:
                    color = datos.color_tocado 
                elif valor == datos.fallo:
                    color = datos.color_fallo 
                else:
                    color = AZUL_MAR 
                    
                x = (MARGEN + TAMANO_CELDA) * c + MARGEN
                y = (MARGEN + TAMANO_CELDA) * f + MARGEN
                pygame.draw.rect(ventana, color, [x, y, TAMANO_CELDA, TAMANO_CELDA])

        texto_imagen = fuente.render(mensaje_juego, True, BLANCO)
        ventana.blit(texto_imagen, (20, ALTO_PANTALLA - 70))
        
        # (Opcional) Mostrar intentos en pantalla
        texto_intentos = fuente.render(f"Tiros: {intentos_realizados}", True, BLANCO)
        ventana.blit(texto_intentos, (ANCHO_PANTALLA - 120, ALTO_PANTALLA - 70))

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
