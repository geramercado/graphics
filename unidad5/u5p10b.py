import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

# === CONFIGURACIÓN INICIAL ===
n_personas = 6          # número de personajes
velocidad = 0.05        # velocidad general
radio_interaccion = 0.5
TRANSITION_SPEED = 0.1  # Velocidad de la transición de altura

# Conexiones del esqueleto
connections = [
    ("head", "neck"),
    ("neck", "shoulder_L"), ("neck", "shoulder_R"),
    ("shoulder_L", "hand_L"), ("shoulder_R", "hand_R"),
    ("neck", "hip"),
    ("hip", "knee_L"), ("hip", "knee_R"),
    ("knee_L", "foot_L"), ("knee_R", "foot_R")
]

# Definición de alturas base para posición de pie y sentada
# Alturas Y de la cadera (hip)
Y_HIP_STAND = 1.0
Y_HIP_SIT = 0.4 
# Alturas Y de la rodilla (knee)
Y_KNEE_STAND = 0.5
Y_KNEE_SIT = 0.3

# Función del esqueleto modificada para interpolación
def skeleton_points(t, offset_x=0, offset_z=0, paso=0.0, estado="caminar", hip_y_factor=1.0):
    
    # Interpolación de alturas: hip_y_factor va de 1.0 (Stand) a 0.0 (Sit)
    y_cadera = Y_HIP_SIT + (Y_HIP_STAND - Y_HIP_SIT) * hip_y_factor
    y_rodilla = Y_KNEE_SIT + (Y_KNEE_STAND - Y_KNEE_SIT) * hip_y_factor
    
    # El resto de las articulaciones se mueven junto con la cadera, manteniendo su proporción
    y_cuello = y_cadera + 0.6
    y_cabeza = y_cadera + 1.0
    y_hombro = y_cuello
    y_pie = 0.0

    joints = {
        "head": [0, y_cabeza, 0],
        "neck": [0, y_cuello, 0],
        "shoulder_L": [-0.3, y_hombro, 0],
        "shoulder_R": [0.3, y_hombro, 0],
        "hand_L": [-0.6, y_cuello - 0.4, 0],
        "hand_R": [0.6, y_cuello - 0.4, 0],
        "hip": [0, y_cadera, 0],
        "knee_L": [-0.2, y_rodilla, 0],
        "knee_R": [0.2, y_rodilla, 0],
        "foot_L": [-0.2, y_pie, 0.1],
        "foot_R": [0.2, y_pie, 0.1],
    }

    # Movimiento tipo caminar (solo si está caminando)
    if estado == "caminar":
        step = np.sin(t + paso)
        joints["hand_L"][2] = 0.3 * step
        joints["hand_R"][2] = -0.3 * step
        joints["foot_L"][2] = -0.2 * step
        joints["foot_R"][2] = 0.2 * step

    # Desplazamiento global
    for k in joints:
        joints[k][0] += offset_x
        joints[k][2] += offset_z
    return joints


# === CLASE PERSONAJE ===
class Personaje:
    def __init__(self, x, z):
        self.x = x
        self.z = z
        self.angulo = random.uniform(0, 2*np.pi)
        self.estado = "sentarse"  # Estado inicial
        self.color = "blue"
        self.paso = random.random() * 10
        # Nueva variable de control para la altura (1.0 = Pie, 0.0 = Sentado)
        self.hip_factor = 1.0 

    def mover(self, t):
        # Cambio aleatorio de comportamiento
        if random.random() < 0.01:
            # Los estados ahora son: "caminar", "girar", "sentarse", "pararse"
            if self.estado in ["sentarse", "detenerse"]:
                self.estado = random.choice(["caminar", "pararse"])
            else:
                self.estado = random.choice(["sentarse", "girar"])


        # --- Lógica de Transición de Altura ---
        target_factor = 1.0 if self.estado in ["caminar", "pararse", "girar"] else 0.0
        
        if self.hip_factor < target_factor:
            self.hip_factor = min(target_factor, self.hip_factor + TRANSITION_SPEED)
        elif self.hip_factor > target_factor:
            self.hip_factor = max(target_factor, self.hip_factor - TRANSITION_SPEED)
        
        # --- Lógica de Movimiento XZ ---
        if self.estado == "caminar" and self.hip_factor > 0.9: # Solo se mueve XZ si está casi de pie
            self.x += np.cos(self.angulo) * velocidad
            self.z += np.sin(self.angulo) * velocidad
            self.color = "green"
            
        elif self.estado == "girar" and self.hip_factor > 0.9: # Gira solo si está casi de pie
            self.angulo += random.uniform(-0.3, 0.3)
            self.color = "yellow"
            
        elif self.estado == "pararse":
            self.color = "orange"
            
        elif self.estado == "sentarse" or self.estado == "detenerse":
            self.color = "blue"


        # Límites del área
        if self.x < -5 or self.x > 5:
            self.angulo = np.pi - self.angulo
        if self.z < -5 or self.z > 5:
            self.angulo = -self.angulo

        # Retorna esqueleto actualizado usando el factor de altura
        # Usamos t=0 si no estamos caminando para detener el balanceo.
        t_walk = t if self.estado == "caminar" else 0
        return skeleton_points(t_walk, self.x, self.z, self.paso, self.estado, self.hip_factor)


# === CONFIGURAR ESCENA 3D (Sin cambios) ===
fig = plt.figure(figsize=(9, 7))
ax = fig.add_subplot(111, projection="3d")
ax.set_xlim(-5, 5)
ax.set_ylim(0, 3)
ax.set_zlim(-5, 5)
ax.set_title("Crowds - Pararse y Sentarse con Transición")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

# Crear personajes
personajes = [Personaje(random.uniform(-4, 4), random.uniform(-4, 4)) for _ in range(n_personas)]

# Crear líneas para todos
all_lines = []
for _ in range(n_personas):
    for _ in connections:
        line, = ax.plot([], [], [], lw=2)
        all_lines.append(line)


# === FUNCIÓN DE ACTUALIZACIÓN (Modificada ligeramente) ===
def update(frame):
    t = frame * 0.2
    i_line = 0
    
    # Detección simple de interacciones (colisiones)
    for i, p1 in enumerate(personajes):
        # Si p1 está detenido por colisión, permítele reaccionar (por ejemplo, sentarse)
        if p1.estado == "detenerse":
            p1.estado = "sentarse" 

        for j, p2 in enumerate(personajes):
            if i != j and p1.estado == "caminar" and p2.estado == "caminar":
                dist = np.sqrt((p1.x - p2.x)**2 + (p1.z - p2.z)**2)
                if dist < radio_interaccion:
                    p1.estado = "detenerse"
                    p2.estado = "detenerse" # Detenerse temporalmente

    # Actualizar y dibujar
    for p in personajes:
        joints = p.mover(t)
        for (a, b) in connections:
            x = [joints[a][0], joints[b][0]]
            y = [joints[a][1], joints[b][1]]
            z = [joints[a][2], joints[b][2]]
            all_lines[i_line].set_data(x, y)
            all_lines[i_line].set_3d_properties(z)
            all_lines[i_line].set_color(p.color)
            i_line += 1

    return all_lines


# === ANIMACIÓN ===
ani = FuncAnimation(fig, update, frames=300, interval=50, blit=False)
plt.show()

