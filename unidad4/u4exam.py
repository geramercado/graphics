#Gerardo Mercado Hurtado
#Raúl Martínez Martínez
# Sombreado: FLAT, GOURAUD, PHONG, SOLID, NORMALS, SOLID WIREFRAME.
#Examen unidad 4, 30 octubre 2025.
# Importar las bibliotecas necesarias
import pygame
import math
import sys

# Inicialización
pygame.init()
WIDTH, HEIGHT = 1200, 900  # Pantalla más grande
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Examen unidad 4, Gerardo Mercado Hurtado, Raúl Martínez Martínez")

# Colores básicos
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (150, 150, 150)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)
GOLD = (255, 215, 0)

# Ancho del Panel (Constante)
PANEL_WIDTH = 250 

# --- Funciones de Álgebra Vectorial
def producto_cruzado(v1, v2):
    x = v1[1] * v2[2] - v1[2] * v2[1]
    y = v1[2] * v2[0] - v1[0] * v2[2]
    z = v1[0] * v2[1] - v1[1] * v2[0]
    return (x, y, z)

def normalizar(v):
    magnitud = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    if magnitud == 0:
        return (0.0, 0.0, 0.0)
    return (v[0] / magnitud, v[1] / magnitud, v[2] / magnitud)

def producto_punto(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]

def restar_vectores(v1, v2):
    return (v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2])

def sumar_vectores(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2])

def escalar_vector(v, s):
    return (v[0] * s, v[1] * s, v[2] * s)

# --- Clases de Geometría y Cámara
class Punto3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.normal = (0.0, 0.0, 0.0) 

class Triangulo:
    def __init__(self, p1, p2, p3, color=GRAY):
        self.puntos = [p1, p2, p3]
        self.color = color

class Camara:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.z = 500  # La cámara está alejada
    
    def proyectar(self, punto):
        factor = 200 / (punto.z + 400) 
        screen_x = self.x + (punto.x - self.x) * factor
        screen_y = self.y + (punto.y - self.y) * factor
        return (int(screen_x), int(screen_y))

class Luz:
    def __init__(self, x, y, z):
        self.posicion = Punto3D(x, y, z)
        self.intensidad = 0.8 

# --- Funciones de Creación de Modelos 3D
def crear_cubo_simple(centro_x, centro_y, centro_z, tamaño):
    medio = tamaño / 2
    
    vertices = [
        Punto3D(centro_x - medio, centro_y - medio, centro_z - medio),  # 0
        Punto3D(centro_x + medio, centro_y - medio, centro_z - medio),  # 1  
        Punto3D(centro_x + medio, centro_y + medio, centro_z - medio),  # 2
        Punto3D(centro_x - medio, centro_y + medio, centro_z - medio),  # 3
        Punto3D(centro_x - medio, centro_y - medio, centro_z + medio),  # 4
        Punto3D(centro_x + medio, centro_y - medio, centro_z + medio),  # 5
        Punto3D(centro_x + medio, centro_y + medio, centro_z + medio),  # 6
        Punto3D(centro_x - medio, centro_y + medio, centro_z + medio),  # 7
    ]
    
    triangulos = [
        Triangulo(vertices[0], vertices[1], vertices[2], RED), Triangulo(vertices[0], vertices[2], vertices[3], RED), # Front
        Triangulo(vertices[1], vertices[5], vertices[6], GREEN), Triangulo(vertices[1], vertices[6], vertices[2], GREEN), # Right
        Triangulo(vertices[5], vertices[4], vertices[7], BLUE), Triangulo(vertices[5], vertices[7], vertices[6], BLUE), # Back
        Triangulo(vertices[4], vertices[0], vertices[3], YELLOW), Triangulo(vertices[4], vertices[3], vertices[7], YELLOW), # Left
        Triangulo(vertices[3], vertices[2], vertices[6], MAGENTA), Triangulo(vertices[3], vertices[6], vertices[7], MAGENTA), # Top
        Triangulo(vertices[4], vertices[5], vertices[1], CYAN), Triangulo(vertices[4], vertices[1], vertices[0], CYAN), # Bottom
    ]
    
    return triangulos

def crear_piramide_simple(centro_x, centro_y, centro_z, tamaño):
    medio = tamaño / 2
    altura = tamaño * 0.8
    
    vertices = [
        Punto3D(centro_x, centro_y - altura, centro_z),  # 0: punta
        Punto3D(centro_x - medio, centro_y + medio, centro_z - medio),  # 1
        Punto3D(centro_x + medio, centro_y + medio, centro_z - medio),  # 2
        Punto3D(centro_x + medio, centro_y + medio, centro_z + medio),  # 3
        Punto3D(centro_x - medio, centro_y + medio, centro_z + medio),  # 4
    ]
    
    triangulos = [
        Triangulo(vertices[0], vertices[1], vertices[2], GREEN), 
        Triangulo(vertices[0], vertices[2], vertices[3], BLUE),
        Triangulo(vertices[0], vertices[3], vertices[4], RED), 
        Triangulo(vertices[0], vertices[4], vertices[1], YELLOW),
        Triangulo(vertices[1], vertices[2], vertices[3], GRAY), 
        Triangulo(vertices[1], vertices[3], vertices[4], GRAY),
    ]
    
    return triangulos
