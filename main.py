from processor import Processor
from system import system, SystemException
import parser


def execute_test(filename):
    print(f"Execute test : {filename}")
    memory = parser.parse(filename)
    start_location = memory.start

    system.memory = memory
    system.terminate = False
    # system.debug = True - uncomment this line to debug the registers to stdout

    print(f"Start location: {hex(start_location)}")
    cpu = Processor()
    cpu.pc = start_location

    try:
        while not system.terminate:
            cpu.cycle()
    except SystemException:
        print(f"Test failed: {filename}")
    else:
        print(f"Test passed: {filename}")


to_test = ["tests/rv32ui-v-addi.mc", "tests/rv32ui-v-beq.mc", "tests/rv32ui-v-lw.mc", "tests/rv32ui-v-srl.mc",
           "tests/rv32ui-v-sw.mc", "tests/rv32ui-v-xor.mc", "tests/rv32um-v-rem.mc"]
for test in to_test:
    execute_test(test)
