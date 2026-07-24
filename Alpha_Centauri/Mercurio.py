import pygame
import pymunk
import sys

pygame.init()
pygame.font.init()
pygame.mixer.init()

#CONSTANTES ACA
FPS=60
JUGADOR_VELOCIDAD=2
TILE_TAM=32
FUENTE_DIALOGOS=pygame.font.SysFont("Consolas",300)

#VARIABLES
CONDICION_COMPLETA=False
RUNNING=True
GRAVEDAD=1000
SELECCIONADOS=[]

#COLORES
NEGRO=(0,0,0)
BLANCO=(255,255,255)

#DEFINICION DE PANTALLA Y BASES PARA EL JUEGO
pantalla=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
pygame.display.set_caption("Mercurio")
fps=pygame.time.Clock()
fisica=pymunk.Space()
fisica.gravity=(0,GRAVEDAD)
fondo=pygame.image.load("Alpha-Centauri-6to-A-o/Alpha_Centauri/imagenes/fondos/laboratorio.png")
fondo_rect=fondo.get_rect()
musica_mercurio="Alpha-Centauri-6to-A-o/Alpha_Centauri/musica_menu.wav"
click_sonido=pygame.mixer.Sound("Alpha-Centauri-6to-A-o/Alpha_Centauri/click.wav")

pygame.mixer.music.load(musica_mercurio)
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play()
            

#DEFINICION DE CLASES,FUNCIONES Y OBJETOS 
ANCHO_PC,ALTO_PC=pygame.display.get_surface().get_size()

def texto_display(texto,fuente,color,x,y):
    img=fuente.render(texto,True,color)
    pantalla.blit(img,(x,y))

""""
class Jugador:
    def __init__(self,textura):
        self.textura_inicial=textura
        self.textura=pygame.transform.scale(self.textura_inicial,(150,50))
        self.hitbox=self.textura.get_rect()
        self.hitbox.center=(ANCHO_PC//2,ALTO_PC//2)
"""

class Partes_Rover:
    #poner esto como una libreria?
    click=False 
    def __init__(self,textura,x):
        self.textura=textura
        self.hitbox=self.textura.get_rect()
        self.hitbox.center=(x,(ALTO_PC//4))
    def descripcion(self,texto):
        self.texto=texto
""""
class Boton:
    def __init__(self,texto,fuente,color_texto):
        self.boton=pygame.Rect(0,0,180,40)
        self.color_fondo=(0,230,150)
        pygame.draw.rect(pantalla,self.color_fondo,self.boton,border_radius=5)
        
        self.fuente_boton=fuente
        self.txt=self.fuente_boton.render(texto,True,color_texto)
        self.hitbox=self.txt.get_rect(center=self.boton.center)
        pantalla.blit(self.txt,self.hitbox)

termine=Boton
termine("Termine de construir",FUENTE_DIALOGOS,BLANCO)
"""

#textura_jugador=pygame.image.load("Alpha-Centauri-6to-A-o/Alpha_Centauri/imagenes/camina_adelante.png").convert_alpha()
#jugador=Jugador(textura_jugador)

textura_rueda=pygame.image.load("Alpha-Centauri-6to-A-o/Alpha_Centauri/imagenes/objetos/mercurio/ROVER_RUEDA.png").convert_alpha()
rueda=Partes_Rover(textura_rueda,(ANCHO_PC//2))
rueda.descripcion("Texto de la rueda, bla bla blaaa")

textura_camara=pygame.image.load("Alpha-Centauri-6to-A-o/Alpha_Centauri/imagenes/objetos/mercurio/ROVER_CAMARAS.png").convert_alpha()
camara=Partes_Rover(textura_camara,(ANCHO_PC//6))
camara.descripcion("Texto de la camata, bla bla blaa")

textura_base=pygame.image.load("Alpha-Centauri-6to-A-o/Alpha_Centauri/imagenes/objetos/mercurio/ROVER_BASE.png").convert_alpha()
base=Partes_Rover(textura_base,(ANCHO_PC-200))
base.descripcion("Texto de la base,bla bla blaa")

class Main:
    while RUNNING:   
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                RUNNING=False
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            #CINEMATICA 
            #SELECCION DE LAS PARTEEESSSS
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if base.hitbox.collidepoint(event.pos):
                    click_sonido.play()
                    texto_display("base.texto",FUENTE_DIALOGOS,BLANCO,220,150)
                    if "BASE" in SELECCIONADOS:
                        print("Ya has seleccionado este componente")
                    else:
                        SELECCIONADOS.append("BASE")
                        print("Que mas podriamos necesitar jsjd")

                elif rueda.hitbox.collidepoint(event.pos):
                    click_sonido.play()
                    texto_display(rueda.texto,NEGRO)
                    if "RUEDA" in SELECCIONADOS:
                        print("Ya has seleccionado este componente")
                    else:
                        SELECCIONADOS.append("RUEDA")
                    print(SELECCIONADOS)
                elif camara.hitbox.collidepoint(event.pos):
                    click_sonido.play()
                    if "CAMARA" in SELECCIONADOS:
                        print("Ya has seleccionado este componente")
                    else:
                        SELECCIONADOS.append("CAMARA")

                #elif termine.hitbox.collidepoint(event.pos):
                    #if len(SELECCIONADOS)>=3:
                        #texto_display("Has terminado de construir tu rover!",FUENTE_DIALOGOS,NEGRO)
               # elif len(SELECCIONADOS)<3:
                    #texto_display("Renee: Seguro de que has terminado de construir?",FUENTE_DIALOGOS,NEGRO)
                    
        fisica.step(1/60.0)


        #MOVIMIENTO DEL JUGRADOR
        """"
        tecla=pygame.key.get_pressed()
        if tecla[pygame.K_LEFT] or tecla[pygame.K_a]:
            jugador.hitbox.move_ip(-JUGADOR_VELOCIDAD,0)

        elif tecla[pygame.K_RIGHT] or tecla[pygame.K_d]:
            jugador.hitbox.move_ip(JUGADOR_VELOCIDAD,0)

        elif tecla[pygame.K_UP] or tecla[pygame.K_w]:
            jugador.hitbox.move_ip(0,-JUGADOR_VELOCIDAD)

        elif tecla[pygame.K_DOWN] or tecla[pygame.K_s]:
            jugador.hitbox.move_ip(0,JUGADOR_VELOCIDAD)
        """
        #MOSTRA TODO EN LA PANTALIA
        pantalla.fill(BLANCO)
        pantalla.blit(fondo,fondo_rect)
        #pantalla.blit(jugador.textura,jugador.hitbox)
        pantalla.blit(camara.textura,camara.hitbox)
        pantalla.blit(base.textura,base.hitbox)
        pantalla.blit(rueda.textura,rueda.hitbox)


        #reiniciooooo
        pygame.display.flip()
        fps.tick(FPS)

Main()
pygame.quit()
        