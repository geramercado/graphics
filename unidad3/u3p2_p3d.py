#importar bibliotecas
import pygame
import math

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Clase 2: Formas Geométricas 3D - Cubos y Pirámides")
reloj = pygame.time.Clock()

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 100, 255)
AMARILLO = (255, 255, 0)
MORADO = (255, 0, 255)

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

class Objeto3D:
    """Clase para representar objetos 3D con vértices y aristas"""
    def __init__(self, vertices, aristas, color=BLANCO):
        self.vertices = vertices  # Lista de Punto3D
        self.aristas = aristas    # Lista de tuplas (índice1, índice2)
        self.color = color
    
    @staticmethod
    def crear_cubo(tamaño=100, x=0, y=0, z=0, color=BLANCO):
        """Crea un cubo centrado en (x, y, z)"""
        vertices = []
        # Crear los 8 vértices del cubo
        for dx in [-tamaño, tamaño]:
            for dy in [-tamaño, tamaño]:
                for dz in [-tamaño, tamaño]:
                    vertices.append(Punto3D(x + dx, y + dy, z + dz))
        
        # Definir las 12 aristas del cubo
        aristas = [
            (0, 1), (1, 3), (3, 2), (2, 0),  # Cara trasera
            (4, 5), (5, 7), (7, 6), (6, 4),  # Cara delantera
            (0, 4), (1, 5), (2, 6), (3, 7)   # Aristas laterales
        ]
        
        return Objeto3D(vertices, aristas, color)
    
    @staticmethod
    def crear_piramide(tamaño_base=100, altura=150, x=0, y=0, z=0, color=VERDE):
        """Crea una pirámide de base cuadrada"""
        vertices = [
            # Base cuadrada
            Punto3D(x - tamaño_base, y - tamaño_base, z - tamaño_base),  # 0: esquina atrás-izquierda
            Punto3D(x + tamaño_base, y - tamaño_base, z - tamaño_base),  # 1: esquina atrás-derecha
            Punto3D(x + tamaño_base, y - tamaño_base, z + tamaño_base),  # 2: esquina adelante-derecha
            Punto3D(x - tamaño_base, y - tamaño_base, z + tamaño_base),  # 3: esquina adelante-izquierda
            # Vértice superior
            Punto3D(x, y - altura, z)  # 4: punta de la pirámide
        ]
        
        # Definir las 8 aristas de la pirámide
        aristas = [
            # Base
            (0, 1), (1, 2), (2, 3), (3, 0),
            # Lados
            (0, 4), (1, 4), (2, 4), (3, 4)
        ]
        
        return Objeto3D(vertices, aristas, color)
    
    @staticmethod
    def crear_plano(tamaño=200, divisiones=4, x=0, y=0, z=0, color=AZUL):
        """Crea un plano cuadriculado"""
        vertices = []
        aristas = []
        
        # Crear vértices en grid
        for i in range(divisiones + 1):
            for j in range(divisiones + 1):
                px = x - tamaño/2 + (tamaño / divisiones) * i
                pz = z - tamaño/2 + (tamaño / divisiones) * j
                vertices.append(Punto3D(px, y, pz))
        
        # Crear aristas horizontales
        for i in range(divisiones + 1):
            for j in range(divisiones):
                idx = i * (divisiones + 1) + j
                aristas.append((idx, idx + 1))
        
        # Crear aristas verticales
        for i in range(divisiones):
            for j in range(divisiones + 1):
                idx = i * (divisiones + 1) + j
                aristas.append((idx, idx + divisiones + 1))
        
        return Objeto3D(vertices, aristas, color)

# Crear escena con múltiples objetos
objetos = [
    Objeto3D.crear_cubo(80, x=-150, y=0, z=0, color=ROJO),
    Objeto3D.crear_piramide(70, 120, x=150, y=50, z=100, color=VERDE),
    Objeto3D.crear_plano(300, 8, x=0, y=100, z=0, color=AZUL),
    Objeto3D.crear_cubo(40, x=0, y=-80, z=150, color=AMARILLO),
]

# Variables de control
distancia_vision = 500
mostrar_ejes = True
angulo_rotacion = 0
objeto_seleccionado = 0  # Índice del objeto actual

