import time
import os
import random

# =========================
# CONFIGURACIÓN INICIAL
# =========================

TAMAÑO = 6  # Tamaño del tablero
raton = (5, 5)
gato = (0, 0)
max_turnos = 10
turno = 0
PROFUNDIDAD = 4  # profundidad del minimax

# =========================
# FUNCIONES DE TABLERO
# =========================

def crear_tablero(tamaño, gato, raton):
    matriz = [["." for _ in range(tamaño)] for _ in range(tamaño)]
    matriz[gato[0]][gato[1]] = "C"
    matriz[raton[0]][raton[1]] = "R"
    return matriz

def imprimir_tablero(matriz):
    for fila in matriz:
        print(" ".join(f"{elemento:2}" for elemento in fila))
    print("-" * 20)

# =========================
# LÓGICA DE MOVIMIENTOS
# =========================

def generar_movimientos(pos, tamaño):
    fila, col = pos
    movimientos = []
    # Direcciones: arriba, abajo, izquierda, derecha
    for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nf, nc = fila + df, col + dc
        if 0 <= nf < tamaño and 0 <= nc < tamaño:
            movimientos.append((nf, nc))
    return movimientos

# =========================
# EVALUACIÓN Y MINIMAX
# =========================

def evaluar(raton, gato):
    # Distancia Manhattan
    return abs(raton[0] - gato[0]) + abs(raton[1] - gato[1])

def es_terminal(gato, raton):
    return gato == raton

def minimax(raton, gato, profundidad, alfa, beta, es_turno_raton):
    # Caso: El gato atrapa al ratón
    if es_terminal(gato, raton):
        # Si es turno del ratón y lo atraparon, es muy malo para él.
        # Sumamos la profundidad para que el gato prefiera atraparlo "rápido"
        return -1000 - profundidad if es_turno_raton else 1000 + profundidad

    if profundidad == 0:
        return abs(raton[0] - gato[0]) + abs(raton[1] - gato[1])

    if es_turno_raton:
        mejor_valor = float("-inf")
        for mov in generar_movimientos(raton, TAMAÑO):
            valor = minimax(mov, gato, profundidad - 1, alfa, beta, False)
            mejor_valor = max(mejor_valor, valor)
            alfa = max(alfa, valor)
            if beta <= alfa:
                break
        return mejor_valor
    else:
        mejor_valor = float("inf")
        for mov in generar_movimientos(gato, TAMAÑO):
            valor = minimax(raton, mov, profundidad - 1, alfa, beta, True)
            mejor_valor = min(mejor_valor, valor)
            beta = min(beta, valor)
            if beta <= alfa:
                break
        return mejor_valor

# =========================
# TOMA DE DECISIONES
# =========================

def mejor_movimiento_raton(raton, gato):
    mejor_valor = float("-inf")
    mejores_movs = []
    
    for mov in generar_movimientos(raton, TAMAÑO):
        valor = minimax(mov, gato, PROFUNDIDAD, float("-inf"), float("inf"), False)
        if valor > mejor_valor:
            mejor_valor = valor
            mejores_movs = [mov]
        elif valor == mejor_valor:
            mejores_movs.append(mov)
    
    return random.choice(mejores_movs) if mejores_movs else raton

def mejor_movimiento_gato(gato, raton):
    mejor_valor = float("inf")
    mejores_movs = []
    
    for mov in generar_movimientos(gato, TAMAÑO):
        valor = minimax(raton, mov, PROFUNDIDAD, float("-inf"), float("inf"), True)
        if valor < mejor_valor:
            mejor_valor = valor
            mejores_movs = [mov]
        elif valor == mejor_valor:
            mejores_movs.append(mov)
            
    return random.choice(mejores_movs) if mejores_movs else gato

def mover_usuario(pos):
    fila, col = pos
    move = input("Mover (w/a/s/d): ").lower()
    if move == "w" and fila > 0: fila -= 1
    elif move == "s" and fila < TAMAÑO - 1: fila += 1
    elif move == "a" and col > 0: col -= 1
    elif move == "d" and col < TAMAÑO - 1: col += 1
    return (fila, col)

# =========================
# EJECUCIÓN DEL JUEGO
# =========================

print("--- JUEGO DEL GATO Y EL RATÓN ---")
print("1 - Automático (IA vs IA)")
print("2 - Controlar Ratón")
print("3 - Controlar Gato")
modo = input("Selecciona modo: ")

while turno < max_turnos:
    os.system("cls" if os.name == "nt" else "clear")
    print(f"Turno {turno + 1}/{max_turnos}")
    
    tablero = crear_tablero(TAMAÑO, gato, raton)
    imprimir_tablero(tablero)

    # Jugar como raton
    if modo == "2":
        raton = mover_usuario(raton)
    else:
        raton = mejor_movimiento_raton(raton, gato)

    # Verificar si el ratón se movió justo a la boca del gato
    if es_terminal(gato, raton):
        break

    # Jugar como gato
    if modo == "3":
        gato = mover_usuario(gato)
    else:
        gato = mejor_movimiento_gato(gato, raton)

    if es_terminal(gato, raton):
        break

    turno += 1
    time.sleep(0.5)

# Resultado final
os.system("cls" if os.name == "nt" else "clear")
tablero_final = crear_tablero(TAMAÑO, gato, raton)
imprimir_tablero(tablero_final)

if es_terminal(gato, raton):
    print("¡EL GATO ATRAPÓ AL RATÓN! 🐱🍴")
else:
    print("¡EL RATÓN ESCAPÓ! 🐭✨")