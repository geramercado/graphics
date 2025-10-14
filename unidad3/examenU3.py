# sistema_solar_base.py
# CÓDIGO BASE PARA PROYECTO FINAL - SISTEMA SOLAR 3D
#Examen de la unidad 3 de graficación, profesor JOEL TAPIA FLORES
#ITSUR - 16 Octubre 2025
#Gerardo Mercado Hurtado
#Raúl Martínez Martínez
import pygame
import math
import numpy as np
import random

# Inicializar Pygame
pygame.init()

# Configuración pantalla
ANCHO, ALTO = 1200, 800
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mi Sistema Solar 3D - Gerardo / Raúl")
reloj = pygame.time.Clock()

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AMARILLO = (255, 240, 160)
AZUL = (0, 120, 255)
GRIS = (200, 200, 200)
ROJO = (255, 80, 80)
NARANJA = (255, 165, 0)
MARRON = (150, 100, 50)

# ESCALAS (ajustables)
DISTANCE_SCALE = 0.6   # escala de distancias (px por unidad)
RADIUS_SCALE = 0.25    # escala de radios (px por unidad)
SECONDS_PER_REAL_DAY = 1.0  # cuánto tiempo en segundos de sim representa 1 día real (antes de time_scale)
# Se podrá cambiar time_scale en tiempo real: time_scale = 1 => 1 sim-day por segundo. mayor => más rápido.

# Generar estrellas para fondo
NUM_ESTRELLAS = 300
random.seed(42)
estrellas = [(random.randint(0, ANCHO), random.randint(0, ALTO), random.choice([1,2,3])) for _ in range(NUM_ESTRELLAS)]

class Punto3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def copiar(self):
        return Punto3D(self.x, self.y, self.z)

def vector_sub(a: Punto3D, b: Punto3D):
    return Punto3D(a.x - b.x, a.y - b.y, a.z - b.z)

def vector_length(v: Punto3D):
    return math.sqrt(v.x*v.x + v.y*v.y + v.z*v.z)

def vector_normalize(v: Punto3D):
    L = vector_length(v)
    if L == 0: return Punto3D(0,0,0)
    return Punto3D(v.x/L, v.y/L, v.z/L)

def cross(a: Punto3D, b: Punto3D):
    return Punto3D(a.y*b.z - a.z*b.y, a.z*b.x - a.x*b.z, a.x*b.y - a.y*b.x)

def dot(a: Punto3D, b: Punto3D):
    return a.x*b.x + a.y*b.y + a.z*b.z

