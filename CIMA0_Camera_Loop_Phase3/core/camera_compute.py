class CameraComputeSystem:
    """
    Camera computation resource dynamics.

    Responsibility:

        manage own compute state
        allocate own resources

    Does not know:

        camera
        image
        meaning
        importance
        sampling
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
            self.capacity
            -
            self.available
        ) * self.decay



        if self.available > self.capacity:

            self.available = self.capacity



    def allocate(
        self,
        signal
    ):

        budget = (
            self.available
            *
            signal
        )


        self.available -= budget


        return {
            "compute_budget":
                budget
        }



    def snapshot(self):

        return {

            "available":
                self.available,

            "capacity":
                self.capacity
        }