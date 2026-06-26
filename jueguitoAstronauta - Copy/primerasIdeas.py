import pygame
import sys  

# ==========================================================
# 1. EL MOLDE DE LOS PERSONAJES (CON IMAGEN REAL)
# ==========================================================
class Character:
    def __init__(self, name, description, position, image_path):
        self.name = name
        self.description = description
        self.position = position 
        self.speed = 4 # Bajamos un pelito la velocidad para que sea más natural

        # INTENTAMOS CARGAR TU IMAGEN
        try:
            # Cargamos el archivo png
            self.image = pygame.image.load(image_path).convert_alpha()
            # Opcional: Si tu dibujo quedó muy chico o muy grande, acá lo escalamos a 64x64 píxeles
            self.image = pygame.transform.scale(self.image, (64, 64))
        except:
            # Si el archivo no está en la carpeta, el juego no se rompe: usa un cuadrado rosa de auxilio
            print(f"¡Error! No se encontró la imagen en: {image_path}. Usando cuadro temporal.")
            self.image = pygame.Surface((64, 64))
            self.image.fill((255, 0, 128))

        # El rect ahora se adapta automáticamente al tamaño de tu imagen
        self.rect = self.image.get_rect(topleft=position)

    def move(self, direction):
        if direction == "up":
            self.rect.y -= self.speed
        elif direction == "down":
            self.rect.y += self.speed
        elif direction == "left":
            self.rect.x -= self.speed
        elif direction == "right":
            self.rect.x += self.speed

class Player(Character):
    def __init__(self, name, description, position, image_path, agency):
        # Heredamos todo de Character usando la ruta de la imagen
        super().__init__(name, description, position, image_path)
        self.agency = agency 
        self.inventory = [] 

# ==========================================================
# 2. EL JUEGO EN SÍ (EL BUCLE PRINCIPAL)
# ==========================================================
pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Crónicas del Sistema Solar - ¡Primer Sprite!")

# CREAMOS AL JUGADOR PASÁNDOLE EL NOMBRE DE TU ARCHIVO DE IMAGEN
# Asegurate de que el archivo se llame 'astronauta.png' y esté en la misma carpeta
player1 = Player("Jugador 1", "Cosmonauta de la CONAE", [200, 200], "astronauta.png", "CONAE")

running = True
clock = pygame.time.Clock() 

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # REVISAR TECLAS PRESIONADAS
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player1.move("up")
    if keys[pygame.K_DOWN]:
        player1.move("down")
    if keys[pygame.K_LEFT]:
        player1.move("left")
    if keys[pygame.K_RIGHT]:
        player1.move("right")

    # DIBUJO EN PANTALLA
    screen.fill((15, 15, 25)) # Fondo espacial oscuro un toque más azulado

    # Dibujamos tu sprite en la pantalla
    screen.blit(player1.image, player1.rect)

    pygame.display.flip()
    clock.tick(60) 

pygame.quit()
sys.exit()




