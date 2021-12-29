from system import system

# LUI instruction opcode
OP_LUI = 0b0110111

# AUIPC instruction opcode
OP_AUIPC = 0b0010111

# JAL instruction opcode
OP_JAL = 0b1101111

# JALR instruction opcode
OP_JALR = 0b1100111

# BRANCH instruction opcode
OP_BRANCH = 0b1100011
BRANCH_FUNCT3_BEQ = 0b000
BRANCH_FUNCT3_BNE = 0b001

# IMM instruction opcode
OP_IMM = 0b0010011
IMM_FUNCT3_ADDI = 0
IMM_FUNCT3_SLTI = 0b010
IMM_FUNCT3_SLTIU = 0b011

# SYSTEM instruction opcode
OP_SYSTEM = 0b1110011
SYSTEM_FUNCT12_ECALL = 0b000000000000

# LOAD instruction opcode
OP_LOAD = 0b0000011
LOAD_FUNCT3_LW = 0b010

# Assembler mnemonics for the registers
mnemonics = ["zero",
             "ra",
             "sp",
             "gp",
             "tp",
             "t0",
             "t1",
             "t2",
             "s0",
             "s1",
             "a0",
             "a1",
             "a2",
             "a3",
             "a4",
             "a5",
             "a6",
             "a7",
             "s2",
             "s3",
             "s4",
             "s5",
             "s6",
             "s7",
             "s8",
             "s9",
             "s10",
             "s11",
             "t3",
             "t4",
             "t5",
             "t6"
             ]


def bit_mask_prefix(n):  # Returns a bitmask that masks the first n bits
    return (1 << n) - 1


def get_two_complement(n, bits):  # Returns the number in two's complement using the given number of bits
    to_return = n
    bitmask = 1 << (bits - 1)

    if n & bitmask:
        to_return -= 2 * bitmask

    return to_return


def ignore_overflow(n, bits):  # Keeps only the first bits of the given number
    return n & bit_mask_prefix(bits)


