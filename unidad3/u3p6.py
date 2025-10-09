# importar bibliotecas
import pygame
import math
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ANCHO, ALTO = 1200, 800
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Maqueta 3D - Campus ITSUR (según croquis)")
reloj = pygame.time.Clock()

# Colores
NEGRO = (10, 10, 10)
BLANCO = (255, 255, 255)
GRIS = (100, 100, 100)
CIAN = (0, 200, 200)

# Colores campus
COLOR_TERRENO = (204, 220, 170)   # fondo claro tipo césped del croquis
COLOR_CAMINO = (120, 120, 120)
COLOR_EDIFICIO_A = (180, 165, 200)
COLOR_EDIFICIO_B = (200, 185, 160)
COLOR_BIBLIOTECA = (190, 160, 150)
COLOR_VINCULACION = (200, 200, 150)
COLOR_TICS = (150, 185, 210)
COLOR_ITSUR = (220, 190, 140)
COLOR_CAFETERIA = (205, 140, 110)
COLOR_CESPED = (130, 170, 100)

# ---------- Clases 3D ----------
class Punto3D:
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
    def copiar(self):
        return Punto3D(self.x, self.y, self.z)

class Camara:
    def __init__(self, posicion=None, distancia_vision=700):
        self.posicion = posicion if posicion else Punto3D(0, -300, -600)
        self.distancia_vision = distancia_vision
        self.fov = 60
    def proyectar_perspectiva(self, punto, centro_x, centro_y):
        # proyectar punto 3D a 2D (simple perspectiva)
        px = punto.x - self.posicion.x
        py = punto.y - self.posicion.y
        pz = punto.z - self.posicion.z
        denom = (self.distancia_vision + pz)
        if denom == 0:
            denom = 0.0001
        factor = self.distancia_vision / denom
        x2d = px * factor + centro_x
        y2d = py * factor + centro_y
        return (int(x2d), int(y2d))
    def proyectar_ortografica(self, punto, centro_x, centro_y, escala=1.0):
        px = (punto.x - self.posicion.x) * escala + centro_x
        py = (punto.y - self.posicion.y) * escala + centro_y
        return (int(px), int(py))
    def proyectar_isometrica(self, punto, centro_x, centro_y, escala=1.0):
        # isométrica (aprox) usando rotación 45° y proyección simple
        x = punto.x - self.posicion.x
        y = punto.y - self.posicion.y
        z = punto.z - self.posicion.z
        angle = math.radians(30)
        x_iso = (x - z) * math.cos(angle) * escala
        y_iso = (x + z) * math.sin(angle) * escala - y * escala
        return (int(x_iso + centro_x), int(y_iso + centro_y))
    def proyectar_elevacion(self, punto, centro_x, centro_y, tipo='frontal', escala=1.0):
        x = punto.x - self.posicion.x
        y = punto.y - self.posicion.y
        z = punto.z - self.posicion.z
        if tipo == 'frontal':
            return (int(x * escala + centro_x), int(y * escala + centro_y))
        elif tipo == 'superior':
            return (int(x * escala + centro_x), int(z * escala + centro_y))
        elif tipo == 'lateral':
            return (int(z * escala + centro_x), int(y * escala + centro_y))
        else:
            return (int(x * escala + centro_x), int(y * escala + centro_y))

