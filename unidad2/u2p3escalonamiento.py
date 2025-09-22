#TEMA: ESCALONAMIENTO
import pygame
import numpy as np

#inicializar pygame
pygame.init()


#funcion para trasnformacion con matrices 3x3

def transformar_punto_homogeneo(punto, matriz):
    #transofrmar un punto 2D a una matriz homogenea
    punto_homogeneo = np.array([punto[0], punto[1], 1])
    matriz_array = np.array(matriz)
    punto_transformado = matriz_array @ punto_homogeneo
    return [punto_transformado[0], punto_transformado[1]]

#definir la geometria original
#creacion de un rectangulo y lo pondremos a la izquierda
rectangulo_original = [
    [100, 150],
    [200, 150],
    [200, 200],
    [100, 200]
]

#definicion de las matrices de escalonamiento
escala_uniforme = 1.5
matriz_escala_uniforme = [
    [escala_uniforme, 0, 0],
    [0, escala_uniforme, 0],
    [0, 0, 1]
]

escala_x = 2.0
escala_y = 0.5
matriz_escala_no_uniforme = [
    [escala_x, 0, 0],
    [0, escala_y, 0],
    [0, 0, 1]
]

#aplicar las transformaciones
rectangulo_escala_uniforme = []
rectangulo_escala_no_uniforme = []

for punto in rectangulo_original:
    punto_uniforme = transformar_punto_homogeneo(punto, matriz_escala_uniforme)
    rectangulo_escala_uniforme.append(punto_uniforme)

    punto_no_uniforme = transformar_punto_homogeneo(punto, matriz_escala_no_uniforme)
    rectangulo_escala_no_uniforme.append(punto_no_uniforme)

#configuracion de la ventana
ANCHO_VENTANA = 800
ALTO_VENTANA = 500

ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Transformacion escalamiento Geraro Mercado")

#definiciio de colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
GRIS = (200, 200, 200)

#fuente para el texto
fuente = pygame.font.SysFont('Arial', 16)

#Bucle principal para rendierizar la app
ejecutandose = True
while ejecutandose:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutandose = False
    #limpiamos la ventana
    ventana.fill(BLANCO)

    #dibujamos ejes de referencias
    pygame.draw.line(ventana, GRIS, (0, 250), (800, 250), 1) #eje x central
    pygame.draw.line(ventana, GRIS, (400, 0), (400, 500), 1) #eje x central

    #dibujar el priginal - azul - ala izquierda
    pygame.draw.polygon(ventana, AZUL, rectangulo_original, 3)

    uniforme_ajustado = []
    for punto in rectangulo_escala_uniforme:
        uniforme_ajustado.append([punto[0] + 200, punto[1]]) #mover a la derecha

    uniforme_dibujable = [(int(x), int(y)) for x, y in uniforme_ajustado]
    pygame.draw.polygon(ventana, VERDE, uniforme_dibujable, 3)

    no_uniforme_ajustado = []
    for punto in rectangulo_escala_no_uniforme:
        no_uniforme_ajustado.append([punto[0] + 400, punto[1]]) #mover a la derecha

    no_uniforme_dibujable = [(int(x), int(y)) for x, y in no_uniforme_ajustado]
    pygame.draw.polygon(ventana, ROJO, no_uniforme_dibujable, 3)

    #dibujar textos explicativos
    texto_original = fuente.render('original (sx=1, sy=1)', True, AZUL)
    texto_uniforme = fuente.render(f'escalamiento uniforme (sx=1.5, sy=1.5)', True, VERDE)
    texto_no_uniforme = fuente.render(f'escalamiento no uniforme (sx=2.0, sy=0.5)', True, ROJO)
    texto_explicacion = fuente.render('todos se escalan en el origen (0, 0)', True, NEGRO)

    ventana.blit(texto_original, (50, 50))
    ventana.blit(texto_uniforme, (300, 50))
    ventana.blit(texto_no_uniforme, (550, 50))
    ventana.blit(texto_explicacion, (200, 450))

    #dibujar punto origen 0,0
    pygame.draw.circle(ventana, NEGRO, (0, 0), 5)
    texto_origen = fuente.render('Origen (0, 0)', True, NEGRO)
    ventana.blit(texto_origen, (10, 10))

    pygame.draw.line(ventana, AZUL, (150, 220), (150, 300), 2)
    pygame.draw.line(ventana, VERDE, (350, 220), (350, 300), 2)
    pygame.draw.line(ventana, ROJO, (550, 220), (550, 300), 2)

    #actualizar pantalla
    pygame.display.flip()

#cerramos correctamente
pygame.quit()



