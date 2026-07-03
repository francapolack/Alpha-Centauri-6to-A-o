import pygame
import os
import sys
# Importamos la biblioteca para reproducir videos
from pyvidplayer2 import Video 

def aplicar_filtro_oscuro(superficie, opacidad_personaje):
    """Genera una copia oscurecida del personaje para darle énfasis al que habla."""
    if superficie is None:
        return None
    img_oscura = superficie.copy()
    filtro = pygame.Surface(img_oscura.get_size(), pygame.SRCALPHA)
    filtro.fill((0, 0, 0, 120)) 
    img_oscura.blit(filtro, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
    img_oscura.set_alpha(opacidad_personaje)
    return img_oscura

def main():
    pygame.init()
    pygame.mixer.init()

    # 1. CONFIGURACIÓN DE VENTANA INICIAL
    ANCHO_BASE = 800
    ALTO_BASE = 600
    screen = pygame.display.set_mode((ANCHO_BASE, ALTO_BASE), pygame.RESIZABLE)
    pygame.display.set_caption("Alpha Centauri")
    
    clock = pygame.time.Clock()
    carpeta_actual = os.path.dirname(__file__)

    # 2. AUDIO
    ruta_musica = os.path.join(carpeta_actual, "musica_menu.mp3")
    if os.path.exists(ruta_musica):
        pygame.mixer.music.load(ruta_musica)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
    
    ruta_click = os.path.join(carpeta_actual, "click.wav")
    sonio_click = pygame.mixer.Sound(ruta_click) if os.path.exists(ruta_click) else None

    #  3. CONFIGURACIÓN DEL VIDEO DEL MENU
    # Buscamos el video dentro de la subcarpeta 'imagenes'
    ruta_video_menu = os.path.join(carpeta_actual, "imagenes", "videomenu.mp4")
    video_menu = None
    if os.path.exists(ruta_video_menu):
        video_menu = Video(ruta_video_menu)
        video_menu.set_volume(0) 

    # 4. CARGA DE ASSETS GRÁFICOS
    assets = {}
    nombres_archivos = {
        "fondointro": "fondointro.png",
        "titulo": "titulomenu.png",
        "jugar": "botoninicio.png",
        "salir": "botonsalir.png",
        "astronauta": "astronautito.png",
        "rene": "rene.png"
    }
    
    for clave, archivo in nombres_archivos.items():
        ruta = os.path.join(carpeta_actual, "imagenes", archivo)
        if os.path.exists(ruta):
            assets[clave] = pygame.image.load(ruta).convert_alpha()
        else:
            assets[clave] = None

    # Variables de control de estado
    estado_actual = "menu"
    fase_narrativa = 1  
    opacidad_astronauta = 0
    opacidad_rene = 0   
    nombre_jugador = ""
    
    # Sistema de diálogos
    texto_prologo = "Año 2142. Sector en reconocimiento... Los sistemas fallan pero la cabina se esta adaptando."
    caracteres_vistos = 0
    conteo_frames = 0

    # Inicializamos el rectángulo del botón de la demo vacío
    boton_demo_rect = pygame.Rect(0, 0, 0, 0)

    while True:
        W_ACTUAL, H_ACTUAL = screen.get_size()
        pos_mouse = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if video_menu: video_menu.close()
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if video_menu: video_menu.close()
                    pygame.quit()
                    sys.exit()
                
                if estado_actual == "cinematica":
                    if fase_narrativa == 1:
                        if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                            if sonio_click: sonio_click.play()
                            fase_narrativa = 2
                    
                    elif fase_narrativa == 2:
                        if event.key == pygame.K_BACKSPACE:
                            nombre_jugador = nombre_jugador[:-1]
                        elif event.key == pygame.K_RETURN and nombre_jugador.strip() != "":
                            if sonio_click: sonio_click.play()
                            fase_narrativa = 3
                            caracteres_vistos = 0 
                            conteo_frames = 0
                        elif event.unicode.isalnum() and len(nombre_jugador) < 14:
                            nombre_jugador += event.unicode
                            if sonio_click: sonio_click.play()
                            
                    elif fase_narrativa == 3:
                        if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                            if sonio_click: sonio_click.play()
                            fase_narrativa = 4
                            caracteres_vistos = 0
                            conteo_frames = 0

            # DETECTAR CLICKS DE MOUSE
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if estado_actual == "menu":
                    if assets["jugar"] and jugar_rect.collidepoint(pos_mouse):
                        if sonio_click: sonio_click.play()
                        if video_menu: video_menu.close() # Cerramos el video al salir del menú
                        estado_actual = "cinematica" 
                        
                    if assets["salir"] and salir_rect.collidepoint(pos_mouse):
                        if sonio_click: sonio_click.play()
                        if video_menu: video_menu.close()
                        pygame.time.wait(300)
                        pygame.quit()
                        sys.exit()
                
                # INTERSECCIÓN: Click en el botón para iniciar la Demo de tu compañera
                elif estado_actual == "cinematica" and fase_narrativa == 4:
                    if caracteres_vistos == len(texto_rene) and boton_demo_rect.collidepoint(pos_mouse):
                        if sonio_click: sonio_click.play()
                        
                        # ACÁ SE UNE CON EL CÓDIGO DE TU COMPAÑERA
                        print("Llamando al nivel de la demo...")
                        # Ejemplo: import nivel1; nivel1.ejecutar_nivel(screen)

        # 🔄 ACTUALIZACIÓN INTERNA DEL VIDEO
        # Es obligatorio indicarle al video que avance de frame en cada vuelta del bucle
        if estado_actual == "menu" and video_menu:
            video_menu.update()
            # si eel video llegó al final o se desactivo solo, lo reiniciamos al segundo 0
            if not video_menu.active:
                video_menu.restart()

        screen.fill((10, 10, 15))

        if estado_actual == "menu":
            # REPRODUCCIÓN DEL VIDEO DE FONDO MODO COMPATIBLE
            if video_menu and video_menu.active:
                frame_superficie = video_menu.frame_surf
                if frame_superficie:
                    # Escalamos dinámicamente la superficie del frame al tamaño actual de la ventana
                    frame_escalado = pygame.transform.smoothscale(frame_superficie, (W_ACTUAL, H_ACTUAL))
                    screen.blit(frame_escalado, (0, 0))
            else:
                screen.fill((20, 20, 40)) # Fondo de auxilio si no encuentra el video

            # Título y botones del menú (Se dibujan arriba del video)
            if assets["titulo"]:
                anc_t = int(W_ACTUAL * 0.36)
                alt_t = int(assets["titulo"].get_height() * (anc_t / assets["titulo"].get_width()))
                titulo_render = pygame.transform.smoothscale(assets["titulo"], (anc_t, alt_t))
                titulo_rect = titulo_render.get_rect(center=(int(W_ACTUAL * 0.22), int(H_ACTUAL * 0.21)))
                screen.blit(titulo_render, titulo_rect)

            if assets["jugar"]:
                anc_b = int(W_ACTUAL * 0.33)
                alt_b = int(assets["jugar"].get_height() * (anc_b / assets["jugar"].get_width()))
                jugar_rect = pygame.Rect(0, 0, anc_b, alt_b)
                jugar_rect.center = (int(W_ACTUAL * 0.22), int(H_ACTUAL * 0.57))
                if jugar_rect.collidepoint(pos_mouse):
                    jugar_h = pygame.transform.smoothscale(assets["jugar"], (int(anc_b * 1.12), int(alt_b * 1.12)))
                    screen.blit(jugar_h, jugar_h.get_rect(center=jugar_rect.center))
                else:
                    jugar_n = pygame.transform.smoothscale(assets["jugar"], (anc_b, alt_b))
                    screen.blit(jugar_n, jugar_rect)

            if assets["salir"]:
                anc_s = int(W_ACTUAL * 0.17)
                alt_s = int(assets["salir"].get_height() * (anc_s / assets["salir"].get_width()))
                salir_rect = pygame.Rect(0, 0, anc_s, alt_s)
                salir_rect.center = (int(W_ACTUAL * 0.22), int(H_ACTUAL * 0.70))
                if salir_rect.collidepoint(pos_mouse):
                    salir_h = pygame.transform.smoothscale(assets["salir"], (int(anc_s * 1.12), int(alt_s * 1.12)))
                    screen.blit(salir_h, salir_h.get_rect(center=salir_rect.center))
                else:
                    salir_n = pygame.transform.smoothscale(assets["salir"], (anc_s, alt_s))
                    screen.blit(salir_n, salir_rect)

        elif estado_actual == "cinematica":
            # Fondo e iluminación de la cinemática
            if assets["fondointro"]:
                fondo_intro = pygame.transform.smoothscale(assets["fondointro"], (W_ACTUAL, H_ACTUAL))
                capa_oscura = pygame.Surface((W_ACTUAL, H_ACTUAL))
                capa_oscura.fill((0, 0, 0))
                capa_oscura.set_alpha(140) 
                screen.blit(fondo_intro, (0, 0))
                screen.blit(capa_oscura, (0, 0))
            
            fuente_dialogo = pygame.font.SysFont("Consolas", 21, bold=True)
            fuente_sistema = pygame.font.SysFont("Consolas", 15)
            fuente_nombre_tag = pygame.font.SysFont("Arial", 22, bold=True)

            # Dibujar Astronauta/usuario
            if assets["astronauta"]:
                if opacidad_astronauta < 255: opacidad_astronauta += 3
                if fase_narrativa == 4:
                    astro_base = aplicar_filtro_oscuro(assets["astronauta"], opacidad_astronauta)
                else:
                    astro_base = assets["astronauta"].copy()
                    astro_base.set_alpha(opacidad_astronauta)
                
                alt_astro = int(H_ACTUAL * 0.75) 
                anc_astro = int(assets["astronauta"].get_width() * (alt_astro / assets["astronauta"].get_height()))
                astro_scaled = pygame.transform.smoothscale(astro_base, (anc_astro, alt_astro))
                astro_rect = astro_scaled.get_rect(bottomleft=(W_ACTUAL * -0.15, H_ACTUAL - int(H_ACTUAL * 0.15)))
                screen.blit(astro_scaled, astro_rect)

            # Dibujar René
            if fase_narrativa == 4 and assets["rene"]:
                if opacidad_rene < 255: opacidad_rene += 4
                rene_base = assets["rene"].copy()
                rene_base.set_alpha(opacidad_rene)
                
                alt_rene = int(H_ACTUAL * 0.70)
                anc_rene = int(assets["rene"].get_width() * (alt_rene / assets["rene"].get_height()))
                rene_scaled = pygame.transform.smoothscale(rene_base, (anc_rene, alt_rene))
                rene_rect = rene_scaled.get_rect(bottomright=(W_ACTUAL * 0.86, H_ACTUAL - int(H_ACTUAL * 0.15)))
                screen.blit(rene_scaled, rene_rect)

            # Caja de diálogos
            ancho_caja = int(W_ACTUAL * 0.90)
            alto_caja = int(H_ACTUAL * 0.22)
            caja_rect = pygame.Rect(0, 0, ancho_caja, alto_caja)
            caja_rect.center = (W_ACTUAL // 2, H_ACTUAL - int(H_ACTUAL * 0.14))
            
            pygame.draw.rect(screen, (20, 20, 35), caja_rect, border_radius=8)
            pygame.draw.rect(screen, (0, 200, 220), caja_rect, width=3, border_radius=8)

            # Renderizado de textos según fase
            if fase_narrativa == 1:
                conteo_frames += 1
                if conteo_frames % 3 == 0 and caracteres_vistos < len(texto_prologo):
                    caracteres_vistos += 1
                texto_actual = texto_prologo[:caracteres_vistos]
                render_txt = fuente_dialogo.render(texto_actual, True, (240, 240, 255))
                screen.blit(render_txt, (caja_rect.x + 25, caja_rect.y + 35))
                
                if caracteres_vistos == len(texto_prologo):
                    render_ayuda = fuente_sistema.render("[ Presioná ENTER para continuar ]", True, (100, 220, 220))
                    screen.blit(render_ayuda, (caja_rect.right - 280, caja_rect.bottom - 25))

            elif fase_narrativa == 2:
                render_pregunta = fuente_dialogo.render("SISTEMA: Ingrese credencial de Tripulante :", True, (255, 220, 120))
                screen.blit(render_pregunta, (caja_rect.x + 25, caja_rect.y + 30))
                render_nombre = fuente_dialogo.render(f"> {nombre_jugador}_", True, (0, 255, 200))
                screen.blit(render_nombre, (caja_rect.x + 25, caja_rect.y + 65))
                
                render_ayuda = fuente_sistema.render("[ Escribí tu nombre y presioná ENTER ]", True, (130, 130, 140))
                screen.blit(render_ayuda, (caja_rect.right - 320, caja_rect.bottom - 25))

            elif fase_narrativa == 3:
                texto_contexto = f"Comandante {nombre_jugador}: CONAE informa que perdimos contacto con la base Tierra hace 4hs."
                conteo_frames += 1
                if conteo_frames % 3 == 0 and caracteres_vistos < len(texto_contexto):
                    caracteres_vistos += 1
                texto_actual = texto_contexto[:caracteres_vistos]
                render_txt = fuente_dialogo.render(texto_actual, True, (240, 240, 255))
                screen.blit(render_txt, (caja_rect.x + 25, caja_rect.y + 35))
                
                tag_nombre = fuente_nombre_tag.render(nombre_jugador, True, (255, 230, 100))
                tag_rect = tag_nombre.get_rect(centerx=astro_rect.centerx, bottom=astro_rect.top + 45)
                tag_sombra = fuente_nombre_tag.render(nombre_jugador, True, (0, 0, 0))
                screen.blit(tag_sombra, (tag_rect.x + 2, tag_rect.y + 2))
                screen.blit(tag_nombre, tag_rect)

                if caracteres_vistos == len(texto_contexto):
                    render_ayuda = fuente_sistema.render("[ Presioná ENTER para reunir a la tripulación ]", True, (255, 100, 100))
                    screen.blit(render_ayuda, (caja_rect.right - 420, caja_rect.bottom - 25))

            elif fase_narrativa == 4:
                texto_rene = "René: ¡Amigo! Qué bueno que se adaptó la cabina. Reporto fallas graves en las comunicaciones externas."
                conteo_frames += 1
                if conteo_frames % 3 == 0 and caracteres_vistos < len(texto_rene):
                    caracteres_vistos += 1
                texto_actual = texto_rene[:caracteres_vistos]
                render_txt = fuente_dialogo.render(texto_actual, True, (240, 240, 255))
                screen.blit(render_txt, (caja_rect.x + 25, caja_rect.y + 35))
                
                # Nombre de jugador opacado
                tag_nombre = fuente_nombre_tag.render(nombre_jugador, True, (130, 120, 70))
                tag_rect = tag_nombre.get_rect(centerx=astro_rect.centerx, bottom=astro_rect.top + 45)
                screen.blit(tag_nombre, tag_rect)

                if assets["rene"]:
                    tag_rene = fuente_nombre_tag.render("RENÉ", True, (0, 200, 255))
                    tag_rene_rect = tag_rene.get_rect(centerx=rene_rect.centerx, bottom=rene_rect.top - 4)
                    tag_rene_sombra = fuente_nombre_tag.render("RENÉ", True, (0, 0, 0))
                    screen.blit(tag_rene_sombra, (tag_rene_rect.x + 2, tag_rene_rect.y + 2))
                    screen.blit(tag_rene, tag_rene_rect)

                # BOTÓN DE INICIAR NIVEL / DEMO
                if caracteres_vistos == len(texto_rene):
                    # Definimos tamaño y posición del botón abajo del texto de ayuda
                    ancho_btn = 180
                    alto_btn = 40
                    boton_demo_rect = pygame.Rect(0, 0, ancho_btn, alto_btn)
                    # Lo posicionamos abajo a la derecha de la caja de diálogo
                    boton_demo_rect.bottomright = (caja_rect.right - 25, caja_rect.bottom - 20)
                    
                    # Efecto Hover (cambia de color si pasas el mouse por encima)
                    color_btn = (0, 230, 150) if boton_demo_rect.collidepoint(pos_mouse) else (0, 160, 100)
                    
                    pygame.draw.rect(screen, color_btn, boton_demo_rect, border_radius=5)
                    
                    fuente_btn = pygame.font.SysFont("Arial", 16, bold=True)
                    txt_btn = fuente_btn.render("INICIAR DEMO", True, (255, 255, 255))
                    txt_btn_rect = txt_btn.get_rect(center=boton_demo_rect.center)
                    screen.blit(txt_btn, txt_btn_rect)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
