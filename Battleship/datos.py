#Modulo donde se encuentran los datos que usamos para el juego

#LISTA DE COLORES RGB 
rojo = (231, 76, 60)
naranja = (255,165,0)
amarillo = (255,255,0)
verde_claro = (0,255,0)
verde_oscuro = (0,128,0)
cian = (0, 255, 200)
azul_claro = (52, 152, 219) 
azul_oscuro = (41, 128, 185)
lila = (186,85,211)
purpura = (128,0,128)
rosado = (255,105,180)
fucsia = (255,20,147)
gris_metalico = (127, 140, 141)
gris_claro = (236, 240, 241)
blanco = (255, 255, 255)
negro = (20, 20, 20)

#Asignamos colores (cambiar el nombre del color por uno de los de arriba)

#Colores del tablero:
color_agua = azul_claro     
color_barco = gris_metalico   
color_tocado = rojo   
color_fallo = gris_claro  
color_texto = blanco  

#Colores de las escenas con personajes: 
color_fondo_dialogo = negro
color_contorno_dialogo = cian 
color_borde = azul_oscuro    
color_ayudas = cian
color_dialogo = blanco

#Color del historial de puntajes
color_historial = blanco

#Colores del menu de nombre
color_fondo_nombre = negro
color_nombre = cian

#Colores de la pantalla de victoria
color_fondo_victoria = negro
color_texto_victoria = verde_claro
color_texto_regreso = blanco

# 3. Configuración del Tablero
filas = 10
columnas = 10
tamaño_celda = 40  # Cada cuadro mide 40x40 píxeles
margen_x = 25      # Espacio a la izquierda de la grilla
margen_y = 150     # Espacio arriba para poner títulos/menús

# 4. Estados de las Celdas (Lo que hay en la matriz)
agua = "~"
Portaaviones = "P"
Acorazados = "A"
Submarino = "S"
Destructor = "D"
fallo = 2    # Disparaste al agua
tocado = 3   # Le diste a un barco
hundido = 4  # El barco ya no existe

# --------------------------- Numeros de Barcos en la Flota ---------------------------
#ACA ES DONDE PODRAS MODIFICAR LA CANTIDAD DE BARCOS SEGUN TU GUSTO DENTRO DE LOS LIMITES ESTABLECIDOS ABAJO.
Numero_de_Portaviones = 3
Numero_de_Acorazados = 2
Numero_de_Subamarinos = 1
Numero_de_Destructores = 0

# =============================================================================
# ⚠️ ASPECTOS A TENER EN CUENTA: LÍMITES DE LA FLOTA (TABLERO 10x10)
# =============================================================================
# REGLA CRÍTICA: La suma de casillas ocupadas NO debe superar 40.
# CONSECUENCIA: Si superas 40, el juego entrará en bucle infinito y se congelará.
#
# CÁLCULO DE ESPACIO OCUPADO:
# (N° Portaaviones * 4) + (N° Acorazados * 3) + (N° Submarinos * 2) + (N° Destructores * 1)
#
# LÍMITES HARDWARE/LOGICA:
# 1. Portaaviones (4 celdas): MÁXIMO 3. (Más de 3 bloquea el algoritmo).
# 2. Espacio Total: Ideal entre 20 y 30 casillas. (Máximo absoluto: 40).
#
# Aqui hay algunos ejemplos que puedes usar para colocar la cantidad de cada barco y aseurar una buena experiencia:
# - Balanceado: 1 Port, 2 Acor, 3 Sub, 4 Dest (Total: 20 casillas / 20%)
# - Guerra:     2 Port, 3 Acor, 4 Sub, 5 Dest (Total: 30 casillas / 30%)
# - Extremo:    3 Port, 2 Acor, 3 Sub, 5 Dest (Total: 29 casillas / 29%)
# =============================================================================

#Definición de la Flota (Módulo A: Backend)
flota = []
#Portaavinones
for p in range(Numero_de_Portaviones):
    flota.append({"nombre": "Portaaviones", "tamaño": 4, "simbolo": f"P{p+1}", "hundido": 4})

#Acorazados
for a in range(Numero_de_Acorazados):
    flota.append({"nombre": "Acorazado", "tamaño": 3, "simbolo": f"A{a+1}", "hundido": 3})
    
#Submarinos
for s in range(Numero_de_Subamarinos):
    flota.append({"nombre": "Submarino", "tamaño": 2, "simbolo": f"S{s+1}", "hundido": 2})

#Destructores
for d in range(Numero_de_Destructores):
    flota.append({"nombre": "Destructor", "tamaño": 1, "simbolo": f"D{d+1}", "hundido": 1})

# Calculamos automáticamente cuántas celdas de barco hay en total (Debe dar 20)
sin_flota = sum(barco["tamaño"] for barco in flota)

# 6. Rutas de Archivos (Persistencia) 
archivo_historial = "historial.txt"
