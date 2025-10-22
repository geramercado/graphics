#introduccion a la animacion por computadora
# Gerardo Mercado Hurtado
# Raúl Martínez Martínez 
#  ejercicio_final_clase1.py
import pygame
import sys
import math

# Inicialización de Pygame 
pygame.init()

# Configuración de la ventana
ANCHO = 800
ALTO = 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Clase 1 - Introducción a la Animación")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
MORADO = (255, 0, 255)
CIAN = (0, 255, 255)

# Reloj para controlar FPS
reloj = pygame.time.Clock()
FPS = 60

def colision(obj1, obj2):
        rect1 = pygame.Rect(obj1.x, obj1.y, 50, 50)
        rect2 = pygame.Rect(obj2.x, obj2.y, 50, 50)
        return rect1.colliderect(rect2)

class AnimacionSimple:
    def __init__(self, color=ROJO):
        self.x = 100
        self.y = 300
        self.velocidad_x = 3
        self.velocidad_y = 2
        self.trayectoria = []
        self.max_trayectoria = 30
        self.escala = 1.0
        self.escala_objetivo = 1.0
        self.rebotes = 0
        self.frames_transcurridos = 0

        # Color actual del objeto
        self.color = color

    

        
    def actualizar(self):
        # Actualizar contadores
        self.frames_transcurridos += 1
        
        # Guardar posición anterior para detectar rebotes
        x_anterior = self.x
        
        # Actualizar posición
        self.x += self.velocidad_x
        self.y += self.velocidad_y
        
        # Efecto de escala (squash and stretch básico)
        if abs(self.escala - self.escala_objetivo) > 0.01:
            self.escala += (self.escala_objetivo - self.escala) * 0.3
        else:
            self.escala_objetivo = 1.0
        
        # Detectar rebotes y cambiar dirección
        rebote = False
        if self.x <= 0:
            self.velocidad_x = abs(self.velocidad_x)
            rebote = True
        elif self.x >= ANCHO - 50:
            self.velocidad_x = -abs(self.velocidad_x)
            rebote = True
            
        if self.y <= 0:
            self.velocidad_y = abs(self.velocidad_y)
            rebote = True
        elif self.y >= ALTO - 50:
            self.velocidad_y = -abs(self.velocidad_y)
            rebote = True
        
        # Aplicar efecto de rebote
        if rebote:
            self.rebotes += 1
            self.escala_objetivo = 0.7  # Comprimir al rebotar

                # Cambiar de color aleatoriamente en cada rebote
            self.color = (
                pygame.time.get_ticks() % 256,
                (pygame.time.get_ticks() * 2) % 256,
                (pygame.time.get_ticks() * 3) % 256
            )

        
        # Guardar posición para trayectoria
        centro_x = self.x + 25
        centro_y = self.y + 25
        self.trayectoria.append((centro_x, centro_y))
        
        # Limitar tamaño de la trayectoria
        if len(self.trayectoria) > self.max_trayectoria:
            self.trayectoria.pop(0)
    
    def dibujar(self, superficie, color=ROJO):
        # Dibujar trayectoria (persistencia de visión)
        for i, pos in enumerate(self.trayectoria):
            # Calcular transparencia y tamaño basado en la antigüedad
            progreso = i / len(self.trayectoria)
            alpha = int(255 * progreso)
            radio = int(8 * progreso)
            
            # Crear superficie temporal para alpha
            surf_temp = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf_temp, (255, 255, 255, alpha), (radio, radio), radio)
            superficie.blit(surf_temp, (pos[0] - radio, pos[1] - radio))
        
        # Calcular dimensiones escaladas
        ancho_escalado = int(50 * self.escala)
        alto_escalado = int(50 * (2 - self.escala))  # Opuesto en Y para efecto natural
        
        # Dibujar objeto principal con efecto de escala
        rect_escalado = pygame.Rect(
            self.x + (50 - ancho_escalado) // 2,
            self.y + (50 - alto_escalado) // 2,
            ancho_escalado,
            alto_escalado
        )
        pygame.draw.rect(superficie, self.color, rect_escalado, border_radius=8)
        
        # Dibujar centro del objeto
        centro_x = self.x + 25
        centro_y = self.y + 25
        pygame.draw.circle(superficie, VERDE, (int(centro_x), int(centro_y)), 5)
        
        # Dibujar vector de velocidad
        punto_final = (
            centro_x + self.velocidad_x * 10,
            centro_y + self.velocidad_y * 10
        )
        pygame.draw.line(superficie, AMARILLO, (centro_x, centro_y), punto_final, 2)
        pygame.draw.circle(superficie, AMARILLO, (int(punto_final[0]), int(punto_final[1])), 3)

