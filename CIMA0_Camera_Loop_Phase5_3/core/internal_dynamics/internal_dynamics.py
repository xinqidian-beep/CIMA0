"""
CIMA0 Phase5_3

Internal Dynamics Interface

Role:

    Connect external system and Planet dynamics.

Does NOT know:

    camera
    cloud
    clip
    observer meaning
    display

Only manages:

    receive external disturbance
    advance local dynamics
    expose current state
"""


class InternalDynamics:


    def __init__(
        self,
        planet
    ):

        self.planet = planet

        self.last_snapshot = None



    def receive(
        self,
        raw
    ):
        """
        Forward external disturbance.

        InternalDynamics does not interpret data.
        Planet decides whether and how to use it.
        """

        if hasattr(
            self.planet,
            "receive"
        ):

            self.planet.receive(
                raw
            )



    def step(
        self
    ):
        """
        Advance the only internal dynamics.

        The evolution rule belongs to Planet.
        """

        if hasattr(
            self.planet,
            "step"
        ):

            self.planet.step()


        if hasattr(
            self.planet,
            "snapshot"
        ):

            self.last_snapshot = {

                "planet":
                    self.planet.snapshot()

            }

        else:

            self.last_snapshot = {}



    def snapshot(
        self
    ):
        """
        Return current Planet state.
        """

        if self.last_snapshot is None:

            if hasattr(
                self.planet,
                "snapshot"
            ):

                return self.planet.snapshot()


            return None


        return self.last_snapshot.copy()