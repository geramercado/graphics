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

    return[y_nuevo,]
