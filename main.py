from processor import Processor 


cpu = Processor()
instruction = 0x00c0006f
jal = cpu.decode(instruction)
print(jal)
cpu.debug_registers()

