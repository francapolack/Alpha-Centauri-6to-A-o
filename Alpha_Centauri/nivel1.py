import pygame
#dame pymunk o dame muerte
import pymunk
import pytmx
import sys

pygame.init()

#constantes
ANCHO_PC=612
ALTO_PC=408
FPS=60
JUGADOR_VELOCIDAD=2
ROJO=(255,0,0)
TILE_TAM=32


#variables
condicion_completa=False
running=True
gravedad=1000


pantalla=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
pygame.display.set_caption("ALPHA CENTAURI")
fps=pygame.time.Clock()
mundo=pymunk.Space()
mundo.gravity=(0,gravedad)

#jugador
jugador_textura=pygame.image.load("Alpha-Centauri-6to-A-o\Alpha_Centauri\imagenes\camina adelante.png")
jugador_rect=jugador_textura.get_rect()
jugador_rect.center=(ANCHO_PC//2,ALTO_PC//2)


#cosas que no son el jugador
enemigo_1_textura=pygame.image.load(r"C:\Users\frmuu\OneDrive\Documentos\colegio(tareas o ejercicios)\alphacentauri_troubleshooting\imagenes\sprites\alien.png")
enemigo_1_rect=enemigo_1_textura.get_rect()
enemigo_1_rect.center=(ANCHO_PC,ALTO_PC//2)

enemigo_2_textura=pygame.image.load(r"C:\Users\frmuu\OneDrive\Documentos\colegio(tareas o ejercicios)\alphacentauri_troubleshooting\imagenes\sprites\alien2.png")
enemigo_2_rect=enemigo_2_textura.get_rect()
enemigo_2_rect.center=(ANCHO_PC//2+3,ALTO_PC)
texto_perrito="Woof(Bienvenido a Marte)"




bg=pygame.image.load("Alpha-Centauri-6to-A-o\Alpha_Centauri\imagenes\fondos\laboratorio.png")
bg_rect=bg.get_rect()


#bucle principal
class main_looop:
    while running:

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        mundo.step(1/60.0)
        

        tecla=pygame.key.get_pressed()
        if tecla[pygame.K_LEFT] or tecla[pygame.K_a]:
            jugador_rect.move_ip(-JUGADOR_VELOCIDAD,0)
        elif tecla[pygame.K_RIGHT] or tecla[pygame.K_d]:
            jugador_rect.move_ip(JUGADOR_VELOCIDAD,0)
        elif tecla[pygame.K_UP] or tecla[pygame.K_w]:
            jugador_rect.move_ip(0,-JUGADOR_VELOCIDAD)
        elif tecla[pygame.K_DOWN] or tecla[pygame.K_s]:
            jugador_rect.move_ip(0,JUGADOR_VELOCIDAD)

        if jugador_rect.colliderect(enemigo_1_rect):
            if not condicion_completa:
                print("Tienes que completar x condicion antes de luchar contra el alien!")
            else:
                print("Hola!")
        elif jugador_rect.colliderect(enemigo_2_rect):
                print("Woof")
                

        if not condicion_completa:
            condicion_rect=pygame.Rect(ANCHO_PC//2-25,ALTO_PC//2-25,50,50)
            pygame.draw.rect(pantalla,(0,0,0),condicion_rect)
            if jugador_rect.colliderect(condicion_rect):
                print("Has completado la conidcion!")
                condicion_completa=True

        pantalla.fill([255,255,255])
        pantalla.blit(bg,bg_rect)
        pantalla.blit(jugador_textura,jugador_rect)
        pantalla.blit(enemigo_1_textura,enemigo_1_rect)
        pantalla.blit(enemigo_2_textura,enemigo_2_rect)
        pygame.display.update()
        fps.tick(FPS)


main_looop()
pygame.display.flip()
pygame.quit()