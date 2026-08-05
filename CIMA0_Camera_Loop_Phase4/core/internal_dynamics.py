class InternalDynamics:
    """
    Internal lifecycle container.

    Only:

        receive()
        step()
        snapshot()


    Does NOT:

        interpret bytes
        sample
        allocate resources
        modify internal rules


    External bytes are passed into
    internal organs.

    Each organ owns its own
    structural projection.
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
        """
        External byte stream.

        No interpretation here.

        Planet and Clip decide
        their own internal projection.
        """

        self.clip.receive(
            data
        )
        

        



    def step(
        self
    ):
        """
        Advance internal dynamics.

        Each component follows
        its own local rule.
        """

        self.planet.step()

        self.clip.step()



    def snapshot(
        self
    ):
        """
        Read-only state export.

        No modification.
        """
        clip_state = self.clip.snapshot()

        return {

            "planet":
            {
                "state":
                self.planet.state.copy()
            },


            "clip":
            clip_state

        }