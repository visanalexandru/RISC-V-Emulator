# RISC-V-Emulator

This is an simple RISCV-V machine code emulator. It can parse and emulate a hexdump of a compiled executable.  
The goal of the implementation is to correctly emulate the given [tests](tests/).
You can find the RISC-V core specifications [here](https://riscv.org/wp-content/uploads/2017/05/riscv-spec-v2.2.pdf).

Currently, the emulator can execute the following instructions: 

- [x] [LUI](processor.py#L353) - load upper immediate
- [x] [AUIPC](processor.py#L360) - add upper immediate to pc
- [x] [JAL](processor.py#L369) - jump and link
- [x] [BEQ](processor.py#L384) - branch if equal
- [x] [BNE](processor.py#L386) - branch if not equal
- [x] [ADDI](processor.py#L401) - add immediate
- [x] [SLTI](processor.py#L407) - set less than signed immediate
- [x] [SLTIU](processor.py#L416) - set less than unsigned immediate
- [x] [SLLI](processor.py#L427) - logical shift left by constant
- [x] [ORI](processor.py#L432) - logical or by constant
- [x] [SRL](processor.py#L494) - logical shift right by register value
- [x] [XOR](processor.py#L500) - register-register logical xor 
- [x] [REM](processor.py#L508) - register-register remainder operation 
- [x] [ECALL](processor.py#L443) - system call instruction
- [x] [LW](processor.py#L457) - load word from memory
- [x] [SW](processor.py#L474) - store word to memory
