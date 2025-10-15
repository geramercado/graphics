#degradado y textura
#Gerardo Mercado Hurtado
#Raúl Martínez Martínez
#importar las bibliotecas necesarias
import pygame
import numpy as np
import sys
import random

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Altar de Día de Muertos")

# --- Paleta de Colores Típica ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PAPEL_PICADO_COLORS = [(227, 63, 50), (243, 133, 53), (252, 224, 61), (63, 182, 115), (61, 146, 206), (195, 75, 154)]
CEMPASUCHIL_ORANGE = (255, 140, 0)
CEMPASUCHIL_YELLOW = (255, 215, 0)
NIGHT_BLUE = (25, 25, 112)
CANDLE_WHITE = (255, 250, 240)
WOOD_BROWN = (139, 69, 19)
NARANJA = (255, 165, 0)

class GradientGenerator:
    
    def __init__(self):
        self.gradient_type = "linear"
        self.colors = [(255, 0, 0), (0, 0, 255)]

    def linear_gradient(self, surface, start_pos, end_pos, colors):
        """Generar degradado lineal entre dos puntos"""
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        
        target_rect = pygame.Rect(min(start_x, end_x), min(start_y, end_y), abs(start_x - end_x), abs(start_y - end_y))
        if target_rect.width == 0: target_rect.width = surface.get_width()
        if target_rect.height == 0: target_rect.height = surface.get_height()
            
        color_rect = pygame.Surface((2, 2))
        for i, c in enumerate(colors):
            pygame.draw.line(color_rect, c, (i, 0), (i, 1))

        gradient = pygame.transform.smoothscale(color_rect, (target_rect.width, target_rect.height))
        surface.blit(gradient, target_rect)

    def radial_gradient(self, surface, center, radius, colors):
        """Generar degradado radial desde un punto central"""
        for r in range(radius, 0, -1):
            t = 1 - (r / radius)
            segment = t * (len(colors) - 1)
            color_index = int(segment)
            local_t = segment - color_index
            
            if color_index >= len(colors) - 1:
                color_r, color_g, color_b = colors[-1]
            else:
                color_r = int(colors[color_index][0] * (1 - local_t) + colors[color_index + 1][0] * local_t)
                color_g = int(colors[color_index][1] * (1 - local_t) + colors[color_index + 1][1] * local_t)
                color_b = int(colors[color_index][2] * (1 - local_t) + colors[color_index + 1][2] * local_t)
            
            pygame.draw.circle(surface, (color_r, color_g, color_b), center, r)

# --- NUEVA FUNCIÓN DE TEXTURA ---
def create_serape_texture(width, height, colors):
    """Crear una textura de serape (rayas horizontales)"""
    texture = pygame.Surface((width, height))
    stripe_height = height // 10  # Grosor de cada franja
    
    for i in range(12):
        color = colors[i % len(colors)]
        y_pos = i * stripe_height
        pygame.draw.rect(texture, color, (0, y_pos, width, stripe_height))
    return texture

# --- NUEVAS FUNCIONES DE DIBUJO PARA EL ALTAR ---
def draw_altar_tiers(surface, texture_tier1, texture_tier2):
    """Dibuja los niveles del altar con su textura"""
    # Nivel inferior
    tier1_rect = pygame.Rect(100, 450, 800, 250)
    surface.blit(texture_tier1, tier1_rect)
    pygame.draw.rect(surface, BLACK, tier1_rect, 3)

    # Nivel superior
    tier2_rect = pygame.Rect(250, 300, 500, 150)
    surface.blit(texture_tier2, tier2_rect)
    pygame.draw.rect(surface, BLACK, tier2_rect, 3)

def draw_candle(surface, position, gradient_gen):
    """Dibuja una veladora con llama"""
    x, y = position
    # Cuerpo de la veladora
    pygame.draw.rect(surface, CANDLE_WHITE, (x, y, 20, 50))
    pygame.draw.rect(surface, BLACK, (x, y, 20, 50), 1)
    
    # Llama con degradado radial
    flame_center = (x + 10, y - 5)
    gradient_gen.radial_gradient(surface, flame_center, 10, [WHITE, CEMPASUCHIL_YELLOW, CEMPASUCHIL_ORANGE])

