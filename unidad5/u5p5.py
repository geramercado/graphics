# importar bibliotecas
import random
import pygame
import math
import sys

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
ANCHO, ALTO = 1000, 700
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Onion Skinning, Animación con Referencias Gerardo, Raúl")

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

#Colores aplicados en cada salto
COLORES_ANIMACION = [ROJO, VERDE, AZUL, AMARILLO, MORADO, CIAN, NARANJA, ROSA] 

# Fuentes
fuente_grande = pygame.font.Font(None, 36)
fuente_mediana = pygame.font.Font(None, 28)
fuente_pequena = pygame.font.Font(None, 22)

reloj = pygame.time.Clock()
FPS = 60

class FuncionesInterpolacion:
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

class SistemaOnionSkinning:
    """Sistema completo de Onion Skinning para animación"""
    
    def __init__(self, max_frames=10):
        self.frames = []  # Almacena todos los frames de la animación
        self.frame_actual = 0
        self.max_frames = max_frames
        self.mostrar_onion_skin = True
        self.cantidad_frames_mostrar = 3  # Cuántos frames mostrar como referencia
        self.alpha_base = 80  # Transparencia base para frames de referencia
        
    def agregar_frame(self, datos_frame):
        """Agrega un nuevo frame a la animación"""
        if len(self.frames) >= self.max_frames:
            self.frames.pop(0)  # Remover frame más viejo si excede el máximo
        self.frames.append(datos_frame.copy())
        self.frame_actual = len(self.frames) - 1
    
    def obtener_frames_referencia(self):
        """Obtiene los frames a mostrar como referencia (onion skinning)"""
        if not self.mostrar_onion_skin or len(self.frames) <= 1:
            return []
        
        frames_referencia = []
        
        # Obtener frames anteriores (hasta la cantidad configurada)
        inicio = max(0, self.frame_actual - self.cantidad_frames_mostrar)
        for i in range(inicio, self.frame_actual):
            if i < len(self.frames):
                # Calcular alpha basado en qué tan lejano está el frame
                distancia = self.frame_actual - i
                alpha = max(20, self.alpha_base - (distancia - 1) * 20)
                frames_referencia.append({
                    'datos': self.frames[i],
                    'alpha': alpha,
                    'tipo': 'anterior',
                    'distancia': distancia
                })
        
        return frames_referencia
    
    def dibujar_onion_skin(self, superficie, dibujar_frame_func):
        """Dibuja los frames de referencia con onion skinning"""
        if not self.mostrar_onion_skin:
            return
        
        frames_referencia = self.obtener_frames_referencia()
        
        for frame_ref in frames_referencia:
            # Crear superficie temporal para aplicar alpha
            surf_temp = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            
            # Dibujar el frame de referencia en la superficie temporal
            dibujar_frame_func(surf_temp, frame_ref['datos'], VERDE)
            
            # Aplicar alpha y dibujar en la superficie principal
            surf_temp.set_alpha(frame_ref['alpha'])
            superficie.blit(surf_temp, (0, 0))
    
    def dibujar_frame_actual(self, superficie, datos_frame, color=ROJO):
        """Dibuja el frame actual (siempre opaco)"""
        if datos_frame:
            # Dibujar el frame actual
            if 'personaje' in datos_frame:
                self._dibujar_personaje(superficie, datos_frame['personaje'], color)
            elif 'forma' in datos_frame:
                self._dibujar_forma(superficie, datos_frame['forma'], color)
    
    def _dibujar_personaje(self, superficie, personaje, color):
        """Dibuja un personaje stick figure"""
        # Cabeza
        pygame.draw.circle(superficie, color, (int(personaje['x']), int(personaje['y'] - 30)), 80)
        
        # Cuerpo
        pygame.draw.line(superficie, color, 
                         (personaje['x'], personaje['y'] - 15), 
                         (personaje['x'], personaje['y'] + 20), 3)
        
        # Brazos
        angulo_brazos = personaje.get('angulo_brazos', 0)
        brazo_longitud = 250
        
        # Brazo izquierdo
        angulo_izq = math.radians(135 + angulo_brazos)
        x_izq = personaje['x'] + brazo_longitud * math.cos(angulo_izq)
        y_izq = personaje['y'] + brazo_longitud * math.sin(angulo_izq)
        pygame.draw.line(superficie, color, 
                         (personaje['x'], personaje['y']), 
                         (x_izq, y_izq), 3)
        
        # Brazo derecho
        angulo_der = math.radians(45 - angulo_brazos)
        x_der = personaje['x'] + brazo_longitud * math.cos(angulo_der)
        y_der = personaje['y'] + brazo_longitud * math.sin(angulo_der)
        pygame.draw.line(superficie, color, 
                         (personaje['x'], personaje['y']), 
                         (x_der, y_der), 3)
        
        # Piernas
        angulo_piernas = personaje.get('angulo_piernas', 0)
        pierna_longitud = 30
        
        # Pierna izquierda
        angulo_pierna_izq = math.radians(225 + angulo_piernas)
        x_pierna_izq = personaje['x'] + pierna_longitud * math.cos(angulo_pierna_izq)
        y_pierna_izq = personaje['y'] + 20 + pierna_longitud * math.sin(angulo_pierna_izq)
        pygame.draw.line(superficie, color, 
                         (personaje['x'], personaje['y'] + 20), 
                         (x_pierna_izq, y_pierna_izq), 3)
        
        # Pierna derecha
        angulo_pierna_der = math.radians(315 - angulo_piernas)
        x_pierna_der = personaje['x'] + pierna_longitud * math.cos(angulo_pierna_der)
        y_pierna_der = personaje['y'] + 20 + pierna_longitud * math.sin(angulo_pierna_der)
        pygame.draw.line(superficie, color, 
                         (personaje['x'], personaje['y'] + 20), 
                         (x_pierna_der, y_pierna_der), 3)
    
    def _dibujar_forma(self, superficie, forma, color):
        """Dibuja una forma geométrica"""
        if forma['tipo'] == 'circulo':
            pygame.draw.circle(superficie, color, 
                             (int(forma['x']), int(forma['y'])), 
                             forma['radio'])
        elif forma['tipo'] == 'rectangulo':
            rect = pygame.Rect(forma['x'] - forma['ancho']//2, 
                             forma['y'] - forma['alto']//2,
                             forma['ancho'], forma['alto'])
            pygame.draw.rect(superficie, color, rect)
        elif forma['tipo'] == 'poligono' and 'puntos' in forma:
            pygame.draw.polygon(superficie, color, forma['puntos'])

