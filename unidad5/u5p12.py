from vpython import *

# Escena básica
scene = canvas(title="Animación 3D controlada por el usuario",
               width=800, height=600, center=vector(0,1,0),
               background=color.cyan)

# Suelo
floor = box(pos=vector(0,0,0), size=vector(20,0.2,20), color=color.green)

# Personaje tipo “robot humanoide” hecho con formas 3D
body = box(pos=vector(0,1,0), size=vector(0.5,1,0.3), color=color.red)
head = sphere(pos=vector(0,1.7,0), radius=0.2, color=color.yellow)
arm_L = cylinder(pos=vector(-0.35,1.2,0), axis=vector(0,-0.5,0), radius=0.08, color=color.blue)
arm_R = cylinder(pos=vector(0.35,1.2,0), axis=vector(0,-0.5,0), radius=0.08, color=color.blue)
leg_L = cylinder(pos=vector(-0.15,0.5,0), axis=vector(0,-0.6,0), radius=0.08, color=color.white)
leg_R = cylinder(pos=vector(0.15,0.5,0), axis=vector(0,-0.6,0), radius=0.08, color=color.white)

# Variables de control
posicion = vector(0,0,0)
angulo = 0
velocidad = 0.1
salto = False
altura_salto = 0

# Movimiento de cámara y personaje
scene.forward = vector(-1,-0.3,-1)

# Bucle principal
while True:
    rate(60)

    # Teclas presionadas
    keys = keysdown()

    # Movimiento adelante / atrás
    if 'up' in keys:
        posicion += vector(velocidad*sin(angulo), 0, velocidad*cos(angulo))
    if 'down' in keys:
        posicion -= vector(velocidad*sin(angulo), 0, velocidad*cos(angulo))

    # Girar izquierda / derecha
    if 'left' in keys:
        angulo -= 0.08
    if 'right' in keys:
        angulo += 0.08

    # Saltar
    if 'space' in keys and not salto:
        salto = True
        altura_salto = 0.15

    # Simulación de salto
    if salto:
        body.pos.y += altura_salto
        head.pos.y += altura_salto
        arm_L.pos.y += altura_salto
        arm_R.pos.y += altura_salto
        leg_L.pos.y += altura_salto
        leg_R.pos.y += altura_salto
        altura_salto -= 0.01
        if body.pos.y <= 1:
            salto = False
            body.pos.y = 1
            head.pos.y = 1.7
            arm_L.pos.y = 1.2
            arm_R.pos.y = 1.2
            leg_L.pos.y = 0.5
            leg_R.pos.y = 0.5

    # Actualizar posición del cuerpo
    body.pos = vector(posicion.x, body.pos.y, posicion.z)
    head.pos = vector(posicion.x, head.pos.y, posicion.z)
    arm_L.pos = vector(posicion.x - 0.35*cos(angulo), arm_L.pos.y, posicion.z + 0.35*sin(angulo))
    arm_R.pos = vector(posicion.x + 0.35*cos(angulo), arm_R.pos.y, posicion.z - 0.35*sin(angulo))
    leg_L.pos = vector(posicion.x - 0.15*cos(angulo), leg_L.pos.y, posicion.z + 0.15*sin(angulo))
    leg_R.pos = vector(posicion.x + 0.15*cos(angulo), leg_R.pos.y, posicion.z - 0.15*sin(angulo))

    # Rotar personaje
    for parte in [body, head, arm_L, arm_R, leg_L, leg_R]:
        parte.axis = vector(sin(angulo), 0, cos(angulo))
