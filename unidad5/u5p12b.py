from vpython import *
import math

# ---------- Escena ----------
scene = canvas(title="Animación 3D - Salto funcional (corregido)",
               width=900, height=600, center=vector(0,1,0), background=color.cyan)

# Suelo
floor = box(pos=vector(0,0,0), size=vector(40,0.2,40), color=color.green)

# ---------- Personaje (partes) ----------
body = cylinder(pos=vector(0,1,0), axis=vector(0,1,0), radius=0.28, color=color.red)
head = sphere(pos=vector(0,2.2,0), radius=0.22, color=color.yellow)

leg_left = cylinder(pos=vector(-0.15,0.5,0), axis=vector(0,-0.5,0), radius=0.07, color=color.blue)
leg_right = cylinder(pos=vector(0.15,0.5,0), axis=vector(0,-0.5,0), radius=0.07, color=color.blue)

arm_left = cylinder(pos=vector(-0.4,1.6,0), axis=vector(0.35,-0.6,0), radius=0.06, color=color.orange)
arm_right = cylinder(pos=vector(0.4,1.6,0), axis=vector(-0.35,-0.6,0), radius=0.06, color=color.orange)

# ---------- Estado y física ----------
posicion = vector(0,0,0)      # x,z in posicion.x,z ; vertical stored in body.pos.y (1 + posicion.y)
vel_y = 0.0
g = -9.8                      # gravedad m/s^2 (usamos escala pequeña)
en_suelo = True

# controles (guardamos solo teclas que nos interesan)
keys_state = {'left': False, 'right': False, 'space': False}

# Mapeo de eventos: más robusto con espacios y con palabra "space"
def keydown(evt):
    k = evt.key
    if k == 'left' or k == 'a':
        keys_state['left'] = True
    elif k == 'right' or k == 'd':
        keys_state['right'] = True
    elif k == ' ' or k.lower() == 'space':
        keys_state['space'] = True

def keyup(evt):
    k = evt.key
    if k == 'left' or k == 'a':
        keys_state['left'] = False
    elif k == 'right' or k == 'd':
        keys_state['right'] = False
    elif k == ' ' or k.lower() == 'space':
        keys_state['space'] = False

scene.bind('keydown', keydown)
scene.bind('keyup', keyup)

# parámetros de movimiento
speed = 2.5          # velocidad horizontal (unidades/segundo)
jump_impulse = 5.0   # impulso inicial del salto (m/s)
dt = 0.01            # paso de tiempo
time_acc = 0.0
leg_phase = 0.0

# posición vertical inicial (posicion.y se usa en la integración)
posicion.y = 0.0
body.pos.y = 1 + posicion.y
head.pos.y = 2.2 + posicion.y
leg_left.pos.y = 1 + posicion.y - 0.5
leg_right.pos.y = 1 + posicion.y - 0.5
arm_left.pos.y = 1.6 + posicion.y
arm_right.pos.y = 1.6 + posicion.y

# cámara inicial
scene.forward = vector(-1, -0.3, -1)

# ---------- Bucle principal ----------
while True:
    rate(1/dt)

    # movimiento horizontal (usamos speed * dt)
    walking = False
    if keys_state['left']:
        posicion.x -= speed * dt
        walking = True
        direction = -1
    if keys_state['right']:
        posicion.x += speed * dt
        walking = True
        direction = 1

    # iniciar salto: sólo si está en suelo
    if keys_state['space'] and en_suelo:
        vel_y = jump_impulse
        en_suelo = False
        # evitar re-trigger inmediato; se volverá a True cuando suelte la tecla
        keys_state['space'] = False

    # integrar vertical (vel_y en unidades/seg)
    if not en_suelo:
        vel_y += g * dt                # gravedad
        posicion.y += vel_y * dt
        # detectar colisión con suelo (posicion.y <= 0)
        if posicion.y <= 0:
            posicion.y = 0
            vel_y = 0
            en_suelo = True

    # actualizar partes con la nueva posicion
    body.pos = vector(posicion.x, 1 + posicion.y, posicion.z)
    head.pos = vector(posicion.x, 2.2 + posicion.y, posicion.z)
    arm_left.pos = vector(posicion.x - 0.4, 1.6 + posicion.y, posicion.z)
    arm_right.pos = vector(posicion.x + 0.4, 1.6 + posicion.y, posicion.z)
    leg_left.pos = vector(posicion.x - 0.15, 1 + posicion.y, posicion.z)
    leg_right.pos = vector(posicion.x + 0.15, 1 + posicion.y, posicion.z)

    # animación de piernas sólo cuando camina
    if walking:
        time_acc += dt * 10            # controla velocidad de oscilación
        leg_phase = math.sin(time_acc)
        # movemos los ejes de las piernas para simular zancada
        leg_left.axis = vector(0, -0.5 + 0.18*leg_phase, 0.15*leg_phase)
        leg_right.axis = vector(0, -0.5 - 0.18*leg_phase, -0.15*leg_phase)
        # brazos contrarios a las piernas
        arm_left.axis = vector(0.35*math.cos(time_acc), -0.55 + 0.08*math.sin(time_acc), 0.1*math.sin(time_acc))
        arm_right.axis = vector(-0.35*math.cos(time_acc), -0.55 - 0.08*math.sin(time_acc), -0.1*math.sin(time_acc))
    else:
        # postura neutra
        leg_left.axis = vector(0, -0.5, 0)
        leg_right.axis = vector(0, -0.5, 0)
        arm_left.axis = vector(0.35, -0.6, 0)
        arm_right.axis = vector(-0.35, -0.6, 0)
        time_acc = 0

    # actualizar cámara: seguir al personaje (suavizado simple)
    scene.center = scene.center * 0.9 + vector(posicion.x, 1.0, 0) * 0.1

