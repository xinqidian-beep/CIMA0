class InternalDynamics:
    """
    Internal lifecycle container.

    Only:

        receive()
        step()
        snapshot()

    No:

        byte interpretation
        sampling decision
        resource allocation
        state modification
    """


    def __init__(
        self,
        planet,
        clip
    ):

        self.planet = planet
        self.clip = clip



    def receive(
        self,
        data
    ):

        if hasattr(
            self.planet,
            "receive"
        ):

            self.planet.receive(
                data
            )


        if hasattr(
            self.clip,
            "receive"
        ):

            self.clip.receive(
                data
            )



    def step(
        self
    ):

        if hasattr(
            self.planet,
            "step"
        ):

            self.planet.step()


        if hasattr(
            self.clip,
            "step"
        ):

            self.clip.step()



    def snapshot(
        self
    ):

        result = {}


        if hasattr(
            self.planet,
            "snapshot"
        ):

            result["planet"] = (
                self.planet.snapshot()
            )


        if hasattr(
            self.clip,
            "snapshot"
        ):

            result["clip"] = (
                self.clip.snapshot()
            )


        return result