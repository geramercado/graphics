# Clase2_Tweening_Completo_CORREGIDO_OPCION2.py
# Gerardo Mercado Hurtado
# Raúl Martínez Martínez 
import pygame
import math
import sys

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
ANCHO, ALTO = 1000, 700
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Clase 2: Tweening - Interpolación y Easing")

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

# Fuentes
fuente_grande = pygame.font.Font(None, 36)
fuente_mediana = pygame.font.Font(None, 28)
fuente_pequena = pygame.font.Font(None, 22)

reloj = pygame.time.Clock()
FPS = 60

class FuncionesTweening:
    @staticmethod
    def lineal(t):
        """Interpolación lineal simple"""
        return t
    
    @staticmethod
    def ease_in_quad(t):
        """Aceleración cuadrática"""
        return t * t
    
    @staticmethod
    def ease_out_quad(t):
        """Desaceleración cuadrática"""
        return 1 - (1 - t) * (1 - t)
    
    @staticmethod
    def ease_in_out_quad(t):
        """Acelera y desacelera cuadráticamente"""
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
    def ease_out_bounce(t):
        """Rebote al final"""
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
        if t == 0 or t == 1:
            return t
        return math.sin(13 * math.pi / 2 * t) * math.pow(2, 10 * (t - 1))

def interpolacion_lineal(inicio, fin, progreso):
    """Interpolación lineal entre dos valores (maneja tuplas para colores)"""
    if isinstance(inicio, (tuple, list)) and isinstance(fin, (tuple, list)):
        # Interpolación para colores (tuplas)
        return tuple(
            int(inicio[i] + (fin[i] - inicio[i]) * progreso)
            for i in range(min(len(inicio), len(fin)))
        )
    else:
        # Interpolación para números normales
        return inicio + (fin - inicio) * progreso

class ObjetoAnimado:
    def __init__(self, x, y, color, radio=20):
        self.x = x
        self.y = y
        self.color = color
        self.radio = radio
        self.alpha = 255
        self.escala = 1.0
        self.rotacion = 0
    
    def dibujar(self, superficie):
        # Crear superficie para alpha
        surf = pygame.Surface((self.radio * 2, self.radio * 2), pygame.SRCALPHA)
        
        # Dibujar círculo con alpha
        color_con_alpha = (*self.color, int(self.alpha))
        pygame.draw.circle(surf, color_con_alpha, (self.radio, self.radio), self.radio)
        
        # Aplicar escala
        if self.escala != 1.0:
            nuevo_tamano = int(self.radio * 2 * self.escala)
            surf = pygame.transform.scale(surf, (nuevo_tamano, nuevo_tamano))
        
        # Aplicar rotación
        if self.rotacion != 0:
            surf = pygame.transform.rotate(surf, self.rotacion)
        
        # Dibujar en posición
        rect = surf.get_rect(center=(self.x, self.y))
        superficie.blit(surf, rect)

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
                self.tiempo_transcurrido = 0  # Resetear tiempo después del delay
            return
        
        progreso = self.tiempo_transcurrido / self.duracion
        
        if progreso >= 1:
            progreso = 1
            self.completado = True
        
        # Aplicar función de easing
        progreso_suavizado = self.funcion_easing(progreso)
        
        # Calcular valor interpolado
        valor_actual = interpolacion_lineal(
            self.valor_inicial, 
            self.valor_final, 
            progreso_suavizado
        )
        
        # Aplicar al objeto
        setattr(self.objeto, self.propiedad, valor_actual)

