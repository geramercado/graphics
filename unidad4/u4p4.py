#Gerardo Mercado Hurtado
#Raúl Martínez Martínez
#Importar bibliotecas
import pygame
import numpy as np
import math
import sys

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clase 4: Técnicas de Sombreado - Flat vs. Gouraud vs. Phong")

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

class Triangle:
    def __init__(self, v1, v2, v3, material):
        self.vertices = [v1, v2, v3]  # Cada vértice es (x, y, z)
        self.material = material
        self.vertex_normals = [None, None, None]  # Normales por vértice
        self.face_normal = None  # Normal de la cara
        self.calculate_face_normal()
    
    def calculate_face_normal(self):
        """Calcular la normal de la cara (flat shading)"""
        v1 = np.array(self.vertices[0])
        v2 = np.array(self.vertices[1])
        v3 = np.array(self.vertices[2])
        
        # Vectores de aristas
        edge1 = v2 - v1
        edge2 = v3 - v1
        
        # Producto cruz para obtener normal
        normal = np.cross(edge1, edge2)
        normal_length = np.linalg.norm(normal)
        
        if normal_length > 0:
            normal = normal / normal_length
        else:
            normal = np.array([0, 0, 1])
        
        self.face_normal = Vector3D(normal[0], normal[1], normal[2])
    
    def calculate_vertex_normals(self, mesh_normals):
        """Calcular/establecer normales por vértice (para Gouraud)"""
        self.vertex_normals = mesh_normals

