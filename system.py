class SystemException(Exception):  # Throw when an unknown system code is called
    pass


class System:
    def __init__(self):
        self.terminate = False
        self.debug = False

    def call(self, parameters):
        if parameters[0] == 1:
            self.terminate = True
        else:
            raise SystemException(f"Unknown system call: {parameters[0]}")


system = System()
