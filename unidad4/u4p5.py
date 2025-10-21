#Gerardo Mercado Hurtado
#Raúl Martínez Martínez
#Importar Librerias necesarias
import pygame
import numpy as np
import math
import sys

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clase 6: Sombreado Gouraud - Algoritmo Detallado")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (150, 150, 150)

class Vector3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def normalize(self):
        length = self.length()
        if length > 0:
            return Vector3D(self.x/length, self.y/length, self.z/length)
        return Vector3D(0, 0, 0)
    
    def reflect(self, normal):
        dot_product = self.dot(normal)
        return Vector3D(
            self.x - 2 * dot_product * normal.x,
            self.y - 2 * dot_product * normal.y,
            self.z - 2 * dot_product * normal.z
        )
    
    def __add__(self, other):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __mul__(self, scalar):
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __str__(self):
        return f"({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"

class Material:
    def __init__(self, Ka, Kd, Ks, shininess):
        self.K_ambient = Ka
        self.K_diffuse = Kd
        self.K_specular = Ks
        self.shininess = shininess

class LightSource:
    def __init__(self, position, Ia, Id, Is):
        self.position = position
        self.I_ambient = Ia
        self.I_diffuse = Id
        self.I_specular = Is

class Vertex:
    def __init__(self, position, normal=None, color=None):
        self.position = position  # (x, y, z)
        self.normal = normal      # Vector3D
        self.color = color        # (r, g, b)
    
    def calculate_illumination(self, light, material, viewer_pos):
        """Calcular iluminación en este vértice usando modelo de Phong"""
        if self.normal is None:
            return (128, 128, 128)  # Gris por defecto
        
        N = self.normal.normalize()
        
        # Vector hacia la luz
        L = Vector3D(
            light.position[0] - self.position[0],
            light.position[1] - self.position[1],
            light.position[2] - self.position[2]
        ).normalize()
        
        # Vector hacia el observador
        V = Vector3D(
            viewer_pos[0] - self.position[0],
            viewer_pos[1] - self.position[1],
            viewer_pos[2] - self.position[2]
        ).normalize()
        
        # Vector de reflexión
        R = L.reflect(N)
        
        # Componente ambiental
        ambient_r = material.K_ambient[0] * light.I_ambient[0]
        ambient_g = material.K_ambient[1] * light.I_ambient[1]
        ambient_b = material.K_ambient[2] * light.I_ambient[2]
        
        # Componente difusa
        L_dot_N = max(0, L.dot(N))
        diffuse_r = material.K_diffuse[0] * L_dot_N * light.I_diffuse[0]
        diffuse_g = material.K_diffuse[1] * L_dot_N * light.I_diffuse[1]
        diffuse_b = material.K_diffuse[2] * L_dot_N * light.I_diffuse[2]
        
        # Componente especular
        R_dot_V = max(0, R.dot(V))
        specular_intensity = R_dot_V ** material.shininess
        specular_r = material.K_specular[0] * specular_intensity * light.I_specular[0]
        specular_g = material.K_specular[1] * specular_intensity * light.I_specular[1]
        specular_b = material.K_specular[2] * specular_intensity * light.I_specular[2]
        
        # Combinar componentes
        final_r = min(1, ambient_r + diffuse_r + specular_r)
        final_g = min(1, ambient_g + diffuse_g + specular_g)
        final_b = min(1, ambient_b + diffuse_b + specular_b)
        
        return (
            int(final_r * 255),
            int(final_g * 255),
            int(final_b * 255)
        )

class Triangle:
    def __init__(self, v1, v2, v3, material):
        self.vertices = [v1, v2, v3]  # Lista de objetos Vertex
        self.material = material
        self.face_normal = self.calculate_face_normal()
    
    def calculate_face_normal(self):
        """Calcular normal de la cara"""
        v1 = np.array(self.vertices[0].position)
        v2 = np.array(self.vertices[1].position)
        v3 = np.array(self.vertices[2].position)
        
        edge1 = v2 - v1
        edge2 = v3 - v1
        
        normal = np.cross(edge1, edge2)
        normal_length = np.linalg.norm(normal)
        
        if normal_length > 0:
            normal = normal / normal_length
        else:
            normal = np.array([0, 0, 1])
        
        return Vector3D(normal[0], normal[1], normal[2])

