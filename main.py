from processor import Processor 


cpu = Processor()
instruction = 0x00108713
jal = cpu.decode(instruction)
print(jal)
cpu.debug_registers()

