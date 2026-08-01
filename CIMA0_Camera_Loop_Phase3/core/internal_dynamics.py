class InternalDynamics:
    """
    Internal dynamic system.

    Responsibility:

        receive external bytes
        evolve internal state
        provide snapshot


    No:

        observation
        sampling
        interpretation
        control
    """


    def __init__(
        self,
        planet=None,
        clip_region=None
    ):

        self.planet = planet

        self.clip_region = clip_region

        self.external_bytes = None



    def receive(
        self,
        data
    ):
        """
        External disturbance.

        Bytes only.
        """

        self.external_bytes = data



    def step(
        self
    ):
        """
        Internal evolution.
        """


        if self.planet is not None:

            self.planet.receive(
                self.external_bytes
            )

            self.planet.step()



        if self.clip_region is not None:

            self.clip_region.update()



    def snapshot(
        self
    ):
        """
        Raw internal state.

        Read only.
        """

        result = {}


        if self.planet is not None:

            result["planet"] = (
                self.planet.snapshot()
            )


        if self.clip_region is not None:

            result["clip"] = (
                self.clip_region.state()
            )


        return result