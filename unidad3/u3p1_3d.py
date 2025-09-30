#importando las librerias
#GerardoMErcadoHurtado
#Graficaicon en 3D
import pygame
import math

#inicializamos pygame.init
pygame.init()

#configuramos la ventana
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Clase 1: graficos en 3D Gerardo Mercado")
reloj = pygame.time.Clock()

#colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (30, 144, 255)
ROJO = (220, 20, 60)
VERDE = (50, 205, 50)

class Punto3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def proyectar(self, distancia_vision=500):
        #convertir de 3d a 2d con perspectiva
        if distancia_vision + self.z == 0:
            return (ANCHO // 2, ALTO // 2)
        factor = distancia_vision / (distancia_vision + self.z)
        x2d = self.x * factor + ANCHO // 2
        y2d = self.y * factor + ALTO // 2
        return (int(x2d), int(y2d))
    
#crear puhtos de ejenplo
puntos = [
    Punto3D(-100, -100, -200), #esquina superior izquierda - cerca
    Punto3D(100, -100, -200), #esquina superior derecha - cerca
    Punto3D(0, 100, -200,), #abajo centro - cerca
    Punto3D(-150, -150, 100), #esquina superior izquierda- lejos
    Punto3D(150, -150, 100), #esuina superior derecha - lejos
    Punto3D(0, 150, 100), #abajo centro - lejos
    Punto3D(0, 0, 0), #en el centro
]

#crear las cariables de control
distancia_vision = 500
mostrar_ejes = True
timepo = 0

#bucle principal
ejecutando = True

while ejecutando:
    #control de tiempo
    dt = reloj.tick(60) / 1000.0
    timepo += dt

    #creamos el manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            #crear los controles de la camara
            if evento.key == pygame.K_UP:
                distancia_vision = max(100, distancia_vision - 50)
            elif evento.key == pygame.K_DOWN:
                distancia_vision = min(1000, distancia_vision + 50)
            #mostare ocultar ejes
            elif evento.key == pygame.K_e:
                mostrar_ejes = not mostrar_ejes
            #reiniciar la animacion
            elif evento.key == pygame.K_r:
                timepo = 0

    radio = 100
    puntos[0].x = math.cos(timepo) * radio
    puntos[0].z = math.sin(timepo) * radio - 200

    #dibujando
    ventana.fill(NEGRO)

    #dibujar ejes cordenados
    if mostrar_ejes:
        origen = Punto3D(0, 0, 0)
        ox, oy = origen.proyectar(distancia_vision)

        #eje x color rojo
        fin_x = Punto3D(200, 0, 0)
        fx, fy = fin_x.proyectar(distancia_vision)
        pygame.draw.line(ventana, ROJO, (ox, oy), (fx, fy), 2)

        #eje y color verde
        fin_y = Punto3D(0, 200, 0)
        fx, fy = fin_y.proyectar(distancia_vision)

        pygame.draw.line(ventana, VERDE, (ox, oy), (fx, fy), 2)

    #dibujar puntos
    for i, punto in enumerate(puntos):
        x2d, y2d = punto.proyectar(distancia_vision)
        #color segun distancia
        brillo = max(100, 255 - abs(punto.z) // 2)
        if punto.z < 0: #puntos mas cercanos
            color = (brillo, brillo, 100) # color mas amarillo
        else:   #puntos mas lejanos
            color = (100, 100, brillo) #azulado

        #tamaño segun distancia
        tamano = max(3, 8 - abs(punto.z) // 50)
        pygame.draw.circle(ventana, color, (x2d, y2d), tamano)

    fuente = pygame.font.SysFont('Arial', 24)
    info_textos = [
        f"distancia: {distancia_vision}",
        f"puntos: {len(puntos)}",
        "controles: arirbaabajo Zoom, e= ejes, R= reiniciar"
    ]

    for i, texto in enumerate(info_textos):
        render = fuente.render(texto, True, BLANCO)
        ventana.blit(render, (10, 10 + i * 30))

    pygame.display.flip()


pygame.quit


