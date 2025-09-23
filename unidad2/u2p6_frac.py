#Fractales

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
NARANJA = (200, 68, 8)

#fuentes
fuente = pygame.font.SysFont('Arial', 16)
fuente_titulo = pygame.font.SysFont('Arial', 24, bold=True)
fuente_subtitulo = pygame.font.SysFont('Arial', 18, bold=True)


#algoritmos de los fractales
def dibujar_sierpinski(superficie, nivel, p1, p2, p3, color):
    #dibujar el triangulo de sierpinski recursivamente
    if nivel == 0:
        pygame.draw.polygon(superficie, color, [p1, p2, p3])
    else:
        p12 = ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)
        p23 = ((p2[0] + p3[0]) // 2, (p2[1] + p3[1]) // 2)
        p31 = ((p3[0] + p1[0]) // 2, (p3[1] + p1[1]) // 2)

        dibujar_sierpinski(superficie, nivel - 1, p1, p12, p31, color)
        dibujar_sierpinski(superficie, nivel - 1, p12, p2, p23, color)
        dibujar_sierpinski(superficie, nivel - 1, p31, p23, p3, color)

def dibujar_koch(superficie, nivel, p1, p2, color):
    #dibujar la curva de koch recursivamente
    if nivel == 0:
        pygame.draw.line(superficie, color, p1, p2, 2)
    else:
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]

        pA = (p1[0] + dx / 3 , p1[1] + dy / 3)
        pC = (p1[0] + 2 * dx / 3, p1[1] + 2 * dy / 3)

        angle = math.radians(60)
        pBx = pA[0] + (dx / 3) * math.cos(angle) - (dy / 3) * math.sin(angle)
        pBy = pA[1] + (dx / 3) * math.sin(angle) + (dy / 3) * math.cos(angle)
        pB = (pBx, pBy)

        dibujar_koch(superficie, nivel - 1, p1, pA, color)
        dibujar_koch(superficie, nivel - 1, pA, pB, color)
        dibujar_koch(superficie, nivel - 1, pB, pC, color)
        dibujar_koch(superficie, nivel - 1, pC, p2, color)

def dibujar_arbol(superficie, nivel, inicio, angulo, longitud, angulo_ramificacion, color):
    #dibujar un arbol fractal recursivamente
    if nivel == 0:
        return
    
    radianes = math.radians(angulo)
    fin = (inicio[0] + longitud * math.cos(radianes),
           inicio[1] + longitud * math.sin(radianes)
           )
    
    pygame.draw.line(superficie, color, inicio, fin, max(1, nivel))

    dibujar_arbol(superficie, nivel - 1, fin, angulo - angulo_ramificacion,
                  longitud * 0.7, angulo_ramificacion, color
                  )
    
    dibujar_arbol(superficie, nivel - 1, fin, angulo + angulo_ramificacion,
                  longitud * 0.7, angulo_ramificacion, color
                  )

def calcular_mandelbrot(c, max_iter = 100):
    #calcular si un punto peertenece al conjunto manderbrot
    z = complex(0, 0)
    for i in range(max_iter):
        z = z * z + c
        if abs(z) > 2:
            return i
    return max_iter

def dibujar_mandelbrot(superficie, x_min, x_max, y_min, y_max, max_iter = 100):
    #dibujar el conjunto de mandelbrot
    ancho, alto = superficie.get_size()

    for x in range(0, ancho, 2):
        for y in range(0, alto, 2):
            cx = x_min + (x / ancho) * (x_max - x_min)
            cy = y_min + ( y / alto) * ( y_max - y_min)
            c = complex(cx, cy)

            iteraciones = calcular_mandelbrot(c, max_iter)

            if iteraciones == max_iter:
                color = NEGRO
            else:
                t = iteraciones / max_iter
                r = int(9 * (1 - t) * t * t * t * 255)
                g = int(15 * (1 - t) * (1 - t) * t * t * 255)
                b = int(8.5 * (1 - t) * (1 - t) * (1 - t) * t * 255)
                color = (r, g, b)

            pygame.draw.rect(superficie, color, (x, y, 2, 2))

def dibujar_dragon(superficie, nivel, p1, p2, color, direccion = 1):
    #dibujar el dragon recursivamente
    if nivel == 0:
        pygame.draw.line(superficie, color, p1, p2, 2)
    else:
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]

        px = p1[0] + (dx - dy * direccion) / 2
        py = p1[1] + (dy - dx * direccion) / 2
        p_medio = (px, py)

        dibujar_dragon(superficie, nivel - 1, p1, p_medio, color, 1)
        dibujar_dragon(superficie, nivel - 1, p_medio, p2, color, -1)

#configuracion inicial
fractal_actual = "sierpinski"
nivel_recursion = 4

#parametros corregidos: para que todos tengan un nivel_max

parametros = {
    "sierpinski": {"nivel_max":8, "color": AZUL},
    "koch": {"nivel_max":5, "color": VERDE},
    "arbol": {"nivel_amx": 10, "angulo_ramificacion": 30, "longitud": 150, "color": MORADO},
    "mandelbrot": {"nivel_max": 15, "max_iter": 100, "x_min": -2.5, "x_max": 1.0, "y_min": 1.5, "y_max": 1.5},
    "dragon": {"nivel_max": 12, "color": NARANJA}
}