def draw_cempasuchil(surface, position, radius, gradient_gen):
    """Dibuja una flor de cempasúchil con degradado radial"""
    gradient_gen.radial_gradient(surface, position, radius, [CEMPASUCHIL_YELLOW, CEMPASUCHIL_ORANGE])
    pygame.draw.circle(surface, WOOD_BROWN, position, radius // 3) # Centro oscuro

def draw_sugar_skull(surface, position):
    """Dibuja una calaverita de azúcar simplificada"""
    x, y = position
    # Cráneo
    pygame.draw.circle(surface, WHITE, (x, y), 25)
    pygame.draw.rect(surface, WHITE, (x - 15, y + 15, 30, 15))
    pygame.draw.circle(surface, BLACK, (x, y + 20), 18, 2) # Mandíbula
    
    # Ojos y nariz
    pygame.draw.circle(surface, BLACK, (x - 10, y - 5), 5)
    pygame.draw.circle(surface, BLACK, (x + 10, y - 5), 5)
    # Nariz (triángulo)
    pygame.draw.polygon(surface, BLACK, [(x, y+5), (x-4, y+12), (x+4, y+12)])

def draw_photo_frame(surface, position):
    """Dibuja un portarretrato"""
    x, y = position
    # Marco exterior
    pygame.draw.rect(surface, WOOD_BROWN, (x, y, 80, 100))
    # "Foto" interior (en escala de grises)
    pygame.draw.rect(surface, (50, 50, 50), (x + 10, y + 10, 60, 60))
    pygame.draw.rect(surface, BLACK, (x, y, 80, 100), 2)

def draw_papel_picado(surface):
    """Dibuja una tira de papel picado en la parte superior"""
    pygame.draw.line(surface, BLACK, (0, 40), (WIDTH, 40), 2)
    for x in range(5, WIDTH, 120):
        color = random.choice(BLACK)
        pygame.draw.rect(surface, color, (x, 40, 100, 60))
        # Pequeños cortes simulados
        pygame.draw.circle(surface, NIGHT_BLUE, (x + 30, 70), 8)
        pygame.draw.circle(surface, NIGHT_BLUE, (x + 70, 70), 8)
    
    """
    for x in range(50, WIDTH, 120):
        color = random.choice(PAPEL_PICADO_COLORS)
        pygame.draw.rect(surface, color, (x, 40, 100, 60))
        # Pequeños cortes simulados
        pygame.draw.circle(surface, NIGHT_BLUE, (x + 30, 70), 8)
        pygame.draw.circle(surface, NIGHT_BLUE, (x + 70, 70), 8) """

def main():
    gradient_gen = GradientGenerator()
    running = True
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    # --- CREAR RECURSOS UNA VEZ ---
    # Textura para los niveles del altar
    serape_colors = [(191, 11, 40), (242, 118, 40), (242, 196, 40), (40, 153, 62), (40, 114, 180)]
    serape_texture_tier1 = create_serape_texture(800, 250, serape_colors)
    serape_texture_tier2 = create_serape_texture(500, 150, serape_colors)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # --- DIBUJAR LA ESCENA ---
        
        # 1. Fondo con degradado lineal (noche)
        gradient_gen.linear_gradient(screen, (0, 0), (0, HEIGHT), [NIGHT_BLUE, BLACK])
        
        # 2. Papel picado
        draw_papel_picado(screen)
        
        # 3. Dibujar los niveles del altar
        draw_altar_tiers(screen, serape_texture_tier1, serape_texture_tier2)

        # 4. Dibujar las ofrendas
        # Portarretrato en el centro del nivel superior
        draw_photo_frame(screen, (460, 210))
        
        # Veladoras
        draw_candle(screen, (300, 250), gradient_gen)
        draw_candle(screen, (680, 250), gradient_gen)
        draw_candle(screen, (150, 400), gradient_gen)
        draw_candle(screen, (830, 400), gradient_gen)
        
        # Calaveritas de azúcar
        draw_sugar_skull(screen, (400, 410))
        draw_sugar_skull(screen, (600, 410))
        
        # Flores de Cempasúchil
        draw_cempasuchil(screen, (220, 430), 25, gradient_gen)
        draw_cempasuchil(screen, (780, 430), 25, gradient_gen)
        draw_cempasuchil(screen, (280, 280), 20, gradient_gen)
        draw_cempasuchil(screen, (720, 280), 20, gradient_gen)
        draw_cempasuchil(screen, (500, 430), 30, gradient_gen)

        # 5. Título
        title_text = font.render("Altar de Día de Muertos", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 10))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
