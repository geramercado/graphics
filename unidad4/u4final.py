#Gerardo Mercado Hurtado
#Raúl Martínez Martínez

import pygame
import sys
import numpy
import math

pygame.init()
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot y su Perro Robot (Gerardo/Raúl)")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 80, 80)
GREEN = (100, 255, 100)
BLUE = (120, 150, 255)
YELLOW = (255, 255, 120)
GRAY = (180, 180, 180)
DARK_GRAY = (80, 80, 80)

# Variable para controlar la opción del cuadrado central
opcion_cuadro = 1  


# Textura simulada
textura = pygame.Surface((100, 100))
for i in range(0, 100, 10):
    pygame.draw.line(textura, GRAY, (i, 0), (i, 100), 2)
    pygame.draw.line(textura, GRAY, (0, i), (100, i), 2)

def draw_filled_polygon(surface, vertices, color, border_color=BLACK):
    pygame.draw.polygon(surface, color, vertices)
    pygame.draw.polygon(surface, border_color, vertices, 2)
    for vertex in vertices:
        pygame.draw.circle(surface, RED, vertex, 4)


def dibujar_cuadro_central(opcion):
    rect = pygame.Rect(WIDTH//2 - 50, HEIGHT//2 - 50, 100, 100)
    if opcion == 1:
        pygame.draw.rect(screen, BLUE, rect)
    elif opcion == 2:
        # Degradado
        for i in range(100):
            color = (0, int(i * 2.55), 255 - int(i * 2.55))
            pygame.draw.line(screen, color, (rect.x, rect.y + i), (rect.x + 100, rect.y + i))
    elif opcion == 3:
        # Textura
        screen.blit(textura, rect.topleft)
        pygame.draw.rect(screen, BLACK, rect, 2)
    elif opcion == 4:
        mouse_pos = pygame.mouse.get_pos()
        dibujar_esferas_luz_dinamico(mouse_pos)
    elif opcion == 5:
        mouse_pos = pygame.mouse.get_pos()
        dibujar_esferas_sombreado_dinamico(mouse_pos)

def mostrar_instrucciones():
    """Muestra las instrucciones en la esquina superior derecha"""
    font = pygame.font.Font(None, 24)
    instrucciones = [
        "Opciones de la figura central, Presiona las teclas 1, 2, 3, 4, 5",
        "1. Relleno uniforme",
        "2. Degradado",
        "3. Textura",
        "4. Luz ambiental, Difusa, Especular (El puntero de tu mouse simula la luz)",
        "5. Sombra FLAT, GOURAUD, PHONG (El puntero de tu mouse simula la luz)"
    ]
    
    x = WIDTH - 700
    y = 10
    for linea in instrucciones:
        label = font.render(linea, True, BLACK)
        screen.blit(label, (x, y))
        y += 25 





def dibujar_esferas_luz_dinamico(mouse_pos):
    """Dibuja tres esferas simulando luz ambiental, difusa y especular con luz que sigue al mouse"""
    tamaño = 100
    margen = 40
    x_inicial = WIDTH//2 - (3*tamaño + 2*margen)//2
    y = HEIGHT//2 - tamaño//2

    # Vector de luz basado en el mouse
    luz_x = mouse_pos[0] - WIDTH//2
    luz_y = mouse_pos[1] - HEIGHT//2
    luz_z = 200  # altura simulada
    luz = numpy.array([luz_x, luz_y, luz_z])
    luz = luz / numpy.linalg.norm(luz)

    # Función para calcular intensidad difusa y especular
    def intensidad_luz(normal, tipo='ambiental'):
        normal = normal / numpy.linalg.norm(normal)
        difusa = max(numpy.dot(normal, luz), 0)
        if tipo == 'ambiental':
            return 0.3  # tenue, color uniforme
        elif tipo == 'difusa':
            return difusa
        elif tipo == 'especular':
            view = numpy.array([0, 0, 1])
            reflejo = 2 * difusa * normal - luz
            especular = max(numpy.dot(reflejo, view), 0) ** 20
            return min(1, difusa + especular)

    # Luz ambiental
    centro1 = numpy.array([x_inicial + tamaño//2, y + tamaño//2])
    intensidad = int(255 * intensidad_luz(numpy.array([0,0,1]), 'ambiental'))
    pygame.draw.circle(screen, (intensidad, intensidad, intensidad), centro1.astype(int), tamaño//2)
    pygame.draw.circle(screen, BLACK, centro1.astype(int), tamaño//2, 2)

    # Luz difusa
    centro2 = numpy.array([x_inicial + tamaño + margen + tamaño//2, y + tamaño//2])
    for i in range(tamaño//2, 0, -1):
        normal = numpy.array([0, 0, 1])
        inten = int(255 * intensidad_luz(normal, 'difusa') * (i/(tamaño//2)))
        color = (inten, inten, inten)
        pygame.draw.circle(screen, color, centro2.astype(int), i)
    pygame.draw.circle(screen, BLACK, centro2.astype(int), tamaño//2, 2)

    # Luz especular
    centro3 = numpy.array([x_inicial + 2*(tamaño + margen) + tamaño//2, y + tamaño//2])
    for i in range(tamaño//2, 0, -1):
        normal = numpy.array([0,0,1])
        inten = int(255 * intensidad_luz(normal, 'especular') * (i/(tamaño//2)))
        color = (inten, inten, inten)
        pygame.draw.circle(screen, color, centro3.astype(int), i)
    pygame.draw.circle(screen, BLACK, centro3.astype(int), tamaño//2, 2)






def dibujar_esferas_sombreado_dinamico(mouse_pos):
    """Simula Flat, Gouraud y Phong con luz que sigue el mouse"""
    tamaño = 100
    margen = 40
    x_inicial = WIDTH//2 - (3*tamaño + 2*margen)//2
    y = HEIGHT//2 - tamaño//2

    # Convertir posición del mouse a vector de luz 3D simple
    luz_x = mouse_pos[0] - WIDTH//2
    luz_y = mouse_pos[1] - HEIGHT//2
    luz_z = 200  # altura simulada
    luz = numpy.array([luz_x, luz_y, luz_z])
    luz = luz / numpy.linalg.norm(luz)

    def calcular_intensidad(normal, tipo='flat'):
        normal = normal / numpy.linalg.norm(normal)
        difusa = max(numpy.dot(normal, luz), 0)
        if tipo == 'flat':
            return 0.6  # color uniforme
        elif tipo == 'gouraud':
            return difusa
        elif tipo == 'phong':
            # Agregar especular
            view = numpy.array([0, 0, 1])
            reflejo = 2 * difusa * normal - luz
            especular = max(numpy.dot(reflejo, view), 0) ** 20
            return difusa + especular

    # Flat shading
    centro1 = numpy.array([x_inicial + tamaño//2, y + tamaño//2])
    intensidad_flat = int(255 * calcular_intensidad(numpy.array([0, 0, 1]), 'flat'))
    pygame.draw.circle(screen, (intensidad_flat, intensidad_flat, intensidad_flat), centro1.astype(int), tamaño//2)
    pygame.draw.circle(screen, BLACK, centro1.astype(int), tamaño//2, 2)

    # Gouraud shading
    centro2 = numpy.array([x_inicial + tamaño + margen + tamaño//2, y + tamaño//2])
    for i in range(tamaño//2, 0, -1):
        normal = numpy.array([0, 0, 1])
        intensidad = int(255 * calcular_intensidad(normal, 'gouraud') * (i/(tamaño//2)))
        color = (intensidad, intensidad, intensidad)
        pygame.draw.circle(screen, color, centro2.astype(int), i)
    pygame.draw.circle(screen, BLACK, centro2.astype(int), tamaño//2, 2)

    # Phong shading
    centro3 = numpy.array([x_inicial + 2*(tamaño + margen) + tamaño//2, y + tamaño//2])
    for i in range(tamaño//2, 0, -1):
        normal = numpy.array([0, 0, 1])
        intensidad = int(min(255, 255 * calcular_intensidad(normal, 'phong') * (i/(tamaño//2))))
        color = (intensidad, intensidad, intensidad)
        pygame.draw.circle(screen, color, centro3.astype(int), i)
    pygame.draw.circle(screen, BLACK, centro3.astype(int), tamaño//2, 2)






def main():
    clock = pygame.time.Clock()
    running = True
    global opcion_cuadro

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    opcion_cuadro = 1
                elif event.key == pygame.K_2:
                    opcion_cuadro = 2
                elif event.key == pygame.K_3:
                    opcion_cuadro = 3
                elif event.key == pygame.K_4:
                    opcion_cuadro = 4
                if event.key == pygame.K_5:
                    opcion_cuadro = 5

        screen.fill(WHITE)

        dibujar_cuadro_central(opcion_cuadro)
        mostrar_instrucciones() 

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

