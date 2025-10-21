#Luces y sombras
#Gerardo Mercado Hurtado
#Raúl Martínez Martínez
#Importamos las bibliotecas necesarias
import pygame
import numpy as np
import math
import sys

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clase 2: Modelos de Iluminación - Ambiental, Difusa, Especular")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class Vector3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def normalize(self):
        length = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        if length > 0:
            return Vector3D(self.x/length, self.y/length, self.z/length)
        return Vector3D(0, 0, 0)
    
    def reflect(self, normal):
        # Reflexión del vector incidente sobre la normal
        dot_product = self.dot(normal)
        return Vector3D(
            self.x - 2 * dot_product * normal.x,
            self.y - 2 * dot_product * normal.y,
            self.z - 2 * dot_product * normal.z
        )

class LightSource:
    def __init__(self, position, intensity_ambient, intensity_diffuse, intensity_specular):
        self.position = position
        self.I_ambient = intensity_ambient  # (r, g, b)
        self.I_diffuse = intensity_diffuse  # (r, g, b)
        self.I_specular = intensity_specular  # (r, g, b)

class Material:
    def __init__(self, K_ambient, K_diffuse, K_specular, shininess):
        self.K_ambient = K_ambient  # (r, g, b)
        self.K_diffuse = K_diffuse  # (r, g, b)
        self.K_specular = K_specular  # (r, g, b)
        self.shininess = shininess


class Sphere:
    def __init__(self, center, radius, material, base_color=(1.0, 1.0, 1.0)):
        self.center = center
        self.radius = radius
        self.material = material
        self.base_color = base_color  # Color base (RGB normalizado)
    
    def get_normal(self, point):
        # Vector desde el centro a la superficie (normalizado)
        normal = Vector3D(
            point[0] - self.center[0],
            point[1] - self.center[1],
            point[2] - self.center[2]
        )
        return normal.normalize()

def calculate_phong_illumination(point, normal, light, material, viewer_pos):
    """Calcular iluminación usando el modelo de Phong"""
    
    # 1. Componente AMBIENTAL
    ambient = (
        material.K_ambient[0] * light.I_ambient[0],
        material.K_ambient[1] * light.I_ambient[1],
        material.K_ambient[2] * light.I_ambient[2]
    )
    
    # 2. Componente DIFUSA
    # Vector de luz (desde el punto hacia la luz)
    light_vector = Vector3D(
        light.position[0] - point[0],
        light.position[1] - point[1],
        light.position[2] - point[2]
    ).normalize()
    
    # Coseno del ángulo entre normal y luz
    diffuse_intensity = max(0, normal.dot(light_vector))
    
    diffuse = (
        material.K_diffuse[0] * light.I_diffuse[0] * diffuse_intensity,
        material.K_diffuse[1] * light.I_diffuse[1] * diffuse_intensity,
        material.K_diffuse[2] * light.I_diffuse[2] * diffuse_intensity
    )
    
    # 3. Componente ESPECULAR
    # Vector de vista (desde el punto hacia el observador)
    view_vector = Vector3D(
        viewer_pos[0] - point[0],
        viewer_pos[1] - point[1],
        viewer_pos[2] - point[2]
    ).normalize()
    
    # Vector de reflexión
    reflection_vector = light_vector.reflect(normal)
    
    # Intensidad especular (producto punto reflexión-vista)
    specular_intensity = max(0, reflection_vector.dot(view_vector))
    specular_intensity = specular_intensity ** material.shininess
    
    specular = (
        material.K_specular[0] * light.I_specular[0] * specular_intensity,
        material.K_specular[1] * light.I_specular[1] * specular_intensity,
        material.K_specular[2] * light.I_specular[2] * specular_intensity
    )
    
    # Combinar componentes
    final_color = (
        min(255, int((ambient[0] + diffuse[0] + specular[0]) * 255)),
        min(255, int((ambient[1] + diffuse[1] + specular[1]) * 255)),
        min(255, int((ambient[2] + diffuse[2] + specular[2]) * 255))
    )
    
    return final_color

