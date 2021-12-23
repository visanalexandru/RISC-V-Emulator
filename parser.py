# Parse the instructions from the given file and return a dictionary of < key: location , value: instruction >
def parse(filename):
    to_return = {}

    with open(filename, "r") as file:
        for line in file:
            line = line.replace(":", " ")
            tokens = line.split()

            try:
                address = int(tokens[0], 16)
                value = int(tokens[1], 16)
                to_return[address] = value
            except ValueError:
                pass

    return to_return
