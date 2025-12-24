import datos
import pygame
#AGREGAR COMENTARIOS
 
def matriz_agua():
    tablero = []
    for f in range(datos.filas):
        fila = []
        for c in range(datos.columnas):
            fila.append(datos.agua)
        tablero.append(fila)
    return tablero

def main():
    tablero_agua = matriz_agua()
    for filas in range(datos.filas):
        print(tablero_agua[filas])
    
if __name__ == "__main__":
    main()