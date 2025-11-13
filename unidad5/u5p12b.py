from vpython import *

# Escena básica
scene = canvas(title="Animación 3D controlada por el usuario",
               width=800, height=600, center=vector(0,1,0),
               background=color.cyan)

# Suelo
floor = box(pos=vector(0,0,0), size=vector(20,0.2,20), color=color.green)

# ------------------------------ Personaje burro nave espacial

# Cuerpo
body = ellipsoid(pos=vector(0,1,0), size=vector(1.2,0.6,0.4), color=color.gray(0.5))

# Cabeza
head = ellipsoid(pos=vector(0,1.4,0.35), size=vector(0.4,0.3,0.3), color=color.gray(0.6))

# Hocico
nose = sphere(pos=vector(0,1.35,0.55), radius=0.12, color=color.gray(0.4))

# Orejas
ear_L = cone(pos=vector(-0.15,1.65,0.25), axis=vector(0,0.25,0), radius=0.07, color=color.gray(0.6))
ear_R = cone(pos=vector(0.15,1.65,0.25), axis=vector(0,0.25,0), radius=0.07, color=color.gray(0.6))

# Patas
leg_FL = cylinder(pos=vector(-0.35,0.3,0.15), axis=vector(0,-0.6,0), radius=0.08, color=color.gray(0.4))
leg_FR = cylinder(pos=vector(0.35,0.3,0.15), axis=vector(0,-0.6,0), radius=0.08, color=color.gray(0.4))
leg_BL = cylinder(pos=vector(-0.35,0.3,-0.15), axis=vector(0,-0.6,0), radius=0.08, color=color.gray(0.4))
leg_BR = cylinder(pos=vector(0.35,0.3,-0.15), axis=vector(0,-0.6,0), radius=0.08, color=color.gray(0.4))

# Cola
tail = cone(pos=vector(0,1,-0.4), axis=vector(0,-0.2,-0.2), radius=0.05, color=color.gray(0.3))

# ------------------------------
posicion = vector(0,0,0)
angulo = 0
velocidad = 0.1
fase_patas = 0
salto = False
altura_salto = 0

# Lista de partículas verdes
particulas = []

scene.forward = vector(-1,-0.3,-1)

# ------------------------------
# bucle principal

while True:
    rate(60)
    keys = keysdown()

    caminando = False

    # Movimiento
    if 'up' in keys:
        posicion += vector(velocidad*sin(angulo), 0, velocidad*cos(angulo))
        caminando = True

    if 'down' in keys:
        posicion -= vector(velocidad*sin(angulo), 0, velocidad*cos(angulo))
        caminando = True

    # Girar
    if 'left' in keys:
        angulo -= 0.08
    if 'right' in keys:
        angulo += 0.08

    # Saltar
    if 'space' in keys and not salto:
        salto = True
        altura_salto = 0.15

    # Simulación salto
    if salto:
        for parte in [body, head, nose, ear_L, ear_R, leg_FL, leg_FR, leg_BL, leg_BR, tail]:
            parte.pos.y += altura_salto
        altura_salto -= 0.01

        if body.pos.y <= 1:
            salto = False
            body.pos.y = 1
            head.pos.y = 1.4
            nose.pos.y = 1.35
            ear_L.pos.y = 1.65
            ear_R.pos.y = 1.65
            leg_FL.pos.y = 0.3
            leg_FR.pos.y = 0.3
            leg_BL.pos.y = 0.3
            leg_BR.pos.y = 0.3
            tail.pos.y = 1

    # ------------------------------
    # Animación de patas
    if caminando:
        fase_patas += 0.12
        amp = 0.3

        leg_FL.axis = vector(0.2*sin(fase_patas)*amp, -0.6, 0)
        leg_BR.axis = vector(0.2*sin(fase_patas)*amp, -0.6, 0)

        leg_FR.axis = vector(-0.2*sin(fase_patas)*amp, -0.6, 0)
        leg_BL.axis = vector(-0.2*sin(fase_patas)*amp, -0.6, 0)
    else:
        leg_FL.axis = vector(0,-0.6,0)
        leg_FR.axis = vector(0,-0.6,0)
        leg_BL.axis = vector(0,-0.6,0)
        leg_BR.axis = vector(0,-0.6,0)

    # ------------------------------
    # Estela
    if caminando:
        pedo = sphere(
            pos=vector(posicion.x, 0.3, posicion.z - 0.6),
            radius=0.12,
            color=vector(0,1,0),
            opacity=0.7,
            shininess=0
        )
        particulas.append(pedo)

    # Actualizar partículas
    for p in particulas[:]:
        p.opacity -= 0.02
        p.radius += 0.005
        if p.opacity <= 0:
            p.visible = False
            particulas.remove(p)

    # ------------------------------
    # Actualizar posición del burro
    body.pos = vector(posicion.x, body.pos.y, posicion.z)
    head.pos = vector(posicion.x, head.pos.y, posicion.z + 0.35)
    nose.pos = vector(posicion.x, nose.pos.y, posicion.z + 0.55)
    ear_L.pos = vector(posicion.x - 0.15*cos(angulo), ear_L.pos.y, posicion.z + 0.25)
    ear_R.pos = vector(posicion.x + 0.15*cos(angulo), ear_R.pos.y, posicion.z + 0.25)
    tail.pos = vector(posicion.x, tail.pos.y, posicion.z - 0.4)

    # Rotación del burro
    for parte in [body, head, nose, ear_L, ear_R, tail]:
        parte.axis = vector(sin(angulo), 0, cos(angulo))

    # Reposicionar patas
    leg_FL.pos = vector(posicion.x - 0.35*cos(angulo), leg_FL.pos.y, posicion.z + 0.15*sin(angulo))
    leg_FR.pos = vector(posicion.x + 0.35*cos(angulo), leg_FR.pos.y, posicion.z + 0.15*sin(angulo))
    leg_BL.pos = vector(posicion.x - 0.35*cos(angulo), leg_BL.pos.y, posicion.z - 0.15*sin(angulo))
    leg_BR.pos = vector(posicion.x + 0.35*cos(angulo), leg_BR.pos.y, posicion.z - 0.15*sin(angulo))
