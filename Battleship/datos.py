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

# 5. Definición de la Flota (Módulo A: Backend)
flota = [
    # 1 Portaaviones de tamaño 4
    {"nombre": "Portaaviones", "tamaño": 4, "simbolo": "P", "hundido": 4},
    
    # 2 Acorazados de tamaño 3
    {"nombre": "Acorazado",    "tamaño": 3, "simbolo": "A1", "hundido": 3},
    {"nombre": "Acorazado",    "tamaño": 3, "simbolo": "A2", "hundido": 3},
    
    # 3 Submarinos de tamaño 2
    {"nombre": "Submarino",    "tamaño": 2, "simbolo": "S1", "hundido": 2},
    {"nombre": "Submarino",    "tamaño": 2, "simbolo": "S2", "hundido": 2},
    {"nombre": "Submarino",    "tamaño": 2, "simbolo": "S3", "hundido": 2},
    
    # 4 Destructores de tamaño 1
    {"nombre": "Destructor",   "tamaño": 1, "simbolo": "D1", "hundido": 1},
    {"nombre": "Destructor",   "tamaño": 1, "simbolo": "D2", "hundido": 1},
    {"nombre": "Destructor",   "tamaño": 1, "simbolo": "D3", "hundido": 1},
    {"nombre": "Destructor",   "tamaño": 1, "simbolo": "D4", "hundido": 1}
]

# Calculamos automáticamente cuántas celdas de barco hay en total (Debe dar 20)
sin_flota = sum(barco["tamaño"] for barco in flota)

# 6. Rutas de Archivos (Persistencia) 
archivo_historial = "historial.txt"