#función para crear el corazón 
def crear_corazon(centro_x, centro_y, centro_z, tamaño, color=RED):
    vertices = []
    triangulos = []

    puntos_2d_base = []
    num_segmentos = 20
    escala = tamaño / 100.0 
    
    for i in range(num_segmentos + 1):
        t = (i / float(num_segmentos)) * 2 * math.pi
        x = centro_x + 16 * math.sin(t)**3 * escala
        y = centro_y - (13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)) * escala
        puntos_2d_base.append((x, y))

    depth = 30
    
    front_vertices = []
    for x, y in puntos_2d_base:
        p = Punto3D(x, y, centro_z + depth / 2)
        vertices.append(p)
        front_vertices.append(p)

    back_vertices = []
    for x, y in puntos_2d_base:
        p = Punto3D(x, y, centro_z - depth / 2)
        vertices.append(p)
        back_vertices.append(p)

    centro_frente = Punto3D(centro_x, centro_y, centro_z + depth / 2)
    vertices.append(centro_frente)
    for i in range(len(front_vertices) - 1):
        triangulos.append(Triangulo(centro_frente, front_vertices[i+1], front_vertices[i], color))

    centro_atras = Punto3D(centro_x, centro_y, centro_z - depth / 2)
    vertices.append(centro_atras)
    for i in range(len(back_vertices) - 1):
        triangulos.append(Triangulo(centro_atras, back_vertices[i], back_vertices[i+1], color))

    for i in range(len(front_vertices) - 1):
        p1 = front_vertices[i]
        p2 = front_vertices[i+1]
        p3 = back_vertices[i+1]
        p4 = back_vertices[i]

        triangulos.append(Triangulo(p1, p2, p3, color))
        triangulos.append(Triangulo(p1, p3, p4, color))
        
    p1 = front_vertices[-1]
    p2 = front_vertices[0]
    p3 = back_vertices[0]
    p4 = back_vertices[-1]

    triangulos.append(Triangulo(p1, p2, p3, color))
    triangulos.append(Triangulo(p1, p3, p4, color))

    return triangulos

#función para crear el trebol en la imagen 3D.
def crear_trebol(centro_x, centro_y, centro_z, tamaño, color=GREEN):
    triangulos = []
    radio_hoja = tamaño / 3
    separacion_hoja = tamaño / 4
    
    def crear_hoja(cx, cy, cz, r, segmentos=10, hoja_color=GREEN):
        hoja_verts = []
        hoja_tris = []
        
        hoja_verts.append(Punto3D(cx, cy - r, cz)) # 0: Vértice superior
        
        for i in range(segmentos):
            angle = 2 * math.pi / segmentos * i
            x_seg = cx + r * math.cos(angle)
            z_seg = cz + r * math.sin(angle)
            y_seg = cy
            hoja_verts.append(Punto3D(x_seg, y_seg, z_seg))
        
        hoja_verts.append(Punto3D(cx, cy + r, cz)) # Vértice inferior
        
        for i in range(segmentos):
            p1 = hoja_verts[0]
            p2 = hoja_verts[i + 1]
            p3 = hoja_verts[(i + 1) % segmentos + 1]
            hoja_tris.append(Triangulo(p1, p3, p2, hoja_color)) 
            
        for i in range(segmentos):
            p1 = hoja_verts[i + 1]
            p2 = hoja_verts[len(hoja_verts) - 1]
            p3 = hoja_verts[(i + 1) % segmentos + 1]
            hoja_tris.append(Triangulo(p1, p2, p3, hoja_color))

        return hoja_tris

    triangulos.extend(crear_hoja(centro_x - separacion_hoja, centro_y - separacion_hoja, centro_z, radio_hoja, 8, GREEN))
    triangulos.extend(crear_hoja(centro_x + separacion_hoja, centro_y - separacion_hoja, centro_z, radio_hoja, 8, GREEN))
    triangulos.extend(crear_hoja(centro_x, centro_y + separacion_hoja, centro_z, radio_hoja, 8, GREEN))

    radio_tallo = radio_hoja / 4
    altura_tallo = tamaño / 2
    
    tallo_verts = []
    tallo_centro_x = centro_x
    tallo_centro_y = centro_y + separacion_hoja + radio_hoja + altura_tallo / 2
    
    for i in range(8): 
        angle = 2 * math.pi / 8 * i
        x_seg = tallo_centro_x + radio_tallo * math.cos(angle)
        z_seg = centro_z + radio_tallo * math.sin(angle)
        y_seg_top = tallo_centro_y - altura_tallo / 2
        y_seg_bottom = tallo_centro_y + altura_tallo / 2
        tallo_verts.append(Punto3D(x_seg, y_seg_top, z_seg))
        tallo_verts.append(Punto3D(x_seg, y_seg_bottom, z_seg))
    
    for i in range(0, len(tallo_verts) - 3, 2):
        p1 = tallo_verts[i]
        p2 = tallo_verts[i+2] 
        p3 = tallo_verts[i+3] 
        p4 = tallo_verts[i+1]

        triangulos.append(Triangulo(p1, p2, p3, BROWN))
        triangulos.append(Triangulo(p1, p3, p4, BROWN))

    p1 = tallo_verts[len(tallo_verts) - 2]
    p2 = tallo_verts[0]
    p3 = tallo_verts[1]
    p4 = tallo_verts[len(tallo_verts) - 1]
    triangulos.append(Triangulo(p1, p2, p3, BROWN))
    triangulos.append(Triangulo(p1, p3, p4, BROWN))
    
    return triangulos


