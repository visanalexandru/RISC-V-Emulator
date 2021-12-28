class System:
    def __init__(self):
        self.terminate = False

    def call(self, parameters):
        if parameters[0] == 1:
            self.terminate = True


system = System()
