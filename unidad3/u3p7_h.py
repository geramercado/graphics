# importar bibliotecas necesarias
import pygame
import math

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ANCHO, ALTO = 1000, 700
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Clase 7: Superficies y Caras - De Wireframe a Volumen 3D")
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
GRIS = (128, 128, 128)
ROSA = (255, 182, 193)

# Colores para materiales
COLOR_MADERA = (139, 69, 19)
COLOR_METAL = (192, 192, 192)
COLOR_VIDRIO = (200, 230, 255, 150)  # Con alpha para transparencia
COLOR_PIEDRA = (120, 120, 120)
COLOR_TELA = (200, 100, 100)

class Punto3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def copiar(self):
        return Punto3D(self.x, self.y, self.z)
    
    def __str__(self):
        return f"({self.x:.1f}, {self.y:.1f}, {self.z:.1f})"
    
    def restar(self, otro):
        return Punto3D(self.x - otro.x, self.y - otro.y, self.z - otro.z)
    
    def producto_cruz(self, otro):
        """Producto cruz entre dos vectores"""
        return Punto3D(
            self.y * otro.z - self.z * otro.y,
            self.z * otro.x - self.x * otro.z,
            self.x * otro.y - self.y * otro.x
        )
    
    def normalizar(self):
        """Normaliza el vector a longitud 1"""
        longitud = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        if longitud == 0:
            return Punto3D(0, 0, 0)
        return Punto3D(self.x/longitud, self.y/longitud, self.z/longitud)

class Cara:
    """Representa una cara poligonal en 3D"""
    def __init__(self, indices_vertices, color, objeto_padre=None):
        self.indices_vertices = indices_vertices
        self.color = color
        self.objeto_padre = objeto_padre
        self.normal = None
        self.centro = None
        
    
    def establecer_objeto_padre(self, objeto_padre):
        """Establece el objeto padre y calcula la normal"""
        self.objeto_padre = objeto_padre
        self.calcular_normal()
    
    def calcular_normal(self):
        """Calcula la normal de la cara usando producto cruz"""
        if len(self.indices_vertices) < 3 or self.objeto_padre is None:
            self.normal = Punto3D(0, 0, 0)
            return
        
        # Obtener los primeros 3 vértices
        v0 = self.objeto_padre.vertices[self.indices_vertices[0]]
        v1 = self.objeto_padre.vertices[self.indices_vertices[1]]
        v2 = self.objeto_padre.vertices[self.indices_vertices[2]]
        
        # Calcular dos vectores en el plano de la cara
        vector1 = v1.restar(v0)
        vector2 = v2.restar(v0)
        
        # Producto cruz para obtener la normal
        self.normal = vector1.producto_cruz(vector2).normalizar()
        
        # Calcular centro de la cara
        self.calcular_centro()
    
    def calcular_centro(self):
        """Calcula el centro de la cara"""
        if self.objeto_padre is None:
            return
            
        suma_x = suma_y = suma_z = 0
        for indice in self.indices_vertices:
            vertice = self.objeto_padre.vertices[indice]
            suma_x += vertice.x
            suma_y += vertice.y
            suma_z += vertice.z
        
        num_vertices = len(self.indices_vertices)
        self.centro = Punto3D(
            suma_x / num_vertices,
            suma_y / num_vertices,
            suma_z / num_vertices
        )
    
    def es_visible(self, punto_vista):
        """Determina si la cara es visible desde el punto de vista"""
        if not self.normal or not self.centro:
            return True
        
        # Vector desde el centro de la cara al punto de vista
        vector_vista = punto_vista.restar(self.centro).normalizar()
        
        # Producto punto entre normal y vector de vista
        producto_punto = (self.normal.x * vector_vista.x + 
                         self.normal.y * vector_vista.y + 
                         self.normal.z * vector_vista.z)
        
        # Si el producto punto es positivo, la cara es visible
        return producto_punto > 0

