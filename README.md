# Batalla Naval - Fundamentos de Programacion

Este proyecto es una implementación del clásico juego "Battleship" utilizando **Python** y la librería gráfica **Pygame**. El sistema está diseñado de manera modular, separando la lógica de datos, la interfaz gráfica y la mecánica de juego para cumplir con principios de programación estructurada.

## Estructura de Archivos

* `main.py`: **Punto de entrada**. Contiene el bucle principal del juego, la detección de eventos y el renderizado del tablero.
* `logica.py`: **Backend lógico**. Contiene funciones puras para la manipulación de matrices, validaciones de coordenadas y algoritmos del CPU.
* `datos.py`: **Configuración**. Almacena constantes globales (colores, dimensiones) y la definición de la flota (diccionarios).
* `menu.py`: **Frontend de Menú**. Gestiona la interfaz inicial, la navegación entre pantallas y la visualización de instrucciones/historial.
* `escenas.py`: **Narrativa**. Sistema para mostrar diálogos y personajes antes de los niveles.
* `botones.py`: **Componentes UI**. Clase para crear botones interactivos con detección de mouse.
* `historial.txt`: **Manejo de Archivos**. Archivo de texto plano donde se persiste el registro de partidas.

---

## Módulos del Sistema

### 1. Módulo A: Gestión del Tablero y Flota (Backend)
**Archivos principales:** `logica.py`, `datos.py`

Este módulo se encarga de la memoria y los datos del juego, funcionando independientemente de la interfaz gráfica.

* **Inicialización de Matrices (`logica.matriz_agua`):**
    * Utiliza **comprensión de listas** para generar matrices de 10x10 de manera eficiente.
    * El tablero lógico diferencia entre agua (`~`), barcos (`P`, `A`, `S`, `D`), impactos (`3`) y fallos (`2`).

* **Algoritmo de Colocación Aleatoria (`logica.generar_flota_random`):**
    * Implementa un algoritmo de colocación automática utilizando la librería `random`.
    * Itera sobre la lista de diccionarios definida en `datos.py`.
    * **Validación (`posicion_valida`):** Antes de colocar un barco, verifica dos condiciones críticas:
        1.  **Límites:** Que el barco no se salga del rango `[0-9]` en filas o columnas.
        2.  **Colisión:** Que las coordenadas destino no estén ocupadas por otro barco existente.

### 2. Módulo B: Mecánica de Juego (Lógica de Turnos)
**Archivos principales:** `main.py`

Controla el flujo de la partida y la interacción en tiempo real con el usuario.

* **Sistema de Coordenadas:**
    * Convierte la posición del clic del mouse `(píxeles)` a índices de matriz `[fila][columna]` mediante fórmulas matemáticas, permitiendo una interacción fluida en la interfaz gráfica.
* **Procesamiento de Disparos:**
    * Evalúa el contenido de la celda seleccionada en la matriz lógica.
    * **Feedback:** Actualiza el estado visual (Rojo para impacto, Blanco para agua) y reproduce efectos de sonido (`pygame.mixer`) condicionales.
* **Condición de Victoria:**
    * El sistema rastrea la "vida" de cada barco individualmente en la lista `flota`. Al llegar a 0, notifica el hundimiento. El juego termina cuando la suma de vidas de toda la flota es 0.

### 3. Módulo C: Interfaz y Menús (Frontend)
**Archivos principales:** `menu.py`, `escenas.py`, `botones.py`

Maneja todo lo que el usuario ve, utilizando la superficie (`Surface`) de Pygame.

* **Sistema de Narrativa (`escenas.py`):**
    * Renderiza secuencias de diálogo utilizando temporizadores (`pygame.time.get_ticks`) para controlar el ritmo de lectura.
    * Cambia dinámicamente los sprites de los personajes según el contexto de la historia.

### 4. Persistencia de Datos
**Archivos principales:** `logica.py`, `historial.txt`

El proyecto implementa persistencia básica mediante lectura y escritura de archivos (`E/S`).

* **Guardado (`logica.guardar_historial`):**
    * Registra cada partida finalizada en `historial.txt` usando el modo *append* (`'a'`) para no borrar datos previos.
    * Incluye *timestamps* precisos gracias a la librería `datetime`.
* **Lectura y Ranking (`logica.guardar_mejor_puntaje`):**
    * Lee el archivo de texto y procesa las cadenas para extraer la información relevante.
    * Ordena los resultados dinámicamente para mostrar un **Top 3** de mejores jugadores (basado en menor cantidad de intentos).

---

## Requisitos e Instalación

1.  Se debe de tener Python instalado.
2.  Instalar la dependencia gráfica:
    ```bash
    pip install pygame
    ```
3.  Ejecutar el juego desde el menú principal:
    ```bash
    python menu.py
    ```
4. Ejecutar el juego desde la carpeta de "Battleship".
