class Cell:

    def __init__(self, id):
        self.id = id

        self.phase = 0.0
        self.energy = 1.0

        self.memory = 0.0

        self.age = 0


    def step(self, influence):

        self.phase += (
            0.05
            + influence * 0.01
        )

        self.energy *= 0.999

        self.memory += (
            influence * 0.001
        )

        self.age += 1