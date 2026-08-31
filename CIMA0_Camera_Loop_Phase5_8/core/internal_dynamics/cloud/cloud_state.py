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
        
        self.step_count = 0
        

    def receive(
        self,
        value
    ):

        self.cells.append(
            {
                "value": value,
                "age": 0,
                "source":"collision",
                "step":self.step_count
            }
        )


        if len(self.cells) > self.capacity:

            self.cells.pop(0)



    def step(self):
        
        self.step_count += 1
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