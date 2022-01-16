# RISC-V-Emulator

This is an simple RISCV-V machine code emulator. It can parse and emulate a hexdump of a compiled executable.  
The goal of the implementation is to correctly emulate the given [tests](tests/).
You can find the RISC-V core specifications [here](https://riscv.org/wp-content/uploads/2017/05/riscv-spec-v2.2.pdf)

Currently, the emulator can execute the following instructions: 

- [x] LUI - load upper immediate
- [x] AUIPC - add upper immediate to pc
- [x] JAL - jump and link
- [x] BEQ - branch if equal
- [x] BNE - branch if not equal
- [x] ADDI - add immediate
- [x] SLTI - set less than signed immediate
- [x] SLTIU - set less than unsigned immediate
- [x] SLLI - logical shift left by constant
- [x] ORI - logical or by constant
- [x] SRL - logical shift right by register value
- [x] XOR - register-register logical xor 
- [x] REM - register-register remainder operation 
- [x] ECALL - system call instruction
- [x] LW - load word from memory
- [x] SW - store word to memory