class SistemaParticulas:
    def __init__(self):
        self.particulas = []
        
    def agregar_particula(self, x, y, color):
        self.particulas.append({
            'x': x,
            'y': y,
            'color': color,
            'vida': 1.0,
            'velocidad_x': (pygame.time.get_ticks() % 10) - 5,
            'velocidad_y': (pygame.time.get_ticks() % 10) - 5
        })
    
    def actualizar(self):
        for particula in self.particulas[:]:
            particula['x'] += particula['velocidad_x'] * 0.5
            particula['y'] += particula['velocidad_y'] * 0.5
            particula['vida'] -= 0.02
            
            if particula['vida'] <= 0:
                self.particulas.remove(particula)
    
    def dibujar(self, superficie):
        for particula in self.particulas:
            alpha = int(255 * particula['vida'])
            tamaño = int(5 * particula['vida'])
            
            surf_temp = pygame.Surface((tamaño * 2, tamaño * 2), pygame.SRCALPHA)
            color = list(particula['color'])
            if len(color) == 3:
                color.append(alpha)
            pygame.draw.circle(surf_temp, color, (tamaño, tamaño), tamaño)
            superficie.blit(surf_temp, (particula['x'] - tamaño, particula['y'] - tamaño))
            

def dibujar_rejilla(superficie):
    """Dibuja una rejilla para referencia espacial"""
    for x in range(0, ANCHO, 50):
        alpha = 30 if x % 100 == 0 else 15
        color = (100, 100, 100, alpha)
        pygame.draw.line(superficie, color, (x, 0), (x, ALTO), 1)
    
    for y in range(0, ALTO, 50):
        alpha = 30 if y % 100 == 0 else 15
        color = (100, 100, 100, alpha)
        pygame.draw.line(superficie, color, (0, y), (ANCHO, y), 1)

