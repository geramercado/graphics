# Importar bibliotecas
#Gerardo Mercado Hurtado
#Raul Martinez Martinez
import pygame
import math

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Clase 3: Transformaciones 3D - Traslación y Escalamiento")
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

class Objeto3D:
    def __init__(self, vertices, aristas, color=BLANCO):
        self.vertices_originales = vertices  # Guardar original para transformaciones
        self.vertices = [v.copiar() for v in vertices]  # Copia para trabajar
        self.aristas = aristas
        self.color = color
        self.posicion = Punto3D(0, 0, 0)  # Posición actual
        self.escala = Punto3D(1, 1, 1)    # Escala actual
    
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
    
    def escalar_uniforme(self, factor):
        """Escala manteniendo proporciones"""
        self.escalar(factor, factor, factor)
    
    def reset_transformaciones(self):
        """Vuelve al estado original"""
        self.posicion = Punto3D(0, 0, 0)
        self.escala = Punto3D(1, 1, 1)
        self.actualizar_vertices()
    
    def actualizar_vertices(self):
        """Aplica todas las transformaciones a los vértices"""
        for i, vertice_original in enumerate(self.vertices_originales):
            # Aplicar escala
            x = vertice_original.x * self.escala.x
            y = vertice_original.y * self.escala.y
            z = vertice_original.z * self.escala.z
            
            # Aplicar traslación
            self.vertices[i].x = x + self.posicion.x
            self.vertices[i].y = y + self.posicion.y
            self.vertices[i].z = z + self.posicion.z

class Transformador3D:
    """Clase para aplicar transformaciones a objetos"""
    
    @staticmethod
    def crear_escena_demo():
        """Crea una escena de demostración con múltiples objetos"""
        return [
            Objeto3D.crear_cubo(60, ROJO),
            Objeto3D.crear_cubo(40, VERDE),
            Objeto3D.crear_cubo(50, AZUL),
            Objeto3D.crear_cubo(35, AMARILLO)
        ]

# Crear escena inicial
objetos = Transformador3D.crear_escena_demo()

# Configurar posiciones iniciales
# objetos[0].trasladar(-150, 0, 0)     # Cubo rojo a la izquierda
# objetos[1].trasladar(150, 0, 0)      # Cubo verde a la derecha
# objetos[2].trasladar(0, -100, 100)   # Cubo azul abajo-atrás
# objetos[3].trasladar(0, 100, -100)   # Cubo amarillo arriba-adelante

# Configurar posiciones iniciales (ligeramente separadas)
objetos[0].trasladar(0, 0, 0)
objetos[1].trasladar(10, 0, 0)
objetos[2].trasladar(0, 10, 0)
objetos[3].trasladar(0, 0, 10)


# Variables de control
distancia_vision = 500
mostrar_ejes = True
objeto_seleccionado = 0
tiempo = 0
modo_animacion = 1  # 1=Traslación, 2=Escalamiento, 3=Combinada

# Bucle principal
ejecutando = True
while ejecutando:
    # Control de tiempo
    dt = reloj.tick(60) / 1000.0
    tiempo += dt
    
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
            
            # Cambiar objeto seleccionado
            elif evento.key == pygame.K_TAB:
                objeto_seleccionado = (objeto_seleccionado + 1) % len(objetos)
            
            # Controles de traslación
            elif evento.key == pygame.K_w:  # Adelante
                objetos[objeto_seleccionado].trasladar(0, 0, -20)
            elif evento.key == pygame.K_s:  # Atrás
                objetos[objeto_seleccionado].trasladar(0, 0, 20)
            elif evento.key == pygame.K_a:  # Izquierda
                objetos[objeto_seleccionado].trasladar(-20, 0, 0)
            elif evento.key == pygame.K_d:  # Derecha
                objetos[objeto_seleccionado].trasladar(20, 0, 0)
            elif evento.key == pygame.K_q:  # Arriba
                objetos[objeto_seleccionado].trasladar(0, -20, 0)
            elif evento.key == pygame.K_e:  # Abajo
                objetos[objeto_seleccionado].trasladar(0, 20, 0)

            
            # Controles de escalamiento
            elif evento.key == pygame.K_z:  # Agrandar
                objetos[objeto_seleccionado].escalar_uniforme(1.2)
            elif evento.key == pygame.K_x:  # Reducir
                objetos[objeto_seleccionado].escalar_uniforme(0.8)
            elif evento.key == pygame.K_c:  # Alargar en Y
                objetos[objeto_seleccionado].escalar(1, 1.2, 1)
            elif evento.key == pygame.K_v:  # Aplanar en Y
                objetos[objeto_seleccionado].escalar(1, 0.8, 1)
            
            # Reset y modos
            elif evento.key == pygame.K_r:  # Reset
                objetos[objeto_seleccionado].reset_transformaciones()
            elif evento.key == pygame.K_1:  # Modo traslación
                modo_animacion = 1
            elif evento.key == pygame.K_2:  # Modo escalamiento
                modo_animacion = 2
            elif evento.key == pygame.K_3:  # Modo combinado
                modo_animacion = 3
            elif evento.key == pygame.K_4:  # Modo manual
                modo_animacion = 0
    
    # --- ANIMACIONES AUTOMÁTICAS ---
    # --- ANIMACIÓN CARRERA ---


