class ComputeSystem:
    """
    Local computation resource dynamics.

    Responsibility:

        manage own compute state
        allocate own resources

    Does not know:

        planet
        observer
        cloud
        meaning
        importance
    """


    def __init__(
        self,
        capacity=1.0,
        decay=0.01
    ):

        self.capacity = capacity

        self.available = capacity

        self.decay = decay



    def step(self):

        self.available += (
            self.capacity -
            self.available
        ) * self.decay


        if self.available > self.capacity:
            self.available = self.capacity



    def allocate(
        self,
        observation_signal
    ):

        """
        Allocate computation according to:

            observation signal
            own available resource

        Does not know:

            signal meaning
        """


        signal = max(
            0.0,
            min(
                1.0,
                observation_signal
            )
        )


        budget = (
            self.available *
            signal
        )


        self.available -= budget


        if self.available < 0:
            self.available = 0


        return {
            "compute_budget": budget
        }



    def snapshot(self):

        return {
            "available":
                self.available,

            "capacity":
                self.capacity
        }