import pygame
from chip8 import Chip8

class Emulator:
    def __init__(self, scale=10):
        pygame.init()
        self.scale = scale
        self.screen = pygame.display.set_mode((64 * scale, 32 * scale))
        pygame.display.set_caption("CHIP-8 Emulator")
        self.clock = pygame.time.Clock()
        self.chip8 = Chip8()
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.fill((0, 0, 0))  # Black screen
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    Emulator().run()
