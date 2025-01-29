import pygame
import sys
from pygame.locals import *
import c_to_py_threading as c_py
import globals
import py_to_c_threading as py_c
py_c.start_periodic_sender("distant.txt", "127.0.0.1", globals.port_send)


def start_game(start_from_loading_flag = 0):

    # pygame.init()
    import affichage_2_5D_isometric as aff_iso
    import sauvegarde as sauv
    
    # Initialisation pygame, surfaces, etc. déjà présentes dans votre code
    tick_graphic = 0

    # On demande les ports en console (comme dans votre code)
    port_receiver = int(input("port receiver"))  
    globals.port_send = int(input("port sender"))

    # *** NOUVEAU *** on lance le thread d'écoute sur 'port_receiver'
    c_py.start_network_listener(port_receiver)
    print(f"Thread d'écoute réseau démarré sur le port {port_receiver}.")

    # Initialisations de la grille, etc.
    if start_from_loading_flag == 0 :
        aff_iso.configuration.config_grid.init_grid()
        print("load with initialisation")
    aff_iso.redefinition_surface()
    aff_iso.set_theme(aff_iso.configuration.config_affichage.themeiso)

    aff_iso.draw_initial_grid_v2(aff_iso.configuration.config_grid)

    run = True
    while run:
        sauv.save = aff_iso.configuration
        for event in pygame.event.get():
            if event.type == aff_iso.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == aff_iso.KEYUP:
                if event.key == aff_iso.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == aff_iso.MOUSEMOTION:
                if event.buttons[0] == 1:
                    aff_iso.grid_offset_x += event.rel[0]
                    aff_iso.grid_offset_y += event.rel[1]
            elif event.type == pygame.MOUSEMOTION:
                aff_iso.bouton.survol = aff_iso.bouton.rect.collidepoint(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Vérifier si le bouton a été cliqué
                if aff_iso.bouton.rect.collidepoint(event.pos):
                    aff_iso.bouton.fonction()
            elif event.type==KEYDOWN and event.key == K_SPACE:
                Pause = True
                while Pause:
                    for event in pygame.event.get():
                        if event.type==KEYDOWN and event.key == K_SPACE:
                            Pause = False
                            #modif après édition
                            pygame.event.clear()
                            break

           
        
        if tick_graphic >= aff_iso.configuration.config_affichage.nombredefps / aff_iso.configuration.config_affichage.vitesse_actualisation:
            aff_iso.configuration.config_grid.action_bob_speed()
            tick_graphic = 0
       
        aff_iso.draw_full_grid_v2(aff_iso.configuration.config_grid , port_receiver)
        aff_iso.draw_visible_grid (aff_iso.grid_offset_x, aff_iso.grid_offset_y)
        aff_iso.displaysurf.blit(aff_iso.screen_surface, (0, 0))
        aff_iso.displaysurf.blit(aff_iso.overlay_image,(0,0))
        aff_iso.displaysurf.blit(aff_iso.overlay_image_red,(aff_iso.displaysurf.get_width()-580,0))
        #--------------------------------------AFFICHAGE OVERLAY---------------------------------------------
       

        aff_iso.Render_Text_OverlayTest("Tick : " + str(aff_iso.configuration.config_grid.tick), (255,255,255))
        aff_iso.Render_Text_OverlayTest("Day : " + str(aff_iso.configuration.config_grid.day), (255,255,255), next_down=-1)
        aff_iso.Render_Text_OverlayTest("Nombre de bobs restant : " + str(aff_iso.configuration.config_grid.nombre_bob_actuel), (255,255,255), next_down=2)
        texte_mort1, texte_mort2 = aff_iso.affichage_bob_morts(aff_iso.configuration.config_grid)
        aff_iso.Render_Text_OverlayTest_red(texte_mort1, (255,255,255),next_down=2)
        aff_iso.Render_Text_OverlayTest_red(texte_mort2, (255,255,255),next_down=-2, font=("Arial", 17))

        aff_iso.bouton.dessiner()
        #----------------------------------------------------------------------------------------------------
        pygame.display.set_caption(f"Simulation of Bobs\tFPS: {int(aff_iso.FPSCLOCK.get_fps())}")
        pygame.display.flip()
        tick_graphic += 1
        aff_iso.FPSCLOCK.tick(aff_iso.configuration.config_affichage.nombredefps)
        
