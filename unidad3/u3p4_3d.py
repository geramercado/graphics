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
    Objeto3D.crear_esfera(20, 6, ROJO),
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
objetos[0].trasladar(-180, 10, 0)   # Esfera roja - izquierda
objetos[1].trasladar(-70, 100, 0)    # Esfera blanco - derecha
objetos[2].trasladar(90, 0, 0)      # Esfera azul - centro
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
                objeto_seleccionado = (objeto_seleccionado + 1) % (len(objetos) - 1)  # Excluir ejes
            
            # Controles de rotación manual
            elif evento.key == pygame.K_q:  # Rotar +X
                objetos[objeto_seleccionado].rotar(5, 0, 0)
            elif evento.key == pygame.K_a:  # Rotar -X
                objetos[objeto_seleccionado].rotar(-5, 0, 0)
            elif evento.key == pygame.K_w:  # Rotar +Y
                objetos[objeto_seleccionado].rotar(0, 5, 0)
            elif evento.key == pygame.K_s:  # Rotar -Y
                objetos[objeto_seleccionado].rotar(0, -5, 0)
            elif evento.key == pygame.K_e:  # Rotar +Z
                objetos[objeto_seleccionado].rotar(0, 0, 5)
            elif evento.key == pygame.K_d:  # Rotar -Z
                objetos[objeto_seleccionado].rotar(0, 0, -5)
            
            # Modos de rotación
            elif evento.key == pygame.K_1:
                modo_rotacion = 1  # Automática
            elif evento.key == pygame.K_2:
                modo_rotacion = 2  # Manual
            elif evento.key == pygame.K_3:
                modo_rotacion = 3  # Orbital
            elif evento.key == pygame.K_4:
                modo_rotacion = 4  # Combinada
            
            # Velocidad de rotación
            elif evento.key == pygame.K_PLUS or evento.key == pygame.K_EQUALS:
                velocidad_rotacion = min(3.0, velocidad_rotacion + 0.1)
            elif evento.key == pygame.K_MINUS:
                velocidad_rotacion = max(0.1, velocidad_rotacion - 0.1)
            
            # Reset rotaciones
            elif evento.key == pygame.K_r:
                objetos[objeto_seleccionado].establecer_rotacion(0, 0, 0)
    
    # --- ANIMACIONES DE ROTACIÓN ---
    if modo_rotacion != 2:  # Si no es modo manual
        for i, objeto in enumerate(objetos):
            if i >= len(objetos) - 1:  # Saltar los ejes
                continue
                
            if modo_rotacion == 1:  # Rotación automática individual
                if i == 0:  # Cubo rojo - rotación en X
                    objeto.rotar(30 * dt * velocidad_rotacion, 0, 0)
                elif i == 1:  # Cubo verde - rotación en Y
                    objeto.rotar(0, 30 * dt * velocidad_rotacion, 0)
                elif i == 2:  # Cubo azul - rotación en Z
                    objeto.rotar(0, 0, 30 * dt * velocidad_rotacion)
                elif i == 3:  # Cubo amarillo - rotación en XYZ
                    objeto.rotar(
                        20 * dt * velocidad_rotacion,
                        25 * dt * velocidad_rotacion,
                        15 * dt * velocidad_rotacion
                    )
            
            elif modo_rotacion == 3:  # Rotación orbital (alrededor de ejes)
                # Todos los cubos orbitan alrededor de los ejes globales
                angulo_orbita = tiempo * 20 * velocidad_rotacion
                if i == 0:  # Orbita en X
                    objeto.establecer_rotacion(angulo_orbita, 0, 0)
                elif i == 1:  # Orbita en Y
                    objeto.establecer_rotacion(0, angulo_orbita, 0)
                elif i == 2:  # Orbita en Z
                    objeto.establecer_rotacion(0, 0, angulo_orbita)
                elif i == 3:  # Orbita combinada
                    objeto.establecer_rotacion(
                        angulo_orbita,
                        angulo_orbita * 1.5,
                        angulo_orbita * 0.7
                    )
            
            elif modo_rotacion == 4:  # Rotación combinada compleja
                base_angulo = tiempo * 25 * velocidad_rotacion
                if i == 0:  # Movimiento de balanceo
                    objeto.establecer_rotacion(
                        math.sin(tiempo) * 45,
                        base_angulo,
                        0
                    )
                elif i == 1:  # Movimiento de cabeceo
                    objeto.establecer_rotacion(
                        0,
                        math.cos(tiempo) * 45,
                        base_angulo
                    )
                elif i == 2:  # Movimiento de giro
                    objeto.establecer_rotacion(
                        base_angulo,
                        0,
                        math.sin(tiempo) * 45
                    )
                elif i == 3:  # Movimiento caótico
                    objeto.establecer_rotacion(
                        math.sin(tiempo * 1.3) * 60,
                        math.cos(tiempo * 1.7) * 60,
                        math.sin(tiempo * 2.1) * 60
                    )
    

    # --- MOVIMIENTO ORBITAL DE ESFERAS ROJA Y BLANCA --- --------------
    angulo_orbita = tiempo * 50 * velocidad_orbita  # velocidad de giro (ajústala a gusto)

    # Esfera roja orbitando en sentido horario
    objetos[0].posicion.x = math.cos(math.radians(angulo_orbita)) * radio_orbita
    objetos[0].posicion.z = math.sin(math.radians(angulo_orbita)) * radio_orbita
    objetos[0].posicion.y = 0  # mantener en el plano XZ
    objetos[0].actualizar_vertices()

    # Esfera blanca orbitando en sentido contrario
    objetos[1].posicion.x = math.cos(math.radians(angulo_orbita)) * 400
    objetos[1].posicion.z = math.sin(math.radians(angulo_orbita)) * 400
    objetos[1].posicion.y = 0  # mantener en el plano XZ
    objetos[1].actualizar_vertices()

    # --- MOVIMIENTO ORBITAL DE ESFERAS ROJA Y BLANCA --- --------------


    # --- DIBUJADO ---
    ventana.fill(NEGRO)
    
    # Dibujar todos los objetos
    for i, objeto in enumerate(objetos):
        if i == len(objetos) - 1:  # Ejes coordenados
            # Dibujar ejes con colores específicos
            for j, arista in enumerate(objeto.aristas):
                punto1 = objeto.vertices[arista[0]]
                punto2 = objeto.vertices[arista[1]]
                
                p1_2d = punto1.proyectar(distancia_vision)
                p2_2d = punto2.proyectar(distancia_vision)
                
                # Asignar colores a los ejes
                if j == 0: color_eje = ROJO    # Eje X
                elif j == 1: color_eje = VERDE # Eje Y
                else: color_eje = AZUL         # Eje Z
                
                pygame.draw.line(ventana, color_eje, p1_2d, p2_2d, 3)
        else:
            # Objetos normales
            color_objeto = objeto.color
            grosor_linea = 3 if i == objeto_seleccionado else 2
            
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
                color_punto = MORADO if i == objeto_seleccionado else BLANCO
                pygame.draw.circle(ventana, color_punto, (x2d, y2d), 3)
    
    # --- INFORMACIÓN EN PANTALLA ---
    fuente = pygame.font.SysFont('Arial', 18)
    modos_rotacion = ["", "AUTOMÁTICA", "MANUAL", "ORBITAL", "COMBINADA"]
    
    info_textos = [
        f"Objeto {objeto_seleccionado + 1}/4 - Modo: {modos_rotacion[modo_rotacion]}",
        f"Rotación: ({objetos[objeto_seleccionado].rotacion.x:.1f}°, "
        f"{objetos[objeto_seleccionado].rotacion.y:.1f}°, "
        f"{objetos[objeto_seleccionado].rotacion.z:.1f}°)",
        f"Velocidad: {velocidad_rotacion:.1f}x",
        "",
        "CONTROLES ROTACIÓN:",
        "Q/A: Rotar eje X, W/S: Rotar eje Y, E/D: Rotar eje Z",
        "1-4: Modos rotación, +/-: Velocidad, R: Reset",
        "TAB: Cambiar objeto, ↑↓: Zoom cámara"
    ]
    
    for i, texto in enumerate(info_textos):
        render = fuente.render(texto, True, BLANCO)
        ventana.blit(render, (10, 10 + i * 22))
    
    # --- LEYENDA DE EJES ---
    leyenda_x = fuente.render("X: Rojo", True, ROJO)
    leyenda_y = fuente.render("Y: Verde", True, VERDE)
    leyenda_z = fuente.render("Z: Azul", True, AZUL)
    
    ventana.blit(leyenda_x, (ANCHO - 100, 20))
    ventana.blit(leyenda_y, (ANCHO - 100, 45))
    ventana.blit(leyenda_z, (ANCHO - 100, 70))
    
    # --- ACTUALIZAR PANTALLA ---
    pygame.display.flip()

# Finalizar
pygame.quit()
