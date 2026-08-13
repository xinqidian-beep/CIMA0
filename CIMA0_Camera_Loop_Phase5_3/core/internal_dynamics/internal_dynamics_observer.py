import numpy as np


class InternalDynamicsObserver:
    """
    CIMA0 Phase5_3

    Read only observer.

    Responsibility:

        InternalDynamics snapshot
                |
                v
        calculate observation values
                |
                v
        sampling information
                |
                v
        ComputeSystem / Sampler


    Does NOT know:

        camera
        planet dynamics
        cloud meaning
        sampler rule
        compute allocation
        interpretation
    """


    def __init__(self):

        self.previous = None

        self.age = None



    def read(
        self,
        snapshot,
        allocation=None
    ):

        if snapshot is None:

            return None



        state = self._extract_state(
            snapshot
        )


        if state is None:

            return None



        #
        # first observation
        #

        if self.previous is None:

            self.previous = state.copy()

            self.age = np.zeros_like(
                state,
                dtype=np.float32
            )


            delta = np.zeros_like(
                state,
                dtype=np.float32
            )


        else:


            delta = np.abs(
                state -
                self.previous
            )


            self.previous = state.copy()


            self.age += 1



            #
            # active area refresh
            #

            active = delta > 0


            self.age[active] = 0



        #
        # local activity
        #

        activity = (
            delta
            +
            1e-6
        )



        return {

            "state":
                self._sample(
                    state,
                    allocation
                ),

            "delta":
                self._sample(
                    delta,
                    allocation
                ),

            "age":
                self._sample(
                    self.age,
                    allocation
                ),

            "activity":
                self._sample(
                    activity,
                    allocation
                )

        }



    def _extract_state(
        self,
        snapshot
    ):

        if not isinstance(
            snapshot,
            dict
        ):

            return None
            
        planet = snapshot.get(
            "planet"
        )    


        if planet is None:

            return None
            
        #
        # new PlanetField snapshot
        #

        if  isinstance(
            planet,
            dict
        ):

            state = planet.get(
                "field"
            )


        #
        # old compatibility
        #
        elif isinstance(
            planet,
            np.ndarray
        ):

            state = planet


        else:

            return None



        if not isinstance(
            state,
            np.ndarray
        ):
            return None

        return state

        
    def _sample(
        self,
        array,
        allocation
    ):
        """
        Observer only applies allocation.

        Sampling decision belongs to Sampler.
        """

        if allocation is None:

            return array.copy()


        #
        # placeholder:
        #
        # ComputeSystem will later
        # provide selected indices.
        #

        return array.copy()



    def encode_field(
        self,
        data,
        source="internal"
    ):

        if data is None:

            return None



        if "state" not in data:

            return None



        array = data["state"]



        return {

            "type":
                "field",

            "source":
                source,

            "bytes":
                array.astype(
                    np.float32
                ).tobytes(),

            "shape":
                array.shape,

            "dtype":
                "float32"

        }