class GouraudRenderer:
    def __init__(self):
        self.show_step_by_step = False
        self.current_step = 0  # 0: Normales, 1: Iluminación, 2: Interpolación
        self.show_wireframe = True
        self.show_vertex_normals = True
    
    def calculate_vertex_normals(self, mesh):
        """PASO 1: Calcular normales suaves por vértice"""
        # Para cada vértice, promediar las normales de las caras adyacentes
        vertex_to_triangles = {}
        
        # Mapear cada vértice a sus triángulos
        for i, triangle in enumerate(mesh):
            for vertex in triangle.vertices:
                pos_key = tuple(vertex.position)
                if pos_key not in vertex_to_triangles:
                    vertex_to_triangles[pos_key] = []
                vertex_to_triangles[pos_key].append(triangle)
        
        # Calcular normal promedio para cada vértice
        for triangle in mesh:
            for vertex in triangle.vertices:
                pos_key = tuple(vertex.position)
                adjacent_triangles = vertex_to_triangles[pos_key]
                
                # Promediar normales de caras adyacentes
                avg_normal = Vector3D(0, 0, 0)
                for adj_triangle in adjacent_triangles:
                    avg_normal = avg_normal + adj_triangle.face_normal
                
                # Normalizar
                if avg_normal.length() > 0:
                    vertex.normal = avg_normal.normalize()
                else:
                    vertex.normal = Vector3D(0, 0, 1)
        
        return mesh
    
    def calculate_vertex_colors(self, mesh, light, viewer_pos):
        """PASO 2: Calcular colores en cada vértice"""
        for triangle in mesh:
            for vertex in triangle.vertices:
                vertex.color = vertex.calculate_illumination(light, triangle.material, viewer_pos)
        
        return mesh
    
    def interpolate_color_along_edge(self, color1, color2, t):
        """Interpolar entre dos colores"""
        r = int(color1[0] * (1 - t) + color2[0] * t)
        g = int(color1[1] * (1 - t) + color2[1] * t)
        b = int(color1[2] * (1 - t) + color2[2] * t)
        return (r, g, b)
    
    def draw_triangle_gouraud(self, surface, triangle):
        """PASO 3: Dibujar triángulo con interpolación Gouraud"""
        # Ordenar vértices por Y
        vertices_sorted = sorted(triangle.vertices, key=lambda v: v.position[1])
        v1, v2, v3 = vertices_sorted
        
        # Convertir a 2D para dibujo
        points_2d = [(v.position[0], v.position[1]) for v in triangle.vertices]
        
        # Crear superficie para interpolación
        tri_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        tri_surface.fill((0, 0, 0, 0))
        
        # Scanline rendering simplificado
        y_min = int(min(v.position[1] for v in triangle.vertices))
        y_max = int(max(v.position[1] for v in triangle.vertices))
        
        for y in range(y_min, y_max + 1):
            intersections = []
            
            # Encontrar intersecciones con cada arista
            for i in range(3):
                v_start = triangle.vertices[i]
                v_end = triangle.vertices[(i + 1) % 3]
                
                y1, y2 = v_start.position[1], v_end.position[1]
                if (y1 <= y <= y2) or (y2 <= y <= y1):
                    if y1 != y2:
                        t = (y - y1) / (y2 - y1)
                        x = v_start.position[0] + (v_end.position[0] - v_start.position[0]) * t
                        # Interpolar color
                        color = self.interpolate_color_along_edge(v_start.color, v_end.color, t)
                        intersections.append((x, color))
            
            # Ordenar intersecciones y dibujar línea
            if len(intersections) >= 2:
                intersections.sort(key=lambda x: x[0])
                x_start, color_start = intersections[0]
                x_end, color_end = intersections[1]
                
                # Interpolar entre colores de las intersecciones
                for x in range(int(x_start), int(x_end) + 1):
                    if len(intersections[0]) > 1 and len(intersections[1]) > 1:
                        t_line = (x - x_start) / (x_end - x_start) if x_end != x_start else 0
                        final_color = self.interpolate_color_along_edge(color_start, color_end, t_line)
                        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                            tri_surface.set_at((x, y), final_color)
        
        # Aplicar superficie a la pantalla
        surface.blit(tri_surface, (0, 0))
        
        # Dibujar wireframe si está activado
        if self.show_wireframe:
            pygame.draw.polygon(surface, BLACK, points_2d, 1)
    
    def draw_vertex_info(self, surface, triangle):
        """Dibujar información de vértices (normales, colores)"""
        for i, vertex in enumerate(triangle.vertices):
            x, y = int(vertex.position[0]), int(vertex.position[1])
            
            # Dibujar punto del vértice
            pygame.draw.circle(surface, RED, (x, y), 6)
            
            # Dibujar normal si está activado
            if self.show_vertex_normals and vertex.normal:
                end_x = x + vertex.normal.x * 30
                end_y = y + vertex.normal.y * 30
                pygame.draw.line(surface, GREEN, (x, y), (end_x, end_y), 2)
            
            # Mostrar color del vértice
            color_rect = pygame.Rect(x + 15, y - 8, 20, 20)
            pygame.draw.rect(surface, vertex.color, color_rect)
            pygame.draw.rect(surface, BLACK, color_rect, 1)

