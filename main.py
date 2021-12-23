from processor import Processor
import parser

instructions = parser.parse("tests/rv32ui-v-beq.mc")
start_location = min(instructions.keys())

print(f"Start location: {hex(start_location)}")

cpu = Processor()
cpu.pc = start_location

while True:
    try:
        instruction = instructions[cpu.pc]
        decoded = cpu.decode(instruction)
    except KeyError:
        print(f"Cannot execute instruction at address: {hex(cpu.pc)}")
        cpu.advance_pc()
        continue

    print(f"Execute {decoded} , OPCODE: {bin(decoded[0])}")
    cpu.execute(decoded)
    cpu.debug_registers()
    input()
