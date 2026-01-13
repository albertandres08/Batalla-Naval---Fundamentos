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

# --- TEXTOS ---
lineas_es = [
    "MANUAL DE INSTRUCCIONES DE \"BATTLESHIP - BATALLA NAVAL\"",
    "OBJETIVO DEL JUEGO",
    "Tu misión es localizar y destruir la flota enemiga oculta en un tablero de 10x10 casillas,", 
    "derrotando a los villanos que ponen en peligro los O.D.S (Objetivos de Desarrollo Sostenible).", 
    "Debes hundir todos los barcos antes de rendirte.",
    "LA FLOTA ENEMIGA",
    "La computadora ha escondido aleatoriamente 10 barcos en el mar. No puedes verlos,",
    "pero están ahí. La flota se compone de:",
    "1 Portaaviones (4 casillas)",
    "2 Acorazados (3 casillas c/u)",
    "3 Submarinos (2 casillas c/u)",
    "4 Destructores (1 casilla c/u)",
    "CÓMO JUGAR (Controles)",
    "Inicio: Al ejecutar el juego, debes escribir tu nombre y presionar Enter para iniciar.",
    "Interfaz:",
    "Al abrirse la ventana de inicio, verás la introducción al juego y el Menú principal,",
    "\"Nueva Partida\" te llevará a jugar contra la CPU, defendiendo los O.D.S.",
    "\"Historial\" te mostrará los mejores puntajes de los que se tienen registro.",
    "\"Instrucciones\" es aquí, donde aprenderás cómo moverte en la interfaz y jugar.",
    "\"Salir\" eliminará la ventana saliendo del juego.",
    "CÓDIGO DE COLORES Y SONIDOS",
    "El tablero al jugar te indicará el resultado de tus disparos visual y auditivamente:",
    "AZUL (Agua desconocida): Zona donde aún no has disparado.",
    "BLANCO (Fallo/Agua): Disparaste y no había nada. Sonido: \"Splash\".",
    "ROJO (Tocado/Hundido): ¡Impacto! Has golpeado una parte de un barco.",
    "Sonido: Escucharás una \"Explosión\".",
    "FINAL DEL JUEGO Y PUNTUACIÓN",
    "Final de Partida: El juego termina al hundir el último barco enemigo.",
    "Aparecerá el mensaje \"¡VICTORIA!\".",
    "Historial: Los resultados se guardarán automáticamente en historial.txt."
]

lineas_en = [
    "INSTRUCTION MANUAL FOR \"BATTLESHIP - NAVAL BATTLE\"",
    "GAME OBJECTIVE",
    "Your mission is to locate and destroy the enemy fleet hidden in a 10x10 grid,",
    "defeating the villains who threaten the SDGs (Sustainable Development Goals).",
    "You must sink all the ships before giving up.",
    "THE ENEMY FLEET",
    "The computer has randomly hidden 10 ships at sea. You cannot see them,",
    "but they are there. The fleet consists of:",
    "1 Aircraft Carrier (4 cells)",
    "2 Battleships (3 cells each)",
    "3 Submarines (2 cells each)",
    "4 Destroyers (1 cell each)",
    "HOW TO PLAY (Controls)",
    "Start: When running the game, type your name and press Enter to start.",
    "Interface:",
    "When the home window opens, you will see the introduction and the Main Menu.",
    "\"New Game\" will take you to play against the CPU, defending the SDGs.",
    "\"History\" will show you the best scores recorded so far.",
    "\"Instructions\" is here, where you will learn how to play.",
    "\"Exit\" will close the game window.",
    "COLOR CODE AND SOUNDS",
    "The game board will indicate the result of your shots visually and audibly:",
    "BLUE (Unknown water): Area where you haven't fired yet.",
    "WHITE (Miss): You fired and there was nothing. Sound: \"Splash\".",
    "RED (Hit/Sunk): Impact! You have hit a part of a ship.",
    "Sound: You will hear an \"Explosion\".",
    "END OF THE GAME AND SCORING",
    "End of Match: The game ends when you sink the last enemy ship.",
    "A \"VICTORY!\" message will appear.",
    "History: Results will be automatically saved in historial.txt."
]

def mostrar_instrucciones():
    viendo = True
    pagina = 0 # 0-1: Español, 2-3: Inglés
    while viendo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RIGHT, pygame.K_SPACE]:
                    pagina = (pagina + 1) % 4
                if event.key == pygame.K_LEFT:
                    pagina = (pagina - 1) % 4
                if event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                    viendo = False

        ventana.blit(fondo_oscuro_img, (0, 0))
        
        # Lógica de división: 15 líneas por página aproximadamente
        if pagina == 0:
            texto_a_mostrar = lineas_es[:15]
            ayuda_txt = "PÁGINA 1/4 (ES) | ESPACIO: Siguiente | ENTER: Volver"
        elif pagina == 1:
            texto_a_mostrar = lineas_es[15:]
            ayuda_txt = "PÁGINA 2/4 (ES) | ESPACIO: Siguiente | ENTER: Volver"
        elif pagina == 2:
            texto_a_mostrar = lineas_en[:15]
            ayuda_txt = "PAGE 3/4 (EN) | SPACE: Next | ENTER: Return"
        else:
            texto_a_mostrar = lineas_en[15:]
            ayuda_txt = "PAGE 4/4 (EN) | SPACE: Next | ENTER: Return"

        y_temp = 30
        for linea in texto_a_mostrar:
            texto_surface = main.fuente.render(linea, True, (255, 255, 255))
            ventana.blit(texto_surface, (40, y_temp))
            y_temp += 30
            
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