def create_house_mesh(center, size):
    """Crear una casita simple con paredes, techo y puerta rojos"""
    x, y, z = center
    s = size

    # Material rojo (para todo)
    material_red = Material(
        Ka=(0.2, 0.0, 0.0),
        Kd=(0.8, 0.1, 0.1),
        Ks=(0.5, 0.5, 0.5),
        shininess=20
    )

    # Vértices de la casita
    vertices = {
        "A": Vertex((x - s, y + s, z - s)),  # Izquierda inferior frente
        "B": Vertex((x + s, y + s, z - s)),  # Derecha inferior frente
        "C": Vertex((x + s, y - s, z - s)),  # Derecha superior frente
        "D": Vertex((x - s, y - s, z - s)),  # Izquierda superior frente

        "E": Vertex((x - s, y + s, z + s)),  # Izquierda inferior atrás
        "F": Vertex((x + s, y + s, z + s)),  # Derecha inferior atrás
        "G": Vertex((x + s, y - s, z + s)),  # Derecha superior atrás
        "H": Vertex((x - s, y - s, z + s)),  # Izquierda superior atrás

        # Picos del techo
        "T1": Vertex((x, y - s * 1.5, z - s)),  # Pico frontal
        "T2": Vertex((x, y - s * 1.5, z + s)),  # Pico trasero
    }

    # Triángulos de paredes y techo
    triangles = [
        # Frente
        Triangle(vertices["A"], vertices["B"], vertices["C"], material_red),
        Triangle(vertices["A"], vertices["C"], vertices["D"], material_red),

        # Atrás
        Triangle(vertices["E"], vertices["F"], vertices["G"], material_red),
        Triangle(vertices["E"], vertices["G"], vertices["H"], material_red),

        # Laterales
        Triangle(vertices["B"], vertices["F"], vertices["G"], material_red),
        Triangle(vertices["B"], vertices["G"], vertices["C"], material_red),
        Triangle(vertices["A"], vertices["E"], vertices["H"], material_red),
        Triangle(vertices["A"], vertices["H"], vertices["D"], material_red),

        # Techo
        Triangle(vertices["D"], vertices["C"], vertices["T1"], material_red),
        Triangle(vertices["H"], vertices["G"], vertices["T2"], material_red),
        Triangle(vertices["D"], vertices["H"], vertices["T1"], material_red),
        Triangle(vertices["H"], vertices["T1"], vertices["T2"], material_red),
        Triangle(vertices["C"], vertices["G"], vertices["T1"], material_red),
        Triangle(vertices["G"], vertices["T2"], vertices["T1"], material_red),
    ]

    # Puerta (también roja)
    door_bottom_left = Vertex((x - s * 0.3, y + s, z - s - 0.01))
    door_bottom_right = Vertex((x + s * 0.1, y + s, z - s - 0.01))
    door_top_left = Vertex((x - s * 0.3, y + s * 0.4, z - s - 0.01))
    door_top_right = Vertex((x + s * 0.1, y + s * 0.4, z - s - 0.01))

    triangles += [
        Triangle(door_bottom_left, door_bottom_right, door_top_right, material_red),
        Triangle(door_bottom_left, door_top_right, door_top_left, material_red)
    ]

    return triangles