# Bucle principal
ejecutando = True
while ejecutando:
    # Control de tiempo
    dt = reloj.tick(60) / 1000.0
    angulo_rotacion += dt * 30  # Rotación automática
    
    # --- MANEJO DE EVENTOS ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            # Controles de cámara
            if evento.key == pygame.K_UP:
                distancia_vision = max(100, distancia_vision - 50)
            elif evento.key == pygame.K_DOWN:
                distancia_vision = min(1000, distancia_vision + 50)
            # Mostrar/ocultar ejes
            elif evento.key == pygame.K_e:
                mostrar_ejes = not mostrar_ejes
            # Cambiar objeto seleccionado
            elif evento.key == pygame.K_TAB:
                objeto_seleccionado = (objeto_seleccionado + 1) % len(objetos)
            # Rotación manual
            elif evento.key == pygame.K_LEFT:
                angulo_rotacion -= 10
            elif evento.key == pygame.K_RIGHT:
                angulo_rotacion += 10
    
    # --- DIBUJADO ---
    ventana.fill(NEGRO)
    
    # Dibujar ejes coordenados
    if mostrar_ejes:
        origen = Punto3D(0, 0, 0)
        ox, oy = origen.proyectar(distancia_vision)
        
        # Eje X (Rojo)
        fin_x = Punto3D(200, 0, 0)
        fx, fy = fin_x.proyectar(distancia_vision)
        pygame.draw.line(ventana, ROJO, (ox, oy), (fx, fy), 2)
        
        # Eje Y (Verde)
        fin_y = Punto3D(0, 200, 0)
        fx, fy = fin_y.proyectar(distancia_vision)
        pygame.draw.line(ventana, VERDE, (ox, oy), (fx, fy), 2)
        
        # Eje Z (Azul)
        fin_z = Punto3D(0, 0, 200)
        fx, fy = fin_z.proyectar(distancia_vision)
        pygame.draw.line(ventana, AZUL, (ox, oy), (fx, fy), 2)
    
    # Dibujar todos los objetos
    for i, objeto in enumerate(objetos):
        color_objeto = objeto.color
        
        # Resaltar objeto seleccionado
        if i == objeto_seleccionado:
            color_objeto = MORADO  # Color especial para seleccionado
        
        # Dibujar aristas del objeto
        for arista in objeto.aristas:
            punto1 = objeto.vertices[arista[0]]
            punto2 = objeto.vertices[arista[1]]
            
            # Aplicar rotación simple en Y a todos los vértices
            if i == objeto_seleccionado:  # Solo rotar el objeto seleccionado
                angulo_rad = math.radians(angulo_rotacion)
                
                # Rotar punto1
                x1_rot = punto1.x * math.cos(angulo_rad) - punto1.z * math.sin(angulo_rad)
                z1_rot = punto1.x * math.sin(angulo_rad) + punto1.z * math.cos(angulo_rad)
                
                # Rotar punto2
                x2_rot = punto2.x * math.cos(angulo_rad) - punto2.z * math.sin(angulo_rad)
                z2_rot = punto2.x * math.sin(angulo_rad) + punto2.z * math.cos(angulo_rad)
                
                # Crear puntos rotados temporalmente
                p1_rot = Punto3D(x1_rot, punto1.y, z1_rot)
                p2_rot = Punto3D(x2_rot, punto2.y, z2_rot)
                
                # Proyectar puntos rotados
                p1_2d = p1_rot.proyectar(distancia_vision)
                p2_2d = p2_rot.proyectar(distancia_vision)
            else:
                # Proyectar puntos sin rotación
                p1_2d = punto1.proyectar(distancia_vision)
                p2_2d = punto2.proyectar(distancia_vision)
            
            # Dibujar la arista
            pygame.draw.line(ventana, color_objeto, p1_2d, p2_2d, 2)
        
        # Dibujar vértices como puntos pequeños
        for vertice in objeto.vertices:
            x2d, y2d = vertice.proyectar(distancia_vision)
            pygame.draw.circle(ventana, BLANCO, (x2d, y2d), 2)
    
    # --- INFORMACIÓN EN PANTALLA ---
    fuente = pygame.font.SysFont('Arial', 20)
    info_textos = [
        f"Objeto {objeto_seleccionado + 1}/{len(objetos)}",
        f"Distancia: {distancia_vision}",
        f"Rotación: {angulo_rotacion:.1f}°",
        "Controles: ↑↓=Zoom, TAB=Cambiar objeto",
        "←→=Rotar, E=Ejes"
    ]
    
    for i, texto in enumerate(info_textos):
        render = fuente.render(texto, True, BLANCO)
        ventana.blit(render, (10, 10 + i * 25))
    
    # --- ACTUALIZAR PANTALLA ---
    pygame.display.flip()

# Finalizar
pygame.quit()