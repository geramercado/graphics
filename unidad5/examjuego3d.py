from vpython import *
import random

# ==============================================================================
# CONFIGURACIÓN DE LA ESCENA Y VARIABLES GLOBALES
# ==============================================================================

# Escena 3D
scene = canvas(title="Aventura 3D: Plataformas y Burros",
               width=800, height=600,
               center=vector(0, 3, 0),  # Centro de la escena para una mejor vista inicial
               background=vector(0.3, 0.4, 0.8)) # Cielo azul oscuro

# Variables de juego
velocidad_caminar = 0.15
velocidad_correr = 0.35
velocidad_actual = velocidad_caminar
angulo = 0
posicion_player = vector(0, 0, 0)
altura_pie = 0.5  # La altura del pie del personaje (mitad del cuerpo + pie)

# Estado del personaje
saltando = False
vel_y = 0
gravedad = 0.012
puntuacion = 0
caminando = False
corriendo = False

# ==============================================================================
# MODELADO DE OBJETOS
# ==============================================================================

# --- Personaje Principal (Donkey Humanoide) ---
# Usamos un conjunto de objetos para el personaje
player_parts = []
color_piel = color.gray(0.5)

# Cuerpo (Body)
body = box(pos=vector(0, 1.5, 0), size=vector(0.6, 1.0, 0.4), color=color_piel)
player_parts.append(body)

# Cabeza (Head)
head = sphere(pos=vector(0, 2.2, 0), radius=0.3, color=color_piel)
# Hocico simplificado
nose = box(pos=vector(0, 2.2, 0.25), size=vector(0.2, 0.15, 0.15), color=color.gray(0.4))
player_parts.extend([head, nose])

# Brazos (Arms) - Cilindros delgados
arm_L = cylinder(pos=vector(-0.4, 1.7, 0), axis=vector(0, -0.7, 0), radius=0.1, color=color_piel)
arm_R = cylinder(pos=vector(0.4, 1.7, 0), axis=vector(0, -0.7, 0), radius=0.1, color=color_piel)
player_parts.extend([arm_L, arm_R])

# Piernas (Legs) - Base de la altura_pie
leg_FL = cylinder(pos=vector(-0.2, 1.0, 0.1), axis=vector(0, -1.0, 0), radius=0.12, color=color.gray(0.3))
leg_FR = cylinder(pos=vector(0.2, 1.0, 0.1), axis=vector(0, -1.0, 0), radius=0.12, color=color.gray(0.3))
leg_BL = cylinder(pos=vector(-0.2, 1.0, -0.1), axis=vector(0, -1.0, 0), radius=0.12, color=color.gray(0.3))
leg_BR = cylinder(pos=vector(0.2, 1.0, -0.1), axis=vector(0, -1.0, 0), radius=0.12, color=color.gray(0.3))
player_parts.extend([leg_FL, leg_FR, leg_BL, leg_BR])

# El personaje completo está agrupado en un compound (aunque lo moveremos manualmente)
player_center = body.pos # Usaremos 'body.pos' como la posición de referencia

# Etiqueta de Puntuación
score_label = wtext(text=f'Puntuación: {puntuacion}', pos=scene.title_anchor)

# --- Plataformas (Obstáculos con Altura) ---
# El suelo base (Platform 0)
floor = box(pos=vector(0, -0.1, 0), size=vector(40, 0.2, 40), color=vector(0.2, 0.6, 0.2))

platforms = [floor]
platforms_data = [
    # [posición_x, posición_y, posición_z, size_x, size_y, size_z]
    [-5, 2.0, 5, 8, 0.3, 8],
    [5, 4.0, 10, 5, 0.3, 5],
    [15, 6.0, 0, 10, 0.3, 10],
    [-10, 1.0, -10, 4, 0.3, 4],
]

for p in platforms_data:
    platforms.append(box(pos=vector(p[0], p[1], p[2]), size=vector(p[3], p[4], p[5]), color=color.gray(0.3)))

