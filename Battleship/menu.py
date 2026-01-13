import pygame, sys, botones, main
from botones import Botón 

# --- CONFIGURACIÓN INICIAL ---
pygame.init()
ventana = pygame.display.set_mode((960,540))
pygame.display.set_caption("Battleship: Batalla Naval")
reloj = pygame.time.Clock()

# --- CARGA DE RECURSOS ---
fondo_img = pygame.image.load("assets/Fondo-Menu.png").convert()  
fondo_img = pygame.transform.scale(fondo_img, (960,540))
fondo_oscuro_img = pygame.image.load("assets/Fondo-Oscuro-Menu.png").convert()   
fondo_oscuro_img = pygame.transform.scale(fondo_oscuro_img, (960,540))

logo_img = pygame.image.load("assets/Battleship-Logo.png").convert_alpha() 
logo_img = pygame.transform.scale(logo_img, (455, 226))

NUEVA_PARTIDA_img = Botón("assets/Boton-NUEVA PARTIDA.png", (480, 265), (231, 68), "assets/golpe_en_madera.mp3")
HISTORIAL_img = Botón("assets/Boton-HISTORIAL.png", (480, 338), (231, 68), "assets/golpe_en_madera.mp3")
INSTRUCCIONES_img = Botón("assets/Boton-INSTRUCCIONES.png", (480, 411), (231, 68), "assets/golpe_en_madera.mp3")
SALIR_img = Botón("assets/Boton-SALIR.png", (480, 484), (231, 68), "assets/golpe_en_madera.mp3")

lineas_es = ["Instrucciones...", "Haz clic para disparar."] # (Añade tus textos aquí)
lineas_en = ["Instructions...", "Click to shoot."]

def mostrar_instrucciones():
    viendo = True
    idioma = "ES"
    while viendo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_SPACE]:
                    idioma = "EN" if idioma == "ES" else "ES"
                if event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                    viendo = False
        ventana.blit(fondo_img, (0, 0))
        texto_a_mostrar = lineas_es if idioma == "ES" else lineas_en
        y_temp = 50
        for linea in texto_a_mostrar:
            texto_surface = main.fuente.render(linea, True, (255, 255, 255))
            ventana.blit(texto_surface, (50, y_temp))
            y_temp += 30
        ayuda_txt = "SPACE: Change Language | ENTER: Return" if idioma == "EN" else "ESPACIO: Cambiar Idioma | ENTER: Volver"
        footer = main.fuente.render(ayuda_txt, True, (200, 200, 0))
        ventana.blit(footer, (200, 500))
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
        dt = reloj.tick(60) / 1000 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

        # LOGICA DE BOTONES
        if NUEVA_PARTIDA_img.es_presionado():
            # LLAMAMOS AL JUEGO, PERO NO CERRAMOS EL MENÚ
            main.main() 
            # Cuando main() termine (con el return), el código seguirá aquí
            # y volverá a dibujar el menú automáticamente.
            
            # Opcional: Recargar historial por si jugaron y se guardó algo nuevo
            try:
                with open("historial.txt", "r") as archivo:
                    global historial
                    historial = archivo.read()
            except: pass

        if HISTORIAL_img.es_presionado():
            print("------------------------------ HISTORIAL ------------------------------") 
            print(historial)

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
    main_menu()
