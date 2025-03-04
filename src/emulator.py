import os
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

        # Key mapping (QWERTY Keyboard -> CHIP-8 Keypad)
        self.keymap = {
            pygame.K_1: 0x1, pygame.K_2: 0x2, pygame.K_3: 0x3, pygame.K_4: 0xC,
            pygame.K_q: 0x4, pygame.K_w: 0x5, pygame.K_e: 0x6, pygame.K_r: 0xD,
            pygame.K_a: 0x7, pygame.K_s: 0x8, pygame.K_d: 0x9, pygame.K_f: 0xE,
            pygame.K_z: 0xA, pygame.K_x: 0x0, pygame.K_c: 0xB, pygame.K_v: 0xF
        }


    def handle_input(self):
        self.chip8.keys = [0] * 16  # Reset key states
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
                if event.key in self.keymap:
                    key = self.keymap[event.key]
                    self.chip8.keys[key] = 1 if event.type == pygame.KEYDOWN else 0
        return True

    def draw_screen(self):
        self.screen.fill((0, 0, 0))  # Clear screen (black)
        for y in range(32):
            for x in range(64):
                if self.chip8.screen[y][x]:  # If pixel is ON
                    rect = pygame.Rect(x * self.scale, y * self.scale, self.scale, self.scale)
                    pygame.draw.rect(self.screen, (255, 255, 255), rect)  # White pixel
        pygame.display.flip()

    def run(self, rom_path):
        self.chip8.load_rom(rom_path)

        # Extract filename without path
        rom_name = os.path.basename(rom_path)
        pygame.display.set_caption(f"CHIP-8 Emulator is Now Playing : {rom_name}")

        running = True
        while running:
            running = self.handle_input()
            self.chip8.execute_cycle()
            self.draw_screen()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    path = input("Enter ROM file name or path (without quotes): ")
    Emulator().run(path)