def crear_ventana(centro_x, centro_y, centro_z, ancho, alto, profundidad, color_marco=BROWN, color_cristal=CYAN):
    triangulos = []
    
    medio_ancho = ancho / 2
    medio_alto = alto / 2
    medio_profundidad = profundidad / 2
    grosor_marco = ancho / 8 

    v0 = Punto3D(centro_x - medio_ancho, centro_y - medio_alto, centro_z + medio_profundidad)
    v1 = Punto3D(centro_x + medio_ancho, centro_y - medio_alto, centro_z + medio_profundidad)
    v2 = Punto3D(centro_x + medio_ancho, centro_y + medio_alto, centro_z + medio_profundidad)
    v3 = Punto3D(centro_x - medio_ancho, centro_y + medio_alto, centro_z + medio_profundidad)
    v4 = Punto3D(centro_x - medio_ancho, centro_y - medio_alto, centro_z - medio_profundidad)
    v5 = Punto3D(centro_x + medio_ancho, centro_y - medio_alto, centro_z - medio_profundidad)
    v6 = Punto3D(centro_x + medio_ancho, centro_y + medio_alto, centro_z - medio_profundidad)
    v7 = Punto3D(centro_x - medio_ancho, centro_y + medio_alto, centro_z - medio_profundidad)

    cubo_exterior_tris = [
        Triangulo(v0,v1,v2, color_marco), Triangulo(v0,v2,v3, color_marco), # Frente
        Triangulo(v1,v5,v6, color_marco), Triangulo(v1,v6,v2, color_marco), # Derecha
        Triangulo(v5,v4,v7, color_marco), Triangulo(v5,v7,v6, color_marco), # Atrás
        Triangulo(v4,v0,v3, color_marco), Triangulo(v4,v3,v7, color_marco), # Izquierda
        Triangulo(v3,v2,v6, color_marco), Triangulo(v3,v6,v7, color_marco), # Arriba
        Triangulo(v4,v5,v1, color_marco), Triangulo(v4,v1,v0, color_marco), # Abajo
    ]
    triangulos.extend(cubo_exterior_tris)

    cx0 = Punto3D(centro_x - medio_ancho + grosor_marco, centro_y - medio_alto + grosor_marco, centro_z + medio_profundidad / 2)
    cx1 = Punto3D(centro_x + medio_ancho - grosor_marco, centro_y - medio_alto + grosor_marco, centro_z + medio_profundidad / 2)
    cx2 = Punto3D(centro_x + medio_ancho - grosor_marco, centro_y + medio_alto - grosor_marco, centro_z + medio_profundidad / 2)
    cx3 = Punto3D(centro_x - medio_ancho + grosor_marco, centro_y + medio_alto - grosor_marco, centro_z + medio_profundidad / 2)
    
    triangulos.append(Triangulo(cx0, cx1, cx2, color_cristal))
    triangulos.append(Triangulo(cx0, cx2, cx3, color_cristal))
    
    cx0_b = Punto3D(centro_x - medio_ancho + grosor_marco, centro_y - medio_alto + grosor_marco, centro_z - medio_profundidad / 2)
    cx1_b = Punto3D(centro_x + medio_ancho - grosor_marco, centro_y - medio_alto + grosor_marco, centro_z - medio_profundidad / 2)
    cx2_b = Punto3D(centro_x + medio_ancho - grosor_marco, centro_y + medio_alto - grosor_marco, centro_z - medio_profundidad / 2)
    cx3_b = Punto3D(centro_x - medio_ancho + grosor_marco, centro_y + medio_alto - grosor_marco, centro_z - medio_profundidad / 2)
    triangulos.append(Triangulo(cx0_b, cx2_b, cx1_b, color_cristal)) 
    triangulos.append(Triangulo(cx0_b, cx3_b, cx2_b, color_cristal))

    return triangulos

#función que crea la imagen del girasol
def crear_girasol(centro_x, centro_y, centro_z, radio_centro, radio_petalo, num_petalos, color_centro=BROWN, color_petalo=YELLOW):
    triangulos = []

    segmentos_centro = 20
    vertices_centro_frente = []
    vertices_centro_atras = []
    
    for i in range(segmentos_centro):
        angle = 2 * math.pi / segmentos_centro * i
        x = centro_x + radio_centro * math.cos(angle)
        y = centro_y + radio_centro * math.sin(angle)
        vertices_centro_frente.append(Punto3D(x, y, centro_z + 5)) 
        vertices_centro_atras.append(Punto3D(x, y, centro_z - 5)) 
    
    centro_punto_frente = Punto3D(centro_x, centro_y, centro_z + 5)
    for i in range(segmentos_centro):
        p1 = vertices_centro_frente[i]
        p2 = vertices_centro_frente[(i + 1) % segmentos_centro]
        triangulos.append(Triangulo(centro_punto_frente, p2, p1, color_centro))

    centro_punto_atras = Punto3D(centro_x, centro_y, centro_z - 5)
    for i in range(segmentos_centro):
        p1 = vertices_centro_atras[i]
        p2 = vertices_centro_atras[(i + 1) % segmentos_centro]
        triangulos.append(Triangulo(centro_punto_atras, p1, p2, color_centro)) 

    for i in range(num_petalos):
        angle_base = 2 * math.pi / num_petalos * i
        
        x_base_in = centro_x + radio_centro * math.cos(angle_base)
        y_base_in = centro_y + radio_centro * math.sin(angle_base)
        
        x_out = centro_x + (radio_centro + radio_petalo) * math.cos(angle_base)
        y_out = centro_y + (radio_centro + radio_petalo) * math.sin(angle_base)
        
        angle_side_offset = math.pi / num_petalos / 2 
        
        x_base_side1 = centro_x + radio_centro * math.cos(angle_base - angle_side_offset)
        y_base_side1 = centro_y + radio_centro * math.sin(angle_base - angle_side_offset)
        
        x_base_side2 = centro_x + radio_centro * math.cos(angle_base + angle_side_offset)
        y_base_side2 = centro_y + radio_centro * math.sin(angle_base + angle_side_offset)

        p_in1 = Punto3D(x_base_in, y_base_in, centro_z + 2) 
        p_in2 = Punto3D(x_base_side1, y_base_side1, centro_z + 2)
        p_in3 = Punto3D(x_base_side2, y_base_side2, centro_z + 2)

        p_out = Punto3D(x_out, y_out, centro_z + 5) 

        triangulos.append(Triangulo(p_in1, p_out, p_in2, color_petalo))
        triangulos.append(Triangulo(p_in1, p_in3, p_out, color_petalo))

    return triangulos


