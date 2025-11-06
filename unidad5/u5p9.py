# Gerardo Mercado Hurtado
# Raúl Martínez Martínez 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- 1. Función del esqueleto ---
def skeleton_points(t, mode):
    # Parámetros básicos de movimiento
    step = np.sin(t)
    sway = np.sin(t / 2) * 0.3
    jump = 0
    height_factor = 1.0 # Factor para transiciones de altura (usado en Sentarse)

    # Movimiento específico por modo
    if mode == "Saltar":
        jump = np.abs(np.sin(t)) * 0.3
    elif mode == "Correr":
        # Aumentamos la velocidad y el rango de movimiento de correr
        t_run = t * 2.0  # Doble de velocidad
        step_run = np.sin(t_run)
        sway = np.sin(t_run / 2) * 0.1 # Menos balanceo lateral
        arm_swing = np.cos(t_run) * 0.4 # Mayor balanceo de brazos
        height_bounce = np.abs(np.sin(t_run)) * 0.08 # Rebote vertical más notorio

    # Posición de transición para Sentarse
    elif mode == "Sentarse":
        transition_t = np.clip(t, 0, np.pi/2)
        height_factor = 1.0 - np.sin(transition_t) 
        sit_height = 0.6 
        
    # Posiciones de base (modo estático o Caminar por defecto)
    joints = {
        # La altura se modula con height_factor para Sentarse y jump para Saltar
        "head": [0, 1.8 + 0.1*np.sin(t*2) * height_factor + jump, 0],
        "neck": [0, 1.6 + jump, 0],
        "shoulder_L": [-0.3, 1.6 + jump, sway * height_factor],
        "shoulder_R": [0.3, 1.6 + jump, -sway * height_factor],
        "hand_L": [-0.3, 1.2, sway],
        "hand_R": [0.3, 1.2, -sway],
        "hip_L": [-0.2, 1.0 + jump, 0],
        "hip_R": [0.2, 1.0 + jump, 0],
        "foot_L": [-0.2, 0.4, 0],
        "foot_R": [0.2, 0.4, 0]
    }

    # Aplicar movimientos de modo
    if mode == "Caminar":
        joints["hand_L"][1] = 1.2 - 0.3*step
        joints["hand_R"][1] = 1.2 + 0.3*step
        joints["foot_L"][1] = 0.4 + 0.3*step
        joints["foot_R"][1] = 0.4 - 0.3*step
    
    elif mode == "Correr":
        # Altura general y rebote
        for joint in joints.values():
            joint[1] += height_bounce # Rebote vertical
        
        # Brazos con mayor swing
        joints["hand_L"][1] = 1.2 + arm_swing
        joints["hand_R"][1] = 1.2 - arm_swing
        
        # Pies: Movimiento Vertical (Y) y Zancada Horizontal (Z)
        # Eje Y: Pies se levantan más al correr (con np.abs)
        joints["foot_L"][1] = 0.4 + np.abs(step_run) * 0.4
        joints["foot_R"][1] = 0.4 + np.abs(-step_run) * 0.4
        
        # Eje Z: Movimiento de atrás a adelante.
        # Una pierna va hacia adelante (+0.5) cuando la otra va hacia atrás (-0.5).
        joints["foot_L"][2] = step_run * 0.5  # Adelante/Atrás
        joints["foot_R"][2] = -step_run * 0.5 # Opuesto

    elif mode == "Bailar":
        # Movimiento rítmico de cadera y balanceo de brazos
        hip_swing = np.sin(t * 3) * 0.15
        joints["hip_L"][0] = -0.2 + hip_swing
        joints["hip_R"][0] = 0.2 + hip_swing
        
        # Brazos en alto y moviéndose
        joints["hand_L"][1] = 1.6 + np.sin(t * 2) * 0.3
        joints["hand_L"][0] = -0.3 + np.cos(t * 2) * 0.1
        joints["hand_R"][1] = 1.6 - np.sin(t * 2) * 0.3
        joints["hand_R"][0] = 0.3 - np.cos(t * 2) * 0.1
        
    elif mode == "Sentarse":
        # Aplicamos la transición de altura a las partes superiores del cuerpo
        for joint_name in ["head", "neck", "shoulder_L", "shoulder_R", "hip_L", "hip_R"]:
            joints[joint_name][1] = joints[joint_name][1] - (1.0 - height_factor) * sit_height
        
        # Ajustamos los brazos (simplificado)
        joints["hand_L"][1] = 1.2 - (1.0 - height_factor) * sit_height + 0.1
        joints["hand_R"][1] = 1.2 - (1.0 - height_factor) * sit_height + 0.1
        
        # Las rodillas se doblan para simular el sentado (llevamos los pies hacia atrás)
        joints["foot_L"][1] = 0.4 + (1.0 - height_factor) * 0.1
        joints["foot_L"][2] = 0.0 + (1.0 - height_factor) * 0.3
        joints["foot_R"][1] = 0.4 + (1.0 - height_factor) * 0.1
        joints["foot_R"][2] = 0.0 + (1.0 - height_factor) * 0.3

    # Si está en modo “Girar brazos”
    if mode == "Girar brazos":
        angle = np.sin(t) * np.pi / 3
        joints["hand_L"][1] = 1.6 + np.cos(angle) * 0.4
        joints["hand_L"][0] = -0.3 - np.sin(angle) * 0.4
        joints["hand_R"][1] = 1.6 + np.cos(angle) * 0.4
        joints["hand_R"][0] = 0.3 + np.sin(angle) * 0.4
    
    return joints

# --- 2. Conexiones---
connections = [
    ("head", "neck"),
    ("neck", "shoulder_L"), ("neck", "shoulder_R"),
    ("shoulder_L", "hand_L"), ("shoulder_R", "hand_R"),
    ("neck", "hip_L"), ("neck", "hip_R"),
    ("hip_L", "foot_L"), ("hip_R", "foot_R")
]

# --- 3. Función de animación ---
def run_mocap(speed=1.0, mode="Caminar"):
    fig = plt.figure(figsize=(7,7))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_xlim(-1, 1)
    ax.set_ylim(0, 2)
    ax.set_zlim(-1, 1)
    ax.set_title(f"Simulación de Motion Capture ({mode})")

    lines = []
    for _ in connections:
        line, = ax.plot([], [], [], 'o-', lw=3)
        lines.append(line)

    def update(frame):
        t = frame / (5/speed)
        joints = skeleton_points(t, mode)
        for i, (a, b) in enumerate(connections):
            x = [joints[a][0], joints[b][0]]
            y = [joints[a][1], joints[b][1]]
            z = [joints[a][2], joints[b][2]]
            lines[i].set_data(x, y)
            lines[i].set_3d_properties(z)
        return lines

    ani = FuncAnimation(fig, update, frames=np.linspace(0, 20, 200), interval=50, blit=False)
    plt.show()

# --- 4. Programa principal ---
if __name__ == "__main__":
    print("=== Simulación de Motion Capture ===")
    print("Modos disponibles: Caminar, Saltar, Girar brazos, Correr, Bailar, Sentarse")
    mode = input("Selecciona el modo de movimiento: ").capitalize()
    
    valid_modes = ["Caminar", "Saltar", "Girar brazos", "Correr", "Bailar", "Sentarse"]
    
    if mode not in valid_modes:
        print("Modo no válido. Se usará 'Caminar'.")
        mode = "Caminar"

    try:
        speed = float(input("Velocidad (1.0 por defecto): ") or 1.0)
    except ValueError:
        speed = 1.0

    run_mocap(speed=speed, mode=mode)

