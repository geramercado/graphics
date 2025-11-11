import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 800, 400
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mini Mario Bros - Animación 2D")

# Colores
AZUL_CIELO = (135, 206, 250)
VERDE_SUELO = (60, 179, 113)
ROJO = (255, 0, 0)
MARRON = (139, 69, 19)
BLANCO = (255, 255, 255)

# Reloj para FPS
clock = pygame.time.Clock()

# Clase Mario
class Mario(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = ALTO - 120
        self.vel_y = 0
        self.en_suelo = True

    def update(self, keys):
        # Movimiento horizontal
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
        if self.rect.y >= ALTO - 120:
            self.rect.y = ALTO - 120
            self.vel_y = 0
            self.en_suelo = True

# Clase Enemigo (Goomba)
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

        # Rebote en bordes
        if self.rect.right >= ANCHO or self.rect.left <= 0:
            self.vel_x *= -1

# Grupo de sprites
mario = Mario()
enemigos = pygame.sprite.Group()
todos = pygame.sprite.Group()
todos.add(mario)

# Crear enemigos
for i in range(4):
    enemigo = Enemigo(random.randint(200, 700))
    enemigos.add(enemigo)
    todos.add(enemigo)

# Fondo
suelo_rect = pygame.Rect(0, ALTO - 60, ANCHO, 60)

# Juego principal
jugando = True
vidas = 3
while jugando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    mario.update(keys)
    enemigos.update()

    # Colisiones
    colisiones = pygame.sprite.spritecollide(mario, enemigos, False)
    for enemigo in colisiones:
        if mario.vel_y > 0 and mario.rect.bottom <= enemigo.rect.top + 20:
            enemigos.remove(enemigo)
            todos.remove(enemigo)
            mario.vel_y = -10
        else:
            vidas -= 1
            mario.rect.x, mario.rect.y = 100, ALTO - 120
            if vidas == 0:
                jugando = False

    # Dibujar
    pantalla.fill(AZUL_CIELO)
    pygame.draw.rect(pantalla, VERDE_SUELO, suelo_rect)
    todos.draw(pantalla)

    # Mostrar vidas
    fuente = pygame.font.SysFont("Arial", 24)
    texto = fuente.render(f"Vidas: {vidas}", True, BLANCO)
    pantalla.blit(texto, (10, 10))

    pygame.display.flip()
    clock.tick(60)

# Pantalla final
pantalla.fill((0, 0, 0))
texto_final = pygame.font.SysFont("Arial", 40).render("¡Juego Terminado!", True, BLANCO)
pantalla.blit(texto_final, (ANCHO//2 - 150, ALTO//2 - 20))
pygame.display.flip()
pygame.time.wait(2000)
pygame.quit()
