class Chip8:
    def __init__(self):
        self.mem = [0] * 4096  # 4KB only
        self.V = [0] * 16      # 16 Registers from V0 to VF
        self.I = 0             # Index Register
        self.pc = 0x200        # Program starts at 0x200
        self.stack = []        # Stack for async stuffs
        self.delay_timer = 0
        self.sound_timer = 0
        self.screen = [[0] * 64 for _ in range(32)]  # 64x32 res
        self.keys = [0] * 16   # Keypad keys

    def load_rom(self, filename):
        with open(filename, "rb") as f:
            rom = f.read()
            for i, byte in enumerate(rom):
                self.mem[0x200 + i] = byte  # Load ROM into memory starting at 0x200

    def execute_cycle(self):
        # Fetch opcode (2 bytes)
        opcode = (self.mem[self.pc] << 8) | self.mem[self.pc + 1]
        self.pc += 2  # Move to the next instruction

        # Decode
        instr = opcode & 0xF000
        X = (opcode & 0x0F00) >> 8
        Y = (opcode & 0x00F0) >> 4
        N = opcode & 0x000F
        NN = opcode & 0x00FF
        NNN = opcode & 0x0FFF

        # Execute basic opcodes
        if instr == 0x0000:
            if opcode == 0x00E0:  # Clear screen
                self.screen = [[0] * 64 for _ in range(32)]
            elif opcode == 0x00EE:  # Return from subroutine
                self.pc = self.stack.pop()

        elif instr == 0x1000:  # JP NNN (Jump to address)
            self.pc = NNN

        elif instr == 0x2000:  # CALL NNN (Call subroutine)
            self.stack.append(self.pc)
            self.pc = NNN

        elif instr == 0x6000:  # LD VX, NN (Set register VX)
            self.V[X] = NN

        elif instr == 0x7000:  # ADD VX, NN (Add value to register)
            self.V[X] = (self.V[X] + NN) & 0xFF

        # Update timers
        if self.delay_timer > 0:
            self.delay_timer -= 1

        if self.sound_timer > 0:
            if self.sound_timer == 1:
                print("\a")  # System beep
            self.sound_timer -= 1
