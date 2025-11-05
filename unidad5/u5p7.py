# Gerardo Mercado Hurtado
# Raúl Martínez Martínez 
#Animación en 3D, animacion Morph.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class MorphOrtCuboOrt:
    def __init__(self, size_x_rect=2.0, size_y_rect=1.0, size_z_rect=1.0, size_cube=1.5, num_frames=120):
        self.size_x_rect = size_x_rect
        self.size_y_rect = size_y_rect
        self.size_z_rect = size_z_rect
        self.size_cube = size_cube
        self.num_frames = num_frames

        # Crear ortoedro inicial
        self.caras_3d, self.vertices_ortoedro = self.crear_ortoedro(self.size_x_rect, self.size_y_rect, self.size_z_rect)
        # Crear cubo intermedio
        self.caras_3d, self.vertices_cubo = self.crear_cubo_3d(self.size_cube)

        # Colores
        self.color_negro = [0.1, 0.1, 0.1]  # Negro
        self.color_violeta = [0.5, 0.2, 0.8]  # Violeta

        # Figura / ejes
        self.fig = plt.figure(figsize=(10, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')

    def crear_ortoedro(self, sx, sy, sz):
        # Vértices de un ortoedro (caja rectangular)
        # El centro estará en el origen (0,0,0)
        vertices = np.array([
            [-sx/2, -sy/2, -sz/2], # 0
            [ sx/2, -sy/2, -sz/2], # 1
            [ sx/2,  sy/2, -sz/2], # 2
            [-sx/2,  sy/2, -sz/2], # 3
            [-sx/2, -sy/2,  sz/2], # 4
            [ sx/2, -sy/2,  sz/2], # 5
            [ sx/2,  sy/2,  sz/2], # 6
            [-sx/2,  sy/2,  sz/2]  # 7
        ])

        # Caras como índices de los vértices
        caras = [
            [0, 1, 2, 3],  # Inferior
            [4, 5, 6, 7],  # Superior
            [0, 1, 5, 4],  # Frontal
            [3, 2, 6, 7],  # Trasera
            [0, 3, 7, 4],  # Izquierda
            [1, 2, 6, 5]   # Derecha
        ]
        return caras, vertices

    def crear_cubo_3d(self, s):
        # Un cubo es un caso especial de ortoedro con todos los lados iguales
        return self.crear_ortoedro(s, s, s)

    def interpolar_vertices(self, v_ini, v_fin, progreso):
        # Ambos arrays ya tienen la misma longitud (8 vértices, cada uno con 3 coords)
        return v_ini * (1.0 - progreso) + v_fin * progreso

    def interpolar_color(self, c1, c2, progreso):
        return [c1[i] * (1 - progreso) + c2[i] * progreso for i in range(3)]

    def dibujar_malla(self, caras, vertices, color):
        self.ax.cla()
        for cara in caras:
            pts = [vertices[idx] for idx in cara]
            poly = Poly3DCollection([pts], alpha=0.95)
            poly.set_facecolor(color)
            poly.set_edgecolor('k')
            poly.set_linewidth(1)
            self.ax.add_collection3d(poly)

        # Configuración de ejes/escala
        max_dim = max(self.size_x_rect, self.size_y_rect, self.size_z_rect, self.size_cube)
        espacio = max_dim * 1.5
        self.ax.set_xlim([-espacio/2, espacio/2])
        self.ax.set_ylim([-espacio/2, espacio/2])
        self.ax.set_zlim([-espacio/2, espacio/2])
        self.ax.set_box_aspect([1,1,1]) # Asegura que los ejes tengan la misma escala
        self.ax.set_axis_off()

    def animar(self):
        print("🔄 Iniciando morph: ORTOEDRO NEGRO → CUBO VIOLETA → ORTOEDRO NEGRO")
        fig = self.fig
        ax = self.ax
        
        caras = self.caras_3d # Las caras son las mismas para el ortoedro y el cubo
        
        v_ortoedro = self.vertices_ortoedro
        v_cubo = self.vertices_cubo

        def actualizar(frame):
            full_progreso = frame / float(self.num_frames - 1)
            t_smooth = full_progreso * full_progreso * (3 - 2 * full_progreso) # Smoothstep

            if full_progreso <= 0.5: # Primera mitad: Ortoedro a Cubo
                progreso_fase = t_smooth * 2 
                v_act = self.interpolar_vertices(v_ortoedro, v_cubo, progreso_fase)
                color = self.interpolar_color(self.color_negro, self.color_violeta, progreso_fase)
                titulo = f"Ortoedro → Cubo | Progreso: {progreso_fase*100:5.1f}%"
            else: # Segunda mitad: Cubo a Ortoedro
                progreso_fase = (t_smooth - 0.5) * 2 
                v_act = self.interpolar_vertices(v_cubo, v_ortoedro, progreso_fase)
                color = self.interpolar_color(self.color_violeta, self.color_negro, progreso_fase)
                titulo = f"Cubo → Ortoedro | Progreso: {progreso_fase*100:5.1f}%"
            
            self.dibujar_malla(caras, v_act, color)
            
            # Rotación para una mejor visualización del 3D
            elev = 20 # Ángulo de elevación fijo
            azim = frame * (360.0 / self.num_frames) * 2 # Rotación completa dos veces en el ciclo
            ax.view_init(elev=elev, azim=azim)
            
            ax.set_title(titulo, fontsize=12)

        anim = FuncAnimation(fig, actualizar, frames=self.num_frames, interval=50, repeat=True)
        plt.tight_layout()
        plt.show()
        print("✅ Animación finalizada.")

if __name__ == "__main__":
    # Definir dimensiones:
    # ortoedro_inicial: más largo en X, más bajo en Y, normal en Z
    morph = MorphOrtCuboOrt(size_x_rect=3.0, size_y_rect=1.0, size_z_rect=1.5, 
                            size_cube=2.0, num_frames=180) # Más frames para más suavidad
    morph.animar()


