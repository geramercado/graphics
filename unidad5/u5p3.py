# Gerardo Mercado Hurtado
# Raúl Martínez Martínez 
#Importamos librerias
import pygame
import math
import sys

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
ANCHO, ALTO = 1000, 700
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Clase 2: Tweening - Shape Tween y Sistemas Avanzados")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 50, 50)
VERDE = (50, 255, 50)
AZUL = (50, 100, 255)
AMARILLO = (255, 255, 50)
MORADO = (180, 50, 230)
NARANJA = (255, 150, 50)
CIAN = (50, 255, 255)
ROSA = (255, 100, 180)

# Fuentes
fuente_grande = pygame.font.Font(None, 36)
fuente_mediana = pygame.font.Font(None, 28)
fuente_pequena = pygame.font.Font(None, 22)

reloj = pygame.time.Clock()
FPS = 60

# --- Funciones y Clases de Tweening (Globales) ---

class FuncionesTweening:
    @staticmethod
    def lineal(t):
        return t
    
    @staticmethod
    def ease_in_quad(t):
        return t * t
    
    @staticmethod
    def ease_out_quad(t):
        return 1 - (1 - t) * (1 - t)
    
    @staticmethod
    def ease_in_out_quad(t):
        if t < 0.5:
            return 2 * t * t
        else:
            return 1 - math.pow(-2 * t + 2, 2) / 2
    
    @staticmethod
    def ease_in_back(t):
        """Retroceso al inicio"""
        c1 = 1.70158
        c3 = c1 + 1
        return c3 * t * t * t - c1 * t * t
    
    @staticmethod
    def ease_out_back(t):
        """Retroceso al final"""
        c1 = 1.70158
        c3 = c1 + 1
        return 1 + c3 * math.pow(t - 1, 3) + c1 * math.pow(t - 1, 2)
    
    @staticmethod
    def ease_out_bounce(t):
        if t < 1 / 2.75:
            return 7.5625 * t * t
        elif t < 2 / 2.75:
            t -= 1.5 / 2.75
            return 7.5625 * t * t + 0.75
        elif t < 2.5 / 2.75:
            t -= 2.25 / 2.75
            return 7.5625 * t * t + 0.9375
        else:
            t -= 2.625 / 2.75
            return 7.5625 * t * t + 0.984375
    
    @staticmethod
    def elastic(t):
        """Efecto elástico"""
        if t <= 0 or t >= 1:
            return t
        return -math.pow(2, 10 * t - 10) * math.sin((t * 10 - 10.75) * (2 * math.pi) / 3)

def interpolacion_lineal(inicio, fin, progreso):
    """Interpolación lineal que maneja números y tuplas"""
    if isinstance(inicio, (tuple, list)) and isinstance(fin, (tuple, list)):
        return tuple(
            int(inicio[i] + (fin[i] - inicio[i]) * progreso)
            for i in range(min(len(inicio), len(fin)))
        )
    else:
        return inicio + (fin - inicio) * progreso

class Tween:
    def __init__(self, objeto, propiedad, valor_final, duracion, funcion_easing=None, delay=0):
        self.objeto = objeto
        self.propiedad = propiedad
        self.valor_inicial = getattr(objeto, propiedad)
        self.valor_final = valor_final
        self.duracion = duracion
        self.delay = delay
        self.tiempo_transcurrido = 0
        self.funcion_easing = funcion_easing or FuncionesTweening.lineal
        self.activo = True
        self.completado = False
        self.en_delay = delay > 0
    
    def actualizar(self, dt):
        if not self.activo or self.completado:
            return
        
        self.tiempo_transcurrido += dt
        
        # Manejar delay
        if self.en_delay:
            if self.tiempo_transcurrido >= self.delay:
                self.en_delay = False
                self.tiempo_transcurrido = 0
            return
        
        progreso = self.tiempo_transcurrido / self.duracion
        
        if progreso >= 1:
            progreso = 1
            self.completado = True
        
        progreso_suavizado = self.funcion_easing(progreso)
        valor_actual = interpolacion_lineal(self.valor_inicial, self.valor_final, progreso_suavizado)
        setattr(self.objeto, self.propiedad, valor_actual)

