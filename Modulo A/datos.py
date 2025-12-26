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
    {"nombre": "Portaaviones", "tamaño": 5, "simbolo": "P", "hundido": 5},
    {"nombre": "Acorazado",    "tamaño": 4, "simbolo": "A1", "hundido": 4},
    {"nombre": "Acorazado",    "tamaño": 4, "simbolo": "A2", "hundido": 4},
    {"nombre": "Submarino",    "tamaño": 3, "simbolo": "S1", "hundido": 3},
    {"nombre": "Submarino",    "tamaño": 3, "simbolo": "S2", "hundido": 3},
    {"nombre": "Submarino",    "tamaño": 3, "simbolo": "S3", "hundido": 3},
    {"nombre": "Destructor",   "tamaño": 2, "simbolo": "D1", "hundido": 2},
    {"nombre": "Destructor",   "tamaño": 2, "simbolo": "D2", "hundido": 2},
    {"nombre": "Destructor",   "tamaño": 2, "simbolo": "D3", "hundido": 2},
    {"nombre": "Destructor",   "tamaño": 2, "simbolo": "D4", "hundido": 2}
]

sin_flota = sum(barco["tamaño"] for barco in flota)  # Total de partes de barcos

# 6. Rutas de Archivos (Persistencia)
archivo_historial = "historial.txt"
