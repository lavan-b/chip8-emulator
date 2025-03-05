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
        self.previous_screen = set()
        self.last_tick = pygame.time.get_ticks()
        self.waiting_for_key = False
        self.key_register = None
        
        print('''|       Enter the path to ROM file      |
+---------------------------------------+''')
        self.rom_path = os.path.normpath(input("  > "))  # cleans input
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
        # Chekcs for quitting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        # key event listener
        pressed = pygame.key.get_pressed()
        for k, v in Emulator.keymap.items():
            self.chip8.keys[v] = 1 if pressed[k] else 0
        return True

    def draw_screen(self):
        updated_pixels = set()
        for y in range(32):
            for x in range(64):
                if self.chip8.screen[y][x]:
                    updated_pixels.add((x, y))
                elif (x, y) in self.previous_screen:
                    updated_pixels.add((x, y))

        for x, y in updated_pixels:
            color = (255, 255, 255) if self.chip8.screen[y][x] else (0, 0, 0)
            pygame.draw.rect(self.window, color, (x * 10, y * 10, 10, 10))

        pygame.display.flip()
        self.previous_screen = updated_pixels

    def run(self): # Main code
        try:
            self.chip8.load_rom(self.rom_path)
        except FileNotFoundError:
            print(f"  Error: ROM file not found at {self.rom_path}")
            return
        pygame.display.set_caption(f"CHIP-8 Emulator - Now Playing : {os.path.basename(self.rom_path)}")

        print('''
+---------------------------------------+
|           Running in pygame           |
|           (Press ALT + TAB)           |
+---------------------------------------+''')
        
        running = True
        while running: # the OG loop!
            cycles = int(10 * self.speed_multiplier)
            for _ in range(cycles):
                if not self.handle_input():
                    running = False
                    break

                if self.waiting_for_key: # Process events
                    pygame.event.pump()
                    keys = pygame.key.get_pressed()
                    for i in range(16):
                        if keys[list(Emulator.keymap.keys())[list(Emulator.keymap.values()).index(i)]]:
                            self.chip8.V[self.key_register] = i
                            self.waiting_for_key = False
                            break
                    continue # No key pressed, continue waiting

                result = self.chip8.execute_cycle()
                if result == ("WAIT_FOR_KEY",):
                    self.waiting_for_key = True
                    self.key_register = result[1]
                    continue #skip timers and screen draw

            current_time = pygame.time.get_ticks()  #timer delay controls
            elapsed = current_time - self.last_tick
            if elapsed >= 16:
                self.chip8.delay_timer -= 4 if self.chip8.delay_timer > 0 else 0
                if self.chip8.sound_timer > 0:
                    self.chip8.sound_timer -= 2
                    if self.chip8.sound_timer == 0:
                        winsound.Beep(420, 50)
                self.last_tick = current_time

            self.draw_screen()
            pygame.time.Clock().tick(60) # tick rate

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
