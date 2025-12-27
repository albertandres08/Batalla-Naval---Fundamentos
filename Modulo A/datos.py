color_agua = (52, 152, 219)     # Azul claro
color_barco = (127, 140, 141)   # Gris metálico
color_tocado = (231, 76, 60)    # Rojo
color_fallo = (236, 240, 241)   # Blanco/Gris claro
color_texto = (255, 255, 255)   # Blanco
color_borde = (41, 128, 185)    # Azul oscuro para la grilla

# 3. Configuración del Tablero
filas = 10
columnas = 10
tamaño_celda = 40  # Cada cuadro mide 40x40 píxeles
margen_x = 25      # Espacio a la izquierda de la grilla
margen_y = 150     # Espacio arriba para poner títulos/menús

# 4. Estados de las Celdas (Lo que hay en la matriz)
agua = "🌊"
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