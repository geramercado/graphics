# sistema_solar_base.py
# CÓDIGO BASE PARA PROYECTO FINAL - SISTEMA SOLAR 3D
import pygame
import math
import numpy as np

# Inicializar Pygame
pygame.init()

# Configuración
ANCHO, ALTO = 1000, 700
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mi Sistema Solar 3D - [Tu Nombre]")
reloj = pygame.time.Clock()

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AMARILLO = (255, 255, 0)
AZUL = (0, 100, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
NARANJA = (255, 165, 0)

class Punto3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def copiar(self):
        return Punto3D(self.x, self.y, self.z)
    
    def restar(self, otro):
        return Punto3D(self.x - otro.x, self.y - otro.y, self.z - otro.z)
    
    def normalizar(self):
        longitud = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        if longitud == 0:
            return Punto3D(0, 0, 0)
        return Punto3D(self.x/longitud, self.y/longitud, self.z/longitud)

class Planeta:
    def __init__(self, radio, distancia, color, nombre, velocidad_orbita=1, velocidad_rotacion=1):
        self.radio = radio
        self.distancia = distancia
        self.color = color
        self.nombre = nombre
        self.velocidad_orbita = velocidad_orbita
        self.velocidad_rotacion = velocidad_rotacion
        
        # Estado actual
        self.angulo_orbita = 0
        self.angulo_rotacion = 0
        self.posicion = Punto3D(0, 0, 0)
        
        # Crear esfera simple
        self.crear_geometria()
    
    def crear_geometria(self):
        """Crea una esfera simple con caras triangulares"""
        self.vertices = []
        self.caras = []
        divisiones = 8
        
        # Generar vértices
        for i in range(divisiones + 1):
            latitud = math.pi * i / divisiones
            for j in range(divisiones):
                longitud = 2 * math.pi * j / divisiones
                x = self.radio * math.sin(latitud) * math.cos(longitud)
                y = self.radio * math.cos(latitud)
                z = self.radio * math.sin(latitud) * math.sin(longitud)
                self.vertices.append(Punto3D(x, y, z))
        
        # Generar caras triangulares
        for i in range(divisiones):
            for j in range(divisiones):
                v0 = i * divisiones + j
                v1 = i * divisiones + (j + 1) % divisiones
                v2 = (i + 1) * divisiones + j
                v3 = (i + 1) * divisiones + (j + 1) % divisiones
                
                if i > 0:
                    self.caras.append([v0, v1, v2])
                if i < divisiones - 1:
                    self.caras.append([v1, v3, v2])
    
    def actualizar(self, dt):
        """Actualiza la posición y rotación del planeta"""
        # Rotación sobre su eje
        self.angulo_rotacion += self.velocidad_rotacion * dt
        
        # Movimiento orbital
        self.angulo_orbita += self.velocidad_orbita * dt
        
        # Calcular nueva posición orbital
        x = math.cos(self.angulo_orbita) * self.distancia
        z = math.sin(self.angulo_orbita) * self.distancia
        self.posicion = Punto3D(x, 0, z)
    
    def obtener_vertices_rotados(self):
        """Retorna los vértices rotados según la rotación del planeta"""
        vertices_rotados = []
        cos_rot = math.cos(self.angulo_rotacion)
        sin_rot = math.sin(self.angulo_rotacion)
        
        for vertice in self.vertices:
            # Rotación en Y (eje vertical)
            x = vertice.x * cos_rot - vertice.z * sin_rot
            z = vertice.x * sin_rot + vertice.z * cos_rot
            y = vertice.y
            
            # Aplicar posición orbital
            x += self.posicion.x
            y += self.posicion.y
            z += self.posicion.z
            
            vertices_rotados.append(Punto3D(x, y, z))
        
        return vertices_rotados

class Camara:
    def __init__(self):
        self.posicion = Punto3D(0, 0, -500)
        self.distancia_vision = 500
    
    def proyectar(self, punto):
        """Convierte un punto 3D a coordenadas 2D de la pantalla"""
        # Punto relativo a la cámara
        x_rel = punto.x - self.posicion.x
        y_rel = punto.y - self.posicion.y
        z_rel = punto.z - self.posicion.z
        
        # Evitar división por cero
        if self.distancia_vision + z_rel == 0:
            return (ANCHO//2, ALTO//2)
        
        # Proyección perspectiva
        factor = self.distancia_vision / (self.distancia_vision + z_rel)
        x2d = x_rel * factor + ANCHO//2
        y2d = y_rel * factor + ALTO//2
        
        return (int(x2d), int(y2d))

class SistemaSolar:
    def __init__(self):
        self.planetas = []
        self.camara = Camara()
        self.crear_sistema_solar()
    
    def crear_sistema_solar(self):
        """Crea el sistema solar completo con 8 planetas + Luna"""
        # Sol
        self.planetas.append(Planeta(40, 0, AMARILLO, "Sol", 0, 0.2))

        # Mercurio
        self.planetas.append(Planeta(6, 100, (169, 169, 169), "Mercurio", 4.15, 0.8))

        # Venus
        self.planetas.append(Planeta(10, 150, (255, 204, 102), "Venus", 1.62, -0.3))

        # Tierra
        self.tierra = Planeta(10, 200, (0, 100, 255), "Tierra", 1.0, 1.0)
        self.planetas.append(self.tierra)

        # Luna (orbita a la Tierra)
        self.luna = Planeta(3, 25, (220, 220, 220), "Luna", 12.0, 0.5)

        # Marte
        self.planetas.append(Planeta(8, 260, ROJO, "Marte", 0.53, 1.03))

        # Júpiter
        self.planetas.append(Planeta(22, 360, (255, 165, 0), "Júpiter", 0.084, 2.4))

        # Saturno
        self.planetas.append(Planeta(18, 450, (210, 180, 140), "Saturno", 0.034, 2.3))

        # Urano
        self.planetas.append(Planeta(14, 530, (173, 216, 230), "Urano", 0.011, -1.4))

        # Neptuno
        self.planetas.append(Planeta(14, 600, (70, 130, 180), "Neptuno", 0.006, 1.5))
    
    def actualizar(self, dt):
        """Actualiza todos los planetas"""
        for planeta in self.planetas:
            planeta.actualizar(dt)

        # Actualizar la Luna orbitando la Tierra
        self.luna.angulo_orbita += self.luna.velocidad_orbita * dt
        x = self.tierra.posicion.x + math.cos(self.luna.angulo_orbita) * self.luna.distancia
        z = self.tierra.posicion.z + math.sin(self.luna.angulo_orbita) * self.luna.distancia
        self.luna.posicion = Punto3D(x, 0, z)
        self.luna.angulo_rotacion += self.luna.velocidad_rotacion * dt
        
    def dibujar(self, ventana):
        """Dibuja todo el sistema solar"""
        # Fondo negro
        ventana.fill(NEGRO)
        
        # Dibujar órbitas
        for planeta in self.planetas:
            if planeta.distancia > 0:  # El sol no tiene órbita
                self.dibujar_orbita(planeta.distancia)
        
        # Dibujar planetas
        for planeta in self.planetas:
            self.dibujar_planeta(ventana, planeta)
            # Dibujar la Luna (después de los planetas)
        self.dibujar_planeta(ventana, self.luna)

        
        # Dibujar información
        self.dibujar_info(ventana)
    
    def dibujar_orbita(self, radio):
        """Dibuja la órbita de un planeta"""
        puntos = []
        for i in range(100):
            angulo = 2 * math.pi * i / 100
            x = math.cos(angulo) * radio
            z = math.sin(angulo) * radio
            punto_3d = Punto3D(x, 0, z)
            punto_2d = self.camara.proyectar(punto_3d)
            puntos.append(punto_2d)
        
        if len(puntos) > 1:
            pygame.draw.lines(ventana, (100, 100, 100), True, puntos, 1)
    
    def dibujar_planeta(self, ventana, planeta):
        """Dibuja un planeta en 3D"""
        vertices_rotados = planeta.obtener_vertices_rotados()
        
        # Dibujar caras
        for cara in planeta.caras:
            puntos_2d = []
            for indice_vertice in cara:
                vertice = vertices_rotados[indice_vertice]
                punto_2d = self.camara.proyectar(vertice)
                puntos_2d.append(punto_2d)
            
            if len(puntos_2d) == 3:
                pygame.draw.polygon(ventana, planeta.color, puntos_2d)
                pygame.draw.polygon(ventana, BLANCO, puntos_2d, 1)
        
        # Dibujar nombre
        centro_2d = self.camara.proyectar(planeta.posicion)
        if centro_2d:
            fuente = pygame.font.SysFont('Arial', 12)
            texto = fuente.render(planeta.nombre, True, BLANCO)
            ventana.blit(texto, (centro_2d[0] + 10, centro_2d[1]))
    
    def dibujar_info(self, ventana):
        """Dibuja información en pantalla"""
        fuente = pygame.font.SysFont('Arial', 16)
        
        info = [
            "MI SISTEMA SOLAR 3D",
            "Controles:",
            "W/S: Acercar/Alejar cámara",
            "A/D: Rotar vista",
            "R: Reiniciar vista",
            "ESPACIO: Pausar/Reanudar",
            "",
            f"Planetas: {len(self.planetas)}"
        ]
        
        for i, linea in enumerate(info):
            texto = fuente.render(linea, True, BLANCO)
            ventana.blit(texto, (10, 10 + i * 25))

def main():
    sistema = SistemaSolar()
    pausado = False
    
    # Bucle principal
    ejecutando = True
    while ejecutando:
        dt = reloj.tick(60) / 1000.0
        
        # Manejar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pausado = not pausado
                elif evento.key == pygame.K_r:
                    sistema.camara.posicion = Punto3D(0, 0, -500)
        
        # Controles de cámara
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w]:
            sistema.camara.posicion.z += 100 * dt
        if teclas[pygame.K_s]:
            sistema.camara.posicion.z -= 100 * dt
        if teclas[pygame.K_a]:
            # Rotar vista horizontalmente
            angulo = 2 * dt
            x_nuevo = sistema.camara.posicion.x * math.cos(angulo) - sistema.camara.posicion.z * math.sin(angulo)
            z_nuevo = sistema.camara.posicion.x * math.sin(angulo) + sistema.camara.posicion.z * math.cos(angulo)
            sistema.camara.posicion.x, sistema.camara.posicion.z = x_nuevo, z_nuevo
        
        # Actualizar sistema
        if not pausado:
            sistema.actualizar(dt)
        
        # Dibujar
        sistema.dibujar(ventana)
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()

