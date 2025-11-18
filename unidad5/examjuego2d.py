import pygame
import sys
import random
import time

# --- Inicialización ---
pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Hombre Lobo - Plataformas Gerardo Mercado Hurtado/ Raúl Martínez Martínez")
clock = pygame.time.Clock()
FPS = 60 # Aumentamos FPS para mejor sensación de plataforma

# --- CONFIGURACIÓN DE MÚSICA ---
# Usaremos un placeholder, asumiendo que tienes 'wolf_theme.mp3'
try:
    pygame.mixer.music.load('wolf_theme.mp3') 
    pygame.mixer.music.play(-1) 
    pygame.mixer.music.set_volume(0.4) 
    print("Música cargada y reproduciéndose.")
except pygame.error as e:
    print(f"ADVERTENCIA: No se pudo cargar la música de fondo 'wolf_theme.mp3'. Error: {e}")
# ----------------------------------------

# --- Colores ---
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
LUNA_AZUL = (150, 180, 255)
AZUL_NOCHE = (10, 20, 40)
MARRON_SUELO = (80, 50, 20)
GRIS_HOMBRE_LOBO = (50, 50, 50)
ROJO_VIDA = (200, 50, 50)
VERDE_VICTORIA = (50, 200, 50)
AMARILLO_MONEDA = (255, 220, 0)
MARRON_BLOQUE = (100, 70, 40)
AZUL_PREGUNTA = (50, 50, 150)
ROJO_LADRILLO = (180, 80, 80)


# --- Tipografía ---
fuente_pequena = pygame.font.Font(None, 24)
fuente_grande = pygame.font.Font(None, 74)

# --- Propiedades del Personaje (Hombre Lobo) ---
x, y = 100, 400
ancho_personaje = 40
alto_personaje = 70
velocidad = 6 # Más rápido que Frankenstein
salto = False
vel_y = 0
gravedad = 1
fuerza_salto = -17 # Salto más alto
suelo_base = ALTO - 50 # Nuevo suelo más bajo

# --- Variables del Juego ---
VIDA_MAXIMA = 100
vida_personaje = VIDA_MAXIMA
juego_terminado = False
victoria = False
monedas_recolectadas = 0
MONEDAS_REQUERIDAS = 5 # Meta del nivel

