import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# ======================
# FUNCIONES DE HUMANOIDES
# ======================
def crear_humanoide(x_offset=0, z_offset=0, escala=1.0):
    joints = {
        "head": np.array([x_offset, 2.0 * escala, z_offset]),
        "body_top": np.array([x_offset, 1.5 * escala, z_offset]),
        "body_bottom": np.array([x_offset, 0.7 * escala, z_offset]),
        "hand_L": np.array([x_offset - 0.4 * escala, 1.4 * escala, z_offset]),
        "hand_R": np.array([x_offset + 0.4 * escala, 1.4 * escala, z_offset]),
        "leg_L": np.array([x_offset - 0.2 * escala, 0, z_offset]),
        "leg_R": np.array([x_offset + 0.2 * escala, 0, z_offset]),
    }
    return joints


def dibujar_humanoide(ax, joints, color='gray', cabeza_color='white'):
    # Cuerpo
    ax.plot([joints["head"][0], joints["body_top"][0]],
            [joints["head"][1], joints["body_top"][1]],
            [joints["head"][2], joints["body_top"][2]], color=color, lw=3) # Cabeza más gruesa
    ax.plot([joints["body_top"][0], joints["body_bottom"][0]],
            [joints["body_top"][1], joints["body_bottom"][1]],
            [joints["body_top"][2], joints["body_bottom"][2]], color=color, lw=4) # Cuerpo más grueso
    # Brazos
    ax.plot([joints["body_top"][0], joints["hand_L"][0]],
            [joints["body_top"][1], joints["hand_L"][1]],
            [joints["body_top"][2], joints["hand_L"][2]], color=color, lw=3)
    ax.plot([joints["body_top"][0], joints["hand_R"][0]],
            [joints["body_top"][1], joints["hand_R"][1]],
            [joints["body_top"][2], joints["hand_R"][2]], color=color, lw=3)
    # Piernas
    ax.plot([joints["body_bottom"][0], joints["leg_L"][0]],
            [joints["body_bottom"][1], joints["leg_L"][1]],
            [joints["body_bottom"][2], joints["leg_L"][2]], color=color, lw=3)
    ax.plot([joints["body_bottom"][0], joints["leg_R"][0]],
            [joints["body_bottom"][1], joints["leg_R"][1]],
            [joints["body_bottom"][2], joints["leg_R"][2]], color=color, lw=3)
    # Cabeza circular (con un 'tornillo' o detalle)
    ax.scatter(joints["head"][0], joints["head"][1], joints["head"][2],
               color=cabeza_color, s=350, edgecolor='black', lw=0.5, depthshade=False)

# ======================
# ANIMACIÓN PRINCIPAL
# ======================
def actualizar(frame):
    ax.clear()
    ax.set_xlim(-4, 4)
    ax.set_ylim(0, 3)
    ax.set_zlim(-2, 2)
    ax.set_title(" Frankenstein: Persecución Ártica ", fontsize=14, color='darkblue')
    ax.set_facecolor("aliceblue") # Fondo de nieve/hielo
    plt.axis('off')

    # Fondo de Nieve (puntos blancos y azules claros)
    np.random.seed(1)
    snow_x = np.random.uniform(-4, 4, 100)
    snow_y = np.random.uniform(0, 3, 100)
    snow_z = np.random.uniform(-2, 2, 100)
    ax.scatter(snow_x, snow_y, snow_z, color='white', s=8, alpha=0.9, zorder=0)
    
    # Simulación de témpanos de hielo (superficie irregular)
    ice_x = np.linspace(-4, 4, 10)
    ice_z = np.linspace(-2, 2, 10)
    X, Z = np.meshgrid(ice_x, ice_z)
    Y = 0.1 * np.sin(X * 3 + frame * 0.05) + 0.1 * np.cos(Z * 2) # Superficie irregular
    ax.plot_surface(X, Y, Z, color='lightcyan', alpha=0.5, zorder=1)


    # Movimiento de Persecución
    t = frame * 0.1
    avance_criatura = np.sin(t) * 1.5 - 0.5 # Avance lento e implacable
    avance_victor = np.sin(t * 1.5) * 1.0 # Movimiento más errático y rápido, luego se detiene

    # Colapso final de Victor
    colapso = 0
    if frame > 120:
        # Victor se detiene y cae por el frío/agotamiento
        colapso = (frame - 120) * 0.03
        avance_victor = avance_victor * (1.0 - (frame - 120) * 0.008) # Disminuye el avance


    # 1. La Criatura (Frankenstein)
    # Es más grande (escala=1.2)
    h1 = crear_humanoide(2 - avance_criatura, z_offset=0.2, escala=1.2)
    h1["head"][2] += np.cos(t * 0.5) * 0.1 # Cabeza pesada
    h1["hand_L"][1] += 0.5 # Brazos levantados, buscando a Victor
    h1["hand_R"][1] += 0.5
    h1["leg_L"][0] += np.sin(t * 2) * 0.1
    h1["leg_R"][0] -= np.sin(t * 2) * 0.1
    
    # 2. Victor Frankenstein
    # Es más pequeño y se mueve rápido
    h2 = crear_humanoide(-2 + avance_victor, z_offset=-0.2, escala=0.9)
    # Aplicar Colapso
    h2["head"][1] -= colapso
    h2["body_top"][1] -= colapso * 0.8
    h2["body_bottom"][1] -= colapso * 0.6
    
    # Movimiento de brazos (defensa/huida)
    if frame < 120:
        h2["hand_R"][0] += np.cos(t * 3) * 0.2
        h2["hand_R"][1] += np.sin(t * 3) * 0.2
        h2["hand_L"][1] += np.sin(t * 2) * 0.1
        h2["leg_L"][0] -= np.cos(t * 4) * 0.15
        h2["leg_R"][0] += np.cos(t * 4) * 0.15


    # Dibujar humanoides
    dibujar_humanoide(ax, h1, color='darkgreen', cabeza_color='lime') # Criatura (verde)
    dibujar_humanoide(ax, h2, color='darkslategray', cabeza_color='navy') # Victor (oscuro)

    # Objeto de Victor (palo/antorcha)
    # Se añade solo si no está colapsando
    if frame < 120:
        ax.plot(
            [h2["hand_R"][0], h2["hand_R"][0] + 0.6],
            [h2["hand_R"][1], h2["hand_R"][1] + 0.2],
            [h2["hand_R"][2], h2["hand_R"][2]],
            color='saddlebrown', lw=3
        )


    # Confrontación
    distancia = np.linalg.norm(h1["body_top"] - h2["body_top"])
    
    # Texto de drama
    if distancia < 1.0 and frame < 120:
        ax.text(0, 2.5, 0, "¡Persecución y Desesperación!", color='firebrick', fontsize=12, ha='center')

    # Texto final
    if frame > 160:
        # La Criatura se inclina sobre Victor
        h1["head"][1] -= 0.1
        ax.text(0, 2.7, 0, " El Creador yace vencido. ", color='darkblue', fontsize=16, ha='center')
        ax.text(0, 0.5, 0, " La Criatura desaparece en la bruma polar. ", color='darkgreen', fontsize=12, ha='center')


# ======================
# CONFIGURACIÓN INICIAL
# ======================
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
plt.axis('off')
ax.set_facecolor("aliceblue") # Fondo blanco-azulado

ani = FuncAnimation(fig, actualizar, frames=200, interval=90)
plt.show()