class Planeta:
    def __init__(self, nombre, radio_km, distancia_au, color, periodo_orbita_dias, periodo_rotacion_dias, inclinacion_deg=0, parent=None, nombre_display=None):
        # Datos "reales" como entrada (escala aplicada internamente)
        self.nombre = nombre
        self.nombre_display = nombre_display or nombre
        self.radio_km = radio_km
        self.distancia_au = distancia_au
        self.color = color
        self.periodo_orbita = periodo_orbita_dias    # en días
        self.periodo_rotacion = periodo_rotacion_dias  # en días (puede ser negativo para rotación retrógrada)
        self.inclinacion = math.radians(inclinacion_deg) # radianes
        self.parent = parent  # si es luna, orbita alrededor de parent (otro Planeta); si None => orbita origen (Sol)

        # Valores escalados para visualización
        # radio: toma radio_km y lo escala (esto es arbitrario, busca que sea visualmente útil)
        self.radio = max(2, radio_km * RADIUS_SCALE / 1000.0)  # px (aprox) - evita radios 0
        # distancia: convertir AU -> px
        self.distancia = (distancia_au * 150.0) * DISTANCE_SCALE  # base 150 (km->arbitrary) * scale

        # Estado dinámico
        self.angulo_orbita = random.random() * 2*math.pi
        self.angulo_rotacion = random.random() * 2*math.pi
        self.posicion = Punto3D(0, 0, 0)

        # Geometría simple (esfera por triangulación baja)
        self._crear_geometria(divisiones=10)

        # Calculados: velocidades angulares (rad/s) dependientes del time_scale y seconds_per_day
        self.orbital_speed = 0.0
        self.rotational_speed = 0.0

    def _crear_geometria(self, divisiones=10):
        self.vertices = []
        self.caras = []
        for i in range(divisiones + 1):
            lat = math.pi * i / divisiones
            for j in range(divisiones):
                lon = 2 * math.pi * j / divisiones
                x = self.radio * math.sin(lat) * math.cos(lon)
                y = self.radio * math.cos(lat)
                z = self.radio * math.sin(lat) * math.sin(lon)
                self.vertices.append(Punto3D(x, y, z))
        for i in range(divisiones):
            for j in range(divisiones):
                v0 = i * divisiones + j
                v1 = i * divisiones + (j+1) % divisiones
                v2 = (i+1) * divisiones + j
                v3 = (i+1) * divisiones + (j+1) % divisiones
                if i > 0:
                    self.caras.append([v0, v1, v2])
                if i < divisiones - 1:
                    self.caras.append([v1, v3, v2])

    def calcular_velocidades(self, time_scale):
        # periodo_orbita en días => velocidad angular rad/s = 2pi / (periodo_dias * seconds_per_real_day / time_scale)
        # reorganizar para que al aumentar time_scale se incremente velocidad
        if self.periodo_orbita == 0:
            self.orbital_speed = 0.0
        else:
            segundos_por_dia = SECONDS_PER_REAL_DAY
            self.orbital_speed = 2*math.pi / (self.periodo_orbita * segundos_por_dia) * time_scale

        if self.periodo_rotacion == 0:
            self.rotational_speed = 0.0
        else:
            # rotación: signo según periodo (neg => retrógrado)
            self.rotational_speed = 2*math.pi / (abs(self.periodo_rotacion) * SECONDS_PER_REAL_DAY) * (time_scale) * (1 if self.periodo_rotacion>0 else -1)

    def actualizar(self, dt):
        # Actualiza posición orbital y rotación (dt en segundos)
        self.angulo_orbita += self.orbital_speed * dt
        self.angulo_rotacion += self.rotational_speed * dt

        # calcular posición en plano (simple) alrededor del parent o alrededor del origen
        x = math.cos(self.angulo_orbita) * self.distancia
        z = math.sin(self.angulo_orbita) * self.distancia
        y = 0.0

        # aplicar inclinación axial: rotación del eje de la esfera (para el render se usa ángulo_rotacion)
        # posición orbital puede incluir pequeña inclinación de órbita si se desea; por simplicidad la dejamos en 0

        if self.parent:
            # sumar posición del parent para obtener coordenadas globales
            self.posicion = Punto3D(self.parent.posicion.x + x, self.parent.posicion.y + y, self.parent.posicion.z + z)
        else:
            self.posicion = Punto3D(x, y, z)

    def obtener_vertices_mundos(self):
        # Rotar los vértices de la esfera por la rotación del planeta (ángulo_rotacion) alrededor del eje Y
        verts = []
        cosr = math.cos(self.angulo_rotacion)
        sinr = math.sin(self.angulo_rotacion)
        # aplicar inclinación axial: rotar vértices alrededor del eje X por inclinación
        cosi = math.cos(self.inclinacion)
        sini = math.sin(self.inclinacion)

        for v in self.vertices:
            # aplicar rotación propia (Y)
            x = v.x * cosr - v.z * sinr
            z = v.x * sinr + v.z * cosr
            y = v.y
            # aplicar inclinación (rotación alrededor X)
            y2 = y * cosi - z * sini
            z2 = y * sini + z * cosi
            # translate to world position
            xw = x + self.posicion.x
            yw = y2 + self.posicion.y
            zw = z2 + self.posicion.z
            verts.append(Punto3D(xw, yw, zw))
        return verts