class Objeto3D:
    def __init__(self, vertices, aristas, color=BLANCO, nombre=""):
        self.vertices_originales = [v.copiar() for v in vertices]
        self.vertices = [v.copiar() for v in vertices]
        self.aristas = list(aristas)
        self.color = color
        self.nombre = nombre
        self.posicion = Punto3D(0, 0, 0)
        self.escala = Punto3D(1, 1, 1)
        self.rot = Punto3D(0, 0, 0)  # grados rotación X,Y,Z
    @staticmethod
    def crear_rectangulo(ancho, alto, profundidad, color=BLANCO, nombre=""):
        hw = ancho/2; hh = alto/2; hd = profundidad/2
        verts = [
            Punto3D(-hw, -hh, -hd), Punto3D(hw, -hh, -hd),
            Punto3D(-hw, hh, -hd),  Punto3D(hw, hh, -hd),
            Punto3D(-hw, -hh, hd),  Punto3D(hw, -hh, hd),
            Punto3D(-hw, hh, hd),   Punto3D(hw, hh, hd)
        ]
        aris = [
            (0,1),(1,3),(3,2),(2,0), # frente
            (4,5),(5,7),(7,6),(6,4), # fondo
            (0,4),(1,5),(2,6),(3,7)
        ]
        return Objeto3D(verts, aris, color, nombre)
    def establecer_transformacion(self, pos=(0,0,0), esc=(1,1,1), rot=(0,0,0)):
        self.posicion = Punto3D(pos[0], pos[1], pos[2])
        self.escala = Punto3D(esc[0], esc[1], esc[2])
        self.rot = Punto3D(rot[0], rot[1], rot[2])
        self.actualizar_vertices()
    def actualizar_vertices(self):
        for i, vo in enumerate(self.vertices_originales):
            v = vo.copiar()
            # escala
            v.x *= self.escala.x
            v.y *= self.escala.y
            v.z *= self.escala.z
            # rot Z
            if self.rot.z != 0:
                rz = math.radians(self.rot.z)
                x = v.x*math.cos(rz) - v.y*math.sin(rz)
                y = v.x*math.sin(rz) + v.y*math.cos(rz)
                v.x, v.y = x, y
            # rot Y
            if self.rot.y != 0:
                ry = math.radians(self.rot.y)
                x = v.x*math.cos(ry) + v.z*math.sin(ry)
                z = -v.x*math.sin(ry) + v.z*math.cos(ry)
                v.x, v.z = x, z
            # rot X
            if self.rot.x != 0:
                rx = math.radians(self.rot.x)
                y = v.y*math.cos(rx) - v.z*math.sin(rx)
                z = v.y*math.sin(rx) + v.z*math.cos(rx)
                v.y, v.z = y, z
            # traslación
            v.x += self.posicion.x
            v.y += self.posicion.y
            v.z += self.posicion.z
            self.vertices[i] = v

