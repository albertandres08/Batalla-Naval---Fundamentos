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
AZUL_MAR = (50, 150, 200, 180) # Añadimos un poco de transparencia
VERDE_EXITO = (0, 200, 100)

# Fuente
fuente = pygame.font.SysFont("Arial", 22, bold=True)
fuente_grande = pygame.font.SysFont("Arial", 40, bold=True)

ANCHO_PANTALLA = 960 
ALTO_PANTALLA = 540
ventana = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))

TAMANO_CELDA = 40 
MARGEN = 5

# --- CARGA DE ACTIVOS VISUALES ADICIONALES ---

# 1. Iconos de disparo (Tamaño 40x40 para encajar en la celda)
explosion_img = pygame.image.load("assets/tablero_explosion.png") 
explosion_img = pygame.transform.scale(explosion_img, (TAMANO_CELDA, TAMANO_CELDA))

agua_img = pygame.image.load("assets/tablero_agua.png") 
agua_img = pygame.transform.scale(agua_img, (TAMANO_CELDA+10, TAMANO_CELDA+10))

# 2. Fondo (Usamos el mismo de escenas)
fondo_juego = pygame.image.load("assets/Fondo-Barco.png")
fondo_juego = pygame.transform.scale(fondo_juego, (ANCHO_PANTALLA, ALTO_PANTALLA))

# 3. Importar personajes para el feedback visual
personajes = {
    "viejo": {
        "normal": pygame.image.load("assets/viejo_normal.png"),
        "alegre": pygame.image.load("assets/viejo_alegre.png"),
        "molesto": pygame.image.load("assets/viejo_molesto.png")
    },
    "niña": {
        "normal": pygame.image.load("assets/niña_normal.png"),
        "alegre": pygame.image.load("assets/niña_alegre.png"),
        "molesto": pygame.image.load("assets/niña_molesta.png")
    }
}

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
                pygame.quit(); sys.exit()
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

