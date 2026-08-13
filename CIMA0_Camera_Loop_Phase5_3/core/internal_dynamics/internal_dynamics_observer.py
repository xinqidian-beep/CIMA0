import numpy as np


class InternalDynamicsObserver:
    """
    CIMA0 Phase5_3

    Read-only observer.

    Input:

        InternalDynamics snapshot

            |
            v

        Planet state field


    Output:

        observation packet

            |
            v

        ComputeSystem


    Responsibility:

        - read state
        - calculate delta
        - maintain age
        - calculate activity
        - request computation


    Does NOT:

        - modify Planet
        - understand camera
        - understand color
        - sample itself
        - allocate compute
    """


    def __init__(
        self,
        w_delta=1.0,
        w_age=0.2,
        w_activity=1.0
    ):

        self.previous = None

        self.age = None


        #
        # adaptive weights
        #
        self.w_delta = w_delta

        self.w_age = w_age

        self.w_activity = w_activity



    def read(
        self,
        snapshot
    ):

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


            active = delta > 0


            self.age[active] = 0



        #
        # activity field
        #
        activity = (
            delta +
            1e-6
        )



        #
        # automatic hand raising
        #
        request_score = (

            self.w_delta *
            delta

            +

            self.w_age *
            self.age

            +

            self.w_activity *
            activity

        )



        return {

            "state":
                self._field_packet(
                    state,
                    "planet_state"
                ),


            "delta":
                self._field_packet(
                    delta,
                    "planet_delta"
                ),


            "age":
                self._field_packet(
                    self.age,
                    "planet_age"
                ),


            "activity":
                self._field_packet(
                    activity,
                    "planet_activity"
                ),


            #
            # send to ComputeSystem
            #
            "compute_request":
                {

                    "type":
                        "field_request",


                    "source":
                        "planet",


                    "shape":
                        state.shape,


                    "score":
                        request_score

                }

        }

    def encode_field(
        self,
        data,
        source="internal"
    ):
        """
        Encode observation field into packet.

        Only:

            ndarray
            ->
            bytes packet


        No:

            color
            semantic
            visualization
        """

        if data is None:

            return None


        if "state" not in data:

            return None


        array = data["state"]


        if not isinstance(
            array,
            np.ndarray
        ):

            return None



        return {

            "type":
                "field",


            "source":
                source,


            "representation":
                "internal_state",


            "bytes":
                array.astype(
                    np.float32
                ).tobytes(),


            "shape":
                array.shape,


            "dtype":
                "float32"

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



        if "planet" not in snapshot:

            return None



        planet = snapshot["planet"]



        #
        # PlanetField style
        #
        if isinstance(
            planet,
            dict
        ):

            if "field" not in planet:

                return None


            state = planet["field"]



        #
        # direct ndarray
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



        return state.astype(
            np.float32,
            copy=False
        )



    def _field_packet(
        self,
        array,
        source
    ):

        return {

            "type":
                "field",


            "source":
                source,


            "representation":
                "internal_dynamic_field",


            "bytes":
                array.astype(
                    np.float32
                ).tobytes(),


            "shape":
                array.shape,


            "dtype":
                "float32"

        }