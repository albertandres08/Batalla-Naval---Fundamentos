import os
import sys

# --- MODULARIDAD  ---

def limpiar_pantalla():
    """Limpia la consola según el sistema operativo."""
    if os.name == 'nt': # Windows
        os.system('cls')
    else: # Mac/Linux
        os.system('clear')

def mostrar_instrucciones():
    """Muestra las reglas en español e inglés"""
    limpiar_pantalla()
    print("====================================================")
    print("      INSTRUCCIONES / GAME INSTRUCTIONS             ")
    print("====================================================")
    print("\n[ESPAÑOL]")
    print("1. El objetivo es hundir todos los barcos enemigos.")
    print("2. En cada turno, ingresa una fila y una columna (0-9).")
    print("3. Símbolos:")
    print("   ~ : Agua desconocida.")
    print("   X : Disparo fallido.")
    print("   * : Barco tocado o hundido.")
    
    print("\n[ENGLISH]")
    print("1. The goal is to sink all enemy ships.")
    print("2. Each turn, enter a row and a column (0-9).")
    print("3. Symbols:")
    print("   ~ : Unknown water.")
    print("   X : Missed shot.")
    print("   * : Hit or sunken ship.")
    print("\n====================================================")
    input("\nPresione Enter para volver al menú / Press Enter to return...")

def ver_historial():
    """Lee el archivo historial.txt """
    limpiar_pantalla()
    print("====================================================")
    print("            HISTORIAL DE PUNTAJES                  ")
    print("====================================================")
    
    try:
        # Intentamos abrir el archivo 
        if os.path.exists("historial.txt"):
            with open("historial.txt", "r") as archivo:
                contenido = archivo.read()
                if contenido.strip() == "":
                    print("El historial está vacío actualmente.")
                else:
                    print(contenido)
        else:
            print("No se encontró el archivo 'historial.txt'.")
            print("Juega una partida primero para generar registros.")
    except Exception as e:
        print(f"Error al leer el historial: {e}")
        
    print("\n====================================================")
    input("Presione Enter para volver al menú...")

def iniciar_juego_consola():
    """Simulación del inicio del juego (Aquí se conectaría con la lógica)."""
    limpiar_pantalla()
    print("--- INICIANDO BATALLA NAVAL (MODO CONSOLA) ---")
    # Aquí es donde pediríamos el nombre 
    nombre = input("Ingresa tu nombre: ")
    print(f"\n¡Bienvenido, {nombre}! Generando tablero de 10x10...")
    print("(Aquí se llamaría a las funciones de logica.py)")
    input("\nPresione Enter para volver (Funcionalidad en desarrollo)...")

# --- MENÚ PRINCIPAL CÍCLICO  ---

def menu_principal():
    while True:
        limpiar_pantalla()
        print("========================================")
        print("       PROYECTO: BATALLA NAVAL          ")
        print("        MENU PRINCIPAL (v1.0)           ")
        print("========================================")
        print("1. Nueva Partida")
        print("2. Ver Historial de Puntajes")
        print("3. Instrucciones (Español/English)")
        print("4. Salir")
        print("========================================")
        
        opcion = input("Seleccione una opción (1-4): ")
        
        # Validación de entrada 
        if opcion == "1":
            iniciar_juego_consola()
        elif opcion == "2":
            ver_historial()
        elif opcion == "3":
            mostrar_instrucciones()
        elif opcion == "4":
            print("\n¡Gracias por jugar! Saliendo del sistema...")
            sys.exit()
        else:
            print("\nError: Opción no válida. Intente de nuevo.")
            input("Presione Enter para continuar...")

if __name__ == "__main__":
    menu_principal()
