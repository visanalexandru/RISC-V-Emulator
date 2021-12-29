from processor import Processor
from system import system
import parser

memory = parser.parse("tests/rv32ui-v-lw.mc")
start_location = memory.start
system.memory = memory

print(f"Start location: {hex(start_location)}")

cpu = Processor()
cpu.pc = start_location

while not system.terminate:
    cpu.cycle()