class Camara:
    def __init__(self):
        self.posicion = Punto3D(0, 150, -1000)
        self.target = Punto3D(0,0,0)
        self.distancia_vision = 800.0
        self.yaw = 0.0
        self.pitch = 0.0
    def proyectar(self, punto: Punto3D):
        # Proyección perspectiva simple con cámara situada en self.posicion mirando a self.target (no se hace matriz completa por simplicidad)
        # transformar punto relativo a cámara
        x_rel = punto.x - self.posicion.x
        y_rel = punto.y - self.posicion.y
        z_rel = punto.z - self.posicion.z
        # aplicar rotación yaw (Y) y pitch (X)
        cosy = math.cos(-self.yaw); siny = math.sin(-self.yaw)
        cosp = math.cos(-self.pitch); sinp = math.sin(-self.pitch)
        # rot Y
        xr = x_rel * cosy - z_rel * siny
        zr = x_rel * siny + z_rel * cosy
        # rot X
        yr = y_rel * cosp - zr * sinp
        zr = y_rel * sinp + zr * cosp
        if self.distancia_vision + zr == 0:
            return (ANCHO//2, ALTO//2)
        factor = self.distancia_vision / (self.distancia_vision + zr)
        x2d = xr * factor + ANCHO/2
        y2d = yr * factor + ALTO/2
        return (int(x2d), int(y2d))

class SistemaSolar:
    def __init__(self):
        self.planetas = []
        self.camara = Camara()
        self.time_scale = 60.0  # cuántos "días" de simulación por segundo (ajustable)
        self.pausado = False
        self.follow_index = None  # indice de planeta a seguir
        self.view_mode = "overview"  # "overview" | "planet_view" | "earth_perspective"
        self._crear_sistema()
        self._calc_velocidades_todo()

    def _crear_sistema(self):
        # Datos: nombre, radio_km, distancia_au, color, periodo_orbita_dias, periodo_rotacion_dias, inclinacion_deg, parent
        # Valores simplificados y aproximados (periodos en días reales)
        sol = Planeta("Sol", radio_km=30000, distancia_au=0, color=NARANJA, periodo_orbita_dias=0, periodo_rotacion_dias=25, inclinacion_deg=7.25)
        sol.posicion = Punto3D(0,0,0)
        self.planetas.append(sol)

        mercury = Planeta("Mercurio", 2439, 0.39, (180,180,180), 88, 58.6, 0.03, parent=None)
        venus = Planeta("Venus", 6052, 0.72, (240,200,150), 225, -243, 177.4, parent=None)
        tierra = Planeta("Tierra", 6371, 1.0, AZUL, 365.25, 1.0, 23.44, parent=None)
        luna = Planeta("Luna", 1737, 0.00257, GRIS, 27.3, 27.3, 6.68, parent=tierra, nombre_display="Luna")
        marte = Planeta("Marte", 3389, 1.52, ROJO, 687, 1.03, 25.0, parent=None)
        jupiter = Planeta("Júpiter", 69911, 5.20, NARANJA, 4333, 0.41, 3.13, parent=None)
        # agregar algunas lunas importantes de Júpiter (aprox distancias pequeñas en AU relativas a Júpiter)
        io = Planeta("Io", 1821, 0.0008, (220,180,120), 1.77, 1.77, 0.04, parent=jupiter, nombre_display="Io")
        europa = Planeta("Europa", 1560, 0.0012, (200,220,255), 3.55, 3.55, 0.47, parent=jupiter, nombre_display="Europa")
        ganymede = Planeta("Ganimedes", 2634, 0.0022, (200,180,160), 7.15, 7.15, 0.2, parent=jupiter, nombre_display="Ganimedes")
        callisto = Planeta("Calisto", 2410, 0.0035, (150,150,150), 16.69, 16.69, 0.19, parent=jupiter, nombre_display="Calisto")

        saturno = Planeta("Saturno", 58232, 9.58, (230,220,200), 10759, 0.45, 26.7, parent=None)

        urano = Planeta("Urano", 25362, 19.2, (160,200,230), 30687, -0.72, 97.77, parent=None)
        neptuno = Planeta("Neptuno", 24622, 30.05, (80,120,255), 60190, 0.67, 28.32, parent=None)

        # Añadir al sistema en orden (Sol primero en índice 0)
        self.planetas.extend([mercury, venus, tierra, luna, marte, jupiter, io, europa, ganymede, callisto, saturno, urano, neptuno])

    def _calc_velocidades_todo(self):
        for p in self.planetas:
            p.calcular_velocidades(self.time_scale)

    def cambiar_time_scale(self, factor):
        self.time_scale *= factor
        # limitar
        self.time_scale = max(0.01, min(self.time_scale, 1000000))
        self._calc_velocidades_todo()

    def actualizar(self, dt):
        if self.pausado: return
        # dt en segundos
        for p in self.planetas:
            p.actualizar(dt)
        # actualizar cámaras si se sigue un planeta
        if self.follow_index is not None and 0 <= self.follow_index < len(self.planetas):
            objetivo = self.planetas[self.follow_index]
            # posición de la cámara: detrás y arriba del planeta (vector desde origen hacia planeta)
            dir_vec = vector_normalize(objetivo.posicion)
            # si planeta está en sol (posicion 0) dir_vec puede ser cero -> colocar cámara en -Z
            if vector_length(dir_vec) == 0:
                dir_vec = Punto3D(0,0,1)
            # colocar cámara con offset detrás del planeta
            distancia_cam = 150 + objetivo.radio * 5
            cam_x = objetivo.posicion.x - dir_vec.x * distancia_cam
            cam_y = objetivo.posicion.y + objetivo.radio*4 + 30
            cam_z = objetivo.posicion.z - dir_vec.z * distancia_cam
            self.camara.posicion = Punto3D(cam_x, cam_y, cam_z)
            self.camara.target = Punto3D(objetivo.posicion.x, objetivo.posicion.y, objetivo.posicion.z)

    def dibujar(self, ventana):
        # fondo espacial: estrellas
        ventana.fill((5,5,15))
        for (x,y,s) in estrellas:
            pygame.draw.circle(ventana, (200,200,255), (x,y), s)

        # dibujar órbitas (líneas)
        for p in self.planetas:
            if p.distancia > 1 and p.parent is None:  # órbita alrededor del sol
                self._dibujar_orbita(ventana, p)
            if p.parent is not None and p.distancia > 1:
                # órbita alrededor del parent (pequeñas)
                self._dibujar_orbita(ventana, p, centered_on=p.parent.posicion, radius_override=p.distancia)

        # dibujar Sol con brillo central
        sol = self.planetas[0]
        sol_screen = self.camara.proyectar(sol.posicion)
        pygame.draw.circle(ventana, AMARILLO, sol_screen, int(sol.radio*1.6))
        # halo
        pygame.draw.circle(ventana, (255,220,140), sol_screen, int(sol.radio*3), 2)

        # luz direccional: desde el sol (posicion origen)
        light_pos = sol.posicion

        # dibujar planetas (caras con sombreado simple)
        for p in self.planetas:
            if p is sol: continue
            self._dibujar_planeta_con_sombra(ventana, p, light_pos)

        # info en pantalla
        self._dibujar_info(ventana)

    def _dibujar_orbita(self, ventana, planeta, centered_on=None, radius_override=None):
        centered = centered_on or Punto3D(0,0,0)
        radio = radius_override or planeta.distancia
        pts = []
        pasos = 160
        for i in range(pasos):
            ang = 2*math.pi*i/pasos
            x = centered.x + math.cos(ang)*radio
            z = centered.z + math.sin(ang)*radio
            p3 = Punto3D(x, 0, z)
            pts.append(self.camara.proyectar(p3))
        if len(pts)>1:
            pygame.draw.lines(ventana, (80,80,80), True, pts, 1)

    def _dibujar_planeta_con_sombra(self, ventana, planeta, light_pos):
        verts_world = planeta.obtener_vertices_mundos()
        # precomputar proyecciones y depth
        proyecciones = [self.camara.proyectar(v) for v in verts_world]

        for cara in planeta.caras:
            v0 = verts_world[cara[0]]
            v1 = verts_world[cara[1]]
            v2 = verts_world[cara[2]]
            # calcular normal de la cara (en mundo)
            a = vector_sub(v1, v0)
            b = vector_sub(v2, v0)
            nrm = cross(a,b)
            nrm = vector_normalize(nrm)
            # dirección a la luz
            ld = vector_sub(light_pos, v0)
            ld = vector_normalize(ld)
            # iluminación simple (Lambertiano)
            intensidad = dot(nrm, ld)
            intensidad = max(0.1, intensidad)  # evitar totalmente negro
            # color sombreado
            base = planeta.color
            color_shaded = (min(255, int(base[0]*intensidad)),
                            min(255, int(base[1]*intensidad)),
                            min(255, int(base[2]*intensidad)))
            pts = [proyecciones[idx] for idx in cara]
            try:
                pygame.draw.polygon(ventana, color_shaded, pts)
                pygame.draw.polygon(ventana, (15,15,15), pts, 1)
            except:
                pass
        # dibujar etiqueta del planeta
        centro2d = self.camara.proyectar(planeta.posicion)
        fuente = pygame.font.SysFont('Arial', 14)
        txt = fuente.render(planeta.nombre_display, True, BLANCO)
        ventana.blit(txt, (centro2d[0]+8, centro2d[1]))

    def _dibujar_info(self, ventana):
        fuente = pygame.font.SysFont('Consolas', 16)
        lines = [
            "MI SISTEMA SOLAR 3D",
            f"Time scale (días/seg): {self.time_scale:.1f}   (usar +/- o rueda mouse)",
            "Controles:",
            "WASD: mover cámara libre (cuando no se sigue planeta)",
            "Q/E: subir/bajar cámara",
            "Mouse click+drag: rotar cámara (ajusta yaw/pitch)",
            "Números 0..9: seguir planeta (0=Sol, 1=Mercurio, ...)",
            "C: toggle seguir planeta on/off",
            "V: cambiar vista (overview / planet_view / earth_perspective)",
            "Espacio: Pausa/Resume",
            "R: Reset cámara",
            "+ / - : Acelerar / desacelerar tiempo",
            "P: Captura pantalla",
        ]
        for i, l in enumerate(lines):
            texto = fuente.render(l, True, BLANCO)
            ventana.blit(texto, (10, 10 + i*20))

    def toggle_pause(self):
        self.pausado = not self.pausado

    def seleccionar_planeta_para_seguir(self, index):
        if index is None:
            self.follow_index = None
        elif 0 <= index < len(self.planetas):
            self.follow_index = index
        else:
            self.follow_index = None

    def cambiar_vista(self):
        if self.view_mode == "overview":
            self.view_mode = "planet_view"
        elif self.view_mode == "planet_view":
            self.view_mode = "earth_perspective"
        else:
            self.view_mode = "overview"

# ---------- Programa principal ----------
def main():
    sistema = SistemaSolar()
    mouse_dragging = False
    last_mouse = (0,0)
    velocidad_cam = 400.0
    sistema._calc_velocidades_todo()

    running = True
    while running:
        dt = reloj.tick(60) / 1000.0  # segundos reales desde último frame
        # Aplica time_scale: las velocidades angulares ya incorporan time_scale, así que dt se usa directamente
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    sistema.toggle_pause()
                elif evento.key == pygame.K_r:
                    sistema.camara = Camara()
                elif evento.key == pygame.K_c:
                    if sistema.follow_index is None:
                        # default seguir la Tierra si existe (buscar índice de "Tierra")
                        idx = next((i for i,p in enumerate(sistema.planetas) if p.nombre=="Tierra"), 2)
                        sistema.seleccionar_planeta_para_seguir(idx)
                    else:
                        sistema.seleccionar_planeta_para_seguir(None)
                elif evento.key == pygame.K_v:
                    sistema.cambiar_vista()
                elif evento.key == pygame.K_p:
                    pygame.image.save(ventana, "captura_sistema.png")
                elif evento.key == pygame.K_EQUALS or evento.key == pygame.K_PLUS:
                    sistema.cambiar_time_scale(2.0)
                elif evento.key == pygame.K_MINUS or evento.key == pygame.K_UNDERSCORE:
                    sistema.cambiar_time_scale(0.5)
                # teclas numéricas para seguir planetas
                elif pygame.K_0 <= evento.key <= pygame.K_9:
                    num = evento.key - pygame.K_0
                    if num < len(sistema.planetas):
                        sistema.seleccionar_planeta_para_seguir(num)
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    mouse_dragging = True
                    last_mouse = evento.pos
                elif evento.button == 4:  # rueda arriba
                    sistema.cambiar_time_scale(2.0)
                elif evento.button == 5:  # rueda abajo
                    sistema.cambiar_time_scale(0.5)
            elif evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1:
                    mouse_dragging = False
            elif evento.type == pygame.MOUSEMOTION:
                if mouse_dragging and sistema.follow_index is None:
                    mx,my = evento.pos
                    dx = mx - last_mouse[0]
                    dy = my - last_mouse[1]
                    sistema.camara.yaw += dx * 0.005
                    sistema.camara.pitch += dy * 0.003
                    last_mouse = (mx,my)

        # Controles teclado para cámara libre (solo si no se sigue un planeta)
        keys = pygame.key.get_pressed()
        if sistema.follow_index is None:
            if keys[pygame.K_w]:
                sistema.camara.posicion.z += velocidad_cam * dt * math.cos(sistema.camara.yaw)
                sistema.camara.posicion.x += velocidad_cam * dt * math.sin(sistema.camara.yaw)
            if keys[pygame.K_s]:
                sistema.camara.posicion.z -= velocidad_cam * dt * math.cos(sistema.camara.yaw)
                sistema.camara.posicion.x -= velocidad_cam * dt * math.sin(sistema.camara.yaw)
            if keys[pygame.K_a]:
                sistema.camara.posicion.x -= velocidad_cam * dt * math.cos(sistema.camara.yaw)
                sistema.camara.posicion.z += velocidad_cam * dt * math.sin(sistema.camara.yaw)
            if keys[pygame.K_d]:
                sistema.camara.posicion.x += velocidad_cam * dt * math.cos(sistema.camara.yaw)
                sistema.camara.posicion.z -= velocidad_cam * dt * math.sin(sistema.camara.yaw)
            if keys[pygame.K_q]:
                sistema.camara.posicion.y -= velocidad_cam * dt
            if keys[pygame.K_e]:
                sistema.camara.posicion.y += velocidad_cam * dt

        # Actualizar sistema (planetas etc.)
        sistema.actualizar(dt)

        # Dibujar todo
        sistema.dibujar(ventana)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
