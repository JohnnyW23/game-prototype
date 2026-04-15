import pygame, sys
from settings import *
from level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Huntersight')
        self.clock = pygame.time.Clock()

        self.level = Level()
        
    
    def run(self):
        while True:

            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                self.level.player.handle_running(e)
            

            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()