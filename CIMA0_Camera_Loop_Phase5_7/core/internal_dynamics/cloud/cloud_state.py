class CloudState:
    """
    Temporary internal state cloud.

    Responsibility:

        receive disturbance
        maintain transient states
        decay old states


    No:

        interpretation
        decision
        observation
    """


    def __init__(
        self,
        capacity=32
    ):

        self.capacity = capacity

        self.cells = []


    def receive(
        self,
        value
    ):

        self.cells.append(
            {
                "value": value,
                "age": 0
            }
        )


        if len(self.cells) > self.capacity:

            self.cells.pop(0)



    def step(self):

        alive = []


        for cell in self.cells:

            cell["age"] += 1


            if cell["age"] < 80:

                alive.append(cell)


        self.cells = alive



    def snapshot(self):

        return [
            cell.copy()
            for cell in self.cells
        ]