def draw_sphere_2d(surface, sphere, light, viewer_pos, show_components=False):
    """Dibujar una esfera en 2D con iluminación simplificada"""
    center_x, center_y = sphere.center[0], sphere.center[1]
    radius = sphere.radius
    
    # Crear superficie para la esfera
    sphere_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    
    # Calcular iluminación para cada pixel
    for x in range(radius * 2):
        for y in range(radius * 2):
            # Coordenadas relativas al centro
            rel_x = x - radius
            rel_y = y - radius
            
            # Verificar si está dentro del círculo
            if rel_x**2 + rel_y**2 <= radius**2:
                # Calcular coordenadas 3D (simplificado)
                point_3d = (
                    center_x + rel_x,
                    center_y + rel_y,
                    sphere.center[2] + math.sqrt(max(0, radius**2 - rel_x**2 - rel_y**2))
                )
                
                # Obtener normal en este punto
                normal = sphere.get_normal(point_3d)
                
                # Calcular color con iluminación
                color = calculate_phong_illumination(point_3d, normal, light, sphere.material, viewer_pos)
                # Aplicar color base de la bola
                color = (
                    min(255, int(color[0] * sphere.base_color[0])),
                    min(255, int(color[1] * sphere.base_color[1])),
                    min(255, int(color[2] * sphere.base_color[2]))
                )

                
                # Dibujar pixel
                sphere_surface.set_at((x, y), color)
    
    # Dibujar la esfera en la posición correcta
    surface.blit(sphere_surface, (center_x - radius, center_y - radius))
    
    # Dibujar contorno
    pygame.draw.circle(surface, BLACK, (center_x, center_y), radius, 1)

def draw_vector(surface, start, direction, color, scale=50):
    """Dibujar un vector en la pantalla"""
    end = (start[0] + direction.x * scale, start[1] + direction.y * scale)
    pygame.draw.line(surface, color, start, end, 2)
    
    # Dibujar cabeza de flecha
    angle = math.atan2(direction.y, direction.x)
    arrow_length = 10
    arrow_angle = math.pi / 6
    
    # Puntos para la cabeza de flecha
    arrow1 = (
        end[0] - arrow_length * math.cos(angle - arrow_angle),
        end[1] - arrow_length * math.sin(angle - arrow_angle)
    )
    arrow2 = (
        end[0] - arrow_length * math.cos(angle + arrow_angle),
        end[1] - arrow_length * math.sin(angle + arrow_angle)
    )
    
    pygame.draw.line(surface, color, end, arrow1, 2)
    pygame.draw.line(surface, color, end, arrow2, 2)

