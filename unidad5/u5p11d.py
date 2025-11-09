import pygame
import sys
import random
import time

# --- Inicialización ---
pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Frankenstein 2D: Supervivencia de Coyote")
clock = pygame.time.Clock()
FPS = 30

# --- Colores ---
BLANCO = (255, 255, 255)
GRIS_CADAVERICO = (180, 180, 190)
NEGRO = (0, 0, 0)
MARRON_OSCURO_ABRIGO = (30, 20, 10)
ROJO_OSCURO_HERIDA = (100, 0, 0)
GRIS_CLARO = (200, 200, 200)
NEGRO_ZAPATO = (10, 10, 10)
AZUL_HIELO = (150, 220, 255)
AZUL_SUELO_HIELO = (100, 180, 255)
ROJO_VIDA = (200, 50, 50)
VERDE_VICTORIA = (50, 200, 50)
GRIS_COYOTE = (80, 70, 60) # Un gris más marrón para el coyote
MARRON_COYOTE = (120, 90, 70) # Un poco de marrón para las patas/orejas

# --- Tipografía ---
fuente_pequena = pygame.font.Font(None, 24)
fuente_grande = pygame.font.Font(None, 74)

# --- Propiedades del Personaje ---
x, y = 100, 400
ancho_personaje = 50
alto_personaje = 100
velocidad = 5
salto = False
vel_y = 0
gravedad = 1
suelo_base = 400

# --- Variables del Juego ---
VIDA_MAXIMA = 100
vida_frankenstein = VIDA_MAXIMA
TIEMPO_SUPERVIVENCIA_SEGS = 60
tiempo_inicio = time.time()
juego_terminado = False
victoria = False

# --- Plataformas de Hielo ---
plataformas = [
    pygame.Rect(150, 420, 100, 15),
    pygame.Rect(400, 450, 150, 15),
    pygame.Rect(600, 430, 80, 15),
]

# --- Animación de Frankenstein ---
frame_counter = 0
animation_speed = 5
current_frame = 0
is_moving = False

