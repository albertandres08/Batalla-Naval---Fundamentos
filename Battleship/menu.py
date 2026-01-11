import pygame, sys, botones, main
from botones import Botón # <--- Se importo la clase "Boton", todos los botones se incluyen en una misma clase pero tienen caracteristicas diferentes.

# --- CONFIGURACIÓN INICIAL ---
pygame.init()
# Inicializar mixer (audio) de forma explícita para evitar errores al cargar sonidos

ventana = pygame.display.set_mode((960,540))
pygame.display.set_caption("Battleship: Batalla Naval")
reloj = pygame.time.Clock()

# --- CARGA DE RECURSOS ---
# Se declaran las imagenes con los parametros requeridos (tamaño, ruta, etc)
fondo_img = pygame.image.load("Battleship/assets/Fondo-Menu.png").convert() # .convert() optimiza la superficie para el formato de la pantalla y mejora el rendimiento.   
fondo_img = pygame.transform.scale(fondo_img, (960,540))

logo_img = pygame.image.load("Battleship/assets/Battleship-Logo.png").convert_alpha() # Es como "convert()", pero para imagenes PNGs con canal alfa, manteniendo su transparencias. 
logo_img = pygame.transform.scale(logo_img, (455, 226))

NUEVA_PARTIDA_img = Botón("Battleship/assets/Boton-NUEVA PARTIDA.png", (480, 265), (231, 68), "Battleship/assets/golpe_en_madera.mp3")
HISTORIAL_img = Botón("Battleship/assets/Boton-HISTORIAL.png", (480, 338), (231, 68), "Battleship/assets/golpe_en_madera.mp3")
INSTRUCCIONES_img = Botón("Battleship/assets/Boton-INSTRUCCIONES.png", (480, 411), (231, 68), "Battleship/assets/golpe_en_madera.mp3")
SALIR_img = Botón("Battleship/assets/Boton-SALIR.png", (480, 484), (231, 68), "Battleship/assets/golpe_en_madera.mp3")

# Se lee el archivo "historial.txt"
with open("historial.txt", "r") as archivo:
    historial = archivo.read()

# --- BUCLE PRINCIPAL DEL MENU ---
def main_menu():
    corriendo = True
    while corriendo:
        dt = reloj.tick(60) / 1000 # 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

    # LOGICA DE BOTONES
        if NUEVA_PARTIDA_img.es_presionado():
            main.main()
            corriendo = False

        if HISTORIAL_img.es_presionado():
            print("------------------------------ HISTORIAL ------------------------------") 
            print(historial)

        if INSTRUCCIONES_img.es_presionado():
            print("MOSTRAR INSTRUCCIONES.")

        if SALIR_img.es_presionado():
            corriendo = False
                    
        ventana.fill("white")
        ventana.blit(fondo_img, (0, 0)) # La posición del fondo
        ventana.blit(logo_img, (250, 0)) # La posición del logo
        NUEVA_PARTIDA_img.draw(ventana) 
        HISTORIAL_img.draw(ventana)
        INSTRUCCIONES_img.draw(ventana)
        SALIR_img.draw(ventana)

        pygame.display.flip() # Se muestra el contenido del codigo en la ventana
            
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_menu()