import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # remove pygame intro text
import pygame
import winsound
from chip8 import Chip8

class Emulator:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((640, 320), pygame.DOUBLEBUF)
        pygame.display.set_caption("Chip-8 Emulator") # title bar
        self.chip8 = Chip8()
        self.last_tick = pygame.time.get_ticks()
        self.waiting_for_key = False
        self.key_register = None
        icon = pygame.image.load("icon.png")  # Load your icon image (must be a .png)
        pygame.display.set_icon(icon)
        # Initialize screen surface and scaling
        self.screen_surface = pygame.Surface((64, 32))
        self.screen_surface.fill((0, 0, 0))

        print('''|       Enter the path to ROM file      |
+---------------------------------------+''')
        self.rom_path = os.path.normpath(input("  > ")) # cleans input
        print('''+---------------------------------------+
|              Enter speed              |
|      (1 for default, or any float)    |
+---------------------------------------+''')
        self.speed_multiplier = float(input("  > "))

        Emulator.keymap = {
            pygame.K_1: 0x1, pygame.K_2: 0x2, pygame.K_3: 0x3, pygame.K_4: 0xC,
            pygame.K_q: 0x4, pygame.K_w: 0x5, pygame.K_e: 0x6, pygame.K_r: 0xD,
            pygame.K_a: 0x7, pygame.K_s: 0x8, pygame.K_d: 0x9, pygame.K_f: 0xE,
            pygame.K_z: 0xA, pygame.K_x: 0x0, pygame.K_c: 0xB, pygame.K_v: 0xF
        }

    def handle_input(self):
        for event in pygame.event.get():   # Chekcs for quitting
            if event.type == pygame.QUIT:
                return False
        pressed = pygame.key.get_pressed()
        for k, v in Emulator.keymap.items(): # key event listener
            self.chip8.keys[v] = 1 if pressed[k] else 0
        return True

    def draw_screen(self):
        if not self.chip8.screen_modified:
            return
        with pygame.PixelArray(self.screen_surface) as pixels:
            for y in range(32):
                for x in range(64):
                    pixels[x, y] = 0xFFFFFF if self.chip8.screen[y][x] else 0x000000
        scaled_surface = pygame.transform.scale(self.screen_surface, (640, 320))
        self.window.blit(scaled_surface, (0, 0))
        pygame.display.flip()
        self.chip8.screen_modified = False

    def run(self): # main code
        try:
            self.chip8.load_rom(self.rom_path)
        except FileNotFoundError:
            print(f"  Error: ROM file not found at {self.rom_path}")
            return
        pygame.display.set_caption(f"CHIP-8 Emulator - {os.path.basename(self.rom_path)}")

        print('''
+---------------------------------------+
|           Running in pygame           |
|           (Press ALT + TAB)           |
+---------------------------------------+''')
        
        running = True  # the OG loop!
        clock = pygame.time.Clock()
        while running:
            if not self.handle_input():
                running = False
                break

            cycles = int(10 * self.speed_multiplier)
            for _ in range(cycles):
                if self.waiting_for_key:    # Process events
                    pygame.event.pump()
                    for i in range(16):
                        if self.chip8.keys[i]:
                            self.chip8.V[self.key_register] = i
                            self.waiting_for_key = False
                            break
                    continue   #skip timers and screen draw

                result = self.chip8.execute_cycle()
                if result and result[0] == "WAIT_FOR_KEY":
                    self.waiting_for_key = True
                    self.key_register = result[1]

            current_time = pygame.time.get_ticks()     #timer delay controls
            elapsed = current_time - self.last_tick
            if elapsed >= 16:
                self.chip8.delay_timer = max(0, self.chip8.delay_timer - 1)
                if self.chip8.sound_timer > 0:
                    self.chip8.sound_timer = max(0, self.chip8.sound_timer - 1)
                    if self.chip8.sound_timer == 0:
                        winsound.Beep(420, 50)
                self.last_tick = current_time

            self.draw_screen()
            clock.tick(60) # tick rate (kinda fps)

if __name__ == "__main__":
    print('''
+---------------------------------------+
|       WELCOME TO CHIP-8 EMULATOR      |
|           Powered by pygame           |
+---------------------------------------+
| Load your favorite ROMs, enjoy all    |
| classic retro games and have fun!     |
+---------------------------------------+''')
    emu = Emulator()
    emu.run()