# --- Clase Murciélago (Enemigo Patrullador) ---
class Murcielago:
    def __init__(self, x, y, ancho, alto, limite_izq, limite_der, velocidad):
        self.ancho = ancho
        self.alto = alto
        self.x = x
        self.y = y
        self.velocidad = velocidad
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        self.limite_izq = limite_izq
        self.limite_der = limite_der
        self.damage_cooldown = 0
        self.color = (150, 0, 150) # Púrpura oscuro

    def mover(self):
        self.x += self.velocidad
        
        if self.x <= self.limite_izq:
            self.velocidad = abs(self.velocidad)
        elif self.x + self.ancho >= self.limite_der:
            self.velocidad = -abs(self.velocidad)
            
        self.rect.x = self.x

    def dibujar(self, pantalla):
        # Cuerpo
        pygame.draw.ellipse(pantalla, self.color, (self.x, self.y, self.ancho, self.alto))
        # Alas (dependiendo de la dirección, simple representación)
        if self.velocidad > 0: # derecha
            pygame.draw.polygon(pantalla, self.color, [(self.x, self.y), (self.x + self.ancho // 2, self.y - 10), (self.x + self.ancho, self.y)])
        else: # izquierda
            pygame.draw.polygon(pantalla, self.color, [(self.x, self.y + self.alto), (self.x + self.ancho // 2, self.y + self.alto + 10), (self.x + self.ancho, self.y + self.alto)])
        self.rect.y = self.y # Asegurarse de que el rectángulo esté actualizado
        self.rect.x = self.x


# --- Bloques y Coleccionables ---
class Bloque:
    def __init__(self, x, y, tipo='plataforma'):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.tipo = tipo # 'plataforma', 'rompible', 'pregunta'
        self.contenido = 'moneda' # Contenido del bloque 'pregunta'
        self.golpeado = False
        self.visible = True
        self.color = MARRON_BLOQUE if tipo == 'plataforma' else ROJO_LADRILLO if tipo == 'rompible' else AZUL_PREGUNTA

    def dibujar(self, pantalla):
        if self.visible:
            pygame.draw.rect(pantalla, self.color, self.rect)
            pygame.draw.rect(pantalla, NEGRO, self.rect, 2) # Borde
            if self.tipo == 'pregunta':
                 # Signo de interrogación
                texto = fuente_pequena.render("?", True, AMARILLO_MONEDA if not self.golpeado else NEGRO)
                pantalla.blit(texto, (self.rect.x + 10, self.rect.y + 5))
            elif self.tipo == 'rompible':
                # Diseño de ladrillo
                pygame.draw.line(pantalla, NEGRO, (self.rect.x + 20, self.rect.y), (self.rect.x + 20, self.rect.y + 40), 1)
                pygame.draw.line(pantalla, NEGRO, (self.rect.x, self.rect.y + 20), (self.rect.x + 40, self.rect.y + 20), 1)
                
    def golpe_cabeza(self):
        if self.tipo == 'pregunta' and not self.golpeado:
            self.golpeado = True
            # Simular que suelta una moneda
            return self.contenido 
        elif self.tipo == 'rompible':
            self.visible = False # El bloque se rompe
            return None
        return None

class Moneda:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 15, 15)
        self.visible = True
        
    def dibujar(self, pantalla):
        if self.visible:
            pygame.draw.circle(pantalla, AMARILLO_MONEDA, self.rect.center, 7)
            pygame.draw.circle(pantalla, NEGRO, self.rect.center, 7, 1) # Borde


# --- Diseño del Nivel ---
# Bloques Fijos y Rompibles
bloques = [
    Bloque(100, suelo_base - 100, 'plataforma'),
    Bloque(140, suelo_base - 100, 'plataforma'),
    Bloque(180, suelo_base - 100, 'plataforma'),
    
    Bloque(300, suelo_base - 180, 'pregunta'),
    Bloque(340, suelo_base - 180, 'rompible'),
    Bloque(380, suelo_base - 180, 'pregunta'),
    
    Bloque(500, suelo_base - 50, 'plataforma'),
    Bloque(540, suelo_base - 50, 'plataforma'),
    
    # Bloques altos para desafío
    Bloque(650, suelo_base - 250, 'plataforma'),
    Bloque(700, suelo_base - 250, 'pregunta'),
]

# Plataformas adicionales (solo para colisión de salto)
plataformas_solas = [b.rect for b in bloques if b.tipo == 'plataforma' or b.tipo == 'rompible' or (b.tipo == 'pregunta' and b.visible)]

# Enemigos Patrulladores
murcielagos = [
    Murcielago(500, suelo_base - 50 - 30, 30, 30, 500, 580, 2), # Patrulla corta
    Murcielago(300, 300, 30, 30, 200, 450, 3), # Patrulla larga flotante
]

# Monedas Iniciales (fuera de bloques)
coleccionables = [
    Moneda(400, suelo_base - 100),
    Moneda(600, suelo_base - 10),
    Moneda(700, suelo_base - 280),
]

# --- Funciones de Dibujo ---

def dibujar_fondo(pantalla):
    # Cielo Nocturno
    pantalla.fill(AZUL_NOCHE)
    
    # Luna (simple círculo)
    pygame.draw.circle(pantalla, BLANCO, (ANCHO - 100, 100), 50)
    pygame.draw.circle(pantalla, LUNA_AZUL, (ANCHO - 105, 95), 45) # Efecto cráter
    
    # Suelo
    pygame.draw.rect(pantalla, MARRON_SUELO, (0, suelo_base, ANCHO, ALTO - suelo_base))
    
    # Estrellas (simples puntos blancos)
    for _ in range(50):
        x_star = random.randint(0, ANCHO)
        y_star = random.randint(0, suelo_base - 10)
        pantalla.set_at((x_star, y_star), BLANCO)

def dibujar_personaje(pantalla, x, y, current_frame, en_movimiento, en_salto):
    # Hombre Lobo simplificado
    cuerpo_x, cuerpo_y = x, y
    
    # Color de Pelo/Piel
    color_pelo = GRIS_HOMBRE_LOBO
    color_garra = BLANCO
    
    # 1. Cuerpo (más robusto)
    pygame.draw.rect(pantalla, color_pelo, (cuerpo_x, cuerpo_y + 10, ancho_personaje, alto_personaje - 10))
    
    # 2. Cabeza y Hocico
    pygame.draw.circle(pantalla, color_pelo, (cuerpo_x + ancho_personaje // 2, cuerpo_y + 10), 15)
    pygame.draw.polygon(pantalla, NEGRO, [
        (cuerpo_x + 15, cuerpo_y + 10), 
        (cuerpo_x + 25, cuerpo_y + 10), 
        (cuerpo_x + 20, cuerpo_y + 0) # Oreja izquierda
    ]) 
    pygame.draw.polygon(pantalla, NEGRO, [
        (cuerpo_x + 25, cuerpo_y + 10), 
        (cuerpo_x + 35, cuerpo_y + 10), 
        (cuerpo_x + 30, cuerpo_y + 0) # Oreja derecha
    ]) 
    
    # Hocico
    pygame.draw.rect(pantalla, NEGRO, (cuerpo_x + 17, cuerpo_y + 15, 6, 8))
    
    # Ojos (Amarillos de lobo)
    pygame.draw.circle(pantalla, AMARILLO_MONEDA, (cuerpo_x + 15, cuerpo_y + 12), 3)
    pygame.draw.circle(pantalla, AMARILLO_MONEDA, (cuerpo_x + 25, cuerpo_y + 12), 3)
    
    # 3. Patas (Animación de caminar/saltar)
    # Posiciones base para las patas
    pata_izq_x = cuerpo_x + 10
    pata_der_x = cuerpo_x + 30
    pata_y_base = cuerpo_y + alto_personaje
    
    # Animación de Patas (Simple balanceo de dos frames)
    # Frame 0: Derecha adelante, Izquierda atrás
    # Frame 1: Izquierda adelante, Derecha atrás
    # En Salto/Caída: Ambas hacia abajo
    
    if en_salto or not en_movimiento:
        # Posición de descanso o salto (patas estiradas)
        pata_izq_offset = 0
        pata_der_offset = 0
    else:
        if current_frame == 0:
            # Caminar Frame 0
            pata_izq_offset = -5
            pata_der_offset = 5
        else:
            # Caminar Frame 1
            pata_izq_offset = 5
            pata_der_offset = -5

    # Dibujar Patas
    # Pata Izquierda
    pygame.draw.rect(pantalla, color_pelo, (pata_izq_x - 5, pata_y_base - 20, 10, 20))
    pygame.draw.rect(pantalla, color_garra, (pata_izq_x - 5 + pata_izq_offset, pata_y_base - 5, 15, 5))
    
    # Pata Derecha
    pygame.draw.rect(pantalla, color_pelo, (pata_der_x - 5, pata_y_base - 20, 10, 20))
    pygame.draw.rect(pantalla, color_garra, (pata_der_x - 5 + pata_der_offset, pata_y_base - 5, 15, 5))


def dibujar_barra_vida(pantalla, vida_actual, vida_maxima):
    ancho_barra = 200
    alto_barra = 20
    x_barra, y_barra = 10, 10
    
    porcentaje_vida = vida_actual / vida_maxima
    ancho_relleno = int(ancho_barra * porcentaje_vida)
    
    pygame.draw.rect(pantalla, NEGRO, (x_barra, y_barra, ancho_barra, alto_barra), 2)
    pygame.draw.rect(pantalla, ROJO_VIDA, (x_barra, y_barra, ancho_relleno, alto_barra))
    
    texto_vida = fuente_pequena.render(f"HP: {max(0, vida_actual)}/{vida_maxima}", True, BLANCO)
    pantalla.blit(texto_vida, (x_barra + 5, y_barra + 2))

def dibujar_hud_monedas(pantalla, cantidad):
    texto_monedas = fuente_pequena.render(f"Monedas: {cantidad}/{MONEDAS_REQUERIDAS}", True, AMARILLO_MONEDA)
    pantalla.blit(texto_monedas, (ANCHO - texto_monedas.get_width() - 10, 10))


# --- Bucle principal ---
frame_counter = 0
animation_speed = 8
current_frame = 0 # 0 o 1 para caminar

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if juego_terminado and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            # Reiniciar juego
            x, y = 100, 400
            vida_personaje = VIDA_MAXIMA
            juego_terminado = False
            victoria = False
            monedas_recolectadas = 0
            vel_y = 0
            salto = False
            # Resetear bloques y coleccionables
            bloques = [
                Bloque(100, suelo_base - 100, 'plataforma'),
                Bloque(140, suelo_base - 100, 'plataforma'),
                Bloque(180, suelo_base - 100, 'plataforma'),
                Bloque(300, suelo_base - 180, 'pregunta'),
                Bloque(340, suelo_base - 180, 'rompible'),
                Bloque(380, suelo_base - 180, 'pregunta'),
                Bloque(500, suelo_base - 50, 'plataforma'),
                Bloque(540, suelo_base - 50, 'plataforma'),
                Bloque(650, suelo_base - 250, 'plataforma'),
                Bloque(700, suelo_base - 250, 'pregunta'),
            ]
            coleccionables = [
                Moneda(400, suelo_base - 100),
                Moneda(600, suelo_base - 10),
                Moneda(700, suelo_base - 280),
            ]
            # Resetear enemigos (si es necesario)

    if not juego_terminado:
        # --- Entrada y Movimiento ---
        teclas = pygame.key.get_pressed()
        is_moving = False
        
        if teclas[pygame.K_LEFT]:
            x -= velocidad
            is_moving = True
        if teclas[pygame.K_RIGHT]:
            x += velocidad
            is_moving = True
            
        if teclas[pygame.K_UP] and not salto:
            salto = True
            vel_y = fuerza_salto 

        # --- Física y Gravedad ---
        if salto:
            y += vel_y
            vel_y += gravedad
        
        # --- Colisión con Bloques y Suelo ---
        rect_personaje = pygame.Rect(x, y, ancho_personaje, alto_personaje)
        en_suelo = False
        
        # Recolectar Monedas
        coleccionables_a_eliminar = []
        for moneda in coleccionables:
            if moneda.visible and rect_personaje.colliderect(moneda.rect):
                monedas_recolectadas += 1
                moneda.visible = False
                coleccionables_a_eliminar.append(moneda)
                
        for moneda_eliminar in coleccionables_a_eliminar:
            if moneda_eliminar in coleccionables:
                coleccionables.remove(moneda_eliminar)

        # Colisión Vertical (Arriba y Abajo)
        bloques_solidos = [b for b in bloques if b.visible]
        for bloque in bloques_solidos:
            
            # Colisión con la cabeza (romper o preguntar)
            if rect_personaje.colliderect(bloque.rect) and vel_y < 0: # Si va subiendo
                if rect_personaje.top <= bloque.rect.bottom <= rect_personaje.top + 10:
                    vel_y = 0 # Detener la subida
                    y = bloque.rect.bottom # Aterrizar en el bloque por debajo
                    
                    contenido_liberado = bloque.golpe_cabeza()
                    if contenido_liberado == 'moneda':
                        # Generar moneda flotante
                        nueva_moneda = Moneda(bloque.rect.centerx - 7, bloque.rect.top - 20)
                        coleccionables.append(nueva_moneda)
                        
            # Colisión con los pies (aterrizaje)
            if rect_personaje.colliderect(bloque.rect) and vel_y >= 0: # Si va cayendo
                if rect_personaje.bottom >= bloque.rect.top >= rect_personaje.bottom - 10:
                    y = bloque.rect.top - alto_personaje
                    salto = False
                    vel_y = 0
                    en_suelo = True
                    break

        # Colisión Suelo Base
        if y + alto_personaje >= suelo_base and vel_y >= 0:
            y = suelo_base - alto_personaje
            salto = False
            vel_y = 0
            en_suelo = True
        elif not en_suelo and not salto: # Si no colisiona con nada y no está saltando, forzar la caída
            salto = True 
            vel_y = 1
            
        # Colisión Horizontal (Simplemente evitar atravesar por ahora)
        for bloque in bloques_solidos:
            if rect_personaje.colliderect(bloque.rect):
                if rect_personaje.right > bloque.rect.left and x < bloque.rect.left:
                    x = bloque.rect.left - ancho_personaje
                elif rect_personaje.left < bloque.rect.right and x > bloque.rect.left:
                    x = bloque.rect.right


        # --- Lógica de Animación (Hombre Lobo) ---
        if is_moving and not salto:
            frame_counter += 1
            if frame_counter >= animation_speed:
                current_frame = 1 - current_frame
                frame_counter = 0
        else:
            current_frame = 0
            frame_counter = 0
            
        # --- Lógica de Murciélagos ---
        
        for murcielago in murcielagos:
            murcielago.mover()
            
            # Colisión con Hombre Lobo
            if rect_personaje.colliderect(murcielago.rect):
                if murcielago.damage_cooldown == 0:
                    vida_personaje -= 10
                    murcielago.damage_cooldown = FPS * 1 # 1 segundo de invulnerabilidad
                    
                    # Empuje (knockback)
                    if x < murcielago.x:
                        x -= 10
                    else:
                        x += 10
                
            if murcielago.damage_cooldown > 0:
                murcielago.damage_cooldown -= 1

        # --- Comprobar Game Over y Victoria ---
        if vida_personaje <= 0:
            juego_terminado = True
            victoria = False
        
        # Condición de victoria: recolectar todas las monedas
        if monedas_recolectadas >= MONEDAS_REQUERIDAS:
            juego_terminado = True
            victoria = True

    # --- Dibujar ---
    dibujar_fondo(pantalla)
    
    # Dibujar Bloques
    for bloque in bloques:
        bloque.dibujar(pantalla)
        
    # Dibujar Coleccionables
    for moneda in coleccionables:
        moneda.dibujar(pantalla)

    # Dibujar Murciélagos
    for murcielago in murcielagos:
        murcielago.dibujar(pantalla)

    # Dibujar el personaje
    if not juego_terminado or victoria:
        dibujar_personaje(pantalla, x, y, current_frame, is_moving, salto)
    
    # Dibujar HUD (Vida y Monedas)
    dibujar_barra_vida(pantalla, vida_personaje, VIDA_MAXIMA)
    dibujar_hud_monedas(pantalla, monedas_recolectadas)

    # Dibujar mensaje de Fin de Juego
    if juego_terminado:
        if victoria:
            mensaje = "¡NIVEL COMPLETADO! ¡La Luna es tuya!"
            color_mensaje = VERDE_VICTORIA
        else:
            mensaje = "¡GAME OVER! Fuiste derrotado."
            color_mensaje = ROJO_VIDA
            
        texto_final = fuente_grande.render(mensaje, True, color_mensaje)
        texto_instruccion = fuente_pequena.render("Presiona ENTER para reiniciar el nivel", True, BLANCO)
        
        pantalla.blit(texto_final, (ANCHO // 2 - texto_final.get_width() // 2, ALTO // 2 - 50))
        pantalla.blit(texto_instruccion, (ANCHO // 2 - texto_instruccion.get_width() // 2, ALTO // 2 + 30))
    
    # --- Actualizar pantalla ---
    pygame.display.flip()
    clock.tick(FPS)
