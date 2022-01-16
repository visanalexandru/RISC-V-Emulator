# RISC-V-Emulator

This is an simple RISCV-V machine code emulator. It can parse and emulate a hexdump of a compiled executable.  
The goal of the implementation is to correctly emulate the given [tests](tests/).
You can find the RISC-V core specifications [here](https://riscv.org/wp-content/uploads/2017/05/riscv-spec-v2.2.pdf).

Currently, the emulator can execute the following instructions: 

- [x] [LUI](processor.py#L354) - load upper immediate
- [x] [AUIPC](processor.py#L361) - add upper immediate to pc
- [x] [JAL](processor.py#L370) - jump and link
- [x] [BEQ](processor.py#L385) - branch if equal
- [x] [BNE](processor.py#L387) - branch if not equal
- [x] [ADDI](processor.py#L402) - add immediate
- [x] [SLTI](processor.py#L408) - set less than signed immediate
- [x] [SLTIU](processor.py#L417) - set less than unsigned immediate
- [x] [SLLI](processor.py#L428) - logical shift left by constant
- [x] [ORI](processor.py#L433) - logical or by constant
- [x] [SRL](processor.py#L495) - logical shift right by register value
- [x] [XOR](processor.py#L501) - register-register logical xor 
- [x] [REM](processor.py#L509) - register-register remainder operation 
- [x] [ECALL](processor.py#L444) - system call instruction
- [x] [LW](processor.py#L458) - load word from memory
- [x] [SW](processor.py#L475) - store word to memory


## Implementation details

You can see how each CPU cycle is executed [here](processor.py#L121).  
The program memory is simulated using a big byte array. The class that manages the memory can be found [here](memory.py).  

Each cycle, a new instruction is fetched from memory, by reading a new 32-bit WORD from the address given by PC. 
Next, the CPU [decodes](processor.py#L136) the new instruction and [executes](processor.py#L327) it.
