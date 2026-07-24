import pygame
import os
import sys
import random
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

    # 2. AUDIO (Música de fondo y efectos)
    ruta_musica = os.path.join(carpeta_actual, "musica_menu.mp3")
    if os.path.exists(ruta_musica):
        pygame.mixer.music.load(ruta_musica)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
    
    ruta_click = os.path.join(carpeta_actual, "click.wav")
    sonio_click = pygame.mixer.Sound(ruta_click) if os.path.exists(ruta_click) else None

    # 3. CONFIGURACIÓN DEL VIDEO DEL MENU (Sin procesar audio para evitar requerir FFmpeg)
    ruta_video_menu = os.path.join(carpeta_actual, "imagenes", "videomenu.mp4")
    video_menu = None
    if os.path.exists(ruta_video_menu):
        # Agregamos audio=False para solucionar el error de ejecutable/FFmpeg
        video_menu = Video(ruta_video_menu)
        video_menu.mute()  # Silenciar el video para evitar conflictos de audio

    # 4. CARGA DE ASSETS GRÁFICOS
    assets = {}
    nombres_archivos = {
        "fondointro": "fondointro.png",
        "titulo": "titulomenu.png",
        "jugar": "botoninicio.png",
        "salir": "botonsalir.png",
        "astronauta": "astronautito.png",
        "rene": "rene.png",
        "pasillo": "habitaciones.png"
    }
    
    for clave, archivo in nombres_archivos.items():
        ruta = os.path.join(carpeta_actual, "imagenes", archivo)
        if os.path.exists(ruta):
            assets[clave] = pygame.image.load(ruta).convert_alpha()
        else:
            assets[clave] = None

    # 4B. CARGA Y ESCALADO PROPORCIONAL DE LAS ANIMACIONES
    ALTO_MAPA_ASTRO = 52  

    def cargar_img_mapa(nombre_archivo, ancho_fijo=None):
        ruta = os.path.join(carpeta_actual, "imagenes", nombre_archivo)
        if os.path.exists(ruta):
            img = pygame.image.load(ruta).convert_alpha()
            if ancho_fijo:
                ancho_final = ancho_fijo
            else:
                ancho_final = int(img.get_width() * (ALTO_MAPA_ASTRO / img.get_height()))
            return pygame.transform.scale(img, (ancho_final, ALTO_MAPA_ASTRO))
        
        ancho_aux = ancho_fijo if ancho_fijo else 35
        surf = pygame.Surface((ancho_aux, ALTO_MAPA_ASTRO))
        surf.fill((255, 0, 0))
        return surf

    img_adelante = cargar_img_mapa("camina adelante.png")
    img_atras = cargar_img_mapa("camina atras.png")
    
    img_adelante_espejo = pygame.transform.flip(img_adelante, True, False)
    img_atras_espejo = pygame.transform.flip(img_atras, True, False)
    
    img_derecha_1 = cargar_img_mapa("caminapataadelante.png")
    ANCHO_LATERAL_FIJO = img_derecha_1.get_width()
    img_derecha_2 = cargar_img_mapa("caminapataatras.png", ancho_fijo=ANCHO_LATERAL_FIJO)
    
    img_izquierda_1 = pygame.transform.flip(img_derecha_1, True, False)
    img_izquierda_2 = pygame.transform.flip(img_derecha_2, True, False)

    # Coordenadas iniciales del jugador
    x_jugador = None   
    y_jugador = None  
    velocidad_jugador = 5
    direccion_jugador = "derecha"
    contador_pasos = 0

    # Variables de control de estado
    estado_actual = "menu"
    fase_narrativa = 1  
    opacidad_astronauta = 0
    opacidad_rene = 0   
    nombre_jugador = ""
    
    # Sistema de diálogos
    texto_prologo = "Año 2142. Sector en reconocimiento... Los sistemas fallan pero la cabina se esta adaptando."
    texto_rene = "" 
    caracteres_vistos = 0
    conteo_frames = 0
    boton_demo_rect = pygame.Rect(0, 0, 0, 0)
    
    # Temporizador Alarma
    alfa_alarma = 0
    incremento_alarma = 4

    mision_completada = False
    mostrar_cartel_exito = False
    frames_cartel = 0

    # Variables del minijuego
    asteroides = []  
    asteroides_destruidos = 0
    max_asteroides_mision = 10
    temporizador_spawn = 0

    while True:
        W_ACTUAL, H_ACTUAL = screen.get_size()
        pos_mouse = pygame.mouse.get_pos()
        esta_moviendose = False
        
        texto_rene_completo = "René: ¡Amigo! Qué bueno que se adaptó la cabina. Reporto fallas graves en las comunicaciones externas."

        # Zona de minijuego (Habitación de la derecha)
        zona_mision = pygame.Rect(
            int(W_ACTUAL * 0.77), 
            int(H_ACTUAL * 0.16), 
            int(W_ACTUAL * 0.15), 
            int(H_ACTUAL * 0.22)
        )

        # Posición inicial dentro del círculo azul
        if x_jugador is None or y_jugador is None:
            x_jugador = int(W_ACTUAL * 0.08)
            y_jugador = int(H_ACTUAL * 0.52)

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

                    elif fase_narrativa == 4:
                        if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                            if sonio_click: sonio_click.play()
                            if caracteres_vistos < len(texto_rene_completo):
                                caracteres_vistos = len(texto_rene_completo)
                            else:
                                estado_actual = "exploracion"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if estado_actual == "menu":
                    if assets["jugar"] and jugar_rect.collidepoint(pos_mouse):
                        if sonio_click: sonio_click.play()
                        if video_menu: video_menu.close()
                        estado_actual = "cinematica" 
                        
                    if assets["salir"] and salir_rect.collidepoint(pos_mouse):
                        if sonio_click: sonio_click.play()
                        if video_menu: video_menu.close()
                        pygame.time.wait(300)
                        pygame.quit()
                        sys.exit()
                
                elif estado_actual == "cinematica" and fase_narrativa == 4:
                    if caracteres_vistos < len(texto_rene_completo):
                        if sonio_click: sonio_click.play()
                        caracteres_vistos = len(texto_rene_completo)
                    elif boton_demo_rect.collidepoint(pos_mouse):
                        if sonio_click: sonio_click.play()
                        estado_actual = "exploracion"

                elif estado_actual == "minijuego_asteroides":
                    for asteroide in asteroides[:]:
                        if asteroide['rect'].collidepoint(pos_mouse):
                            asteroides.remove(asteroide)
                            asteroides_destruidos += 1
                            if sonio_click: sonio_click.play()
                            break

        if estado_actual == "exploracion":
            keys = pygame.key.get_pressed()
            ancho_actual_astro = img_adelante.get_width() if direccion_jugador in ["adelante", "atras"] else ANCHO_LATERAL_FIJO

            # Movimiento base
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                x_jugador -= velocidad_jugador
                direccion_jugador = "izquierda"
                esta_moviendose = True
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                x_jugador += velocidad_jugador
                direccion_jugador = "derecha"
                esta_moviendose = True

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                y_jugador -= velocidad_jugador
                direccion_jugador = "atras"
                esta_moviendose = True
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                y_jugador += velocidad_jugador
                direccion_jugador = "adelante"
                esta_moviendose = True

            if esta_moviendose:
                contador_pasos += 1
            else:
                contador_pasos = 0

            # Límites del pasillo
            Y_MIN_PASILLO = int(H_ACTUAL * 0.44)  
            Y_MAX_PASILLO = int(H_ACTUAL * 0.62)  
            X_ENTRADA_HAB3 = int(W_ACTUAL * 0.74) 

            if x_jugador < X_ENTRADA_HAB3:
                if y_jugador < Y_MIN_PASILLO:
                    y_jugador = Y_MIN_PASILLO
                if y_jugador > Y_MAX_PASILLO:
                    y_jugador = Y_MAX_PASILLO
            else:
                if y_jugador < int(H_ACTUAL * 0.12):
                    y_jugador = int(H_ACTUAL * 0.12)
                if y_jugador > Y_MAX_PASILLO:
                    y_jugador = Y_MAX_PASILLO
                
                if y_jugador < Y_MIN_PASILLO:
                    if x_jugador < int(W_ACTUAL * 0.74):
                        x_jugador = int(W_ACTUAL * 0.74)
                    if x_jugador > int(W_ACTUAL * 0.93) - ancho_actual_astro:
                        x_jugador = int(W_ACTUAL * 0.93) - ancho_actual_astro

            if x_jugador < int(W_ACTUAL * 0.04): 
                x_jugador = int(W_ACTUAL * 0.04)
            if x_jugador > int(W_ACTUAL * 0.94) - ancho_actual_astro: 
                x_jugador = int(W_ACTUAL * 0.94) - ancho_actual_astro

            # Disparador del minijuego
            hitbox_final = pygame.Rect(x_jugador, y_jugador, ancho_actual_astro, ALTO_MAPA_ASTRO)
            if hitbox_final.colliderect(zona_mision) and not mision_completada:
                estado_actual = "minijuego_asteroides"
                asteroides_destruidos = 0
                asteroides.clear()

        elif estado_actual == "minijuego_asteroides":
            temporizador_spawn += 1
            if temporizador_spawn >= 30 and (asteroides_destruidos + len(asteroides)) < max_asteroides_mision:
                temporizador_spawn = 0
                radio = random.randint(15, 30)
                pos_x = random.randint(50, W_ACTUAL - 50)
                rect_ast = pygame.Rect(pos_x, -40, radio*2, radio*2)
                asteroides.append({
                    'rect': rect_ast,
                    'vel_y': random.randint(3, 6),
                    'vel_x': random.choice([-1, 0, 1])
                })

            for asteroide in asteroides[:]:
                asteroide['rect'].y += asteroide['vel_y']
                asteroide['rect'].x += asteroide['vel_x']
                if asteroide['rect'].y > H_ACTUAL:
                    asteroides.remove(asteroide)

            if asteroides_destruidos >= max_asteroides_mision:
                mision_completada = True
                mostrar_cartel_exito = True
                frames_cartel = 0
                estado_actual = "exploracion"
                x_jugador = int(W_ACTUAL * 0.80)
                y_jugador = int(H_ACTUAL * 0.52)

        if estado_actual == "menu" and video_menu:
            video_menu.update()
            if not video_menu.active:
                video_menu.restart()

        screen.fill((10, 10, 15))

        if estado_actual == "menu":
            if video_menu and video_menu.active:
                frame_superficie = video_menu.frame_surf
                if frame_superficie:
                    frame_escalado = pygame.transform.smoothscale(frame_superficie, (W_ACTUAL, H_ACTUAL))
                    screen.blit(frame_escalado, (0, 0))
            else:
                screen.fill((20, 20, 40))

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

            if fase_narrativa == 4 and assets["rene"]:
                if opacidad_rene < 255: opacidad_rene += 4
                rene_base = assets["rene"].copy()
                rene_base.set_alpha(opacidad_rene)
                
                alt_rene = int(H_ACTUAL * 0.70)
                anc_rene = int(assets["rene"].get_width() * (alt_rene / assets["rene"].get_height()))
                rene_scaled = pygame.transform.smoothscale(rene_base, (anc_rene, alt_rene))
                rene_rect = rene_scaled.get_rect(bottomright=(W_ACTUAL * 0.86, H_ACTUAL - int(H_ACTUAL * 0.15)))
                screen.blit(rene_scaled, rene_rect)

            ancho_caja = int(W_ACTUAL * 0.90)
            alto_caja = int(H_ACTUAL * 0.22)
            caja_rect = pygame.Rect(0, 0, ancho_caja, alto_caja)
            caja_rect.center = (W_ACTUAL // 2, H_ACTUAL - int(H_ACTUAL * 0.14))
            
            pygame.draw.rect(screen, (20, 20, 35), caja_rect, border_radius=8)
            pygame.draw.rect(screen, (0, 200, 220), caja_rect, width=3, border_radius=8)

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
                conteo_frames += 1
                if conteo_frames % 3 == 0 and caracteres_vistos < len(texto_rene_completo):
                    caracteres_vistos += 1
                texto_actual = texto_rene_completo[:caracteres_vistos]
                render_txt = fuente_dialogo.render(texto_actual, True, (240, 240, 255))
                screen.blit(render_txt, (caja_rect.x + 25, caja_rect.y + 35))
                
                tag_nombre = fuente_nombre_tag.render(nombre_jugador, True, (130, 120, 70))
                tag_rect = tag_nombre.get_rect(centerx=astro_rect.centerx, bottom=astro_rect.top + 45)
                screen.blit(tag_nombre, tag_rect)

                if assets["rene"]:
                    tag_rene = fuente_nombre_tag.render("RENÉ", True, (0, 200, 255))
                    tag_rene_rect = tag_rene.get_rect(centerx=rene_rect.centerx, bottom=rene_rect.top - 4)
                    tag_rene_sombra = fuente_nombre_tag.render("RENÉ", True, (0, 0, 0))
                    screen.blit(tag_rene_sombra, (tag_rene_rect.x + 2, tag_rene_rect.y + 2))
                    screen.blit(tag_rene, tag_rene_rect)

                if caracteres_vistos < len(texto_rene_completo):
                    render_ayuda = fuente_sistema.render("[ Click o ENTER para saltear texto ]", True, (0, 180, 180))
                    screen.blit(render_ayuda, (caja_rect.right - 290, caja_rect.bottom - 25))
                else:
                    ancho_btn = 180
                    alto_btn = 40
                    boton_demo_rect = pygame.Rect(0, 0, ancho_btn, alto_btn)
                    boton_demo_rect.bottomright = (caja_rect.right - 25, caja_rect.bottom - 20)
                    
                    color_btn = (0, 230, 150) if boton_demo_rect.collidepoint(pos_mouse) else (0, 160, 100)
                    pygame.draw.rect(screen, color_btn, boton_demo_rect, border_radius=5)
                    
                    fuente_btn = pygame.font.SysFont("Arial", 16, bold=True)
                    txt_btn = fuente_btn.render("INICIAR DEMO", True, (255, 255, 255))
                    txt_btn_rect = txt_btn.get_rect(center=boton_demo_rect.center)
                    screen.blit(txt_btn, txt_btn_rect)

        elif estado_actual == "exploracion":
            if assets["pasillo"]:
                mapa_escalado = pygame.transform.smoothscale(assets["pasillo"], (W_ACTUAL, H_ACTUAL))
                screen.blit(mapa_escalado, (0, 0))
            else:
                screen.fill((40, 40, 60))

            if not mision_completada:
                alfa_alarma += incremento_alarma
                if alfa_alarma >= 110 or alfa_alarma <= 0:
                    incremento_alarma *= -1  
                
                superficie_alarma = pygame.Surface((zona_mision.width, zona_mision.height), pygame.SRCALPHA)
                superficie_alarma.fill((240, 0, 0, max(0, alfa_alarma)))
                screen.blit(superficie_alarma, (zona_mision.x, zona_mision.y))
                
                pygame.draw.rect(screen, (255, 50, 50), zona_mision, width=2)
                
                if alfa_alarma > 35:
                    fuente_alerta = pygame.font.SysFont("Consolas", 11, bold=True)
                    txt_alerta = fuente_alerta.render("¡FALLA DETECTADA!", True, (255, 255, 255))
                    txt_alerta_rect = txt_alerta.get_rect(center=(zona_mision.centerx, zona_mision.centery))
                    screen.blit(txt_alerta, txt_alerta_rect)

            if direccion_jugador == "adelante":
                img_actual = img_adelante if (contador_pasos // 10) % 2 == 0 else img_adelante_espejo
            elif direccion_jugador == "atras":
                img_actual = img_atras if (contador_pasos // 10) % 2 == 0 else img_atras_espejo
            elif direccion_jugador == "derecha":
                img_actual = img_derecha_1 if (contador_pasos // 8) % 2 == 0 else img_derecha_2
            elif direccion_jugador == "izquierda":
                img_actual = img_izquierda_1 if (contador_pasos // 8) % 2 == 0 else img_izquierda_2

            screen.blit(img_actual, (x_jugador, y_jugador))

            if mostrar_cartel_exito:
                frames_cartel += 1
                if frames_cartel < 180:  
                    caja_exito = pygame.Rect(0, 0, 460, 80)
                    caja_exito.center = (W_ACTUAL // 2, 100)
                    pygame.draw.rect(screen, (10, 40, 25), caja_exito, border_radius=6)
                    pygame.draw.rect(screen, (0, 255, 120), caja_exito, width=2, border_radius=6)
                    
                    fuente_exito = pygame.font.SysFont("Consolas", 15, bold=True)
                    txt1 = fuente_exito.render("¡SISTEMAS ESTABILIZADOS!", True, (0, 255, 150))
                    txt2 = fuente_exito.render("Presión de la cabina equilibrada correctamente.", True, (230, 255, 240))
                    
                    screen.blit(txt1, txt1.get_rect(centerx=caja_exito.centerx, top=caja_exito.y + 18))
                    screen.blit(txt2, txt2.get_rect(centerx=caja_exito.centerx, top=caja_exito.y + 42))
                else:
                    mostrar_cartel_exito = False

        elif estado_actual == "minijuego_asteroides":
            pantalla_verde = pygame.Surface((W_ACTUAL, H_ACTUAL), pygame.SRCALPHA)
            pantalla_verde.fill((0, 200, 100, 45))  
            screen.blit(pantalla_verde, (0, 0))

            pygame.draw.rect(screen, (0, 255, 150), (10, 10, W_ACTUAL-20, H_ACTUAL-20), width=4)

            for asteroide in asteroides:
                centro_x = asteroide['rect'].centerx
                centro_y = asteroide['rect'].centery
                radio_dibujo = asteroide['rect'].width // 2
                pygame.draw.circle(screen, (220, 100, 50), (centro_x, centro_y), radio_dibujo)
                pygame.draw.circle(screen, (255, 160, 100), (centro_x, centro_y), radio_dibujo, width=2) 

            fuente_mision = pygame.font.SysFont("Consolas", 24, bold=True)
            txt_mision = fuente_mision.render(f"DESTRUÍDOS: {asteroides_destruidos} / {max_asteroides_mision}", True, (255, 255, 255))
            screen.blit(txt_mision, (30, 30))

            pygame.draw.circle(screen, (0, 255, 255), pos_mouse, 15, width=2)
            pygame.draw.line(screen, (0, 255, 255), (pos_mouse[0] - 22, pos_mouse[1]), (pos_mouse[0] + 22, pos_mouse[1]), 2)
            pygame.draw.line(screen, (0, 255, 255), (pos_mouse[0], pos_mouse[1] - 22), (pos_mouse[0], pos_mouse[1] + 22), 2)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()