#    if modo_animacion != 0:
#        for i, objeto in enumerate(objetos):
#            if modo_animacion == 1:  # Traslación
#                if i == 0:  # Cubo rojo - círculo horizontal
#                    objeto.trasladar(math.cos(tiempo) * 2, 0, math.sin(tiempo) * 2)
#                elif i == 1:  # Cubo verde - línea vertical
#                    objeto.trasladar(0, math.sin(tiempo * 2) * 3, 0)
#                elif i == 2:  # Cubo azul - diagonal
#                    objeto.trasladar(math.sin(tiempo) * 2, math.cos(tiempo) * 2, 0)

            if modo_animacion == 1:  # Modo traslación = carrera
                    # Parámetros de la trayectoria
                    radio = 200
                    velocidad = 2
                    desfase = 0.5  # Retraso entre cada cubo
                    
                    for i, objeto in enumerate(objetos):
                        # Cada cubo sigue al anterior con un desfase en tiempo
                        t = tiempo * velocidad - i * desfase
                        x = math.cos(t) * radio
                        y = math.sin(t) * 50  # Onda vertical leve
                        z = math.sin(t) * radio
                        
                        # Actualizar posición
                        objeto.posicion.x = x
                        objeto.posicion.y = y
                        objeto.posicion.z = z
                        objeto.actualizar_vertices()
            
            elif modo_animacion == 2:  # Escalamiento
                if i == 0:  # Pulso uniforme
                    escala = 1 + math.sin(tiempo * 2) * 0.3
                    objeto.escalar_uniforme(escala / objeto.escala.x)
                elif i == 1:  # Aplastamiento vertical
                    escala_y = 1 + math.sin(tiempo * 3) * 0.5
                    objeto.escalar(1, escala_y / objeto.escala.y, 1)
            
            elif modo_animacion == 3:  # Combinado
                if i == 0:  # Traslación + escalamiento
                    objeto.trasladar(math.cos(tiempo) * 1.5, 0, 0)
                    escala = 1 + math.sin(tiempo * 2) * 0.2
                    objeto.escalar_uniforme(escala / objeto.escala.x)
    
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
            color_objeto = MORADO
            grosor_linea = 3
        else:
            grosor_linea = 2
        
        # Dibujar aristas del objeto
        for arista in objeto.aristas:
            punto1 = objeto.vertices[arista[0]]
            punto2 = objeto.vertices[arista[1]]
            
            p1_2d = punto1.proyectar(distancia_vision)
            p2_2d = punto2.proyectar(distancia_vision)
            
            pygame.draw.line(ventana, color_objeto, p1_2d, p2_2d, grosor_linea)
        
        # Dibujar vértices como puntos
        for vertice in objeto.vertices:
            x2d, y2d = vertice.proyectar(distancia_vision)
            pygame.draw.circle(ventana, BLANCO, (x2d, y2d), 3)
        
        # Dibujar información del objeto
        if i == objeto_seleccionado:
            x2d, y2d = objeto.vertices[0].proyectar(distancia_vision)
            fuente_pequena = pygame.font.SysFont('Arial', 12)
            info = f"Pos:({objeto.posicion.x:.0f},{objeto.posicion.y:.0f},{objeto.posicion.z:.0f})"
            info += f" Esc:({objeto.escala.x:.1f},{objeto.escala.y:.1f},{objeto.escala.z:.1f})"
            texto = fuente_pequena.render(info, True, BLANCO)
            ventana.blit(texto, (x2d - 60, y2d - 20))
    
    # --- INFORMACIÓN EN PANTALLA ---
    fuente = pygame.font.SysFont('Arial', 20)
    modos = ["MANUAL", "TRASLACIÓN", "ESCALAMIENTO", "COMBINADO"]
    
    info_textos = [
        f"Objeto {objeto_seleccionado + 1}/{len(objetos)} - Modo: {modos[modo_animacion]}",
        f"Posición: ({objetos[objeto_seleccionado].posicion.x:.0f}, "
        f"{objetos[objeto_seleccionado].posicion.y:.0f}, "
        f"{objetos[objeto_seleccionado].posicion.z:.0f})",
        f"Escala: ({objetos[objeto_seleccionado].escala.x:.1f}, "
        f"{objetos[objeto_seleccionado].escala.y:.1f}, "
        f"{objetos[objeto_seleccionado].escala.z:.1f})",
        "",
        "CONTROLES MANUALES:",
        "WASD QE: Mover objeto (3D)",
        "Z/X: Escalar uniforme, C/V: Escalar en Y",
        "TAB: Cambiar objeto, R: Reset objeto",
        "1-4: Modos animación, ↑↓: Zoom cámara"
    ]
    
    for i, texto in enumerate(info_textos):
        render = fuente.render(texto, True, BLANCO)
        ventana.blit(render, (10, 10 + i * 25))
    
    # --- ACTUALIZAR PANTALLA ---
    pygame.display.flip()

# Finalizar
pygame.quit()
