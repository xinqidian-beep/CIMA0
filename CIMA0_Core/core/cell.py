import numpy as np

from .planet import PlanetEngine


class Cell:
    """
    Local dynamic organization.

    A Cell is not the primitive.

    Primitive:
        PlanetEngine

    Cell:
        a local collection of PlanetEngine.

    External world cannot know:
        - internal population
        - internal trajectory
        - complete state

    Only local activity can be sampled.
    """


    def __init__(
        self,
        initial_planets=4,
        dt=0.01
    ):

        self._planets = []


        for _ in range(initial_planets):

            self._planets.append(
                PlanetEngine(
                    x=np.random.uniform(-1, 1),
                    v=np.random.uniform(-0.05, 0.05),
                    omega=np.random.uniform(0.8, 1.2),
                    dt=dt
                )
            )


        self._last_activity = 0.0



    def step(
        self,
        disturbance=None
    ):

        """
        Only local evolution.

        No global information.
        """


        total_change = 0.0


        for i, planet in enumerate(self._planets):

            old_x = planet.x


            local_force = 0.0


            if disturbance is not None:

                if i < len(disturbance):

                    local_force = disturbance[i]


            planet.step(
                external_force=local_force
            )


            total_change += abs(
                planet.x - old_x
            )


        self._last_activity = (
            total_change
            /
            max(
                len(self._planets),
                1
            )
        )



    def local_activity(self):

        """
        Internal compression.

        External does not receive
        all planet states.

        Only one local signal.
        """

        return float(
            self._last_activity
        )



    def sample(self):

        """
        Local sampling.

        Not full internal state.
        """

        return {

            "activity":
                self.local_activity()

        }