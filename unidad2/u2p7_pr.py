#fuentes, tamaños, colores, bitmap, estilos.
#Gerardo Mercado Hurtado
# Importar las librerías necesarias
import pygame  # Librería principal para crear juegos y aplicaciones gráficas
import numpy as np  # Para operaciones matemáticas 
import math  # Para funciones matemáticas (
from pygame import freetype  # Módulo específico para trabajar con fuentes y texto

# Inicializar Pygame - siempre necesario para usar sus funciones
pygame.init()
pygame.freetype.init()  # Inicializar específicamente el módulo de fuentes

# --- CONFIGURACIÓN ---
# Definir el tamaño de la ventana
ANCHO, ALTO = 1200, 800
# Crear la ventana principal con el tamaño definido
ventana = pygame.display.set_mode((ANCHO, ALTO))
# Poner título a la ventana
pygame.display.set_caption("Sistema de Fuentes y Texto - Visualizador Interactivo")
# Crear un reloj para controlar la velocidad de fotogramas
reloj = pygame.time.Clock()

# --- COLORES ---
# Definir colores usando valores RGB (Red, Green, Blue)
BLANCO = (255, 255, 255)      # Máximo de rojo, verde y azul
NEGRO = (0, 0, 0)             # Mínimo de rojo, verde y azul
AZUL = (59, 130, 246)         # Azul moderno
ROJO = (239, 68, 68)          # Rojo vibrante
VERDE = (34, 197, 94)         # Verde brillante
MORADO = (147, 112, 219)      # Morado suave
AMARILLO = (255, 193, 7)      # Amarillo dorado
NARANJA = (255, 159, 64)      # Naranja cálido
GRIS = (200, 200, 200)        # Gris claro
FONDO = (25, 35, 45)          # Fondo oscuro azulado para buen contraste

# --- FUENTES DISPONIBLES ---
# Lista de fuentes del sistema que queremos cargar
fuentes_sistema = [
    "Arial", "Times New Roman", "Courier New", "Verdana", 
    "Georgia", "Comic Sans MS", "Impact", "Trebuchet MS"
]

cuento_contado = [
    "erase una vez", "un cuento que se", "contaba solo"
]

# Diccionario para guardar las fuentes cargadas
fuentes_cargadas = {}

# Intentar cargar cada fuente de la lista
for nombre_fuente in fuentes_sistema:
    try:
        # Intentar cargar la fuente con tamaño inicial 24
        fuentes_cargadas[nombre_fuente] = pygame.freetype.SysFont(nombre_fuente, 24)
    except:
        # Si hay error, mostrar mensaje (la fuente no está disponible)
        print(f"Fuente {nombre_fuente} no disponible")

# Si no se pudo cargar ninguna fuente del sistema, usar una por defecto
if not fuentes_cargadas:
    fuentes_cargadas["Default"] = pygame.freetype.Font(None, 24)

