"""
CIMA0 Phase5_3

PlanetField

State holder of the planetary dynamical system.

Responsibility:

    hold current state
    store pending disturbance
    delegate evolution to Planet rule
    expose read-only snapshot


Does NOT know:

    camera
    bytes
    image
    RGB
    CLIP
    CloudField
    display
    compute budget


Architecture:

    external disturbance
            |
            v

    PlanetField.receive()

            |
            v

    pending disturbance


            |
            v

    Planet.evolve(
        state,
        disturbance
    )


            |
            v

    new state

"""


import numpy as np



class PlanetField:


    def __init__(
        self,
        planet,
        size=128,
        initial_state=None
    ):
        """
        planet:

            pure evolution rule


        state:

            actual evolving field

        """


        self.planet = planet


        if initial_state is not None:

            self.state = (
                initial_state
                .astype(
                    np.float32,
                    copy=True
                )
            )

        else:

            self.state = (
                np.random.randn(
                    size,
                    size
                )
                .astype(
                    np.float32
                )
                *
                0.01
            )


        #
        # disturbance waiting for next evolution
        #
        self.pending_disturbance = None



    def receive(
        self,
        disturbance
    ):
        """
        Receive external disturbance.

        Only store.

        Do not modify state directly.

        The actual effect is decided by
        Planet.evolve().
        """


        if disturbance is None:

            return



        if not isinstance(
            disturbance,
            np.ndarray
        ):

            return



        self.pending_disturbance = (
            disturbance.astype(
                np.float32,
                copy=True
            )
        )



    def step(
        self
    ):
        """
        Advance one time step.

        Delegate physics to Planet.
        """


        if self.planet is None:

            return



        self.state = (
            self.planet.evolve(
                self.state,
                self.pending_disturbance
            )
        )


        #
        # disturbance consumed
        #
        self.pending_disturbance = None



    def snapshot(
        self
    ):
        """
        Read-only state exposure.
        """


        return self.state.copy()