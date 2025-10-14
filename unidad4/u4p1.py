#Relleno de poligonos con metodos basados en la ciencia de food fill and scan line
#unidad 4 practica 1
#Gerardo Mercado Hurtado
#Raúl Martínez Martínez
import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot  y su Perro Robot (Gerardo/Raúl)")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 80, 80)
GREEN = (100, 255, 100)
BLUE = (120, 150, 255)
YELLOW = (255, 255, 120)
GRAY = (180, 180, 180)
DARK_GRAY = (80, 80, 80)

def draw_filled_polygon(surface, vertices, color, border_color=BLACK):
    """Rellena y dibuja el contorno y vértices de un polígono"""
    pygame.draw.polygon(surface, color, vertices)
    pygame.draw.polygon(surface, border_color, vertices, 2)
    for vertex in vertices:
        pygame.draw.circle(surface, RED, vertex, 4)

def crear_robot(x, y):
    """Crea las partes del robot principal"""
    # Cabeza triangular
    cabeza = [(x, y), (x - 40, y + 80), (x + 40, y + 80)]
    
    # Cuerpo cuadrado
    cuerpo = [(x - 60, y + 80), (x - 60, y + 200), (x + 60, y + 200), (x + 60, y + 80)]
    
    # Brazos
    brazo_izq = [(x - 80, y + 90), (x - 100, y + 160), (x - 80, y + 160), (x - 60, y + 90)]
    brazo_der = [(x + 80, y + 90), (x + 100, y + 160), (x + 80, y + 160), (x + 60, y + 90)]
    
    # Piernas
    pierna_izq = [(x - 40, y + 200), (x - 40, y + 280), (x, y + 280), (x, y + 200)]
    pierna_der = [(x + 40, y + 200), (x + 40, y + 280), (x + 5, y + 280), (x + 5, y + 200)]
    
    # Dibujar todas las partes
    draw_filled_polygon(screen, cabeza, BLUE)
    draw_filled_polygon(screen, cuerpo, GRAY)
    draw_filled_polygon(screen, brazo_izq, DARK_GRAY)
    draw_filled_polygon(screen, brazo_der, DARK_GRAY)
    draw_filled_polygon(screen, pierna_izq, DARK_GRAY)
    draw_filled_polygon(screen, pierna_der, DARK_GRAY)
    
    # Texto
    font = pygame.font.Font(None, 36)
    label = font.render("Robot Principal", True, BLACK)
    screen.blit(label, (x - 80, y - 40))

def crear_perro(x, y):
    """Crea las partes del perro robot"""
    # Cuerpo hexagonal
    cuerpo = [(x, y), (x - 40, y + 20), (x - 40, y + 60),
              (x, y + 80), (x + 40, y + 60), (x + 40, y + 20)]
    
    # Cabeza cuadrada
    cabeza = [(x + 50, y + 10), (x + 50, y + 50), (x + 90, y + 50), (x + 90, y + 10)]
    
    # Patas
    pata1 = [(x - 30, y + 70), (x - 20, y + 90), (x - 10, y + 90), (x - 20, y + 70)]
    pata2 = [(x + 10, y + 70), (x + 20, y + 90), (x + 30, y + 90), (x + 20, y + 70)]
    
    # Dibujar
    draw_filled_polygon(screen, cuerpo, YELLOW)
    draw_filled_polygon(screen, cabeza, GREEN)
    draw_filled_polygon(screen, pata1, DARK_GRAY)
    draw_filled_polygon(screen, pata2, DARK_GRAY)
    
    # Texto
    font = pygame.font.Font(None, 30)
    label = font.render("Perro Robot", True, BLACK)
    screen.blit(label, (x - 40, y - 40))

def main():
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(WHITE)
        
        # Dibujar robot y perro robot
        crear_robot(400, 200)
        crear_perro(650, 350)
        
        # Suelo y título
        pygame.draw.line(screen, BLACK, (0, 500), (WIDTH, 500), 3)
        font = pygame.font.Font(None, 40)
        titulo = font.render("Robot con Cabeza Triangular y su Perro Robot", True, RED)
        screen.blit(titulo, (120, 40))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
