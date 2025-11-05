# Gerardo Mercado Hurtado
# Raúl Martínez Martínez 
#importamos librerias
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math

class HumanoideSimple:
    def __init__(self):
        self.fig = plt.figure(figsize=(12, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.num_frames = 100

        # Estructura del esqueleto (articulaciones)
        self.articulaciones_base = {
            'cadera': [0, 0, 0],
            'muslo_izq': [0, 0.5, 0],
            'rodilla_izq': [0, 1.0, 0],
            'tobillo_izq': [0, 1.5, 0],
            'muslo_der': [0, -0.5, 0],
            'rodilla_der': [0, -1.0, 0],
            'tobillo_der': [0, -1.5, 0],
            'cintura': [0, 0, 1],
            'pecho': [0, 0, 2],
            'cuello': [0, 0, 2.5],
            'cabeza': [0, 0, 3],
            'hombro_izq': [0.5, 0, 2],
            'codo_izq': [1.0, 0, 2],
            'mano_izq': [1.5, 0, 2],
            'hombro_der': [-0.5, 0, 2],
            'codo_der': [-1.0, 0, 2],
            'mano_der': [-1.5, 0, 2],
        }

        # Conexiones (huesos)
        self.huesos_base = [
            ('cadera', 'muslo_izq'), ('muslo_izq', 'rodilla_izq'), ('rodilla_izq', 'tobillo_izq'),
            ('cadera', 'muslo_der'), ('muslo_der', 'rodilla_der'), ('rodilla_der', 'tobillo_der'),
            ('cadera', 'cintura'), ('cintura', 'pecho'), ('pecho', 'cuello'), ('cuello', 'cabeza'),
            ('pecho', 'hombro_izq'), ('hombro_izq', 'codo_izq'), ('codo_izq', 'mano_izq'),
            ('pecho', 'hombro_der'), ('hombro_der', 'codo_der'), ('codo_der', 'mano_der'),
        ]

    def rotar_punto(self, punto, eje, angulo, origen=[0, 0, 0]):
        """Rotación 3D alrededor de un eje dado (punto como lista o array) relativo a un origen."""
        # Trasladar el punto para que el origen sea el centro de rotación
        p_rel = [punto[i] - origen[i] for i in range(3)]
        x, y, z = p_rel

        if eje == 'x':
            y_rot = y * math.cos(angulo) - z * math.sin(angulo)
            z_rot = y * math.sin(angulo) + z * math.cos(angulo)
            return [x + origen[0], y_rot + origen[1], z_rot + origen[2]]
        elif eje == 'y':
            x_rot = x * math.cos(angulo) + z * math.sin(angulo)
            z_rot = -x * math.sin(angulo) + z * math.cos(angulo)
            return [x_rot + origen[0], y + origen[1], z_rot + origen[2]]
        elif eje == 'z':
            x_rot = x * math.cos(angulo) - y * math.sin(angulo)
            y_rot = x * math.sin(angulo) + y * math.cos(angulo)
            return [x_rot + origen[0], y_rot + origen[1], z + origen[2]]
        return punto # Si el eje no es válido, no hay rotación

    def generar_humanoide(self, frame, offset_x, color, tiene_dedos_pies=False, tiene_dedos_manos=False):
        angulo = math.sin(frame * 2 * math.pi / self.num_frames) * (math.pi / 6)

        articulaciones_mod = {k: [v[0] + offset_x, v[1], v[2]] for k, v in self.articulaciones_base.items()}

        # Movimiento brazos (rotación alrededor del eje Z local del hombro/pecho)
        # Se rota alrededor del punto del hombro
        hombro_izq_pos = articulaciones_mod['hombro_izq']
        articulaciones_mod['codo_izq'] = self.rotar_punto([1.0 + offset_x, 0, 2], 'z', angulo, origen=hombro_izq_pos)
        articulaciones_mod['mano_izq'] = self.rotar_punto([1.5 + offset_x, 0, 2], 'z', angulo, origen=hombro_izq_pos)

        hombro_der_pos = articulaciones_mod['hombro_der']
        articulaciones_mod['codo_der'] = self.rotar_punto([-1.0 + offset_x, 0, 2], 'z', -angulo, origen=hombro_der_pos)
        articulaciones_mod['mano_der'] = self.rotar_punto([-1.5 + offset_x, 0, 2], 'z', -angulo, origen=hombro_der_pos)

        # Movimiento piernas (rotación alrededor del eje Y local de la cadera)
        # Se rota alrededor del punto de la cadera
        cadera_pos = articulaciones_mod['cadera']
        articulaciones_mod['rodilla_izq'] = self.rotar_punto([0 + offset_x, 1.0, 0], 'y', angulo, origen=cadera_pos)
        articulaciones_mod['tobillo_izq'] = self.rotar_punto([0 + offset_x, 1.5, 0], 'y', angulo, origen=cadera_pos)
        articulaciones_mod['rodilla_der'] = self.rotar_punto([0 + offset_x, -1.0, 0], 'y', -angulo, origen=cadera_pos)
        articulaciones_mod['tobillo_der'] = self.rotar_punto([0 + offset_x, -1.5, 0], 'y', -angulo, origen=cadera_pos)

        huesos_actuales = list(self.huesos_base) # Copiar la lista base

        # Agregar dedos a los pies
        if tiene_dedos_pies:
            tobillo_izq_pos = articulaciones_mod['tobillo_izq']
            articulaciones_mod['dedo_izq_1'] = [tobillo_izq_pos[0] + 0.1, tobillo_izq_pos[1], tobillo_izq_pos[2] - 0.2]
            articulaciones_mod['dedo_izq_2'] = [tobillo_izq_pos[0] - 0.1, tobillo_izq_pos[1], tobillo_izq_pos[2] - 0.2]
            huesos_actuales.append(('tobillo_izq', 'dedo_izq_1'))
            huesos_actuales.append(('tobillo_izq', 'dedo_izq_2'))

            tobillo_der_pos = articulaciones_mod['tobillo_der']
            articulaciones_mod['dedo_der_1'] = [tobillo_der_pos[0] + 0.1, tobillo_der_pos[1], tobillo_der_pos[2] - 0.2]
            articulaciones_mod['dedo_der_2'] = [tobillo_der_pos[0] - 0.1, tobillo_der_pos[1], tobillo_der_pos[2] - 0.2]
            huesos_actuales.append(('tobillo_der', 'dedo_der_1'))
            huesos_actuales.append(('tobillo_der', 'dedo_der_2'))

        # Agregar dedos a las manos
        if tiene_dedos_manos:
            mano_izq_pos = articulaciones_mod['mano_izq']
            articulaciones_mod['dedo_mano_izq_1'] = [mano_izq_pos[0] + 0.1, mano_izq_pos[1], mano_izq_pos[2] - 0.2]
            articulaciones_mod['dedo_mano_izq_2'] = [mano_izq_pos[0] + 0.1, mano_izq_pos[1], mano_izq_pos[2] + 0.2]
            huesos_actuales.append(('mano_izq', 'dedo_mano_izq_1'))
            huesos_actuales.append(('mano_izq', 'dedo_mano_izq_2'))

            mano_der_pos = articulaciones_mod['mano_der']
            articulaciones_mod['dedo_mano_der_1'] = [mano_der_pos[0] - 0.1, mano_der_pos[1], mano_der_pos[2] - 0.2]
            articulaciones_mod['dedo_mano_der_2'] = [mano_der_pos[0] - 0.1, mano_der_pos[1], mano_der_pos[2] + 0.2]
            huesos_actuales.append(('mano_der', 'dedo_mano_der_1'))
            huesos_actuales.append(('mano_der', 'dedo_mano_der_2'))

        # Dibujar huesos
        for h1, h2 in huesos_actuales:
            p1 = articulaciones_mod[h1]
            p2 = articulaciones_mod[h2]
            x = [p1[0], p2[0]]
            y = [p1[1], p2[1]]
            z = [p1[2], p2[2]]
            self.ax.plot(x, y, z, color=color, linewidth=2, markersize=4, marker='o')


    def actualizar(self, frame):
        """Actualiza las posiciones de los humanoides en cada cuadro."""
        self.ax.cla()

        # Humanoide azul (original)
        self.generar_humanoide(frame, 0, 'blue')
        # Humanoide amarillo (con dedos en los pies)
        self.generar_humanoide(frame, 2, 'yellow', tiene_dedos_pies=True)
        # Humanoide rojo (con dedos en las manos)
        self.generar_humanoide(frame, 4, 'red', tiene_dedos_manos=True)

        # Configuración de la vista
        self.ax.set_xlim(-1, 6)
        self.ax.set_ylim(-2, 2)
        self.ax.set_zlim(0, 3.5)
        self.ax.set_title("Animación de Humanoides (Stick Figures)")
        
        # Rotamos la cámara lentamente para que se vea mejor la caminata
        elev = 20
        azim = (frame / self.num_frames) * 360 + 45 # Añadir un offset para que se vea mejor al inicio
        self.ax.view_init(elev=elev, azim=azim)
        self.ax.set_axis_off()

    def animar(self):
        """Ejecuta la animación."""
        anim = FuncAnimation(self.fig, self.actualizar, frames=self.num_frames, interval=100, repeat=True)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    humanoide = HumanoideSimple()
    humanoide.animar()