class ShapeTween:
    """Sistema de Shape Tween para interpolación de formas"""
    def __init__(self, forma_inicial, forma_final, duracion, funcion_easing=None):
        min_puntos = min(len(forma_inicial), len(forma_final))
        self.forma_inicial = forma_inicial[:min_puntos]
        self.forma_final = forma_final[:min_puntos]
        self.duracion = duracion
        self.funcion_easing = funcion_easing or FuncionesTweening.lineal
        self.tiempo_transcurrido = 0
        self.completado = False
        self.forma_actual = self.forma_inicial[:]
    
    def actualizar(self, dt):
        if self.completado:
            return
        
        self.tiempo_transcurrido += dt
        progreso = min(self.tiempo_transcurrido / self.duracion, 1.0)
        
        if progreso >= 1:
            self.completado = True
            self.forma_actual = self.forma_final[:]
            return
        
        progreso_suavizado = self.funcion_easing(progreso)
        
        for i in range(len(self.forma_actual)):
            x1, y1 = self.forma_inicial[i]
            x2, y2 = self.forma_final[i]
            x_actual = x1 + (x2 - x1) * progreso_suavizado
            y_actual = y1 + (y2 - y1) * progreso_suavizado
            self.forma_actual[i] = (int(x_actual), int(y_actual))

class SistemaTweening:
    """Sistema para gestionar múltiples tweens"""
    def __init__(self):
        self.tweens = []
        self.shape_tweens = []
        self.tiempo_total = 0
    
    def agregar_tween(self, tween):
        self.tweens.append(tween)
    
    def agregar_shape_tween(self, shape_tween):
        self.shape_tweens.append(shape_tween)
    
    def actualizar(self, dt):
        self.tiempo_total += dt
        # Actualizar en copias para permitir que un tween agregue otro tween
        for tween in self.tweens[:]:
            tween.actualizar(dt)
        for shape_tween in self.shape_tweens[:]:
            shape_tween.actualizar(dt)
    
    def limpiar_completados(self):
        self.tweens = [t for t in self.tweens if not t.completado]
        self.shape_tweens = [st for st in self.shape_tweens if not st.completado]

# NUEVO: Clases movidas al ámbito global para ser reutilizadas

class Particula:
    """Define una partícula simple para efectos visuales"""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.tamano = 15
        self.alpha = 255
        self.activa = True
    
    def dibujar(self, superficie):
        if not self.activa:
            return
        surf = pygame.Surface((self.tamano * 2, self.tamano * 2), pygame.SRCALPHA)
        color_con_alpha = (*self.color, int(self.alpha))
        pygame.draw.circle(surf, color_con_alpha, (self.tamano, self.tamano), self.tamano)
        rect = surf.get_rect(center=(int(self.x), int(self.y)))
        superficie.blit(surf, rect)

class TweenAvanzado(Tween):
    """Un Tween que acepta un callback on_complete"""
    def __init__(self, objeto, propiedad, valor_final, duracion, 
                 funcion_easing=None, delay=0, on_complete=None):
        super().__init__(objeto, propiedad, valor_final, duracion, funcion_easing, delay)
        self.on_complete = on_complete
        self._callback_ejecutado = False # Para evitar ejecuciones múltiples
    
    def actualizar(self, dt):
        if self.completado: 
            return

        super().actualizar(dt)
        
        if self.completado and self.on_complete and not self._callback_ejecutado:
            self.on_complete()
            self._callback_ejecutado = True


# --- Demostraciones ---

