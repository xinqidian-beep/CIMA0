"""
CIMA0 Phase5_7

PlanetField

Local continuous evolution field.

Responsibility:

    hold planetary local state

    receive external disturbance

    delegate evolution to Planet rule

    provide activity signal

    export collision projection


Does NOT know:

    camera
    bytes
    image
    RGB
    CLIP
    display
    compute policy
    CloudField


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


PlanetField state


        |

        v


collision projection


"""



import numpy as np

from core.io.transport.packet import BitPacket




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
        # external disturbance buffer
        #

        self.pending_disturbance = None



        #
        # history
        #

        self.previous_state = None

        self.age = 0



        #
        # compute
        #

        self.compute_budget = 0





    #
    # external input
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

    def activity(
        self
    ):


        if self.previous_state is None:


            return {


                "activity":
                    float(
                        np.mean(
                            np.abs(
                                self.state
                            )
                        )
                    ),


                "signal":
                    1.0,


                "changed":
                    True,


                "source":
                    "planet",


                "age":
                    self.age

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


            "signal":
                float(delta),


            "changed":
                bool(
                    delta > 0
                ),


            "source":
                "planet",


            "age":
                self.age

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



        old_state = (

            self.state
            .copy()

        )



        #
        # Planet owns evolution
        #

        if hasattr(
            self.planet,
            "evolve"
        ):


            self.state = (

                self.planet.evolve(

                    self.state,

                    self.pending_disturbance

                )

            ).astype(

                np.float32,

                copy=True

            )



        else:


            #
            # compatibility fallback
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



        self.previous_state = old_state


        self.age += 1



        #
        # disturbance consumed
        #

        self.pending_disturbance = None



        self.compute_budget = 0






    #
    # packet output
    #

    def packet(
        self
    ):


        print(
            "PLANET PACKET CREATED"
        )


        field = (

            self.state
            .astype(
                np.float32
            )

        )



        return BitPacket(


            source="planet",


            tag="visual",


            data=field.tobytes(),


            shape=field.shape,


            dtype="float32",


            schema="continuous_field",


            meta={

                "age":
                    self.age

            }

        )






    #
    # collision projection
    #

    def collision_projection(
        self
    ):
        """
        PlanetField state

                |

                v

        planet cloud representation


        Read only.
        Used by CloudCollision.
        No modification.

        No activity evaluation.

        """



        field = self.state.copy()



        cloud = {


            "mean":

                float(
                    np.mean(field)
                ),



            "energy":

                float(
                    np.mean(
                        np.abs(field)
                    )
                ),



            "variance":

                float(
                    np.var(field)
                ),



            "density":

                float(

                    np.count_nonzero(field)

                    /

                    field.size

                )

        }



        return {


            "source":

                "planet",



            "representation":

                "planet_cloud",



            "cloud":

                cloud,



            "shape":

                field.shape

        }






    #
    # observer
    #

    def snapshot(
        self
    ):


        return self.state.copy()