# --- Enemigo Patrullando (Nopal Malvado Simplificado) ---
enemy_pos_min = -8
enemy_pos_max = 8
enemy_speed = 0.05
enemy_direction = 1 # 1: hacia adelante, -1: hacia atrás

enemy_body = sphere(pos=vector(enemy_pos_min, 1, 10), radius=0.5, color=color.red, shininess=0)
enemy_body.label = label(pos=enemy_body.pos + vector(0, 1, 0), text='¡Nopal Malvado!', color=color.red, opacity=0)

# --- Monedas Recolectables ---
monedas = []
monedas_data = [
    [0, 1.5, 0],
    [-5, 2.5, 5],
    [5, 4.5, 10],
    [15, 6.5, 0],
    [-10, 1.5, -10],
    [3, 1.5, -5]
]

for d in monedas_data:
    coin = cylinder(pos=vector(d[0], d[1], d[2]), axis=vector(0, 0.1, 0), radius=0.3, color=color.yellow, texture=textures.metal)
    coin.rotation_speed = random.uniform(0.05, 0.1) # Velocidad de giro individual
    monedas.append(coin)

# ==============================================================================
# LÓGICA DE JUEGO Y FUNCIONES DE COLISIÓN
# ==============================================================================

def find_ground_y(current_pos):
    """
    Determina la altura Y de la plataforma de soporte bajo el personaje.
    Retorna la altura Y máxima de la superficie de una plataforma que el
    personaje está tocando o por encima de la cual está cayendo.
    """
    ground_y = -0.1 + (floor.size.y / 2) # Altura del suelo base
    
    # Altura máxima del pie del personaje (y_pos + altura_pie)
    player_feet_y = current_pos.y
    
    for p in platforms:
        # 1. Comprobar si el jugador está horizontalmente sobre la plataforma
        # Nota: p.pos es el centro de la caja. p.size/2 es la mitad de la dimensión.
        
        plataforma_min_x = p.pos.x - p.size.x / 2
        plataforma_max_x = p.pos.x + p.size.x / 2
        plataforma_min_z = p.pos.z - p.size.z / 2
        plataforma_max_z = p.pos.z + p.size.z / 2
        
        on_x = (current_pos.x + 0.3) > plataforma_min_x and (current_pos.x - 0.3) < plataforma_max_x
        on_z = (current_pos.z + 0.3) > plataforma_min_z and (current_pos.z - 0.3) < plataforma_max_z
        
        # 2. Comprobar si el jugador está verticalmente aterrizando en la parte superior
        plataforma_top_y = p.pos.y + p.size.y / 2
        
        # El jugador está cerca de la superficie Y de la plataforma
        if on_x and on_z:
            # Si el jugador está justo por encima o tocando la plataforma,
            # actualiza la altura del suelo.
            if player_feet_y >= plataforma_top_y - 0.1 and player_feet_y <= plataforma_top_y + 0.1:
                ground_y = max(ground_y, plataforma_top_y)

    return ground_y

