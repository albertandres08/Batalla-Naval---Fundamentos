# Módulos del Sistema

# Módulo A: Gestión del Tablero y Flota (El "Backend")

Este es el núcleo lógico. Se encarga de la memoria y los datos.

- **Inicialización de Matrices:** Crear la matriz lógica (donde están los barcos) y la matriz visible (lo que ve el usuario) llenas de "agua" inicialmente.
- **Algoritmo de Colocación Aleatoria:** Esta es la parte más compleja (vale 2.0 puntos). Debe colocar la flota específica (1 Portaaviones, 2 Acorazados, 3 Submarinos, 4 Destructores) sin que se superpongan ni salgan del mapa.
- **Validación de coordenadas:** Verificar si una coordenada (Fila/Columna) está dentro del rango 0-9.

## Módulo: Persistencia (Archivos)

Manejo del archivo historial.txt.

- **Guardar Partida:** Al terminar, escribir: Nombre, Fecha, Intentos y Resultado.
- **Leer Historial:** Mostrar los mejores puntajes desde el archivo en el menú principal.

# Módulo B: Mecánica de Juego (La Lógica de Turnos)

Controla lo que pasa cuando el usuario juega.

- **Procesar Disparo:** Recibe las coordenadas del usuario, verifica en la matriz lógica y devuelve el resultado: "AGUA", "TOCADO" o "HUNDIDO".
- **Actualizar Tableros:** Si el usuario acierta, marcar la matriz visible con *; si falla, marcar con X.
- **Verificar Victoria:** Revisar si todos los barcos de la flota han sido hundidos para terminar el juego.

# Módulo C: Interfaz y Menús (El "Frontend" en Consola)

Se encarga de todo lo que el usuario ve y lee.

- **Menú Principal:** Mostrar opciones: Nueva Partida, Historial, Instrucciones, Salir.
- **Imprimir Tablero:** Una función que "limpie" la pantalla y dibuje la matriz visible de forma bonita (con números de fila/columna).
- **Instrucciones:** Mostrar el texto de ayuda en español e inglés.
- **Captura de Datos:** Pedir el nombre del jugador y las coordenadas, validando que no metan letras.
