#Fractales

#Gerardo Mercado Hurtado

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
NARANJA = (200, 165, 0)
AMARILLO = (255, 255, 0)

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
        py = p1[1] + (dy + dx * direccion) / 2
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
    "arbol": {"nivel_max": 10, "angulo_ramificacion": 30, "longitud": 150, "color": MORADO},
    "mandelbrot": {"nivel_max": 15, "max_iter": 100, "x_min": -2.5, "x_max": 1.0, "y_min": 1.5, "y_max": 1.5},
    "dragon": {"nivel_max": 12, "color": NARANJA}
}


superficie_mandelbrot = pygame.Surface((ANCHO, ALTO))
mandelbrot_actualizado = False


ejecutando = True

while ejecutando:
    dt = reloj.tick(60) / 1000.0

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_1:
                fractal_actual = "sierpinski"
            elif evento.key == pygame.K_2:
                fractal_actual = "koch"
            elif evento.key == pygame.K_3:
                fractal_actual = "arbol"
            elif evento.key == pygame.K_4:
                fractal_actual = "mandelbrot"
            elif evento.key == pygame.K_5:
                fractal_actual = "dragon"
            
            #control de nivel si solo el fractal usa niveles
            elif evento.key == pygame.K_UP:
                if fractal_actual != "mandelbrot": #mandelbrot no usa niveles
                    if nivel_recursion < parametros[fractal_actual]["nivel_max"]:
                        nivel_recursion += 1
            elif evento.key == pygame.K_DOWN:
                if fractal_actual != "mandelbrot": #mandelbrot no usa noveles
                    if nivel_recursion > 0:
                        nivel_recursion -= 1
            
            elif evento.key == pygame.K_LEFT and fractal_actual == "arbol":
                parametros["arbol"]["angulo_ramificacion"] = max(10, parametros["arbol"]["angulo_ramificacion"] - 5)

            elif evento.key == pygame.K_RIGHT and fractal_actual == "arbol":
                parametros["arbol"]["angulo_ramificacion"] = min(80, parametros["arbol"]["angulo_ramificacion"] + 5)

            elif evento.key == pygame.K_z and fractal_actual == "mandelbrot":
                centro_x = (parametros["mandelbrot"]["x_min"] + parametros["mandelbrot"]["x_max"]) / 2
                centro_y = (parametros["mandelbrot"]["y_min"] + parametros["mandelbrot"]["y_max"]) / 2
                ancho = (parametros["mandelbrot"]["x_max"] + parametros["mandelbrot"]["x_min"]) / 2
                alto = (parametros["mandelbrot"]["y_max"] + parametros["mandelbrot"]["x_min"]) / 2

                parametros["mandelbrot"]["x_min"] = centro_x - ancho
                parametros["mandelbrot"]["x_max"] = centro_x + ancho
                parametros["mandelbrot"]["y_min"] = centro_y - alto
                parametros["mandelbrot"]["y_max"] = centro_y + alto
                mandelbrot_actualizado = False

    #dibujar
    ventana.fill(FONDO)

    if fractal_actual == "sierpinski":
        p1 = (ANCHO // 2, 100)
        p2 = (100, ALTO - 100)
        p3 = (ANCHO - 100, ALTO - 100)
        dibujar_sierpinski(ventana, nivel_recursion, p1, p2, p3, parametros ["sierpinski"]["color"])

    elif fractal_actual == "koch":
        p1 = (100, ALTO // 2)
        p2 = (ANCHO - 100, ALTO // 2)
        dibujar_koch(ventana, nivel_recursion, p1, p2, parametros["koch"]["color"])

    elif fractal_actual == "arbol":
        inicio = (ANCHO // 2, ALTO - 50)
        dibujar_arbol(ventana, nivel_recursion, inicio, -90,
                            parametros["arbol"]["longitud"],
                            parametros["arbol"]["angulo_ramificacion"],
                            parametros["arbol"]["color"]
        )

    elif fractal_actual == "mandelbrot":
        if not mandelbrot_actualizado:
            superficie_mandelbrot.fill(FONDO)
            dibujar_mandelbrot(superficie_mandelbrot, 
                                parametros["mandelbrot"]["x_min"],
                                parametros["mandelbrot"]["x_max"],
                                parametros["mandelbrot"]["y_min"],
                                parametros["mandelbrot"]["y_max"],
                                parametros["mandelbrot"]["max_iter"]
            )
            mandelbrot_actualizado = True
        ventana.blit(superficie_mandelbrot, (0,0))

    elif fractal_actual == "dragon":
        p1 = (ANCHO // 3, ALTO // 2)
        p2 = (2 * ANCHO // 3, ALTO // 2)
        dibujar_dragon(ventana, nivel_recursion, p1, p2, parametros["dragon"]["color"])


# --- INTERFAZ DE USUARIO MEJORADA ---
    pygame.draw.rect(ventana, (40, 40, 50, 200), (10, 10, 350, 200), 0, 10)
    pygame.draw.rect(ventana, MORADO, (10, 10, 350, 200), 2, 10)
    
    titulo = fuente_titulo.render("Visualizador de Fractales", True, BLANCO)
    ventana.blit(titulo, (20, 20))
    
    nombres_fractales = {
        "sierpinski": "Triángulo de Sierpinski",
        "koch": "Copo de Nieve de Koch",
        "arbol": "Árbol Fractal",
        "mandelbrot": "Conjunto de Mandelbrot",
        "dragon": "Curva del Dragón"
    }
    
    # TEXTO MEJORADO: Muestra controles diferentes para Mandelbrot
    textos_info = [
        f"Fractal: {nombres_fractales[fractal_actual]}",
        f"Nivel: {nivel_recursion}" if fractal_actual != "mandelbrot" else "Iteraciones: 100",
        "",
        "CONTROLES:",
        "1-5: Cambiar fractal",
    ]
    
    if fractal_actual != "mandelbrot":
        textos_info.extend([
            "↑↓: Aumentar/disminuir nivel",
            "",
            "CONTROLES ESPECÍFICOS:",
            "←→: Ángulo ramificación (árbol)" if fractal_actual == "arbol" else ""
        ])
    else:
        textos_info.extend([
            "Z/X: Zoom in/out",
            "",
            "El Mandelbrot no usa niveles de recursión",
            "Usa Z/X para hacer zoom"
        ])
    
    for i, texto in enumerate(textos_info):
        if texto:  # Solo dibujar si el texto no está vacío
            color = VERDE if i == 0 else (AMARILLO if i == 1 else BLANCO)
            surf = fuente.render(texto, True, color)
            ventana.blit(surf, (20, 50 + i * 18))
    
    # Información específica del fractal
    info_y = ALTO - 150
    pygame.draw.rect(ventana, (40, 40, 50, 200), (10, info_y, 400, 140), 0, 10)
    pygame.draw.rect(ventana, AZUL, (10, info_y, 400, 140), 2, 10)
    
    info_titulo = fuente_subtitulo.render("Información del Fractal", True, BLANCO)
    ventana.blit(info_titulo, (20, info_y + 10))
    
    if fractal_actual == "sierpinski":
        info_textos = [
            "• Dimensión fractal: log₂(3) ≈ 1.585",
            "• Autosimilaridad perfecta",
            "• Primer fractal descubierto (1915)",
            "• Aplicaciones: antenas, compresión"
        ]
    elif fractal_actual == "koch":
        info_textos = [
            "• Dimensión fractal: log₄(3) ≈ 1.262",
            "• Longitud infinita, área finita",
            "• Curva continua no diferenciable",
            "• Modelado de costas naturales"
        ]
    elif fractal_actual == "arbol":
        info_textos = [
            f"• Ángulo: {parametros['arbol']['angulo_ramificacion']}°",
            "• Simula crecimiento de árboles",
            "• Usado en gráficos 3D y naturaleza",
            "• Algoritmo L-system"
        ]
    elif fractal_actual == "mandelbrot":
        info_textos = [
            "• Conjunto más famoso",
            "• Dimensión fractal: 2",
            "• Frontera infinitamente compleja",
            "• Descubierto por Benoit Mandelbrot"
        ]
    else:
        info_textos = [
            "• Dimensión fractal: 2",
            "• Llena el plano",
            "• También llamado 'dragón de Heighway'",
            "• Aplicaciones: diseño de circuitos"
        ]
    
    for i, texto in enumerate(info_textos):
        surf = fuente.render(texto, True, BLANCO)
        ventana.blit(surf, (20, info_y + 40 + i * 16))
    
    pygame.display.flip()

pygame.quit()

