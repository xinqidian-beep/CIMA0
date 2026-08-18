"""
CIMA0 Phase5_6

PlanetField

Internal organ.

Responsibility:

    hold planetary local state

    receive external disturbance

    delegate evolution to Planet rule

    provide activity signal

    expose snapshot


Does NOT know:

    camera
    bytes
    image
    RGB
    CLIP
    display
    compute policy


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


    Planet.evolve()


            |

            v


    local planetary state


"""


import numpy as np



class PlanetField:


    def __init__(
        self,
        planet,
        size=128,
        initial_state=None
    ):


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
        # pending external disturbance
        #

        self.pending_disturbance = None



        #
        # organ state
        #

        self.previous_state = None

        self.age = 0


        #
        # compute allocation
        #

        self.compute_budget = 0





    #
    # receive external disturbance
    #

    def receive(
        self,
        disturbance
    ):


        if disturbance is None:

            return



        if not isinstance(
            disturbance,
            np.ndarray
        ):

            return



        self.pending_disturbance = (
            disturbance
            .astype(
                np.float32,
                copy=True
            )
        )





    #
    # attention signal
    #
    # self evaluation
    #

    def activity(
        self
    ):


        if self.previous_state is None:


            return {

                "activity":
                    0.0,

                "age":
                    self.age,

                "delta":
                    0.0

            }



        delta = np.mean(
            np.abs(
                self.state
                -
                self.previous_state
            )
        )



        return {

            "activity":
                float(delta),

            "age":
                self.age,

            "delta":
                float(delta)

        }






    #
    # compute allocation
    #

    def apply_compute(
        self,
        amount
    ):

        self.compute_budget = amount






    #
    # evolution
    #

    def step(
        self
    ):


        if self.planet is None:

            return



        #
        # preserve previous state
        #

        old_state = (
            self.state
            .copy()
        )



        #
        # delegate to pure Planet rule
        #

        self.planet.step()


        self.state = (
            self.planet
            .snapshot()
            .astype(
                np.float32,
                copy=True
            )
        )


        #
        # observe local change
        #

        delta = np.mean(
            np.abs(
                self.state
                -
                old_state
            )
        )


        print(
            "PLANETFIELD DELTA:",
            float(delta)
        )



        #
        # update history
        #

        self.previous_state = old_state


        self.age += 1



        #
        # consume disturbance
        #

        self.pending_disturbance = None



        #
        # consume compute
        #

        self.compute_budget = 0






    #
    # packet output
    #

    def packet(
        self
    ):


        return {

            "type":
                "field",

            "representation":
                "planet",

            "organ":
                "planet",

            "shape":
                self.state.shape,

            "dtype":
                "float32",

            "bytes":
                self.state
                .astype(
                    np.float32
                )
                .tobytes(),

            "timestamp":
                self.age

        }





    #
    # observer interface
    #

    def snapshot(
        self
    ):


        return self.state.copy()