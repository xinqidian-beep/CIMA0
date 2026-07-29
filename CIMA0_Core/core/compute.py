class ComputeSystem:

    """
    Autonomous resource dynamics.

    """

    def __init__(
        self
    ):

        self.compute_capacity = 1.0

        self.compute_ephemeral_load = 0.0



    def receive_compute_ephemeral_load(
        self,
        load
    ):

        self.compute_ephemeral_load = (
            float(load)
        )



    def step_compute_dynamics(
        self
    ):

        self.compute_capacity += 0.001

        self.compute_capacity -= (
            self.compute_ephemeral_load
        )


        if self.compute_capacity < 0:

            self.compute_capacity = 0.0


        if self.compute_capacity > 1:

            self.compute_capacity = 1.0


        self.compute_ephemeral_load = 0.0



    def project_compute_ephemeral_state(
        self
    ):

        return self.compute_capacity