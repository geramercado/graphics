


import pygame
import numpy as np
import math
import random

#inicializar pygame

pygame.init()

#configuracion

ANCHO, ALTO = 1000, 800
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("visualizar fractales gerardo mercado")
reloj = pygame.time.Clock()


#colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (59, 130, 246)
ROJO = (239, 68, 8)
VERDE = (34, 97, 94)
MORADO = (139, 92, 246)
GRIS = (209, 213, 219)
FONDO = (249, 250, 251)