import pygame
import sys
import random

pygame.init()

# Constantes
Ancho = 300
Alto = 600
COLUMNAS = 10
FILAS = 20
TAM_CELDA = Ancho // COLUMNAS

Pantalla = pygame.display.set_mode((Ancho, Alto))
pygame.display.set_caption("Tetris")

# Piezas y colores
PIEZAS = {
    "I": [(0, 1), (1, 1), (2, 1), (3, 1)],
    "O": [(0, 0), (0, 1), (1, 0), (1, 1)],
    "T": [(0, 1), (1, 0), (1, 1), (1, 2)],
    "S": [(0, 1), (0, 2), (1, 0), (1, 1)],
    "Z": [(0, 0), (0, 1), (1, 1), (1, 2)],
    "J": [(0, 0), (1, 0), (2, 0), (2, 1)],
    "L": [(0, 1), (1, 1), (2, 1), (2, 0)],
}

COLORES = {
    "I": (0, 255, 255),
    "O": (255, 255, 0),
    "T": (128, 0, 128),
    "S": (0, 255, 0),
    "Z": (255, 0, 0),
    "J": (0, 0, 255),
    "L": (255, 165, 0),
}

# Carga sonidos (pon los archivos en la misma carpeta)
try:
    pygame.mixer.music.load("linea.wav")  # sonido de fondo
    sonido_gameover = pygame.mixer.Sound("gameover.wav")  # sonido game over
    pygame.mixer.music.play(-1)  # reproduce fondo en loop (-1 infinito)
except pygame.error:
    print("No se pudieron cargar los sonidos. Revisa que 'fondo.wav' y 'gameover.wav' estén en la carpeta.")

# Funciones y resto del código igual...

def crear_tablero_vacio():
    return [[(0, 0, 0) for _ in range(COLUMNAS)] for _ in range(FILAS)]

def nueva_pieza():
    tipo = random.choice(list(PIEZAS.keys()))
    forma = PIEZAS[tipo]
    pieza = [(fila, columna + 3) for fila, columna in forma]
    return pieza, tipo

def fijar_pieza(pieza, tablero, color):
    for fila, columna in pieza:
        tablero[fila][columna] = color

def puede_mover(pieza, dx, dy, tablero):
    for fila, columna in pieza:
        nueva_fila = fila + dy
        nueva_col = columna + dx
        if (
            nueva_col < 0 or nueva_col >= COLUMNAS or
            nueva_fila < 0 or nueva_fila >= FILAS or
            tablero[nueva_fila][nueva_col] != (0, 0, 0)
        ):
            return False
    return True

def rotar_pieza(pieza, tipo, tablero):
    if tipo == "O":
        return pieza
    centro_fila, centro_col = pieza[1]
    nueva_pieza = []
    for fila, columna in pieza:
        nueva_fila = centro_fila - (columna - centro_col)
        nueva_col = centro_col + (fila - centro_fila)
        nueva_pieza.append((nueva_fila, nueva_col))
    if puede_mover(nueva_pieza, 0, 0, tablero):
        return nueva_pieza
    else:
        return pieza

def eliminar_filas_completas(tablero):
    filas_restantes = []
    eliminadas = 0
    for fila in tablero:
        if (0, 0, 0) not in fila:
            eliminadas += 1
        else:
            filas_restantes.append(fila)
    while len(filas_restantes) < FILAS:
        filas_restantes.insert(0, [(0, 0, 0) for _ in range(COLUMNAS)])
    return filas_restantes, eliminadas

def dibujar_tablero(pantalla, tablero):
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            color = tablero[fila][columna]
            if color != (0, 0, 0):
                pygame.draw.rect(
                    pantalla,
                    color,
                    (columna * TAM_CELDA, fila * TAM_CELDA, TAM_CELDA, TAM_CELDA)
                )

def dibujar_cuadricula(pantalla):
    for fila in range(FILAS):
        pygame.draw.line(pantalla, (200, 200, 200), (0, fila * TAM_CELDA), (Ancho, fila * TAM_CELDA), 1)
    for columna in range(COLUMNAS):
        pygame.draw.line(pantalla, (200, 200, 200), (columna * TAM_CELDA, 0), (columna * TAM_CELDA, Alto), 1)

