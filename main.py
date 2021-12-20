from processor import Processor

cpu = Processor()
instruction = 0x00000093 
jal = cpu.decode(instruction)
print(jal)
cpu.execute(jal)
cpu.debug_registers()
