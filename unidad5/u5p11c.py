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
GRIS_CADAVERICO = (180, 180, 190) # Piel pálida
NEGRO = (0, 0, 0)
MARRON_OSCURO_ABRIGO = (30, 20, 10) # Abrigo muy oscuro, casi negro
ROJO_OSCURO_HERIDA = (100, 0, 0) # Para simular heridas
GRIS_CLARO = (200, 200, 200) # Para el efecto de nieve/desgaste en el abrigo
NEGRO_ZAPATO = (10, 10, 10) # Color para los zapatos
AZUL_HIELO = (150, 220, 255) # Color para las plataformas de hielo
AZUL_SUELO_HIELO = (100, 180, 255) # Color para el suelo de hielo (NUEVO)

# --- Propiedades del Personaje ---
x, y = 100, 400
ancho_personaje = 50
alto_personaje = 80 + 15 + 5 # Cuerpo (80) + Pierna (15) + Zapato (5) = 100
velocidad = 5
salto = False
vel_y = 0
gravedad = 1
suelo_base = 400 # Altura original del suelo (donde aterriza la parte superior del personaje)

# --- Plataformas de Hielo (AJUSTADAS) ---
# [x, y, ancho, alto]
plataformas = [
    pygame.Rect(150, 420, 100, 15), # Bajada para fácil acceso
    pygame.Rect(400, 450, 150, 15), # Plataforma media
    pygame.Rect(600, 430, 80, 15), # Bajada para fácil acceso
]

# --- Animación ---
frame_counter = 0
animation_speed = 5 # Cambia la pose cada 5 frames
current_frame = 0   # 0 (reposo/paso derecho) o 1 (paso izquierdo)
is_moving = False

# --- Funciones de Dibujo ---