def demostracion_motion_tween():
    """Demostración de interpolación de movimiento con diferentes easings"""
    
    # Crear objetos
    objetos = [
        ObjetoAnimado(100, 100, ROJO),      # Lineal
        ObjetoAnimado(100, 180, VERDE),     # Ease In
        ObjetoAnimado(100, 260, AZUL),      # Ease Out
        ObjetoAnimado(100, 340, AMARILLO),  # Ease In Out
        ObjetoAnimado(100, 420, MORADO),    # Bounce
        ObjetoAnimado(100, 500, NARANJA)    # Elastic
    ]
    
    funciones = [
        ("Lineal", FuncionesTweening.lineal),
        ("Ease In", FuncionesTweening.ease_in_quad),
        ("Ease Out", FuncionesTweening.ease_out_quad),
        ("Ease In Out", FuncionesTweening.ease_in_out_quad),
        ("Bounce", FuncionesTweening.ease_out_bounce),
        ("Elastic", FuncionesTweening.elastic)
    ]
    
    tweens = []
    tiempo_entre_animaciones = 1.0  # segundos
    
    # Configurar tweens
    for i, (objeto, (nombre, funcion)) in enumerate(zip(objetos, funciones)):
        tween = Tween(
            objeto=objeto,
            propiedad='x',
            valor_final=ANCHO - 100,
            duracion=3.0,
            funcion_easing=funcion,
            delay=i * tiempo_entre_animaciones  # Usar delay en lugar de tiempo negativo
        )
        tweens.append((nombre, tween))
    
    # Variables de control
    ejecutando = True
    tiempo_total = 0
    
    while ejecutando:
        dt = reloj.tick(FPS) / 1000.0  # Delta time en segundos
        tiempo_total += dt
        
        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return
                elif evento.key == pygame.K_r:  # Reiniciar
                    demostracion_motion_tween()
                    return
        
        # Actualizar tweens
        for nombre, tween in tweens:
            tween.actualizar(dt)
        
        # Dibujado
        ventana.fill(NEGRO)
        
        # Dibujar objetos
        for i, (objeto, (nombre, _)) in enumerate(zip(objetos, tweens)):
            objeto.dibujar(ventana)
            
            # Dibujar información
            texto = fuente_pequena.render(nombre, True, BLANCO)
            ventana.blit(texto, (objeto.x - texto.get_width() // 2, objeto.y + 30))
            
            # Dibujar línea de referencia
            pygame.draw.line(ventana, (100, 100, 100), (100, objeto.y), (ANCHO - 100, objeto.y), 1)
        
        # Información general
        texto_tiempo = fuente_mediana.render(f"Tiempo: {tiempo_total:.1f}s", True, BLANCO)
        ventana.blit(texto_tiempo, (20, 20))
        
        texto_instrucciones = fuente_pequena.render("R: Reiniciar animaciones | ESC: Volver al menú", True, BLANCO)
        ventana.blit(texto_instrucciones, (20, ALTO - 30))
        
        pygame.display.flip()
        
        # Reiniciar ciclo
        if tiempo_total > 15:  # Reiniciar después de 15 segundos
            demostracion_motion_tween()
            return

class CuboAnimado:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = ROJO
        self.ancho = 60
        self.alto = 60
        self.rotacion = 0
        self.alpha = 255
        self.escala = 1.0
    
    def dibujar(self, superficie):
        # Crear superficie para transformaciones
        surf = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        
        # Dibujar cubo con alpha
        color_con_alpha = (*self.color, int(self.alpha))
        pygame.draw.rect(surf, color_con_alpha, (0, 0, self.ancho, self.alto), border_radius=8)
        
        # Dibujar detalles
        pygame.draw.rect(surf, (255, 255, 255, int(self.alpha)), 
                       (10, 10, self.ancho-20, self.alto-20), 2, border_radius=4)
        
        # Aplicar escala
        if self.escala != 1.0:
            nuevo_ancho = int(self.ancho * self.escala)
            nuevo_alto = int(self.alto * self.escala)
            surf = pygame.transform.scale(surf, (nuevo_ancho, nuevo_alto))
        
        # Aplicar rotación
        if self.rotacion != 0:
            surf = pygame.transform.rotate(surf, self.rotacion)
        
        # Dibujar en posición
        rect = surf.get_rect(center=(self.x, self.y))
        superficie.blit(surf, rect)

class SistemaTweening:
    def __init__(self):
        self.tweens = []
        self.tiempo_total = 0
    
    def agregar_tween(self, tween):
        self.tweens.append(tween)
    
    def actualizar(self, dt):
        self.tiempo_total += dt
        for tween in self.tweens:
            tween.actualizar(dt)
    
    def todos_completados(self):
        return all(tween.completado for tween in self.tweens)

def demostracion_tweening_complejo():
    """Demostración de tweening aplicado a múltiples propiedades simultáneamente"""
    
    # Crear cubo
    cubo = CuboAnimado(ANCHO // 2, ALTO // 2)
    
    # Crear sistema de tweening
    sistema = SistemaTweening()
    
    # Secuencia de animaciones con delays apropiados
    secuencia = [
        # Fase 1: Movimiento y cambio de color (inician juntos)
        {'propiedad': 'x', 'valor': 200, 'duracion': 2.0, 'easing': FuncionesTweening.ease_out_quad, 'delay': 0},
        {'propiedad': 'color', 'valor': VERDE, 'duracion': 2.0, 'easing': FuncionesTweening.lineal, 'delay': 0},
        
        # Fase 2: Rotación y escala (inician después de la fase 1)
        {'propiedad': 'rotacion', 'valor': 360, 'duracion': 2.0, 'easing': FuncionesTweening.ease_in_out_quad, 'delay': 2.0},
        {'propiedad': 'escala', 'valor': 1.5, 'duracion': 1.0, 'easing': FuncionesTweening.ease_out_quad, 'delay': 2.0},
        
        # Fase 3: Movimiento y transparencia (inician después de la fase 2)
        {'propiedad': 'y', 'valor': 500, 'duracion': 1.5, 'easing': FuncionesTweening.ease_in_back, 'delay': 4.0},
        {'propiedad': 'alpha', 'valor': 100, 'duracion': 1.5, 'easing': FuncionesTweening.lineal, 'delay': 4.0},
        
        # Fase 4: Regreso a estado inicial (inician después de la fase 3)
        {'propiedad': 'x', 'valor': ANCHO // 2, 'duracion': 2.0, 'easing': FuncionesTweening.ease_out_bounce, 'delay': 5.5},
        {'propiedad': 'y', 'valor': ALTO // 2, 'duracion': 2.0, 'easing': FuncionesTweening.ease_out_bounce, 'delay': 5.5},
        {'propiedad': 'color', 'valor': ROJO, 'duracion': 2.0, 'easing': FuncionesTweening.lineal, 'delay': 5.5},
        {'propiedad': 'rotacion', 'valor': 0, 'duracion': 1.0, 'easing': FuncionesTweening.lineal, 'delay': 5.5},
        {'propiedad': 'escala', 'valor': 1.0, 'duracion': 1.0, 'easing': FuncionesTweening.lineal, 'delay': 5.5},
        {'propiedad': 'alpha', 'valor': 255, 'duracion': 1.0, 'easing': FuncionesTweening.lineal, 'delay': 5.5},
    ]
    
    # Configurar todos los tweens
    for anim in secuencia:
        tween = Tween(
            objeto=cubo,
            propiedad=anim['propiedad'],
            valor_final=anim['valor'],
            duracion=anim['duracion'],
            funcion_easing=anim['easing'],
            delay=anim['delay']
        )
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
                    demostracion_tweening_complejo()
                    return
        
        # Actualizar sistema
        sistema.actualizar(dt)
        
        # Dibujado
        ventana.fill(NEGRO)
        
        # Dibujar cubo
        cubo.dibujar(ventana)
        
        # Información
        texto_titulo = fuente_grande.render("Tweening Múltiples Propiedades", True, BLANCO)
        ventana.blit(texto_titulo, (ANCHO//2 - texto_titulo.get_width()//2, 20))
        
        # Mostrar estado actual de las propiedades
        info_lines = [
            f"Posición: ({cubo.x:.0f}, {cubo.y:.0f})",
            f"Rotación: {cubo.rotacion:.0f}°",
            f"Escala: {cubo.escala:.1f}",
            f"Alpha: {cubo.alpha:.0f}",
            f"Tiempo: {sistema.tiempo_total:.1f}s",
            f"Color: {cubo.color}",
            "",
            "Secuencia:",
            "0-2s: Mover + Cambiar color",
            "2-4s: Rotar + Escalar", 
            "4-5.5s: Mover Y + Transparencia",
            "5.5s+: Regresar al inicio"
        ]
        
        for i, linea in enumerate(info_lines):
            texto = fuente_pequena.render(linea, True, BLANCO)
            ventana.blit(texto, (20, 80 + i * 20))
        
        # Mostrar tweens activos
        tweens_activos = [t for t in sistema.tweens if not t.completado and not t.en_delay]
        texto_activos = fuente_pequena.render(f"Tweens activos: {len(tweens_activos)}", True, VERDE)
        ventana.blit(texto_activos, (ANCHO - 200, 80))
        
        texto_instrucciones = fuente_pequena.render("R: Reiniciar | ESC: Volver al menú", True, BLANCO)
        ventana.blit(texto_instrucciones, (20, ALTO - 30))
        
        pygame.display.flip()
        
        # Reiniciar después de completar ciclo
        if sistema.tiempo_total > 12 and sistema.todos_completados():
            demostracion_tweening_complejo()
            return

class SistemaTweeningCompleto:
    def __init__(self):
        self.objetos = []
        self.tweens = []
        self.crear_escena()
    
    def crear_escena(self):
        # Crear objetos en diferentes posiciones
        colores = [ROJO, VERDE, AZUL, AMARILLO, MORADO, NARANJA]
        posiciones_iniciales = [
            (150, 150), (150, 300), (150, 450),
            (ANCHO-150, 150), (ANCHO-150, 300), (ANCHO-150, 450)
        ]
        
        for i, (pos, color) in enumerate(zip(posiciones_iniciales, colores)):
            obj = ObjetoAnimado(pos[0], pos[1], color, 25)
            self.objetos.append(obj)
            
            # Configurar animaciones diferentes para cada objeto con delays
            if i == 0:  # Movimiento horizontal con bounce
                tween = Tween(obj, 'x', ANCHO-150, 4.0, FuncionesTweening.ease_out_bounce, delay=0)
            elif i == 1:  # Movimiento vertical elástico
                tween = Tween(obj, 'y', ALTO-150, 4.0, FuncionesTweening.elastic, delay=0.5)
            elif i == 2:  # Cambio de escala
                tween = Tween(obj, 'escala', 2.5, 3.0, FuncionesTweening.ease_in_out_quad, delay=1.0)
            elif i == 3:  # Rotación
                tween = Tween(obj, 'rotacion', 720, 5.0, FuncionesTweening.lineal, delay=1.5)
            elif i == 4:  # Transparencia
                tween = Tween(obj, 'alpha', 50, 2.0, FuncionesTweening.ease_in_out_quad, delay=2.0)
            else:  # Movimiento circular aproximado
                tween = Tween(obj, 'x', 150, 4.0, FuncionesTweening.ease_in_out_quad, delay=2.5)
            
            self.tweens.append(tween)
    
    def actualizar(self, dt):
        for tween in self.tweens:
            tween.actualizar(dt)
        
        # Reiniciar tweens cuando se completen
        if all(tween.completado for tween in self.tweens):
            self.reiniciar_animaciones()
    
    def reiniciar_animaciones(self):
        for tween in self.tweens:
            tween.tiempo_transcurrido = 0
            tween.completado = False
            tween.en_delay = tween.delay > 0
            tween.valor_inicial = getattr(tween.objeto, tween.propiedad)
    
    def dibujar(self, superficie):
        for obj in self.objetos:
            obj.dibujar(superficie)

def ejercicio_final_clase2():
    """Ejercicio final que integra todos los conceptos de tweening"""
    
    # Sistema principal
    sistema = SistemaTweeningCompleto()
    tiempo_total = 0
    
    ejecutando = True
    while ejecutando:
        dt = reloj.tick(FPS) / 1000.0
        tiempo_total += dt
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return
        
        # Actualizar sistema
        sistema.actualizar(dt)
        
        # Dibujado
        ventana.fill(NEGRO)
        
        # Dibujar objetos
        sistema.dibujar(ventana)
        
        # Información
        texto_titulo = fuente_grande.render("Sistema Completo de Tweening", True, BLANCO)
        ventana.blit(texto_titulo, (ANCHO//2 - texto_titulo.get_width()//2, 20))
        
        info_lines = [
            "Diferentes tipos de interpolación:",
            "• Rojo: Movimiento con Bounce",
            "• Verde: Movimiento Elástico", 
            "• Azul: Cambio de Escala",
            "• Amarillo: Rotación Continua",
            "• Morado: Transparencia",
            "• Naranja: Movimiento Circular"
        ]
        
        for i, linea in enumerate(info_lines):
            color = BLANCO if i == 0 else (200, 200, 200)
            texto = fuente_pequena.render(linea, True, color)
            ventana.blit(texto, (20, 80 + i * 25))
        
        texto_tiempo = fuente_mediana.render(f"Tiempo: {tiempo_total:.1f}s", True, BLANCO)
        ventana.blit(texto_tiempo, (ANCHO - 150, 20))
        
        texto_instrucciones = fuente_pequena.render("ESC: Volver al menú", True, BLANCO)
        ventana.blit(texto_instrucciones, (20, ALTO - 30))
        
        pygame.display.flip()



def mostrar_triangulo_central():
    """Muestra un triángulo amarillo y un cuadrado al lado derecho con animaciones"""
    
    # --- Configuración inicial ---
    centro_x, centro_y = ANCHO // 2, ALTO // 2
    tamaño = 100
    lado_cuadrado = 120
    distancia = 150

    # Posiciones iniciales
    x_inicial_triangulo = 150
    x_inicial_cuadrado = 150

    # Objetos "simulados" para tween
    class Figura:
        def __init__(self, x):
            self.x = x

    triangulo = Figura(x_inicial_triangulo)
    cuadrado = Figura(x_inicial_cuadrado)

    # Crear tweens
    tween_triangulo = Tween(
        objeto=triangulo,
        propiedad='x',
        valor_final=ANCHO - 250,
        duracion=3.0,
        funcion_easing=FuncionesTweening.lineal
    )

    tween_cuadrado = Tween(
        objeto=cuadrado,
        propiedad='x',
        valor_final=ANCHO - 250,
        duracion=3.0,
        funcion_easing=FuncionesTweening.ease_in_quad
    )

    # Control de animación
    ejecutando = True
    tiempo_total = 0

    while ejecutando:
        dt = reloj.tick(FPS) / 1000.0
        tiempo_total += dt

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return  # Regresar al menú

        # Actualizar tweens
        tween_triangulo.actualizar(dt)
        tween_cuadrado.actualizar(dt)

        # --- Dibujo en pantalla ---
        ventana.fill((0, 0, 0))

        # Dibujar triángulo con posición animada
        puntos_triangulo = [
            (triangulo.x, centro_y - tamaño),          # vértice superior
            (triangulo.x - tamaño, centro_y + tamaño), # esquina inferior izquierda
            (triangulo.x + tamaño, centro_y + tamaño)  # esquina inferior derecha
        ]
        pygame.draw.polygon(ventana, (255, 255, 0), puntos_triangulo)

        # Dibujar cuadrado con posición animada
        cuadrado_x = cuadrado.x + distancia
        cuadrado_y = centro_y - lado_cuadrado // 2
        pygame.draw.rect(
            ventana,
            (0, 200, 255),
            (cuadrado_x, cuadrado_y, lado_cuadrado, lado_cuadrado),
            border_radius=8
        )

        # Texto de información
        texto = fuente_pequena.render("ESC: Volver al menú", True, BLANCO)
        ventana.blit(texto, (20, ALTO - 30))

        texto2 = fuente_pequena.render("Triángulo: Lineal | Cuadrado: Ease In", True, VERDE)
        ventana.blit(texto2, (20, 20))

        pygame.display.flip()

        # Reinicio automático después de 6 segundos
        if tiempo_total > 6:
            mostrar_triangulo_central()
            return


        
def menu_principal_clase2():
    """Menú principal para seleccionar demostraciones"""
    
    opciones = [
        ("0. Mostrar Triángulo Amarillo", mostrar_triangulo_central),
        ("1. Motion Tween - Diferentes Easings", demostracion_motion_tween),
        ("2. Tweening Múltiples Propiedades", demostracion_tweening_complejo),
        ("3. Ejercicio Final Integrador", ejercicio_final_clase2),
        ("4. Salir", None)
    ]
    
    while True:
        ventana.fill(NEGRO)
        
        # Título
        titulo = fuente_grande.render("CLASE 2: TWEENING - INTERPOLACIÓN", True, BLANCO)
        ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 50))
        
        subtitulo = fuente_mediana.render("Selecciona una demostración:", True, VERDE)
        ventana.blit(subtitulo, (ANCHO//2 - subtitulo.get_width()//2, 100))
        
        # Opciones
        for i, (texto, _) in enumerate(opciones):
            color = CIAN
            if i == len(opciones) - 1:  # Última opción (Salir)
                color = ROJO
            render = fuente_mediana.render(texto, True, color)
            ventana.blit(render, (ANCHO//2 - render.get_width()//2, 180 + i * 60))
        
        # Instrucciones
        instrucciones = fuente_pequena.render("Presiona 0-4 para seleccionar una opción", True, AMARILLO)
        ventana.blit(instrucciones, (ANCHO//2 - instrucciones.get_width()//2, ALTO - 50))
        
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_0:
                    mostrar_triangulo_central()
                elif evento.key == pygame.K_1:
                    demostracion_motion_tween()
                elif evento.key == pygame.K_2:
                    demostracion_tweening_complejo()
                elif evento.key == pygame.K_3:
                    ejercicio_final_clase2()
                elif evento.key == pygame.K_4 or evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


# Ejecutar el menú principal
if __name__ == "__main__":
    menu_principal_clase2()
