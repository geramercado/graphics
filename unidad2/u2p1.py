#importar las librerias necesarias
import pygame           #sirve para la visualizacion grafica y la ventana
import numpy as np      #sirve para realizar operaciones matematicas con matrices de manera eficiente
import math             #para usar constantes como py o sqrt(raiz)

#Inicializar todos los modulos de Pygame
pygame.init()

#funcion fundamental que hace la transformacion de un punto 
#esta funcion aplica la operacion matemática P' = m*p 
def transformar_punto(punto, matriz):
    #transformar un punto 2D (x,y) usando una matriz de transformacion 2x2
    #argumentos:
    #punto (lista): una lista con las cordenadas [x,y] del punto original
    #matriz (list): una lista de listas 2x2 [[a,b],[c,d]] que representa la transformacion

    #returns:
    #list: una nueva lista [x_nuevo, y_nuevo] con las cordenadas del punto transformado

    #convertir la lista del punto en un array de numPy para, 
    #operarlo con la matriz.
    #Ej: [100,100] -> np.array([100,100])
    punto_array=np.array(punto)

    #convierte la lista de listas de la matriz en un array de Numpy 2x2
    #Ej: ([cos, -sin], [sin, cos] -> np.array([cos,-sin], [sin, cos]))
    matriz_array=np.array(matriz)

    #Realizamos una multiplicacion de matrices: Matriz (2x2)
    # @ Vector (2, )
    #El operador @ en Numpy está sobrecargado para hacer multiplicaiocnes de matrices
    punto_transformado=matriz_array @ punto_array

    #convertir el resultado de vuelta a una lista de python simple [x, y] para usarlo facilmente
    return punto_transformado.tolist()

#Definicion de la geometria original
#creamos una lista de puntos (vertices) que definen el triangulo 
#Cada punto es una lista de [cordenada_x, cordenada_y].
#Este es el objeto que vamos a transformar.

triangulo_original=[
    [100, 100], #vertice inferior izquierdo
    [150, 100], #vertice inferior derecho
    [125, 50]   #vertice superior (punta)
]

#Definicion de la matriz de transformacion
#Elegimos un ángulo de rotación de 45 grados.

angulo_grados=45
#convertir el angulo de grados a radianes porque las funciones mat.sin y math.cos trabajan con radianes
angulo_radianes=math.radians(angulo_grados)

#calculamos el seno y el coseno del angulo una sola vez para la eficiencia
coseno=math.cos(angulo_radianes)
seno=math.sin(angulo_radianes)

#construimos la matriz de rotacion de 2x2
#matriz R=[[cos(), -sin()], [sin(), cos()]]
matriz_rotacion=[
    [coseno, -seno],
    [seno, coseno]
]

#Aplicar la transformacion a la geometria
#Creamos una lista vacia para guardar los nuevos puntos del triangulo transformado
triangulo_transformado=[]

#recorremos cada punto(vertices) en el triangulo original
for punto in triangulo_original:
    #llamamos nuestra funcion para transformar el punto usando la matriz de rotacion
    punto_nuevo=transformar_punto(punto, matriz_rotacion)
    #añadir el punto transformado a la nueva lista.
    triangulo_transformado.append(punto_nuevo)

#configuracion de la ventana pygame, definir el tamaño de la ventana de visualizacion
ANCHO_VENTANA=400
ALTO_VENTANA=400
#crear la ventana con el tamaño especificado
ventana=pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
#le ponemos un titulo a la ventana
pygame.display.set_caption("transformaciones 2D, rotacion 45 (2x2)")

#definicion de colores RGB
BLANCO=(255,255,255)
AZUL=(0,0,255)   #color para el triangulo original
ROJO=(255,0,0)  #color para el triangulo

# blucle principal de l ampliacacion
#
ejecutandose=True
while ejecutandose:
        #manejo de eventos
        #revisamos que todos los eventos que paygame ha detectado (cliec, teclas, etc)
    for evento in pygame.event.get():
            #
        if evento.type==pygame.QUIT:
            #cambiamos la variable para salir del bucle
            ejecutandose=False

    #logica del dibujo 
    #1.- limpiar la ventana llenable de color blaco en cada frame
    ventana.fill(BLANCO)

    #2.- dibujamos el triangulo original (en azul)
    #pygame.draw.polygon(superficie, color, lista_de_puntos, gorsor_de_linea)
    pygame.draw.polygon(ventana, AZUL, triangulo_original, 2)

    #3.- dibujar el trinagulo transformado (en rojo)
    #los puntos ttansofrmados nos lo da en coma flotante (ej. 123.456)
    #pygame necesitamos redondearlos

    triangulo_a_dibujar=[]
    for punto in triangulo_transformado:
        x_redondeado=int(round(punto[0]))
        y_redondeado=int(round(punto[1]))
        triangulo_a_dibujar.append((x_redondeado, y_redondeado))

    #dibujamos el triangulo con las cordenadas convertidas a entero 
    pygame.draw.polygon(ventana, ROJO, triangulo_a_dibujar, 2)

    #actualizar la pantalla
    #esto se hace que todo lo que dibujamos se muestre en la ventana
    pygame.display.flip()

#inicializacion
#una vez que salimos del bucle cerramos correctamente pygame
pygame.quit()
