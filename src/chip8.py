import random

class Chip8:
    def __init__(self):
        self.mem = [0] * 4096          # 4KB memory
        self.V = [0] * 16              # V0-VF registers
        self.I = 0                     # Index register
        self.pc = 0x200                # Program counter starts at 0x200
        self.stack = []                 # Stack for subroutine calls
        self.delay_timer = 0           # Delay timer
        self.sound_timer = 0           # Sound timer
        self.screen = [[0] * 64 for _ in range(32)]  # 64x32 pixel screen
        self.keys = [0] * 16           # Key states
        self.screen_modified = False   # Track if screen needs redraw

        # Load fontset into memory (0x000-0x080)
        fontset = [
            0xF0, 0x90, 0x90, 0x90, 0xF0, 0x20, 0x60, 0x20, 0x20, 0x70,
            0xF0, 0x10, 0xF0, 0x80, 0xF0, 0xF0, 0x10, 0xF0, 0x10, 0xF0,
            0x90, 0x90, 0xF0, 0x10, 0x10, 0xF0, 0x80, 0xF0, 0x10, 0xF0,
            0xF0, 0x80, 0xF0, 0x90, 0xF0, 0xF0, 0x10, 0x20, 0x40, 0x40,
            0xF0, 0x90, 0xF0, 0x90, 0xF0, 0xF0, 0x90, 0xF0, 0x10, 0xF0,
            0xF0, 0x90, 0xF0, 0x90, 0x90, 0xE0, 0x90, 0xE0, 0x90, 0xE0,
            0xF0, 0x80, 0x80, 0x80, 0xF0, 0xE0, 0x90, 0x90, 0x90, 0xE0,
            0xF0, 0x80, 0xF0, 0x80, 0xF0, 0xF0, 0x80, 0xF0, 0x80, 0x80
        ]
        self.mem[0:80] = fontset

    def load_rom(self, filename):
        with open(filename, "rb") as f:
            rom = f.read()
            start = 0x200
            end = start + len(rom)
            self.mem[start:end] = list(rom)  # Efficient slice assignment

    def execute_cycle(self):
        opcode = (self.mem[self.pc] << 8) | self.mem[self.pc + 1]
        self.pc += 2

        # Decode opcode
        X = (opcode & 0x0F00) >> 8
        Y = (opcode & 0x00F0) >> 4
        N = opcode & 0x000F
        NN = opcode & 0x00FF
        NNN = opcode & 0x0FFF

        if (opcode & 0xF000) == 0x0000:
            if opcode == 0x00E0:
                self.screen = [[0]*64 for _ in range(32)]
                self.screen_modified = True
            elif opcode == 0x00EE:
                self.pc = self.stack.pop()
        elif (opcode & 0xF000) == 0x1000:
            self.pc = NNN
        elif (opcode & 0xF000) == 0x2000:
            self.stack.append(self.pc)
            self.pc = NNN
        elif (opcode & 0xF000) == 0x3000:
            if self.V[X] == NN:
                self.pc += 2
        elif (opcode & 0xF000) == 0x4000:
            if self.V[X] != NN:
                self.pc += 2
        elif (opcode & 0xF000) == 0x5000:
            if self.V[X] == self.V[Y]:
                self.pc += 2
        elif (opcode & 0xF000) == 0x6000:
            self.V[X] = NN
        elif (opcode & 0xF000) == 0x7000:
            self.V[X] = (self.V[X] + NN) & 0xFF
        elif (opcode & 0xF000) == 0x8000:
            if N == 0x0:
                self.V[X] = self.V[Y]
            elif N == 0x1:
                self.V[X] |= self.V[Y]
            elif N == 0x2:
                self.V[X] &= self.V[Y]
            elif N == 0x3:
                self.V[X] ^= self.V[Y]
            elif N == 0x4:
                total = self.V[X] + self.V[Y]
                self.V[0xF] = 1 if total > 255 else 0
                self.V[X] = total & 0xFF
            elif N == 0x5:
                self.V[0xF] = 1 if self.V[X] > self.V[Y] else 0
                self.V[X] = (self.V[X] - self.V[Y]) & 0xFF
            elif N == 0x6:
                self.V[0xF] = self.V[X] & 0x1
                self.V[X] >>= 1
            elif N == 0x7:
                self.V[0xF] = 1 if self.V[Y] > self.V[X] else 0
                self.V[X] = (self.V[Y] - self.V[X]) & 0xFF
            elif N == 0xE:
                self.V[0xF] = (self.V[X] >> 7) & 0x1
                self.V[X] = (self.V[X] << 1) & 0xFF
        elif (opcode & 0xF000) == 0x9000:
            if self.V[X] != self.V[Y]:
                self.pc += 2
        elif (opcode & 0xF000) == 0xA000:
            self.I = NNN
        elif (opcode & 0xF000) == 0xB000:
            self.pc = NNN + self.V[0]
        elif (opcode & 0xF000) == 0xC000:
            self.V[X] = random.randint(0, 255) & NN
        elif (opcode & 0xF000) == 0xD000:
            x = self.V[X] & 0x3F  # Wrap using bitwise AND
            y = self.V[Y] & 0x1F
            self.V[0xF] = 0
            for row in range(N):
                sprite = self.mem[(self.I + row) % 4096]  # Wrap memory access
                for col in range(8):
                    if sprite & (0x80 >> col):
                        px = (x + col) & 0x3F
                        py = (y + row) & 0x1F
                        if self.screen[py][px]:
                            self.V[0xF] = 1
                        self.screen[py][px] ^= 1
            self.screen_modified = True
        elif (opcode & 0xF000) == 0xE000:
            if NN == 0x9E and self.keys[self.V[X]]:
                self.pc += 2
            elif NN == 0xA1 and not self.keys[self.V[X]]:
                self.pc += 2
        elif (opcode & 0xF000) == 0xF000:
            if NN == 0x07:
                self.V[X] = self.delay_timer
            elif NN == 0x0A:
                return ("WAIT_FOR_KEY", X)
            elif NN == 0x15:
                self.delay_timer = self.V[X]
            elif NN == 0x18:
                self.sound_timer = self.V[X]
            elif NN == 0x1E:
                self.I = (self.I + self.V[X]) & 0xFFFF
            elif NN == 0x29:
                self.I = self.V[X] * 5
            elif NN == 0x33:
                self.mem[self.I] = self.V[X] // 100
                self.mem[self.I + 1] = (self.V[X] % 100) // 10
                self.mem[self.I + 2] = self.V[X] % 10
            elif NN == 0x55:
                for i in range(X + 1):
                    self.mem[self.I + i] = self.V[i]
            elif NN == 0x65:
                for i in range(X + 1):
                    self.V[i] = self.mem[self.I + i]
        return None
