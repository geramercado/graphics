#Trasladar
#Resetear

#importando las librerias necesarias
import pygame
import numpy as np
import os

pygame.init()

#funcion para transformar matrices 3x3
def transformar_punto_homogeneo(punto, matriz):
    punto_homogeneo = np.array([punto [0], punto [1], 1])
    matriz_array = np.array(matriz)
    punto_trasnformado = matriz @ punto_homogeneo
    return [punto_trasnformado[0], punto_trasnformado[1]]

def transformar_geometria(geometria, matriz):
    #aplicar una transformacion a toda la geometria - lista de puntos
    return [transformar_punto_homogeneo(punto, matriz) for punto in geometria]

#configuracion de la ventana
ANCHO_VENTANA = 1000
ALTO_VENTANA = 600
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Traslacion mas escalamiento, Gerardo Mercado")
icono = pygame.Surface((32, 32))
icono.fill((255, 0, 0))
pygame.display.set_icon(icono)

#Tardar la imgane que vamos a ocupar
#Intentar cargar la imagen, si no eite vamos a crear un rectangulo de color
try:
    #colocar la ruta de la imagen
    imagen_original = pygame.image.load('C:/Users/Gerardo/Documents/graficacion/mg.JPG+')
    imagen_original = pygame.transform.scale(imagen_original, (100, 100))
    usar_imagen = True
    print("Imagen cargada corectamente")
except:
    print("no se encotro la imagen, usando forma geometrica...")
    usar_imagen = False

#definicion de la geometria alternatica si no hay imagen
if not usar_imagen:
    #usar una fomr a de nave espacial simple
    nave_espacial = [
        [0, -20], # punta superior 
        [15, 10], # ala derecha
        [40, 15], # propulsro derecho
        [20, 40], # base derecha 
        [0, 30], # propulsor izquierdo
        [-20, 40], 
        [-40, 15],
        [-15, 10]
    ]

    #centrar la geometria
    nave_centrada = [[x + 50, y + 50] for x, y in nave_espacial]

#parametros de transformacion
#traslacion inicial
tx, ty = 200, 200
#factores de escala
escala_normal = 1.0
escala_grande = 1.8
escala_pequeña = 0.6
escala_actual = escala_normal

#velocidades de animacion
velocidad_traslacion = 3
velocidad_escala = 0.02

#modo actual - 0: normal, 1 traslado, 2: escalado
modo_actual = 0
contador_animacion = 0


#coores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (30, 144, 255)
ROJO = (220, 20, 60)
VERDE = (50, 205, 50)
MORADO = (147, 112, 219)
GRIS = (100, 100, 100)
FONDO = (240, 248, 255)

#fuentes
fuente_grande = pygame.font.SysFont('Arial', 24, bold=True)
fuente_pequeña = pygame.font.SysFont('Arial', 16)

#bucle principal
reloj = pygame.time.Clock()
ejecutandose = True

while ejecutandose:
    dt = reloj.tick(60) / 1000.0 #delta time en segundos

    #manejo de evntos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutandose = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_t: #teca t para trasladar
                modo_actual = 1
                contador_animacion = 0
            elif evento.key == pygame.K_e: #flecha para escalar
                modo_actual = 2
                contador_animacion = 0
            elif evento.key == pygame.K_r: #tecla para resetear
                tx, ty = 200, 200
                escala_actual = escala_normal
                modo_actual = 0
    #logica de animacion
    if modo_actual == 1: #modo animacion
        contador_animacion += dt
        if contador_animacion < 2.0: # 2 segunods  de animacion
            tx += velocidad_traslacion * 2 
            ty += velocidad_traslacion
        else:
            modo_actual = 0

    elif modo_actual == 2:
        contador_animacion += dt
        if contador_animacion < 1.5:
            escala_actual = escala_normal + 0.5 * np.sin(contador_animacion * 4)
        else:
            modo_actual = 0
            escala_actual = escala_normal
    # matrices de transformacion
    #matriz de traslacion
    matriz_traslacion = [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ]

    #matriz escalonamiento
    matriz_escalonamiento = [
        [escala_actual, 0, 0],
        [0, escala_actual, 0],
        [0, 0, 1]
    ]

    #matriz combinada: primero escalar, luego trasladar
    matriz_combinada = np.array(matriz_traslacion) @ np.array(matriz_escalonamiento)

    #dibujado
    ventana.fill(FONDO)

    #dibujar rejillas de referencia

    for x in range(0, ANCHO_VENTANA, 50):
        pygame.draw.line(ventana, (220, 220, 200), (x,0), (x, ALTO_VENTANA), 1)
    for y in range(0, ALTO_VENTANA, 50):
        pygame.draw.line(ventana, (220, 220, 200), (0,y), (ANCHO_VENTANA, y), 1)

    #dibujar los ejes principales
    pygame.draw.line(ventana, GRIS, (0, ALTO_VENTANA//2), (ANCHO_VENTANA, ALTO_VENTANA//2), 2)
    pygame.draw.line(ventana, GRIS, (ANCHO_VENTANA//2, 0), (ANCHO_VENTANA//2, ALTO_VENTANA))

    #dibujar le objeto transformado
    if usar_imagen:
        #caluclar posicion y tamaño para la imagen
        ancho_imagen = int(100 * escala_actual)
        alto_imagen = int(100 * escala_actual)
        imagen_escalada = pygame.transform.scale(imagen_original, (ancho_imagen, alto_imagen))
        ventana.blit(imagen_escalada, (tx - ancho_imagen//2, ty - alto_imagen//2))
    else:

        nave_transformada = transformar_geometria(nave_centrada, matriz_combinada)
        puntos_dibujables = [(int(x), int(y)) for x, y in nave_transformada]
        pygame.draw.polygon(ventana, AZUL, puntos_dibujables, 0)
        pygame.draw.polygon(ventana, NEGRO, puntos_dibujables, 2)

    #dibujar punto central
    pygame.draw.circle(ventana, ROJO, (int(tx), int(ty)), 5)


    pygame.draw.rect(ventana, (240, 240, 240), (10, 10, 300, 120), 0, 10)
    pygame.draw.rect(ventana, NEGRO, (10, 10, 300, 120), 2, 10)

    texto_titulo = fuente_grande.render("Transformaciones 2D", True, MORADO)
    texto_posicion = fuente_pequeña.render(f"posicion: ({int(tx)}, {int(ty)})", True, NEGRO)
    texto_escala = fuente_pequeña.render(f"Escala: {escala_actual:.2f}x", True, NEGRO)
    texto_controles = fuente_pequeña.render("Controles: T= trasladar, E: escalar, R= reset", True, VERDE)


    ventana.blit(texto_titulo, (20, 20))
    ventana.blit(texto_posicion, (20, 50))
    ventana.blit(texto_escala, (20, 70))
    ventana.blit(texto_controles, (20, 90))

    #indicador de modo actual
    if modo_actual == 1:
        texto_modo = fuente_pequeña.render("modo: traslacion activa", True, ROJO)
        ventana.blit(texto_modo, (20, 110))
    elif modo_actual == 2:
        texto_modo = fuente_pequeña.render("modo: escalonamiento activo", True, ROJO)
        ventana.blit(texto_modo, (20, 100))
        #actualizar pantalla
    pygame.display.flip()

#cerrar el juego
pygame.quit()