def main():
    nombre_jugador = ingresar_nombre(ventana)
    pygame.display.set_caption(f"Batalla Naval - Jugador: {nombre_jugador}")

    escena_actual = 0  
    max_escenas = 3    
    
    while True:
        escenas.mostrar_escena(ventana, fuente, escena_actual)

        flota_viva = copy.deepcopy(datos.flota)
        vidas_restantes = datos.sin_flota 
        intentos_realizados = 0
        tablero_logico = logica.matriz_agua()
        logica.generar_flota_random(tablero_logico, flota_viva)

        mensaje_juego = f"Capítulo {escena_actual + 1}: ¡Busca los barcos enemigos!" 
        
        # Variables para efectos visuales
        efecto_icono = None
        pos_efecto = (0, 0)
        tiempo_efecto = 0  # Guardará el momento en que se activó
        duracion_visual = 800 # Milisegundos que dura el icono y la expresión
        expresion_personaje = "normal"
        
        # Determinar qué personaje mostrar según el nivel
        tipo_pj = "niña" if escena_actual == 1 else "viejo"

        reloj = pygame.time.Clock()
        corriendo_nivel = True
        juego_terminado = False 
        
        while corriendo_nivel:
            tiempo_actual = pygame.time.get_ticks()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    if not juego_terminado:
                        guardar_historial(nombre_jugador, intentos_realizados, "ABANDONO")
                    pygame.quit(); sys.exit()
                
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if juego_terminado: continue 

                    posicion = pygame.mouse.get_pos()
                    x_mouse, y_mouse = posicion
            
                    if y_mouse < (ALTO_PANTALLA - 100): 
                        fila_clic = (y_mouse - MARGEN) // (TAMANO_CELDA + MARGEN)
                        columna_clic =  (x_mouse - MARGEN) // (TAMANO_CELDA + MARGEN)
                        
                        if logica.coordenada_valida(fila_clic, columna_clic):
                            contenido = tablero_logico[fila_clic][columna_clic]

                            if contenido != datos.tocado and contenido != datos.fallo:
                                intentos_realizados += 1
                                tiempo_efecto = tiempo_actual # Iniciamos temporizador
                                pos_efecto = (MARGEN + (TAMANO_CELDA + MARGEN) * columna_clic, 
                                              MARGEN + (TAMANO_CELDA + MARGEN) * fila_clic)
                                
                                if contenido == datos.agua:
                                    mensaje_juego = "¡AGUA! No había nada." 
                                    tablero_logico[fila_clic][columna_clic] = datos.fallo
                                    efecto_icono = agua_img
                                    expresion_personaje = "alegre" # Se alegra si fallas
                                    if sonido_agua: sonido_agua.play()
                                else:
                                    mensaje_juego = "¡IMPACTO CONFIRMADO! 💥"
                                    efecto_icono = explosion_img
                                    expresion_personaje = "molesto" # Se molesta si aciertas
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

            # Resetear expresión si pasó el tiempo
            if tiempo_actual - tiempo_efecto > duracion_visual:
                expresion_personaje = "normal"
                efecto_icono = None

            # --- DIBUJAR ---
            # 1. Fondo
            ventana.blit(fondo_juego, (0,0))
            
            # 2. Personaje (Feedback)
            img_pj = personajes[tipo_pj][expresion_personaje]
            ventana.blit(img_pj, (550, 100)) # Posicionado a la derecha del tablero

            # 3. Tablero
            for f in range(datos.filas):
                for c in range(datos.columnas):
                    valor = tablero_logico[f][c]
                    x = (MARGEN + TAMANO_CELDA) * c + MARGEN
                    y = (MARGEN + TAMANO_CELDA) * f + MARGEN
                    
                    if valor == datos.tocado: color = datos.color_tocado 
                    elif valor == datos.fallo: color = datos.color_fallo 
                    else: color = AZUL_MAR 
                    
                    # Dibujar cuadro con borde para que se vea mejor sobre el fondo
                    pygame.draw.rect(ventana, color, [x, y, TAMANO_CELDA, TAMANO_CELDA])
                    pygame.draw.rect(ventana, (255,255,255), [x, y, TAMANO_CELDA, TAMANO_CELDA], 1)

            # 4. Dibujar Icono de efecto temporal
            if efecto_icono and tiempo_actual - tiempo_efecto < duracion_visual:
                ventana.blit(efecto_icono, pos_efecto)

            # 5. UI (Textos)
            # Fondo para los textos inferiores para legibilidad
            pygame.draw.rect(ventana, (0,0,0,150), (0, ALTO_PANTALLA - 100, ANCHO_PANTALLA, 100))
            
            texto_imagen = fuente.render(mensaje_juego, True, (BLANCO))
            ventana.blit(texto_imagen, (20, ALTO_PANTALLA - 70))
            texto_intentos = fuente.render(f"Tiros: {intentos_realizados}", True, BLANCO)
            ventana.blit(texto_intentos, (ANCHO_PANTALLA - 120, ALTO_PANTALLA - 70))
            texto_cap = fuente.render(f"CAPÍTULO {escena_actual + 1}", True, (0, 0, 0))
            ventana.blit(texto_cap, (ANCHO_PANTALLA - 140, 20))

            pygame.display.flip()
            reloj.tick(60)

            if juego_terminado:
                pygame.time.delay(2000)
                escena_actual += 1
                
                if escena_actual >= max_escenas:
                    ventana.fill(NEGRO)
                    txt_fin = fuente_grande.render("¡MISIÓN CUMPLIDA!", True, VERDE_EXITO)
                    txt_sub = fuente.render("Has salvado los ODS. Volviendo al menú...", True, BLANCO)
                    rect_fin = txt_fin.get_rect(center=(ANCHO_PANTALLA//2, ALTO_PANTALLA//2 - 20))
                    rect_sub = txt_sub.get_rect(center=(ANCHO_PANTALLA//2, ALTO_PANTALLA//2 + 30))
                    ventana.blit(txt_fin, rect_fin)
                    ventana.blit(txt_sub, rect_sub)
                    pygame.display.flip()
                    pygame.time.delay(4000) 
                    return 
                
                corriendo_nivel = False 

if __name__ == "__main__":
    main()
