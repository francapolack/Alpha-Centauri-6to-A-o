import pygame
#dame pymunk o dame muerte
import pymunk
import pytmx

pygame.init()

#constantes
ancho_pc=612
alto_pc=408
FPS=60
jugador_velocidad=2
ROJO=(255,0,0)
TILE_TAM=32

#odio todo maldita sea quiero dormir

#variables
condicion_completa=False
running=True
gravedad=1000


pantalla=pygame.display.set_mode((ancho_pc,alto_pc),pygame.RESIZABLE)
pygame.display.set_caption("ALPHA CENTAURI")
fps=pygame.time.Clock()
mundo=pymunk.Space()
mundo.gravity=(0,gravedad)

tmx_datos=pytmx.load_pygame(r"C:\Users\frmuu\OneDrive\Documentos\colegio(tareas o ejercicios)\alphacentauri_troubleshooting\tilesets\space.tsx")
tile_ancho=tmx_datos.tilewidth
tile_alto=tmx_datos.tileheight



#jugador
jugador_textura=pygame.image.load(r"C:\Users\frmuu\OneDrive\Documentos\colegio(tareas o ejercicios)\alphacentauri_troubleshooting\imagenes\sprites\astronauta.png")
jugador_rect=jugador_textura.get_rect()
jugador_rect.center=(ancho_pc//2,alto_pc//2)


#cosas que no son el jugador
enemigo_1_textura=pygame.image.load(r"C:\Users\frmuu\OneDrive\Documentos\colegio(tareas o ejercicios)\alphacentauri_troubleshooting\imagenes\sprites\alien.png")
enemigo_1_rect=enemigo_1_textura.get_rect()
enemigo_1_rect.center=(ancho_pc//4,alto_pc//2)

bg=pygame.image.load(r"C:\Users\frmuu\OneDrive\Imágenes\Acer\CW Leo From GALEX_desktop.png")
bg_rect=bg.get_rect()



def dibujar_nivel():
    for capa in tmx_datos.visible_layers:
        if isinstance(capa,pytmx.TiledTileLayer):
            for x,y,gid in capa:
                tile=tmx_datos.get_tile_image_by_gid(gid)
                if tile:
                    pantalla.blit(tile,(x*tile_ancho,y*tile_alto))

#bucle principal
class main_looop:
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
        mundo.step(1/60.0)
        dibujar_nivel()

        tecla=pygame.key.get_pressed()
        if tecla[pygame.K_LEFT] or tecla[pygame.K_a]:
            jugador_rect.move_ip(-jugador_velocidad,0)
        elif tecla[pygame.K_RIGHT] or tecla[pygame.K_d]:
            jugador_rect.move_ip(jugador_velocidad,0)
        elif tecla[pygame.K_UP] or tecla[pygame.K_w]:
            jugador_rect.move_ip(0,-jugador_velocidad)
        elif tecla[pygame.K_DOWN] or tecla[pygame.K_s]:
            jugador_rect.move_ip(0,jugador_velocidad)

        if jugador_rect.colliderect(enemigo_1_rect):
            if not condicion_completa:
                print("Tienes que completar x condicion antes de luchar contra el alien!")
            else:
                print("Hola!")

        if not condicion_completa:
            condicion_rect=pygame.Rect(ancho_pc//2-25,alto_pc//2-25,50,50)
            pygame.draw.rect(pantalla,(0,0,0),condicion_rect)
            if jugador_rect.colliderect(condicion_rect):
                print("Has completado la conidcion!")
                condicion_completa=True

        pantalla.fill([255,255,255])
        pantalla.blit(bg,bg_rect)
        pantalla.blit(jugador_textura,jugador_rect)
        pantalla.blit(enemigo_1_textura,enemigo_1_rect)
        pygame.display.update()
        fps.tick(FPS)
main_looop()
pygame.display.flip()
pygame.quit()