def main():
    # Configurar materiales
    plastic_material = Material(
        K_ambient=(0.1, 0.1, 0.1),
        K_diffuse=(0.7, 0.7, 0.7),
        K_specular=(0.3, 0.3, 0.3),
        shininess=10
    )
    
    metal_material = Material(
        K_ambient=(0.2, 0.2, 0.2),
        K_diffuse=(0.3, 0.3, 0.3),
        K_specular=(0.8, 0.8, 0.8),
        shininess=50
    )
    
    rubber_material = Material(
        K_ambient=(0.05, 0.05, 0.05),
        K_diffuse=(0.5, 0.5, 0.5),
        K_specular=(0.1, 0.1, 0.1),
        shininess=5
    )

    billiard_material = Material(
        K_ambient=(0.15, 0.15, 0.15),
        K_diffuse=(0.6, 0.6, 0.6),
        K_specular=(0.6, 0.6, 0.6),
        shininess=30
    )
    
    # Configurar luz
    light = LightSource(
        position=(300, 200, 100),
        intensity_ambient=(0.2, 0.2, 0.2),
        intensity_diffuse=(0.8, 0.8, 0.8),
        intensity_specular=(1.0, 1.0, 1.0)
    )
    
    # Crear esferas con diferentes materiales
    spheres = [
    Sphere((200, 300, 0), 80, plastic_material, base_color=(1.0, 0.1, 0.1)),   # Roja
    Sphere((400, 300, 0), 80, metal_material, base_color=(0.1, 0.1, 1.0)),     # Azul
    Sphere((600, 300, 0), 80, rubber_material, base_color=(0.1, 1.0, 0.1)),    # Verde
    Sphere((800, 300, 0), 80, billiard_material, base_color=(1.0, 1.0, 0.0))   # Amarilla 🎱
    ]


    
    # Posición del observador
    viewer_pos = (WIDTH // 2, HEIGHT // 2, 300)
    
    running = True
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)
    
    # Modos de visualización
    show_vectors = True
    current_component = "all"  # "ambient", "diffuse", "specular", "all"
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v:
                    show_vectors = not show_vectors
                elif event.key == pygame.K_1:
                    current_component = "ambient"
                    print("Mostrando solo componente AMBIENTAL")
                elif event.key == pygame.K_2:
                    current_component = "diffuse"
                    print("Mostrando solo componente DIFUSA")
                elif event.key == pygame.K_3:
                    current_component = "specular"
                    print("Mostrando solo componente ESPECULAR")
                elif event.key == pygame.K_4:
                    current_component = "all"
                    print("Mostrando TODOS los componentes")
                elif event.key == pygame.K_LEFT:
                    # Mover luz a la izquierda
                    light.position = (light.position[0] - 20, light.position[1], light.position[2])
                elif event.key == pygame.K_RIGHT:
                    # Mover luz a la derecha
                    light.position = (light.position[0] + 20, light.position[1], light.position[2])
                elif event.key == pygame.K_UP:
                    # Mover luz arriba
                    light.position = (light.position[0], light.position[1] - 20, light.position[2])
                elif event.key == pygame.K_DOWN:
                    # Mover luz abajo
                    light.position = (light.position[0], light.position[1] + 20, light.position[2])
        
        # Dibujar
        screen.fill(WHITE)
        
        # Dibujar esferas
        for i, sphere in enumerate(spheres):
            # Modificar temporalmente el material según el componente mostrado
            original_material = sphere.material
            temp_material = Material(
                K_ambient=original_material.K_ambient,
                K_diffuse=original_material.K_diffuse,
                K_specular=original_material.K_specular,
                shininess=original_material.shininess
            )
            
            if current_component == "ambient":
                temp_material.K_diffuse = (0, 0, 0)
                temp_material.K_specular = (0, 0, 0)
            elif current_component == "diffuse":
                temp_material.K_ambient = (0, 0, 0)
                temp_material.K_specular = (0, 0, 0)
            elif current_component == "specular":
                temp_material.K_ambient = (0, 0, 0)
                temp_material.K_diffuse = (0, 0, 0)
            
            sphere.material = temp_material
            draw_sphere_2d(screen, sphere, light, viewer_pos)
            sphere.material = original_material
        
        # Dibujar vectores si está activado
        if show_vectors:
            # Dibujar vector de luz
            light_vector = Vector3D(
                spheres[0].center[0] - light.position[0],
                spheres[0].center[1] - light.position[1],
                spheres[0].center[2] - light.position[2]
            ).normalize()
            
            draw_vector(screen, (spheres[0].center[0], spheres[0].center[1]), light_vector, RED, 80)
            
            # Dibujar vector normal (en la parte superior de la esfera)
            normal_vector = Vector3D(0, -1, 0)
            draw_vector(screen, (spheres[0].center[0], spheres[0].center[1] - 80), normal_vector, GREEN, 60)
            
            # Dibujar vector de vista
            view_vector = Vector3D(
                viewer_pos[0] - spheres[0].center[0],
                viewer_pos[1] - spheres[0].center[1],
                viewer_pos[2] - spheres[0].center[2]
            ).normalize()
            
            draw_vector(screen, (spheres[0].center[0], spheres[0].center[1]), view_vector, BLUE, 60)
        
        # Dibujar posición de la luz
        pygame.draw.circle(screen, YELLOW, (int(light.position[0]), int(light.position[1])), 10)
        pygame.draw.circle(screen, BLACK, (int(light.position[0]), int(light.position[1])), 10, 2)
        
        # Dibujar instrucciones
        instructions = [
            "CLASE 2: MODELOS DE ILUMINACIÓN",
            "1, 2, 3, 4: Componentes (Ambiental, Difusa, Especular, Todos)",  
            "Flechas: Mover fuente de luz",
            "V: Alternar vectores",
            f"Modo: {current_component.upper()}",
            f"Luz en: ({light.position[0]}, {light.position[1]})"
        ]
        
        for i, instruction in enumerate(instructions):
            color = BLUE if i == 0 else BLACK
            text = font.render(instruction, True, color)
            screen.blit(text, (10, 10 + i * 30))
        
        # Dibujar información de materiales
        material_info = [
        "MATERIALES:",
        "Izq: Plástico (shininess=10)",
        "Centro: Metal (shininess=50)", 
        "Der: Goma (shininess=5)",
        "Ext. Derecha: Billar (shininess=30)"
        ]

        
        for i, info in enumerate(material_info):
            text = font.render(info, True, RED)
            screen.blit(text, (WIDTH - 250, 10 + i * 25))
        
        # Dibujar leyenda de vectores
        if show_vectors:
            vector_legend = [
                "VECTORES:",
                "Rojo: Dirección de la luz",
                "Verde: Normal de la superficie",
                "Azul: Dirección de vista"
            ]
            for i, legend in enumerate(vector_legend):
                text = font.render(legend, True, BLACK)
                screen.blit(text, (WIDTH - 300, 150 + i * 25))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