def dibujar_pieza(pantalla, pieza, color):
    for fila, columna in pieza:
        pygame.draw.rect(
            pantalla,
            color,
            (columna * TAM_CELDA, fila * TAM_CELDA, TAM_CELDA, TAM_CELDA)
        )

def dibujar_puntaje(pantalla, puntuacion):
    texto = fuente.render(f"Puntos: {puntuacion}", True, (255, 255, 255))
    pantalla.blit(texto, (10, 10))

def dibujar_game_over(pantalla):
    texto = fuente_grande.render("GAME OVER", True, (255, 0, 0))
    pantalla.blit(texto, (Ancho // 2 - texto.get_width() // 2, Alto // 2 - texto.get_height() // 2))

def hard_drop(pieza, tablero):
    while puede_mover(pieza, 0, 1, tablero):
        pieza = [(f + 1, c) for f, c in pieza]
    return pieza

def reiniciar_juego():
    global tablero, pieza_actual, tipo_actual, puntuacion, tiempo_ultimo_movimiento, game_over
    tablero = crear_tablero_vacio()
    pieza_actual, tipo_actual = nueva_pieza()
    puntuacion = 0
    tiempo_ultimo_movimiento = pygame.time.get_ticks()
    game_over = False
    pygame.mixer.music.play(-1)  # reanuda música fondo al reiniciar

# Estado inicial
tablero = crear_tablero_vacio()
pieza_actual, tipo_actual = nueva_pieza()
puntuacion = 0
fuente = pygame.font.SysFont("Arial", 24)
fuente_grande = pygame.font.SysFont("Arial", 48)
intervalo = 500
tiempo_ultimo_movimiento = pygame.time.get_ticks()
game_over = False

# Bucle principal
while True:
    tiempo_actual = pygame.time.get_ticks()

    if not game_over and tiempo_actual - tiempo_ultimo_movimiento > intervalo:
        if puede_mover(pieza_actual, 0, 1, tablero):
            pieza_actual = [(f + 1, c) for f, c in pieza_actual]
        else:
            fijar_pieza(pieza_actual, tablero, COLORES[tipo_actual])
            tablero, eliminadas = eliminar_filas_completas(tablero)
            puntuacion += eliminadas * 100
            pieza_actual, tipo_actual = nueva_pieza()
            if not puede_mover(pieza_actual, 0, 0, tablero):
                game_over = True
                pygame.mixer.music.stop()   # paro música fondo cuando game over
                sonido_gameover.play()
        tiempo_ultimo_movimiento = tiempo_actual

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r and game_over:
                reiniciar_juego()
            if not game_over:
                if evento.key == pygame.K_DOWN:
                    if puede_mover(pieza_actual, 0, 1, tablero):
                        pieza_actual = [(f + 1, c) for f, c in pieza_actual]
                if evento.key == pygame.K_LEFT:
                    if puede_mover(pieza_actual, -1, 0, tablero):
                        pieza_actual = [(f, c - 1) for f, c in pieza_actual]
                if evento.key == pygame.K_RIGHT:
                    if puede_mover(pieza_actual, 1, 0, tablero):
                        pieza_actual = [(f, c + 1) for f, c in pieza_actual]
                if evento.key == pygame.K_UP:
                    pieza_actual = rotar_pieza(pieza_actual, tipo_actual, tablero)
                if evento.key == pygame.K_SPACE:
                    pieza_actual = hard_drop(pieza_actual, tablero)
                    fijar_pieza(pieza_actual, tablero, COLORES[tipo_actual])
                    tablero, eliminadas = eliminar_filas_completas(tablero)
                    puntuacion += eliminadas * 100
                    pieza_actual, tipo_actual = nueva_pieza()
                    if not puede_mover(pieza_actual, 0, 0, tablero):
                        game_over = True
                        pygame.mixer.music.stop()   # paro música fondo cuando game over
                        sonido_gameover.play()

    Pantalla.fill((30, 30, 60))
    dibujar_tablero(Pantalla, tablero)
    if not game_over:
        dibujar_pieza(Pantalla, pieza_actual, COLORES[tipo_actual])
    else:
        dibujar_game_over(Pantalla)
    dibujar_cuadricula(Pantalla)
    dibujar_puntaje(Pantalla, puntuacion)
    pygame.display.flip()