# --- Funciones de Normales para Gouraud/Phong
def calcular_normales_vertice(todos_triangulos):
    normales_por_vertice = {}
    
    for triangulo in todos_triangulos:
        puntos = triangulo.puntos
        p1, p2, p3 = puntos[0], puntos[1], puntos[2]

        v1 = (p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)
        v2 = (p3.x - p1.x, p3.y - p1.y, p3.z - p1.z)
        normal_cara = normalizar(producto_cruzado(v1, v2))
        
        for punto in puntos:
            clave = id(punto) 
            if clave not in normales_por_vertice:
                normales_por_vertice[clave] = []
            normales_por_vertice[clave].append(normal_cara)

    for punto in [p for t in todos_triangulos for p in t.puntos]:
        clave = id(punto)
        if clave in normales_por_vertice:
            suma_x, suma_y, suma_z = 0, 0, 0
            
            for nx, ny, nz in normales_por_vertice[clave]:
                suma_x += nx
                suma_y += ny
                suma_z += nz
            
            normal_promedio = (suma_x, suma_y, suma_z) 
            punto.normal = normalizar(normal_promedio)
            
# --- Funciones de Sombreado y Dibujo
def obtener_intensidad_gouraud(punto, luz):
    normal_n = punto.normal
    luz_v = (luz.posicion.x - punto.x, luz.posicion.y - punto.y, luz.posicion.z - punto.z)
    luz_n = normalizar(luz_v)
    intensidad = producto_punto(normal_n, luz_n)
    intensidad = max(0.2, min(luz.intensidad, intensidad)) 
    return intensidad

def calcular_color_phong(triangulo, camara, luz):
    p1, p2, p3 = triangulo.puntos
    centro_x = (p1.x + p2.x + p3.x) / 3.0
    centro_y = (p1.y + p2.y + p3.y) / 3.0
    centro_z = (p1.z + p2.z + p3.z) / 3.0
    centroide = Punto3D(centro_x, centro_y, centro_z)

    v1 = (p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)
    v2 = (p3.x - p1.x, p3.y - p1.y, p3.z - p1.z)
    normal_n = normalizar(producto_cruzado(v1, v2))
    
    ambiental_f = 0.15 
    especular_poder = 10.0 
    especular_color = (255, 255, 255) 
    luz_i = luz.intensidad
    
    P = (centroide.x, centroide.y, centroide.z) 
    L_v = restar_vectores((luz.posicion.x, luz.posicion.y, luz.posicion.z), P)
    L_n = normalizar(L_v) 

    V_v = restar_vectores((camara.x, camara.y, camara.z), P)
    V_n = normalizar(V_v) 

    color_base_r, color_base_g, color_base_b = triangulo.color
    
    ambiente_r = color_base_r * ambiental_f
    ambiente_g = color_base_g * ambiental_f
    ambiente_b = color_base_b * ambiental_f

    difusa_factor = max(0.0, producto_punto(normal_n, L_n))
    
    difusa_r = color_base_r * luz_i * difusa_factor
    difusa_g = color_base_g * luz_i * difusa_factor
    difusa_b = color_base_b * luz_i * difusa_factor

    R_n = normalizar(restar_vectores(escalar_vector(normal_n, 2 * difusa_factor), L_n))
    
    especular_factor = max(0.0, producto_punto(R_n, V_n))
    especular_i = luz_i * (especular_factor ** especular_poder)
    
    especular_r = especular_color[0] * especular_i
    especular_g = especular_color[1] * especular_i
    especular_b = especular_color[2] * especular_i
    
    final_r = ambiente_r + difusa_r + especular_r
    final_g = ambiente_g + difusa_g + especular_b
    final_b = ambiente_b + difusa_b + especular_b
    
    final_r = int(min(255, final_r))
    final_g = int(min(255, final_g))
    final_b = int(min(255, final_b))

    return (final_r, final_g, final_b)

def dibujar_normal_cara(screen, triangulo, camara):
    p1, p2, p3 = triangulo.puntos
    
    centro_x = (p1.x + p2.x + p3.x) / 3.0
    centro_y = (p1.y + p2.y + p3.y) / 3.0
    centro_z = (p1.z + p2.z + p3.z) / 3.0
    centroide = Punto3D(centro_x, centro_y, centro_z)
    
    v1 = (p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)
    v2 = (p3.x - p1.x, p3.y - p1.y, p3.z - p1.z)
    normal_n = normalizar(producto_cruzado(v1, v2))

    longitud = 20 
    
    punto_final = Punto3D(
        centroide.x + normal_n[0] * longitud,
        centroide.y + normal_n[1] * longitud,
        centroide.z + normal_n[2] * longitud
    )
    
    start_2d = camara.proyectar(centroide)
    end_2d = camara.proyectar(punto_final)
    
    pygame.draw.line(screen, (0, 255, 255), start_2d, end_2d, 1)
    pygame.draw.circle(screen, (0, 255, 255), start_2d, 2)


def dibujar_triangulo_solido(screen, triangulo, camara):
    puntos_2d = [camara.proyectar(p) for p in triangulo.puntos]
    pygame.draw.polygon(screen, triangulo.color, puntos_2d)
    pygame.draw.polygon(screen, BLACK, puntos_2d, 1)

