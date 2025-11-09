from vpython import *
import math

# ---------------- ESCENA ----------------
scene = canvas(title="Animación 3D - Fase 3: entorno y cámara dinámica",
               width=1000, height=600, background=color.cyan)
scene.forward = vector(-1, -0.3, -1)
scene.range = 10

# Luz ambiental simulada
local_light(pos=vector(5,10,0), color=color.white)

# Suelo principal
floor = box(pos=vector(0,0,0), size=vector(40,0.2,40), color=color.green)

# Plataformas adicionales
platforms = [
    box(pos=vector(5,1,0), size=vector(4,0.2,4), color=color.orange),
    box(pos=vector(10,2,0), size=vector(3,0.2,3), color=color.red),
    box(pos=vector(15,3,0), size=vector(2,0.2,2), color=color.blue)
]

# ---------------- PERSONAJE ----------------
body = cylinder(pos=vector(0,1,0), axis=vector(0,1,0), radius=0.28, color=color.red)
head = sphere(pos=vector(0,2.2,0), radius=0.22, color=color.yellow)

leg_left = cylinder(pos=vector(-0.15,0.5,0), axis=vector(0,-0.5,0), radius=0.07, color=color.blue)
leg_right = cylinder(pos=vector(0.15,0.5,0), axis=vector(0,-0.5,0), radius=0.07, color=color.blue)

arm_left = cylinder(pos=vector(-0.4,1.6,0), axis=vector(0.35,-0.6,0), radius=0.06, color=color.orange)
arm_right = cylinder(pos=vector(0.4,1.6,0), axis=vector(-0.35,-0.6,0), radius=0.06, color=color.orange)

# ---------------- FÍSICA Y ESTADO ----------------
posicion = vector(0,0,0)
vel_y = 0.0
g = -9.8
en_suelo = True

keys = {"left":False, "right":False, "run":False, "space":False}

def keydown(evt):
    k = evt.key
    if k in ["left", "a"]:
        keys["left"] = True
    elif k in ["right", "d"]:
        keys["right"] = True
    elif k in ["shift", "r"]:
        keys["run"] = True
    elif k in [" ", "space"]:
        keys["space"] = True

def keyup(evt):
    k = evt.key
    if k in ["left", "a"]:
        keys["left"] = False
    elif k in ["right", "d"]:
        keys["right"] = False
    elif k in ["shift", "r"]:
        keys["run"] = False
    elif k in [" ", "space"]:
        keys["space"] = False

scene.bind("keydown", keydown)
scene.bind("keyup", keyup)

# ---------------- PARÁMETROS DE MOVIMIENTO ----------------
walk_speed = 2.5
run_speed = 5.0
jump_impulse = 6.0
dt = 0.01
t = 0.0

# ---------------- BUCLE PRINCIPAL ----------------
while True:
    rate(1/dt)
    walking = False
    direction = 0
    speed = walk_speed

    # Control de velocidad
    if keys["run"]:
        speed = run_speed

    # Movimiento lateral
    if keys["left"]:
        posicion.x -= speed * dt
        walking = True
        direction = -1
    if keys["right"]:
        posicion.x += speed * dt
        walking = True
        direction = 1

    # Salto
    if keys["space"] and en_suelo:
        vel_y = jump_impulse
        en_suelo = False
        keys["space"] = False

    # Gravedad
    if not en_suelo:
        vel_y += g * dt
        posicion.y += vel_y * dt
        if posicion.y <= 0:
            posicion.y = 0
            vel_y = 0
            en_suelo = True
        else:
            # Chequeo de plataformas
            for p in platforms:
                top = p.pos.y + p.size.y/2
                half_x = p.size.x/2
                if abs(posicion.x - p.pos.x) < half_x and abs(posicion.y - top) < 0.1 and vel_y < 0:
                    posicion.y = top
                    vel_y = 0
                    en_suelo = True

    # Actualiza cuerpo
    body.pos = vector(posicion.x, 1 + posicion.y, posicion.z)
    head.pos = vector(posicion.x, 2.2 + posicion.y, posicion.z)
    leg_left.pos = vector(posicion.x - 0.15, 1 + posicion.y, posicion.z)
    leg_right.pos = vector(posicion.x + 0.15, 1 + posicion.y, posicion.z)
    arm_left.pos = vector(posicion.x - 0.4, 1.6 + posicion.y, posicion.z)
    arm_right.pos = vector(posicion.x + 0.4, 1.6 + posicion.y, posicion.z)

    # Animación
    if walking:
        t += dt * 10
        swing = math.sin(t)
        leg_left.axis = vector(0, -0.5 + 0.18*swing, 0.15*swing)
        leg_right.axis = vector(0, -0.5 - 0.18*swing, -0.15*swing)
        arm_left.axis = vector(0.35*math.cos(t), -0.55 + 0.08*swing, 0.1*swing)
        arm_right.axis = vector(-0.35*math.cos(t), -0.55 - 0.08*swing, -0.1*swing)
    else:
        leg_left.axis = vector(0, -0.5, 0)
        leg_right.axis = vector(0, -0.5, 0)
        arm_left.axis = vector(0.35, -0.6, 0)
        arm_right.axis = vector(-0.35, -0.6, 0)

    # Cámara dinámica (tercera persona)
    camera_target = vector(posicion.x, 1.5 + posicion.y, posicion.z)
    scene.center = scene.center * 0.9 + camera_target * 0.1
    scene.forward = vector(-1, -0.2, -1)