# Función para dibujar el personaje (simplificada)
def dibujar_personaje(pantalla, x, y, current_frame):
    # Definiciones de dibujo existentes (colores y tamaños)
    brazo_largo = 40
    grosor_brazo = 10
    alto_pierna = 15
    ancho_pierna = 10

    # 1. BRAZOS
    sh_x_l, sh_y_l = x + 5, y + 5
    sh_x_r, sh_y_r = x + 45, y + 5
    
    # BRAZO IZQUIERDO
    if current_frame == 0:
        e_x_l, e_y_l = sh_x_l - 10, sh_y_l + brazo_largo * 0.9 
    else:
        e_x_l, e_y_l = sh_x_l + 10, sh_y_l + brazo_largo * 0.9
    pygame.draw.line(pantalla, MARRON_OSCURO_ABRIGO, (sh_x_l, sh_y_l), (e_x_l, e_y_l), grosor_brazo)
    pygame.draw.circle(pantalla, GRIS_CADAVERICO, (e_x_l, e_y_l), grosor_brazo // 2 + 2)

    # BRAZO DERECHO
    if current_frame == 0:
        e_x_r, e_y_r = sh_x_r + 10, sh_y_r + brazo_largo * 0.9 
    else:
        e_x_r, e_y_r = sh_x_r - 10, sh_y_r + brazo_largo * 0.9
    pygame.draw.line(pantalla, MARRON_OSCURO_ABRIGO, (sh_x_r, sh_y_r), (e_x_r, e_y_r), grosor_brazo)
    pygame.draw.circle(pantalla, GRIS_CADAVERICO, (e_x_r, e_y_r), grosor_brazo // 2 + 2)
    
    # 2. CUERPO Y CABEZA 
    pygame.draw.rect(pantalla, MARRON_OSCURO_ABRIGO, (x, y, 50, 80))
    pygame.draw.polygon(pantalla, MARRON_OSCURO_ABRIGO, [(x - 10, y - 50), (x + 60, y - 50), (x + 55, y - 20), (x - 5, y - 20)])
    pygame.draw.line(pantalla, GRIS_CLARO, (x + 5, y + 5), (x + 15, y + 5), 2)
    pygame.draw.line(pantalla, GRIS_CLARO, (x + 35, y + 10), (x + 45, y + 10), 2)
    pygame.draw.line(pantalla, GRIS_CLARO, (x + 0, y + 60), (x + 10, y + 65), 2)
    pygame.draw.line(pantalla, GRIS_CLARO, (x + 50, y + 60), (x + 40, y + 65), 2)
    pygame.draw.line(pantalla, GRIS_CLARO, (x + 10, y - 45), (x + 20, y - 40), 2)
    pygame.draw.line(pantalla, GRIS_CLARO, (x + 40, y - 45), (x + 30, y - 40), 2)

    pygame.draw.circle(pantalla, GRIS_CADAVERICO, (x + 25, y - 20), 20)
    pygame.draw.circle(pantalla, NEGRO, (x + 19, y - 28), 2)
    pygame.draw.circle(pantalla, NEGRO, (x + 31, y - 28), 2)
    pygame.draw.line(pantalla, NEGRO, (x + 18, y - 15), (x + 32, y - 15), 1)
    pygame.draw.line(pantalla, NEGRO, (x + 15, y - 35), (x + 35, y - 25), 2)
    pygame.draw.line(pantalla, NEGRO, (x + 10, y - 20), (x + 25, y - 10), 2)
    pygame.draw.line(pantalla, ROJO_OSCURO_HERIDA, (x + 12, y - 18), (x + 23, y - 12), 1)
    pygame.draw.line(pantalla, NEGRO, (x + 25, y - 5), (x + 30, y + 5), 2)

    # 3. PIERNAS Y PIES
    base_y = y + 80
    hip_x_l, hip_x_r = x + 18, x + 32
    
    if current_frame == 0:
        offset_x_l = 0
        offset_x_r = 5
    else:
        offset_x_l = 5
        offset_x_r = 0
        
    pygame.draw.rect(pantalla, MARRON_OSCURO_ABRIGO, (hip_x_l - ancho_pierna/2, base_y, ancho_pierna, alto_pierna))
    pygame.draw.rect(pantalla, NEGRO_ZAPATO, (hip_x_l - 10 + offset_x_l, base_y + alto_pierna, ancho_pierna * 1.5, 5))
    
    pygame.draw.rect(pantalla, MARRON_OSCURO_ABRIGO, (hip_x_r - ancho_pierna/2, base_y, ancho_pierna, alto_pierna))
    pygame.draw.rect(pantalla, NEGRO_ZAPATO, (hip_x_r - 10 + offset_x_r, base_y + alto_pierna, ancho_pierna * 1.5, 5))

# --- Bucle principal ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # --- Movimiento con teclas ---
    teclas = pygame.key.get_pressed()
    is_moving = False

    # Guardar la posición antigua para la colisión
    old_x = x
    
    # Movimiento horizontal
    if teclas[pygame.K_LEFT]:
        x -= velocidad
        is_moving = True
    if teclas[pygame.K_RIGHT]:
        x += velocidad
        is_moving = True
        
    # Colisión con límites de pantalla 
    if x < 0:
        x = 0
    if x > ANCHO - ancho_personaje:
        x = ANCHO - ancho_personaje

    # Salto
    if teclas[pygame.K_UP] and not salto:
        salto = True
        vel_y = -15  #impulso de salto

    # --- Física del salto y gravedad ---
    if salto:
        y += vel_y
        vel_y += gravedad
    
    # --- Colisión con plataformas ---
    
    # 1. Crear el rectángulo de colisión del personaje (incluyendo piernas)
    # Se usa y + 20 para hacer el "hitbox" un poco más pequeño que el cuerpo visual
    rect_personaje = pygame.Rect(x, y + 20, ancho_personaje, alto_personaje - 20)
    
    # 2. Inicializar la superficie de aterrizaje más baja (el suelo principal)
    # Si no hay colisión con plataforma, debe caer al suelo base
    y_aterrizaje = suelo_base
    
    colision_plataforma = False
    
    for plataforma in plataformas:
        # 3. Detectar colisión con plataformas
        if rect_personaje.colliderect(plataforma):
            # 4. Comprobar si está cayendo y la colisión es por encima (aterrizaje)
            # El personaje debe estar tocando la parte superior de la plataforma
            if vel_y >= 0 and rect_personaje.bottom <= plataforma.top + 10: 
                y_aterrizaje = plataforma.top - (alto_personaje - 20)
                colision_plataforma = True
                break
            
    # 5. Aplicar aterrizaje
    if colision_plataforma:
        y = y_aterrizaje - 20 # Ajustar la posición y del personaje (restamos 20 porque el hitbox empieza en y+20)
        salto = False
        vel_y = 0
    elif y >= suelo_base: # Si no hay colisión con plataforma y ha pasado el suelo base
        y = suelo_base
        salto = False
        vel_y = 0
    else:
        # Si no toca ninguna plataforma ni el suelo, o está subiendo, el salto permanece activo
        salto = True


    # --- Lógica de Animación ---
    if is_moving and not salto:
        frame_counter += 1
        if frame_counter >= animation_speed:
            current_frame = 1 - current_frame
            frame_counter = 0
    else:
        current_frame = 0
        frame_counter = 0


    # --- Dibujar ---
    pantalla.fill(BLANCO)
    
    # NUEVO SUELO DE HIELO (Rectángulo azul que cubre la parte inferior de la pantalla)
    y_suelo_inicio = suelo_base + alto_personaje # Donde los pies del personaje tocan
    pygame.draw.rect(pantalla, AZUL_SUELO_HIELO, (0, y_suelo_inicio, ANCHO, ALTO - y_suelo_inicio))
    # Dibuja la parte superior del suelo como una línea blanca para simular el borde del hielo
    pygame.draw.line(pantalla, BLANCO, (0, y_suelo_inicio), (ANCHO, y_suelo_inicio), 3)

    # Dibujar plataformas de hielo 
    for plataforma in plataformas:
        pygame.draw.rect(pantalla, AZUL_HIELO, plataforma)
        # Efecto de grietas/hielo 
        pygame.draw.line(pantalla, BLANCO, (plataforma.left, plataforma.top + 5), (plataforma.left + 5, plataforma.top), 1)
        pygame.draw.line(pantalla, BLANCO, (plataforma.right, plataforma.top + 5), (plataforma.right - 10, plataforma.top), 1)

    # Dibujar el personaje (usando la función)
    dibujar_personaje(pantalla, x, y, current_frame)
    
    # --- Actualizar pantalla ---
    pygame.display.flip()
    clock.tick(30)
