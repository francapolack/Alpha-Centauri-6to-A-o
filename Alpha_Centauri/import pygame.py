import pygame

pygame.init()
pygame.font.init()

pantalla=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
fnt=pygame.font.SysFont("Consolas",30)

def dibujar_texto(texto,fuente,color,x,y):
    img=fuente.render(texto,True,color)
    pantalla.blit(img,(x,y))

running=True
while running:
    pantalla.fill((255,255,255))
    tecla=pygame.key.get_pressed()
    if tecla[pygame.K_LEFT]:    
        dibujar_texto("Hola Mundo",fnt,(0,0,0),220,150)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    pygame.display.flip()

pygame.quit()