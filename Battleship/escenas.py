import pygame
import sys

# We load assets here once so they are ready
fondo_barco = pygame.image.load("assets/Fondo-Barco.png")

# Character images
niña_normal = pygame.image.load("assets/niña_normal.png")
niña_alegre = pygame.image.load("assets/niña_alegre.png")
niña_molesta = pygame.image.load("assets/niña_molesta.png")
viejo_normal = pygame.image.load("assets/viejo_normal.png")
viejo_alegre = pygame.image.load("assets/viejo_alegre.png")
viejo_molesto = pygame.image.load("assets/viejo_molesto.png")

dialogos = [
    ["El trabajo honesto no es suficiente, pero estos planes malvados nos garantizarán el exito.",
     "Logramos producir un nuevo tipo de energía capaz de mantener a todo el país.",
     "Es muy dañina, pero nadie tiene porque saberlo.",
     "¿Quién cree en el calentamiento global de todas formas?",
     "Ya entramos en acción, las piezas de nuestro generador vienen en los barcos...",
     "(¡Debes detener esos barcos para proteger los ODS 7, 11 y 13!)"],
    
    ["Puede que el plan anterior fracasara...",
     "Pero con mi nuevo invento cumpliremos todos nuestros objetivos.",
     "He desarrollado un contaminante el cual solo podrá ser erradicado con mi formula secreta.",
     "¡Si la vendo nos haremos millonarios! ¡Todos dependerán de nosotros!",
     "¿Qué importa si algunas cosechas se arruinan? O si alguien bebe esa agua...", 
     "(Esta vez protegeremos las ODS 3, 6, 12, 14, 15 y 17.)"],
    
    ["No pudiste acabar conmigo... ¡Jamás frustrarás nuestros planes!",
     "Haré que seamos los dueños del todo, todo nos pertenecerá.",
     "Cada escuela, alimento, cada trabajador e industria en el país será nuestros.",
     "Y si alguien tiene quejas, tal vez nada de eso sea para ellos.",
     "Será su decisión si impulsarnos o vivir en la miseria.",
     "(Tenemos que acabar esto de una vez por todas. Protege las ODS 1, 2, 4, 8, 9, 10 y 16.)"]
]

imagenes = [
    [viejo_molesto, viejo_normal, viejo_alegre, viejo_alegre, viejo_normal, None],
    [niña_molesta, niña_normal, niña_normal, niña_alegre, niña_alegre, None],
    [viejo_molesto, viejo_alegre, viejo_normal, viejo_alegre, viejo_normal, None]
]

def mostrar_escena(ventana, fuente, num_escena):
    """Muestra una escena de historia y no sale hasta terminar los diálogos."""
    if num_escena >= len(dialogos): return

    clic_actual = 0
    total_dialogos = len(dialogos[num_escena])
    reloj = pygame.time.Clock()
    corriendo_escena = True

    while corriendo_escena:
        # 1. EVENTOS: Detectar el clic para avanzar
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clic_actual += 1
                if clic_actual >= total_dialogos:
                    corriendo_escena = False # AQUÍ se cierra la escena y regresa al main

        if corriendo_escena:
            # 2. DIBUJO
            ventana.blit(fondo_barco, (0, 0))
            
            # Personaje
            personaje = imagenes[num_escena][clic_actual]
            if personaje:
                ventana.blit(personaje, (500, 100))

            # Cuadro de texto
            rect_txt = pygame.Rect(20, 400, 920, 120)
            pygame.draw.rect(ventana, (30, 30, 30), rect_txt)
            pygame.draw.rect(ventana, (0, 255, 200), rect_txt, 3)

            # Texto
            txt_surface = fuente.render(dialogos[num_escena][clic_actual], True, (255, 255, 255))
            ventana.blit(txt_surface, (40, 430))
            
            pygame.display.flip()
            reloj.tick(30)