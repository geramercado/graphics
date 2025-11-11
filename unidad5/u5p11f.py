import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configuración
ANCHO, ALTO = 800, 450
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mario 2D con Bloques y Monedas")
clock = pygame.time.Clock()

# Colores
AZUL_CIELO = (135, 206, 250)
VERDE_SUELO = (60, 179, 113)
DORADO = (255, 215, 0)
CAFE = (139, 69, 19)
ROJO = (200, 30, 30)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Clase Mario (dibujado con partes)
class Mario(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = ALTO - 120
        self.vel_y = 0
        self.en_suelo = False

    def draw_mario(self):
        self.image.fill((0, 0, 0, 0))
        # Cabeza
        pygame.draw.circle(self.image, (255, 200, 150), (20, 10), 10)
        # Cuerpo
        pygame.draw.rect(self.image, ROJO, (10, 20, 20, 25))
        # Brazos
        pygame.draw.line(self.image, ROJO, (10, 25), (0, 35), 5)
        pygame.draw.line(self.image, ROJO, (30, 25), (40, 35), 5)
        # Piernas
        pygame.draw.line(self.image, (0, 0, 255), (15, 45), (15, 60), 5)
        pygame.draw.line(self.image, (0, 0, 255), (25, 45), (25, 60), 5)

    def update(self, keys, plataformas):
        self.draw_mario()

        # Movimiento lateral
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        # Saltar
        if keys[pygame.K_SPACE] and self.en_suelo:
            self.vel_y = -15
            self.en_suelo = False

        # Gravedad
        self.vel_y += 1
        self.rect.y += self.vel_y

        # Suelo
        if self.rect.bottom >= ALTO - 60:
            self.rect.bottom = ALTO - 60
            self.vel_y = 0
            self.en_suelo = True

        # Colisión con plataformas
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect) and self.vel_y >= 0:
                self.rect.bottom = plataforma.rect.top
                self.vel_y = 0
                self.en_suelo = True

# Clase Plataforma (bloques en el cielo)
class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h=20):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(CAFE)
        self.rect = self.image.get_rect(topleft=(x, y))

# Clase Moneda
class Moneda(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, DORADO, (10, 10), 10)
        self.rect = self.image.get_rect(center=(x, y))

# Clase Enemigo
class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((139, 69, 19))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = ALTO - 100
        self.vel_x = random.choice([-2, 2])

    def update(self):
        self.rect.x += self.vel_x
        if self.rect.right >= ANCHO or self.rect.left <= 0:
            self.vel_x *= -1

# Crear objetos
mario = Mario()
plataformas = pygame.sprite.Group()
monedas = pygame.sprite.Group()
enemigos = pygame.sprite.Group()
todos = pygame.sprite.Group()

# Suelo
suelo = pygame.Rect(0, ALTO - 60, ANCHO, 60)

# Agregar plataformas
niveles = [(200, 300, 120), (400, 250, 100), (600, 180, 140)]
for x, y, w in niveles:
    p = Plataforma(x, y, w)
    plataformas.add(p)
    todos.add(p)

# Agregar monedas
for i in range(8):
    x = random.randint(100, 700)
    y = random.randint(100, 300)
    moneda = Moneda(x, y)
    monedas.add(moneda)
    todos.add(moneda)

# Agregar enemigos
for i in range(3):
    e = Enemigo(random.randint(200, 700))
    enemigos.add(e)
    todos.add(e)

todos.add(mario)

# Variables de juego
vidas = 3
puntos = 0
jugando = True

# Bucle principal
while jugando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    mario.update(keys, plataformas)
    enemigos.update()

    # Colisión Mario - monedas
    colision_monedas = pygame.sprite.spritecollide(mario, monedas, True)
    puntos += len(colision_monedas) * 10

    # Colisión Mario - enemigos
    colisiones = pygame.sprite.spritecollide(mario, enemigos, False)
    for enemigo in colisiones:
        if mario.vel_y > 0 and mario.rect.bottom <= enemigo.rect.top + 20:
            enemigos.remove(enemigo)
            todos.remove(enemigo)
            mario.vel_y = -10
            puntos += 20
        else:
            vidas -= 1
            mario.rect.x, mario.rect.y = 100, ALTO - 120
            if vidas == 0:
                jugando = False

    # Dibujar pantalla
    pantalla.fill(AZUL_CIELO)
    pygame.draw.rect(pantalla, VERDE_SUELO, suelo)
    todos.draw(pantalla)

    # Mostrar HUD
    fuente = pygame.font.SysFont("Arial", 24)
    texto_vidas = fuente.render(f"Vidas: {vidas}", True, BLANCO)
    texto_puntos = fuente.render(f"Puntos: {puntos}", True, BLANCO)
    pantalla.blit(texto_vidas, (10, 10))
    pantalla.blit(texto_puntos, (10, 40))

    pygame.display.flip()
    clock.tick(60)

# Fin del juego
pantalla.fill(NEGRO)
fuente_final = pygame.font.SysFont("Arial", 40)
pantalla.blit(fuente_final.render("¡Juego Terminado!", True, BLANCO), (ANCHO//2 - 150, ALTO//2 - 20))
pantalla.blit(fuente_final.render(f"Puntaje final: {puntos}", True, DORADO), (ANCHO//2 - 160, ALTO//2 + 30))
pygame.display.flip()
pygame.time.wait(3000)
pygame.quit()
