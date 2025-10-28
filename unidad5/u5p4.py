# Gerardo Mercado Hurtado
# Raúl Martínez Martínez 
# Importamos librerias
import pygame
import math
import sys

# ----------------- Configuración Pygame -----------------
pygame.init()
ANCHO, ALTO = 1000, 700
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Clase 3: Morphing - Formas y Patrones")
reloj = pygame.time.Clock()
FPS = 60

# ----------------- Colores y fuentes -----------------
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 50, 50)
VERDE = (50, 255, 50)
AZUL = (50, 100, 255)
AMARILLO = (255, 255, 50)
MORADO = (180, 50, 230)
CIAN = (50, 255, 255)
ROSA = (255, 100, 180)
NARANJA = (255, 150, 50)

fuente_grande = pygame.font.Font(None, 36)
fuente_mediana = pygame.font.Font(None, 28)
fuente_pequena = pygame.font.Font(None, 20)

# ----------------- Utilidades -----------------
class FuncionesInterpolacion:
    @staticmethod
    def lineal(t): return t
    @staticmethod
    def ease_in_out_quad(t):
        if t < 0.5:
            return 2 * t * t
        return 1 - math.pow(-2 * t + 2, 2) / 2

def interpolacion_lineal_valor(a, b, t):
    return a + (b - a) * t

def interpolacion_lineal_color(ca, cb, t):
    return tuple(int(ca[i] + (cb[i] - ca[i]) * t) for i in range(3))