class Objeto3D:
    """Objeto 3D con caras sólidas"""
    def __init__(self, vertices, caras, color_base=BLANCO, nombre=""):
        self.vertices_originales = vertices
        self.vertices = [v.copiar() for v in vertices]
        self.caras = caras
        self.color_base = color_base
        self.nombre = nombre
        self.posicion = Punto3D(0, 0, 0)
        self.escala = Punto3D(1, 1, 1)
        self.rotacion = Punto3D(0, 0, 0)
        
        # Actualizar referencias de las caras
        for cara in self.caras:
            cara.establecer_objeto_padre(self)
    
    @staticmethod
    def crear_cubo(tamaño=100, color=BLANCO, nombre=""):
        """Crea un cubo con caras sólidas"""
        vertices = []
        for dx in [-tamaño, tamaño]:
            for dy in [-tamaño, tamaño]:
                for dz in [-tamaño, tamaño]:
                    vertices.append(Punto3D(dx, dy, dz))
        
        # Definir caras (cada cara es una lista de índices de vértices)
        caras = [
            Cara([0, 1, 3, 2], color),  # Cara trasera
            Cara([4, 5, 7, 6], color),  # Cara delantera
            Cara([0, 4, 6, 2], color),  # Cara izquierda
            Cara([1, 5, 7, 3], color),  # Cara derecha
            Cara([0, 1, 5, 4], color),  # Cara inferior
            Cara([2, 3, 7, 6], color),  # Cara superior
        ]
        
        return Objeto3D(vertices, caras, color, nombre)
    
    @staticmethod
    def crear_piramide(tamaño_base=80, altura=120, color=VERDE, nombre=""):
        """Crea una pirámide con caras sólidas"""
        vertices = [
            Punto3D(-tamaño_base, tamaño_base, -tamaño_base),   # 0: base atrás-izq
            Punto3D(tamaño_base, tamaño_base, -tamaño_base),    # 1: base atrás-der
            Punto3D(tamaño_base, tamaño_base, tamaño_base),     # 2: base adelante-der
            Punto3D(-tamaño_base, tamaño_base, tamaño_base),    # 3: base adelante-izq
            Punto3D(0, -altura, 0)                             # 4: vértice superior
        ]
        
        caras = [
            Cara([0, 1, 2, 3], color),  # Base
            Cara([0, 4, 1], color),     # Cara trasera
            Cara([1, 4, 2], color),     # Cara derecha
            Cara([2, 4, 3], color),     # Cara frontal
            Cara([3, 4, 0], color),     # Cara izquierda
        ]
        
        return Objeto3D(vertices, caras, color, nombre)
    
    @staticmethod
    def crear_esfera(radio=50, divisiones=8, color=AZUL, nombre=""):
        """Crea una esfera aproximada con caras"""
        vertices = []
        caras = []
        
        # Generar vértices
        for i in range(divisiones + 1):
            latitud = math.pi * i / divisiones  # 0 a PI
            for j in range(divisiones):
                longitud = 2 * math.pi * j / divisiones  # 0 a 2PI
                
                x = radio * math.sin(latitud) * math.cos(longitud)
                y = radio * math.cos(latitud)
                z = radio * math.sin(latitud) * math.sin(longitud)
                
                vertices.append(Punto3D(x, y, z))
        
        # Generar caras (triángulos)
        for i in range(divisiones):
            for j in range(divisiones):
                # Cuadrante actual
                v0 = i * divisiones + j
                v1 = i * divisiones + (j + 1) % divisiones
                v2 = (i + 1) * divisiones + j
                v3 = (i + 1) * divisiones + (j + 1) % divisiones
                
                # Dos triángulos por cuadrante
                if i > 0:  # Triángulo superior
                    caras.append(Cara([v0, v1, v2], color))
                if i < divisiones - 1:  # Triángulo inferior
                    caras.append(Cara([v1, v3, v2], color))
        
        return Objeto3D(vertices, caras, color, nombre)
    
    @staticmethod
    def crear_cilindro(radio=40, altura=80, divisiones=12, color=ROJO, nombre=""):
        """Crea un cilindro con caras"""
        vertices = []
        caras = []
        
        # Vértices de la tapa superior
        for i in range(divisiones):
            angulo = 2 * math.pi * i / divisiones
            x = radio * math.cos(angulo)
            z = radio * math.sin(angulo)
            vertices.append(Punto3D(x, -altura/2, z))  # Superior
        
        # Vértices de la tapa inferior
        for i in range(divisiones):
            angulo = 2 * math.pi * i / divisiones
            x = radio * math.cos(angulo)
            z = radio * math.sin(angulo)
            vertices.append(Punto3D(x, altura/2, z))   # Inferior
        
        # Centro de las tapas
        vertices.append(Punto3D(0, -altura/2, 0))  # Centro superior
        vertices.append(Punto3D(0, altura/2, 0))   # Centro inferior
        
        centro_sup = divisiones * 2
        centro_inf = divisiones * 2 + 1
        
        # Caras laterales
        for i in range(divisiones):
            next_i = (i + 1) % divisiones
            # Rectángulo lateral
            caras.append(Cara([
                i, next_i, next_i + divisiones, i + divisiones
            ], color))
        
        # Tapas
        for i in range(divisiones):
            next_i = (i + 1) % divisiones
            # Tapa superior
            caras.append(Cara([i, next_i, centro_sup], color))
            # Tapa inferior
            caras.append(Cara([
                i + divisiones, centro_inf, next_i + divisiones
            ], color))
        
        return Objeto3D(vertices, caras, color, nombre)
    
    def trasladar(self, dx, dy, dz):
        self.posicion.x += dx
        self.posicion.y += dy
        self.posicion.z += dz
        self.actualizar_vertices()
    
    def rotar(self, dx, dy, dz):
        self.rotacion.x = (self.rotacion.x + dx) % 360
        self.rotacion.y = (self.rotacion.y + dy) % 360
        self.rotacion.z = (self.rotacion.z + dz) % 360
        self.actualizar_vertices()
    
    def actualizar_vertices(self):
        for i, vertice_original in enumerate(self.vertices_originales):
            vertice = vertice_original.copiar()
            
            # Aplicar escala
            vertice.x *= self.escala.x
            vertice.y *= self.escala.y
            vertice.z *= self.escala.z
            
            # Aplicar rotación
            if self.rotacion.z != 0:
                rad = math.radians(self.rotacion.z)
                x_nuevo = vertice.x * math.cos(rad) - vertice.y * math.sin(rad)
                y_nuevo = vertice.x * math.sin(rad) + vertice.y * math.cos(rad)
                vertice.x, vertice.y = x_nuevo, y_nuevo
            
            if self.rotacion.y != 0:
                rad = math.radians(self.rotacion.y)
                x_nuevo = vertice.x * math.cos(rad) + vertice.z * math.sin(rad)
                z_nuevo = -vertice.x * math.sin(rad) + vertice.z * math.cos(rad)
                vertice.x, vertice.z = x_nuevo, z_nuevo
            
            if self.rotacion.x != 0:
                rad = math.radians(self.rotacion.x)
                y_nuevo = vertice.y * math.cos(rad) - vertice.z * math.sin(rad)
                z_nuevo = vertice.y * math.sin(rad) + vertice.z * math.cos(rad)
                vertice.y, vertice.z = y_nuevo, z_nuevo
            
            # Aplicar traslación
            vertice.x += self.posicion.x
            vertice.y += self.posicion.y
            vertice.z += self.posicion.z
            
            self.vertices[i] = vertice
        
        # Recalcular normales de todas las caras
        for cara in self.caras:
            cara.calcular_normal()