def ejercicio_final_clase1():
        
    # Crear objetos de animación
    animacion = AnimacionSimple()
    particulas = SistemaParticulas()
    animacion_espejo = AnimacionSimple(CIAN)

    # Actualizar animación principal
    animacion.actualizar()
    animacion_espejo.actualizar()

    # Detectar colisión entre las dos figuras
    if colision(animacion, animacion_espejo):
        # Intercambiar velocidades (rebote)
        animacion.velocidad_x *= -1
        animacion.velocidad_y *= -1
        animacion_espejo.velocidad_x *= -1
        animacion_espejo.velocidad_y *= -1
        
        # Cambiar colores aleatoriamente
        animacion.color = (
            pygame.time.get_ticks() % 256,
            (pygame.time.get_ticks() * 2) % 256,
            (pygame.time.get_ticks() * 3) % 256
        )
        animacion_espejo.color = (
            (pygame.time.get_ticks() * 3) % 256,
            (pygame.time.get_ticks() * 2) % 256,
            pygame.time.get_ticks() % 256
        )


    # Configurar la posición inicial del espejo
    animacion_espejo.x = ANCHO - 150
    animacion_espejo.y = 300

    # Hacer que se mueva en sentido contrario
    animacion_espejo.velocidad_x = -animacion.velocidad_x
    animacion_espejo.velocidad_y = -animacion.velocidad_y
    
    # Variables de control
    frame_count = 0
    tiempo_inicio = pygame.time.get_ticks()
    pausa = False
    mostrar_rejilla = True
    mostrar_trayectoria = True
    mostrar_vector = True
    
    # Fuentes para texto
    fuente_grande = pygame.font.Font(None, 36)
    fuente_pequena = pygame.font.Font(None, 24)
    
    ejecutando = True
    while ejecutando:
        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif evento.key == pygame.K_SPACE:
                    pausa = not pausa
                elif evento.key == pygame.K_g:
                    mostrar_rejilla = not mostrar_rejilla
                elif evento.key == pygame.K_t:
                    mostrar_trayectoria = not mostrar_trayectoria
                elif evento.key == pygame.K_v:
                    mostrar_vector = not mostrar_vector
                elif evento.key == pygame.K_r:
                    # Resetear animación
                    animacion = AnimacionSimple()
                    particulas = SistemaParticulas()
                    frame_count = 0
                    tiempo_inicio = pygame.time.get_ticks()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                # Agregar partículas al hacer clic
                x, y = pygame.mouse.get_pos()
                for _ in range(10):
                    particulas.agregar_particula(x, y, CIAN)
        
        if not pausa:
            # Actualizar contadores
            frame_count += 1
            tiempo_actual = pygame.time.get_ticks() - tiempo_inicio
            
            # Actualizar animación principal
            animacion.actualizar()
            animacion_espejo.actualizar()
            
            # Agregar partículas en rebotes (simular efecto)
            if animacion.rebotes > 0 and frame_count % 2 == 0:
                centro_x = animacion.x + 25
                centro_y = animacion.y + 25
                for _ in range(3):
                    particulas.agregar_particula(centro_x, centro_y, MORADO)
            
            # Actualizar sistema de partículas
            particulas.actualizar()
        
        # Dibujado
        ventana.fill(NEGRO)
        
        # Dibujar rejilla si está activada
        if mostrar_rejilla:
            dibujar_rejilla(ventana)
        
        # Dibujar trayectoria si está activada
        if mostrar_trayectoria:
            animacion.dibujar(ventana)
            animacion_espejo.dibujar(ventana, CIAN)
        else:
            # Dibujar solo el objeto sin trayectoria
            centro_x = animacion.x + 25
            centro_y = animacion.y + 25
            pygame.draw.rect(ventana, ROJO, (animacion.x, animacion.y, 50, 50), border_radius=8)
            pygame.draw.circle(ventana, VERDE, (int(centro_x), int(centro_y)), 5)
            
            # Dibujar vector si está activado
            if mostrar_vector:
                punto_final = (
                    centro_x + animacion.velocidad_x * 10,
                    centro_y + animacion.velocidad_y * 10
                )
                pygame.draw.line(ventana, AMARILLO, (centro_x, centro_y), punto_final, 2)
        
        # Dibujar partículas
        particulas.dibujar(ventana)
        
        # Mostrar información en pantalla
        info_lines = [
            f"FPS: {int(reloj.get_fps())}",
            f"Frame: {frame_count}",
            f"Tiempo: {tiempo_actual/1000:.1f}s",
            f"Posición: ({animacion.x:.1f}, {animacion.y:.1f})",
            f"Velocidad: ({animacion.velocidad_x:.1f}, {animacion.velocidad_y:.1f})",
            f"Rebotes: {animacion.rebotes}",
            f"Escala: {animacion.escala:.2f}",
            "",
            "CONTROLES:",
            "ESPACIO: Pausa/Reanudar",
            "G: Mostrar/Ocultar rejilla",
            "T: Mostrar/Ocultar trayectoria", 
            "V: Mostrar/Ocultar vector",
            "R: Reiniciar animación",
            "CLIC: Crear partículas",
            "ESC: Salir"
        ]
        
        for i, linea in enumerate(info_lines):
            if i < 7:  # Información principal
                color = BLANCO
                fuente = fuente_pequena
            elif i == 7:  # Línea vacía
                continue
            elif i == 8:  "CONTROLES"
            color = AMARILLO
            fuente = fuente_pequena
        else:  # Controles
                color = VERDE
                fuente = fuente_pequena
                
        texto = fuente.render(linea, True, color)
        ventana.blit(texto, (10, 10 + i * 20))
        
        # Estado de pausa
        if pausa:
            texto_pausa = fuente_grande.render("PAUSA", True, ROJO)
            ventana.blit(texto_pausa, (ANCHO//2 - texto_pausa.get_width()//2, ALTO//2 - 50))
        
        # Actualizar pantalla
        pygame.display.flip()
        
        # Controlar FPS
        reloj.tick(FPS)
    
    pygame.quit()
    sys.exit()

# Ejecutar el ejercicio final
if __name__ == "__main__":
    ejercicio_final_clase1()



