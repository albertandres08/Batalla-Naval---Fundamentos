import pygame
import sys
import datos  
import logica  

# --- CONFIGURACIÓN INICIAL ---
pygame.init()

# Colores RGB
negro = (0, 0, 0)
blanco = (255, 255, 255)
azul= (50, 150, 200)

# Tamaño de la celda y margen
tamaño_celda = 40
margen = 5

# Tamaño de la pantalla segun el archivo datos.py
ancho_pantalla = (tamaño_celda + margen) * datos.columnas + margen
alto_pantalla = (tamaño_celda + margen) * datos.filas + margen

ventana = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
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
        ventana.fill(negro) # Fondo negro

        # Dibujar la cuadrícula
        for f in range(datos.filas):
            for c in range(datos.columnas):
                color = azul
                
                # Coordenadas para dibujar el rectanguito
                x = (margen + tamaño_celda) * c + margen
                y = (margen + tamaño_celda) * f + margen
                
                pygame.draw.rect(ventana, color, [x, y, tamaño_celda, tamaño_celda])

        # 3. Actualizar la pantalla
        pygame.display.flip()
        
        # 60 cuadros por segundo
        reloj.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()