class Camara:
    def __init__(self):
        self.posicion = Punto3D(0, 0, -500)
        self.distancia_vision = 500
    
    def proyectar(self, punto):
        """Proyección perspectiva simple"""
        punto_relativo = Punto3D(
            punto.x - self.posicion.x,
            punto.y - self.posicion.y,
            punto.z - self.posicion.z
        )
        
        if self.distancia_vision + punto_relativo.z == 0:
            return (ANCHO//2, ALTO//2)
        
        factor = self.distancia_vision / (self.distancia_vision + punto_relativo.z)
        x2d = punto_relativo.x * factor + ANCHO//2
        y2d = punto_relativo.y * factor + ALTO//2
        
        return (int(x2d), int(y2d))

class SistemaIluminacion:
    """Sistema básico de iluminación"""
    def __init__(self):
        self.direccion_luz = Punto3D(1, -1, 1).normalizar()
        self.intensidad_ambiental = 0.3
        self.intensidad_difusa = 0.7
    
    def calcular_iluminacion(self, normal, color_base):
        """Calcula el color iluminado de una cara"""
        if not normal:
            return color_base
        
        # Producto punto entre normal y dirección de luz
        producto_punto = (normal.x * self.direccion_luz.x + 
                         normal.y * self.direccion_luz.y + 
                         normal.z * self.direccion_luz.z)
        
        # Limitar entre 0 y 1
        intensidad = max(0, min(1, producto_punto))
        
        # Combinar luz ambiental y difusa
        intensidad_final = self.intensidad_ambiental + self.intensidad_difusa * intensidad
        
        # Aplicar intensidad al color
        r = int(color_base[0] * intensidad_final)
        g = int(color_base[1] * intensidad_final)
        b = int(color_base[2] * intensidad_final)
        
        return (r, g, b)

# Crear escena con objetos sólidos
objetos = [
    Objeto3D.crear_cubo(60, NARANJA, "Calabaza Halloween"),
    Objeto3D.crear_piramide(50, 80, COLOR_PIEDRA, "Pirámide de Piedra"),
    Objeto3D.crear_esfera(40, 12, COLOR_METAL, "Esfera Metálica"),
    Objeto3D.crear_cilindro(30, 60, 16, COLOR_TELA, "Cilindro de Tela"),
]

# Configurar posiciones
objetos[0].trasladar(-150, 0, 0)
objetos[1].trasladar(150, 0, 0)
objetos[2].trasladar(0, 0, -150)
objetos[3].trasladar(0, 0, 150)

# Sistema de cámara e iluminación
camara = Camara()
iluminacion = SistemaIluminacion()

# Variables de control
modo_visualizacion = 1  # 1=Sólido, 2=Wireframe, 3=Normales, 4=Mixto
mostrar_caras_ocultas = False
rotacion_automatica = True
tiempo = 0

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
            # Cambiar modo de visualización
            if evento.key == pygame.K_1:
                modo_visualizacion = 1
            elif evento.key == pygame.K_2:
                modo_visualizacion = 2
            elif evento.key == pygame.K_3:
                modo_visualizacion = 3
            elif evento.key == pygame.K_4:
                modo_visualizacion = 4
            
            # Mostrar caras ocultas
            elif evento.key == pygame.K_h:
                mostrar_caras_ocultas = not mostrar_caras_ocultas
            
            # Rotación automática
            elif evento.key == pygame.K_r:
                rotacion_automatica = not rotacion_automatica
            
            # Control de cámara
            elif evento.key == pygame.K_UP:
                camara.distancia_vision = max(100, camara.distancia_vision - 50)
            elif evento.key == pygame.K_DOWN:
                camara.distancia_vision = min(1000, camara.distancia_vision + 50)
    
    # --- ANIMACIÓN ---
    if rotacion_automatica:
        objetos[0].rotar(0, 20 * dt, 10 * dt)
        objetos[1].rotar(15 * dt, 0, 25 * dt)
        objetos[2].rotar(10 * dt, 15 * dt, 0)
        objetos[3].rotar(0, 25 * dt, 15 * dt)
    
    # --- DIBUJADO ---
    ventana.fill(NEGRO)
    
    # Dibujar ejes de referencia
    origen = camara.proyectar(Punto3D(0, 0, 0))
    eje_x = camara.proyectar(Punto3D(100, 0, 0))
    eje_y = camara.proyectar(Punto3D(0, 100, 0))
    eje_z = camara.proyectar(Punto3D(0, 0, 100))
    
    if eje_x: pygame.draw.line(ventana, ROJO, origen, eje_x, 2)
    if eje_y: pygame.draw.line(ventana, VERDE, origen, eje_y, 2)
    if eje_z: pygame.draw.line(ventana, AZUL, origen, eje_z, 2)
    
    # Dibujar objetos
    for objeto in objetos:
        # Ordenar caras por profundidad (painter's algorithm simple)
        caras_ordenadas = sorted(
            objeto.caras,
            key=lambda cara: objeto.vertices[cara.indices_vertices[0]].z if cara.indices_vertices else 0,
            reverse=True
        )
        
        for cara in caras_ordenadas:
            # Verificar visibilidad
            if not mostrar_caras_ocultas and not cara.es_visible(camara.posicion):
                continue
            
            # Proyectar vértices de la cara
            puntos_2d = []
            for indice in cara.indices_vertices:
                punto_3d = objeto.vertices[indice]
                punto_2d = camara.proyectar(punto_3d)
                if punto_2d:
                    puntos_2d.append(punto_2d)
            
            if len(puntos_2d) < 3:
                continue
            
            # Dibujar según el modo de visualización
            if modo_visualizacion == 1:  # Sólido
                color_iluminado = iluminacion.calcular_iluminacion(cara.normal, cara.color)
                pygame.draw.polygon(ventana, color_iluminado, puntos_2d)
                # Borde sutil
                pygame.draw.polygon(ventana, BLANCO, puntos_2d, 1)
            
            elif modo_visualizacion == 2:  # Wireframe
                pygame.draw.polygon(ventana, cara.color, puntos_2d, 2)
            
            elif modo_visualizacion == 3:  # Normales
                # Dibujar cara semitransparente
                color_transparente = cara.color + (100,) if len(cara.color) == 3 else cara.color
                pygame.draw.polygon(ventana, color_transparente, puntos_2d)
                
                # Dibujar normal
                if cara.centro and cara.normal:
                    centro_2d = camara.proyectar(cara.centro)
                    normal_fin = Punto3D(
                        cara.centro.x + cara.normal.x * 30,
                        cara.centro.y + cara.normal.y * 30,
                        cara.centro.z + cara.normal.z * 30
                    )
                    normal_fin_2d = camara.proyectar(normal_fin)
                    
                    if centro_2d and normal_fin_2d:
                        pygame.draw.line(ventana, AMARILLO, centro_2d, normal_fin_2d, 2)
                        pygame.draw.circle(ventana, AMARILLO, centro_2d, 3)
            
            elif modo_visualizacion == 4:  # Mixto (sólido + wireframe)
                color_iluminado = iluminacion.calcular_iluminacion(cara.normal, cara.color)
                pygame.draw.polygon(ventana, color_iluminado, puntos_2d)
                pygame.draw.polygon(ventana, NEGRO, puntos_2d, 1)
    
    # Dibujar cara de Halloween sobre el cubo
    cubo = objetos[0]  # el cubo es el primer objeto

    # Obtener proyección aproximada de su centro frontal
    centro_cubo = camara.proyectar(Punto3D(
        cubo.posicion.x,
        cubo.posicion.y,
        cubo.posicion.z + 60  # cara frontal del cubo
    ))

    if centro_cubo:
        cx, cy = centro_cubo

        # Ojos (triángulos)
        ojo_izq = [(cx - 25, cy - 20), (cx - 10, cy - 35), (cx - 5, cy - 20)]
        ojo_der = [(cx + 25, cy - 20), (cx + 10, cy - 35), (cx + 5, cy - 20)]

        pygame.draw.polygon(ventana, NEGRO, ojo_izq)
        pygame.draw.polygon(ventana, NEGRO, ojo_der)

        # Nariz (triángulo pequeño)
        nariz = [(cx - 5, cy - 5), (cx + 5, cy - 5), (cx, cy - 15)]
        pygame.draw.polygon(ventana, NEGRO, nariz)

        # Boca (zigzag)
        boca_pts = [
            (cx - 30, cy + 15),
            (cx - 20, cy + 25),
            (cx - 10, cy + 15),
            (cx, cy + 25),
            (cx + 10, cy + 15),
            (cx + 20, cy + 25),
            (cx + 30, cy + 15)
        ]
        pygame.draw.polygon(ventana, NEGRO, boca_pts)

    
    # --- INFORMACIÓN EN PANTALLA ---
    fuente = pygame.font.SysFont('Arial', 18)
    
    modos_vis = ["", "SÓLIDO", "WIREFRAME", "NORMALES", "MIXTO"]
    info_textos = [
        f"Modo: {modos_vis[modo_visualizacion]}",
        f"Caras ocultas: {'VISIBLES' if mostrar_caras_ocultas else 'OCULTAS'}",
        f"Rotación: {'AUTOMÁTICA' if rotacion_automatica else 'MANUAL'}",
        f"Objetos: {len(objetos)} | Caras totales: {sum(len(o.caras) for o in objetos)}",
        "",
        "CONTROLES VISUALIZACIÓN:",
        "1-4: Cambiar modo de visualización",
        "H: Mostrar/ocultar caras ocultas",
        "R: Activar/desactivar rotación automática",
        "↑↓: Zoom cámara"
    ]
    
    for i, texto in enumerate(info_textos):
        render = fuente.render(texto, True, BLANCO)
        ventana.blit(render, (10, 10 + i * 22))
    
    # --- LEYENDA DE MATERIALES ---
    leyenda = pygame.font.SysFont('Arial', 14)
    materiales = [
        "Cubo: Madera",
        "Pirámide: Piedra", 
        "Esfera: Metal",
        "Cilindro: Tela"
    ]
    
    for i, material in enumerate(materiales):
        render = leyenda.render(material, True, BLANCO)
        ventana.blit(render, (ANCHO - 150, 100 + i * 20))
    
    # --- ACTUALIZAR PANTALLA ---
    pygame.display.flip()

# Finalizar
pygame.quit()

