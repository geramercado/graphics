#Rotacion
#Sesgado

import pygame
import numpy as np
import math

#inicializar pygame

pygame.init()

#funcion de transformacion
def transformar_punto(punto, matriz):
    punto_homog = np.array([punto[0], punto[1], 1])
    matriz_np = np.array(matriz)
    punto_transformado = matriz_np @ punto_homog
    return [punto_transformado[0], punto_transformado[1]]

def transformar_geometria(geometria, matriz):
    #aplicar transformacion a todos los puntos de una geometria
    return [transformar_punto(punto, matriz) for punto in geometria]

#crear una geometria de ejemplo
def crear_cuadrado(tamano):
    #centrar un cuadrado en el origen
    medio = tamano / 2 
    return [
        [-medio, -medio],
        [medio, -medio],
        [medio, medio],
        [-medio, medio]
    ]

#creamos la geometria
cuadrado = crear_cuadrado(80)
triangulo = [[0, -40], [-30, 30], [30, 30]] #esto nos genera un triangulo equilatero

#configuracion de pygame
ANCHO, ALTO = 900, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Rotacion sesgado Gerardo Mercado Hurtado")
reloj = pygame.time.Clock()


#parametros interactivos 
angulo_rotacion = 0
factor_sesgado_x = 0.0 #sesgado horizontal
factor_sesgado_y = 0.0 #sesgado verticcal 
centro_rotacion = [ANCHO//2, ALTO//2]
escala_visual = 1.5 

#colores 
BLANCO = (255, 255, 255)
NEGRO = (0,0,0)
AZUL = (59,130,246)
ROJO = (239,68,68)
VERDE = (34,197,94)
MORADO = (139,92,246)
GRIS = (209,213,219)
FONDO = (249,250,251)

#creamos las fuentes
fuente = pygame.font.SysFont('Arial', 16)
fuente_titulo = pygame.font.SysFont('Arial', 20, bold=True)


#creamos el bucle
ejecutandose = True
modo_automatico = True

while ejecutandose: 
    dt = reloj.tick(60) / 1000.0
    #manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutandose = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                modo_automatico = not modo_automatico
            elif evento.key == pygame.K_r:
                #con la tecla R se resetean los parametros
                angulo_rotacion = 0
                factor_sesgado_x = 0.0
                factor_sesgado_y = 0.0 
            elif evento.key == pygame.K_1:
                #activar el modo solo rotacion
                factor_sesgado_x = 0.0
                factor_sesgado_y = 0.0
            elif evento.key == pygame.K_2:
                #activar el modo solo sesgado
                angulo_rotacion = 0
    
    #actualizar parametrso modo automatico
    if modo_automatico:
        angulo_rotacion += 0.5 * dt #rotacion continua
        factor_sesgado_x = 0.3 * math.sin(pygame.time.get_ticks() / 1000)
        factor_sesgado_y = 0.2 * math.cos(pygame.time.get_ticks() / 800)

    #crear las matrices de transformacion
    #1.- la matriz de rotacion
    radianes = math.radians(angulo_rotacion)
    cos_theta = math.cos(radianes)
    sin_theta = math.sin(radianes)

    matriz_rotacion = [
        [cos_theta, -sin_theta, 0],
        [sin_theta, cos_theta, 0],
        [0,0,1]
    ]

    #2.- matriz de sesgado horizontal
    matriz_sesgado_x = [
        [1, factor_sesgado_x, 0],
        [0,1,0],
        [0,0,1]
    ]

    #3.- matriz de sesgado vertical
    matriz_sesgado_y = [
        [1,0,0],
        [factor_sesgado_y, 1, 0],
        [0,0,1]
    ]

    #4.- matriz de traslacion al centro de la pantalla
    matriz_traslacion = [
        [1,0, centro_rotacion[0]],
        [0,1, centro_rotacion[1]],
        [0,0,1]
    ]

    #5.- matriz de escala para visualizacion
    matriz_escala = [
        [escala_visual, 0,0],
        [0, escala_visual, 0],
        [0,0,1]
    ]

    #Combinar las transformaciones
    #orden: escala - sesgado_x -  sesgado_y - rotacion - traslacion
    matriz_temp = np.array(matriz_escala)
    matriz_temp = np.array(matriz_sesgado_x) @ matriz_temp
    matriz_temp = np.array(matriz_sesgado_y) @ matriz_temp
    matriz_temp = np.array(matriz_rotacion) @ matriz_temp
    matriz_final = np.array(matriz_traslacion) @ matriz_temp

    #aplicar las trasnformaciones
    cuadrado_transformado = transformar_geometria(cuadrado, matriz_final)
    triangulo_transformado = transformar_geometria(triangulo, matriz_final)

    #dibujar
    ventana.fill(FONDO)

    #dibujar las rejillas de referencia
    for x in range(0, ANCHO, 50):
        alpha = 50 if x %100 == 0 else 30
        color = (200,200,200, alpha)
        pygame.draw.line(ventana, color, (x, 0), (x, ALTO), 1)
    for y in range(0, ALTO, 50):
        alpha = 50 if y %100 == 0 else 30
        color = (200, 200, 200, alpha)
        pygame.draw.line(ventana, color, (0,y), (ANCHO, y), 1)

    #dibijar los ejes de las cordenadas
    pygame.draw.line(ventana, (150, 150, 150), (0, centro_rotacion[1]), (ANCHO, centro_rotacion[1]), 2)
    pygame.draw.line(ventana, (150, 150, 150), (centro_rotacion[0], 0), (centro_rotacion[0], ALTO), 2)
        
    #dibujar formas transformadas
    pygame.draw.polygon(ventana, AZUL, [(int(x), int(y)) for x, y in cuadrado_transformado], 3)
    pygame.draw.polygon(ventana, ROJO, [(int(x), int(y)) for x, y in triangulo_transformado], 3)

    #dibujar le ppunto central
    pygame.draw.circle(ventana, VERDE, centro_rotacion, 6)
    pygame.draw.circle(ventana, BLANCO, centro_rotacion, 3)

    # interfaz informativa
    pygame.draw.rect(ventana, (255, 255, 255, 200), (10, 10, 300, 150), 0, 10)
    pygame.draw.rect(ventana, NEGRO, (10, 10, 300, 150), 2, 10)

    textos = [
        f"rotacion: {angulo_rotacion:.1f}°",
        f"sesgado_x: {factor_sesgado_x:.2f}°",
        f"sesgado_y: {factor_sesgado_y:.2f}°",
        f"modo: {'automatico' if modo_automatico else 'manual'}",
        "controles:"
        "espacio - alternar modo",
        "r - resetear",
        "1 - solo rotar",
        "2 - solo sesgado"
    ]

    for i, texto in enumerate(textos):
        color = NEGRO if i < 4 else GRIS
        superficie = fuente.render(texto, True, color)
        ventana.blit(superficie, (20, 15 + i * 18))

    #titulo
    titulo = fuente_titulo.render("rotacion + sesgado + Gerardo MErcado Hurtado", True, MORADO)
    ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 20))

    #actualizar pantalla
    pygame.display.flip()


#finalizar
pygame.quit()



