# Gerardo Mercado Hurtado
# Raúl Martínez Martínez 
#figuras tipo anime
#Importamos las librerias necesarias
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection 

def piramide_cel_shaded_completa():
    # Crear la figura 3D
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    print("Creando PIRÁMIDE 3D COMPLETA con efecto Cel-Shaded")
    
    # 1. DEFINIR LOS VÉRTICES DE LA PIRÁMIDE (base cuadrada, 4 vértices; ápice, 1 vértice)
    vertices = np.array([
        # Base (en z = -1)
        [-1, -1, -1],  # V0: inferior izquierda frontal
        [ 1, -1, -1],  # V1: inferior derecha frontal   
        [ 1,  1, -1],  # V2: superior derecha frontal
        [-1,  1, -1],  # V3: superior izquierda frontal
        
        # Ápice (en z = 1)
        [ 0,  0,  1]   # V4: Ápice central
    ])
    
    # 2. DEFINIR LAS 5 CARAS DE LA PIRÁMIDE (1 base, 4 laterales)
    caras = [
        [0, 1, 2, 3],  # Base cuadrada
        [0, 1, 4],     # Cara lateral 1 (triangular)
        [1, 2, 4],     # Cara lateral 2 (triangular)
        [2, 3, 4],     # Cara lateral 3 (triangular)
        [3, 0, 4]      # Cara lateral 4 (triangular)
    ]
    
    # 3. COLORES CEL-SHADED para la pirámide negra
    color_base_negro = [0.1, 0.1, 0.1]    # Negro oscuro
    color_sombra_negro = [0.0, 0.0, 0.0]  # Negro más oscuro
    color_contorno = [1.0, 1.0, 1.0]      # Blanco para el contorno sobre negro
    
    # 4. DIRECCIÓN DE LA LUZ
    direccion_luz = np.array([1, 1, 1])  # Luz desde arriba-derecha-delante
    direccion_luz = direccion_luz / np.linalg.norm(direccion_luz)
    
    # 5. CALCULAR NORMALES Y COLORES PARA CADA CARA
    print("Calculando iluminación Cel-Shaded ")
    
    colores_caras = []
    
    for i, cara in enumerate(caras):
        # Calcular normal usando los primeros 3 vértices
        v0, v1, v2 = vertices[cara[0]], vertices[cara[1]], vertices[cara[2]]
        edge1 = v1 - v0
        edge2 = v2 - v0
        normal = np.cross(edge1, edge2)
        normal = normal / np.linalg.norm(normal)
        
        # Ajustar la normal si apunta hacia adentro (común en caras triangulares)
        if normal[2] < 0 and i != 0: 
             normal = -normal 
        elif normal[2] > 0 and i == 0: 
             normal = -normal 

        # Aplicar Cel-Shading (umbral fijo)
        intensidad = np.dot(normal, direccion_luz)
        color_cara = color_base_negro if intensidad > 0.3 else color_sombra_negro
        colores_caras.append(color_cara)
        
        print(f"Cara {i}: Intensidad = {intensidad:.2f}, Color = {'Claro' if intensidad > 0.3 else 'Oscuro'}")
    
    # 6. DIBUJAR CONTORNOS (OUTLINES)
    print(" Dibujando contornos blancos...")
    
    vertices_contorno = vertices * 1.03  # Ligeramente más grande para el contorno
    
    # Definir todas las aristas de la pirámide
    aristas = [
        [0, 1], [1, 2], [2, 3], [3, 0], # Aristas de la base
        [0, 4], [1, 4], [2, 4], [3, 4]  # Aristas que van al ápice
    ]
    
    for arista in aristas:
        v0, v1 = vertices_contorno[arista[0]], vertices_contorno[arista[1]]
        ax.plot([v0[0], v1[0]], [v0[1], v1[1]], [v0[2], v1[2]], 
                color=color_contorno, linewidth=3, zorder=10)
    
    # 7. DIBUJAR TODAS LAS CARAS DE LA PIRÁMIDE
    print(" Dibujando las 5 caras de la pirámide...")
    
    for i, cara_indices in enumerate(caras):
        face_verts = vertices[cara_indices]
        
        if len(cara_indices) == 4: # Cara de la base (cuadrada)
            x = np.array([[face_verts[0][0], face_verts[1][0]], 
                          [face_verts[3][0], face_verts[2][0]]])
            y = np.array([[face_verts[0][1], face_verts[1][1]], 
                          [face_verts[3][1], face_verts[2][1]]])
            z = np.array([[face_verts[0][2], face_verts[1][2]], 
                          [face_verts[3][2], face_verts[2][2]]])
            ax.plot_surface(x, y, z, 
                            color=colores_caras[i],
                            alpha=0.9,
                            shade=False,
                            edgecolor='none',
                            zorder=5)
        elif len(cara_indices) == 3: # Caras laterales (triangulares)
            # Ahora Poly3DCollection está definida gracias a la importación superior
            tri = Poly3DCollection([face_verts], alpha=0.9) 
            tri.set_facecolor(colores_caras[i])
            tri.set_edgecolor('none') 
            ax.add_collection3d(tri)
            
        print(f"   - Cara {i} dibujada: {'Base' if len(cara_indices) == 4 else 'Lateral'}")
    
    # 8. CONFIGURACIÓN FINAL
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    
    ax.view_init(elev=20, azim=45)
    
    ax.set_title('PIRÁMIDE 3D NEGRA con EFECTO CEL-SHADED', 
                 fontsize=16, fontweight='bold', pad=20)
    
    ax.set_facecolor([0.9, 0.95, 1.0])
    ax.set_axis_off()
    
    info_text = """ EFECTO CEL-SHADED:
• PIRÁMIDE TRIANGULAR NEGRA
• Colores PLANOS
• Contornos BLANCOS
• Sin degradados
• Estilo ANIME"""
    
    ax.text(-1.8, -1.8, -1.5, info_text, 
            fontsize=11, 
            bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.8),
            zorder=20)
    
    print(" ¡Pirámide COMPLETA creada exitosamente!")
    
    plt.tight_layout()
    plt.show()