class ShadingTechniques:
    def __init__(self):
        self.current_shading = "flat"  # "flat", "gouraud", "phong"
    
    def phong_illumination(self, point, normal, light, material, viewer_pos):
        """Calcular iluminación en un punto usando modelo de Phong"""
        N = normal.normalize()
        
        # Vector hacia la luz
        L = Vector3D(
            light.position[0] - point[0],
            light.position[1] - point[1],
            light.position[2] - point[2]
        ).normalize()
        
        # Vector hacia el observador
        V = Vector3D(
            viewer_pos[0] - point[0],
            viewer_pos[1] - point[1],
            viewer_pos[2] - point[2]
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
    
    def flat_shading(self, triangle, light, viewer_pos):
        """Sombreado FLAT: calcular iluminación una vez por triángulo"""
        # Usar el centro del triángulo para el cálculo
        center = self.get_triangle_center(triangle)
        color = self.phong_illumination(center, triangle.face_normal, light, triangle.material, viewer_pos)
        return color
    
    def gouraud_shading(self, triangle, light, viewer_pos):
        """Sombreado GOURAUD: calcular iluminación en vértices y interpolar"""
        if None in triangle.vertex_normals:
            # Si no hay normales por vértice, usar flat shading como fallback
            return self.flat_shading(triangle, light, viewer_pos)
        
        # Calcular color en cada vértice
        vertex_colors = []
        for i in range(3):
            color = self.phong_illumination(
                triangle.vertices[i], 
                triangle.vertex_normals[i], 
                light, 
                triangle.material, 
                viewer_pos
            )
            vertex_colors.append(color)
        
        return vertex_colors
    
    def get_triangle_center(self, triangle):
        """Obtener el centro de un triángulo"""
        x = sum(v[0] for v in triangle.vertices) / 3
        y = sum(v[1] for v in triangle.vertices) / 3
        z = sum(v[2] for v in triangle.vertices) / 3
        return (x, y, z)

def create_sphere_mesh(center, radius, rings=12, sectors=24):
    """Crear una esfera más detallada con triángulos"""
    mesh_triangles = []
    material = Material(
        Ka=(0.1, 0.1, 0.1),
        Kd=(0.7, 0.7, 0.7),
        Ks=(0.3, 0.3, 0.3),
        shininess=20
    )

    for r in range(rings):
        for s in range(sectors):
            theta1 = math.pi * r / rings
            theta2 = math.pi * (r + 1) / rings
            phi1 = 2 * math.pi * s / sectors
            phi2 = 2 * math.pi * (s + 1) / sectors

            # Coordenadas de 4 puntos en la "rejilla"
            v1 = (
                center[0] + radius * math.sin(theta1) * math.cos(phi1),
                center[1] + radius * math.cos(theta1),
                center[2] + radius * math.sin(theta1) * math.sin(phi1)
            )
            v2 = (
                center[0] + radius * math.sin(theta2) * math.cos(phi1),
                center[1] + radius * math.cos(theta2),
                center[2] + radius * math.sin(theta2) * math.sin(phi1)
            )
            v3 = (
                center[0] + radius * math.sin(theta2) * math.cos(phi2),
                center[1] + radius * math.cos(theta2),
                center[2] + radius * math.sin(theta2) * math.sin(phi2)
            )
            v4 = (
                center[0] + radius * math.sin(theta1) * math.cos(phi2),
                center[1] + radius * math.cos(theta1),
                center[2] + radius * math.sin(theta1) * math.sin(phi2)
            )

            # Dos triángulos por cuadrilátero
            mesh_triangles.append(Triangle(v1, v2, v3, material))
            mesh_triangles.append(Triangle(v1, v3, v4, material))

    return mesh_triangles


def calculate_vertex_normals(mesh):
    """Calcular normales suaves por vértice para Gouraud shading"""
    # Para una malla simple, usar la normal de la esfera en cada vértice
    for triangle in mesh:
        vertex_normals = []
        for vertex in triangle.vertices:
            # Normal de esfera: vector desde centro a vértice
            center = (400, 300, 0)  # Centro de nuestra esfera
            normal = Vector3D(
                vertex[0] - center[0],
                vertex[1] - center[1], 
                vertex[2] - center[2]
            ).normalize()
            vertex_normals.append(normal)
        triangle.calculate_vertex_normals(vertex_normals)
    
    return mesh

def draw_triangle_flat(surface, triangle, color):
    """Dibujar triángulo con color uniforme (Flat Shading)"""
    points_2d = [(v[0], v[1]) for v in triangle.vertices]
    pygame.draw.polygon(surface, color, points_2d)
    pygame.draw.polygon(surface, BLACK, points_2d, 1)  # Contorno

def draw_triangle_gouraud(surface, triangle, vertex_colors):
    """Dibujar triángulo con interpolación de color (Gouraud Shading)"""
    # Para simplificar, usaremos un promedio de los colores de vértice
    avg_color = (
        sum(c[0] for c in vertex_colors) // 3,
        sum(c[1] for c in vertex_colors) // 3,
        sum(c[2] for c in vertex_colors) // 3
    )
    
    points_2d = [(v[0], v[1]) for v in triangle.vertices]
    pygame.draw.polygon(surface, avg_color, points_2d)
    pygame.draw.polygon(surface, BLACK, points_2d, 1)

def draw_mesh(surface, mesh, light, viewer_pos, shading_tech):
    """Dibujar toda la malla con la técnica de sombreado especificada"""
    for triangle in mesh:
        if shading_tech.current_shading == "flat":
            color = shading_tech.flat_shading(triangle, light, viewer_pos)
            draw_triangle_flat(surface, triangle, color)
        
        elif shading_tech.current_shading == "gouraud":
            vertex_colors = shading_tech.gouraud_shading(triangle, light, viewer_pos)
            if isinstance(vertex_colors, tuple):  # Fallback a flat
                draw_triangle_flat(surface, triangle, vertex_colors)
            else:
                draw_triangle_gouraud(surface, triangle, vertex_colors)
        
        elif shading_tech.current_shading == "phong":
            # Por simplicidad, usamos flat para Phong en esta demo
            color = shading_tech.flat_shading(triangle, light, viewer_pos)
            draw_triangle_flat(surface, triangle, color)

def main():
    shading = ShadingTechniques()
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)
    small_font = pygame.font.Font(None, 22)
    
    # Configurar luz
    light = LightSource(
        position=(300, 200, 100),
        Ia=(0.2, 0.2, 0.2),
        Id=(0.8, 0.8, 0.8),
        Is=(1.0, 1.0, 1.0)
    )
    
    viewer_pos = (WIDTH // 2, HEIGHT // 2, 300)
    
    # Crear mallas para diferentes técnicas
    mesh_flat = create_sphere_mesh((250, 300, 0), 80)
    mesh_gouraud = create_sphere_mesh((500, 300, 0), 80)
    mesh_gouraud = calculate_vertex_normals(mesh_gouraud)  # Normales para Gouraud
    mesh_phong = create_sphere_mesh((750, 300, 0), 80)
    
    meshes = {
        "flat": mesh_flat,
        "gouraud": mesh_gouraud, 
        "phong": mesh_phong
    }
    
    rotation_angle = 0
    show_wireframe = False
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    shading.current_shading = "flat"
                elif event.key == pygame.K_2:
                    shading.current_shading = "gouraud"
                elif event.key == pygame.K_3:
                    shading.current_shading = "phong"
                elif event.key == pygame.K_w:
                    show_wireframe = not show_wireframe
                elif event.key == pygame.K_LEFT:
                    light.position = (light.position[0] - 20, light.position[1], light.position[2])
                elif event.key == pygame.K_RIGHT:
                    light.position = (light.position[0] + 20, light.position[1], light.position[2])
                elif event.key == pygame.K_UP:
                    light.position = (light.position[0], light.position[1] - 20, light.position[2])
                elif event.key == pygame.K_DOWN:
                    light.position = (light.position[0], light.position[1] + 20, light.position[2])
        
        screen.fill(WHITE)
        
        # Rotar las esferas ligeramente para mejor visualización
        rotation_angle += 0.01
        
        # Dibujar todas las técnicas lado a lado
        techniques = [
            ("FLAT", (250, 300), mesh_flat),
            ("GOURAUD", (500, 300), mesh_gouraud),
            ("PHONG", (750, 300), mesh_phong)
        ]
        
        for tech_name, center, mesh in techniques:
            # Dibujar esfera
            draw_mesh(screen, mesh, light, viewer_pos, shading)
            
            # Etiqueta de técnica
            label_color = RED if tech_name.lower() == shading.current_shading else BLACK
            label = font.render(tech_name, True, label_color)
            screen.blit(label, (center[0] - 40, center[1] + 120))
            
            # Dibujar contorno rojo alrededor de la técnica actual
            if tech_name.lower() == shading.current_shading:
                pygame.draw.circle(screen, RED, center, 95, 3)
        
        # Dibujar información
        info_text = [
            "CLASE 4: TÉCNICAS DE SOMBRADO",
            "1: Flat Shading (Por polígono)",
            "2: Gouraud Shading (Por vértice)", 
            "3: Phong Shading (Por píxel)",
            "W: Alternar wireframe",
            "Flechas: Mover luz",
            f"Técnica actual: {shading.current_shading.upper()}",
            f"Luz en: ({light.position[0]}, {light.position[1]})"
        ]
        
        for i, text in enumerate(info_text):
            color = BLUE if i == 0 else BLACK
            text_surface = font.render(text, True, color) if i < 6 else small_font.render(text, True, color)
            screen.blit(text_surface, (10, 10 + i * 25))
        
        # Dibujar explicación de cada técnica
        explanations = [
            "FLAT SHADING:",
            "- 1 cálculo de iluminación por triángulo",
            "- Rápido pero con facetas visibles",
            "",
            "GOURAUD SHADING:", 
            "- Cálculo en vértices + interpolación",
            "- Suave pero pierde highlights",
            "",
            "PHONG SHADING:",
            "- Cálculo en CADA píxel",
            "- Máxima calidad, más costoso"
        ]
        
        for i, text in enumerate(explanations):
            color = BLUE if i in [0, 4, 8] else BLACK
            text_surface = small_font.render(text, True, color)
            screen.blit(text_surface, (WIDTH - 300, 100 + i * 20))
        
        # Dibujar posición de la luz
        pygame.draw.circle(screen, YELLOW, (int(light.position[0]), int(light.position[1])), 8)
        pygame.draw.circle(screen, BLACK, (int(light.position[0]), int(light.position[1])), 8, 2)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()


