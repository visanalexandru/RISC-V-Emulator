from memory import Memory


def parse(filename):  # Parse the instructions from the given file and return a memory object
    instructions = []

    with open(filename, "r") as file:
        for line in file:
            line = line.replace(":", " ")
            tokens = line.split()

            try:
                address = int(tokens[0], 16)
                value = int(tokens[1], 16)
                instructions.append((address, value))
            except ValueError:
                pass

    begin = instructions[0][0]  # The starting address of the memory
    end = instructions[len(instructions) - 1][0]  # The end address of the memory
    size = end - begin + 16  # Compute the total size of the memory

    to_return = Memory(size, begin)
    for instruction in instructions:
        address, data = instruction
        to_return.write_word(data, address)
    return to_return
