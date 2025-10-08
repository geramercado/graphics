#Importar bibliotecas necesarias
import pygame
import math

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ANCHO, ALTO = 1000, 700
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Clase 5: Sesgado y Matrices de Transformación 3D")
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
ROSA = (255, 182, 193)

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
        return Punto3D(self.x, self.y, self.z)
    
    def __str__(self):
        return f"({self.x:.1f}, {self.y:.1f}, {self.z:.1f})"

class MatrizTransformacion:
    """Clase para manejar matrices de transformación 4x4"""
    
    @staticmethod
    def identidad():
        """Retorna matriz identidad 4x4"""
        return [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
    
    @staticmethod
    def traslacion(dx, dy, dz):
        """Matriz de traslación"""
        return [
            [1, 0, 0, dx],
            [0, 1, 0, dy],
            [0, 0, 1, dz],
            [0, 0, 0, 1]
        ]
    
    @staticmethod
    def escalamiento(sx, sy, sz):
        """Matriz de escalamiento"""
        return [
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ]
    
    @staticmethod
    def rotacion_x(angulo):
        """Matriz de rotación alrededor del eje X"""
        rad = math.radians(angulo)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        return [
            [1, 0, 0, 0],
            [0, cos_a, -sin_a, 0],
            [0, sin_a, cos_a, 0],
            [0, 0, 0, 1]
        ]
    
    @staticmethod
    def rotacion_y(angulo):
        """Matriz de rotación alrededor del eje Y"""
        rad = math.radians(angulo)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        return [
            [cos_a, 0, sin_a, 0],
            [0, 1, 0, 0],
            [-sin_a, 0, cos_a, 0],
            [0, 0, 0, 1]
        ]
    
    @staticmethod
    def rotacion_z(angulo):
        """Matriz de rotación alrededor del eje Z"""
        rad = math.radians(angulo)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        return [
            [cos_a, -sin_a, 0, 0],
            [sin_a, cos_a, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
    
    @staticmethod
    def sesgado_xy(factor):
        """Matriz de sesgado en plano XY (inclinar en Z)"""
        return [
            [1, 0, factor, 0],
            [0, 1, factor, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
    
    @staticmethod
    def sesgado_xz(factor):
        """Matriz de sesgado en plano XZ (inclinar en Y)"""
        return [
            [1, factor, 0, 0],
            [0, 1, 0, 0],
            [0, factor, 1, 0],
            [0, 0, 0, 1]
        ]
    
    @staticmethod
    def sesgado_yz(factor):
        """Matriz de sesgado en plano YZ (inclinar en X)"""
        return [
            [1, 0, 0, 0],
            [factor, 1, 0, 0],
            [factor, 0, 1, 0],
            [0, 0, 0, 1]
        ]
    
    @staticmethod
    def multiplicar_matrices(a, b):
        """Multiplica dos matrices 4x4"""
        result = [[0 for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    result[i][j] += a[i][k] * b[k][j]
        return result
    
    @staticmethod
    def transformar_punto(punto, matriz):
        """Aplica matriz de transformación a un punto 3D"""
        # Convertir punto a coordenadas homogéneas [x, y, z, 1]
        x = punto.x * matriz[0][0] + punto.y * matriz[0][1] + punto.z * matriz[0][2] + matriz[0][3]
        y = punto.x * matriz[1][0] + punto.y * matriz[1][1] + punto.z * matriz[1][2] + matriz[1][3]
        z = punto.x * matriz[2][0] + punto.y * matriz[2][1] + punto.z * matriz[2][2] + matriz[2][3]
        # w = punto.x * matriz[3][0] + punto.y * matriz[3][1] + punto.z * matriz[3][2] + matriz[3][3]
        
        return Punto3D(x, y, z)

class Objeto3D:
    def __init__(self, vertices, aristas, color=BLANCO):
        self.vertices_originales = vertices
        self.vertices = [v.copiar() for v in vertices]
        self.aristas = aristas
        self.color = color
        
        # Transformaciones actuales
        self.posicion = Punto3D(0, 0, 0)
        self.escala = Punto3D(1, 1, 1)
        self.rotacion = Punto3D(0, 0, 0)
        self.sesgado = Punto3D(0, 0, 0)  # Factores de sesgado para XY, XZ, YZ
    
    @staticmethod
    def crear_cubo(tamaño=100, color=BLANCO):
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
    
    @staticmethod
    def crear_piramide(tamaño_base=80, altura=120, color=VERDE):
        vertices = [
            Punto3D(-tamaño_base, -tamaño_base, -tamaño_base),
            Punto3D(tamaño_base, -tamaño_base, -tamaño_base),
            Punto3D(tamaño_base, -tamaño_base, tamaño_base),
            Punto3D(-tamaño_base, -tamaño_base, tamaño_base),
            Punto3D(0, -altura, 0)
        ]
        
        aristas = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Base
            (0, 4), (1, 4), (2, 4), (3, 4)   # Lados
        ]
        
        return Objeto3D(vertices, aristas, color)
    
    def trasladar(self, dx, dy, dz):
        self.posicion.x += dx
        self.posicion.y += dy
        self.posicion.z += dz
        self.actualizar_con_matrices()
    
    def escalar(self, sx, sy, sz):
        self.escala.x *= sx
        self.escala.y *= sy
        self.escala.z *= sz
        self.actualizar_con_matrices()
    
    def rotar(self, dx, dy, dz):
        self.rotacion.x = (self.rotacion.x + dx) % 360
        self.rotacion.y = (self.rotacion.y + dy) % 360
        self.rotacion.z = (self.rotacion.z + dz) % 360
        self.actualizar_con_matrices()
    
    def sesgar(self, tipo, factor):
        """Aplica sesgado: 0=XY, 1=XZ, 2=YZ"""
        if tipo == 0:  # Sesgado XY
            self.sesgado.x += factor
        elif tipo == 1:  # Sesgado XZ
            self.sesgado.y += factor
        elif tipo == 2:  # Sesgado YZ
            self.sesgado.z += factor
        self.actualizar_con_matrices()
    
    def reset_sesgado(self):
        self.sesgado = Punto3D(0, 0, 0)
        self.actualizar_con_matrices()
    
    def actualizar_con_matrices(self):
        """Aplica todas las transformaciones usando matrices"""
        # Matriz identidad inicial
        matriz_final = MatrizTransformacion.identidad()
        
        # Aplicar transformaciones en orden (escala -> rotación -> sesgado -> traslación)
        
        # 1. Escalamiento
        matriz_escala = MatrizTransformacion.escalamiento(
            self.escala.x, self.escala.y, self.escala.z
        )
        matriz_final = MatrizTransformacion.multiplicar_matrices(matriz_final, matriz_escala)
        
        # 2. Rotación (orden Z, Y, X)
        if self.rotacion.z != 0:
            matriz_rot_z = MatrizTransformacion.rotacion_z(self.rotacion.z)
            matriz_final = MatrizTransformacion.multiplicar_matrices(matriz_final, matriz_rot_z)
        
        if self.rotacion.y != 0:
            matriz_rot_y = MatrizTransformacion.rotacion_y(self.rotacion.y)
            matriz_final = MatrizTransformacion.multiplicar_matrices(matriz_final, matriz_rot_y)
        
        if self.rotacion.x != 0:
            matriz_rot_x = MatrizTransformacion.rotacion_x(self.rotacion.x)
            matriz_final = MatrizTransformacion.multiplicar_matrices(matriz_final, matriz_rot_x)
        
        # 3. Sesgado
        if self.sesgado.x != 0:  # Sesgado XY
            matriz_sesgado_xy = MatrizTransformacion.sesgado_xy(self.sesgado.x)
            matriz_final = MatrizTransformacion.multiplicar_matrices(matriz_final, matriz_sesgado_xy)
        
        if self.sesgado.y != 0:  # Sesgado XZ
            matriz_sesgado_xz = MatrizTransformacion.sesgado_xz(self.sesgado.y)
            matriz_final = MatrizTransformacion.multiplicar_matrices(matriz_final, matriz_sesgado_xz)
        
        if self.sesgado.z != 0:  # Sesgado YZ
            matriz_sesgado_yz = MatrizTransformacion.sesgado_yz(self.sesgado.z)
            matriz_final = MatrizTransformacion.multiplicar_matrices(matriz_final, matriz_sesgado_yz)
        
        # 4. Traslación
        matriz_traslacion = MatrizTransformacion.traslacion(
            self.posicion.x, self.posicion.y, self.posicion.z
        )
        matriz_final = MatrizTransformacion.multiplicar_matrices(matriz_final, matriz_traslacion)
        
        # Aplicar matriz final a todos los vértices
        for i, vertice_original in enumerate(self.vertices_originales):
            self.vertices[i] = MatrizTransformacion.transformar_punto(vertice_original, matriz_final)

# Crear escena de demostración
objetos = [
    Objeto3D.crear_cubo(80, ROJO),
    Objeto3D.crear_cubo(60, VERDE),
    Objeto3D.crear_piramide(70, 100, AZUL),
    Objeto3D.crear_cubo(50, AMARILLO),
]

# Configurar posiciones iniciales
objetos[0].trasladar(-200, 0, 0)    # Cubo rojo - izquierda
objetos[1].trasladar(200, 0, 0)     # Cubo verde - derecha
objetos[2].trasladar(0, -150, 0)    # Pirámide azul - abajo
objetos[3].trasladar(0, 150, 0)     # Cubo amarillo - arriba

# Variables de control
distancia_vision = 500
objeto_seleccionado = 0
tiempo = 0
modo_animacion = 1  # 1=Rotación, 2=Sesgado, 3=Combinado, 4=Manual
mostrar_info_matriz = False

# Bucle principal
ejecutando = True
while ejecutando:
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
            
            # Controles de transformación manual
            elif evento.key == pygame.K_w:  # Rotar +Y
                objetos[objeto_seleccionado].rotar(0, 5, 0)
            elif evento.key == pygame.K_s:  # Rotar -Y
                objetos[objeto_seleccionado].rotar(0, -5, 0)
            elif evento.key == pygame.K_a:  # Rotar -X
                objetos[objeto_seleccionado].rotar(-5, 0, 0)
            elif evento.key == pygame.K_d:  # Rotar +X
                objetos[objeto_seleccionado].rotar(5, 0, 0)
            elif evento.key == pygame.K_q:  # Rotar +Z
                objetos[objeto_seleccionado].rotar(0, 0, 5)
            elif evento.key == pygame.K_e:  # Rotar -Z
                objetos[objeto_seleccionado].rotar(0, 0, -5)
            
            # Controles de sesgado
            elif evento.key == pygame.K_1:  # Sesgado XY +
                objetos[objeto_seleccionado].sesgar(0, 0.1)
            elif evento.key == pygame.K_2:  # Sesgado XY -
                objetos[objeto_seleccionado].sesgar(0, -0.1)
            elif evento.key == pygame.K_3:  # Sesgado XZ +
                objetos[objeto_seleccionado].sesgar(1, 0.1)
            elif evento.key == pygame.K_4:  # Sesgado XZ -
                objetos[objeto_seleccionado].sesgar(1, -0.1)
            elif evento.key == pygame.K_5:  # Sesgado YZ +
                objetos[objeto_seleccionado].sesgar(2, 0.1)
            elif evento.key == pygame.K_6:  # Sesgado YZ -
                objetos[objeto_seleccionado].sesgar(2, -0.1)
            
            # Reset sesgado
            elif evento.key == pygame.K_r:
                objetos[objeto_seleccionado].reset_sesgado()
            
            # Modos de animación
            elif evento.key == pygame.K_F1:
                modo_animacion = 1  # Rotación
            elif evento.key == pygame.K_F2:
                modo_animacion = 2  # Sesgado
            elif evento.key == pygame.K_F3:
                modo_animacion = 3  # Combinado
            elif evento.key == pygame.K_F4:
                modo_animacion = 4  # Manual
            
            # Mostrar información de matriz
            elif evento.key == pygame.K_m:
                mostrar_info_matriz = not mostrar_info_matriz
    
    # --- ANIMACIONES AUTOMÁTICAS ---
    if modo_animacion != 4:  # Si no es modo manual
        for i, objeto in enumerate(objetos):
            if modo_animacion == 1:  # Rotación pura
                if i == 0:  # Cubo rojo - rotación en X
                    objeto.rotar(30 * dt, 0, 0)
                elif i == 1:  # Cubo verde - rotación en Y
                    objeto.rotar(0, 25 * dt, 0)
                elif i == 2:  # Pirámide azul - rotación en Z
                    objeto.rotar(0, 0, 20 * dt)
                elif i == 3:  # Cubo amarillo - rotación XYZ
                    objeto.rotar(15 * dt, 20 * dt, 10 * dt)
            
            elif modo_animacion == 2:  # Sesgado puro
                if i == 0:  # Sesgado XY oscilante
                    objeto.sesgar(0, math.sin(tiempo * 2) * 0.05)
                elif i == 1:  # Sesgado XZ oscilante
                    objeto.sesgar(1, math.cos(tiempo * 1.5) * 0.05)
                elif i == 2:  # Sesgado YZ oscilante
                    objeto.sesgar(2, math.sin(tiempo * 3) * 0.03)
                elif i == 3:  # Sesgado combinado
                    objeto.sesgar(0, math.sin(tiempo) * 0.02)
                    objeto.sesgar(1, math.cos(tiempo * 1.2) * 0.02)
            
            elif modo_animacion == 3:  # Combinado (rotación + sesgado)
                if i == 0:  # Rotación X + Sesgado XY
                    objeto.rotar(25 * dt, 0, 0)
                    objeto.sesgar(0, math.sin(tiempo * 2) * 0.03)
                elif i == 1:  # Rotación Y + Sesgado XZ
                    objeto.rotar(0, 20 * dt, 0)
                    objeto.sesgar(1, math.cos(tiempo * 1.8) * 0.04)
                elif i == 2:  # Rotación Z + Sesgado YZ
                    objeto.rotar(0, 0, 15 * dt)
                    objeto.sesgar(2, math.sin(tiempo * 2.5) * 0.02)
                elif i == 3:  # Combinación compleja
                    objeto.rotar(10 * dt, 15 * dt, 5 * dt)
                    objeto.sesgar(0, math.sin(tiempo * 1.3) * 0.02)
                    objeto.sesgar(1, math.cos(tiempo * 1.7) * 0.02)
    
    # --- DIBUJADO ---
    ventana.fill(NEGRO)
    
    # Dibujar ejes coordenados
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
    
    # --- INFORMACIÓN EN PANTALLA ---
    fuente = pygame.font.SysFont('Arial', 16)
    modos_animacion = ["", "ROTACIÓN", "SESGADO", "COMBINADO", "MANUAL"]
    
    info_textos = [
        f"Objeto {objeto_seleccionado + 1}/{len(objetos)} - Modo: {modos_animacion[modo_animacion]}",
        f"Posición: ({objetos[objeto_seleccionado].posicion.x:.0f}, "
        f"{objetos[objeto_seleccionado].posicion.y:.0f}, "
        f"{objetos[objeto_seleccionado].posicion.z:.0f})",
        f"Rotación: ({objetos[objeto_seleccionado].rotacion.x:.1f}°, "
        f"{objetos[objeto_seleccionado].rotacion.y:.1f}°, "
        f"{objetos[objeto_seleccionado].rotacion.z:.1f}°)",
        f"Sesgado: XY={objetos[objeto_seleccionado].sesgado.x:.2f}, "
        f"XZ={objetos[objeto_seleccionado].sesgado.y:.2f}, "
        f"YZ={objetos[objeto_seleccionado].sesgado.z:.2f}",
        "",
        "CONTROLES MANUALES:",
        "W/S: Rotar Y, A/D: Rotar X, Q/E: Rotar Z",
        "1/2: Sesgado XY, 3/4: Sesgado XZ, 5/6: Sesgado YZ",
        "R: Reset sesgado, TAB: Cambiar objeto",
        "F1-F4: Modos animación, M: Info matriz",
        "↑↓: Zoom cámara"
    ]
    
    for i, texto in enumerate(info_textos):
        render = fuente.render(texto, True, BLANCO)
        ventana.blit(render, (10, 10 + i * 20))
    
    # --- INFORMACIÓN DE MATRICES (OPCIONAL) ---
    if mostrar_info_matriz:
        fuente_matriz = pygame.font.SysFont('Arial', 12)
        texto_matriz = fuente_matriz.render(
            f"Transformaciones aplicadas con matrices 4x4 - "
            f"Orden: Escala → Rotación → Sesgado → Traslación", 
            True, CIAN
        )
        ventana.blit(texto_matriz, (10, ALTO - 30))
    
    # --- LEYENDA DE SESGADO ---
    leyenda = pygame.font.SysFont('Arial', 14)
    ventana.blit(leyenda.render("SESGADO XY: Inclinar en Z", True, ROSA), (ANCHO - 200, 20))
    ventana.blit(leyenda.render("SESGADO XZ: Inclinar en Y", True, ROSA), (ANCHO - 200, 40))
    ventana.blit(leyenda.render("SESGADO YZ: Inclinar en X", True, ROSA), (ANCHO - 200, 60))
    
    # --- ACTUALIZAR PANTALLA ---
    pygame.display.flip()

# Finalizar
pygame.quit()