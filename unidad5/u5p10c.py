import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

# ==== CONFIGURACIÓN ====
n_personas = 5
# Ajustamos la velocidad para que el seguimiento parezca más fluido
velocidad = 0.08 
radio_colision = 0.5
radio_lider = 1.0 # Distancia ideal de seguimiento

# Conexiones del esqueleto
connections = [
    ("head", "neck"),
    ("neck", "shoulder_L"), ("neck", "shoulder_R"),
    ("shoulder_L", "hand_L"), ("shoulder_R", "hand_R"),
    ("neck", "hip"),
    ("hip", "knee_L"), ("hip", "knee_R"),
    ("knee_L", "foot_L"), ("knee_R", "foot_R")
]

def skeleton_points(t, offset_x=0, offset_z=0, paso=0.0):
    """Esqueleto animado con patrón de 'baile'."""
    fase_baile = t + paso

    # Movimiento vertical de rebote (en el eje Y)
    rebote = np.sin(fase_baile * 3) * 0.1

    # Rotación simple en el eje Y (alrededor del cuerpo)
    rotacion_y = np.sin(fase_baile / 2) * 0.3 # Ángulo de rotación

    # Se usa el ángulo de movimiento (dirección de seguimiento) para orientar el esqueleto
    # En este caso, usaremos la rotación de baile para que se vean dinámicos
    
    joints = {
        "head": [0, 2 + rebote, 0],
        "neck": [0, 1.6 + rebote, 0],
        "shoulder_L": [-0.3, 1.6 + rebote, 0],
        "shoulder_R": [0.3, 1.6 + rebote, 0],
        "hand_L": [-0.6, 1.2 + rebote, 0],
        "hand_R": [0.6, 1.2 + rebote, 0],
        "hip": [0, 1.0 + rebote, 0],
        "knee_L": [-0.2, 0.5 + rebote, 0],
        "knee_R": [0.2, 0.5 + rebote, 0],
        "foot_L": [-0.2, 0.0 + rebote, 0.0],
        "foot_R": [0.2, 0.0 + rebote, 0.0],
    }

    # Movimiento de 'baile' de brazos y piernas
    swing = np.sin(fase_baile * 2) * 0.4
    
    # Brazos
    joints["hand_L"][2] = -swing 
    joints["hand_R"][2] = swing
    
    # Piernas (pequeño desplazamiento lateral en el eje X)
    joints["foot_L"][0] += -np.sin(fase_baile * 4) * 0.1
    joints["foot_R"][0] += np.sin(fase_baile * 4) * 0.1


    # Aplicar ROTACIÓN de baile (simple en el plano XZ)
    for k in joints:
        x_orig = joints[k][0]
        z_orig = joints[k][2]
        
        # Rotación
        joints[k][0] = x_orig * np.cos(rotacion_y) - z_orig * np.sin(rotacion_y)
        joints[k][2] = x_orig * np.sin(rotacion_y) + z_orig * np.cos(rotacion_y)

    # Aplicar OFFSET de posición (el movimiento de traslación)
    for k in joints:
        joints[k][0] += offset_x
        joints[k][2] += offset_z
        
    return joints


# ==== CLASE PERSONAJE ====
class Personaje:
    def __init__(self, x, z, lider=False):
        self.x = x
        self.z = z
        self.angulo = random.uniform(0, 2*np.pi)
        self.lider = lider
        self.color = "blue" if lider else "green" 
        self.paso = random.random() * 10 

    def mover(self, t, destino, otros):
        if self.lider:
            # El líder se mueve libremente en círculo
            self.x = np.cos(t/10) * 3
            self.z = np.sin(t/10) * 3
            self.color = "blue"
        else:
            # Lógica de seguimiento al destino (líder)
            dx = destino[0] - self.x
            dz = destino[1] - self.z
            distancia = np.sqrt(dx**2 + dz**2)

            if distancia > 0.1:
                # Normalizar el vector de dirección
                dx_norm = dx / distancia
                dz_norm = dz / distancia
                
                # Evitación de colisiones y seguimiento
                for o in otros:
                    if o is not self:
                        dist = np.sqrt((self.x - o.x)**2 + (self.z - o.z)**2)
                        if dist < radio_colision:
                            # Repulsión
                            dx_norm += (self.x - o.x) * 0.5 
                            dz_norm += (self.z - o.z) * 0.5
                            self.color = "yellow"
                            
                # Re-normalizar después de aplicar la evitación (para no acelerar demasiado)
                evitacion_magnitud = np.sqrt(dx_norm**2 + dz_norm**2)
                if evitacion_magnitud > 0:
                     dx_norm /= evitacion_magnitud
                     dz_norm /= evitacion_magnitud
                     
                # Movimiento hacia el destino (con ajuste de velocidad si está cerca)
                vel_ajustada = velocidad
                if distancia < radio_lider:
                    # Frena si está demasiado cerca del líder
                    vel_ajustada *= (distancia / radio_lider)
                    self.color = "red" # Indicador de que están cerca
                elif self.color != "yellow":
                    self.color = "green"
                    
                self.x += dx_norm * vel_ajustada
                self.z += dz_norm * vel_ajustada

        # Retorna el esqueleto actualizado con la nueva posición (x, z) Y el movimiento de baile
        return skeleton_points(t, self.x, self.z, self.paso)


# ==== CONFIGURAR ESCENA ====
fig = plt.figure(figsize=(9, 7))
ax = fig.add_subplot(111, projection="3d")
ax.set_xlim(-6, 6)
ax.set_ylim(0, 3)
ax.set_zlim(-6, 6)
ax.set_title("Crowds - ¡Siguiendo al líder y bailando! 💃")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

# Crear personajes
personajes = [Personaje(random.uniform(-4, 4), random.uniform(-4, 4)) for _ in range(n_personas)]
lider = Personaje(0, 0, lider=True)
personajes.insert(0, lider)

# Crear líneas para todos los esqueletos
all_lines = []
for _ in personajes:
    for _ in connections:
        line, = ax.plot([], [], [], lw=2)
        all_lines.append(line)


# ==== ANIMACIÓN ====
def update(frame):
    t = frame * 0.3
    i_line = 0

    destino = (lider.x, lider.z)

    for p in personajes:
        # Llama a mover(), que calcula la nueva posición (x, z) Y genera el esqueleto de baile
        joints = p.mover(t, destino, personajes) 
        
        for (a, b) in connections:
            x = [joints[a][0], joints[b][0]]
            y = [joints[a][1], joints[b][1]]
            z = [joints[a][2], joints[b][2]]
            all_lines[i_line].set_data(x, y)
            all_lines[i_line].set_3d_properties(z)
            all_lines[i_line].set_color(p.color)
            i_line += 1

    return all_lines


ani = FuncAnimation(fig, update, frames=400, interval=50, blit=False)
plt.show()

