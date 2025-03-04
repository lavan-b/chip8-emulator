# CHIP-8 Emulator

A simple CHIP-8 emulator built using Python and Pygame.

## Features
✔ Loads CHIP-8 ROMs
✔ Executes opcodes
✔ Renders graphics using pygame
✔ Supports keyboard input
✔ Implements timers and sound

## Installation & Setup
1. **Clone the repository:**
   ```sh
   git clone https://github.com/laavn-b/chip8-emulator.git
   cd chip8-emulator
   ```

2. **Install dependencies:**
   ```sh
   pip install pygame
   ```

3. **Run the emulator with a ROM:**
   ```sh
   python src/emulator.py "path/to/rom.ch8"
   ```

## Controls (QWERTY Keyboard → CHIP-8 Keys)
```
1 2 3 4      → 1 2 3 C
Q W E R      → 4 5 6 D
A S D F      → 7 8 9 E
Z X C V      → A 0 B F
```