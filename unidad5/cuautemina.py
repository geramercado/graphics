#importamos librerias
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math

class HumanoideSimple:
    def __init__(self):
        self.fig = plt.figure(figsize=(10, 7))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.num_frames = 1 # Un solo frame para la pose estática

        # Estructura del esqueleto (articulaciones base)
        # Se añaden articulaciones para la "muñeca" y los "dedos" de cada mano
        self.articulaciones_base = {
            'cadera': [0, 0, 0.2],  # Bajamos la cadera inicial
            'muslo_izq': [0, 0.25, 0],
            'rodilla_izq': [0, 0.5, 0],
            'tobillo_izq': [0, 0.75, 0],
            'pie_izq': [0, 0.75, 0], 
            'muslo_der': [0, -0.25, 0],
            'rodilla_der': [0, -0.5, 0],
            'tobillo_der': [0, -0.75, 0],
            'pie_der': [0, -0.75, 0], 
            'cintura': [0, 0, 0.7],
            'pecho': [0, 0, 1.2],
            'cuello': [0, 0, 1.7],
            'cabeza': [0, 0, 2.2],
            'hombro_izq': [0.5, 0, 1.2],
            'codo_izq': [1.0, 0, 1.2],
            'muñeca_izq': [1.5, 0, 1.2], # Nueva articulación
            'dedo1_izq': [1.6, 0.1, 1.2], # Deducción de dedos
            'dedo2_izq': [1.6, 0, 1.2],
            'dedo3_izq': [1.6, -0.1, 1.2],
            'hombro_der': [-0.5, 0, 1.2],
            'codo_der': [-1.0, 0, 1.2],
            'muñeca_der': [-1.5, 0, 1.2], # Nueva articulación
            'dedo1_der': [-1.6, 0.1, 1.2],
            'dedo2_der': [-1.6, 0, 1.2],
            'dedo3_der': [-1.6, -0.1, 1.2],
        }
        
        self.articulaciones = {k: list(v) for k, v in self.articulaciones_base.items()}

        # Conexiones (huesos) - Añadimos muñecas y dedos
        self.huesos = [
            ('cadera', 'muslo_izq'), ('muslo_izq', 'rodilla_izq'), ('rodilla_izq', 'tobillo_izq'), ('tobillo_izq', 'pie_izq'), 
            ('cadera', 'muslo_der'), ('muslo_der', 'rodilla_der'), ('rodilla_der', 'tobillo_der'), ('tobillo_der', 'pie_der'), 
            ('cadera', 'cintura'), ('cintura', 'pecho'), ('pecho', 'cuello'), ('cuello', 'cabeza'),
            ('pecho', 'hombro_izq'), ('hombro_izq', 'codo_izq'), ('codo_izq', 'muñeca_izq'), # Hacia la muñeca
            ('muñeca_izq', 'dedo1_izq'), ('muñeca_izq', 'dedo2_izq'), ('muñeca_izq', 'dedo3_izq'), # Hacia los dedos
            ('pecho', 'hombro_der'), ('hombro_der', 'codo_der'), ('codo_der', 'muñeca_der'), # Hacia la muñeca
            ('muñeca_der', 'dedo1_der'), ('muñeca_der', 'dedo2_der'), ('muñeca_der', 'dedo3_der'), # Hacia los dedos
        ]

    def rotar_punto(self, punto, eje, angulo):
        """Rotación 3D (se mantiene aunque no se use para la pose estática)."""
        x, y, z = punto
        if eje == 'x':
            y2 = y * math.cos(angulo) - z * math.sin(angulo)
            z2 = y * math.sin(angulo) + z * math.cos(angulo)
            return [x, y2, z2]
        elif eje == 'y':
            x2 = x * math.cos(angulo) + z * math.sin(angulo)
            z2 = -x * math.sin(angulo) + z * math.cos(angulo)
            return [x2, y, z2]
        elif eje == 'z':
            x2 = x * math.cos(angulo) - y * math.sin(angulo)
            y2 = x * math.sin(angulo) + y * math.cos(angulo)
            return [x2, y2, z]
        return [x, y, z]

    def aplicar_pose_cuauhtemiña_arrodillado(self):
        """Aplica la pose de Cuauhtémoc Blanco arrodillado con mano derecha apuntando."""
        
        # --- Cadera y Tronco ---
        self.articulaciones['cadera'] = [0, 0, 0.3] 
        self.articulaciones['cintura'] = [0, 0, 0.8]
        self.articulaciones['pecho'] = [0, 0, 1.3]
        self.articulaciones['cuello'] = [0, 0, 1.8]
        self.articulaciones['cabeza'] = [0, 0, 2.3]

        # --- Pierna Derecha (arrodillada) ---
        self.articulaciones['muslo_der'] = [-0.2, -0.2, 0.1] 
        self.articulaciones['rodilla_der'] = [-0.4, -0.4, 0.0] 
        self.articulaciones['tobillo_der'] = [-0.6, -0.6, 0.0] 
        self.articulaciones['pie_der'] = [-0.7, -0.7, 0.0] 

        # --- Pierna Izquierda (flexionada con pie en el suelo) ---
        self.articulaciones['muslo_izq'] = [0.2, 0.2, 0.1]
        self.articulaciones['rodilla_izq'] = [0.4, 0.4, 0.5] 
        self.articulaciones['tobillo_izq'] = [0.6, 0.6, 0.0] 
        self.articulaciones['pie_izq'] = [0.7, 0.7, 0.0] 

        # --- Brazo Izquierdo (extendido y ligeramente levantado) ---
        self.articulaciones['hombro_izq'] = [0.4, 0.1, 1.4] 
        self.articulaciones['codo_izq'] = [1.0, 0.2, 1.5]
        self.articulaciones['muñeca_izq'] = [1.6, 0.3, 1.6]
        self.articulaciones['dedo1_izq'] = [1.7, 0.35, 1.7] # Dedos ligeramente abiertos
        self.articulaciones['dedo2_izq'] = [1.7, 0.3, 1.6]
        self.articulaciones['dedo3_izq'] = [1.7, 0.25, 1.5]
        
        # --- Brazo Derecho (doblado y apuntando) ---
        self.articulaciones['hombro_der'] = [-0.4, 0.1, 1.4]
        self.articulaciones['codo_der'] = [-1.0, 0.2, 1.0] # Codo más bajo y adelante
        self.articulaciones['muñeca_der'] = [-0.8, 0.3, 0.8] # Muñeca doblada
        self.articulaciones['dedo1_der'] = [-0.6, 0.4, 0.7] # Dedos apuntando
        self.articulaciones['dedo2_der'] = [-0.7, 0.3, 0.7]
        self.articulaciones['dedo3_der'] = [-0.8, 0.2, 0.7]


    def actualizar(self, frame):
        """Dibuja la pose estática."""
        self.ax.cla()
        
        self.aplicar_pose_cuauhtemiña_arrodillado()

        # Dibujar huesos y los puntos de articulación normales
        for h1, h2 in self.huesos:
            p1 = self.articulaciones[h1]
            p2 = self.articulaciones[h2]
            x = [p1[0], p2[0]]
            y = [p1[1], p2[1]]
            z = [p1[2], p2[2]]
            self.ax.plot(x, y, z, 'bo-', linewidth=3, markersize=6)
        
        # Resaltar las "manos" y "pies" con un marcador más grande
        # En este caso, la "muñeca" y el "pie" son los marcadores más grandes
        
        # Manos (marcadores en las muñecas)
        p_muñeca_izq = self.articulaciones['muñeca_izq']
        p_muñeca_der = self.articulaciones['muñeca_der']
        self.ax.plot(p_muñeca_izq[0], p_muñeca_izq[1], p_muñeca_izq[2], 'o', color='blue', markersize=12, markeredgecolor='black', markeredgewidth=1)
        self.ax.plot(p_muñeca_der[0], p_muñeca_der[1], p_muñeca_der[2], 'o', color='blue', markersize=12, markeredgecolor='black', markeredgewidth=1)

        # Pies
        p_pie_izq = self.articulaciones['pie_izq']
        p_pie_der = self.articulaciones['pie_der']
        self.ax.plot(p_pie_izq[0], p_pie_izq[1], p_pie_izq[2], 'o', color='blue', markersize=12, markeredgecolor='black', markeredgewidth=1)
        self.ax.plot(p_pie_der[0], p_pie_der[1], p_pie_der[2], 'o', color='blue', markersize=12, markeredgecolor='black', markeredgewidth=1)


        # Configuración de la vista
        self.ax.set_xlim(-2, 2)
        self.ax.set_ylim(-2, 2)
        self.ax.set_zlim(0, 2.5) 
        self.ax.set_title("Pose Cuauhtemiña (Arrodillado) con Mano Derecha Apuntando y Dedos ⚽")
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        
        elev = 15
        azim = -45 
        self.ax.view_init(elev=elev, azim=azim)
        self.ax.set_axis_off()

    def animar(self):
        """Ejecuta la animación (muestra la pose estática)."""
        anim = FuncAnimation(self.fig, self.actualizar, frames=self.num_frames, interval=100, repeat=False)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    humanoide = HumanoideSimple()
    humanoide.animar()