# --- Clase Coyote (Enemigo Mejorado) ---
class Coyote:
    def __init__(self, x, y, velocidad):
        self.ancho = 60 # Más grande
        self.alto = 35 # Más alto
        self.x = x
        self.y = y - self.alto
        self.velocidad = velocidad
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        self.damage_cooldown = 0
        self.color_cuerpo = GRIS_COYOTE
        self.color_detalles = MARRON_COYOTE
        
        self.salto = False
        self.vel_salto_y = 0
        self.fuerza_salto = -10 # Menos que Frankenstein, pero suficiente para plataformas

    def mover_hacia_jugador(self, jugador_x, plataformas):
        # Aplicar gravedad primero para el salto
        if self.salto:
            self.y += self.vel_salto_y
            self.vel_salto_y += gravedad
            self.rect.y = self.y
        
        # Colisión y aterrizaje del coyote
        en_suelo_actual = False
        # Para el coyote, el hitbox inferior es importante para el suelo
        coyote_pie_rect = pygame.Rect(self.x, self.y + self.alto - 5, self.ancho, 5) 

        # Verificar plataformas
        for plat in plataformas:
            if coyote_pie_rect.colliderect(plat) and self.vel_salto_y >= 0:
                self.y = plat.top - self.alto
                self.rect.y = self.y
                self.salto = False
                self.vel_salto_y = 0
                en_suelo_actual = True
                break

        # Verificar suelo principal
        y_suelo_inicio = suelo_base + alto_personaje
        if coyote_pie_rect.bottom >= y_suelo_inicio and self.vel_salto_y >= 0:
            self.y = y_suelo_inicio - self.alto
            self.rect.y = self.y
            self.salto = False
            self.vel_salto_y = 0
            en_suelo_actual = True
            
        if not en_suelo_actual and not self.salto: # Si no está en el suelo, está en el aire (cae)
            self.salto = True 
            self.vel_salto_y = 1 # Pequeña velocidad inicial para empezar a caer
        
        # Lógica de salto para el coyote
        if en_suelo_actual and random.randint(0, 100) < 2 and abs(self.x - jugador_x) < 200: # 2% de probabilidad de saltar si el jugador está cerca
            self.salto = True
            self.vel_salto_y = self.fuerza_salto

        # Movimiento horizontal (solo si no está en medio de un salto muy alto, para evitar movimientos erráticos)
        if not self.salto or self.vel_salto_y > -5: # Permite moverse un poco durante la caída o un salto bajo
            if self.x < jugador_x:
                self.x += abs(self.velocidad)
            elif self.x > jugador_x:
                self.x -= abs(self.velocidad)
            self.rect.x = self.x

    def dibujar(self, pantalla):
        # Cuerpo principal (óvalo más robusto)
        pygame.draw.ellipse(pantalla, self.color_cuerpo, (self.x, self.y + 5, self.ancho, self.alto - 5))

        # Cabeza (forma más triangular)
        if self.velocidad > 0: # Mirando a la derecha
            # Hocico
            pygame.draw.polygon(pantalla, self.color_cuerpo, [
                (self.x + self.ancho - 5, self.y + self.alto // 2),
                (self.x + self.ancho + 15, self.y + self.alto // 3),
                (self.x + self.ancho + 15, self.y + self.alto * 2 // 3)
            ])
            # Oreja 1
            pygame.draw.polygon(pantalla, self.color_detalles, [
                (self.x + self.ancho - 10, self.y + 5),
                (self.x + self.ancho - 2, self.y - 5),
                (self.x + self.ancho + 5, self.y + 10)
            ])
            # Oreja 2 (más atrás)
            pygame.draw.polygon(pantalla, self.color_detalles, [
                (self.x + self.ancho - 20, self.y + 10),
                (self.x + self.ancho - 12, self.y + 0),
                (self.x + self.ancho - 5, self.y + 15)
            ])
            # Ojo
            pygame.draw.circle(pantalla, NEGRO, (int(self.x + self.ancho + 5), int(self.y + self.alto // 2.5)), 2)

        else: # Mirando a la izquierda
            # Hocico
            pygame.draw.polygon(pantalla, self.color_cuerpo, [
                (self.x + 5, self.y + self.alto // 2),
                (self.x - 15, self.y + self.alto // 3),
                (self.x - 15, self.y + self.alto * 2 // 3)
            ])
            # Oreja 1
            pygame.draw.polygon(pantalla, self.color_detalles, [
                (self.x + 10, self.y + 5),
                (self.x + 2, self.y - 5),
                (self.x - 5, self.y + 10)
            ])
            # Oreja 2 (más atrás)
            pygame.draw.polygon(pantalla, self.color_detalles, [
                (self.x + 20, self.y + 10),
                (self.x + 12, self.y + 0),
                (self.x + 5, self.y + 15)
            ])
            # Ojo
            pygame.draw.circle(pantalla, NEGRO, (int(self.x - 5), int(self.y + self.alto // 2.5)), 2)

        # Patas (rectángulos simples)
        # Pata delantera
        pygame.draw.rect(pantalla, self.color_detalles, (self.x + 5, self.y + self.alto - 10, 8, 10))
        # Pata trasera
        pygame.draw.rect(pantalla, self.color_detalles, (self.x + self.ancho - 15, self.y + self.alto - 10, 8, 10))


# --- Funciones de Dibujo ---

def dibujar_personaje(pantalla, x, y, current_frame):
    # (El código de dibujo de Frankenstein se mantiene igual)
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
    # Abrigo (hombros)
    pygame.draw.polygon(pantalla, MARRON_OSCURO_ABRIGO, [(x - 10, y - 50), (x + 60, y - 50), (x + 55, y - 20), (x - 5, y - 20)])
    # Desgaste
    pygame.draw.line(pantalla, GRIS_CLARO, (x + 5, y + 5), (x + 15, y + 5), 2)
    pygame.draw.line(pantalla, GRIS_CLARO, (x + 35, y + 10), (x + 45, y + 10), 2)
    pygame.draw.line(pantalla, GRIS_CLARO, (x + 0, y + 60), (x + 10, y + 65), 2)
    pygame.draw.line(pantalla, GRIS_CLARO, (x + 50, y + 60), (x + 40, y + 65), 2)
    pygame.draw.line(pantalla, GRIS_CLARO, (x + 10, y - 45), (x + 20, y - 40), 2)
    pygame.draw.line(pantalla, GRIS_CLARO, (x + 40, y - 45), (x + 30, y - 40), 2)

    # Cabeza
    pygame.draw.circle(pantalla, GRIS_CADAVERICO, (x + 25, y - 20), 20)
    pygame.draw.circle(pantalla, NEGRO, (x + 19, y - 28), 2) # Ojo izquierdo
    pygame.draw.circle(pantalla, NEGRO, (x + 31, y - 28), 2) # Ojo derecho
    pygame.draw.line(pantalla, NEGRO, (x + 18, y - 15), (x + 32, y - 15), 1) # Boca
    pygame.draw.line(pantalla, NEGRO, (x + 15, y - 35), (x + 35, y - 25), 2) # Pelo
    pygame.draw.line(pantalla, NEGRO, (x + 10, y - 20), (x + 25, y - 10), 2) # Cicatriz
    pygame.draw.line(pantalla, ROJO_OSCURO_HERIDA, (x + 12, y - 18), (x + 23, y - 12), 1) # Herida
    pygame.draw.line(pantalla, NEGRO, (x + 25, y - 5), (x + 30, y + 5), 2) # Costura en el cuello

    # 3. PIERNAS Y PIES
    base_y = y + 80
    hip_x_l, hip_x_r = x + 18, x + 32
    
    # Lógica de animación de piernas
    if current_frame == 0:
        offset_x_l = 0
        offset_x_r = 5
    else:
        offset_x_l = 5
        offset_x_r = 0
        
    # Pierna Izquierda
    pygame.draw.rect(pantalla, MARRON_OSCURO_ABRIGO, (hip_x_l - ancho_pierna/2, base_y, ancho_pierna, alto_pierna))
    pygame.draw.rect(pantalla, NEGRO_ZAPATO, (hip_x_l - 10 + offset_x_l, base_y + alto_pierna, ancho_pierna * 1.5, 5))
    
    # Pierna Derecha
    pygame.draw.rect(pantalla, MARRON_OSCURO_ABRIGO, (hip_x_r - ancho_pierna/2, base_y, ancho_pierna, alto_pierna))
    pygame.draw.rect(pantalla, NEGRO_ZAPATO, (hip_x_r - 10 + offset_x_r, base_y + alto_pierna, ancho_pierna * 1.5, 5))

def dibujar_barra_vida(pantalla, vida_actual, vida_maxima):
    ancho_barra = 200
    alto_barra = 20
    x_barra, y_barra = 10, 10
    
    porcentaje_vida = vida_actual / vida_maxima
    ancho_relleno = int(ancho_barra * porcentaje_vida)
    
    pygame.draw.rect(pantalla, NEGRO, (x_barra, y_barra, ancho_barra, alto_barra), 2)
    pygame.draw.rect(pantalla, ROJO_VIDA, (x_barra, y_barra, ancho_relleno, alto_barra))
    
    texto_vida = fuente_pequena.render(f"VIDA: {vida_actual}/{vida_maxima}", True, NEGRO)
    pantalla.blit(texto_vida, (x_barra + 5, y_barra + 2))

def dibujar_temporizador(pantalla, tiempo_restante):
    texto_tiempo = fuente_pequena.render(f"Tiempo: {max(0, int(tiempo_restante))}s", True, NEGRO)
    pantalla.blit(texto_tiempo, (ANCHO - texto_tiempo.get_width() - 10, 10))

# --- Gestión de Coyotes ---
coyotes = []
intervalo_aparicion_frames = 90
contador_aparicion = 0
VELOCIDAD_COYOTE = 3 # Un poco más rápido
DAÑO_COYOTE = 15 # Más daño

# --- Bucle principal ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if juego_terminado and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            # Resetear variables
            x, y = 100, 400
            vida_frankenstein = VIDA_MAXIMA
            tiempo_inicio = time.time()
            juego_terminado = False
            victoria = False
            coyotes = [] # Limpiar la lista de coyotes
            vel_y = 0
            salto = False

    if not juego_terminado:
        # --- Cálculo de Tiempo ---
        tiempo_transcurrido = time.time() - tiempo_inicio
        tiempo_restante = TIEMPO_SUPERVIVENCIA_SEGS - tiempo_transcurrido

        if tiempo_restante <= 0:
            juego_terminado = True
            victoria = True
        
        # --- Movimiento con teclas ---
        teclas = pygame.key.get_pressed()
        is_moving = False
        
        if teclas[pygame.K_LEFT]:
            x -= velocidad
            is_moving = True
        if teclas[pygame.K_RIGHT]:
            x += velocidad
            is_moving = True
            
        if x < 0:
            x = 0
        if x > ANCHO - ancho_personaje:
            x = ANCHO - ancho_personaje

        if teclas[pygame.K_UP] and not salto:
            salto = True
            vel_y = -15 

        # --- Física del salto y gravedad ---
        if salto:
            y += vel_y
            vel_y += gravedad
        
        # --- Colisión con plataformas (Frankenstein) ---
        rect_personaje = pygame.Rect(x, y + 20, ancho_personaje, alto_personaje - 20)
        y_aterrizaje = suelo_base
        colision_plataforma = False
        
        for plataforma in plataformas:
            if rect_personaje.colliderect(plataforma):
                if vel_y >= 0 and rect_personaje.bottom <= plataforma.top + 10: 
                    y_aterrizaje = plataforma.top - (alto_personaje - 20)
                    colision_plataforma = True
                    break
                
        if colision_plataforma:
            y = y_aterrizaje - 20 
            salto = False
            vel_y = 0
        elif y >= suelo_base:
            y = suelo_base
            salto = False
            vel_y = 0
        else:
            salto = True


        # --- Lógica de Animación (Frankenstein) ---
        if is_moving and not salto:
            frame_counter += 1
            if frame_counter >= animation_speed:
                current_frame = 1 - current_frame
                frame_counter = 0
        else:
            current_frame = 0
            frame_counter = 0
            
        # --- Lógica de Coyotes ---
        
        # 1. Aparición
        contador_aparicion += 1
        if contador_aparicion >= intervalo_aparicion_frames and tiempo_restante > 0:
            lado_aparicion = random.choice([0, ANCHO])
            # Ajustar la y_spawn para que el coyote aparezca sobre el suelo/plataforma
            y_spawn = suelo_base + alto_personaje - Coyote(0, 0, 0).alto
            
            if lado_aparicion == 0:
                vel_coyote = VELOCIDAD_COYOTE
            else:
                vel_coyote = -VELOCIDAD_COYOTE
                
            nuevo_coyote = Coyote(lado_aparicion, y_spawn, vel_coyote)
            coyotes.append(nuevo_coyote)
            contador_aparicion = 0
            
        # 2. Movimiento y Colisión
        coyotes_a_eliminar = []
        for coyote in coyotes:
            coyote.mover_hacia_jugador(x + ancho_personaje / 2, plataformas) 
            
            if rect_personaje.colliderect(coyote.rect):
                if coyote.damage_cooldown == 0:
                    vida_frankenstein -= DAÑO_COYOTE
                    coyote.damage_cooldown = FPS * 1 
                
                coyote.velocidad *= -1 
            
            if coyote.damage_cooldown > 0:
                coyote.damage_cooldown -= 1

            if coyote.x < -100 or coyote.x > ANCHO + 100:
                if abs(coyote.x - (x + ancho_personaje / 2)) > ANCHO * 0.7:
                    coyotes_a_eliminar.append(coyote)

        for coyote_eliminar in coyotes_a_eliminar:
            if coyote_eliminar in coyotes:
                coyotes.remove(coyote_eliminar)

        # 3. Comprobar Game Over
        if vida_frankenstein <= 0:
            juego_terminado = True
            victoria = False

    # --- Dibujar ---
    pantalla.fill(BLANCO)
    
    # Suelo de Hielo
    y_suelo_inicio = suelo_base + alto_personaje
    pygame.draw.rect(pantalla, AZUL_SUELO_HIELO, (0, y_suelo_inicio, ANCHO, ALTO - y_suelo_inicio))
    pygame.draw.line(pantalla, BLANCO, (0, y_suelo_inicio), (ANCHO, y_suelo_inicio), 3)

    # Plataformas de hielo 
    for plataforma in plataformas:
        pygame.draw.rect(pantalla, AZUL_HIELO, plataforma)
        pygame.draw.line(pantalla, BLANCO, (plataforma.left, plataforma.top + 5), (plataforma.left + 5, plataforma.top), 1)
        pygame.draw.line(pantalla, BLANCO, (plataforma.right, plataforma.top + 5), (plataforma.right - 10, plataforma.top), 1)

    # Dibujar Coyotes
    for coyote in coyotes:
        coyote.dibujar(pantalla)

    # Dibujar el personaje
    if not juego_terminado or victoria:
        dibujar_personaje(pantalla, x, y, current_frame)
    
    # Dibujar HUD (Vida y Tiempo)
    dibujar_barra_vida(pantalla, vida_frankenstein, VIDA_MAXIMA)
    dibujar_temporizador(pantalla, tiempo_restante if not juego_terminado else 0)

    # Dibujar mensaje de Fin de Juego
    if juego_terminado:
        if victoria:
            mensaje = "¡SUPERVIVENCIA LOGRADA!"
            color_mensaje = VERDE_VICTORIA
        else:
            mensaje = "GAME OVER - ¡Atrapado por los Coyotes Feroces!"
            color_mensaje = ROJO_VIDA
            
        texto_final = fuente_grande.render(mensaje, True, color_mensaje)
        texto_instruccion = fuente_pequena.render("Presiona ENTER para volver a intentarlo", True, NEGRO)
        
        pantalla.blit(texto_final, (ANCHO // 2 - texto_final.get_width() // 2, ALTO // 2 - 50))
        pantalla.blit(texto_instruccion, (ANCHO // 2 - texto_instruccion.get_width() // 2, ALTO // 2 + 30))
    
    # --- Actualizar pantalla ---
    pygame.display.flip()
    clock.tick(FPS)