# ---------- Crear campus según croquis (posiciones aproximadas) ----------
def crear_campus_crokis():
    proyecto = []
    # TERRENO (polígono simple simulado como gran rectángulo)
    terreno = Objeto3D.crear_rectangulo(900, 2, 700, COLOR_TERRENO, "Terreno")
    terreno.establecer_transformacion(pos=(0, 120, 0), esc=(1,1,1))
    proyecto.append(terreno)
    # Caminos principales (simples rectángulos planos)
    camino = Objeto3D.crear_rectangulo(700, 2, 60, COLOR_CAMINO, "Camino principal")
    camino.establecer_transformacion(pos=(0, 119, 110), esc=(1,1,1))
    proyecto.append(camino)
    # Césped y zonas
    cesped = Objeto3D.crear_rectangulo(750, 2, 650, COLOR_CESPED, "Área césped")
    cesped.establecer_transformacion(pos=(0, 119, 0), esc=(1,1,1))
    proyecto.append(cesped)

    # Edificios (posiciones ajustadas para parecerse al croquis)
    # Biblioteca (norte - más grande)
    biblioteca = Objeto3D.crear_rectangulo(160, 70, 90, COLOR_BIBLIOTECA, "Biblioteca")
    biblioteca.establecer_transformacion(pos=( -20, -120, -220), esc=(1,1,1), rot=(0,0,4))
    proyecto.append(biblioteca)

    # Vinculación (noroeste)
    vinculacion = Objeto3D.crear_rectangulo(140, 60, 100, COLOR_VINCULACION, "Edificio Vinculación")
    vinculacion.establecer_transformacion(pos=(-200, -30, -160), esc=(1,1,1), rot=(0,0,-8))
    proyecto.append(vinculacion)

    # Edificio A (centro ligeramente arriba)
    edificio_a = Objeto3D.crear_rectangulo(180, 70, 120, COLOR_EDIFICIO_A, "Edificio A")
    edificio_a.establecer_transformacion(pos=( -10, -40, -30), esc=(1,1,1), rot=(0,0,10))
    proyecto.append(edificio_a)

    # Edificio B (centro-derecha)
    edificio_b = Objeto3D.crear_rectangulo(140, 60, 100, COLOR_EDIFICIO_B, "Edificio B")
    edificio_b.establecer_transformacion(pos=(90, -20, -10), esc=(1,1,1), rot=(0,0,6))
    proyecto.append(edificio_b)

    # TIC's (sureste)
    tics = Objeto3D.crear_rectangulo(160, 60, 110, COLOR_TICS, "TIC's")
    tics.establecer_transformacion(pos=(140, -10, 120), esc=(1,1,1), rot=(0,0,12))
    proyecto.append(tics)

    # ITSUR Uriangato (pequeño, frente a A)
    itsur = Objeto3D.crear_rectangulo(120, 40, 70, COLOR_ITSUR, "ITSUR Uriangato")
    itsur.establecer_transformacion(pos=(-10, 20, 70), esc=(1,1,1), rot=(0,0,0))
    proyecto.append(itsur)

    # Cafetería (sur-este frente a TIC's)
    cafeteria = Objeto3D.crear_rectangulo(110, 40, 70, COLOR_CAFETERIA, "Cafetería ITSUR")
    cafeteria.establecer_transformacion(pos=(40, 30, 150), esc=(1,1,1))
    proyecto.append(cafeteria)

    # Piscina/área rectangular en el croquis (zona en teal)
    area_rect = Objeto3D.crear_rectangulo(90, 6, 160, (100,200,190), "Área verde/estanque")
    area_rect.establecer_transformacion(pos=(220, 118, 30), esc=(1,1,1))
    proyecto.append(area_rect)

    return proyecto

# Crear proyecto
proyecto = crear_campus_crokis()

# Cámara y control de rotación (órbita)
camara = Camara(posicion=Punto3D(350, -260, 300), distancia_vision=700)
orbit_angle = 0.0
orbit_radius = 420.0
orbit_speed = 20.0  # grados por segundo
auto_orbit = True

# Vistas
cam_persp = camara
cam_iso = Camara(posicion=Punto3D(240, -180, 220), distancia_vision=700)
cam_top = Camara(posicion=Punto3D(0, -420, 0), distancia_vision=700)

vista_actual = 4  # 1:persp,2:planta,3:isom,4:multipanel
mostrar_nombres = True

# Fuente
fuente_peq = pygame.font.SysFont("Arial", 14)
fuente_tit = pygame.font.SysFont("Arial", 20)