# This class implements the functionality of a RISC-V 32-bit cpu
class Processor:

    def __init__(self):
        self.architecture = 32  # how many bits per register

        self.num_registers = 32  # the number of registers in the cpu

        self.registers = [0] * 32  # the register file, from x0 to x31

        self.pc = 0  # the program counter, holds the address of the current instruction

        self.instruction_size = 4  # how many bytes per instruction

    def advance_pc(self):
        self.pc = ignore_overflow(self.pc + self.instruction_size, self.architecture)

    def cycle(self):
        to_execute = system.memory.read_word(self.pc)  # Fetch a new instruction
        if to_execute == 0:  # There is no instruction at the current address
            print(f"Skipping over memory address:{self.pc}")
            self.advance_pc()
        else:
            decoded = self.decode(to_execute)  # Decode the instruction

            print(f"Execute {decoded} , OPCODE: {bin(decoded[0])}")

            self.execute(decoded)  # Execute the instruction

            self.debug_registers()  # Debug registers to stdout

            input()

    def decode(self, instruction):  # Decodes the instruction and returns the instruction operands

        opcode = instruction & bit_mask_prefix(7)
        instruction >>= 7  # get rid of the first 7 bits that denote the opcode

        if opcode == OP_LUI:
            return self.decode_lui(instruction)
        elif opcode == OP_AUIPC:
            return self.decode_auipc(instruction)
        elif opcode == OP_JAL:
            return self.decode_jal(instruction)
        elif opcode == OP_JALR:
            return self.decode_jalr(instruction)
        elif opcode == OP_BRANCH:
            return self.decode_branch(instruction)
        elif opcode == OP_IMM:
            return self.decode_imm(instruction)
        elif opcode == OP_SYSTEM:
            return self.decode_system(instruction)
        elif opcode == OP_LOAD:
            return self.decode_load(instruction)
        else:
            raise NotImplementedError(f"Cannot decode opcode: {opcode}")

    def decode_lui(self, instruction):  # Decodes a lui instruction
        rd = instruction & bit_mask_prefix(5)
        instruction >>= 5

        imm = instruction & bit_mask_prefix(20)
        instruction >>= 20

        return [OP_LUI, rd, imm]

    def decode_auipc(self, instruction):  # Decodes an auipc instruction
        rd = instruction & bit_mask_prefix(5)
        instruction >>= 5

        imm = instruction & bit_mask_prefix(20)
        instruction >>= 20

        return [OP_AUIPC, rd, imm]

    def decode_jal(self, instruction):  # Decodes a jal instruction
        rd = instruction & bit_mask_prefix(5)
        instruction >>= 5

        jal_19_12 = bit_mask_prefix(8) & instruction
        instruction >>= 8

        jal_11 = bit_mask_prefix(1) & instruction
        instruction >>= 1

        jal_10_1 = bit_mask_prefix(10) & instruction
        instruction >>= 10

        jal_20 = bit_mask_prefix(1) & instruction
        instruction >>= 1

        offset = jal_10_1 | (jal_11 << 10) | (jal_19_12 << 11) | (jal_20 << 19)

        return [OP_JAL, rd, offset]

    def decode_jalr(self, instruction):  # Decodes a jalr instruction
        rd = instruction & bit_mask_prefix(5)
        instruction >>= 5

        funct3 = instruction & bit_mask_prefix(3)
        instruction >>= 3

        rs1 = instruction & bit_mask_prefix(5)
        instruction >>= 5

        imm_11_0 = instruction & bit_mask_prefix(12)
        instruction >>= 12

        offset = imm_11_0

        return [OP_JALR, rd, funct3, rs1, offset]

    def decode_branch(self, instruction):  # Decodes a branch instruction
        imm_11 = instruction & bit_mask_prefix(1)
        instruction >>= 1

        imm_4_1 = instruction & bit_mask_prefix(4)
        instruction >>= 4

        funct3 = instruction & bit_mask_prefix(3)
        instruction >>= 3

        rs1 = instruction & bit_mask_prefix(5)
        instruction >>= 5

        rs2 = instruction & bit_mask_prefix(5)
        instruction >>= 5

        imm_10_5 = instruction & bit_mask_prefix(6)
        instruction >>= 6

        imm_12 = instruction & bit_mask_prefix(1)
        instruction >>= 1

        offset = imm_4_1 | (imm_10_5 << 4) | (imm_11 << 10) | (imm_12 << 11)

        return [OP_BRANCH, offset, funct3, rs1, rs2]

    def decode_imm(self, instruction):  # Decodes an imm instruction
        rd = instruction & bit_mask_prefix(5)
        instruction >>= 5

        funct3 = instruction & bit_mask_prefix(3)
        instruction >>= 3

        rs1 = instruction & bit_mask_prefix(5)
        instruction >>= 5

        imm_11_0 = instruction & bit_mask_prefix(12)
        instruction >>= 12

        return [OP_IMM, rd, funct3, rs1, imm_11_0]

    # Decodes a system instruction. We parse rd,funct3 and rs1 even if they are unused.
    def decode_system(self, instruction):
        rd = instruction & bit_mask_prefix(5)
        instruction >>= 5

        funct3 = instruction & bit_mask_prefix(3)
        instruction >>= 3

        rs1 = instruction & bit_mask_prefix(5)
        instruction >>= 5

        funct12 = instruction & bit_mask_prefix(12)
        instruction >>= 12

        return [OP_SYSTEM, funct12]  # Only funct12 is relevant for this instruction

    def decode_load(self, instruction):  # Decodes a load instruction
        rd = instruction & bit_mask_prefix(5)
        instruction >>= 5

        funct3 = instruction & bit_mask_prefix(3)
        instruction >>= 3

        rs1 = instruction & bit_mask_prefix(5)
        instruction >>= 5

        imm_11_0 = instruction & bit_mask_prefix(12)
        instruction >>= 12

        return [OP_LOAD, rd, funct3, rs1, imm_11_0]

    def execute(self, instruction):  # Executes the given instruction
        opcode = instruction[0]
        if opcode == OP_LUI:
            self.execute_lui(instruction)
        elif opcode == OP_AUIPC:
            self.execute_auipc(instruction)
        elif opcode == OP_JAL:
            self.execute_jal(instruction)
        elif opcode == OP_IMM:
            self.execute_imm(instruction)
        elif opcode == OP_BRANCH:
            self.execute_branch(instruction)
        elif opcode == OP_SYSTEM:
            self.execute_system(instruction)
        elif opcode == OP_LOAD:
            self.execute_load(instruction)
        else:
            raise NotImplementedError(f"Cannot execute opcode: {opcode}")

        # The x0 register is hardwired to zero, so reset it after execution
        self.registers[0] = 0

    # Overwrite the top 20 bits of the destination register and set the other 12 bits to zero
    def execute_lui(self, instruction):
        rd = instruction[1]
        self.registers[rd] = instruction[2] << 12
        self.advance_pc()

    # Build a 32 bit offset from the 20 bit immediate, add the offset to pc and save
    # the result in the destination register
    def execute_auipc(self, instruction):
        rd = instruction[1]
        offset = get_two_complement(instruction[2] << 12, self.architecture)

        self.registers[rd] = ignore_overflow(self.pc + offset, self.architecture)  # Store the result into rd
        self.advance_pc()

    # Add the offset (in multiples of 2 bytes) to the pc and store the address of the instruction
    # following the jump (pc+4) into the destination register
    def execute_jal(self, instruction):
        rd = instruction[1]
        offset = get_two_complement(instruction[2], 20) * 2
        self.pc = ignore_overflow(self.pc + offset, self.architecture)
        self.registers[rd] = self.pc + 4

    # Executes the corresponding branch instruction given by funct3
    def execute_branch(self, instruction):
        offset = get_two_complement(instruction[1], 12) * 2
        funct3 = instruction[2]
        rs1 = instruction[3]
        rs2 = instruction[4]

        jump = False  # Set this flag accordingly based on funct3

        if funct3 == BRANCH_FUNCT3_BEQ:
            jump = self.registers[rs1] == self.registers[rs2]
        elif funct3 == BRANCH_FUNCT3_BNE:
            jump = self.registers[rs1] != self.registers[rs2]

        if jump:
            self.pc = ignore_overflow(self.pc + offset, self.architecture)
        else:
            self.advance_pc()

    # Execute the given imm instruction by computing the corresponding operation given by funct3
    def execute_imm(self, instruction):
        rd = instruction[1]
        funct3 = instruction[2]
        rs1 = instruction[3]
        immediate = instruction[4]

        if funct3 == IMM_FUNCT3_ADDI:
            # Add the sign extended 12-bit immediate to rs1. Ignore overflow and store the result into rd
            value = get_two_complement(immediate, 12)
            result = ignore_overflow(self.registers[rs1] + value, self.architecture)
            self.registers[rd] = result

        elif funct3 == IMM_FUNCT3_SLTI:
            # Set less than immediate, place the value 1 in rd if rs1 is less than the sign-extended immediate,
            # else 0 is written to rd
            value = get_two_complement(immediate, 12)
            if self.registers[rs1] < value:
                self.registers[rd] = 1
            else:
                self.registers[rd] = 0

        elif funct3 == IMM_FUNCT3_SLTIU:
            # Set less than unsigned immediate, similar to SLTI but sign-extends the immediate then
            # treats it and the rs register as unsigned integers
            value = get_two_complement(immediate, 12)
            unsigned_immediate = value & bit_mask_prefix(self.architecture)
            unsigned_register = self.registers[rs1] & bit_mask_prefix(self.architecture)

            if unsigned_register < unsigned_immediate:
                self.registers[rd] = 1
            else:
                self.registers[rd] = 0

        else:
            raise NotImplementedError(f"Cannot execute funct3: {funct3}")
        self.advance_pc()

    # Executes a system call
    def execute_system(self, instruction):
        funct12 = instruction[1]
        if funct12 == SYSTEM_FUNCT12_ECALL:
            system.call(self.registers[10:16])  # The parameters are passed through a0 to a5
        else:
            raise NotImplementedError(f"Cannot execute funct12: {funct12}")

        self.advance_pc()

    # Executes a load instruction
    def execute_load(self, instruction):
        rd = instruction[1]
        funct3 = instruction[2]
        rs1 = instruction[3]
        imm_11_0 = instruction[4]

        if funct3 == LOAD_FUNCT3_LW:
            offset = get_two_complement(imm_11_0, 12)
            address = ignore_overflow(self.registers[rs1] + offset, self.architecture)
            self.registers[rd] = system.memory.read_word(address)
        else:
            raise NotImplementedError(f"Cannot execute funct13: {funct3}")

        self.advance_pc()

    def debug_registers(self):
        for x in range(32):
            print(f"{mnemonics[x]}", self.registers[x])

        print(f"pc:{hex(self.pc)}")
