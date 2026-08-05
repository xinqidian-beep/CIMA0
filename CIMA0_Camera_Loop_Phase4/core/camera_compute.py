import time


class CameraComputeSystem:
    """
    Camera computation system.

    Responsibility:

        manage own computation state
        provide available computation capability


    No:

        image understanding
        sampling
        semantic judgment
        camera control
    """


    def __init__(self):

        self.available = 1.0

        self.last_time = time.time()

        self.process_time = 0.0


    def step(
        self
    ):
        """
        Update own computation state.

        No external decision.
        """

        now = time.time()

        self.process_time = now - self.last_time

        self.last_time = now


        #
        # Current simple capability estimation
        #
        # Later can be replaced by real hardware statistics.
        #

        if self.process_time <= 0:

            self.available = 1.0

        else:

            load = min(
                1.0,
                self.process_time / 0.05
            )

            self.available = 1.0 - load



        return self.state()



    def state(
        self
    ):
        """
        Provide computation state.

        Used by other modules.
        """

        return {

            "available":
                float(
                    self.available
                ),

            "process_time":
                float(
                    self.process_time
                )

        }