# Bucle principal
ejecutando = True
while ejecutando:
    dt = reloj.tick(60) / 1000.0
    # Orbita automática
    if auto_orbit:
        orbit_angle += orbit_speed * dt
    # Convertir ángulo a radianes y actualizar posición de la cámara alrededor del centro (0,0,0)
    rad = math.radians(orbit_angle)
    camara.posicion.x = math.cos(rad) * orbit_radius
    camara.posicion.z = math.sin(rad) * orbit_radius
    camara.posicion.y = -260  # altura fija para vista agradable

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                ejecutando = False
            elif evento.key == pygame.K_1:
                vista_actual = 1
            elif evento.key == pygame.K_2:
                vista_actual = 2
            elif evento.key == pygame.K_3:
                vista_actual = 3
            elif evento.key == pygame.K_4:
                vista_actual = 4
            elif evento.key == pygame.K_n:
                mostrar_nombres = not mostrar_nombres
            elif evento.key == pygame.K_r:
                auto_orbit = not auto_orbit
            elif evento.key == pygame.K_LEFT:
                orbit_angle -= 10
            elif evento.key == pygame.K_RIGHT:
                orbit_angle += 10
            elif evento.key == pygame.K_UP:
                camara.distancia_vision = max(200, camara.distancia_vision - 40)
            elif evento.key == pygame.K_DOWN:
                camara.distancia_vision = min(2000, camara.distancia_vision + 40)

    # Dibujado
    ventana.fill(NEGRO)

    if vista_actual == 4:
        # paneles: 2x2
        panels = [
            (0, 0, ANCHO//2, ALTO//2, "PERSPECTIVA", camara, "perspectiva"),
            (ANCHO//2, 0, ANCHO//2, ALTO//2, "PLANTA", cam_top, "planta"),
            (0, ALTO//2, ANCHO//2, ALTO//2, "ELEVACIÓN FRONTAL", cam_persp, "frontal"),
            (ANCHO//2, ALTO//2, ANCHO//2, ALTO//2, "ISOMÉTRICA", cam_iso, "isometrica"),
        ]
        for (x,y,w,h,tit,cam,tipo) in panels:
            # fondo del panel
            pygame.draw.rect(ventana, (28,28,36), (x,y,w,h))
            # marco
            pygame.draw.rect(ventana, GRIS, (x,y,w,h), 2)
            centrox = x + w//2
            centroy = y + h//2
            # dibujar objetos
            for obj in proyecto:
                for a,b in obj.aristas:
                    p1 = obj.vertices[a]
                    p2 = obj.vertices[b]
                    if tipo == "perspectiva":
                        pp1 = cam.proyectar_perspectiva(p1, centrox, centroy)
                        pp2 = cam.proyectar_perspectiva(p2, centrox, centroy)
                    elif tipo == "isometrica":
                        pp1 = cam.proyectar_isometrica(p1, centrox, centroy, 0.9)
                        pp2 = cam.proyectar_isometrica(p2, centrox, centroy, 0.9)
                    elif tipo == "frontal":
                        pp1 = cam.proyectar_elevacion(p1, centrox, centroy, 'frontal', 1.0)
                        pp2 = cam.proyectar_elevacion(p2, centrox, centroy, 'frontal', 1.0)
                    elif tipo == "planta":
                        pp1 = cam.proyectar_elevacion(p1, centrox, centroy, 'superior', 0.9)
                        pp2 = cam.proyectar_elevacion(p2, centrox, centroy, 'superior', 0.9)
                    else:
                        pp1 = cam.proyectar_perspectiva(p1, centrox, centroy)
                        pp2 = cam.proyectar_perspectiva(p2, centrox, centroy)
                    pygame.draw.line(ventana, obj.color, pp1, pp2, 2)
            # título panel
            lbl = fuente_peq.render(tit, True, BLANCO)
            ventana.blit(lbl, (x + 10, y + 8))
    else:
        # vista única centrada
        if vista_actual == 1:
            cam_act = camara
            modo = "perspectiva"
            titulo_vista = "VISTA PERSPECTIVA"
        elif vista_actual == 2:
            cam_act = cam_top
            modo = "planta"
            titulo_vista = "PLANTA - VISTA SUPERIOR"
        elif vista_actual == 3:
            cam_act = cam_iso
            modo = "isometrica"
            titulo_vista = "VISTA ISOMÉTRICA"
        centrox = ANCHO//2
        centroy = ALTO//2
        # fondo
        pygame.draw.rect(ventana, (28,28,36), (0,0,ANCHO,ALTO))
        # dibujar objetos
        for obj in proyecto:
            for a,b in obj.aristas:
                p1 = obj.vertices[a]
                p2 = obj.vertices[b]
                if modo == "perspectiva":
                    pp1 = cam_act.proyectar_perspectiva(p1, centrox, centroy)
                    pp2 = cam_act.proyectar_perspectiva(p2, centrox, centroy)
                elif modo == "isometrica":
                    pp1 = cam_act.proyectar_isometrica(p1, centrox, centroy, 1.0)
                    pp2 = cam_act.proyectar_isometrica(p2, centrox, centroy, 1.0)
                elif modo == "planta":
                    pp1 = cam_act.proyectar_elevacion(p1, centrox, centroy, 'superior', 1.0)
                    pp2 = cam_act.proyectar_elevacion(p2, centrox, centroy, 'superior', 1.0)
                else:
                    pp1 = cam_act.proyectar_perspectiva(p1, centrox, centroy)
                    pp2 = cam_act.proyectar_perspectiva(p2, centrox, centroy)
                pygame.draw.line(ventana, obj.color, pp1, pp2, 2)
        # título
        titulo = fuente_tit.render(titulo_vista, True, BLANCO)
        ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 12))

    # Información en pantalla
    info_lines = [
        "CROQUIS ITSUR - Vista aproximada",
        f"Vista: {'MÚLTIPLE' if vista_actual==4 else 'INDIVIDUAL'}   (1:Persp 2:Planta 3:Isom 4:Múltiple)",
        f"R: alternar rotación automática   |  ← →: rotar manual  |  ↑↓: zoom",
        "N: alternar etiquetas   |  ESC: salir"
    ]
    for i, t in enumerate(info_lines):
        r = fuente_peq.render(t, True, BLANCO)
        ventana.blit(r, (10, 10 + i*18))

    # Etiquetas (si están activadas) - en vista individual centrar sobre cada edificio
    if mostrar_nombres:
        if vista_actual == 4:
            # lista lateral en múltiple
            items = [
                ("Biblioteca", COLOR_BIBLIOTECA),
                ("Edificio Vinculación", COLOR_VINCULACION),
                ("Edificio A", COLOR_EDIFICIO_A),
                ("Edificio B", COLOR_EDIFICIO_B),
                ("TIC's", COLOR_TICS),
                ("ITSUR Uriangato", COLOR_ITSUR),
                ("Cafetería ITSUR", COLOR_CAFETERIA)
            ]
            x_ley = ANCHO - 230
            y_ley = 110
            for i, (nombre, color) in enumerate(items):
                pygame.draw.rect(ventana, color, (x_ley, y_ley + i*22, 14, 14))
                lbl = fuente_peq.render(nombre, True, BLANCO)
                ventana.blit(lbl, (x_ley + 20, y_ley + i*22 - 2))
        else:
            # proyectar el punto central de cada objeto con la cámara correspondiente
            if vista_actual == 1:
                cam_usar = camara
                centrox = ANCHO//2; centroy = ALTO//2
                proy_func = cam_usar.proyectar_perspectiva
            elif vista_actual == 2:
                cam_usar = cam_top
                centrox = ANCHO//2; centroy = ALTO//2
                proy_func = cam_usar.proyectar_elevacion
            elif vista_actual == 3:
                cam_usar = cam_iso
                centrox = ANCHO//2; centroy = ALTO//2
                proy_func = cam_usar.proyectar_isometrica
            else:
                cam_usar = camara
                centrox = ANCHO//2; centroy = ALTO//2
                proy_func = cam_usar.proyectar_perspectiva
            for obj in proyecto:
                # filtrar etiquetas de terreno/áreas grandes
                if obj.nombre in ("Terreno", "Área césped", "Camino principal"):
                    continue
                c = obj.posicion
                try:
                    if proy_func == cam_usar.proyectar_elevacion and vista_actual == 2:
                        pt = proy_func(c, centrox, centroy, 'superior', 1.0)
                    else:
                        pt = proy_func(c, centrox, centroy)
                except TypeError:
                    pt = proy_func(c, centrox, centroy)
                if pt:
                    lbl = fuente_peq.render(obj.nombre, True, BLANCO)
                    ventana.blit(lbl, (pt[0] - lbl.get_width()//2, pt[1] - 14))

    pygame.display.flip()

pygame.quit()
sys.exit()
