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

# --- Personaje ---
x, y = 100, 400
velocidad = 5
salto = False
vel_y = 0
gravedad = 1

# --- Animación (NUEVO) ---
frame_counter = 0
animation_speed = 5 # Cambia la pose cada 5 frames
current_frame = 0   # 0 (reposo/paso derecho) o 1 (paso izquierdo)
is_moving = False

# --- Bucle principal ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # --- Movimiento con teclas ---
    teclas = pygame.key.get_pressed()
    is_moving = False # Reiniciar estado de movimiento

    if teclas[pygame.K_LEFT]:
        x -= velocidad
        is_moving = True
    if teclas[pygame.K_RIGHT]:
        x += velocidad
        is_moving = True
    if teclas[pygame.K_UP] and not salto:
        salto = True
        vel_y = -15  # impulso de salto

    # --- Física del salto ---
    if salto:
        y += vel_y
        vel_y += gravedad
        if y >= 400:  #suelo
            y = 400
            salto = False

    # --- Lógica de Animación (NUEVO) ---
    if is_moving and not salto:
        frame_counter += 1
        if frame_counter >= animation_speed:
            current_frame = 1 - current_frame # Alternar entre 0 y 1
            frame_counter = 0
    else:
        # Volver al estado "quieto" (Frame 0) cuando no se mueve o está saltando
        current_frame = 0
        frame_counter = 0


    # --- Dibujar ---
    pantalla.fill(BLANCO)
    
    # ---------------------------
    # 1. BRAZOS 
    brazo_largo = 40
    grosor_brazo = 10
    
    # Posición base de los hombros (parte superior del abrigo)
    sh_x_l, sh_y_l = x + 5, y + 5
    sh_x_r, sh_y_r = x + 45, y + 5
    
    # Brazos: Se mueven de forma opuesta a las piernas (paso derecho = brazo izquierdo adelante)
    
    # BRAZO IZQUIERDO
    if current_frame == 0: # Reposo o paso derecho (Brazo Izquierdo hacia atrás)
        e_x_l, e_y_l = sh_x_l - 10, sh_y_l + brazo_largo * 0.9 
    else: # current_frame == 1 (Paso izquierdo, Brazo Izquierdo hacia adelante)
        e_x_l, e_y_l = sh_x_l + 10, sh_y_l + brazo_largo * 0.9

    pygame.draw.line(pantalla, MARRON_OSCURO_ABRIGO, (sh_x_l, sh_y_l), (e_x_l, e_y_l), grosor_brazo)
    # Mano izquierda
    pygame.draw.circle(pantalla, GRIS_CADAVERICO, (e_x_l, e_y_l), grosor_brazo // 2 + 2)


    # BRAZO DERECHO
    if current_frame == 0: # Reposo o paso derecho (Brazo Derecho hacia adelante)
        e_x_r, e_y_r = sh_x_r + 10, sh_y_r + brazo_largo * 0.9 
    else: # current_frame == 1 (Paso izquierdo, Brazo Derecho hacia atrás)
        e_x_r, e_y_r = sh_x_r - 10, sh_y_r + brazo_largo * 0.9

    pygame.draw.line(pantalla, MARRON_OSCURO_ABRIGO, (sh_x_r, sh_y_r), (e_x_r, e_y_r), grosor_brazo)
    # Mano derecha
    pygame.draw.circle(pantalla, GRIS_CADAVERICO, (e_x_r, e_y_r), grosor_brazo // 2 + 2)
    
    
    # ---------------------------
    # 2. CUERPO Y CABEZA 
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


    # ---------------------------
    # 3. PIERNAS Y PIES
    alto_pierna = 15
    ancho_pierna = 10
    
    # Las piernas salen de la parte inferior del abrigo (y + 80)
    base_y = y + 80
    
    # Posición de las piernas (separadas por la cadera)
    hip_x_l, hip_x_r = x + 18, x + 32
    
    # PIERNA IZQUIERDA
    if current_frame == 0:
        # Reposo o paso derecho (Pie izquierdo se ve más vertical/atrás)
        offset_x_l = 0
    else: # current_frame == 1
        # Paso izquierdo (Pie izquierdo se ve más adelante)
        offset_x_l = 5
        
    pygame.draw.rect(pantalla, MARRON_OSCURO_ABRIGO, (hip_x_l - ancho_pierna/2, base_y, ancho_pierna, alto_pierna))
    # Pie/Zapato izquierdo
    pygame.draw.rect(pantalla, NEGRO_ZAPATO, (hip_x_l - 10 + offset_x_l, base_y + alto_pierna, ancho_pierna * 1.5, 5))


    # PIERNA DERECHA
    if current_frame == 0:
        # Reposo o paso derecho (Pie derecho se ve más adelante)
        offset_x_r = 5
    else: # current_frame == 1
        # Paso izquierdo (Pie derecho se ve más vertical/atrás)
        offset_x_r = 0
        
    pygame.draw.rect(pantalla, MARRON_OSCURO_ABRIGO, (hip_x_r - ancho_pierna/2, base_y, ancho_pierna, alto_pierna))
    # Pie/Zapato derecho
    pygame.draw.rect(pantalla, NEGRO_ZAPATO, (hip_x_r - 10 + offset_x_r, base_y + alto_pierna, ancho_pierna * 1.5, 5))

    
    # --- Actualizar pantalla
    pygame.display.flip()
    clock.tick(30)
