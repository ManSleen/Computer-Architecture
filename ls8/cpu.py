"""CPU functionality."""

import sys

# ALU OPERATIONS
ADD = 0b10100000  # Takes 2 parameters : 00000aaa 00000bbb
SUB = 0b10100001  # Takes 2 parameters : 00000aaa 00000bbb
MUL = 0b10100010  # Takes 2 parameters : 00000aaa 00000bbb
DIV = 0b10100011  # Takes 2 parameters : 00000aaa 00000bbb
MOD = 0b10100100  # Takes 2 parameters : 00000aaa 00000bbb
INC = 0b01100101  # Takes 1 parameters : 00000rrr
DEC = 0b01100110  # Takes 1 parameters : 00000rrr
CMP = 0b10100111  # Takes 2 parameters : 00000aaa 00000bbb
AND = 0b10101000  # Takes 2 parameters : 00000aaa 00000bbb
NOT = 0b01101001  # Takes 1 parameters : 00000rrr
OR = 0b10101010  # Takes 2 parameters : 00000aaa 00000bbb
XOR = 0b10101011  # Takes 2 parameters : 00000aaa 00000bbb
SHL = 0b10101100  # Takes 2 parameters : 00000aaa 00000bbb
SHR = 0b10101101  # Takes 2 parameters : 00000aaa 00000bbb

# PC MUTATORS
CALL = 0b01010000  # Takes 1 parameter 00000rrr
RET = 0b00010001  # Takes 1 parameter
INT = 0b01010010  # Takes 1 parameter 00000rrr
IRET = 0b00010011  # Takes 1 parameter
JMP = 0b01010100  # Takes 1 parameter 00000rrr
JEQ = 0b01010101  # Takes 1 parameter 00000rrr
JNE = 0b01010110  # Takes 1 parameter 00000rrr
JGT = 0b01010111  # Takes 1 parameter 00000rrr
JLT = 0b01011000  # Takes 1 parameter 00000rrr
JLE = 0b01011001  # Takes 1 parameter 00000rrr
JGE = 0b01011010  # Takes 1 parameter 00000rrr


# OTHER PROGRAMS
# No-op
NOP = 0b00000000  # Takes no parameters

# Halt
HLT = 0b00000001  # Takes no parameters

# LDI Register Immediate
# Set the value of a register to an integer.
# Parameter 1: Register #
# Parameter 2: Value to store in register
LDI = 0b10000010  # Takes 2 parameters

LD = 0b10000011  # Takes 2 parameters
ST = 0b10000100  # Takes 2 parameters

PUSH = 0b01000101  # Takes 1 parameter
POP = 0b01000110  # Takes 1 parameter

# Print
# Print numeric value stored in the given register.
PRN = 0b01000111  # Takes 1 parameter
PRA = 0b01001000  # Takes 1 parameter


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = {}
        self.reg = [0] * 8
        self.reg[7] = 0xf4
        self.pc = 0

    def load(self):
        """Load a program into memory."""
        filename = sys.argv[1]

        address = 0

        # Read the file
        with open(filename) as f:
            for line in f:
                n = line.split("#")
                n[0] = n[0].strip()

                if n[0] is "":
                    continue

                instruction = int(n[0], 2)
                self.ram_write(address, instruction)
                address += 1

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, instruction):
        self.ram[address] = instruction

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op is "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op is "SUB":
            self.reg[reg_a] -= self.reg[reg_b]

        elif op is "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op is "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
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

        while running:
            instruction = self.ram_read(self.pc)

            if instruction is HLT:
                running = False

            elif instruction is LDI:
                register_number = self.ram_read(self.pc + 1)
                number_to_save = self.ram_read(self.pc + 2)
                self.reg[register_number] = number_to_save
                self.pc += 3

            elif instruction is PRN:
                register_number = self.ram_read(self.pc + 1)
                number_to_print = self.reg[register_number]
                print(number_to_print)
                self.pc += 2

            elif instruction is MUL:
                register_a = self.ram_read(self.pc + 1)
                register_b = self.ram_read(self.pc + 2)
                self.alu("MUL", register_a, register_b)
                self.pc += 3

            else:
                print(f"Unknown instruction at index {self.pc}")
                sys.exit(1)