def main():
    renderer = GouraudRenderer()
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)
    small_font = pygame.font.Font(None, 22)
    
    # Configurar luz
    light = LightSource(
        position=(400, 200, 100),
        Ia=(0.2, 0.2, 0.2),
        Id=(0.8, 0.8, 0.8),
        Is=(1.0, 1.0, 1.0)
    )
    
    viewer_pos = (WIDTH // 2, HEIGHT // 2, 300)
    
    # Crear malla de casita
    pyramid_mesh = create_house_mesh((500, 400, 0), 60)

    
    # Aplicar algoritmo Gouraud paso a paso
    pyramid_mesh = renderer.calculate_vertex_normals(pyramid_mesh)  # Paso 1
    pyramid_mesh = renderer.calculate_vertex_colors(pyramid_mesh, light, viewer_pos)  # Paso 2
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    renderer.show_vertex_normals = not renderer.show_vertex_normals
                elif event.key == pygame.K_w:
                    renderer.show_wireframe = not renderer.show_wireframe
                elif event.key == pygame.K_s:
                    renderer.show_step_by_step = not renderer.show_step_by_step
                    if renderer.show_step_by_step:
                        renderer.current_step = 0
                elif event.key == pygame.K_SPACE and renderer.show_step_by_step:
                    renderer.current_step = (renderer.current_step + 1) % 3
                elif event.key == pygame.K_LEFT:
                    light.position = (light.position[0] - 20, light.position[1], light.position[2])
                    # Recalcular colores cuando se mueve la luz
                    pyramid_mesh = renderer.calculate_vertex_colors(pyramid_mesh, light, viewer_pos)
                elif event.key == pygame.K_RIGHT:
                    light.position = (light.position[0] + 20, light.position[1], light.position[2])
                    pyramid_mesh = renderer.calculate_vertex_colors(pyramid_mesh, light, viewer_pos)
                elif event.key == pygame.K_UP:
                    light.position = (light.position[0], light.position[1] - 20, light.position[2])
                    pyramid_mesh = renderer.calculate_vertex_colors(pyramid_mesh, light, viewer_pos)
                elif event.key == pygame.K_DOWN:
                    light.position = (light.position[0], light.position[1] + 20, light.position[2])
                    pyramid_mesh = renderer.calculate_vertex_colors(pyramid_mesh, light, viewer_pos)
        
        screen.fill(WHITE)
        
        # Dibujar título
        title = font.render("CLASE 6: SOMBRADO GOURAUD - ALGORITMO POR VÉRTICE", True, BLUE)
        screen.blit(title, (WIDTH // 2 - 250, 20))
        
        # Dibujar pirámide con Gouraud shading
        for triangle in pyramid_mesh:
            renderer.draw_triangle_gouraud(screen, triangle)
            if renderer.show_vertex_normals:
                renderer.draw_vertex_info(screen, triangle)
        
        # Dibujar información del algoritmo
        algorithm_steps = [
            "PASOS DEL ALGORITMO GOURAUD:",
            "1. Calcular normales por vértice",
            "2. Aplicar iluminación en vértices", 
            "3. Interpolar colores en el polígono"
        ]
        
        for i, step in enumerate(algorithm_steps):
            color = BLUE if i == 0 else GREEN if i == renderer.current_step + 1 else BLACK
            text = font.render(step, True, color) if i == 0 else small_font.render(step, True, color)
            screen.blit(text, (50, 100 + i * 25))
        
        # Dibujar información de vértices
        vertex_info = [
            "INFORMACIÓN DE VÉRTICES:",
            "● Puntos ROJOS: Posición de vértices",
            "● Líneas VERDES: Normales de vértices", 
            "□ Cuadrados: Color calculado en vértice"
        ]
        
        for i, info in enumerate(vertex_info):
            color = BLUE if i == 0 else BLACK
            text = small_font.render(info, True, color)
            screen.blit(text, (50, 220 + i * 20))
        
        # Dibujar controles
        controls = [
            "CONTROLES:",
            "N: Alternar visualización de normales",
            "W: Alternar wireframe",
            "S: Modo paso a paso",
            "ESPACIO: Siguiente paso (en modo paso a paso)",
            "FLECHAS: Mover fuente de luz"
        ]
        
        for i, control in enumerate(controls):
            color = BLUE if i == 0 else BLACK
            text = small_font.render(control, True, color)
            screen.blit(text, (WIDTH - 300, 100 + i * 20))
        
        # Dibujar posición de la luz
        pygame.draw.circle(screen, YELLOW, (int(light.position[0]), int(light.position[1])), 30)
        pygame.draw.circle(screen, YELLOW, (int(light.position[0]), int(light.position[1])), 10, 2)
        light_text = small_font.render(f"Sol: ({light.position[0]}, {light.position[1]})", True, BLACK)
        screen.blit(light_text, (light.position[0] + 15, light.position[1] - 10))
        
        # Información adicional
        if renderer.show_step_by_step:
            step_names = ["Cálculo de Normales", "Iluminación en Vértices", "Interpolación de Colores"]
            current_step_text = font.render(f"PASO ACTUAL: {step_names[renderer.current_step]}", True, RED)
            screen.blit(current_step_text, (WIDTH // 2 - 150, HEIGHT - 50))
        
        # Ventajas y desventajas
        pros_cons = [
            "VENTAJAS DE GOURAUD:",
            "• Apariencia suave",
            "• Buen rendimiento",
            "• Adecuado para tiempo real",
            "",
            "LIMITACIONES:",
            "• Pérdida de highlights especulares",
            "• Artefactos en esquinas afiladas",
            "• Depende de la densidad de la malla"
        ]
        
        for i, text in enumerate(pros_cons):
            color = GREEN if i == 0 else RED if i == 5 else BLACK
            text_surface = small_font.render(text, True, color)
            screen.blit(text_surface, (WIDTH - 350, 300 + i * 20))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