def dibujar_triangulo_flat(screen, triangulo, camara, luz):
    color_sombreado = obtener_color_sombreado_flat(triangulo, luz)
    puntos_2d = [camara.proyectar(p) for p in triangulo.puntos]
    pygame.draw.polygon(screen, color_sombreado, puntos_2d)
    pygame.draw.polygon(screen, BLACK, puntos_2d, 1) 

def dibujar_triangulo_gouraud(screen, triangulo, camara, luz):
    puntos = triangulo.puntos
    intensidades = [obtener_intensidad_gouraud(p, luz) for p in puntos]
    
    r, g, b = triangulo.color
    max_intensity = max(intensidades)
    color_final = (int(r * max_intensity), int(g * max_intensity), int(b * max_intensity))
    
    puntos_2d = [camara.proyectar(p) for p in puntos]
    
    pygame.draw.polygon(screen, color_final, puntos_2d)
    pygame.draw.polygon(screen, BLACK, puntos_2d, 1)

def dibujar_triangulo_phong(screen, triangulo, camara, luz):
    color_sombreado = calcular_color_phong(triangulo, camara, luz)
    
    puntos_2d = [camara.proyectar(p) for p in triangulo.puntos]
    
    pygame.draw.polygon(screen, color_sombreado, puntos_2d)
    pygame.draw.polygon(screen, BLACK, puntos_2d, 1)


def dibujar_triangulo_alambre(screen, triangulo, camara):
    puntos_2d = [camara.proyectar(p) for p in triangulo.puntos]
    pygame.draw.polygon(screen, BLACK, puntos_2d, 1)


def obtener_color_sombreado_flat(triangulo, luz):
    p1, p2, p3 = triangulo.puntos
    v1 = (p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)
    v2 = (p3.x - p1.x, p3.y - p1.y, p3.z - p1.z)
    normal_n = normalizar(producto_cruzado(v1, v2))
    luz_v = (luz.posicion.x - p1.x, luz.posicion.y - p1.y, luz.posicion.z - p1.z)
    luz_n = normalizar(luz_v)
    intensidad = producto_punto(normal_n, luz_n)
    intensidad = max(0.2, min(luz.intensidad, intensidad)) 
    r, g, b = triangulo.color
    return (int(r * intensidad), int(g * intensidad), int(b * intensidad))

