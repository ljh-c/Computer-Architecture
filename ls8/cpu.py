"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # holds 256 bytes of memory
        self.ram = [0] * 256
        # 8 general-purpose registers
        self.reg = [0] * 8
        # program counter, special-purpose register
        self.pc = 0

    def load(self, file_path: str):
        """Load a program into memory."""
        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        with open(file_path) as file:
            for line in file.readlines():
                if line == '\n' or line[0] == '#':
                    continue
                else:
                    self.ram[address] = int(line[:8], 2)
                    address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        # instruction to opcode
        HLT = 0b00000001 # Exit emulator
        LDI = 0b10000010 # Set value of register
        PRN = 0b01000111 # Print value at register

        while running:
            # read the memory address stored in register PC
            # then store in ir, the instruction register
            ir = self.ram_read(self.pc)

            # read bytes at PC+1 and PC+2 in case instruction needs them
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == HLT:
                running = False
                self.pc += 1

            elif ir == LDI:
                self.ram_write(operand_a, operand_b)
                self.pc += 3

            elif ir == PRN:
                print(self.ram_read(operand_a))
                self.pc += 2

            else:
                print(f'Unknown instruction {ir} at address {self.pc}')
                sys.exit(1)

    def ram_read(self, address: int):
        """Return the value stored at the address."""
        return self.ram[address]
    
    def ram_write(self, address: int, data):
        self.ram[address] = data