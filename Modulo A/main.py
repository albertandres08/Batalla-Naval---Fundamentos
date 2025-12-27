import pygame
import sys
import datos  
import logica  

# --- CONFIGURACIÓN INICIAL ---
pygame.init()

# Colores RGB
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL_MAR = (50, 150, 200)

# Tamaño de la celda y margen
TAMANO_CELDA = 40
MARGEN = 5

# Tamaño de la pantalla segun el archivo datos.py
ANCHO_PANTALLA = (TAMANO_CELDA + MARGEN) * datos.columnas + MARGEN
ALTO_PANTALLA = (TAMANO_CELDA + MARGEN) * datos.filas + MARGEN

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