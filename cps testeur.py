#cps testeur

import pygame
import threading
import time

#parametrage jeu/fenetre
pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Cps Test")

#definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHT_RED = (255, 50, 50)
ORANGE = (255, 255, 0)

running = True
chrono_start = None
font = pygame.font.Font(None, 36)
nb_clics = 0

#para son
son_lock = threading.Lock()
son_clic_souris = "ressources/clic_souris.mp3"

#para icone
icon = pygame.image.load("ressources/curseur_en_feu.ico")
pygame.display.set_icon(icon)

def jouer_son(fichier_audio):
    with son_lock:  # Bloquer l'accès aux autres threads
        pygame.mixer.music.load(fichier_audio)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # Attendre la fin du son
            pygame.time.wait(1)  # Attendre 

# Fonction pour jouer un son dans un thread
def jouer_son_dans_thread(fichier_audio):
    threading.Thread(target=jouer_son, args=(fichier_audio,), daemon=True).start()

def draw_button(screen, color, rect, text):
    pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (rect[0] + (rect[2] - text_surface.get_width()) // 2,
                               rect[1] + (rect[3] - text_surface.get_height()) // 2))

def setup_jeu():
    global nb_clics
    if nb_clics ==0:
        debut_chrono = time.time() 
    print("Bouton cliqué",nb_clics)
    nb_clics=nb_clics+1

def clic_bouton():
    global nb_clics 
    print("Bouton cliqué",nb_clics)
    jouer_son_dans_thread(son_clic_souris)
    nb_clics=nb_clics+1

while running:
    screen.fill(WHITE)
    if chrono_start is None:
        chrono_start = time.time()  # Démarrer le chrono au début
    chrono = time.time() - chrono_start

    button_rect = pygame.Rect(150, 200, 200, 50)
    mouse_pos = pygame.mouse.get_pos()

    # Vérifier si la souris est sur le bouton
    if button_rect.collidepoint(mouse_pos):
        button_color = LIGHT_RED 
    else:
        button_color = RED
    draw_button(screen, button_color, button_rect, "clic_bouton")

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(mouse_pos):
                clic_bouton()

    pygame.display.flip() #update l'ecran 
pygame.quit()                                                