def dibujar_ejes(screen, camara):
    offset_x = 0
    if main.mostrar_menu: # Acceso a mostrar_menu desde main
        offset_x = PANEL_WIDTH

    origen = Punto3D(offset_x + (WIDTH - offset_x) // 2 - 100, HEIGHT // 2, 0) 
    eje_x = Punto3D(origen.x + 100, origen.y, 0)
    px1 = camara.proyectar(origen)
    px2 = camara.proyectar(eje_x)
    pygame.draw.line(screen, RED, px1, px2, 2)
    eje_y = Punto3D(origen.x, origen.y - 100, 0)
    py2 = camara.proyectar(eje_y)
    pygame.draw.line(screen, GREEN, px1, py2, 2)
    eje_z = Punto3D(origen.x, origen.y, 100)
    pz2 = camara.proyectar(eje_z)
    pygame.draw.line(screen, BLUE, px1, pz2, 2)
    font = pygame.font.Font(None, 24)
    screen.blit(font.render("X", True, RED), (px2[0] + 5, px2[1]))
    screen.blit(font.render("Y", True, GREEN), (py2[0], py2[1] - 20))
    screen.blit(font.render("Z", True, BLUE), (pz2[0] + 5, pz2[1]))


# --- Panel de Menú
def dibujar_panel_menu(screen, modo_dibujo, modelo_seleccionado, mostrar_wireframe, mostrar_normales):
    PANEL_HEIGHT = HEIGHT; PANEL_COLOR = (240, 240, 240) 
    BUTTON_ACTIVE_COLOR = (100, 100, 100); BUTTON_INACTIVE_COLOR = (180, 180, 180); TEXT_COLOR = BLACK
    
    pygame.draw.rect(screen, PANEL_COLOR, (0, 0, PANEL_WIDTH, PANEL_HEIGHT))
    
    font_large = pygame.font.Font(None, 20); font_medium = pygame.font.Font(None, 20); font_small = pygame.font.Font(None, 20)
    y_offset = 20
    titulo_line1 = font_large.render("RENDERIZADOR 3D", True, BLACK); titulo_line2 = font_large.render("TÉCNICAS DE SOMBREADO", True, BLACK)
    screen.blit(titulo_line1, (20, y_offset)); y_offset += 30
    screen.blit(titulo_line2, (20, y_offset)); y_offset += 50

    color = BUTTON_ACTIVE_COLOR if modo_dibujo == "solido" else BUTTON_INACTIVE_COLOR
    pygame.draw.rect(screen, color, pygame.Rect(30, y_offset, 180, 40), border_radius=5)
    screen.blit(font_medium.render("1 - SÓLIDO (Color Base)", True, WHITE), (55, y_offset + 10)); y_offset += 50
    
    color = BUTTON_ACTIVE_COLOR if modo_dibujo == "alambre" else BUTTON_INACTIVE_COLOR
    pygame.draw.rect(screen, color, pygame.Rect(30, y_offset, 180, 40), border_radius=5)
    screen.blit(font_medium.render("2 - ALAMBRE", True, WHITE), (80, y_offset + 10)); y_offset += 50
    
    color = BUTTON_ACTIVE_COLOR if modo_dibujo == "flat" else BUTTON_INACTIVE_COLOR
    pygame.draw.rect(screen, color, pygame.Rect(30, y_offset, 180, 40), border_radius=5)
    screen.blit(font_medium.render("3 - FLAT (Por Cara)", True, WHITE), (45, y_offset + 10)); y_offset += 50
    
    color = BUTTON_ACTIVE_COLOR if modo_dibujo == "gouraud" else BUTTON_INACTIVE_COLOR
    pygame.draw.rect(screen, color, pygame.Rect(30, y_offset, 180, 40), border_radius=5)
    screen.blit(font_medium.render("4 - GOURAUD (Por Vértice)", True, WHITE), (35, y_offset + 10)); y_offset += 50

    color = BUTTON_ACTIVE_COLOR if modo_dibujo == "phong" else BUTTON_INACTIVE_COLOR
    pygame.draw.rect(screen, color, pygame.Rect(30, y_offset, 180, 40), border_radius=5)
    screen.blit(font_medium.render("5 - PHONG (Con Especularidad)", True, WHITE), (25, y_offset + 10)); y_offset += 60

    screen.blit(font_medium.render("MODELOS Y SHADING", True, BLACK), (20, y_offset)); y_offset += 30

    color = BUTTON_ACTIVE_COLOR if modelo_seleccionado == "CORAZON_FLAT" else BUTTON_INACTIVE_COLOR
    pygame.draw.rect(screen, color, pygame.Rect(30, y_offset, 180, 30), border_radius=5)
    screen.blit(font_small.render("6 - Corazón (Flat)", True, WHITE), (60, y_offset + 7)); y_offset += 35

    color = BUTTON_ACTIVE_COLOR if modelo_seleccionado == "TREBOL_GOURAUD" else BUTTON_INACTIVE_COLOR
    pygame.draw.rect(screen, color, pygame.Rect(30, y_offset, 180, 30), border_radius=5)
    screen.blit(font_small.render("7 - Trébol (Gouraud)", True, WHITE), (45, y_offset + 7)); y_offset += 35
    
    color = BUTTON_ACTIVE_COLOR if modelo_seleccionado == "VENTANA_PHONG" else BUTTON_INACTIVE_COLOR
    pygame.draw.rect(screen, color, pygame.Rect(30, y_offset, 180, 30), border_radius=5)
    screen.blit(font_small.render("8 - Ventana (Phong)", True, WHITE), (50, y_offset + 7)); y_offset += 35

    color = BUTTON_ACTIVE_COLOR if modelo_seleccionado == "GIRASOL_SOLID" else BUTTON_INACTIVE_COLOR
    pygame.draw.rect(screen, color, pygame.Rect(30, y_offset, 180, 30), border_radius=5)
    screen.blit(font_small.render("9 - Girasol (Solid)", True, WHITE), (40, y_offset + 7)); y_offset += 45

    # Controles de visualización reasignados
    color_z = BUTTON_ACTIVE_COLOR if mostrar_wireframe else BUTTON_INACTIVE_COLOR
    pygame.draw.rect(screen, color_z, pygame.Rect(30, y_offset, 85, 30), border_radius=5)
    screen.blit(font_small.render("Z - Malla", True, WHITE), (40, y_offset + 8)); 
    
    color_x = BUTTON_ACTIVE_COLOR if mostrar_normales else BUTTON_INACTIVE_COLOR
    pygame.draw.rect(screen, color_x, pygame.Rect(125, y_offset, 85, 30), border_radius=5)
    screen.blit(font_small.render("X - Normales", True, WHITE), (130, y_offset + 8)); y_offset += 40

    y_offset += 10
    screen.blit(font_small.render("ESTADO:", True, TEXT_COLOR), (30, y_offset)); y_offset += 30
    
    screen.blit(font_small.render("Modelo:", True, TEXT_COLOR), (40, y_offset)); 
    screen.blit(font_small.render(modelo_seleccionado.replace("_", " "), True, BLUE), (120, y_offset)); y_offset += 25
    
    screen.blit(font_small.render("Visual:", True, TEXT_COLOR), (40, y_offset)); 
    screen.blit(font_small.render(modo_dibujo.upper(), True, BLUE), (120, y_offset)); y_offset += 25
    
    screen.blit(font_small.render("Malla:", True, TEXT_COLOR), (40, y_offset)); 
    screen.blit(font_small.render("ACTIVA" if mostrar_wireframe else "INACTIVA", True, RED if mostrar_wireframe else BLACK), (120, y_offset)); y_offset += 25
    
    screen.blit(font_small.render("Normales:", True, TEXT_COLOR), (40, y_offset)); 
    screen.blit(font_small.render("ACTIVO" if mostrar_normales else "INACTIVO", True, RED if mostrar_normales else BLACK), (120, y_offset))
    
    controles = ["CONTROLES:", "Flechas - Rotar Modelo", "W,A,S,D - Mover Luz X,Y", "Q,E - Mover Luz Z", "R - Resetear", "T - Ocultar/Mostrar Menú", "ESC - Salir"]
    y_controles = HEIGHT - 120 # Un poco más arriba para más controles
    for i, texto in enumerate(controles):
        color = BLACK
        texto_surface = font_small.render(texto, True, color)
        screen.blit(texto_surface, (20, y_controles + i * 20))


# --- Función Principal
def main():
    camara = Camara()
    luz = Luz(700, 250, 50) 
    
    centro_rotacion_x = WIDTH // 2 + 100 
    centro_rotacion_y = HEIGHT // 2
    centro_rotacion_z = 100
    
    main.mostrar_menu = True
    if main.mostrar_menu:
        centro_rotacion_x = (WIDTH + PANEL_WIDTH) // 2 
    
    modelos = {
        "CUBO_COMBINADO": {
            "triangulos_func": lambda: crear_cubo_simple(centro_rotacion_x - 100, centro_rotacion_y, centro_rotacion_z, 80) + \
                                       crear_piramide_simple(centro_rotacion_x + 100, centro_rotacion_y, centro_rotacion_z, 100),
            "modo": "phong", "wireframe": True, "normales": False
        },
        "CORAZON_FLAT": {
            "triangulos_func": lambda: crear_corazon(centro_rotacion_x, centro_rotacion_y, centro_rotacion_z, 150),
            "modo": "flat", "wireframe": False, "normales": True
        },
        "TREBOL_GOURAUD": {
            "triangulos_func": lambda: crear_trebol(centro_rotacion_x, centro_rotacion_y, centro_rotacion_z, 100),
            "modo": "gouraud", "wireframe": False, "normales": True
        },
        "VENTANA_PHONG": {
            "triangulos_func": lambda: crear_ventana(centro_rotacion_x, centro_rotacion_y, centro_rotacion_z, 150, 200, 30),
            "modo": "phong", "wireframe": False, "normales": True
        },
        "GIRASOL_SOLID": {
            "triangulos_func": lambda: crear_girasol(centro_rotacion_x, centro_rotacion_y, centro_rotacion_z, 40, 60, 16),
            "modo": "solido", "wireframe": False, "normales": False
        },
    }

    modelo_actual_key = "CUBO_COMBINADO"
    todos_triangulos = modelos[modelo_actual_key]["triangulos_func"]() 
    modo_dibujo = modelos[modelo_actual_key]["modo"]
    mostrar_wireframe = modelos[modelo_actual_key]["wireframe"]
    mostrar_normales = modelos[modelo_actual_key]["normales"]
    modelo_seleccionado_nombre = "CUBO + PIRÁMIDE"

    calcular_normales_vertice(todos_triangulos)
    
    angulo_rotacion_x = 0
    angulo_rotacion_y = 0
    
    clock = pygame.time.Clock()
    
    print("PRESIONA T para ocultar/mostrar el menú lateral.")
    print("Usa W,A,S,D para mover la luz en X/Y, y Q,E para mover la luz en Z.")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                elif event.key == pygame.K_t:
                    main.mostrar_menu = not main.mostrar_menu 
                    print(f"Menú: {'Visible' if main.mostrar_menu else 'Oculto'}")
                
                # Modos de sombreado
                elif event.key == pygame.K_1: modo_dibujo = "solido"; print("Modo: Sólido")
                elif event.key == pygame.K_2: modo_dibujo = "alambre"; print("Modo: Alambre")
                elif event.key == pygame.K_3: modo_dibujo = "flat"; print("Modo: FLAT")
                elif event.key == pygame.K_4: modo_dibujo = "gouraud"; print("Modo: GOURAUD")
                elif event.key == pygame.K_5: modo_dibujo = "phong"; print("Modo: PHONG") 
                
                # Selección de modelos
                elif event.key == pygame.K_6:
                    modelo_actual_key = "CORAZON_FLAT"
                    current_model_data = modelos[modelo_actual_key]
                    todos_triangulos = current_model_data["triangulos_func"]()
                    modo_dibujo = current_model_data["modo"]
                    mostrar_wireframe = current_model_data["wireframe"]
                    mostrar_normales = current_model_data["normales"]
                    modelo_seleccionado_nombre = "CORAZON_FLAT"
                    calcular_normales_vertice(todos_triangulos)
                    print("Modelo: Corazón (Flat Shading)")
                elif event.key == pygame.K_7:
                    modelo_actual_key = "TREBOL_GOURAUD"
                    current_model_data = modelos[modelo_actual_key]
                    todos_triangulos = current_model_data["triangulos_func"]()
                    modo_dibujo = current_model_data["modo"]
                    mostrar_wireframe = current_model_data["wireframe"]
                    mostrar_normales = current_model_data["normales"]
                    modelo_seleccionado_nombre = "TREBOL_GOURAUD"
                    calcular_normales_vertice(todos_triangulos)
                    print("Modelo: Trébol (Gouraud Shading)")
                elif event.key == pygame.K_8:
                    modelo_actual_key = "VENTANA_PHONG"
                    current_model_data = modelos[modelo_actual_key]
                    todos_triangulos = current_model_data["triangulos_func"]()
                    modo_dibujo = current_model_data["modo"]
                    mostrar_wireframe = current_model_data["wireframe"]
                    mostrar_normales = current_model_data["normales"]
                    modelo_seleccionado_nombre = "VENTANA_PHONG"
                    calcular_normales_vertice(todos_triangulos)
                    print("Modelo: Ventana (Phong Shading)")
                elif event.key == pygame.K_9:
                    modelo_actual_key = "GIRASOL_SOLID"
                    current_model_data = modelos[modelo_actual_key]
                    todos_triangulos = current_model_data["triangulos_func"]()
                    modo_dibujo = current_model_data["modo"]
                    mostrar_wireframe = current_model_data["wireframe"]
                    mostrar_normales = current_model_data["normales"]
                    modelo_seleccionado_nombre = "GIRASOL_SOLID"
                    calcular_normales_vertice(todos_triangulos)
                    print("Modelo: Girasol (Solid Shading)")
                
                # Controles de visualización reasignados
                elif event.key == pygame.K_z: # Antes W
                    mostrar_wireframe = not mostrar_wireframe
                    print(f"Malla de Alambre: {'ACTIVA' if mostrar_wireframe else 'INACTIVA'}")
                elif event.key == pygame.K_x: # Antes N
                    mostrar_normales = not mostrar_normales
                    print(f"Normales: {'ACTIVO' if mostrar_normales else 'INACTIVO'}")
                
                elif event.key == pygame.K_r:
                    angulo_rotacion_x = 0 
                    angulo_rotacion_y = 0
                    modelo_actual_key = "CUBO_COMBINADO"
                    current_model_data = modelos[modelo_actual_key]
                    todos_triangulos = current_model_data["triangulos_func"]()
                    modo_dibujo = current_model_data["modo"]
                    mostrar_wireframe = current_model_data["wireframe"]
                    mostrar_normales = current_model_data["normales"]
                    modelo_seleccionado_nombre = "CUBO + PIRÁMIDE"
                    calcular_normales_vertice(todos_triangulos)
                    print("Rotación y modelo reseteados")
        
        # --- Movimiento de la Luz
        keys_pressed = pygame.key.get_pressed()
        light_speed = 10

        if keys_pressed[pygame.K_a]: luz.posicion.x -= light_speed
        if keys_pressed[pygame.K_d]: luz.posicion.x += light_speed
        if keys_pressed[pygame.K_w]: luz.posicion.y -= light_speed
        if keys_pressed[pygame.K_s]: luz.posicion.y += light_speed
        if keys_pressed[pygame.K_q]: luz.posicion.z += light_speed # Acercar luz
        if keys_pressed[pygame.K_e]: luz.posicion.z -= light_speed # Alejar luz

        # Rotación del Modelo
        delta_angulo_y = 0 
        delta_angulo_x = 0 

        if keys_pressed[pygame.K_LEFT]: delta_angulo_y = -0.03
        if keys_pressed[pygame.K_RIGHT]: delta_angulo_y = 0.03
        if keys_pressed[pygame.K_UP]: delta_angulo_x = -0.03 
        if keys_pressed[pygame.K_DOWN]: delta_angulo_x = 0.03
            
        if delta_angulo_y != 0 or delta_angulo_x != 0:
            for triangulo in todos_triangulos:
                for punto in triangulo.puntos:
                    current_center_x = (WIDTH + PANEL_WIDTH) // 2 if main.mostrar_menu else WIDTH // 2 
                    current_center_y = HEIGHT // 2
                    
                    x_orig = punto.x - current_center_x
                    y_orig = punto.y - current_center_y
                    z_orig = punto.z - centro_rotacion_z # Z no se ajusta con el menú

                    if delta_angulo_y != 0:
                        cos_y = math.cos(delta_angulo_y)
                        sin_y = math.sin(delta_angulo_y)
                        temp_x = x_orig * cos_y - z_orig * sin_y
                        temp_z = x_orig * sin_y + z_orig * cos_y
                        x_orig, z_orig = temp_x, temp_z

                    if delta_angulo_x != 0:
                        cos_x = math.cos(delta_angulo_x)
                        sin_x = math.sin(delta_angulo_x)
                        temp_y = y_orig * cos_x - z_orig * sin_x
                        temp_z = y_orig * sin_x + z_orig * cos_x
                        y_orig, z_orig = temp_y, temp_z

                    punto.x = x_orig + current_center_x
                    punto.y = y_orig + current_center_y
                    punto.z = z_orig + centro_rotacion_z
        
        #Lógica de dibujo
        screen.fill(WHITE)
        
        if main.mostrar_menu:
            dibujar_panel_menu(screen, modo_dibujo, modelo_seleccionado_nombre, mostrar_wireframe, mostrar_normales)
            pygame.draw.line(screen, BLACK, (PANEL_WIDTH, 0), (PANEL_WIDTH, HEIGHT), 2)

        dibujar_ejes(screen, camara) 
        
        # Dibuja la representación de la fuente de luz
        light_pos_2d = camara.proyectar(luz.posicion)
        pygame.draw.circle(screen, YELLOW, light_pos_2d, 15) # Círculo amarillo más grande
        pygame.draw.circle(screen, BLACK, light_pos_2d, 15, 1) # Contorno negro
        # Texto con coordenadas de la luz
        font = pygame.font.Font(None, 20)
        light_text = font.render(f"Luz: ({luz.posicion.x}, {luz.posicion.y}, {luz.posicion.z})", True, BLACK)
        screen.blit(light_text, (light_pos_2d[0] + 20, light_pos_2d[1] - 10))


        # Recalcular normales de vértice si Gouraud o Phong están activos
        if modo_dibujo == "gouraud" or modo_dibujo == "phong":
            calcular_normales_vertice(todos_triangulos)

        for triangulo in todos_triangulos:
            if modo_dibujo == "solido": 
                dibujar_triangulo_solido(screen, triangulo, camara)
            elif modo_dibujo == "flat": 
                dibujar_triangulo_flat(screen, triangulo, camara, luz)
            elif modo_dibujo == "gouraud": 
                dibujar_triangulo_gouraud(screen, triangulo, camara, luz)
            elif modo_dibujo == "phong": 
                dibujar_triangulo_phong(screen, triangulo, camara, luz)
            elif modo_dibujo == "alambre":
                dibujar_triangulo_alambre(screen, triangulo, camara)
                continue 

            if mostrar_wireframe:
                dibujar_triangulo_alambre(screen, triangulo, camara)
            
            if mostrar_normales:
                dibujar_normal_cara(screen, triangulo, camara)

        font = pygame.font.Font(None, 24)
        rot_text_x = font.render(f"Rotación X: {angulo_rotacion_x:.2f} rad", True, BLACK)
        rot_text_y = font.render(f"Rotación Y: {angulo_rotacion_y:.2f} rad", True, BLACK)
        # Posición del texto de rotación ajustada para no chocar con el círculo de luz o menú
        text_x_offset = PANEL_WIDTH if main.mostrar_menu else 0
        screen.blit(rot_text_x, (text_x_offset + 20, 20)) 
        screen.blit(rot_text_y, (text_x_offset + 20, 45))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

