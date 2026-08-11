class Cell:
    """
    Minimal cloud state unit.
    """

    def __init__(self):

        self.value = None

        self.age = 0

        self.activity = 0.0


    @property
    def empty(self):

        return self.value is None


    def occupy(
        self,
        value
    ):

        self.value = float(value)

        self.age = 0

        self.activity = abs(
            self.value
        )


    def release(self):

        self.value = None

        self.age = 0

        self.activity = 0.0