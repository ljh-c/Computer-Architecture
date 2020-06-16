"""CPU functionality."""

import sys

# instruction to opcode
HLT = 0b00000001 # Exit emulator
LDI = 0b10000010 # Set value of register
PRN = 0b01000111 # Print value at register
MUL = 0b10100010 # Multiply values of two registers

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

        self.running = False

    def handle_hlt(self, a, b):
        self.running = False
        self.pc += 1

    def handle_ldi(self, a, b):
        self.reg[a] = b
        self.pc += 3

    def handle_prn(self, a, b):
        print(self.reg[a])
        self.pc += 2

    def handle_mul(self, a, b):
        self.alu('MUL', a, b)
        self.pc += 3

    def exec(self, instruction, a=None, b=None):
        # set up branch table
        dispatch = {
            HLT: self.handle_hlt,
            LDI: self.handle_ldi,
            PRN: self.handle_prn,
            MUL: self.handle_mul
        }

        dispatch[instruction](a, b)

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
            for line in file:
                if line == '\n' or line[0] == '#':
                    continue
                else:
                    self.ram[address] = int(line.split()[0], 2)

                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        # arithmetic logic unit

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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
        self.running = True

        while self.running:
            # read the memory address stored in register PC
            # then store in ir, the instruction register
            ir = self.ram_read(self.pc)

            # read bytes at PC+1 and PC+2 in case instruction needs them
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            self.exec(ir, operand_a, operand_b)

            # try:
            #     self.exec(ir, operand_a, operand_b)
            # except:
            #     print(f'Unknown instruction {ir} at address {self.pc}')
            #     sys.exit(1)
            
            # n_operands = ir & 0b11000000 >> 6
            # n_move_pc = n_operands + 1
            # self.pc += n_move_pc

    def ram_read(self, address: int):
        """Return the value stored at the address."""
        return self.ram[address]
    
    def ram_write(self, address: int, data):
        self.ram[address] = data