import numpy as np


class InternalDynamicsObserver:
    """
    Read only internal dynamics observer.

    Input:

        snapshot packet

    Output:

        observation packet

        {
            state,
            delta,
            age,
            activity,
            compute_request
        }

    Responsibility:

        observe change
        calculate activity
        raise computation request

    No:

        modify dynamics
        control planet
        decode semantics
    """


    def __init__(
        self,
        w_delta=1.0,
        w_age=0.1,
        w_activity=1.0
    ):

        self.previous = None

        self.age = None

        self.last_observation = None


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



        state = state.astype(
            np.float32
        )



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


            self.age += 1.0


            active = delta > 0


            self.age[active] = 0



        #
        # activity
        #

        activity = (
            delta +
            1e-6
        )



        #
        # automatic hand raising
        #

        score = (

            self.w_delta *
            delta

            +

            self.w_age *
            self.age

            +

            self.w_activity *
            activity

        )



        result = {


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



            "compute_request":
            {

                "type":
                    "field_request",


                "source":
                    "planet",


                "shape":
                    state.shape,


                "score":
                    score

            }

        }



        self.last_observation = result


        return result



    def encode_field(
        self,
        data,
        source="internal"
    ):


        if data is None:

            return None


        if "state" not in data:

            return None


        packet = data["state"]


        return {

            "type":
                "field",


            "format":
                "field",


            "source":
                source,


            "representation":
                "internal_state",


            "bytes":
                packet["bytes"],


            "shape":
                packet["shape"],


            "dtype":
                packet["dtype"],
                
            #
            # same-structure information
            #

            "structure":
                data.get(
                    "structure"
                ),


            "projection":
                data.get(
                    "projection"
                )    
                
                

        }



    def snapshot(
        self
    ):

        if self.last_observation is None:

            return None


        return self.last_observation.copy()



    def _field_packet(
        self,
        array,
        name
    ):


        return {


            "type":
                "field",


            "format":
                "field",


            "name":
                name,


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


        if snapshot is None:

            return None



        if not isinstance(
            snapshot,
            dict
        ):

            return None



        #
        # InternalDynamics snapshot
        #
        # {
        #     "planet": ...
        # }
        #

        planet = snapshot.get(
            "planet"
        )


        if planet is None:

            return None



        if isinstance(
            planet,
            dict
        ):

            state = planet.get(
                "state"
            )


            if isinstance(
                state,
                np.ndarray
            ):

                return state

            #
            # optional packet state
            #

            if isinstance(
                state,
                dict
            ):

                try:

                    raw = np.frombuffer(
                        state["bytes"],
                        dtype=np.dtype(
                            state["dtype"]
                        )
                    )


                    return raw.reshape(
                        state["shape"]
                    )


                except Exception:

                    pass

        #
        # direct ndarray
        #

        if isinstance(
            planet,
            np.ndarray
        ):

            return planet



        return None