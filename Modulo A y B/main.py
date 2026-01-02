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

# Tamaño de la celda y margen
TAMANO_CELDA = 40 
MARGEN = 5

# INICIAR EL MIXER Y CARGAR SONIDOS
pygame.mixer.init()
# Declarando los Sonidos
# (Nota: Asegúrate de que los archivos estén en la carpeta)
try:
    sonido_boom = pygame.mixer.Sound("explosion.mp3")
    sonido_agua = pygame.mixer.Sound("splash.mp3")
except:
    print("Advertencia: No se encontraron los audios. El juego seguirá sin sonido.")
    sonido_boom = None
    sonido_agua = None

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
    # --- 1. PEDIR NOMBRE (Requerimiento PDF) ---
    print("\n" + "="*30)
    nombre_jugador = input(" INGRESA TU NOMBRE: ")
    print("="*30 + "\n")

    # 1. SETUP DE DATOS
    flota_viva = copy.deepcopy(datos.flota)
    vidas_restantes = datos.sin_flota 

    # Variable para contar disparos (Requerimiento PDF)
    intentos_realizados = 0

    # 2. SETUP DE VENTANA
    ANCHO_PANTALLA = (TAMANO_CELDA + MARGEN) * datos.columnas + MARGEN
    ALTO_PANTALLA = ((TAMANO_CELDA + MARGEN) * datos.filas + MARGEN) + 100 

    ventana = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption(f"Batalla Naval - Jugador: {nombre_jugador}")
    
    reloj = pygame.time.Clock()

    fuente = pygame.font.SysFont("Arial", 22, bold=True)
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