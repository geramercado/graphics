from vpython import *

# --- Configuración inicial ---
scene.title = "Animación 3D controlada por el usuario (Mario Style)"
scene.width = 1000
scene.height = 600
scene.background = color.cyan
scene.center = vector(0, 2, 0)
scene.forward = vector(0, -0.2, -1)

# --- Suelo y plataformas ---
ground = box(pos=vector(0, 0, 0), size=vector(40, 0.5, 20), color=color.green)
plataformas = [
    box(pos=vector(5, 2, 0), size=vector(4, 0.5, 4), color=color.orange),
    box(pos=vector(-5, 4, 0), size=vector(4, 0.5, 4), color=color.yellow),
    box(pos=vector(10, 6, 0), size=vector(4, 0.5, 4), color=color.red)
]

# --- Enemigo simple ---
enemigo = sphere(pos=vector(8, 0.5, 0), radius=0.5, color=color.magenta, make_trail=False)
enemigo_direccion = -0.05

# --- Personaje principal ---
body = cylinder(pos=vector(0, 1, 0), axis=vector(0, 1.5, 0), radius=0.4, color=color.blue)
head = sphere(pos=body.pos + vector(0, 2, 0), radius=0.5, color=color.red)
hand_L = sphere(pos=body.pos + vector(-0.6, 1.3, 0), radius=0.2, color=color.white)
hand_R = sphere(pos=body.pos + vector(0.6, 1.3, 0), radius=0.2, color=color.white)
foot_L = sphere(pos=body.pos + vector(-0.3, 0, 0), radius=0.2, color=color.black)
foot_R = sphere(pos=body.pos + vector(0.3, 0, 0), radius=0.2, color=color.black)

# --- Variables de control ---
velocity_y = 0
is_jumping = False
speed = 0.2
direction = 0  # Ángulo de rotación en grados

# --- Entrada de teclas ---
keys = {"left": False, "right": False, "forward": False, "backward": False, "shift": False, "space": False}

def keydown(evt):
    s = evt.key
    if s in ['left', 'a']: keys["left"] = True
    if s in ['right', 'd']: keys["right"] = True
    if s in ['up', 'w']: keys["forward"] = True
    if s in ['down', 's']: keys["backward"] = True
    if s == 'shift': keys["shift"] = True
    if s == ' ': keys["space"] = True

def keyup(evt):
    s = evt.key
    if s in ['left', 'a']: keys["left"] = False
    if s in ['right', 'd']: keys["right"] = False
    if s in ['up', 'w']: keys["forward"] = False
    if s in ['down', 's']: keys["backward"] = False
    if s == 'shift': keys["shift"] = False
    if s == ' ': keys["space"] = False

scene.bind('keydown', keydown)
scene.bind('keyup', keyup)

# --- Bucle principal ---
dt = 0.01
while True:
    rate(100)

    # Movimiento enemigo simple (va de un lado a otro)
    enemigo.pos.x += enemigo_direccion
    if enemigo.pos.x < 6 or enemigo.pos.x > 10:
        enemigo_direccion *= -1

    # Control de movimiento lateral y rotación
    move_dir = vector(0, 0, 0)
    if keys["left"]: 
        direction += 3
    if keys["right"]: 
        direction -= 3
    if keys["forward"]: 
        move_dir = vector(sin(radians(direction)), 0, cos(radians(direction)))
    if keys["backward"]: 
        move_dir = vector(-sin(radians(direction)), 0, -cos(radians(direction)))

    current_speed = speed * (2 if keys["shift"] else 1)
    body.pos += move_dir * current_speed

    # --- SALTO y GRAVEDAD ---
    if keys["space"] and not is_jumping:
        velocity_y = 0.3
        is_jumping = True

    velocity_y -= 0.01
    body.pos.y += velocity_y

    # --- DETECCIÓN DE PLATAFORMAS ---
    on_platform = False
    for plat in plataformas:
        if abs(body.pos.x - plat.pos.x) < 1.5 and abs(body.pos.z - plat.pos.z) < 1.5:
            top_surface = plat.pos.y + plat.size.y / 2
            if 0 < (body.pos.y - top_surface) < 1:
                body.pos.y = top_surface + 0.75
                velocity_y = 0
                on_platform = True
                is_jumping = False
                break

    # --- Suelo ---
    if body.pos.y <= 0.75:
        body.pos.y = 0.75
        velocity_y = 0
        is_jumping = False

    # --- Actualiza las partes del cuerpo ---
    head.pos = body.pos + vector(0, 1.5, 0)
    hand_L.pos = body.pos + vector(-0.6 * cos(radians(direction)), 1.3, -0.6 * sin(radians(direction)))
    hand_R.pos = body.pos + vector(0.6 * cos(radians(direction)), 1.3, 0.6 * sin(radians(direction)))
    foot_L.pos = body.pos + vector(-0.3 * cos(radians(direction)), 0, -0.3 * sin(radians(direction)))
    foot_R.pos = body.pos + vector(0.3 * cos(radians(direction)), 0, 0.3 * sin(radians(direction)))

    # --- Cámara dinámica ---
    scene.center = body.pos + vector(0, 1, 0)
    scene.forward = vector(sin(radians(direction)) * -1, -0.2, cos(radians(direction)) * -1)
