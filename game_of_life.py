import time

import numpy as np
import pygame

pygame.init()

width, height = 500, 500
screen = pygame.display.set_mode((height, width))

# Color de fondo
bg = 25, 25, 25
screen.fill(bg)
# Celdas
nxC, nyC = 50, 50

# Ancho y alto de cada celda
dimCW = width / nxC
dimCH = height / nyC

# Inicializo matriz con ceros
gameState = np.zeros((nxC, nyC))

# Autómata palo:
# 0 1 0
# 0 1 0
# 0 1 0
gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1

# Control de la ejecución
pauseExec = True
pauseOneSec = False
# Finalización del juego:
endGame = False

# Ejecución principal (Main Loop):
while not endGame:

    newGameState = np.copy(gameState)
    screen.fill(bg)
    time.sleep(0.1)

    # Registro de eventos de teclado y mouse
    ev = pygame.event.get()

    for event in ev:

        if event.type == pygame.QUIT:
            endGame = True

        if event.type == pygame.KEYDOWN:
            pauseExec = not pauseExec

        # Click del mouse:
        mouseClick = pygame.mouse.get_pressed()

        # Posición del cursor en la pantalla:
        if sum(mouseClick) > 0:
            posX, posY, = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = not mouseClick[2]

        if mouseClick[1]:
            pauseExec = not pauseExec

    for y in range(0, nxC):
        for x in range(0, nyC):

            if not pauseExec:

                n_neigh = (
                        gameState[(x - 1) % nxC, (y - 1) % nyC]
                        + gameState[x % nxC, (y - 1) % nyC]
                        + gameState[(x + 1) % nxC, (y - 1) % nyC]
                        + gameState[(x - 1) % nxC, y % nyC]
                        + gameState[(x + 1) % nxC, y % nyC]
                        + gameState[(x - 1) % nxC, (y + 1) % nyC]
                        + gameState[x % nxC, (y + 1) % nyC]
                        + gameState[(x + 1) % nxC, (y + 1) % nyC]
                )

                # Una célula muerta con exactamente 3 vecinas vivas: "revive"
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1

                # Una célula viva con menos de 2 o más de 3 vecinas vivas : "muere"
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

            # Creación del polígono de cada celda a dibujar
            poly = [
                (int(x * dimCW), int(y * dimCH)),
                (int((x + 1) * dimCW), int(y * dimCH)),
                (int((x + 1) * dimCW), int((y + 1) * dimCH)),
                (int(x * dimCW), int((y + 1) * dimCH))
            ]

            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    # Actualizo gameState
    gameState = np.copy(newGameState)
    pygame.display.flip()

    if pauseOneSec:
        time.sleep(1)
