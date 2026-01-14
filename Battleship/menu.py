import pygame, sys, botones, main
from botones import Botón 

# --- CONFIGURACIÓN INICIAL ---
pygame.init()
icono = pygame.image.load("assets/Icono-Battleship.png")
pygame.display.set_icon(icono)
ventana = pygame.display.set_mode((960,540))
pygame.display.set_caption("Battleship: Batalla Naval")
reloj = pygame.time.Clock()

# --- CARGA DE RECURSOS ---
# --- IMÁGENES DE INTRODUCCIÓN ---
logo_ucab = pygame.image.load("assets/Logo-UCAB.jpeg").convert()
logo_ucab = pygame.transform.scale(logo_ucab, (960, 540))

logo_pygame = pygame.image.load("assets/Logo-Pygame.jpeg").convert()
logo_pygame = pygame.transform.scale(logo_pygame, (960, 540))

# Superficie para el efecto de fundido (negra)
fundido = pygame.Surface((960, 540))
fundido.fill((255, 255, 255))

fondo_img = pygame.image.load("assets/Fondo-Menu.png").convert()  
fondo_img = pygame.transform.scale(fondo_img, (960,540))
fondo_oscuro_img = pygame.image.load("assets/Fondo-Oscuro-Menu.png").convert()   
fondo_oscuro_img = pygame.transform.scale(fondo_oscuro_img, (960,540))

MANUAL_INSTRUCCIONES_img = pygame.image.load("assets/manual-instrucciones.png").convert()
MANUAL_INSTRUCCIONES_img = pygame.transform.scale(MANUAL_INSTRUCCIONES_img, (960, 540))

logo_img = pygame.image.load("assets/Battleship-Logo.png").convert_alpha() 
logo_img = pygame.transform.scale(logo_img, (455, 226))

NUEVA_PARTIDA_img = Botón("assets/Boton-NUEVA PARTIDA.png", (480, 265), (231, 68), "assets/golpe_en_madera.mp3")
HISTORIAL_img = Botón("assets/Boton-HISTORIAL.png", (480, 338), (231, 68), "assets/golpe_en_madera.mp3")
INSTRUCCIONES_img = Botón("assets/Boton-INSTRUCCIONES.png", (480, 411), (231, 68), "assets/golpe_en_madera.mp3")
SALIR_img = Botón("assets/Boton-SALIR.png", (480, 484), (231, 68), "assets/golpe_en_madera.mp3")
VOLVER_AL_MENU_img = Botón("assets\Boton-VOLVER AL MENU.png", (25, 25), (55, 55), "assets/golpe_en_madera.mp3")

# --- TEXTOS Y FUNCIONES---
def mostrar_introduccion():
    """Muestra intros con efecto fade-in/out sin posibilidad de saltar"""
    logos = [logo_ucab, logo_pygame]
    
    for imagen in logos:
        # --- FADE IN (Aparecer) ---
        for alpha in range(255, -1, -5): # De 255 (negro) a 0 (transparente)
            ventana.blit(imagen, (0, 0))
            fundido.set_alpha(alpha)
            ventana.blit(fundido, (0, 0))
            pygame.display.update()
            reloj.tick(60)
            # Procesar eventos mínimos para que Windows no diga "No responde"
            pygame.event.pump() 

        # --- TIEMPO DE ESPERA (Imagen visible) ---
        pygame.time.delay(1500) # 1.5 segundos visible

        # --- FADE OUT (Desaparecer) ---
        for alpha in range(0, 256, 5): # De 0 (transparente) a 255 (negro)
            ventana.blit(imagen, (0, 0))
            fundido.set_alpha(alpha)
            ventana.blit(fundido, (0, 0))
            pygame.display.update()
            reloj.tick(60)
            pygame.event.pump()

def mostrar_historial():
    """Nueva función para visualizar los mejores puntajes en pantalla"""
    viendo = True
    # Intentamos leer el archivo de mejores puntajes
    try:
        with open("mejores_puntajes.txt", "r", encoding="utf-8") as archivo:
            lineas_historial = archivo.readlines()
    except FileNotFoundError:
        lineas_historial = ["No hay registros de puntajes aún."]

    while viendo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                    viendo = False

        ventana.blit(fondo_oscuro_img, (0, 0))
        
        y_temp = 50
        # Renderizamos cada línea del archivo [cite: 1, 2, 3]
        for linea in lineas_historial:
            # Limpiamos saltos de línea para evitar caracteres extraños
            linea_limpia = linea.strip()
            texto_surface = main.fuente.render(linea_limpia, True, (255, 255, 255))
            ventana.blit(texto_surface, (50, y_temp))
            y_temp += 35 # Espaciado entre líneas
            
        # Boton para volver
        if VOLVER_AL_MENU_img.es_presionado():
            main_menu()
            viendo = False

        # Mensaje de instrucción para volver
        footer = main.fuente.render("PULSA ENTER PARA VOLVER AL MENÚ", True, (255, 255, 0))
        ventana.blit(footer, (ANCHO_CENTRO := 300, 500))
        VOLVER_AL_MENU_img.draw(ventana)
        pygame.display.flip()

def mostrar_instrucciones():
    viendo = True
    while viendo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
        ventana.blit(MANUAL_INSTRUCCIONES_img, (0, 0))
        if VOLVER_AL_MENU_img.es_presionado():
            main_menu()
            viendo = False

        VOLVER_AL_MENU_img.draw(ventana) 
        pygame.display.flip()

# Leer historial una vez al inicio
try:
    with open("historial.txt", "r") as archivo:
        historial = archivo.read()
except:
    historial = "No hay historial aún."

# --- BUCLE PRINCIPAL DEL MENU ---
def main_menu():
    corriendo = True
    while corriendo:
        reloj.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

        if NUEVA_PARTIDA_img.es_presionado():
            main.main() 
            try:
                with open("historial.txt", "r") as archivo:
                    global historial
                    historial = archivo.read()
            except: pass

        if HISTORIAL_img.es_presionado():
            mostrar_historial()

        if INSTRUCCIONES_img.es_presionado():
            mostrar_instrucciones()

        if SALIR_img.es_presionado():
            corriendo = False
                    
        ventana.fill("white")
        ventana.blit(fondo_img, (0, 0)) 
        ventana.blit(logo_img, (250, 0)) 
        NUEVA_PARTIDA_img.draw(ventana) 
        HISTORIAL_img.draw(ventana)
        INSTRUCCIONES_img.draw(ventana)
        SALIR_img.draw(ventana)

        pygame.display.flip() 
            
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    mostrar_introduccion()
    main_menu()

