import pygame
import numpy as np

pygame.init()



def transformar_punto_homogeneo(punto, matriz):
    #convertirmos 
    punto_homogeneo=np.array([punto[0], punto[1], 1])

    #convertir la matriz array con numpy
    matriz_array=np.array(matriz)

    #multoplicar matriz de 3x3 por el vector homogeneo 3x1
    punto_transformado_homogeneo=matriz_array @ punto_homogeneo

    #convertir de vuelta a cordenadas cartesianas 2D(x´, /w. y´/w)
    #como w=1 en cordenadas homogeneas, podemos tomar solo x e y
    x_nuevo=punto_transformado_homogeneo[0]
    y_nuevo=punto_transformado_homogeneo[1]

    return[x_nuevo, y_nuevo]

triangulo_original=[
    [100, 100], #vertice inferior izquierdo
    [150, 100], #vertice inferior derecho
    [125, 50]   #vertice superior (punta)
]

cuadrado_original=[

    [50, 50],
    [100, 50],
    [100, 100],
    [50, 100]

]

tx=150
ty=100

matriz_traslacion=[

    [1, 0, tx],
    [0, 1, ty],
    [0, 0, 1]

]

triangulo_trasladado=[
    [1, tx], #vertice inferior izquierdo
    [0, ty], #vertice inferior derecho
    [0, 0]   #vertice superior (punta)
]

cuadrado_trasladado=[]
for punto in cuadrado_original:
    punto_trasladado=transformar_punto_homogeneo(punto, matriz_traslacion)
    cuadrado_trasladado.append(punto_trasladado)

#configuracion de la ventana pygame
ANCHO_VENTANA=400
ALTO_VENTANA=300

ventana=pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Transformacion 2D - traslación")

#Definicion de colores
BLANCO=(255, 255, 255) #PANTALLA
AZUL=(0, 0, 255) #Color para el cuadrado original
ROJO=(255, 0, 0) #Colot para el cuadrado trasladado
VERDE=(0, 255, 0) #Color para las felchas de traslacion

#Bucle principal de la aplicacion
ejecutandose=True
while ejecutandose:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutandose=False
    #limpiar la ventana
    ventana.fill(BLANCO)
    #dibujar el cuadrado original ; azul
    pygame.draw.polygon(ventana, AZUL, triangulo_original, 2)
    #dibujar el cuadrado trasladado - rojo
    #convertir las cordenadas float a entero para pygame
    cuadrado_dibujable=[]
    for punto in cuadrado_trasladado:
        x_int = int( round(punto[0]) )
        y_int = int( round(punto[1]) )
        cuadrado_dibujable.append((x_int, y_int))
    
    pygame.draw.polygon(ventana, ROJO, triangulo_trasladado, 2)

    #
    #
    centro_original=[75, 75] # centro aproximado del cuadrado original
    centro_trasladado=[255, 175] # centro

    #dibujar las felcha
    pygame.draw.line(ventana, VERDE, centro_original, centro_trasladado)

    #dibujar punto de la flechas
    #calcular la direccion del vector de traslacion 
    dx=centro_trasladado[0] - centro_original[0]
    dy=centro_trasladado[1] - centro_original[1]

    #actualizar la pantalla
    pygame.display.flip()

#cerrar pygame correctamente
pygame.quit()