def distancia(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

# Re-muestrear un polígono (lista de puntos) a N puntos uniformes aproximados
def resample_polygon(points, N):
    if len(points) == 0:
        return [(0,0)] * N
    seg_lengths = []
    L = 0.0
    for i in range(len(points)):
        a = points[i]
        b = points[(i+1) % len(points)]
        l = distancia(a,b)
        seg_lengths.append(l)
        L += l
    if L == 0:
        return [points[0]] * N
    step = L / N
    res = []
    ring = points[:]
    ring.append(points[0])
    for i_pt in range(N):
        target = i_pt * step
        s = 0.0
        found = False
        for j, seg in enumerate(seg_lengths):
            if s + seg >= target - 1e-9:
                a = ring[j]
                b = ring[j+1]
                seg_t = (target - s) / seg if seg > 0 else 0
                x = a[0] + (b[0]-a[0]) * seg_t
                y = a[1] + (b[1]-a[1]) * seg_t
                res.append((x,y))
                found = True
                break
            s += seg
        if not found:
            res.append(points[-1])
    return res

# Interpolar dos polígonos con mismo número de puntos
def morph_points(a_pts, b_pts, t, easing=FuncionesInterpolacion.ease_in_out_quad):
    t2 = easing(t)
    return [(a_pts[i][0] + (b_pts[i][0]-a_pts[i][0]) * t2,
             a_pts[i][1] + (b_pts[i][1]-a_pts[i][1]) * t2) for i in range(len(a_pts))]

# ----------------- Generadores de formas -----------------
def crear_cuadrado(centro_x, centro_y, tamaño):
    return [
        (centro_x - tamaño, centro_y - tamaño),
        (centro_x + tamaño, centro_y - tamaño),
        (centro_x + tamaño, centro_y + tamaño),
        (centro_x - tamaño, centro_y + tamaño)
    ]

def crear_circulo(centro_x, centro_y, radio, puntos=40):
    pts = []
    for i in range(puntos):
        a = 2 * math.pi * i / puntos
        pts.append((centro_x + radio * math.cos(a), centro_y + radio * math.sin(a)))
    return pts

def crear_triangulo(centro_x, centro_y, tamaño):
    return [
        (centro_x, centro_y - tamaño),
        (centro_x - tamaño, centro_y + tamaño),
        (centro_x + tamaño, centro_y + tamaño)
    ]

def crear_estrellaparam(centro_x, centro_y, radio_externo, radio_interno, puntas=5):
    pts = []
    for i in range(puntas*2):
        a = math.pi * i / puntas
        r = radio_externo if i%2==0 else radio_interno
        pts.append((centro_x + r*math.cos(a), centro_y + r*math.sin(a)))
    return pts

def crear_corazon(centro_x, centro_y, escala=1.0, puntos=80):
    pts = []
    for i in range(puntos):
        t = 2*math.pi * i / puntos
        x = 16 * math.sin(t)**3
        y = 13 * math.cos(t) - 5*math.cos(2*t) - 2*math.cos(3*t) - math.cos(4*t)
        pts.append((centro_x + x * escala, centro_y - y * escala))
    return pts

def crear_flor(centro_x, centro_y, petalos, escala=1.0, puntos=120):
    pts = []
    for i in range(puntos):
        t = 2*math.pi * i / puntos
        radio = 40 * escala + 20 * math.sin(petalos * t) * escala
        x = centro_x + radio * math.cos(t)
        y = centro_y + radio * math.sin(t)
        pts.append((x,y))
    return pts


# ----------------- 

def crear_rectangulo(centro_x, centro_y, ancho, alto):
    return [
        (centro_x - ancho/2, centro_y - alto/2),
        (centro_x + ancho/2, centro_y - alto/2),
        (centro_x + ancho/2, centro_y + alto/2),
        (centro_x - ancho/2, centro_y + alto/2)
    ]



# ----------------- trebol

def crear_trebol(centro_x, centro_y, escala=1.0, puntos=120):
    """Genera los puntos de un trébol de tres hojas."""
    pts = []
    # Usamos una función polar modificada para crear tres lóbulos
    for i in range(puntos):
        t = 2 * math.pi * i / puntos
        # Curva de rosa (r = a * cos(k*t) + C) para tres lóbulos
        radio_base = 1.2 * math.cos(3 * t) + 2.0
        r = radio_base * escala * 20 # Factor de escala
        
        # Transformación a coordenadas cartesianas
        x = centro_x + r * math.cos(t)
        y = centro_y - r * math.sin(t) # El eje Y está invertido en Pygame
        
        # Ajuste para simular un pequeño 'tallo' o base
        if i < puntos // 6 or i > puntos - puntos // 6:
            y += escala * 20 

        pts.append((x, y))
    return pts



# ----------------- Clase MorphingGenerico -----------------
class MorphingGenerico:
    def __init__(self, forma_a, forma_b, duracion=3.0, color=(200,200,200), nombre=""):
        N = max(len(forma_a), len(forma_b), 40)
        N = max(N, 80)  # asegurar suavidad
        self.forma_a = resample_polygon(forma_a, N)
        self.forma_b = resample_polygon(forma_b, N)
        self.forma_actual = [p for p in self.forma_a]
        self.duracion = duracion
        self.tiempo = 0.0
        self.completado = False
        self.color = color
        self.nombre = nombre
        self.pausado = False

    def reiniciar(self):
        self.tiempo = 0.0
        self.completado = False
        self.forma_actual = [p for p in self.forma_a]

    def actualizar(self, dt):
        if self.completado or self.pausado:
            return
        self.tiempo += dt
        t = min(self.tiempo / self.duracion, 1.0)
        if t >= 1.0:
            self.completado = True
        self.forma_actual = morph_points(self.forma_a, self.forma_b, t)

    def dibujar(self, surf, dibujar_puntos=True):
        if len(self.forma_actual) >= 3:
            pygame.draw.polygon(surf, self.color, [(int(x), int(y)) for (x,y) in self.forma_actual])
        if dibujar_puntos:
            for p in self.forma_actual:
                pygame.draw.circle(surf, BLANCO, (int(p[0]), int(p[1])), 3)

class MorphingAvanzado(MorphingGenerico):
    def __init__(self, forma_a, forma_b, duracion=4.0, color=(180,120,220), nombre=""):
        super().__init__(forma_a, forma_b, duracion, color, nombre)
        cx = sum(p[0] for p in self.forma_a)/len(self.forma_a)
        cy = sum(p[1] for p in self.forma_a)/len(self.forma_a)
        self.puntos_control = []
        for i in range(8):
            ang = 2*math.pi*i/8
            r = 70
            self.puntos_control.append((cx + r*math.cos(ang), cy + r*math.sin(ang)))
        self.mostrar_control = True

    def _calcular_deformacion(self, p, t):
        dx_total = 0.0
        dy_total = 0.0
        factor = math.sin(t*math.pi)
        for ctl in self.puntos_control:
            dx = p[0] - ctl[0]
            dy = p[1] - ctl[1]
            dist = math.hypot(dx, dy) + 1e-6
            influencia = 1.0 / (1.0 + dist/60.0)
            dx_total += dx * influencia * factor * 0.04
            dy_total += dy * influencia * factor * 0.04
        return dx_total, dy_total

    def actualizar(self, dt):
        if self.completado or self.pausado:
            return
        self.tiempo += dt
        t = min(self.tiempo / self.duracion, 1.0)
        if t >= 1.0:
            self.completado = True
        base = morph_points(self.forma_a, self.forma_b, t)
        t_e = FuncionesInterpolacion.ease_in_out_quad(t)
        nueva = []
        for p in base:
            dx, dy = self._calcular_deformacion(p, t_e)
            nueva.append((p[0] + dx, p[1] + dy))
        self.forma_actual = nueva

    def dibujar(self, surf, dibujar_puntos=True):
        super().dibujar(surf, dibujar_puntos)
        if self.mostrar_control:
            for ctl in self.puntos_control:
                pygame.draw.circle(surf, ROJO, (int(ctl[0]), int(ctl[1])), 5)
                pygame.draw.circle(surf, BLANCO, (int(ctl[0]), int(ctl[1])), 5, 1)

# ----------------- Morphing de patrones de color
class MorphingImagenPatrones:
    """Morphing entre dos patrones de color (lista de tuplas RGB)."""
    def __init__(self, patron_a, patron_b, ancho, alto, duracion=5.0):
        self.patron_a = patron_a
        self.patron_b = patron_b
        self.ancho = ancho
        self.alto = alto
        self.patron_actual = patron_a[:]
        self.progreso = 0.0
        self.duracion = duracion
        self.tiempo_transcurrido = 0.0
        self.completado = False

    def actualizar(self, dt):
        if self.completado:
            return
        self.tiempo_transcurrido += dt
        self.progreso = self.tiempo_transcurrido / self.duracion
        if self.progreso >= 1.0:
            self.progreso = 1.0
            self.completado = True
        progreso_suavizado = FuncionesInterpolacion.ease_in_out_quad(self.progreso)
        for i in range(len(self.patron_actual)):
            if i < len(self.patron_a) and i < len(self.patron_b):
                self.patron_actual[i] = interpolacion_lineal_color(self.patron_a[i], self.patron_b[i], progreso_suavizado)

    def dibujar(self, superficie, x, y, tamaño_celda=20):
        for i, color in enumerate(self.patron_actual):
            fila = i // self.ancho
            columna = i % self.ancho
            rect = pygame.Rect(x + columna * tamaño_celda, y + fila * tamaño_celda, tamaño_celda - 2, tamaño_celda - 2)
            pygame.draw.rect(superficie, color, rect)

    def reiniciar(self):
        self.tiempo_transcurrido = 0.0
        self.progreso = 0.0
        self.completado = False
        self.patron_actual = self.patron_a[:]

def generar_patron_colores(ancho, alto, tipo):
    patron = []
    for fila in range(alto):
        for columna in range(ancho):
            if tipo == "degradado_vertical":
                intensidad = int(255 * fila / (alto - 1 if alto>1 else 1))
                color = (intensidad, max(0,255 - intensidad), 128)
            elif tipo == "degradado_horizontal":
                intensidad = int(255 * columna / (ancho - 1 if ancho>1 else 1))
                color = (128, intensidad, max(0,255 - intensidad))
            elif tipo == "ajedrez":
                color = (255, 100, 100) if (fila + columna) % 2 == 0 else (100, 100, 255)
            elif tipo == "radial":
                centro_x = (ancho - 1) / 2.0
                centro_y = (alto - 1) / 2.0
                dist = math.sqrt((columna - centro_x) ** 2 + (fila - centro_y) ** 2)
                max_dist = math.sqrt(centro_x ** 2 + centro_y ** 2) if centro_x>0 or centro_y>0 else 1.0
                intensidad = int(255 * max(0.0, (1 - dist / max_dist)))
                color = (intensidad, max(0,255 - intensidad), 128)
            else:
                color = (128, 128, 128)
            patron.append(color)
    return patron


def demostracion_morphing_basico():
    # --- Primer Morphing: Triángulo Morado a Cuadrado Blanco ---
    tri_start = crear_triangulo(250, 350, 80) # Triángulo inicial, centrado
    sq_end = crear_cuadrado(250, 350, 70)   # Cuadrado final, centrado

    morph1 = MorphingGenerico(
        tri_start,
        sq_end,
        duracion=3.5,
        color=MORADO, # Color inicial morado
        nombre="Triángulo Morado → Cuadrado Blanco"
    )

    # --- Segundo Morphing: Rectángulo Rojo a Triángulo Naranja ---
    rect_start = crear_rectangulo(750, 350, 150, 70) # Rectángulo inicial
    tri_end = crear_triangulo(750, 350, 90)       # Triángulo final

    morph2 = MorphingGenerico(
        rect_start,
        tri_end,
        duracion=3.5,
        color=ROJO, # Color inicial rojo
        nombre="Rectángulo Rojo → Triángulo Naranja"
    )

    morphs = [morph1, morph2]

    tiempo_total = 0.0
    ejecutando = True
    pausado_global = False

    while ejecutando:
        dt = reloj.tick(FPS) / 1000.0
        tiempo_total += dt

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif evento.key == pygame.K_r:
                    for m in morphs: m.reiniciar()
                    tiempo_total = 0.0
                elif evento.key == pygame.K_SPACE:
                    pausado_global = not pausado_global
                    for m in morphs: m.pausado = pausado_global

        for m in morphs:
            # Lógica de interpolación de color
            t_progress = min(m.tiempo / m.duracion, 1.0)
            if m.nombre == "Triángulo Morado → Cuadrado Blanco":
                m.color = interpolacion_lineal_color(MORADO, BLANCO, t_progress)
            elif m.nombre == "Rectángulo Rojo → Triángulo Naranja":
                m.color = interpolacion_lineal_color(ROJO, NARANJA, t_progress)

            m.actualizar(dt)
        
        ventana.fill(NEGRO)
        titulo = fuente_grande.render("Morphing Básico - Formas Personalizadas", True, BLANCO)
        ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 12))

        for i, m in enumerate(morphs):
            m.dibujar(ventana, dibujar_puntos=True)
            if m.forma_actual:
                cx = sum(p[0] for p in m.forma_actual)/len(m.forma_actual)
                cy = sum(p[1] for p in m.forma_actual)/len(m.forma_actual)
                txt = fuente_pequena.render(m.nombre + f" ({min(100, int(100*(m.tiempo/m.duracion)))}%)", True, BLANCO)
                # Ajustamos la posición del texto para que no se superpongan y estén sobre cada figura
                ventana.blit(txt, (cx - txt.get_width()//2, cy - 120)) # Posiciona el texto más arriba

        pista = fuente_pequena.render("R: Reiniciar | ESPACIO: Pausa | ESC: Volver", True, AMARILLO)
        ventana.blit(pista, (20, ALTO - 40))
        pygame.display.flip()



def demostracion_morphing_avanzado():
    # El morphing de las flores se mantiene
    flor8 = crear_flor(500, 320, petalos=8, escala=1.0, puntos=160)
    flor4 = crear_flor(500, 320, petalos=4, escala=1.0, puntos=160)
    
    # --- CAMBIO AQUÍ: Reemplazamos Corazón por Trébol ---
    # Trebol Pequeño (Centro 250)
    trebol_small = crear_trebol(250, 300, escala=1.8, puntos=140) 
    # Trebol Grande (Centro 750)
    trebol_big = crear_trebol(750, 300, escala=3.0, puntos=140)
    # -----------------------------------------------------

    morph_flor = MorphingAvanzado(flor8, flor4, duracion=4.5, color=MORADO, nombre="Flor 8 → Flor 4")
    
    # --- CAMBIO AQUÍ: Usamos las nuevas formas y el color VERDE ---
    morph_trebol = MorphingAvanzado(
        trebol_small, 
        trebol_big, 
        duracion=5.0, 
        color=VERDE, # 👈 Cambiado a VERDE
        nombre="Trébol Pequeño → Trébol Grande" 
    )
    # -----------------------------------------------------------------
    
    morphs = [morph_flor, morph_trebol]
    tiempo_total = 0.0
    ejecutando = True
    pausado_global = False
    
    while ejecutando:
        dt = reloj.tick(FPS) / 1000.0
        tiempo_total += dt
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif evento.key == pygame.K_r:
                    for m in morphs: m.reiniciar()
                    tiempo_total = 0.0
                elif evento.key == pygame.K_c:
                    for m in morphs:
                        if isinstance(m, MorphingAvanzado):
                            m.mostrar_control = not m.mostrar_control
                elif evento.key == pygame.K_SPACE:
                    pausado_global = not pausado_global
                    for m in morphs: m.pausado = pausado_global
        
        for m in morphs:
            m.actualizar(dt)
            
        ventana.fill(NEGRO)
        titulo = fuente_grande.render("Morphing Avanzado - Deformación Controlada", True, BLANCO)
        ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 12))
        
        for m in morphs:
            m.dibujar(ventana, dibujar_puntos=True)
            if m.forma_actual:
                cx = sum(p[0] for p in m.forma_actual)/len(m.forma_actual)
                cy = sum(p[1] for p in m.forma_actual)/len(m.forma_actual)
                txt = fuente_pequena.render(m.nombre + f"  ({min(100, int(100*(m.tiempo/m.duracion)))}%)", True, BLANCO)
                ventana.blit(txt, (cx - txt.get_width()//2, cy - 120))
                
        info = [
            "C: Mostrar/Ocultar puntos de control (rojos)",
            "R: Reiniciar | ESPACIO: Pausa | ESC: Volver"
        ]
        for i,l in enumerate(info):
            ventana.blit(fuente_pequena.render(l, True, AMARILLO), (20, ALTO - 60 + i*20))
            
        pygame.display.flip()


def demostracion_morphing_imagen_like():
    # --- MORPH 1: Corazón Naranja a Círculo Cian ---
    # La forma inicial es un Corazón. Escala 2.6, 200 puntos. Centro (300, 320)
    heart = crear_corazon(300, 320, escala=2.6, puntos=200) 
    # La forma final es un Círculo. Radio 100, 200 puntos (para igualar el número de puntos aproximado). Centro (300, 320)
    circle = crear_circulo(300, 320, radio=100, puntos=200)

    morph_a = MorphingGenerico(
        heart, 
        circle, 
        duracion=4.0, 
        color=NARANJA, 
        nombre="Corazón → Círculo" # Nombre actualizado
    )
    
    # --- MORPH 2: Triángulo Azul a Rectángulo Rojo ---
    # La forma inicial es un Triángulo. Tamaño 90. Centro (700, 320)
    triangle_start = crear_triangulo(700, 320, 90)
    # La forma final es un Rectángulo. Ancho 180, Alto 100. Centro (700, 320)
    rectangle_end = crear_rectangulo(700, 320, 180, 100) 

    morph_b = MorphingGenerico(
        triangle_start, 
        rectangle_end, 
        duracion=4.0, 
        color=AZUL, 
        nombre="Triángulo → Rectángulo" # Nombre actualizado
    )
    
    # Lista de morphings a ejecutar
    morphs = [morph_a, morph_b]

    # ... (El resto de la lógica de Pygame se mantiene igual)
    tiempo_total = 0.0
    ejecutando = True
    pausado_global = False
    
    while ejecutando:
        dt = reloj.tick(FPS) / 1000.0
        tiempo_total += dt
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif evento.key == pygame.K_r:
                    for m in morphs: m.reiniciar()
                    tiempo_total = 0.0
                elif evento.key == pygame.K_SPACE:
                    pausado_global = not pausado_global
                    for m in morphs: m.pausado = pausado_global
                    
        for m in morphs:
            # Lógica de interpolación de color
            t_progress = min(m.tiempo / m.duracion, 1.0)
            if m.nombre == "Corazón → Círculo":
                # Interpolación de NARANJA a CIAN
                m.color = interpolacion_lineal_color(NARANJA, CIAN, t_progress) 
            elif m.nombre == "Triángulo → Rectángulo":
                # Interpolación de AZUL a ROJO
                m.color = interpolacion_lineal_color(AZUL, ROJO, t_progress)

            m.actualizar(dt)
            
        ventana.fill(NEGRO)
        titulo = fuente_grande.render("Morphing tipo 'Imagen' - Contornos interpolados", True, BLANCO)
        ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 12))
        
        for m in morphs:
            m.dibujar(ventana, dibujar_puntos=True)
            if m.forma_actual:
                cx = sum(p[0] for p in m.forma_actual)/len(m.forma_actual)
                cy = sum(p[1] for p in m.forma_actual)/len(m.forma_actual)
                txt = fuente_pequena.render(m.nombre + f"  ({min(100, int(100*(m.tiempo/m.duracion)))}%)", True, BLANCO)
                ventana.blit(txt, (cx - txt.get_width()//2, cy - 120))
                
        pista = fuente_pequena.render("R: Reiniciar | ESPACIO: Pausa | ESC: Volver", True, AMARILLO)
        ventana.blit(pista, (20, ALTO - 40))
        pygame.display.flip()





def demostracion_morphing_patrones():
    ancho_grid, alto_grid = 10, 10
    tamaño_celda = 20 # Definimos el tamaño para usarlo en el círculo también

    patrones = [
        {
            'nombre': "Degradado Vertical → Horizontal",
            'patron_a': generar_patron_colores(ancho_grid, alto_grid, "degradado_vertical"),
            'patron_b': generar_patron_colores(ancho_grid, alto_grid, "degradado_horizontal"),
            'pos_x': 180,
        },
        {
            'nombre': "Ajedrez → Radial",
            'patron_a': generar_patron_colores(ancho_grid, alto_grid, "ajedrez"),
            'patron_b': generar_patron_colores(ancho_grid, alto_grid, "radial"),
            'pos_x': 560,
        }
    ]
    morphings = []
    for pd in patrones:
        # Se asegura que la duración sea la misma para que la animación del círculo sea coherente
        m = MorphingImagenPatrones(pd['patron_a'], pd['patron_b'], ancho_grid, alto_grid, duracion=5.0) 
        m.nombre = pd['nombre']
        m.pos_x = pd['pos_x']
        morphings.append(m)

    # --- Configuración del Círculo Central ---
    centro_x_circulo = ANCHO // 2
    centro_y_circulo = 300
    radio_circulo = (ancho_grid * tamaño_celda) // 2 + 10 # Un poco más grande que la cuadrícula

    ejecutando = True
    tiempo_total = 0.0

    while ejecutando:
        dt = reloj.tick(FPS) / 1000.0
        tiempo_total += dt
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif evento.key == pygame.K_r:
                    for m in morphings: m.reiniciar()
                    tiempo_total = 0.0

        for m in morphings:
            m.actualizar(dt)

        ventana.fill(NEGRO)
        texto_titulo = fuente_grande.render("Morphing de Imágenes - Interpolación de Colores", True, BLANCO)
        ventana.blit(texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, 20))

        # Dibujar los dos morphings laterales
        for m in morphings:
            m.dibujar(ventana, m.pos_x, 150, tamaño_celda)
            texto = fuente_pequena.render(m.nombre, True, BLANCO)
            # Centrar el nombre sobre la cuadrícula
            ventana.blit(texto, (m.pos_x + (ancho_grid * tamaño_celda) // 2 - texto.get_width() // 2, 120)) 
            texto_progreso = fuente_pequena.render(f"Progreso: {m.progreso*100:.1f}%", True, VERDE)
            ventana.blit(texto_progreso, (m.pos_x, 440))

        # --- Lógica y Dibujo del Círculo Central ---
        morph_central = morphings[1] # Seleccionamos el segundo morphing (Ajedrez → Radial)
        
        # 1. Crear una superficie temporal con el patrón del segundo morphing
        # Se crea con un tamaño ligeramente mayor para evitar problemas de recorte al dibujar el círculo.
        temp_surf = pygame.Surface((ancho_grid * tamaño_celda, alto_grid * tamaño_celda))
        temp_surf.fill(NEGRO) # Fondo negro para el recorte

        # Dibujar el patrón actual del segundo morphing en la superficie temporal
        # Usamos 0, 0 como posición inicial porque se dibuja en la superficie temporal
        # Usamos 'tamaño_celda' que definimos al inicio.
        morph_central.dibujar(temp_surf, 0, 0, tamaño_celda) 

        # 2. Crear una máscara de círculo
        mask = pygame.Surface((ancho_grid * tamaño_celda, alto_grid * tamaño_celda), pygame.SRCALPHA)
        pygame.draw.circle(mask, (255, 255, 255, 255), 
                           (mask.get_width() // 2, mask.get_height() // 2), 
                           radio_circulo - 10) # Radio para la máscara

        # 3. Aplicar la máscara (requiere convertir el patrón a Surface)
        temp_surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # 4. Dibujar la superficie temporal con el patrón recortado en la ventana principal
        # Posicionamos en el centro entre los dos morphings.
        ventana.blit(temp_surf, (centro_x_circulo - temp_surf.get_width() // 2, centro_y_circulo - temp_surf.get_height() // 2))

        # 5. Dibujar el contorno del círculo
        pygame.draw.circle(ventana, BLANCO, (centro_x_circulo, centro_y_circulo), radio_circulo - 9, 2)
        
        # 6. Añadir texto para el círculo central
        texto_central = fuente_mediana.render("Patrón Central: Ajedrez → Radial", True, AMARILLO)
        ventana.blit(texto_central, (centro_x_circulo - texto_central.get_width() // 2, centro_y_circulo + radio_circulo + 10))

        # Información de control
        info_lines = [
            f"Tiempo: {tiempo_total:.1f}s",
            "Cada celda es un píxel de ejemplo; los colores se interpolan.",
            "",
            "Controles:",
            "R: Reiniciar animación",
            "ESC: Volver"
        ]
        for i, linea in enumerate(info_lines):
            texto = fuente_pequena.render(linea, True, AMARILLO)
            ventana.blit(texto, (20, ALTO - 180 + i * 25))
            
        pygame.display.flip()


# ----------------- Menú principal -----------------
def menu_principal_clase3():
    opciones = [
        ("1. Morphing Básico - Formas Simples", demostracion_morphing_basico),
        ("2. Morphing Avanzado - Deformación Controlada", demostracion_morphing_avanzado),
        ("3. Morphing 'Imagen' - Contornos (Cuadrado↔Corazón)", demostracion_morphing_imagen_like),
        ("4. Morphing de Imágenes - Interpolación de Colores", demostracion_morphing_patrones),
        ("5. Salir", None)
    ]
    while True:
        ventana.fill(NEGRO)
        titulo = fuente_grande.render("CLASE 3: MORPHING - INTEGRADO", True, BLANCO)
        ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 40))
        subt = fuente_mediana.render("Formas generadas + Patrones de color", True, VERDE)
        ventana.blit(subt, (ANCHO//2 - subt.get_width()//2, 90))
        for i, (txt, _) in enumerate(opciones):
            color = CIAN if i < len(opciones)-1 else ROJO
            render = fuente_mediana.render(txt, True, color)
            ventana.blit(render, (ANCHO//2 - render.get_width()//2, 160 + i*60))
        instrucciones = fuente_pequena.render("Presiona 1-5 para seleccionar. ESC para salir.", True, AMARILLO)
        ventana.blit(instrucciones, (ANCHO//2 - instrucciones.get_width()//2, ALTO - 60))
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    demostracion_morphing_basico()
                elif evento.key == pygame.K_2:
                    demostracion_morphing_avanzado()
                elif evento.key == pygame.K_3:
                    demostracion_morphing_imagen_like()
                elif evento.key == pygame.K_4:
                    demostracion_morphing_patrones()
                elif evento.key == pygame.K_5 or evento.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

if __name__ == "__main__":
    menu_principal_clase3()


