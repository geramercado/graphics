import pygame
import sys
import random
import math

# --- Inicialización ---
pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Animación 2D tipo Mario Bros")
clock = pygame.time.Clock()

# --- Colores ---
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (80, 120, 255)
ROJO = (255, 50, 50)
VERDE = (0, 200, 0)
AMARILLO = (255, 220, 0)
CAFE = (139, 69, 19)
GRIS = (150, 150, 150)

# --- Variables del jugador ---
x, y = 100, 500
vel_x = 0
vel_y = 0
en_suelo = False
gravedad = 1
velocidad = 5
tiempo = 0
vidas = 3
puntos = 0

# --- Suelo y bloques ---
suelo_y = 550
bloques = [
    pygame.Rect(0, suelo_y, ANCHO, 50),            # suelo
    pygame.Rect(200, 450, 100, 20),                # bloque flotante 1
    pygame.Rect(350, 350, 100, 20),                # bloque flotante 2
    pygame.Rect(500, 250, 100, 20),                # bloque flotante 3
]

# --- Monedas y enemigos ---
monedas = [pygame.Rect(random.randint(150, 700), random.randint(200, 400), 15, 15) for _ in range(5)]
enemigos = [pygame.Rect(random.randint(300, 700), suelo_y - 40, 30, 30) for _ in range(2)]

# --- Función para dibujar el jugador ---
def dibujar_jugador(x, y, tiempo, en_suelo):
    paso = math.sin(tiempo * 0.2) * 10 if en_suelo else 0

    # Cuerpo
    pygame.draw.rect(pantalla, ROJO, (x - 10, y - 40, 20, 40))  # cuerpo

    # Cabeza
    pygame.draw.circle(pantalla, AMARILLO, (x, y - 55), 13)

    # Piernas
    pygame.draw.line(pantalla, NEGRO, (x, y), (x - 8, y + 20 - paso), 5)
    pygame.draw.line(pantalla, NEGRO, (x, y), (x + 8, y + 20 + paso), 5)

# --- Bucle principal ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    teclas = pygame.key.get_pressed()

    # Movimiento horizontal
    vel_x = 0
    if teclas[pygame.K_LEFT]:
        vel_x = -velocidad
    if teclas[pygame.K_RIGHT]:
        vel_x = velocidad

    # Salto
    if teclas[pygame.K_UP] and en_suelo:
        vel_y = -18
        en_suelo = False

    # Aplicar movimiento y gravedad
    x += vel_x
    vel_y += gravedad
    y += vel_y

    # Colisiones con suelo y bloques
    en_suelo = False
    for bloque in bloques:
        if bloque.colliderect(x - 10, y - 40, 20, 40):
            # Desde arriba
            if vel_y > 0 and y - 40 < bloque.top < y:
                y = bloque.top
                vel_y = 0
                en_suelo = True
            # Desde abajo (golpea bloque)
            elif vel_y < 0 and y - 40 > bloque.bottom - 10:
                y = bloque.bottom + 40
                vel_y = 0

    # Límite inferior (pierde vida)
    if y > ALTO:
        vidas -= 1
        x, y = 100, 500
        vel_y = 0
        if vidas <= 0:
            print("GAME OVER")
            pygame.quit()
            sys.exit()

    # Recoge monedas
    for moneda in monedas[:]:
        if moneda.colliderect(x - 10, y - 40, 20, 40):
            monedas.remove(moneda)
            puntos += 10

    # Movimiento y colisión enemigos
    for enemigo in enemigos:
        enemigo.x += random.choice([-2, 2])  # se mueven de forma aleatoria
        if enemigo.colliderect(x - 10, y - 40, 20, 40):
            # Si cae encima del enemigo, lo elimina
            if vel_y > 0 and y - 35 < enemigo.top:
                enemigos.remove(enemigo)
                puntos += 20
                vel_y = -10  # rebote
            else:
                vidas -= 1
                x, y = 100, 500
                vel_y = 0
                if vidas <= 0:
                    print("GAME OVER")
                    pygame.quit()
                    sys.exit()

    # Bordes pantalla
    if x < 20:
        x = 20
    elif x > ANCHO - 20:
        x = ANCHO - 20

    if en_suelo:
        tiempo += 1

    # --- Dibujar escena ---
    pantalla.fill((135, 206, 235))  # cielo
    pygame.draw.rect(pantalla, (100, 200, 100), (0, suelo_y, ANCHO, 50))  # suelo

    # Bloques
    for b in bloques:
        pygame.draw.rect(pantalla, CAFE, b)

    # Monedas
    for m in monedas:
        pygame.draw.circle(pantalla, AMARILLO, m.center, 8)

    # Enemigos
    for e in enemigos:
        pygame.draw.rect(pantalla, NEGRO, e)

    # Jugador
    dibujar_jugador(int(x), int(y), tiempo, en_suelo)

    # HUD
    fuente = pygame.font.SysFont("Arial", 22)
    texto = fuente.render(f"Puntos: {puntos}   Vidas: {vidas}", True, NEGRO)
    pantalla.blit(texto, (10, 10))

    pygame.display.flip()
    clock.tick(30)
