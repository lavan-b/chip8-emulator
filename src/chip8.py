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
