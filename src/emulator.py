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
            self.chip8.execute_cycle()
            self.draw_screen()
            self.clock.tick(60)

        pygame.quit()

    def draw_screen(self):
        self.screen.fill((0, 0, 0))  # Clear screen (black)
        for y in range(32):
            for x in range(64):
                if self.chip8.screen[y][x]:  # If pixel is ON
                    rect = pygame.Rect(x * self.scale, y * self.scale, self.scale, self.scale)
                    pygame.draw.rect(self.screen, (255, 255, 255), rect)  # White pixel
        pygame.display.flip()


if __name__ == "__main__":
    Emulator().run()
