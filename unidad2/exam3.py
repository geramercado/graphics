#Gerardo Mercado Hurtado 
#Agustin Paniagua Flores

import pygame
import numpy as np

pygame.init()

# Funciones de transformación
def transformar_punto_homogeneo(punto, matriz):
    punto_homogeneo = np.array((punto[0], punto[1], 1))
    punto_transformado = matriz @ punto_homogeneo
    return [punto_transformado[0], punto_transformado[1]]

def transformar_geometria(geometria, matriz):
    return [transformar_punto_homogeneo(punto, matriz) for punto in geometria]

# Configuración de ventana
ANCHO_VENTANA = 1000
ALTO_VENTANA = 600
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Traslacion, Gerardo Mercado Hurtado/Agustin Paniagua Flores")
icono = pygame.Surface((32, 32))
icono.fill((255, 0, 0))
pygame.display.set_icon(icono)

# Intentar cargar imagen
try:
    imegen_original = pygame.image.load('ruta de la imagen')
    imegen_original = pygame.transform.scale(imegen_original, (100, 100))
    usar_iamgen = True
except:
    usar_iamgen = False

# Geometría alternativa: rombo centrado
if not usar_iamgen:
    rombo = [
        [0, -30],
        [30, 0],
        [0, 30],
        [-30, 0]
    ]
    nave_centrada = [[x + 50, y + 50] for x, y in rombo]

# Parámetros de transformación
tx, ty = 200, 200
escala_normal = 1.0
escala_actual = escala_normal
velocidad_traslacion = 3
modo_actual = 0
contador_animacion = 0

# Colores y fuentes
FONDO = (240, 248, 255)
AZUL = (30, 144, 255)
NEGRO = (0, 0, 0)
ROJO = (220, 20, 60)
VERDE = (50, 205, 50)
MORADO = (147, 112, 219)
GRIS = (100, 100, 100)
fuente_grande = pygame.font.SysFont('Arial', 24, bold=True)
fuente_pequeña = pygame.font.SysFont('Arial', 16)

# Bucle principal
relog = pygame.time.Clock()
ejecutandose = True

while ejecutandose:
    dt = relog.tick(60) / 1000.0

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutandose = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_t:
                modo_actual = 1
                contador_animacion = 0
            elif evento.key == pygame.K_e:
                modo_actual = 2
                contador_animacion = 0
            elif evento.key == pygame.K_r:
                tx, ty = 200, 200
                escala_actual = escala_normal
                modo_actual = 0

    # Movimiento manual con flechas
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        tx -= velocidad_traslacion
    if keys[pygame.K_RIGHT]:
        tx += velocidad_traslacion
    if keys[pygame.K_UP]:
        ty -= velocidad_traslacion
    if keys[pygame.K_DOWN]:
        ty += velocidad_traslacion

    # Animaciones
    if modo_actual == 1:
        contador_animacion += dt
        if contador_animacion < 2.0:
            tx += velocidad_traslacion * 2
            ty += velocidad_traslacion
        else:
            modo_actual = 0
    elif modo_actual == 2:
        contador_animacion += dt
        if contador_animacion < 1.5:
            escala_actual = escala_normal + 1.0 * np.sin(contador_animacion * 4)
        else:
            modo_actual = 0
            escala_actual = escala_normal

    # Matrices de transformación compuesta
    cx, cy = 50, 50
    matriz_trasladar_origen = [
        [1, 0, -cx],
        [0, 1, -cy],
        [0, 0, 1]
    ]
    matriz_escalonamiento = [
        [escala_actual, 0, 0],
        [0, escala_actual, 0],
        [0, 0, 1]
    ]
    matriz_regresar_centro = [
        [1, 0, cx],
        [0, 1, cy],
        [0, 0, 1]
    ]
    matriz_traslacion = [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ]
    matriz_combinada = (
        np.array(matriz_traslacion) @
        np.array(matriz_regresar_centro) @
        np.array(matriz_escalonamiento) @
        np.array(matriz_trasladar_origen)
    )

    # Dibujado
    ventana.fill(FONDO)

    for x in range(0, ANCHO_VENTANA, 50):
        pygame.draw.line(ventana, (220, 220, 200), (x, 0), (x, ALTO_VENTANA), 1)
    for y in range(0, ALTO_VENTANA, 50):
        pygame.draw.line(ventana, (220, 220, 200), (0, y), (ANCHO_VENTANA, y), 1)

    pygame.draw.line(ventana, GRIS, (0, ALTO_VENTANA // 2), (ANCHO_VENTANA, ALTO_VENTANA // 2), 2)
    pygame.draw.line(ventana, GRIS, (ANCHO_VENTANA // 2, 0), (ANCHO_VENTANA // 2, ALTO_VENTANA), 2)

    if usar_iamgen:
        ancho_imagen = int(100 * escala_actual)
        alto_imagen = int(100 * escala_actual)
        imagen_escalada = pygame.transform.scale(imegen_original, (ancho_imagen, alto_imagen))
        ventana.blit(imagen_escalada, (tx - ancho_imagen // 2, ty - alto_imagen // 2))
    else:
        nave_transformada = transformar_geometria(nave_centrada, matriz_combinada)
        puntos_dibujales = [(int(x), int(y)) for x, y in nave_transformada]
        pygame.draw.polygon(ventana, AZUL, puntos_dibujales, 0)
        pygame.draw.polygon(ventana, NEGRO, puntos_dibujales, 2)

    pygame.draw.circle(ventana, ROJO, (int(tx), int(ty)), 5)

    pygame.draw.rect(ventana, (240, 240, 240), (10, 10, 300, 120), 0, 10)
    pygame.draw.rect(ventana, NEGRO, (10, 10, 300, 120), 2, 10)
    ventana.blit(fuente_grande.render("Transformaciones 2D", True, MORADO), (20, 20))
    ventana.blit(fuente_pequeña.render(f"Posicion: ({int(tx)}, {int(ty)})", True, NEGRO), (20, 50))
    ventana.blit(fuente_pequeña.render(f"Escala: {escala_actual:.2f} x", True, NEGRO), (20, 70))
    ventana.blit(fuente_pequeña.render("Controles: T=Trasladar, E=Escalar, R=Reset", True, VERDE), (20, 90))

    if modo_actual == 1:
        ventana.blit(fuente_pequeña.render("modo: Traslacion Activa", True, ROJO), (20, 110))
    elif modo_actual == 2:
        ventana.blit(fuente_pequeña.render("modo: Escalamiento Activo", True, ROJO), (20, 110))

    pygame.display.flip()

pygame.quit()