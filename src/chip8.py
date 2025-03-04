import pygame
import random
import time

class Chip8:
    def __init__(self):
        self.mem = [0] * 4096          # 4KB
        self.V = [0] * 16               # V0-VF register (General purpose registers)
        self.I = 0                      # Index register
        self.pc = 0x200
        self.stack = []
        self.delay_timer = 0  #Delay timer register
        self.sound_timer = 0  # Sound timer register
        self.screen = [[0] * 64 for _ in range(32)]  #pixel
        self.keys = [0] * 16
        
        fontset = [
            0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
            0x20, 0x60, 0x20, 0x20, 0x70,  # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
            0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
            0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
            0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
            0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
            0xF0, 0x80, 0xF0, 0x80, 0x80   # F
        ]
        self.mem[0:80] = fontset  # Load fonts into mem

    def load_rom(self, filename):
        # Load the ROM into memory start at 0x200
        with open(filename, "rb") as f:
            rom = f.read()
            for i, byte in enumerate(rom):
                self.mem[0x200 + i] = byte  # Should probably check size, but eh

    def execute_cycle(self):
        opcode = (self.mem[self.pc] << 8) | self.mem[self.pc + 1]
        self.pc += 2  # 2 bytes

        # decoding
        instr = opcode & 0xF000
        X = (opcode & 0x0F00) >> 8  # Getting X register
        Y = (opcode & 0x00F0) >> 4  # Y register
        N = opcode & 0x000F  # Single nibble - 4 bits
        NN = opcode & 0x00FF # Byte operand
        NNN = opcode & 0x0FFF # Address operand

        if instr == 0x0000:
            if opcode == 0x00E0:  # Clear screen
                self.screen = [[0]*64 for _ in range(32)]
            elif opcode == 0x00EE:
                self.pc = self.stack.pop()
            elif opcode == 0x0000:
                pass
        
        elif instr == 0x1000: # JMP to address
            self.pc = NNN

        elif instr == 0x2000: # Call Subroutine
            self.stack.append(self.pc)
            self.pc = NNN

        elif instr == 0x3000: # Skip if VX == NN
            if self.V[X] == NN:
                self.pc += 2

        elif instr == 0x4000: # Skip if VX != NN
            if self.V[X] != NN:
                self.pc += 2

        elif instr == 0x5000:  # Skip if VX == VY
            if self.V[X] == self.V[Y]:
                self.pc += 2
        
        elif instr == 0x6000:
            self.V[X] = NN # Set VX to NN

        elif instr == 0x7000:
            self.V[X] = (self.V[X] + NN) & 0xFF # Add NN to VX (with carry)

        elif instr == 0x8000:
            if (opcode & 0x000F) == 0x0000:
                self.V[X] = self.V[Y] # VX = VY

            elif (opcode & 0x000F) == 0x0001:
                self.V[X] = self.V[X] | self.V[Y]  # VX = VX OR VY

            elif (opcode & 0x000F) == 0x0002:
                self.V[X] = self.V[X] & self.V[Y]  # VX = VX AND VY

            elif (opcode & 0x000F) == 0x0003:
                self.V[X] = self.V[X] ^ self.V[Y]  # VX = VX XOR VY

            elif (opcode & 0x000F) == 0x0004: # Add VY to VX. VF is 1 if carry, 0 if not.
                sum_val = self.V[X] + self.V[Y]
                self.V[0xF] = 1 if sum_val > 255 else 0
                self.V[X] = sum_val & 0xFF

            elif (opcode & 0x000F) == 0x0005: # VX = VX - VY, VF is 0 if borrow, 1 if not
                borrow = 0 if self.V[X] > self.V[Y] else 1
                self.V[0xF] = 1 - borrow  # Set to 1 if no borrow
                self.V[X] = (self.V[X] - self.V[Y]) & 0xFF

            elif (opcode & 0x000F) == 0x0006: # VX = VX SHR 1. VF is the least significant bit of VX before the shift.
                 self.V[0xF] = self.V[X] & 1 # Store LSB in VF
                 self.V[X] = self.V[X] >> 1

            elif (opcode & 0x000F) == 0x0007: # VX = VY - VX.  VF is 0 if borrow, 1 if not.
                 borrow = 0 if self.V[Y] > self.V[X] else 1
                 self.V[0xF] = 1 - borrow # set if no borrow
                 self.V[X] = (self.V[Y] - self.V[X]) & 0xFF

            elif (opcode & 0x000F) == 0x000E:  # VX = VX SHL 1. VF is the most significant bit of VX before the shift.
                 self.V[0xF] = (self.V[X] >> 7) & 1 # Store MSB in VF
                 self.V[X] = (self.V[X] << 1) & 0xFF

        elif instr == 0x9000: # Skip if VX != VY.
            if self.V[X] != self.V[Y]:
                self.pc += 2

        elif instr == 0xA000:
            self.I = NNN # Sets I to the address NNN.

        elif instr == 0xB000: # Jump to location NNN + V0.
            self.pc = NNN + self.V[0]

        elif instr == 0xC000:  # VX = random byte AND NN.
            rand_byte = random.randint(0, 255)
            self.V[X] = rand_byte & NN

        elif instr == 0xD000:  # Display n-byte sprite starting at memory location I at (VX, VY), set VF = collision.
            x = self.V[X] % 64  # Wrap around the screen
            y = self.V[Y] % 32  # Wrap around the screen
            self.V[0xF] = 0  # Reset collision flag
            
            for row in range(N):  # Each row of the sprite
                sprite = self.mem[self.I + row] # Get the row data from memory
                for col in range(8):  # Each bit in the row (each pixel)
                    if (sprite & (0x80 >> col)):  # Check if the pixel should be drawn
                        px = (x + col) % 64  # Calculate screen position, handling wrapping
                        py = (y + row) % 32  # Same but for Y
                        if self.screen[py][px] == 1:
                            self.V[0xF] = 1  # Set collision flag
                        self.screen[py][px] ^= 1  # XOR the pixels on the screen

        elif instr == 0xE000:
            if NN == 0x9E: # Skip next instruction if key with the value of VX is pressed
                if self.keys[self.V[X]]:
                    self.pc += 2
            elif NN == 0xA1: #   not pressed.
                if not self.keys[self.V[X]]:
                    self.pc += 2

        elif instr == 0xF000:
            if NN == 0x07: # VX = get_delay()   VX is set to the value of the delay timer
                self.V[X] = self.delay_timer

            elif NN == 0x0A: # Wait for a key press, store the value of the key in VX.
                key_pressed = False
                while not key_pressed: # Loop until a key is pressed
                    pygame.event.pump() # Process events
                    keys = pygame.key.get_pressed()  # get all pressed keys
                    for i in range(16):
                        if keys[list(Emulator.keymap.keys())[list(Emulator.keymap.values()).index(i)]]: #check key by key
                            self.V[X] = i  # Store key in VX
                            key_pressed = True # Stop looking
                            break  # from inner loop
                time.sleep(0.01) #small delay

            elif NN == 0x15: # set_delay(VX). Delay timer is set to VX.
                self.delay_timer = self.V[X]    

            elif NN == 0x18: # set_sound(VX). Sound timer is set to VX.
                self.sound_timer = self.V[X]      

            elif NN == 0x1E:  # I = I + VX.
                self.I = (self.I + self.V[X]) & 0xFFFF  # carry

            elif NN == 0x29: # I = sprite_addr[VX]. Set I = location of sprite for digit VX.
                self.I = self.V[X] * 5 # Each sprite is 5 bytes long

            elif NN == 0x33: # Store BCD representation of VX in memory locations I, I+1, and I+2.
                 self.mem[self.I] = self.V[X] // 100 # hundreds digit
                 self.mem[self.I + 1] = (self.V[X] // 10) % 10 # tens digit
                 self.mem[self.I + 2] = self.V[X] % 10 # ones digit

            elif NN == 0x55: # Store registers V0 through VX in memory starting at location I.
                for i in range(X + 1):
                    self.mem[self.I + i] = self.V[i]

            elif NN == 0x65:  # Read registers V0 through VX from memory starting at location I.
                for i in range(X + 1):
                    self.V[i] = self.mem[self.I + i]