# --- CLASE PARA CREACIÓN DE FUENTES BITMAP ---
class FuenteBitmap:
    def __init__(self, tamaño=16):
        # Tamaño de cada carácter en píxeles
        self.tamaño = tamaño
        # Diccionario para guardar cada carácter dibujado
        self.caracteres = {}
        # Crear los caracteres básicos al iniciar
        self.crear_fuente_basica()
    
    def crear_fuente_basica(self):
        """Crea una fuente bitmap básica estilo 8-bit"""
        # Crear caracteres desde el espacio (32) hasta la tilde (126)
        for codigo in range(32, 127):
            char = chr(codigo)  # Convertir número a carácter
            self.caracteres[char] = self.crear_glyph(char)  # Crear y guardar el glifo
    
    def crear_glyph(self, caracter):
        """Crea un glyph bitmap para un caracter"""
        # Crear superficie transparente para el carácter
        surf = pygame.Surface((self.tamaño, self.tamaño), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 0))  # Rellenar con transparente
        
        # Dibujar diferentes caracteres (solo implementados algunos como ejemplo)
        if caracter == 'A':
            self.dibujar_A(surf)
        elif caracter == 'B':
            self.dibujar_B(surf)
        elif caracter == 'C':
            self.dibujar_C(surf)
        # Para otros caracteres no implementados, dibujar un cuadrado simple
        else:
            pygame.draw.rect(surf, BLANCO, (2, 2, self.tamaño-4, self.tamaño-4), 1)
        
        return surf
    
    def dibujar_A(self, surf):
        """Dibuja la letra A en bitmap usando píxeles individuales"""
        # Recorrer cada píxel de la superficie
        for y in range(self.tamaño):
            for x in range(self.tamaño):
                # Dibujar píxeles para formar la letra A
                if (y == 0 and 3 <= x <= self.tamaño-4) or \
                   (y == self.tamaño//2 and 3 <= x <= self.tamaño-4) or \
                   (x == 3 and y >= 0) or \
                   (x == self.tamaño-4 and y >= 0):
                    surf.set_at((x, y), BLANCO)  # Poner píxel blanco
    
    # Métodos similares para otras letras...
    def dibujar_B(self, surf):
        """Dibuja la letra B en bitmap"""
        for y in range(self.tamaño):
            for x in range(self.tamaño):
                if (x == 3) or \
                   (y == 0 and x <= self.tamaño-4) or \
                   (y == self.tamaño-1 and x <= self.tamaño-4) or \
                   (y == self.tamaño//2 and x <= self.tamaño-4) or \
                   (x == self.tamaño-4 and (y <= self.tamaño//2 or y >= self.tamaño//2)):
                    surf.set_at((x, y), BLANCO)
    
    def dibujar_C(self, surf):
        """Dibuja la letra C en bitmap"""
        for y in range(self.tamaño):
            for x in range(self.tamaño):
                if (x == 3 and y >= 3 and y <= self.tamaño-4) or \
                   (y == 3 and x >= 3) or \
                   (y == self.tamaño-4 and x >= 3):
                    surf.set_at((x, y), BLANCO)
    
    def renderizar_texto(self, texto, color=BLANCO):
        """Renderiza texto usando la fuente bitmap"""
        # Calcular el ancho total necesario
        ancho_total = len(texto) * self.tamaño
        # Crear superficie para todo el texto
        superficie = pygame.Surface((ancho_total, self.tamaño), pygame.SRCALPHA)
        superficie.fill((0, 0, 0, 0))  # Hacerla transparente
        
        # Dibujar cada carácter uno por uno
        for i, char in enumerate(texto):
            if char in self.caracteres:
                # Copiar el glifo del carácter
                glyph = self.caracteres[char].copy()
                # Cambiar el color del glifo
                for y in range(self.tamaño):
                    for x in range(self.tamaño):
                        if glyph.get_at((x, y))[0] > 0:  # Si el píxel no es negro
                            glyph.set_at((x, y), color)  # Cambiar al color deseado
                # Pegar el glifo en la posición correcta
                superficie.blit(glyph, (i * self.tamaño, 0))
        
        return superficie

# --- EFECTOS DE TEXTO AVANZADOS ---
class EfectosTexto:
    @staticmethod
    def texto_con_sombra(fuente, texto, tamaño, color_principal, color_sombra, offset=(2, 2)):
        """Renderiza texto con efecto de sombra"""
        # Renderizar el texto de la sombra y el principal por separado
        texto_sombra = fuente.render(texto, color_sombra, size=tamaño)
        texto_principal = fuente.render(texto, color_principal, size=tamaño)
        
        # Crear superficie más grande para acomodar la sombra
        surf = pygame.Surface((texto_principal[0].get_width() + abs(offset[0]), 
                              texto_principal[0].get_height() + abs(offset[1])), 
                             pygame.SRCALPHA)
        surf.fill((0, 0, 0, 0))  # Hacerla transparente
        
        # Dibujar primero la sombra, luego el texto principal
        surf.blit(texto_sombra[0], (max(0, offset[0]), max(0, offset[1])))
        surf.blit(texto_principal[0], (max(0, -offset[0]), max(0, -offset[1])))
        
        return surf
    
    @staticmethod
    def texto_con_borde(fuente, texto, tamaño, color_principal, color_borde, grosor=2):
        """Renderiza texto con borde"""
        texto_base = fuente.render(texto, color_borde, size=tamaño)
        texto_front = fuente.render(texto, color_principal, size=tamaño)
        
        # Crear superficie más grande para el borde
        surf = pygame.Surface((texto_base[0].get_width() + grosor * 2, 
                              texto_base[0].get_height() + grosor * 2), 
                             pygame.SRCALPHA)
        surf.fill((0, 0, 0, 0))
        
        # Dibujar el borde en todas las direcciones alrededor del texto
        for dx in range(-grosor, grosor + 1):
            for dy in range(-grosor, grosor + 1):
                if dx != 0 or dy != 0:  # No dibujar en la posición central
                    surf.blit(texto_base[0], (grosor + dx, grosor + dy))
        
        # Dibujar el texto principal encima
        surf.blit(texto_front[0], (grosor, grosor))
        
        return surf
    
    @staticmethod
    def texto_degradado(fuente, texto, tamaño, color_inicio, color_fin):
        """Renderiza texto con efecto de degradado"""
        texto_render = fuente.render(texto, BLANCO, size=tamaño)
        surf_texto = texto_render[0]
        
        # Crear superficie para el degradado
        surf = pygame.Surface(surf_texto.get_size(), pygame.SRCALPHA)
        
        # Crear máscara del texto (saber dónde están los píxeles del texto)
        mascara = pygame.mask.from_surface(surf_texto)
        
        # Aplicar degradado línea por línea
        for y in range(surf.get_height()):
            # Calcular color interpolado para esta línea
            t = y / surf.get_height()  # Porcentaje de progreso (0 a 1)
            r = int(color_inicio[0] + (color_fin[0] - color_inicio[0]) * t)
            g = int(color_inicio[1] + (color_fin[1] - color_inicio[1]) * t)
            b = int(color_inicio[2] + (color_fin[2] - color_inicio[2]) * t)
            color_linea = (r, g, b)
            
            # Aplicar color solo a los píxeles del texto
            for x in range(surf.get_width()):
                if mascara.get_at((x, y)):  # Si este píxel pertenece al texto
                    surf.set_at((x, y), color_linea)
        
        return surf
    
    @staticmethod
    def texto_neumorfico(fuente, texto, tamaño, color_base, intensidad=10):
        """Efecto neumórfico moderno (claros y oscuros)"""
        # Calcular colores más claros y oscuros para el efecto 3D
        color_claro = (min(255, color_base[0] + intensidad), 
                      min(255, color_base[1] + intensidad), 
                      min(255, color_base[2] + intensidad))
        color_oscuro = (max(0, color_base[0] - intensidad), 
                       max(0, color_base[1] - intensidad), 
                       max(0, color_base[2] - intensidad))
        
        # Renderizar tres versiones del texto
        texto_claro = fuente.render(texto, color_claro, size=tamaño)
        texto_oscuro = fuente.render(texto, color_oscuro, size=tamaño)
        texto_principal = fuente.render(texto, color_base, size=tamaño)
        
        ancho, alto = texto_principal[0].get_size()
        surf = pygame.Surface((ancho + 4, alto + 4), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 0))
        
        # Dibujar sombras para crear efecto 3D
        surf.blit(texto_claro[0], (2, 2))  # Sombra clara abajo-derecha
        surf.blit(texto_oscuro[0], (-2, -2))  # Sombra oscura arriba-izquierda
        
        # Texto principal en el centro
        surf.blit(texto_principal[0], (2, 2))
        
        return surf

# --- CONFIGURACIÓN INICIAL ---
# Valores por defecto al iniciar el programa
fuente_actual = list(fuentes_cargadas.keys())[0] if fuentes_cargadas else "Default"
tamaño_fuente = 36
color_texto = BLANCO
color_secundario = MORADO
texto_ejemplo = "Python & Pygame"
efecto_actual = "normal"
fuente_bitmap = FuenteBitmap(16)  # Crear instancia de fuente bitmap
mostrar_bitmap = False  # Comenzar mostrando fuentes vectoriales

# --- BUCLE PRINCIPAL ---
ejecutando = True

while ejecutando:
    # Controlar velocidad: 60 FPS, dt = tiempo entre fotogramas en segundos
    dt = reloj.tick(60) / 1000.0
    
    # --- MANEJO DE EVENTOS ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False  # Salir del bucle si cierran la ventana
        
        elif evento.type == pygame.KEYDOWN:
            # Tecla F - Cambiar fuente
            if evento.key == pygame.K_f:
                fuentes_disponibles = list(fuentes_cargadas.keys())
                indice_actual = fuentes_disponibles.index(fuente_actual)
                fuente_actual = fuentes_disponibles[(indice_actual + 1) % len(fuentes_disponibles)]
            
            # Teclas UP/DOWN - Cambiar tamaño de fuente
            elif evento.key == pygame.K_UP:
                tamaño_fuente = min(120, tamaño_fuente + 4)  # Límite máximo 120
            elif evento.key == pygame.K_DOWN:
                tamaño_fuente = max(8, tamaño_fuente - 4)  # Límite mínimo 8
            
            # Tecla E - Cambiar efecto de texto
            elif evento.key == pygame.K_e:
                efectos = ["normal", "sombra", "borde", "degradado", "neumorfico"]
                efecto_actual = efectos[(efectos.index(efecto_actual) + 1) % len(efectos)]
            
            # Tecla T - Cambiar texto de ejemplo
            elif evento.key == pygame.K_t:
                textos = [
                    "Python & Pygame",
                    "GrÁfIcOs CoMpUtAcIoNaLeS",
                    "Hello World!",
                    "1234567890",
                    "¡Tipografía!"
                ]
                texto_ejemplo = textos[(textos.index(texto_ejemplo) + 1) % len(textos)] if texto_ejemplo in textos else textos[0]
            
            # Tecla B - Alternar entre fuente bitmap y vectorial
            elif evento.key == pygame.K_b:
                mostrar_bitmap = not mostrar_bitmap
            
            # Tecla C - Cambiar color del texto
            elif evento.key == pygame.K_c:
                colores = [BLANCO, ROJO, VERDE, AZUL, MORADO, AMARILLO, NARANJA]
                color_texto = colores[(colores.index(color_texto) + 1) % len(colores)] if color_texto in colores else colores[0]
    
    # --- DIBUJADO ---
    ventana.fill(FONDO)  # Limpiar pantalla con color de fondo
    
    # Obtener el objeto de fuente actual
    fuente_obj = fuentes_cargadas[fuente_actual] if fuente_actual in fuentes_cargadas else list(fuentes_cargadas.values())[0]
    
    # --- RENDERIZAR TEXTO CON EFECTO SELECCIONADO ---
    if mostrar_bitmap:
        # Usar fuente bitmap personalizada
        texto_surf = fuente_bitmap.renderizar_texto(texto_ejemplo, color_texto)
        ventana.blit(texto_surf, (ANCHO//2 - texto_surf.get_width()//2, ALTO//2 - 50))
    
    else:
        # Usar efectos avanzados con fuentes del sistema
        if efecto_actual == "normal":
            texto_render = fuente_obj.render(texto_ejemplo, color_texto, size=tamaño_fuente)
            ventana.blit(texto_render[0], (ANCHO//2 - texto_render[0].get_width()//2, ALTO//2 - 50))
        
        elif efecto_actual == "sombra":
            texto_surf = EfectosTexto.texto_con_sombra(
                fuente_obj, texto_ejemplo, tamaño_fuente, color_texto, NEGRO, (2, 2)
            )
            ventana.blit(texto_surf, (ANCHO//2 - texto_surf.get_width()//2, ALTO//2 - 50))
        
        elif efecto_actual == "borde":
            texto_surf = EfectosTexto.texto_con_borde(
                fuente_obj, texto_ejemplo, tamaño_fuente, color_texto, NEGRO, 2
            )
            ventana.blit(texto_surf, (ANCHO//2 - texto_surf.get_width()//2, ALTO//2 - 50))
        
        elif efecto_actual == "degradado":
            texto_surf = EfectosTexto.texto_degradado(
                fuente_obj, texto_ejemplo, tamaño_fuente, color_texto, ROJO
            )
            ventana.blit(texto_surf, (ANCHO//2 - texto_surf.get_width()//2, ALTO//2 - 50))
        
        elif efecto_actual == "neumorfico":
            texto_surf = EfectosTexto.texto_neumorfico(
                fuente_obj, texto_ejemplo, tamaño_fuente, color_texto, 20
            )
            ventana.blit(texto_surf, (ANCHO//2 - texto_surf.get_width()//2, ALTO//2 - 50))
    
    # --- PANEL DE INFORMACIÓN ---
    y_pos = 50
    # Dibujar panel de información con fondo
    pygame.draw.rect(ventana, (40, 40, 50, 200), (20, 20, 400, 200), 0, 10)
    pygame.draw.rect(ventana, MORADO, (20, 20, 400, 200), 2, 10)
    
    # Textos informativos
    info_textos = [
        f"Fuente: {fuente_actual}",
        f"Tamaño: {tamaño_fuente}px",
        f"Efecto: {efecto_actual}",
        f"Modo: {'Bitmap' if mostrar_bitmap else 'Vectorial'}",
        "",
        "CONTROLES:",
        "F - Cambiar fuente",
        "↑↓ - Tamaño fuente",
        "E - Cambiar efecto",
        "T - Cambiar texto",
        "B - Alternar bitmap/vectorial",
        "C - Cambiar color"
    ]
    
    # Dibujar cada línea de información
    for i, texto in enumerate(info_textos):
        color = VERDE if i == 0 else (AMARILLO if i in [1, 2, 3] else BLANCO)
        surf = pygame.font.SysFont('Arial', 16).render(texto, True, color)
        ventana.blit(surf, (40, 40 + i * 22))
    
    # --- MUESTRA DE CARACTERES (solo en modo vectorial) ---
    if not mostrar_bitmap:
        y_chars = ALTO - 150
        # Panel para mostrar caracteres
        pygame.draw.rect(ventana, (40, 40, 50, 200), (20, y_chars, ANCHO - 40, 130), 0, 10)
        pygame.draw.rect(ventana, AZUL, (20, y_chars, ANCHO - 40, 130), 2, 10)
        
        # Mostrar alfabeto y números de ejemplo
        texto_muestra = "ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789 !@#$%^&*()"
        muestra_render = fuente_obj.render(texto_muestra, BLANCO, size=20)
        ventana.blit(muestra_render[0], (40, y_chars + 20))
        
        # Información técnica de la fuente
        info_fuente = f"Familia: {fuente_actual} | Estilo: Regular | Charset: Unicode"
        info_render = pygame.font.SysFont('Arial', 14).render(info_fuente, True, GRIS)
        ventana.blit(info_render, (40, y_chars + 60))
    
    # --- EJEMPLO DE KERNING (espaciado entre letras) ---
    if not mostrar_bitmap:
        x_kerning = ANCHO - 400
        y_kerning = 100
        
        # Panel para ejemplo de kerning
        pygame.draw.rect(ventana, (40, 40, 50, 200), (x_kerning, y_kerning, 380, 120), 0, 10)
        pygame.draw.rect(ventana, VERDE, (x_kerning, y_kerning, 380, 120), 2, 10)
        
        # Texto que muestra bien el kerning
        texto_kerning = "AVA TY W."
        kerning_render = fuente_obj.render(texto_kerning, AMARILLO, size=28)
        ventana.blit(kerning_render[0], (x_kerning + 20, y_kerning + 20))
        
        # Explicación del kerning
        kerning_info = "Ejemplo de kerning (espaciado entre letras)"
        info_render = pygame.font.SysFont('Arial', 14).render(kerning_info, True, GRIS)
        ventana.blit(info_render, (x_kerning + 20, y_kerning + 70))
    
    # --- PIE DE PÁGINA ---
    footer = "Sistema de Renderizado de Texto - Gráficos por Computadora"
    footer_render = pygame.font.SysFont('Arial', 12).render(footer, True, GRIS)
    ventana.blit(footer_render, (ANCHO//2 - footer_render.get_width()//2, ALTO - 30))
    
    # --- ACTUALIZAR PANTALLA ---
    pygame.display.flip()  # Mostrar todo lo dibujado

# --- FINALIZAR ---
pygame.freetype.quit()  # Cerrar módulo de fuentes
pygame.quit()  # Cerrar Pygame completamente