import pygame
import sys
import datos   
import logica
import copy

# --- CONFIGURACIÓN INICIAL ---
pygame.init()

# Colores RGB
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL_MAR = (50, 150, 200)

# Tamaño de la celda y margen
TAMANO_CELDA = 40 
MARGEN = 5

# --- BUCLE PRINCIPAL DEL JUEGO ---
def main():
    # 1. SETUP DE DATOS
    # Copia de la flota para hacer los cambios del propio juego alli
    flota_viva = copy.deepcopy(datos.flota)
    
    # Duplicamos el valor de datos sin flota para no modificar el original
    # Asumo que datos.sin_flota es el total de vidas/aciertos necesarios
    vidas_restantes = datos.sin_flota 

    # 2. SETUP DE VENTANA
    # Calculamos ancho y alto, pero sumamos 100 pixeles extra abajo para el texto
    ANCHO_PANTALLA = (TAMANO_CELDA + MARGEN) * datos.columnas + MARGEN
    ALTO_PANTALLA = ((TAMANO_CELDA + MARGEN) * datos.filas + MARGEN) + 100 # <--- +100 para texto

    ventana = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Batalla Naval")
    
    reloj = pygame.time.Clock()

    # ### NUEVO: Configuración de Fuente y Mensaje ###
    fuente = pygame.font.SysFont("Arial", 22, bold=True)
    mensaje_juego = "¡Busca los barcos enemigos! Haz clic." 

    # Generamos el tablero lógico
    tablero_logico = logica.matriz_agua()
    
    # Flota en el Tablero del Usuario (Usando la copia flota_viva)
    logica.generar_flota_random(tablero_logico, flota_viva)
    
    corriendo = True
    
    while corriendo:
        # 1. Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                posicion = pygame.mouse.get_pos()
                x_mouse = posicion[0]
                y_mouse = posicion[1]
        
                # Convertir Píxeles a Fila y Columna
                # NOTA: Si hacen clic en la zona negra del texto (muy abajo), ignoramos
                if y_mouse < (ALTO_PANTALLA - 100): 
                    fila_clic = (y_mouse - MARGEN) // (TAMANO_CELDA + MARGEN)
                    columna_clic =  (x_mouse - MARGEN) // (TAMANO_CELDA + MARGEN)
                    
                    if logica.coordenada_valida(fila_clic, columna_clic):
                        contenido = tablero_logico[fila_clic][columna_clic]

                        # A. ¿Repetido?
                        if contenido == datos.tocado or contenido == datos.fallo:
                            mensaje_juego = "¡Ya disparaste ahí! Busca otro sitio." 

                        # B. ¿Agua?
                        elif contenido == datos.agua:
                            mensaje_juego = "¡AGUA! No había nada." 
                            tablero_logico[fila_clic][columna_clic] = datos.fallo
                        
                        # C. ¡Barco!
                        else:
                            mensaje_juego = "¡IMPACTO CONFIRMADO! 💥"
                            
                            # Buscamos qué barco tocamos para restarle vida
                            for barco in flota_viva:
                                if barco["simbolo"] == contenido:
                                    barco["hundido"] -= 1
                                    
                                    # Si llega a 0 es que se hundió completo
                                    if barco["hundido"] == 0:
                                        mensaje_juego = f"¡HUNDISTE UN {barco['nombre'].upper()}! 💀"
                                    break 

                            # Marcamos en el tablero visual
                            tablero_logico[fila_clic][columna_clic] = datos.tocado
                            
                            # Restamos a la condición de victoria global
                            vidas_restantes -= 1
                            
                            if vidas_restantes == 0:
                                mensaje_juego = "¡VICTORIA! FLOTA HUNDIDA 🎉"
                                # Aquí puedes poner corriendo = False si quieres que cierre al ganar
                    else:
                        pass # Clic fuera del tablero válido
                else:
                    pass # Clic en la zona del texto

        # 2. Dibujar en pantalla
        ventana.fill(NEGRO) 

        # Dibujar la cuadrícula
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

        # ### DIBUJAR EL TEXTO ABAJO ###
        # Renderizamos el texto (Texto, Antialias, Color)
        texto_imagen = fuente.render(mensaje_juego, True, BLANCO)
        
        # Lo centramos o lo ponemos a la izquierda en la zona negra inferior
        posicion_texto_y = ALTO_PANTALLA - 70 # Un poco hacia arriba del borde final
        ventana.blit(texto_imagen, (20, posicion_texto_y))

        # 3. Actualizar la pantalla
        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()