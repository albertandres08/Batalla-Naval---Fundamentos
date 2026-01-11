import pygame

# --- CONFIGURACIÓN DE LA CLASE "Botón" ---
class Botón:
    # "self" se refiere a la clase, y las demas variables son parametros de cada boton.
    # Cada clase va a pedir la ruta de la imagen del boton, la posición de la boton en la ventana, el tamaño del boton y el sonido que hara el boton al tocarlo.
    def __init__(self, ruta_imagen, posición, tamaño, ruta_sonido):
        self.imagen = pygame.image.load(ruta_imagen).convert_alpha()
        self.imagen = pygame.transform.smoothscale(self.imagen, tamaño) # .smoothscale escala la imagen de forma suave al tamaño deseado
        self.rect = self.imagen.get_rect(center=posición) # Obtiene la colisión de cada boton
        self.sonido = pygame.mixer.Sound(ruta_sonido)
        # self.pressed evita múltiples detecciones del mismo click al mantener el botón presionado
        self.pressed = False

    def draw(self, ventana):
        ventana.blit(self.imagen, self.rect)
    
    def es_presionado(self):
        posición_mouse = pygame.mouse.get_pos()
        mouse_presionado = pygame.mouse.get_pressed()[0]  # botón izquierdo

        # Detecta si el ratón está sobre la colisión del boton
        if self.rect.collidepoint(posición_mouse):
            # Detecta si el click izquierdo del boton es pulsado en el momento y no fue pulsado anteriormente
            if mouse_presionado and not self.pressed:
                self.pressed = True
                # Reproduce sonido de click
                self.sonido.play()
                return True

        # Si no hay botón presionado, resetea self.pressed para permitir nuevos clicks
        if not mouse_presionado:
            self.pressed = False
        return False
