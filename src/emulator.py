# emulate.py
import pygame
import time
import winsound
import os
import shlex # Add import
from chip8 import Chip8  # Import the Chip8 class

class Emulator:
    def __init__(self, scale=10): #rom_path="d:/breakout.ch8"
        pygame.init()
        self.scale = scale
        self.window = pygame.display.set_mode((64 * scale, 32 * scale))  # Make it actual size
        pygame.display.set_caption("Chip-8 Emulator")  # Set title bar
        self.clock = pygame.time.Clock()
        self.chip8 = Chip8()
        #Get file path input
        rom_path = input("Enter the path to the ROM file: ")
        try:
            self.rom_path = shlex.split(rom_path)[0] # Splits path ensuring it is a single element and handles quoting.
        except:
            print("Invalid Path, Exiting...") #error catching
            exit()

        Emulator.keymap = {
            pygame.K_1: 0x1,
            pygame.K_2: 0x2,
            pygame.K_3: 0x3,
            pygame.K_4: 0xC,
            pygame.K_q: 0x4,
            pygame.K_w: 0x5,
            pygame.K_e: 0x6,
            pygame.K_r: 0xD,
            pygame.K_a: 0x7,
            pygame.K_s: 0x8,
            pygame.K_d: 0x9,
            pygame.K_f: 0xE,
            pygame.K_z: 0xA,
            pygame.K_x: 0x0,
            pygame.K_c: 0xB,
            pygame.K_v: 0xF
        }
        self.waiting_for_key = False
        self.key_register = None
        self.speed_multiplier = float(input("Enter the emulation speed multiplier (e.g., 1.0, 0.5, 2.0): ")) #get input

    def handle_input(self):
        # Chekcs for quitting and key press
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False # exits

        # key event listener
        pressed = pygame.key.get_pressed()
        for key, value in Emulator.keymap.items():
            self.chip8.keys[value] = 1 if pressed[key] else 0 # Sets to 1 if key is pressed

        return True #still running

    def draw_screen(self):

        self.window.fill((0, 0, 0))
        for y in range(32):
            for x in range(64):
                if self.chip8.screen[y][x]:
                    pygame.draw.rect(self.window, (255,255,255),
                                   (x*self.scale, y*self.scale, self.scale, self.scale))
        pygame.display.flip()

    def run(self, speed=300):
        # Main emulation
        try: #Catches error if file doesn't exist.
            self.chip8.load_rom(self.rom_path)
        except FileNotFoundError:
            print(f"Error: ROM file not found at {self.rom_path}")
            return  # Exit if the ROM file isn't found
        rom_name = os.path.basename(self.rom_path)
        pygame.display.set_caption(f"CHIP-8 Emulator - Now Playing : {rom_name}")

        running = True

        # MAIN LOOP
        while running:
            cycles = int((speed // 60) * self.speed_multiplier) #apply multiplier
            for _ in range(cycles):
                if not self.handle_input():
                    running = False
                    break

                if self.waiting_for_key:
                    pygame.event.pump()  # Process events
                    keys = pygame.key.get_pressed()
                    for i in range(16):
                        if keys[list(Emulator.keymap.keys())[list(Emulator.keymap.values()).index(i)]]:
                            self.chip8.V[self.key_register] = i
                            self.waiting_for_key = False  # Key pressed, continue
                            break
                    else:
                        continue  # No key pressed, continue waiting
                else:
                   result = self.chip8.execute_cycle()
                   if result == ("WAIT_FOR_KEY",):
                       self.waiting_for_key = True
                       self.key_register = result[1]
                       continue #skip timers and screen draw

            #timers delay and sound
            if self.chip8.delay_timer > 0:  # If delay timer is active
                self.chip8.delay_timer -= 1
            if self.chip8.sound_timer > 0:  # If sound timer is active
                self.chip8.sound_timer -= 1
                if self.chip8.sound_timer == 0:
                    winsound.Beep(440, 60)

            self.draw_screen()
            self.clock.tick(144)  # display fps

if __name__ == "__main__":
    emu = Emulator(scale=10)
    emu.run()