def update_player_position():
    """Aplica la posición y rotación a todas las partes del personaje."""
    global angulo, posicion_player

    # Calcula el vector de dirección y desplazamiento
    direction_vector = vector(sin(angulo), 0, cos(angulo))
    
    # 1. Mueve el centro del personaje (posicion_player)
    # 2. Rota el eje de todas las partes
    # 3. Posiciona las partes en relación al centro rotado

    # Mover el centro del cuerpo a la nueva posición_player
    diff_pos = body.pos - player_center # La diferencia vertical ya aplicada por la gravedad

    # El punto de pivote para la rotación es el centro del cuerpo (body.pos.y)
    pivote = vector(posicion_player.x, body.pos.y, posicion_player.z)
    
    for parte in player_parts:
        # Calcular la posición relativa al centro del personaje
        rel_pos_unrotated = parte.pos - player_center
        
        # Aplicar la rotación (solo en el plano XZ)
        x_rotated = rel_pos_unrotated.x * cos(-angulo) + rel_pos_unrotated.z * sin(-angulo)
        z_rotated = -rel_pos_unrotated.x * sin(-angulo) + rel_pos_unrotated.z * cos(-angulo)
        
        # Nueva posición absoluta
        parte.pos = pivote + vector(x_rotated, rel_pos_unrotated.y, z_rotated)

        # La rotación del eje solo afecta a los cilindros (brazos/piernas/cuerpo si tuviera)
        if hasattr(parte, 'axis') and parte != body:
             # Para los brazos/piernas/cuerpo, queremos que su orientación siga la rotación del personaje
             # Esto simplifica la rotación de los cilindros si tienen un eje que debe alinearse con la dirección.
             # Para este modelo simple, solo rotaremos las piernas en el loop principal para la animación.
             pass

    # Aplicar la rotación al cuerpo y la cabeza para que miren en la dirección
    body.axis = direction_vector
    head.axis = direction_vector
    nose.axis = direction_vector
    
    # Sincronizar la posición de referencia con la posición global XZ
    player_center = body.pos # Esto mantiene el centro del grupo en el centro del cuerpo

# ==============================================================================
# LOOP PRINCIPAL DEL JUEGO
# ==============================================================================

def animar_patas(velocidad_de_paso):
    """
    Animación simple de las extremidades del personaje.
    Utiliza la velocidad_de_paso para hacer que la animación sea más rápida al correr.
    """
    global fase_patas
    fase_patas += velocidad_de_paso
    amp = 0.3 # Amplitud del movimiento de las piernas

    # Movimiento cruzado
    swing = amp * sin(fase_patas)
    
    # Piernas
    leg_FL.axis = vector(swing, -1.0, 0)
    leg_BR.axis = vector(swing, -1.0, 0)
    leg_FR.axis = vector(-swing, -1.0, 0)
    leg_BL.axis = vector(-swing, -1.0, 0)

    # Brazos (opcional, pero mejora la sensación de movimiento)
    arm_L.axis = vector(swing * 0.5, -0.7, 0)
    arm_R.axis = vector(-swing * 0.5, -0.7, 0)

