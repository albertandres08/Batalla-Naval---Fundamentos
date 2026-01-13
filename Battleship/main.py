import pygame
import sys
import datos   
import logica
import copy
import datetime
import os
import escenas

# --- CONFIGURACIÓN INICIAL ---
pygame.init()

# Colores RGB
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL_MAR = (50, 150, 200)
VERDE_EXITO = (0, 200, 100)

#Fuente
fuente = pygame.font.SysFont("Arial", 22, bold=True)
fuente_grande = pygame.font.SysFont("Arial", 40, bold=True)

ANCHO_PANTALLA = 960 
ALTO_PANTALLA = 540
ventana = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))

TAMANO_CELDA = 40 
MARGEN = 5

# SONIDOS
try:
    sonido_boom = pygame.mixer.Sound("assets/explosion.mp3")
    sonido_agua = pygame.mixer.Sound("assets/splash.mp3")
except:
    sonido_boom = None
    sonido_agua = None

def ingresar_nombre(ventana):
    pygame.display.set_caption(f"Batalla Naval")
    nombre = ""
    escribiendo = True
    COLOR_FONDO = (20, 20, 20)
    COLOR_TEXTO = (0, 255, 200)

    while escribiendo:
        ventana.fill(COLOR_FONDO)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN: 
                    if len(nombre) > 0: escribiendo = False
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    if len(nombre) < 12: nombre += evento.unicode

        txt_instruccion = fuente.render("INGRESA TU NOMBRE Y PULSA ENTER:", True, (150, 150, 150))
        txt_nombre = fuente.render(nombre, True, COLOR_TEXTO)
        
        rect_ins = txt_instruccion.get_rect(center=(ANCHO_PANTALLA//2, ALTO_PANTALLA//2 - 50))
        rect_nom = txt_nombre.get_rect(center=(ANCHO_PANTALLA//2, ALTO_PANTALLA//2 + 20))
        
        ventana.blit(txt_instruccion, rect_ins)
        ventana.blit(txt_nombre, rect_nom)
        pygame.draw.rect(ventana, COLOR_TEXTO, (ANCHO_PANTALLA//2 - 150, ALTO_PANTALLA//2 - 10, 300, 60), 2)
        pygame.display.flip()
        
    return nombre

def guardar_historial(nombre, intentos, resultado):
    try:
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"JUGADOR: {nombre} | FECHA: {fecha} | INTENTOS: {intentos} | RESULTADO: {resultado}\n"
        with open("historial.txt", "a") as archivo:
            archivo.write(linea)
    except Exception as e:
        print(f"Error guardando archivo: {e}")

# --- BUCLE PRINCIPAL DEL JUEGO ---
def main():
    nombre_jugador = ingresar_nombre(ventana)
    pygame.display.set_caption(f"Batalla Naval - Jugador: {nombre_jugador}")

    escena_actual = 0  
    max_escenas = 3    
    
    while True:
        # 1. MOSTRAR HISTORIA
        escenas.mostrar_escena(ventana, fuente, escena_actual)

        # 2. SETUP NIVEL
        flota_viva = copy.deepcopy(datos.flota)
        vidas_restantes = datos.sin_flota 
        intentos_realizados = 0
        tablero_logico = logica.matriz_agua()
        logica.generar_flota_random(tablero_logico, flota_viva)

        mensaje_juego = f"Capítulo {escena_actual + 1}: ¡Busca los barcos enemigos!" 
        
        reloj = pygame.time.Clock()
        corriendo_nivel = True
        juego_terminado = False 
        
        # 3. JUGAR NIVEL
        while corriendo_nivel:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    if not juego_terminado:
                        guardar_historial(nombre_jugador, intentos_realizados, "ABANDONO")
                    pygame.quit(); sys.exit()
                
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if juego_terminado: continue 

                    posicion = pygame.mouse.get_pos()
                    x_mouse = posicion[0]
                    y_mouse = posicion[1]
            
                    if y_mouse < (ALTO_PANTALLA - 100): 
                        fila_clic = (y_mouse - MARGEN) // (TAMANO_CELDA + MARGEN)
                        columna_clic =  (x_mouse - MARGEN) // (TAMANO_CELDA + MARGEN)
                        
                        if logica.coordenada_valida(fila_clic, columna_clic):
                            contenido = tablero_logico[fila_clic][columna_clic]

                            if contenido == datos.tocado or contenido == datos.fallo:
                                mensaje_juego = "¡Ya disparaste ahí! Busca otro sitio." 
                            else:
                                intentos_realizados += 1 
                                if contenido == datos.agua:
                                    mensaje_juego = "¡AGUA! No había nada." 
                                    tablero_logico[fila_clic][columna_clic] = datos.fallo
                                    if sonido_agua: sonido_agua.play()
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
                                    
                                    if vidas_restantes == 0 and not juego_terminado:
                                        mensaje_juego = "¡NIVEL COMPLETADO! 🎉"
                                        juego_terminado = True
                                        guardar_historial(nombre_jugador, intentos_realizados, f"GANO NIVEL {escena_actual + 1}")
                                        logica.guardar_mejor_puntaje(nombre_jugador, intentos_realizados)

            # DIBUJAR
            ventana.fill(NEGRO) 
            for f in range(datos.filas):
                for c in range(datos.columnas):
                    valor = tablero_logico[f][c]
                    if valor == datos.tocado: color = datos.color_tocado 
                    elif valor == datos.fallo: color = datos.color_fallo 
                    else: color = AZUL_MAR 
                    x = (MARGEN + TAMANO_CELDA) * c + MARGEN
                    y = (MARGEN + TAMANO_CELDA) * f + MARGEN
                    pygame.draw.rect(ventana, color, [x, y, TAMANO_CELDA, TAMANO_CELDA])

            texto_imagen = fuente.render(mensaje_juego, True, BLANCO)
            ventana.blit(texto_imagen, (20, ALTO_PANTALLA - 70))
            texto_intentos = fuente.render(f"Tiros: {intentos_realizados}", True, BLANCO)
            ventana.blit(texto_intentos, (ANCHO_PANTALLA - 120, ALTO_PANTALLA - 70))
            texto_cap = fuente.render(f"CAPÍTULO {escena_actual + 1}", True, (100, 100, 100))
            ventana.blit(texto_cap, (ANCHO_PANTALLA - 140, 20))

            pygame.display.flip()
            reloj.tick(60)

            # TRANSICIÓN / FINAL
            if juego_terminado:
                pygame.time.delay(2000)
                escena_actual += 1
                
                # --- AQUÍ ESTÁ EL CAMBIO PRINCIPAL ---
                if escena_actual >= max_escenas:
                    # Mostrar pantalla final
                    ventana.fill(NEGRO)
                    txt_fin = fuente_grande.render("¡MISIÓN CUMPLIDA!", True, VERDE_EXITO)
                    txt_sub = fuente.render("Has salvado los ODS. Volviendo al menú...", True, BLANCO)
                    
                    rect_fin = txt_fin.get_rect(center=(ANCHO_PANTALLA//2, ALTO_PANTALLA//2 - 20))
                    rect_sub = txt_sub.get_rect(center=(ANCHO_PANTALLA//2, ALTO_PANTALLA//2 + 30))
                    
                    ventana.blit(txt_fin, rect_fin)
                    ventana.blit(txt_sub, rect_sub)
                    pygame.display.flip()
                    
                    pygame.time.delay(4000) # Esperar 4 segundos leyendo el mensaje
                    
                    return # <--- ESTO DEVUELVE AL MENÚ (sale de main)
                
                corriendo_nivel = False 

if __name__ == "__main__":
    main()
