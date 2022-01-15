class Memory:
    def __init__(self, size, start):
        self.size = size  # The number of bytes in memory
        self.start = start  # The start address is subtracted from each address
        self.data = bytearray(size)  # The actual data

    def write_word(self, data, address):  # Writes a 32-bit word to the given address
        address -= self.start
        byte_1 = data & 0xff
        data >>= 8

        byte_2 = data & 0xff
        data >>= 8

        byte_3 = data & 0xff
        data >>= 8

        byte_4 = data & 0xff
        data >>= 8

        self.data[address] = byte_1
        self.data[address + 1] = byte_2
        self.data[address + 2] = byte_3
        self.data[address + 3] = byte_4

    def read_word(self, address):  # Reads a 32-bit word from the given address
        address -= self.start
        byte_1 = self.data[address]
        byte_2 = self.data[address + 1]
        byte_3 = self.data[address + 2]
        byte_4 = self.data[address + 3]

        return byte_1 | (byte_2 << 8) | (byte_3 << 16) | (byte_4 << 24)
