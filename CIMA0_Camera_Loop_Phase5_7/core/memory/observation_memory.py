class ObservationMemory:


    def __init__(
        self,
        capacity=128
    ):

        self.capacity = capacity

        self.records = []



    def receive(
        self,
        observation
    ):

        self.records.append(
            observation
        )


        if len(self.records) > self.capacity:

            self.records.pop(0)



    def snapshot(
        self
    ):

        return list(
            self.records
        )