def demostracion_shape_tween():
    """Demostración de Shape Tween - Transformación de formas CORREGIDA"""
    
    formas = [
        {
            'inicial': [(100, 100), (200, 100), (200, 200), (100, 200)],
            'final': [(150, 50), (250, 150), (150, 250), (50, 150)],
            'color': ROJO,
            'nombre': "Cuadrado → Rombo"
        },
        {
            'inicial': [(400, 150), (350, 250), (450, 250)],
            'final': [(400, 250), (350, 150), (450, 150)],
            'color': VERDE,
            'nombre': "Triángulo → Invertido"
        }
    ]
    
    sistema = SistemaTweening()
    shape_tweens = []
    
    for i, forma_data in enumerate(formas):
        shape_tween = ShapeTween(
            forma_data['inicial'],
            forma_data['final'],
            duracion=4.0,
            funcion_easing=FuncionesTweening.ease_in_out_quad
        )
        shape_tween.delay = i * 1.5 # Esto es un atributo personalizado, no de la clase
        shape_tween.color = forma_data['color']
        shape_tween.nombre = forma_data['nombre']
        shape_tweens.append(shape_tween)
        sistema.agregar_shape_tween(shape_tween)
    
    ejecutando = True
    mostrar_puntos = True
    
    while ejecutando:
        dt = reloj.tick(FPS) / 1000.0
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return
                elif evento.key == pygame.K_r:
                    demostracion_shape_tween()
                    return
                elif evento.key == pygame.K_p:
                    mostrar_puntos = not mostrar_puntos
        
        sistema.actualizar(dt)
        
        ventana.fill(NEGRO)
        
        for shape_tween in shape_tweens:
            # (El 'delay' personalizado no está implementado en la clase ShapeTween,
            # la clase Tween sí lo maneja. Aquí solo se dibujan).
            if len(shape_tween.forma_actual) >= 3:
                pygame.draw.polygon(ventana, shape_tween.color, shape_tween.forma_actual)
                pygame.draw.polygon(ventana, BLANCO, shape_tween.forma_actual, 2)
            
            if mostrar_puntos:
                for punto in shape_tween.forma_actual:
                    pygame.draw.circle(ventana, BLANCO, (int(punto[0]), int(punto[1])), 4)
            
            texto = fuente_pequena.render(shape_tween.nombre, True, BLANCO)
            if shape_tween.forma_actual:
                centro_x = sum(p[0] for p in shape_tween.forma_actual) / len(shape_tween.forma_actual)
                centro_y = sum(p[1] for p in shape_tween.forma_actual) / len(shape_tween.forma_actual)
                ventana.blit(texto, (centro_x - texto.get_width()//2, centro_y + 50))
        
        texto_titulo = fuente_grande.render("Shape Tween - Transformación de Formas", True, BLANCO)
        ventana.blit(texto_titulo, (ANCHO//2 - texto_titulo.get_width()//2, 20))
        
        info_lines = [
            f"Tiempo: {sistema.tiempo_total:.1f}s",
            f"Formas activas: {sum(1 for st in shape_tweens if not st.completado)}/{len(shape_tweens)}",
            "P: Mostrar/Ocultar puntos | R: Reiniciar | ESC: Volver"
        ]
        
        for i, linea in enumerate(info_lines):
            texto = fuente_pequena.render(linea, True, BLANCO)
            ventana.blit(texto, (20, ALTO - 100 + i * 25))
        
        pygame.display.flip()
        
        if all(st.completado for st in shape_tweens) and sistema.tiempo_total > 10:
            demostracion_shape_tween()
            return

def demostracion_tweening_secuencial():
    """Demostración de tweens secuenciales y paralelos"""
    
    class ObjetoMultiple:
        def __init__(self, x, y, color):
            self.x = x
            self.y = y
            self.color = color
            self.escala = 1.0
            self.rotacion = 0
            self.alpha = 255
        
        def dibujar(self, superficie):
            surf = pygame.Surface((40, 40), pygame.SRCALPHA)
            color_con_alpha = (*self.color, int(self.alpha))
            pygame.draw.rect(surf, color_con_alpha, (0, 0, 40, 40), border_radius=6)
            
            if self.escala != 1.0:
                nuevo_tamano = int(40 * self.escala)
                surf = pygame.transform.scale(surf, (nuevo_tamano, nuevo_tamano))
            
            if self.rotacion != 0:
                surf = pygame.transform.rotate(surf, self.rotacion)
            
            rect = surf.get_rect(center=(self.x, self.y))
            superficie.blit(surf, rect)
    
    objetos = [
        ObjetoMultiple(100, 200, ROJO),
        ObjetoMultiple(100, 300, VERDE),
        ObjetoMultiple(100, 400, AZUL),
    ]
    
    sistema = SistemaTweening()
    
    secuencia_objeto1 = [
        {'prop': 'x', 'val': 400, 'dur': 1.5, 'easing': FuncionesTweening.ease_out_quad, 'delay': 0},
        {'prop': 'y', 'val': 100, 'dur': 1.5, 'easing': FuncionesTweening.ease_in_out_quad, 'delay': 1.5},
        {'prop': 'x', 'val': 100, 'dur': 1.5, 'easing': FuncionesTweening.ease_in_back, 'delay': 3.0},
        {'prop': 'y', 'val': 200, 'dur': 1.5, 'easing': FuncionesTweening.ease_out_bounce, 'delay': 4.5},
    ]
    
    for anim in secuencia_objeto1:
        tween = Tween(objetos[0], anim['prop'], anim['val'], anim['dur'], anim['easing'], anim['delay'])
        sistema.agregar_tween(tween)
    
    paralelo_objeto2 = [
        {'prop': 'x', 'val': 400, 'dur': 3.0, 'easing': FuncionesTweening.ease_in_out_quad, 'delay': 1.0},
        {'prop': 'escala', 'val': 1.8, 'dur': 1.5, 'easing': FuncionesTweening.ease_out_quad, 'delay': 1.0},
        {'prop': 'rotacion', 'val': 360, 'dur': 2.0, 'easing': FuncionesTweening.lineal, 'delay': 1.0},
    ]
    
    for anim in paralelo_objeto2:
        tween = Tween(objetos[1], anim['prop'], anim['val'], anim['dur'], anim['easing'], anim['delay'])
        sistema.agregar_tween(tween)
    
    combinado_objeto3 = [
        {'prop': 'x', 'val': 400, 'dur': 2.0, 'easing': FuncionesTweening.ease_out_quad, 'delay': 0.5},
        {'prop': 'escala', 'val': 0.5, 'dur': 1.0, 'easing': FuncionesTweening.ease_in_quad, 'delay': 0.5},
        {'prop': 'escala', 'val': 1.5, 'dur': 1.0, 'easing': FuncionesTweening.ease_out_quad, 'delay': 1.5},
        {'prop': 'alpha', 'val': 100, 'dur': 1.5, 'easing': FuncionesTweening.lineal, 'delay': 2.0},
        {'prop': 'alpha', 'val': 255, 'dur': 1.5, 'easing': FuncionesTweening.lineal, 'delay': 3.5},
        {'prop': 'x', 'val': 100, 'dur': 2.0, 'easing': FuncionesTweening.ease_in_out_quad, 'delay': 3.5},
    ]
    
    for anim in combinado_objeto3:
        tween = Tween(objetos[2], anim['prop'], anim['val'], anim['dur'], anim['easing'], anim['delay'])
        sistema.agregar_tween(tween)
    
    ejecutando = True
    while ejecutando:
        dt = reloj.tick(FPS) / 1000.0
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return
                elif evento.key == pygame.K_r:
                    demostracion_tweening_secuencial()
                    return
        
        sistema.actualizar(dt)
        
        ventana.fill(NEGRO)
        
        for obj in objetos:
            obj.dibujar(ventana)
        
        texto_titulo = fuente_grande.render("Tweens Secuenciales y Paralelos", True, BLANCO)
        ventana.blit(texto_titulo, (ANCHO//2 - texto_titulo.get_width()//2, 20))
        
        etiquetas = [
            ("SECUENCIAL: Un tween después de otro", objetos[0].y + 50, ROJO),
            ("PARALELO: Múltiples tweens simultáneos", objetos[1].y + 50, VERDE),
            ("COMBINADO: Mezcla de ambos", objetos[2].y + 50, AZUL),
        ]
        
        for texto, y, color in etiquetas:
            render = fuente_pequena.render(texto, True, color)
            ventana.blit(render, (150, y))
        
        info_general = [
            f"Tiempo: {sistema.tiempo_total:.1f}s",
            "R: Reiniciar | ESC: Volver al menú"
        ]
        
        for i, linea in enumerate(info_general):
            texto = fuente_pequena.render(linea, True, BLANCO)
            ventana.blit(texto, (20, ALTO - 60 + i * 25))
        
        pygame.display.flip()
        
        if sistema.tiempo_total > 8 and all(t.completado for t in sistema.tweens):
            demostracion_tweening_secuencial()
            return

def demostracion_sistema_avanzado():
    """Demostración de un sistema de tweening avanzado con callbacks"""
    
    # NUEVO: Las clases Particula y TweenAvanzado ya no están aquí,
    # son globales y accesibles.
    
    particulas = []
    for i in range(8):
        color = [ROJO, VERDE, AZUL, AMARILLO, MORADO, NARANJA, CIAN, ROSA][i % 8]
        particula = Particula(ANCHO // 2, ALTO // 2, color)
        particulas.append(particula)
    
    sistema = SistemaTweening()
    
    def crear_animacion_circular(particula, angulo, radio):
        radianes = math.radians(angulo)
        x_final = ANCHO // 2 + math.cos(radianes) * radio
        y_final = ALTO // 2 + math.sin(radianes) * radio
        
        def on_complete_desvanecimiento():
            particula.activa = False
            if all(not p.activa for p in particulas):
                pygame.time.set_timer(pygame.USEREVENT, 1000, True)
        
        def on_complete_movimiento():
            tween_alpha = TweenAvanzado(particula, 'alpha', 0, 1.0, 
                                     FuncionesTweening.ease_in_quad, delay=0.5,
                                     on_complete=on_complete_desvanecimiento)
            sistema.agregar_tween(tween_alpha)
        
        tween_x = TweenAvanzado(particula, 'x', x_final, 2.0, 
                             FuncionesTweening.ease_out_quad, delay=angulo/90,
                             on_complete=on_complete_movimiento)
        tween_y = TweenAvanzado(particula, 'y', y_final, 2.0, 
                             FuncionesTweening.ease_out_quad, delay=angulo/90)
        
        sistema.agregar_tween(tween_x)
        sistema.agregar_tween(tween_y)
    
    for i, particula in enumerate(particulas):
        angulo = i * 45
        crear_animacion_circular(particula, angulo, 200)
    
    for particula in particulas:
        tween_tamano = Tween(particula, 'tamano', 8, 1.5, 
                             FuncionesTweening.ease_in_out_quad, delay=0)
        sistema.agregar_tween(tween_tamano)
    
    ejecutando = True
    reiniciar_evento = False
    
    while ejecutando:
        dt = reloj.tick(FPS) / 1000.0
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return
                elif evento.key == pygame.K_r:
                    demostracion_sistema_avanzado()
                    return
            elif evento.type == pygame.USEREVENT:
                reiniciar_evento = True
        
        if reiniciar_evento:
            demostracion_sistema_avanzado()
            return
        
        sistema.actualizar(dt)
        
        ventana.fill(NEGRO)
        
        for particula in particulas:
            particula.dibujar(ventana)
        
        texto_titulo = fuente_grande.render("Sistema Avanzado de Tweening", True, BLANCO)
        ventana.blit(texto_titulo, (ANCHO//2 - texto_titulo.get_width()//2, 20))
        
        particulas_activas = sum(1 for p in particulas if p.activa)
        info_lines = [
            f"Tiempo: {sistema.tiempo_total:.1f}s",
            f"Partículas activas: {particulas_activas}/8",
            "Sistema con callbacks y animaciones encadenadas",
            "R: Reiniciar manual | ESC: Volver al menú"
        ]
        
        for i, linea in enumerate(info_lines):
            texto = fuente_pequena.render(linea, True, BLANCO)
            ventana.blit(texto, (20, 80 + i * 22))
        
        pygame.display.flip()


# =========== funcion de rectangulocuadrado

def demostracion_rectangulo_a_cuadrado():
    """
    Demostración de Rectángulo -> Cuadrado -> Mover -> Explosión
    """
    
    # --- Definir formas ---
    ancho_rect, alto_rect = 300, 150
    tam_cuadrado = 200
    desplazamiento_x = 200
    
    forma_inicial = [
        (ANCHO//2 - ancho_rect//2, ALTO//2 - alto_rect//2),
        (ANCHO//2 + ancho_rect//2, ALTO//2 - alto_rect//2),
        (ANCHO//2 + ancho_rect//2, ALTO//2 + alto_rect//2),
        (ANCHO//2 - ancho_rect//2, ALTO//2 + alto_rect//2)
    ]
    
    forma_media = [
        (ANCHO//2 - tam_cuadrado//2, ALTO//2 - tam_cuadrado//2),
        (ANCHO//2 + tam_cuadrado//2, ALTO//2 - tam_cuadrado//2),
        (ANCHO//2 + tam_cuadrado//2, ALTO//2 + tam_cuadrado//2),
        (ANCHO//2 - tam_cuadrado//2, ALTO//2 + tam_cuadrado//2)
    ]
    
    forma_final = [
        (p[0] + desplazamiento_x, p[1]) for p in forma_media
    ]
    
    # Centro final para la explosión
    centro_explosion_x = ANCHO//2 + desplazamiento_x
    centro_explosion_y = ALTO//2
    
    # --- Configurar sistema de Tweening ---
    sistema = SistemaTweening()
    
    shape_tween_1 = ShapeTween(forma_inicial, forma_media, duracion=2.0, 
                               funcion_easing=FuncionesTweening.ease_in_out_quad)
    
    shape_tween_2 = ShapeTween(forma_media, forma_final, duracion=1.5, 
                               funcion_easing=FuncionesTweening.lineal)
    
    sistema.agregar_shape_tween(shape_tween_1)
    
    # --- Variables de estado ---
    ejecutando = True
    mostrar_puntos = True
    tween_2_iniciado = False
    particulas_lanzadas = False # NUEVO
    particulas = []             # NUEVO
    reiniciar_evento = False    # NUEVO

    # NUEVO: Función helper para lanzar partículas (copiada y adaptada de Opción 3)
    def lanzar_particulas(centro_x, centro_y):
        nonlocal particulas_lanzadas, particulas, sistema
        particulas_lanzadas = True
        
        particulas = []
        for i in range(8):
            color = [ROJO, VERDE, AZUL, AMARILLO, MORADO, NARANJA, CIAN, ROSA][i % 8]
            particula = Particula(centro_x, centro_y, color)
            particulas.append(particula)

        def crear_animacion_circular(particula, angulo, radio):
            radianes = math.radians(angulo)
            x_final = centro_x + math.cos(radianes) * radio
            y_final = centro_y + math.sin(radianes) * radio

            def on_complete_desvanecimiento():
                particula.activa = False
                if all(not p.activa for p in particulas):
                    # Reiniciar esta demo
                    pygame.time.set_timer(pygame.USEREVENT, 500, True) 

            def on_complete_movimiento():
                tween_alpha = TweenAvanzado(particula, 'alpha', 0, 1.0, 
                                         FuncionesTweening.ease_in_quad, delay=0.2,
                                         on_complete=on_complete_desvanecimiento)
                sistema.agregar_tween(tween_alpha)

            tween_x = TweenAvanzado(particula, 'x', x_final, 1.0, 
                                   FuncionesTweening.ease_out_quad, delay=angulo/180,
                                   on_complete=on_complete_movimiento)
            tween_y = TweenAvanzado(particula, 'y', y_final, 1.0, 
                                   FuncionesTweening.ease_out_quad, delay=angulo/180)
            tween_tamano = Tween(particula, 'tamano', 8, 0.8, 
                                 FuncionesTweening.ease_in_out_quad, delay=0)

            sistema.agregar_tween(tween_x)
            sistema.agregar_tween(tween_y)
            sistema.agregar_tween(tween_tamano)

        for i, particula in enumerate(particulas):
            angulo = i * 45
            crear_animacion_circular(particula, angulo, 150) # Radio de explosión

    # --- Bucle principal ---
    while ejecutando:
        dt = reloj.tick(FPS) / 1000.0
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return
                elif evento.key == pygame.K_r:
                    demostracion_rectangulo_a_cuadrado()
                    return
                elif evento.key == pygame.K_p:
                    mostrar_puntos = not mostrar_puntos
            elif evento.type == pygame.USEREVENT: # NUEVO
                reiniciar_evento = True
        
        if reiniciar_evento: # NUEVO
            demostracion_rectangulo_a_cuadrado()
            return
            
        sistema.actualizar(dt)
        
        # --- Lógica de encadenamiento ---
        if shape_tween_1.completado and not tween_2_iniciado:
            sistema.agregar_shape_tween(shape_tween_2)
            tween_2_iniciado = True
        
        # NUEVO: Encadenar partículas
        if shape_tween_2.completado and not particulas_lanzadas:
            lanzar_particulas(centro_explosion_x, centro_explosion_y)

        # --- Dibujado ---
        ventana.fill(NEGRO)
        
        forma_a_dibujar = shape_tween_2.forma_actual if tween_2_iniciado else shape_tween_1.forma_actual
        
        # Ocultar el cuadrado cuando explota
        if not particulas_lanzadas:
            pygame.draw.polygon(ventana, NARANJA, forma_a_dibujar)
            pygame.draw.polygon(ventana, BLANCO, forma_a_dibujar, 2)
            
            if mostrar_puntos:
                for punto in forma_a_dibujar:
                    pygame.draw.circle(ventana, BLANCO, (int(punto[0]), int(punto[1])), 4)
        
        # NUEVO: Dibujar partículas
        for particula in particulas:
            particula.dibujar(ventana)

        # Información
        if not tween_2_iniciado:
            titulo = "Rectángulo → Cuadrado"
        elif not shape_tween_2.completado:
            titulo = "Moviendo Cuadrado (Lineal)"
        elif not particulas_lanzadas:
             titulo = "Moviendo Cuadrado (Lineal)" # Frame de transición
        else:
            titulo = "¡Explosión!"

        texto_titulo = fuente_grande.render(titulo, True, BLANCO)
        ventana.blit(texto_titulo, (ANCHO//2 - texto_titulo.get_width()//2, 20))
        
        info_lines = [
            "P: Mostrar/Ocultar puntos | R: Reiniciar | ESC: Volver"
        ]
        for i, linea in enumerate(info_lines):
            texto = fuente_pequena.render(linea, True, BLANCO)
            ventana.blit(texto, (20, ALTO - 60 + i * 25))
        
        pygame.display.flip()
        
        # NUEVO: El reinicio ahora es manejado por el callback de las partículas

# ======


def menu_principal_clase2_parte2():
    """Menú principal para la parte 2 de Tweening"""
    
    opciones = [
        ("1. Shape Tween - Transformación de Formas", demostracion_shape_tween),
        ("2. Tweens Secuenciales y Paralelos", demostracion_tweening_secuencial),
        ("3. Sistema Avanzado con Callbacks", demostracion_sistema_avanzado),
        ("4. Salir", None),
        ("5. Secuencia Completa (Shape + Move + FX)", demostracion_rectangulo_a_cuadrado) # NUEVO: Texto actualizado
    ]
    
    while True:
        ventana.fill(NEGRO)
        
        titulo = fuente_grande.render("CLASE 2: TWEENING - PARTE 2", True, BLANCO)
        ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 50))
        
        subtitulo = fuente_mediana.render("Técnicas Avanzadas de Interpolación", True, VERDE)
        ventana.blit(subtitulo, (ANCHO//2 - subtitulo.get_width()//2, 100))
        
        for i, (texto, _) in enumerate(opciones):
            color = CIAN
            if i == 3: # Opción "Salir"
                color = ROJO
            render = fuente_mediana.render(texto, True, color)
            ventana.blit(render, (ANCHO//2 - render.get_width()//2, 180 + i * 60))
        
        descripciones = [
            "Shape Tween: Interpolación entre formas diferentes",
            "Secuencial/Paralelo: Control de timing de animaciones", 
            "Sistema Avanzado: Callbacks y animaciones encadenadas"
        ]
        
        for i, desc in enumerate(descripciones):
            texto = fuente_pequena.render(desc, True, AMARILLO)
            ventana.blit(texto, (ANCHO//2 - texto.get_width()//2, 450 + i * 30))
        
        instrucciones = fuente_pequena.render("Presiona 1-5 para seleccionar una opción", True, BLANCO)
        ventana.blit(instrucciones, (ANCHO//2 - instrucciones.get_width()//2, ALTO - 50))
        
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    demostracion_shape_tween()
                elif evento.key == pygame.K_2:
                    demostracion_tweening_secuencial()
                elif evento.key == pygame.K_3:
                    demostracion_sistema_avanzado()
                elif evento.key == pygame.K_4 or evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif evento.key == pygame.K_5:
                    demostracion_rectangulo_a_cuadrado()

# Ejecutar el menú principal
if __name__ == "__main__":
    menu_principal_clase2_parte2()


