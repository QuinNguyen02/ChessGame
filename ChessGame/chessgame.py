from menu import *
from twoPlayer import*
from OnePlayer import*

def main():
    pygame.init()
    pygame.mixer.init()
    
    continue_game = True
    while continue_game:
        pygame.display.set_mode((500,600))
        pygame.display.set_caption("Xiangqi Chess")
        surface = pygame.display.get_surface()
        menu = Menu(surface)
        setMusic("track3.mp3")
        if menu.play() == 2: # choose 2 players 
            setMusic("track2.mp3")
            pygame.mixer.music.stop()
            pygame.display.set_mode((650,600))
            game = twoPlayer(surface,menu)
            game.play()
        elif menu.play() == 1:
            pygame.mixer.music.stop()
            setMusic("track1.mp3")
            game = onePlayer(surface)
            game.play() 
        elif menu.play() == 0:
            continue_game = False
        
    pygame.quit()

def setMusic(musicfile):
    pygame.mixer.music.load(musicfile)
    pygame.mixer.music.play(-1)

main()

