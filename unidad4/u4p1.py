import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Relleno Visual Paso a Paso")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def draw_filled_polygon(surface, vertices, color):
    """Función simple que SÍ rellena el polígono"""
    if len(vertices) < 3:
        return
    
    # Usar la función integrada de Pygame para rellenar
    pygame.draw.polygon(surface, color, vertices)
    
    # Dibujar contorno
    pygame.draw.polygon(surface, BLUE, vertices, 2)
    
    # Dibujar vértices
    for vertex in vertices:
        pygame.draw.circle(surface, RED, vertex, 5)

def main_simple():
    # Polígonos de ejemplo
    triangle = [(400, 100), (300, 300), (500, 300)]
    square = [(100, 100), (100, 300), (300, 300), (300, 100)]
    pentagon = [(600, 150), (550, 250), (600, 350), (700, 350), (750, 250)]
    hexagon = [(200, 400), (100, 450), (100, 550), (200, 600), (300, 550), (300, 450)]
    
    running = True
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(WHITE)
        
        # Dibujar polígonos rellenos
        draw_filled_polygon(screen, triangle, (255, 200, 200))  # Rosa
        draw_filled_polygon(screen, square, (200, 255, 200))    # Verde claro
        draw_filled_polygon(screen, pentagon, (200, 200, 255))  # Azul claro
        draw_filled_polygon(screen, hexagon, (255, 255, 200))   # Amarillo claro
        
        # Etiquetas
        labels = [
            ("Triángulo", (400, 50)),
            ("Cuadrado", (200, 50)), 
            ("Pentágono", (650, 50)),
            ("Hexágono", (200, 380))
        ]
        
        for text, pos in labels:
            label = font.render(text, True, BLACK)
            screen.blit(label, pos)
        
        # Instrucción
        inst = font.render("Estos polígonos están rellenos con color homogéneo", True, RED)
        screen.blit(inst, (100, HEIGHT - 50))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

# Ejecutar la versión simple para ver resultados inmediatos
if __name__ == "__main__":
    main_simple()