def demostracion_onion_basico():
    """Ciempiés moviéndose al azar, por el plano con un stickman"""
    
    sistema = SistemaOnionSkinning(max_frames=25)
    tiempo_total = 0.0
    animando = True
    
    # Parámetros del ciempies
    num_segmentos = 20
    longitud_segmento = 25
    velocidad = 150
    cambio_direccion_t = 2.5 
    
    # Posición inicial y dirección
    cabeza_x, cabeza_y = ANCHO // 2, ALTO // 2
    angulo_direccion = random.uniform(0, 2 * math.pi)
    tiempo_cambio = 0.0
    
    # Segmentos iniciales
    segmentos = []
    for i in range(num_segmentos):
        segmentos.append({'x': cabeza_x - i * longitud_segmento, 'y': cabeza_y})
    
    # mono
    stick_x = 0
    stick_y = 0
    stick_balanceo = 0.0
    stick_inclinacion = 0.0
    
    ejecutando = True
    while ejecutando:
        dt = reloj.tick(FPS) / 500.0
        tiempo_total += dt
        tiempo_cambio += dt

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return
                elif evento.key == pygame.K_o:
                    sistema.mostrar_onion_skin = not sistema.mostrar_onion_skin
                elif evento.key in (pygame.K_PLUS, pygame.K_EQUALS):
                    sistema.cantidad_frames_mostrar = min(10, sistema.cantidad_frames_mostrar + 1)
                elif evento.key == pygame.K_MINUS:
                    sistema.cantidad_frames_mostrar = max(1, sistema.cantidad_frames_mostrar - 1)
                elif evento.key == pygame.K_SPACE:
                    animando = not animando
                elif evento.key == pygame.K_r:
                    sistema.frames = []
                    tiempo_total = 0.0
                    cabeza_x, cabeza_y = ANCHO // 2, ALTO // 2
                    angulo_direccion = random.uniform(0, 2 * math.pi)
                    tiempo_cambio = 0.0

        if animando:
            # Cambiar dirección aleatoriamente de forma suave
            if tiempo_cambio > cambio_direccion_t:
                tiempo_cambio = 0
                angulo_direccion += random.uniform(-math.pi/6, math.pi/6)
                cambio_direccion_t = random.uniform(1.5, 3.5)
            
            # Movimiento de la cabeza
            cabeza_x += math.cos(angulo_direccion) * velocidad * dt
            cabeza_y += math.sin(angulo_direccion) * velocidad * dt

            # Rebote en bordes
            if cabeza_x < 50 or cabeza_x > ANCHO - 50:
                angulo_direccion = math.pi - angulo_direccion
            if cabeza_y < 50 or cabeza_y > ALTO - 50:
                angulo_direccion = -angulo_direccion

            # Actualizar posiciones de los segmentos (siguiendo al anterior)
            prev_x, prev_y = cabeza_x, cabeza_y
            for seg in segmentos:
                dx = prev_x - seg['x']
                dy = prev_y - seg['y']
                dist = math.hypot(dx, dy)
                if dist > longitud_segmento:
                    factor = longitud_segmento / dist
                    seg['x'] = prev_x - dx * factor
                    seg['y'] = prev_y - dy * factor
                prev_x, prev_y = seg['x'], seg['y']

            # Movimiento aleatorio del mono
            stick_balanceo += dt * 8
            stick_inclinacion = math.sin(stick_balanceo) * 10 + random.uniform(-5, 5)
            
            cabeza = segmentos[0]
            stick_x = cabeza['x'] + random.uniform(-4, 4)
            stick_y = cabeza['y'] - 40 + random.uniform(-3, 3)

            # Guardar frame
            if tiempo_total % 0.08 < dt:
                sistema.agregar_frame({'segmentos': [s.copy() for s in segmentos]})
        
        # Fondo
        ventana.fill(NEGRO)
        
        # Dibujar ciempies
        def dibujar_ciempies(superficie, datos, color):
            if 'segmentos' in datos:
                for i, seg in enumerate(datos['segmentos']):
                    tamaño = 18 if i == 0 else 14
                    pygame.draw.circle(superficie, color, (int(seg['x']), int(seg['y'])), tamaño)
        
        sistema.dibujar_onion_skin(ventana, dibujar_ciempies)
        dibujar_ciempies(ventana, {'segmentos': segmentos}, AZUL)
        
        # Dibujar mono
        def dibujar_stickman(superficie, x, y, inclinacion):
            cuerpo_color = BLANCO
            cabeza_radio = 8
            rotacion = math.radians(inclinacion)
            cos_r, sin_r = math.cos(rotacion), math.sin(rotacion)
            
            def rotar(px, py):
                return (x + px * cos_r - py * sin_r,
                        y + px * sin_r + py * cos_r)
            
            cabeza_p = rotar(0, -15)
            cuello = rotar(0, 0)
            cadera = rotar(0, 20)
            pierna_izq = rotar(-10, 35)
            pierna_der = rotar(10, 35)
            brazo_izq = rotar(-15, -5)
            brazo_der = rotar(15, -5)
            
            pygame.draw.circle(superficie, cuerpo_color, (int(cabeza_p[0]), int(cabeza_p[1])), cabeza_radio)
            pygame.draw.line(superficie, cuerpo_color, cuello, cadera, 3)
            pygame.draw.line(superficie, cuerpo_color, cuello, brazo_izq, 2)
            pygame.draw.line(superficie, cuerpo_color, cuello, brazo_der, 2)
            pygame.draw.line(superficie, cuerpo_color, cadera, pierna_izq, 3)
            pygame.draw.line(superficie, cuerpo_color, cadera, pierna_der, 3)
        
        dibujar_stickman(ventana, stick_x, stick_y, stick_inclinacion)
        
        # Texto
        texto_titulo = fuente_grande.render("Ciempiés con Stickman randon", True, BLANCO)
        ventana.blit(texto_titulo, (ANCHO//2 - texto_titulo.get_width()//2, 20))
        
        estado_onion = "ACTIVADO" if sistema.mostrar_onion_skin else "DESACTIVADO"
        info_lines = [
            f"Onion Skinning: {estado_onion} | Frames: {len(sistema.frames)}",
            "",
            "O: Activar/Desactivar Onion Skinning",
            "+/-: Cambiar cantidad de frames",
            "ESPACIO: Pausar/Reanudar",
            "R: Reiniciar",
            "ESC: Volver al menú"
        ]
        for i, linea in enumerate(info_lines):
            texto = fuente_pequena.render(linea, True, BLANCO)
            ventana.blit(texto, (20, ALTO - 160 + i * 25))
        
        pygame.display.flip()


#Dibuja el objeto central en la opcion 2
def dibujar_objetos_frame_onion(superficie, datos_frame, color, sistema_ref):
    """
    Dibuja los círculos y el personaje en un frame, usado para el onion skinning.
    'color' será VERDE para el onion skin y el color actual para el frame actual.
    """
    
    # Dibujar los círculos
    if 'objetos' in datos_frame:
        for obj in datos_frame['objetos']:
            # Usar COLORES_ANIMACION
            color_obj = COLORES_ANIMACION[obj['color_idx'] % len(COLORES_ANIMACION)]
            if color == VERDE: # Onion skin (contorno y color)
                pygame.draw.circle(superficie, color_obj, 
                                 (int(obj['x']), int(obj['y'])), 
                                 int(obj['radio']), 1)
            else: # Frame actual
                pygame.draw.circle(superficie, color_obj, 
                                 (int(obj['x']), int(obj['y'])), 
                                 int(obj['radio']))

    # Dibujar el personaje central (solo para onion skin)
    if 'personaje' in datos_frame and color == VERDE:
        # Usar un color fijo para el onion skin del personaje
        color_onion_personaje = CIAN
        sistema_ref._dibujar_personaje(superficie, datos_frame['personaje'], color_onion_personaje)


def demostracion_onion_animacion_compleja():
    """Demostración de Onion Skinning con animación compleja"""
    
    sistema = SistemaOnionSkinning(max_frames=30)
    tiempo_total = 0.0
    animando = True
    
    # Crear múltiples objetos para animar
    objetos_actuales = []
    num_objetos = 10
    
    for i in range(num_objetos):
        angulo = 2 * math.pi * i / num_objetos
        radio = 150
        objetos_actuales.append({
            'tipo': 'circulo',
            'x': ANCHO // 2 + radio * math.cos(angulo),
            'y': ALTO // 2 + radio * math.sin(angulo),
            'radio': 20,
            'color_idx': i,
            'fase': angulo
        })
    
    # DATOS DEL PERSONAJE CENTRAL
    personaje_central = {
        'x': ANCHO // 2,
        'y': ALTO // 2,
        'angulo_brazos': 0,
        'angulo_piernas': 0,
        'color_idx': 0 
    }
    colores_personaje = [ROJO, VERDE, AZUL, AMARILLO, MORADO, CIAN, NARANJA]
    periodo_brinco = 1.0  # Duración de un ciclo de brinco en segundos
    periodo_cambio_color = 0.5 # Duración para el cambio de color
    
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
                elif evento.key == pygame.K_o:
                    sistema.mostrar_onion_skin = not sistema.mostrar_onion_skin
                elif evento.key == pygame.K_PLUS or evento.key == pygame.K_EQUALS:
                    sistema.cantidad_frames_mostrar = min(15, sistema.cantidad_frames_mostrar + 1)
                elif evento.key == pygame.K_MINUS:
                    sistema.cantidad_frames_mostrar = max(1, sistema.cantidad_frames_mostrar - 1)
                elif evento.key == pygame.K_SPACE:
                    animando = not animando
                elif evento.key == pygame.K_r:
                    sistema.frames = []
                    tiempo_total = 0.0
                    
        if animando:
            # Actualizar animación de objetos
            for obj in objetos_actuales:
                frecuencia = 1.5
                fase = obj['fase']
                radio_base = 150
                radio_actual = radio_base + 30 * math.sin(tiempo_total * frecuencia + fase)
                
                obj['x'] = ANCHO // 2 + radio_actual * math.cos(tiempo_total * frecuencia + fase)
                obj['y'] = ALTO // 2 + radio_actual * math.sin(tiempo_total * frecuencia + fase)
                
                obj['radio'] = 15 + 10 * math.sin(tiempo_total * 2 * frecuencia + fase)
            
            #Actualiza la esfera central brinco y color
            t_norm = (tiempo_total % periodo_brinco) / periodo_brinco
            
            # Altura del brinco (interpolación)
            altura_base = ALTO // 2 + 100 # Se mueve un poco hacia abajo para centrar
            max_altura = 100
            
            if t_norm < 0.5:
                # Subiendo
                t_ease = FuncionesInterpolacion.ease_out_quad(t_norm * 2)
                personaje_central['y'] = altura_base - max_altura * t_ease
                # Brazos y piernas se preparan para el salto (encogen)
                personaje_central['angulo_brazos'] = 5 * t_norm * 2
                personaje_central['angulo_piernas'] = 10 * t_norm * 2
            else:
                # Bajando
                t_ease = FuncionesInterpolacion.ease_in_quad((t_norm - 0.5) * 2)
                personaje_central['y'] = altura_base - max_altura * (1 - t_ease)
                # Brazos y piernas se extienden al tocar el suelo
                personaje_central['angulo_brazos'] = 5 * (1 - (t_norm - 0.5) * 2)
                personaje_central['angulo_piernas'] = 10 * (1 - (t_norm - 0.5) * 2)
            
            # Cambio de color
            if tiempo_total % periodo_cambio_color < dt:
                 personaje_central['color_idx'] = (personaje_central['color_idx'] + 1) % len(colores_personaje)
            # ---------------------------------------------------
            
            # Agregar frame actual a la animación (frame key)
            if tiempo_total % 0.08 < dt: 
                sistema.agregar_frame({
                    'objetos': [obj.copy() for obj in objetos_actuales],
                    'personaje': personaje_central.copy() 
                })
        
        # Dibujado
        ventana.fill(NEGRO)
        
        # Dibujar onion skinning
        # Usamos una función lambda para pasar la referencia del sistema a la función de dibujo
        sistema.dibujar_onion_skin(ventana, lambda surf, datos, color: dibujar_objetos_frame_onion(surf, datos, color, sistema))
        
        # Dibujar frame actual (Objetos)
        for obj in objetos_actuales:
            color_obj = COLORES_ANIMACION[obj['color_idx'] % len(COLORES_ANIMACION)]
            pygame.draw.circle(ventana, color_obj, 
                             (int(obj['x']), int(obj['y'])), 
                             int(obj['radio']))
        
        # Dibujar frame actual (Personaje)
        color_personaje_actual = colores_personaje[personaje_central['color_idx']]
        # Reutilizamos el método de dibujo de la clase para el personaje actual (opaco)
        sistema._dibujar_personaje(ventana, personaje_central, color_personaje_actual)

        # Información
        texto_titulo = fuente_grande.render("Onion Skinning Complejo - Personaje Brincando y Objetos", True, BLANCO)
        ventana.blit(texto_titulo, (ANCHO//2 - texto_titulo.get_width()//2, 20))
        
        estado_onion = "ACTIVADO" if sistema.mostrar_onion_skin else "DESACTIVADO"
        info_lines = [
            f"Tiempo: {tiempo_total:.1f}s | Frames: {len(sistema.frames)}",
            f"Onion Skinning: {estado_onion} | Frames mostrados: {sistema.cantidad_frames_mostrar}",
            f"Objetos animados: {num_objetos}",
            "Personaje central (cuerpo opaco) brinca y cambia de color (referencias cian).",
            "Los objetos externos giran y cambian de tamaño (referencias contorno).",
            "",
            "Controles:",
            "O: Activar/Desactivar Onion Skinning",
            "+/-: Ajustar frames mostrados", 
            "ESPACIO: Pausar/Reanudar",
            "R: Reiniciar animación",
            "ESC: Volver al menú"
        ]
        
        for i, linea in enumerate(info_lines):
            texto = fuente_pequena.render(linea, True, BLANCO)
            ventana.blit(texto, (20, ALTO - 240 + i * 25))
        
        pygame.display.flip()

class SistemaAnimacionCuadroPorCuadro:
    """Sistema para animación cuadro por cuadro con onion skinning"""
    
    def __init__(self):
        self.frames = []
        self.frame_actual = 0
        self.editando = True
        self.mostrar_onion = True
        self.onion_frames = 2
        
    def agregar_frame(self, datos):
        if self.frame_actual < len(self.frames):
            self.frames[self.frame_actual] = datos
        else:
            self.frames.append(datos)
    
    def frame_siguiente(self):
        if self.frame_actual < len(self.frames) - 1:
            self.frame_actual += 1
        else:
            self.frame_actual = len(self.frames)
            if self.frame_actual >= 20:  # Límite de frames
                self.frame_actual = 19
    
    def frame_anterior(self):
        if self.frame_actual > 0:
            self.frame_actual -= 1
    
    def obtener_datos_actuales(self):
        if self.frame_actual < len(self.frames):
            return self.frames[self.frame_actual]
        return None
    
    def obtener_frames_onion(self):
        frames = []
        if not self.mostrar_onion:
            return frames
        
        # Frames anteriores
        for i in range(max(0, self.frame_actual - self.onion_frames), self.frame_actual):
            if i < len(self.frames):
                alpha = 100 - (self.frame_actual - i - 1) * 30
                frames.append({'datos': self.frames[i], 'alpha': max(20, alpha)})
        
        return frames

def demostracion_animacion_cuadro_por_cuadro():
    """Demostración de animación manual cuadro por cuadro con onion skinning"""
    
    sistema = SistemaAnimacionCuadroPorCuadro()
    
    # Datos iniciales
    bola_actual = {'x': ANCHO // 2, 'y': ALTO // 2, 'radio': 30}
    
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
                elif evento.key == pygame.K_RIGHT:
                    sistema.frame_siguiente()
                    if sistema.frame_actual < len(sistema.frames):
                        bola_actual = sistema.frames[sistema.frame_actual].copy()
                    else:
                        # Nuevo frame - copiar el anterior o resetear
                        if sistema.frames:
                            bola_actual = sistema.frames[-1].copy()
                        else:
                            bola_actual = {'x': ANCHO // 2, 'y': ALTO // 2, 'radio': 30}
                elif evento.key == pygame.K_LEFT:
                    sistema.frame_anterior()
                    if sistema.frame_actual < len(sistema.frames):
                        bola_actual = sistema.frames[sistema.frame_actual].copy()
                elif evento.key == pygame.K_o:
                    sistema.mostrar_onion = not sistema.mostrar_onion
                elif evento.key == pygame.K_s:
                    # Guardar frame actual
                    sistema.agregar_frame(bola_actual.copy())
                elif evento.key == pygame.K_c:
                    # Limpiar animación
                    sistema.frames = []
                    sistema.frame_actual = 0
                    bola_actual = {'x': ANCHO // 2, 'y': ALTO // 2, 'radio': 30}
            
            elif evento.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:  # Click izquierdo sostenido
                    pos = pygame.mouse.get_pos()
                    bola_actual['x'] = pos[0]
                    bola_actual['y'] = pos[1]
                    sistema.agregar_frame(bola_actual.copy())
        
        # Dibujado
        ventana.fill(NEGRO)
        
        # Dibujar onion skinning
        if sistema.mostrar_onion:
            frames_onion = sistema.obtener_frames_onion()
            for frame_ref in frames_onion:
                surf_temp = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
                datos = frame_ref['datos']
                pygame.draw.circle(surf_temp, VERDE, 
                                 (int(datos['x']), int(datos['y'])), 
                                 datos['radio'])
                surf_temp.set_alpha(frame_ref['alpha'])
                ventana.blit(surf_temp, (0, 0))
        
        # Dibujar frame actual
        pygame.draw.circle(ventana, ROJO, 
                         (int(bola_actual['x']), int(bola_actual['y'])), 
                         bola_actual['radio'])
        
        # Información
        texto_titulo = fuente_grande.render("Animación Cuadro por Cuadro con Onion Skinning", True, BLANCO)
        ventana.blit(texto_titulo, (ANCHO//2 - texto_titulo.get_width()//2, 20))
        
        estado_onion = "ACTIVADO" if sistema.mostrar_onion else "DESACTIVADO"
        modo = "EDITANDO" if sistema.editando else "REPRODUCIENDO"
        info_lines = [
            f"Frame: {sistema.frame_actual + 1}/{max(len(sistema.frames), sistema.frame_actual + 1)}",
            f"Onion Skinning: {estado_onion} | Modo: {modo}",
            "Arrastra el mouse para mover la bola y crear frames de animación",
            "Onion skinning muestra frames anteriores como referencia visual",
            "",
            "Controles:",
            "CLIC + ARRASTRAR: Mover bola y crear frame",
            "S: Guardar frame actual",
            "FLECHA DERECHA: Frame siguiente",
            "FLECHA IZQUIERDA: Frame anterior",
            "O: Activar/Desactivar Onion Skinning",
            "C: Limpiar animación",
            "ESC: Volver al menú"
        ]
        
        for i, linea in enumerate(info_lines):
            texto = fuente_pequena.render(linea, True, BLANCO)
            ventana.blit(texto, (20, ALTO - 280 + i * 25))
        
        # Mostrar frames como miniaturas
        for i, frame in enumerate(sistema.frames):
            x_mini = 20 + i * 25
            y_mini = 100
            color_mini = ROJO if i == sistema.frame_actual else VERDE
            pygame.draw.circle(ventana, color_mini, (x_mini, y_mini), 8)
        
        pygame.display.flip()

def menu_principal_clase4():
    """Menú principal para la Clase 4: Onion Skinning"""
    
    opciones = [
        ("1. Onion Skinning Básico - Personaje", demostracion_onion_basico),
        ("2. Onion Skinning Complejo - Cabeza brincando", demostracion_onion_animacion_compleja),
        ("3. Animación Cuadro por Cuadro", demostracion_animacion_cuadro_por_cuadro),
        ("4. Salir", None)
    ]
    
    while True:
        ventana.fill(NEGRO)
        
        titulo = fuente_grande.render("Onnion Skinning", True, BLANCO)
        ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 50))
        
        subtitulo = fuente_mediana.render("Técnica de Referencia para Animación", True, VERDE)
        ventana.blit(subtitulo, (ANCHO//2 - subtitulo.get_width()//2, 100))
        
        for i, (texto, _) in enumerate(opciones):
            color = CIAN
            if i == len(opciones) - 1:
                color = ROJO
            render = fuente_mediana.render(texto, True, color)
            ventana.blit(render, (ANCHO//2 - render.get_width()//2, 180 + i * 60))
        
        descripciones = [
            "Onion Skinning Básico: Animación automática con referencia visual",
            "Onion Skinning Complejo: Personaje central con movimiento y color dinámico, rodeado de objetos complejos",
            "Animación Manual: Creación cuadro por cuadro con edición interactiva"
        ]
        
        for i, desc in enumerate(descripciones):
            texto = fuente_pequena.render(desc, True, AMARILLO)
            ventana.blit(texto, (ANCHO//2 - texto.get_width()//2, 450 + i * 30))
        
        instrucciones = fuente_pequena.render("Presiona 1-4 para seleccionar una opción", True, BLANCO)
        ventana.blit(instrucciones, (ANCHO//2 - instrucciones.get_width()//2, ALTO - 50))
        
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    demostracion_onion_basico()
                elif evento.key == pygame.K_2:
                    demostracion_onion_animacion_compleja()
                elif evento.key == pygame.K_3:
                    demostracion_animacion_cuadro_por_cuadro()
                elif evento.key == pygame.K_4 or evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    menu_principal_clase4()