# VERSIÓN ALTERNATIVA CON MÉTODO DIFERENTE
def piramide_con_poly3dcollection():
    """Versión usando Poly3DCollection (más robusta para pirámides)"""
    # NO NECESITA la importación aquí porque ya se hizo arriba
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    print("Creando pirámide")
    
    # Definir vértices
    vertices = np.array([
        [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1], # Base
        [ 0,  0,  1]                                        # Ápice
    ])
    
    # Definir caras como polígonos de 3 o 4 vértices
    caras_poly = [
        [vertices[0], vertices[1], vertices[2], vertices[3]],  # Base
        [vertices[0], vertices[1], vertices[4]],              # Cara lateral 1
        [vertices[1], vertices[2], vertices[4]],              # Cara lateral 2
        [vertices[2], vertices[3], vertices[4]],              # Cara lateral 3
        [vertices[3], vertices[0], vertices[4]]               # Cara lateral 4
    ]
    
    # Colores Cel-Shaded para la pirámide violeta
    colores_violeta = [
        [0.4, 0.0, 0.8],  # Base - violeta oscuro
        [0.6, 0.2, 1.0],  # Lateral 1 - violeta claro
        [0.5, 0.1, 0.9],  # Lateral 2 - violeta medio
        [0.7, 0.3, 1.0],  # Lateral 3 - violeta más claro
        [0.55, 0.15, 0.95] # Lateral 4 - violeta medio-claro
    ]
    
    # Crear colección de polígonos
    piramide = Poly3DCollection(caras_poly, alpha=0.9)
    piramide.set_facecolor(colores_violeta)
    piramide.set_edgecolor('black') 
    piramide.set_linewidth(3)
    
    ax.add_collection3d(piramide)
    
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.view_init(elev=20, azim=45)
    ax.set_facecolor([0.9, 0.95, 1.0])
    ax.set_axis_off()
    ax.set_title('PIRÁMIDE CEL-SHADED VIOLETA', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.show()

# EJECUTAR
if __name__ == "__main__":
    print("Elige el método:")
    print("1. Pirámide negra completa con plot_surface ")
    print("2. Pirámide violeta con Poly3DCollection ")
    
    opcion = input("Ingresa 1 o 2: ").strip()
    
    if opcion == "1":
        piramide_cel_shaded_completa()
    else:
        piramide_con_poly3dcollection()


