# importar bibliotecas
import pygame
import math
import sys

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
ANCHO, ALTO = 1000, 700
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Clase 4: Onion Skinning - Animación con Referencias")

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
        pygame.draw.circle(superficie, color, (int(personaje['x']), int(personaje['y'] - 30)), 15)
        
        # Cuerpo
        pygame.draw.line(superficie, color, 
                        (personaje['x'], personaje['y'] - 15), 
                        (personaje['x'], personaje['y'] + 20), 3)
        
        # Brazos
        angulo_brazos = personaje.get('angulo_brazos', 0)
        brazo_longitud = 25
        
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
    """Demostración básica de Onion Skinning con animación simple"""
    
    sistema = SistemaOnionSkinning(max_frames=20)
    tiempo_total = 0.0
    animando = True
    
    # Datos iniciales del personaje
    personaje_actual = {
        'x': ANCHO // 2,
        'y': ALTO // 2,
        'angulo_brazos': 0,
        'angulo_piernas': 0
    }
    
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
                    sistema.cantidad_frames_mostrar = min(10, sistema.cantidad_frames_mostrar + 1)
                elif evento.key == pygame.K_MINUS:
                    sistema.cantidad_frames_mostrar = max(1, sistema.cantidad_frames_mostrar - 1)
                elif evento.key == pygame.K_SPACE:
                    animando = not animando
                elif evento.key == pygame.K_r:
                    # Reiniciar animación
                    sistema.frames = []
                    tiempo_total = 0.0
                    personaje_actual = {
                        'x': ANCHO // 2,
                        'y': ALTO // 2,
                        'angulo_brazos': 0,
                        'angulo_piernas': 0
                    }
        
        if animando:
            # Actualizar animación del personaje
            frecuencia = 2.0  # Velocidad de la animación
            personaje_actual['angulo_brazos'] = 30 * math.sin(tiempo_total * frecuencia * 2)
            personaje_actual['angulo_piernas'] = 20 * math.sin(tiempo_total * frecuencia)
            personaje_actual['x'] = ANCHO // 2 + 100 * math.sin(tiempo_total * frecuencia * 0.5)
            
            # Agregar frame actual a la animación
            if tiempo_total % 0.1 < dt:  # Agregar frame cada ~0.1 segundos
                sistema.agregar_frame({'personaje': personaje_actual.copy()})
        
        # Dibujado
        ventana.fill(NEGRO)
        
        # Dibujar onion skinning (frames anteriores)
        sistema.dibujar_onion_skin(ventana, 
                                 lambda surf, datos, color: sistema.dibujar_frame_actual(surf, datos, color))
        
        # Dibujar frame actual
        sistema.dibujar_frame_actual(ventana, {'personaje': personaje_actual}, ROJO)
        
        # Información
        texto_titulo = fuente_grande.render("Onion Skinning Básico - Animación de Personaje", True, BLANCO)
        ventana.blit(texto_titulo, (ANCHO//2 - texto_titulo.get_width()//2, 20))
        
        estado_onion = "ACTIVADO" if sistema.mostrar_onion_skin else "DESACTIVADO"
        info_lines = [
            f"Tiempo: {tiempo_total:.1f}s | Frames: {len(sistema.frames)}",
            f"Onion Skinning: {estado_onion} | Frames mostrados: {sistema.cantidad_frames_mostrar}",
            "Los frames anteriores se muestran semitransparentes como referencia",
            "Permite ver la trayectoria y mantener la consistencia de la animación",
            "",
            "Controles:",
            "O: Activar/Desactivar Onion Skinning",
            "+/-: Aumentar/Disminuir frames mostrados",
            "ESPACIO: Pausar/Reanudar animación",
            "R: Reiniciar animación",
            "ESC: Volver al menú"
        ]
        
        for i, linea in enumerate(info_lines):
            texto = fuente_pequena.render(linea, True, BLANCO)
            ventana.blit(texto, (20, ALTO - 220 + i * 25))
        
        # Leyenda de colores
        pygame.draw.rect(ventana, ROJO, (20, 100, 20, 20))
        texto_actual = fuente_pequena.render("Frame Actual", True, BLANCO)
        ventana.blit(texto_actual, (50, 100))
        
        pygame.draw.rect(ventana, VERDE, (20, 130, 20, 20))
        texto_referencia = fuente_pequena.render("Frames Anteriores (Onion Skin)", True, BLANCO)
        ventana.blit(texto_referencia, (50, 130))
        
        pygame.display.flip()

def demostracion_onion_animacion_compleja():
    """Demostración de Onion Skinning con animación compleja"""
    
    sistema = SistemaOnionSkinning(max_frames=30)
    tiempo_total = 0.0
    animando = True
    
    # Crear múltiples objetos para animar
    objetos_actuales = []
    num_objetos = 5
    
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
                # Movimiento circular con fase diferente para cada objeto
                frecuencia = 1.5
                fase = obj['fase']
                radio_base = 150
                radio_actual = radio_base + 30 * math.sin(tiempo_total * frecuencia + fase)
                
                obj['x'] = ANCHO // 2 + radio_actual * math.cos(tiempo_total * frecuencia + fase)
                obj['y'] = ALTO // 2 + radio_actual * math.sin(tiempo_total * frecuencia + fase)
                
                # Cambiar tamaño
                obj['radio'] = 15 + 10 * math.sin(tiempo_total * 2 * frecuencia + fase)
            
            # Agregar frame actual a la animación
            if tiempo_total % 0.08 < dt:  # Agregar frame cada ~0.08 segundos
                sistema.agregar_frame({'objetos': [obj.copy() for obj in objetos_actuales]})
        
        # Dibujado
        ventana.fill(NEGRO)
        
        # Función personalizada para dibujar frames de objetos
        def dibujar_objetos_frame(superficie, datos_frame, color):
            if 'objetos' in datos_frame:
                colores = [ROJO, VERDE, AZUL, AMARILLO, MORADO, CIAN, NARANJA, ROSA]
                for obj in datos_frame['objetos']:
                    color_obj = colores[obj['color_idx'] % len(colores)] if color == VERDE else color
                    if obj['tipo'] == 'circulo':
                        pygame.draw.circle(superficie, color_obj, 
                                         (int(obj['x']), int(obj['y'])), 
                                         int(obj['radio']))
        
        # Dibujar onion skinning
        sistema.dibujar_onion_skin(ventana, dibujar_objetos_frame)
        
        # Dibujar frame actual
        colores = [ROJO, VERDE, AZUL, AMARILLO, MORADO, CIAN, NARANJA, ROSA]
        for obj in objetos_actuales:
            color_obj = colores[obj['color_idx'] % len(colores)]
            pygame.draw.circle(ventana, color_obj, 
                             (int(obj['x']), int(obj['y'])), 
                             int(obj['radio']))
        
        # Información
        texto_titulo = fuente_grande.render("Onion Skinning Complejo - Múltiples Objetos", True, BLANCO)
        ventana.blit(texto_titulo, (ANCHO//2 - texto_titulo.get_width()//2, 20))
        
        estado_onion = "ACTIVADO" if sistema.mostrar_onion_skin else "DESACTIVADO"
        info_lines = [
            f"Tiempo: {tiempo_total:.1f}s | Frames: {len(sistema.frames)}",
            f"Onion Skinning: {estado_onion} | Frames mostrados: {sistema.cantidad_frames_mostrar}",
            f"Objetos animados: {num_objetos}",
            "Cada objeto tiene movimiento circular independiente con diferentes fases",
            "Onion skinning muestra las trayectorias completas de todos los objetos",
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
        ("2. Onion Skinning Complejo - Múltiples Objetos", demostracion_onion_animacion_compleja),
        ("3. Animación Cuadro por Cuadro", demostracion_animacion_cuadro_por_cuadro),
        ("4. Salir", None)
    ]
    
    while True:
        ventana.fill(NEGRO)
        
        titulo = fuente_grande.render("CLASE 4: ONION SKINNING", True, BLANCO)
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
            "Onion Skinning Complejo: Múltiples objetos con trayectorias complejas",
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

   