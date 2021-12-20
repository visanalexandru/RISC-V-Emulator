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

        offset = get_two_complement(jal_10_1 | (jal_11 << 10) | (jal_19_12 << 11) | (jal_20 << 19), 20)

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

        offset = get_two_complement(imm_11_0, 12)

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

        offset = get_two_complement(imm_4_1 | (imm_10_5 << 4) | (imm_11 << 10) | (imm_12 << 11), 12)

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

    # Overwrite the top 20 bits of the destination register and set the other 12 bits to zero
    def execute_lui(self, instruction):
        rd = instruction[1]
        self.registers[rd] = get_two_complement(instruction[2] << 12, self.architecture)

    # Build a 32 bit offset from the 20 bit immediate, add the offset to pc and save
    # the result in the destination register
    def execute_auipc(self, instruction):
        rd = instruction[1]
        offset = get_two_complement(instruction[2] << 12, self.architecture)

        self.pc = ignore_overflow(self.pc + offset, self.architecture)  # Add the offset to pc, and ignore the overflow
        self.registers[rd] = self.pc  # Store the result into rd

    def debug_registers(self):
        for x in range(32):
            print(f"x{x}", self.registers[x])

        print(f"pc:{self.pc}")
