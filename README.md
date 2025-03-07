# CHIP-8 Emulator

A simple CHIP-8 emulator built using Python and Pygame.

## Features
✔ Loads CHIP-8 ROMs

✔ Executes opcodes

✔ Renders graphics using pygame

✔ Supports keyboard input

✔ Implements timers and sound

## The Process

# 1. Understanding CHIP-8 Architecture

Researched CHIP-8, its memory structure, registers, opcodes, and display mechanics.

Studied how CHIP-8 interpreters work and how they execute instructions.



# 2. Finding a Reference Implementation

Discovered a CHIP-8 emulator written in C from this GitHub repository.

Analyzed its structure, key functions, and overall implementation.



# 3. Converting the C Code to Python

Used the C implementation as a reference to understand how the emulator processes opcodes.

With AI assistance, rewrote the core logic in Python while ensuring readability and maintainability.



# 4. Implementing Key Components in Python

Memory & Registers: Defined memory, registers, stack, and program counter in Python.

Opcode Handling: Implemented opcode fetching, decoding, and execution.

Display: Used a Python library (such as Pygame) to handle graphics rendering.

Input Handling: Mapped CHIP-8 keys to modern keyboard inputs.

Timers: Implemented delay and sound timers using Python’s timing functions.



# 5. Testing and Debugging

Ran multiple CHIP-8 ROMs to check opcode execution accuracy.

Debugged and fixed issues related to rendering, input, and opcode behavior.



# 6. Final Improvements

Optimized performance for smooth execution.

Cleaned up the code and improved structure for maintainability.

Verified functionality with additional CHIP-8 programs.

## Controls (QWERTY Keyboard → CHIP-8 Keys)
```
1 2 3 4      →     1 2 3 C
Q W E R      →     4 5 6 D
A S D F      →     7 8 9 E
Z X C V      →     A 0 B F
```
