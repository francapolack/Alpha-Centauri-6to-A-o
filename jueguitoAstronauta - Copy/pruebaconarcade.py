import arcade
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Crónicas del Sistema Solar - Arcade"

class Player(arcade.Sprite):
    def __init__(self, name, description, position, agency):
        carpeta_actual = os.path.dirname(__file__)
        ruta_completa = os.path.join(carpeta_actual, "astronauta.png")

        #definicion de texturas waos
        if os.path.exists(ruta_completa):
            textura_inicial = arcade.load_texture(ruta_completa)
        elif os.path.exists("astronauta.png"):
            textura_inicial = arcade.load_texture("astronauta.png")
        else:
            print("⚠️ Nota: Usando cuadro rosa temporal.")
            textura_inicial = arcade.texture.make_soft_square_texture(64, arcade.color.BARBIE_PINK)

        adentro_nave=arcade.load_texture("./imagenes/nivel1_adentro_nave.png")

        super().__init__(textura_inicial)
        
        self.name = name
        self.description = description
        self.agency = agency
        self.inventory = []
        
        # Esta es la velocidad máxima que alcanzará al mantener apretado
        self.movement_speed = 5 
        
        self.width = 64
        self.height = 64
        
        self.center_x = position[0] + 32
        self.center_y = SCREEN_HEIGHT - position[1] - 32

        self.nivel=1

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color((15, 15, 25)) 
        
        self.jugadores_list = arcade.SpriteList()
        self.player1 = None

    def setup(self):
        self.scene=arcade.Scene()
        self.camera=arcade.Camera(600,600)
        self.player1 = Player("Jugador 1", "Cosmonauta de la CONAE", [200, 200], "CONAE")
        self.jugadores_list.append(self.player1)
        fondo=arcade.Sprite(f"fondo_{self.level}.png")
        fondo.center_x=300
        fondo.center_y=32
        self.scene.add_sprite("Platforms",fondo)
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, self.scene.get_sprite_list("Platforms"), 0.5
        )

    def on_draw(self):
        self.clear()
        self.jugadores_list.draw()
        self.camera.use()
        self.scene.draw()

    def on_update(self, delta_time):
        # 1. Le decimos a la lista que calcule el movimiento fluido en base a change_x y change_y
        self.jugadores_list.update()

        # 2. Mantenemos los límites de pantalla de forma estricta
        if self.player1.left < 0:
            self.player1.left = 0
        if self.player1.right > SCREEN_WIDTH:
            self.player1.right = SCREEN_WIDTH
        if self.player1.bottom < 0:
            self.player1.bottom = 0
        if self.player1.top > SCREEN_HEIGHT:
            self.player1.top = SCREEN_HEIGHT
        
        self.player1_sprite.center_x+=self.vel_x*delta_time
        self.physics_engine.update()
        self.camera_move()
        if self.player1_sprite.center_x>690:
            self.level+=1
            self.setup()

    def on_key_press(self, key, modifiers):
        # Al presionar, modificamos los "vectores de cambio" nativos de Arcade
        if key == arcade.key.UP:    
            self.player1.change_y = self.player1.movement_speed
        if key == arcade.key.DOWN:  
            self.player1.change_y = -self.player1.movement_speed
        if key == arcade.key.LEFT:  
            self.player1.change_x = -self.player1.movement_speed
        if key == arcade.key.RIGHT: 
            self.player1.change_x = self.player1.movement_speed

    def on_key_release(self, key, modifiers):
        # NUEVA FUNCIÓN: Al soltar la tecla, frenamos el movimiento en ese eje
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player1.change_y = 0
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player1.change_x = 0
def main():
    game = MyGame()
    game.setup()
    arcade.run()

if __name__ == "pruebaconarcade":
    main()

