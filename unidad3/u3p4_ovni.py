#Gerardo Mercado Hurtado
# importar librerias
import pygame
import math

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ANCHO, ALTO = 1000, 700
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Clase 4: Rotaciones 3D - Giros en Tres Dimensiones")
reloj = pygame.time.Clock()

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 100, 255)
AMARILLO = (255, 255, 0)
MORADO = (255, 0, 255)
NARANJA = (255, 165, 0)
CIAN = (0, 255, 255)

class Punto3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def proyectar(self, distancia_vision=500):
        """Convierte 3D a 2D con perspectiva"""
        if distancia_vision + self.z == 0:
            return (ANCHO//2, ALTO//2)
        factor = distancia_vision / (distancia_vision + self.z)
        x2d = self.x * factor + ANCHO//2
        y2d = self.y * factor + ALTO//2
        return (int(x2d), int(y2d))
    
    def copiar(self):
        """Crea una copia del punto"""
        return Punto3D(self.x, self.y, self.z)
    
    def rotar_x(self, angulo):
        """Rota el punto alrededor del eje X"""
        rad = math.radians(angulo)
        nuevo_y = self.y * math.cos(rad) - self.z * math.sin(rad)
        nuevo_z = self.y * math.sin(rad) + self.z * math.cos(rad)
        return Punto3D(self.x, nuevo_y, nuevo_z)
    
    def rotar_y(self, angulo):
        """Rota el punto alrededor del eje Y"""
        rad = math.radians(angulo)
        nuevo_x = self.x * math.cos(rad) + self.z * math.sin(rad)
        nuevo_z = -self.x * math.sin(rad) + self.z * math.cos(rad)
        return Punto3D(nuevo_x, self.y, nuevo_z)
    
    def rotar_z(self, angulo):
        """Rota el punto alrededor del eje Z"""
        rad = math.radians(angulo)
        nuevo_x = self.x * math.cos(rad) - self.y * math.sin(rad)
        nuevo_y = self.x * math.sin(rad) + self.y * math.cos(rad)
        return Punto3D(nuevo_x, nuevo_y, self.z)

class Objeto3D:
    def __init__(self, vertices, aristas, color=BLANCO):
        self.vertices_originales = vertices
        self.vertices = [v.copiar() for v in vertices]
        self.aristas = aristas
        self.color = color
        self.posicion = Punto3D(0, 0, 0)
        self.escala = Punto3D(1, 1, 1)
        self.rotacion = Punto3D(0, 0, 0)  # Ángulos de rotación en X, Y, Z
    
    @staticmethod
    def crear_cubo(tamaño=100, color=BLANCO):
        """Crea un cubo centrado en el origen"""
        vertices = []
        for dx in [-tamaño, tamaño]:
            for dy in [-tamaño, tamaño]:
                for dz in [-tamaño, tamaño]:
                    vertices.append(Punto3D(dx, dy, dz))
        
        aristas = [
            (0, 1), (1, 3), (3, 2), (2, 0),  # Cara trasera
            (4, 5), (5, 7), (7, 6), (6, 4),  # Cara delantera
            (0, 4), (1, 5), (2, 6), (3, 7)   # Aristas laterales
        ]
        
        return Objeto3D(vertices, aristas, color)
    #metodo para crear esfera ---------------------------------------------------------------------
    @staticmethod
    def crear_esfera(radio=80, segmentos=20, color=BLANCO):
        """Crea una esfera 3D mediante puntos conectados por líneas"""
        vertices = []
        aristas = []
        
        # Generar vértices en coordenadas esféricas
        for i in range(segmentos + 1):
            theta = math.pi * i / segmentos  # Ángulo vertical (0 a π)
            for j in range(segmentos * 2 + 1):
                phi = 2 * math.pi * j / (segmentos * 2)  # Ángulo horizontal (0 a 2π)
                x = radio * math.sin(theta) * math.cos(phi)
                y = radio * math.sin(theta) * math.sin(phi)
                z = radio * math.cos(theta)
                vertices.append(Punto3D(x, y, z))
        
        # Conectar vértices adyacentes (malla tipo wireframe)
        for i in range(segmentos):
            for j in range(segmentos * 2):
                a = i * (segmentos * 2 + 1) + j
                b = a + 1
                c = a + (segmentos * 2 + 1)
                d = c + 1
                aristas += [(a, b), (a, c)]
        
        return Objeto3D(vertices, aristas, color)

    # ---------------------------------------------------------------------------- metodo para esfera
    
    @staticmethod
    def crear_ejes(longitud=150, grosor=5):
        """Crea ejes coordenados 3D"""
        vertices = []
        aristas = []
        
        # Eje X (Rojo)
        vertices.append(Punto3D(0, 0, 0))
        vertices.append(Punto3D(longitud, 0, 0))
        aristas.append((0, 1))
        
        # Eje Y (Verde)
        vertices.append(Punto3D(0, 0, 0))
        vertices.append(Punto3D(0, longitud, 0))
        aristas.append((2, 3))
        
        # Eje Z (Azul)
        vertices.append(Punto3D(0, 0, 0))
        vertices.append(Punto3D(0, 0, longitud))
        aristas.append((4, 5))
        
        return Objeto3D(vertices, aristas, BLANCO)
    
    def trasladar(self, dx, dy, dz):
        """Mueve el objeto en el espacio 3D"""
        self.posicion.x += dx
        self.posicion.y += dy
        self.posicion.z += dz
        self.actualizar_vertices()
    
    def escalar(self, sx, sy, sz):
        """Cambia el tamaño del objeto"""
        self.escala.x *= sx
        self.escala.y *= sy
        self.escala.z *= sz
        self.actualizar_vertices()
    
    def rotar(self, dx, dy, dz):
        """Rota el objeto alrededor de los ejes"""
        self.rotacion.x = (self.rotacion.x + dx) % 360
        self.rotacion.y = (self.rotacion.y + dy) % 360
        self.rotacion.z = (self.rotacion.z + dz) % 360
        self.actualizar_vertices()
    
    def establecer_rotacion(self, x, y, z):
        """Establece rotación absoluta"""
        self.rotacion.x = x % 360
        self.rotacion.y = y % 360
        self.rotacion.z = z % 360
        self.actualizar_vertices()
    
    def actualizar_vertices(self):
        """Aplica todas las transformaciones a los vértices"""
        for i, vertice_original in enumerate(self.vertices_originales):
            # Crear copia del vértice original
            vertice = vertice_original.copiar()
            
            # 1. Aplicar ESCALA
            vertice.x *= self.escala.x
            vertice.y *= self.escala.y
            vertice.z *= self.escala.z
            
            # 2. Aplicar ROTACIÓN (en orden Z, Y, X - convención común)
            if self.rotacion.z != 0:
                vertice = vertice.rotar_z(self.rotacion.z)
            if self.rotacion.y != 0:
                vertice = vertice.rotar_y(self.rotacion.y)
            if self.rotacion.x != 0:
                vertice = vertice.rotar_x(self.rotacion.x)
            
            # 3. Aplicar TRASLACIÓN
            vertice.x += self.posicion.x
            vertice.y += self.posicion.y
            vertice.z += self.posicion.z
            
            # Actualizar vértice transformado
            self.vertices[i] = vertice

# Crear escena con múltiples objetos
#objetos = [
#    Objeto3D.crear_cubo(80, ROJO),
#    Objeto3D.crear_cubo(60, VERDE),
#    Objeto3D.crear_cubo(70, AZUL),
#    Objeto3D.crear_cubo(50, AMARILLO),
#    Objeto3D.crear_ejes(200)  # Ejes coordenados
#]

# crear la escena de las esferas  ------------------------------------------------------

objetos = [
    Objeto3D.crear_esfera(60, 6, BLANCO),
    Objeto3D.crear_esfera(20, 6, VERDE),
    Objeto3D.crear_esfera(80, 6, AZUL),
    Objeto3D.crear_ejes(0)  # Ejes coordenados
]

# escena de las esferas ----------------------------------------------------------------

# Configurar posiciones y rotaciones iniciales  ---------------------------------
#objetos[0].trasladar(-180, 0, 0)     # Cubo rojo - izquierda
#objetos[1].trasladar(180, 0, 0)      # Cubo verde - derecha
#objetos[2].trasladar(0, -120, 0)     # Cubo azul - abajo
#objetos[3].trasladar(0, 120, 0)      # Cubo amarillo - arriba
#objetos[4].trasladar(0, 0, 0)        # Ejes en el centro
# ------------------------------------------------------------------------------------

# inicio posiciones esferas --------------------------------------------------------
# Configurar posiciones iniciales
objetos[0].trasladar(-180, 10, 0)   # Esfera blanco - izquierda
objetos[1].trasladar(-70, 100, 0)    # Esfera rojo - derecha
objetos[2].trasladar(0, 0, 0)      # Esfera azul - centro
objetos[3].trasladar(0, 0, 0)      # Ejes coordenados

#final posiciones esferas -----------------------------------------------------------


# Variables de control
distancia_vision = 500
objeto_seleccionado = 0
tiempo = 0
modo_rotacion = 1  # 1=Automática, 2=Manual, 3=Orbital, 4=Combinada
velocidad_rotacion = 1.0

#agregado para velicidad --------------------------------------------------
radio_orbita = 250  # distancia al centro (esfera azul)
velocidad_orbita = 1.0  # velocidad de giro
#final de lo de velocidad --------------------------------------------------


# Variables adicionales
balas = []  # Lista de disparos
velocidad_movimiento = 5.0  # Velocidad de desplazamiento de la esfera roja
velocidad_bala = 15.0  # Velocidad de las balas
vida_bala = 120  # duración en frames (~2 segundos)

# Bucle principal
ejecutando = True
while ejecutando:
    dt = reloj.tick(60) / 1000.0
    tiempo += dt

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            # Cámara
            if evento.key == pygame.K_UP:
                objetos[1].posicion.y -= velocidad_movimiento  # subir
                objetos[1].actualizar_vertices()
            elif evento.key == pygame.K_DOWN:
                objetos[1].posicion.y += velocidad_movimiento  # bajar
                objetos[1].actualizar_vertices()
            elif evento.key == pygame.K_LEFT:
                objetos[1].posicion.x -= velocidad_movimiento  # izquierda
                objetos[1].actualizar_vertices()
            elif evento.key == pygame.K_RIGHT:
                objetos[1].posicion.x += velocidad_movimiento  # derecha
                objetos[1].actualizar_vertices()

            # Disparo con espacio
            elif evento.key == pygame.K_SPACE:
                balas.append({
                    "x": objetos[1].posicion.x,
                    "y": objetos[1].posicion.y,
                    "z": objetos[1].posicion.z,
                    "vx": 0,
                    "vy": 0,
                    "vz": -velocidad_bala,  # dirección hacia adelante
                    "vida": vida_bala
                })

            # Resto de tus controles (rotación, modos, zoom, etc)
            elif evento.key == pygame.K_TAB:
                objeto_seleccionado = (objeto_seleccionado + 1) % (len(objetos) - 1)
            elif evento.key == pygame.K_q: objetos[objeto_seleccionado].rotar(5, 0, 0)
            elif evento.key == pygame.K_a: objetos[objeto_seleccionado].rotar(-5, 0, 0)
            elif evento.key == pygame.K_w: objetos[objeto_seleccionado].rotar(0, 5, 0)
            elif evento.key == pygame.K_s: objetos[objeto_seleccionado].rotar(0, -5, 0)
            elif evento.key == pygame.K_e: objetos[objeto_seleccionado].rotar(0, 0, 5)
            elif evento.key == pygame.K_d: objetos[objeto_seleccionado].rotar(0, 0, -5)
            elif evento.key == pygame.K_1: modo_rotacion = 1
            elif evento.key == pygame.K_2: modo_rotacion = 2
            elif evento.key == pygame.K_3: modo_rotacion = 3
            elif evento.key == pygame.K_4: modo_rotacion = 4
            elif evento.key == pygame.K_PLUS or evento.key == pygame.K_EQUALS:
                velocidad_rotacion = min(3.0, velocidad_rotacion + 0.1)
            elif evento.key == pygame.K_MINUS:
                velocidad_rotacion = max(0.1, velocidad_rotacion - 0.1)
            elif evento.key == pygame.K_r:
                objetos[objeto_seleccionado].establecer_rotacion(0, 0, 0)

    # Animaciones existentes (rotación/orbital)
    if modo_rotacion != 2:
        for i, objeto in enumerate(objetos):
            if i >= len(objetos) - 1: continue
            if modo_rotacion == 1:
                if i == 2:
                    objeto.rotar(0, 0, 30 * dt * velocidad_rotacion)

    
    

    # --- MOVIMIENTO ORBITAL DE ESFERAS ROJA Y BLANCA --- --------------
    angulo_orbita = tiempo * 50 * velocidad_orbita  # velocidad de giro (ajústala a gusto)

    # Esfera roja orbitando en sentido horario
    objetos[0].posicion.x = math.cos(math.radians(angulo_orbita)) * radio_orbita
    objetos[0].posicion.z = math.sin(math.radians(angulo_orbita)) * radio_orbita
    objetos[0].posicion.y = 0  # mantener en el plano XZ
    objetos[0].actualizar_vertices()

    # Esfera blanca orbitando en sentido contrario
    

    # --- MOVIMIENTO ORBITAL DE ESFERAS ROJA Y BLANCA --------------

    # Actualizar balas
    nuevas_balas = []
    for bala in balas:
        bala["x"] += bala["vx"]
        bala["y"] += bala["vy"]
        bala["z"] += bala["vz"]
        bala["vida"] -= 1
        if bala["vida"] > 0:
            nuevas_balas.append(bala)
    balas = nuevas_balas

    # Dibujar escena
    ventana.fill(NEGRO)
    for i, objeto in enumerate(objetos):
        if i == len(objetos) - 1:
            for j, arista in enumerate(objeto.aristas):
                p1_2d = objeto.vertices[arista[0]].proyectar(distancia_vision)
                p2_2d = objeto.vertices[arista[1]].proyectar(distancia_vision)
                color_eje = [ROJO, VERDE, AZUL][j]
                pygame.draw.line(ventana, color_eje, p1_2d, p2_2d, 3)
        else:
            for arista in objeto.aristas:
                p1_2d = objeto.vertices[arista[0]].proyectar(distancia_vision)
                p2_2d = objeto.vertices[arista[1]].proyectar(distancia_vision)
                pygame.draw.line(ventana, objeto.color, p1_2d, p2_2d, 2)

    # Dibujar balas
    for bala in balas:
        p1 = Punto3D(bala["x"], bala["y"], bala["z"]).proyectar(distancia_vision)
        p2 = Punto3D(bala["x"], bala["y"], bala["z"] + 10).proyectar(distancia_vision)
        pygame.draw.line(ventana, AMARILLO, p1, p2, 3)

        # --- INFORMACIÓN EN PANTALLA ---
    fuente = pygame.font.SysFont('Arial', 18)
    
    info_textos = [
        f"Balas activas: {len(balas)}",
        "",
        "CONTROLES:",
        "↑ ↓ ← →  →  Mover nave",
        "ESPACIO  →  Disparar"
    ]
    
    for i, texto in enumerate(info_textos):
        render = fuente.render(texto, True, BLANCO)
        ventana.blit(render, (20, 20 + i * 22))


    pygame.display.flip()

pygame.quit()
