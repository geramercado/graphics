import pygame
import sys

# --- Inicialización ---
pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Frankenstein 2D by GerardoMH")
clock = pygame.time.Clock()

# --- Colores ---
BLANCO = (255, 255, 255)
GRIS_CADAVERICO = (180, 180, 190)  # Piel pálida
NEGRO = (0, 0, 0)
MARRON_OSCURO_ABRIGO = (30, 20, 10) # Abrigo muy oscuro, casi negro
ROJO_OSCURO_HERIDA = (100, 0, 0) # Para simular heridas
GRIS_CLARO = (200, 200, 200) # Para el efecto de nieve/desgaste en el abrigo

# --- Personaje ---
x, y = 100, 400
velocidad = 5
salto = False
vel_y = 0
gravedad = 1

# --- Bucle principal ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # --- Movimiento con teclas ---
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        x -= velocidad
    if teclas[pygame.K_RIGHT]:
        x += velocidad
    if teclas[pygame.K_UP] and not salto:
        salto = True
        vel_y = -15  # impulso de salto

    # --- Física del salto ---
    if salto:
        y += vel_y
        vel_y += gravedad
        if y >= 400:  # suelo
            y = 400
            salto = False

    # --- Dibujar ---
    pantalla.fill(BLANCO)

    # Cuerpo (abrigo con capucha)
    # Cuerpo principal del abrigo
    pygame.draw.rect(pantalla, MARRON_OSCURO_ABRIGO, (x, y, 50, 80))
    # Capucha (por encima de la cabeza y conectada al cuerpo)
    pygame.draw.polygon(pantalla, MARRON_OSCURO_ABRIGO, [(x - 10, y - 50), (x + 60, y - 50), (x + 55, y - 20), (x - 5, y - 20)])
    # Detalles de "nieve" o desgaste en el abrigo y la capucha
    pygame.draw.line(pantalla, GRIS_CLARO, (x + 5, y + 5), (x + 15, y + 5), 2)
    pygame.draw.line(pantalla, GRIS_CLARO, (x + 35, y + 10), (x + 45, y + 10), 2)
    pygame.draw.line(pantalla, GRIS_CLARO, (x + 0, y + 60), (x + 10, y + 65), 2)
    pygame.draw.line(pantalla, GRIS_CLARO, (x + 50, y + 60), (x + 40, y + 65), 2)
    pygame.draw.line(pantalla, GRIS_CLARO, (x + 10, y - 45), (x + 20, y - 40), 2) # Nieve en capucha
    pygame.draw.line(pantalla, GRIS_CLARO, (x + 40, y - 45), (x + 30, y - 40), 2) # Nieve en capucha

    # Cabeza (Frankenstein pálido)
    pygame.draw.circle(pantalla, GRIS_CADAVERICO, (x + 25, y - 20), 20)
    
    # Rasgos faciales más sombríos y cicatrices
    # Ojos (más hundidos o pequeños)
    pygame.draw.circle(pantalla, NEGRO, (x + 19, y - 28), 2)
    pygame.draw.circle(pantalla, NEGRO, (x + 31, y - 28), 2)
    # Boca (línea recta o ligeramente hacia abajo)
    pygame.draw.line(pantalla, NEGRO, (x + 18, y - 15), (x + 32, y - 15), 1)
    
    # Cicatrices / Costuras (más prominentes y con posible color de herida)
    pygame.draw.line(pantalla, NEGRO, (x + 15, y - 35), (x + 35, y - 25), 2) # Cicatriz en la frente/lado
    pygame.draw.line(pantalla, NEGRO, (x + 10, y - 20), (x + 25, y - 10), 2) # Cicatriz bajando por la cara
    pygame.draw.line(pantalla, ROJO_OSCURO_HERIDA, (x + 12, y - 18), (x + 23, y - 12), 1) # Sombra de herida
    pygame.draw.line(pantalla, NEGRO, (x + 25, y - 5), (x + 30, y + 5), 2) # Cicatriz en el cuello
    
    # --- Actualizar pantalla ---
    pygame.display.flip()
    clock.tick(30)
