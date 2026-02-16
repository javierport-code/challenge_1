import time
import os

# =========================
# CONFIGURACIÓN INICIAL
# =========================

tamaño = 6
raton = (2, 2)
gato = (0, 0)
max_turnos = 20
turno = 0
PROFUNDIDAD = 4  # profundidad del minimax


# =========================
# FUNCIONES DE TABLERO
# =========================

def crear_tablero(tamaño, gato, raton):
    matriz = []
    for i in range(tamaño):
        fila = []
        for j in range(tamaño):
            fila.append(".")
        matriz.append(fila)

    matriz[gato[0]][gato[1]] = "C"
    matriz[raton[0]][raton[1]] = "R"
    return matriz


def imprimir_tablero(matriz):
    for fila in matriz:
        for elemento in fila:
            print(f"{elemento:2}", end=" ")
        print()
    print()


# =========================
# MOVIMIENTOS
# =========================

def generar_movimientos(pos, tamaño):
    fila, col = pos
    movimientos = []

    if fila > 0:
        movimientos.append((fila - 1, col))
    if fila < tamaño - 1:
        movimientos.append((fila + 1, col))
    if col > 0:
        movimientos.append((fila, col - 1))
    if col < tamaño - 1:
        movimientos.append((fila, col + 1))

    return movimientos


# =========================
# EVALUACIÓN
# =========================

def evaluar(raton, gato):
    # distancia Manhattan
    return abs(raton[0] - gato[0]) + abs(raton[1] - gato[1])


def es_terminal(gato, raton):
    return gato == raton


# =========================
# MINIMAX
# =========================

def minimax(raton, gato, profundidad, es_turno_raton):

    if profundidad == 0 or es_terminal(gato, raton):
        return evaluar(raton, gato)

    if es_turno_raton:
        # Maximiza distancia
        mejor_valor = float("-inf")
        for mov in generar_movimientos(raton, tamaño):
            valor = minimax(mov, gato, profundidad - 1, False)
            mejor_valor = max(mejor_valor, valor)
        return mejor_valor

    else:
        # Minimiza distancia
        mejor_valor = float("inf")
        for mov in generar_movimientos(gato, tamaño):
            valor = minimax(raton, mov, profundidad - 1, True)
            mejor_valor = min(mejor_valor, valor)
        return mejor_valor


def mejor_movimiento_raton(raton, gato):
    mejor_valor = float("-inf")
    mejor_mov = raton

    for mov in generar_movimientos(raton, tamaño):
        valor = minimax(mov, gato, PROFUNDIDAD, False)
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_mov = mov

    return mejor_mov


def mejor_movimiento_gato(gato, raton):
    mejor_valor = float("inf")
    mejor_mov = gato

    for mov in generar_movimientos(gato, tamaño):
        valor = minimax(raton, mov, PROFUNDIDAD, True)
        if valor < mejor_valor:
            mejor_valor = valor
            mejor_mov = mov

    return mejor_mov


# =========================
# MOVIMIENTO USUARIO
# =========================

def mover_usuario(pos):
    fila, col = pos
    move = input("Mover (w/a/s/d): ")

    if move == "w" and fila > 0:
        fila -= 1
    elif move == "s" and fila < tamaño - 1:
        fila += 1
    elif move == "a" and col > 0:
        col -= 1
    elif move == "d" and col < tamaño - 1:
        col += 1

    return (fila, col)


# =========================
# SELECCIÓN DE MODO
# =========================

print("Modo de juego:")
print("1 - Automático (IA vs IA)")
print("2 - Controlar Ratón")
print("3 - Controlar Gato")

modo = input("Selecciona 1, 2 o 3: ")

# =========================
# LOOP PRINCIPAL
# =========================

while turno < max_turnos:

    os.system("cls")
    print(f"Turno {turno + 1}/{max_turnos}\n")

    tablero = crear_tablero(tamaño, gato, raton)
    imprimir_tablero(tablero)

    # Movimiento ratón
    if modo == "2":
        raton = mover_usuario(raton)
    else:
        raton = mejor_movimiento_raton(raton, gato)

    # Movimiento gato
    if modo == "3":
        gato = mover_usuario(gato)
    else:
        gato = mejor_movimiento_gato(gato, raton)

    if es_terminal(gato, raton):
        tablero = crear_tablero(tamaño, gato, raton)
        imprimir_tablero(tablero)
        print("¡El gato atrapó al ratón! 🐱🐭")
        break

    turno += 1
    time.sleep(0.6)

if turno == max_turnos:
    print("El ratón sobrevivió 🐭✨")
