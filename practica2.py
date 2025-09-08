import cv2
import numpy as np
from matplotlib import pyplot as plt

def mostrar_img_con_matplotlib(imagenes, titulo, cmap='gray'):
    
    n=len(imagenes)
    plt.figure(figsize=(15,8))

    for i in range(n):
        plt.subplot(2,3, i+1)
        plt.imshow(imagenes[i], cmap=cmap)
        plt.title(titulos[i])
        plt.axis('off')

    plt.tight_layout()
    plt.show()

img=cv2.imread('C:/graficacion/mg.JPG',0)

if img is None:
    print("Error: No se pudo cargar la imagen")
else:
    #1.- Filtro gausioano

    #kernel gausiano 3x3

    kernel_gaus=np.array([[1,2,1],[2,4,2],[1,2,1]])/16 

    #Aplicar convolucion
    blur_manual=cv2.filter2D(img, -1, kernel_gaus)

    #Comparar con funcion built-in de openCV
    blur_opencv=cv2.GaussianBlur(img, (3,3), 0)

    #Operador sobel
    #Calcular los gradientes
    sobelx=cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    sobely=cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)

    #Convertir a valores absolutos y escalar
    sobelx_abs=np.uint8(np.abs(sobelx))
    sobely_abs=np.uint8(np.abs(sobely))

    #Magnitud del gradiente
    magnitud_gradiente=np.sqrt(sobelx**2 + sobely**2)
    magnitud_uint8=np.uint8(magnitud_gradiente)

    #Mostrar los resultados
    imagenes = [img, blur_manual, blur_opencv, sobelx_abs, sobely_abs, magnitud_uint8]
    titulos = ['imagen original', 'filtros gausiano normal', 'filtro gausiano opncv',
               'sobelx bordes verticales', 'sobely bordes horizontales', 'magnitud del gradeinte todos los bordes']

    mostrar_img_con_matplotlib(imagenes, titulos)

    #4.- Explicaiocn adicional
    print("Informacion tecnica")
    print(f"dimension de la imagen: {img.shape}")
    print(f"kernel gausioano\n{kernel_gaus}")
    print("El operador sonel calcula aproximaciones de las derivadas")
    print("Gx detecta los bordes verticales, Gy detecta los horizontales")