def game_loop():
    global angulo, posicion_player, saltando, vel_y, velocidad_actual, caminando, corriendo, puntuacion
    
    rate(60)
    keys = keysdown()
    
    # --- 1. Entrada del Jugador y Movimiento ---
    caminando = False
    corriendo = False
    
    # Modo Correr: Si se presiona Shift, aumenta la velocidad
    if 'shift' in keys:
        velocidad_actual = velocidad_correr
        corriendo = True
    else:
        velocidad_actual = velocidad_caminar

    # Movimiento 360° (Adelante/Atrás)
    if 'up' in keys or 'w' in keys:
        posicion_player += vector(velocidad_actual * sin(angulo), 0, velocidad_actual * cos(angulo))
        caminando = True

    if 'down' in keys or 's' in keys:
        posicion_player -= vector(velocidad_actual * sin(angulo), 0, velocidad_actual * cos(angulo))
        caminando = True

    # Girar (Izquierda/Derecha)
    if 'left' in keys or 'a' in keys:
        angulo -= 0.08
    if 'right' in keys or 'd' in keys:
        angulo += 0.08

    # Saltar
    current_ground_y = find_ground_y(body.pos)
    if ('space' in keys or 'j' in keys) and not saltando and body.pos.y <= current_ground_y + 0.1:
        saltando = True
        vel_y = 0.25 # Impulso inicial de salto

    # --- 2. Gravedad y Colisión con Plataformas ---
    
    # Aplica gravedad (si no está en el suelo)
    if body.pos.y > current_ground_y or vel_y > 0:
        vel_y -= gravedad
        # Mover todo el personaje verticalmente
        for parte in player_parts:
            parte.pos.y += vel_y
    
    # Aterrizaje en Plataforma/Suelo
    if body.pos.y <= current_ground_y + 0.1:
        # Corrige la posición Y de todo el personaje para que se asiente en el suelo
        diff = current_ground_y - body.pos.y
        for parte in player_parts:
            parte.pos.y += diff
        
        vel_y = 0
        saltando = False
        
    # Corregir la posición XZ del personaje (body.pos solo tiene la Y correcta aquí)
    body.pos.x = posicion_player.x
    body.pos.z = posicion_player.z

    # --- 3. Animación de Pasos y Estela ---
    if caminando and not saltando:
        paso_speed = 0.12 * (velocidad_actual / velocidad_caminar) # Más rápido al correr
        animar_patas(paso_speed)
    else:
        # Restablecer piernas y brazos a la posición de descanso
        leg_FL.axis = vector(0, -1.0, 0)
        leg_FR.axis = vector(0, -1.0, 0)
        leg_BL.axis = vector(0, -1.0, 0)
        leg_BR.axis = vector(0, -1.0, 0)
        arm_L.axis = vector(0, -0.7, 0)
        arm_R.axis = vector(0, -0.7, 0)

    # Actualizar la posición y rotación de todas las partes del personaje
    update_player_position()
    
    # --- 4. Lógica de Enemigo ---
    
    # Movimiento del enemigo (patrullaje lineal en el eje X)
    enemy_body.pos.x += enemy_speed * enemy_direction
    enemy_body.label.pos = enemy_body.pos + vector(0, 1, 0) # Actualizar posición de la etiqueta

    if enemy_body.pos.x > enemy_pos_max or enemy_body.pos.x < enemy_pos_min:
        enemy_direction *= -1 # Cambiar dirección
        
    # Colisión con Enemigo (reinicio si el jugador está en el mismo nivel)
    dist_to_enemy = mag(vector(posicion_player.x, 0, posicion_player.z) - vector(enemy_body.pos.x, 0, enemy_body.pos.z))
    # Colisión solo si el jugador no está saltando por encima
    if dist_to_enemy < 0.8 and abs(body.pos.y - enemy_body.pos.y) < 1.0: 
        # REINICIO
        posicion_player = vector(0, 0, 0)
        body.pos = vector(0, 1.5, 0)
        vel_y = 0
        saltando = False
        print("¡Colisión con el enemigo! Reiniciando posición.")

    # --- 5. Lógica de Monedas ---
    monedas_a_eliminar = []
    for coin in monedas:
        # Rotar la moneda
        coin.rotate(angle=coin.rotation_speed, axis=vector(0, 1, 0))
        
        # Comprobar colisión con el jugador
        dist_to_coin = mag(body.pos - coin.pos)
        if dist_to_coin < 0.6: # Distancia de recolección
            monedas_a_eliminar.append(coin)
            puntuacion += 10
            score_label.text = f'Puntuación: {puntuacion}'
            
    # Eliminar monedas recolectadas
    for coin in monedas_a_eliminar:
        coin.visible = False
        monedas.remove(coin)

    # --- 6. Cámara de Seguimiento ---
    # La cámara debe seguir al personaje, manteniendo una vista desde atrás y arriba.
    
    offset = vector(-5, 5, -5) # Posición de la cámara relativa al personaje (atrás, arriba, a un lado)
    
    # Rotar el offset de la cámara para que se alinee con el ángulo del personaje
    cam_x = offset.x * cos(angulo) - offset.z * sin(angulo)
    cam_z = offset.x * sin(angulo) + offset.z * cos(angulo)
    
    camera_pos = body.pos + vector(cam_x, offset.y, cam_z)
    
    # Mover la cámara lentamente hacia la posición deseada para un movimiento suave
    scene.center = body.pos
    scene.camera.pos = scene.camera.pos * 0.95 + camera_pos * 0.05
    scene.camera.axis = body.pos - scene.camera.pos

    # Llamar al bucle de juego continuamente
    scene.bind('enter', game_loop)

# Iniciar el bucle de juego
while True:
    game_loop()
