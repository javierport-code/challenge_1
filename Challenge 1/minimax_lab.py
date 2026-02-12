# Importaciones
import time # Permite pausar la impresion de del programa usando time.sleep para poder ver bien cada turno
import os # Permite usar comandos del sistema operativos, en este caso limpiar la consola en cada turno

# Variables iniciales
tamaño = 10 # Indica el tamaño del tablero
raton = (2, 2) # Idnica la posicion inicial del raton
gato = (0, 0) # Idnica la posicion inicial del gato 
max_turnos = 15
turno = 0

# Tablero y posiciones iniciales
def crear_tablero(tamaño, gato, raton):
    """Crea el tablero y coloca gato y ratón"""
    matriz = []
    for i in range(tamaño):
        fila = []
        for j in range(tamaño):
            fila.append('.')
        matriz.append(fila)
    matriz[gato[0]][gato[1]] = 'C'
    matriz[raton[0]][raton[1]] = 'R'
    return matriz

def imprimir_tablero(matriz):
    """Imprime la matriz en consola"""
    for fila in matriz:
        for elemento in fila:
            print(f"{elemento:2}", end=" ")
        print()
    print()  # Línea extra para separar turnos

def generar_movimientos(pos, tamaño):
    fila, col = pos
    movimientos=[]

    if fila > 0:
        movimientos.append((fila-1, col)) # si la fila es mayor a 0, se puede mover para la arriba
    if fila < tamaño-1:
        movimientos.append((fila+1, col)) # si la fila es menor a -1, se puede mover para la abajo
    if col > 0:
        movimientos.append((fila, col-1)) # si la columna es mayor a 0, se puede mover para izquierda
    if col < tamaño-1:
        movimientos.append((fila, col+1)) # si la columna es menor a -1, se puede mover para derecha

    return movimientos

# Funcion de evaluacion 
def evaluar_tablero(raton, gato):
    fila_r, col_r = raton
    fila_g, col_g = gato
    return abs(fila_r - fila_g) + abs(col_r - col_g)

# Movimientos del raton
def movimiento_raton(raton, gato, tamaño):
    posibles = generar_movimientos(raton, tamaño)

    mejor_pos = raton
    mejor_dist = evaluar_tablero(raton, gato)

    for pos in posibles:
        dist = evaluar_tablero(pos, gato)
        if dist >= mejor_dist:
            mejor_dist = dist 
            mejor_pos = pos

    return mejor_pos

#Loop interactivo 

while turno < max_turnos:
    os.system('cls') # limpieza de la consola 

    print(f"Turno: {turno + 1}/{max_turnos}")
    print()

    tablero = crear_tablero(tamaño, gato, raton)
    imprimir_tablero(tablero)

    raton = movimiento_raton(raton, gato, tamaño)

# Movimiento automatico del gato

    fila_gato, col_gato = gato 
    fila_raton, col_raton = raton

    if fila_gato < fila_raton:
        fila_gato += 1
    elif fila_gato > fila_raton:
        fila_gato -= 1

    if col_gato < col_raton:
        col_gato += 1
    elif col_gato > col_raton:
        col_gato -= 1

    gato = (fila_gato, col_gato)

    

# Comprobamos si el gato atrapo al raton

    if gato == raton:
        tablero = crear_tablero(tamaño, gato, raton)
        imprimir_tablero(tablero)
        print('¡El gato atrapó al ratón! 🐱🐭')
        break

    


    print('distancia actual:', evaluar_tablero(raton, gato))

    turno += 1
    time.sleep(0.5)

    if turno == max_turnos:
        print("Se acabaron los turnos. El ratón sobrevivió 🐭✨")

    