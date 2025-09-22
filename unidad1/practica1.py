import cv2 
import numpy as np

#carga la imagen en escala de grises
img = cv2.imread('C:/graficacion/mg.JPG',0)

if img is None:
    print("error: no se pudo cargar la imagen")

else:
    img_eq = cv2.equalizeHist (img)
    #muestra las imagenes
    cv2.imshow('original', img)
    cv2.imshow('ecualizada', img_eq)
    #Sesan las pantallas
    cv2.waitKey(0)
    cv2.destroyAllWindows()



