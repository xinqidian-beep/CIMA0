import numpy as np



class InternalDynamicsObserver:
    """
    Internal dynamics observer.


    Input:

        Planet snapshot


    Output:

        observation field

        compute request


    Responsibility:

        observe state

        calculate temporal change

        raise hand


    No:

        dynamics

        compute allocation

        sampling execution

        display

    """



    def __init__(
        self,
        w_delta=0.5,
        w_age=0.3,
        w_activity=0.2
    ):

        self.previous = None

        self.age = None


        #
        # self adaptive observation weights
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



        activity = delta + 1e-6



        observation = {


            "state":

                state.copy(),



            "delta":

                delta.copy(),



            "age":

                self.age.copy(),



            "activity":

                activity.copy(),



            "type":

                "planet_observation",



            "source":

                "internal_dynamics"

        }



        #
        # automatic hand raising
        #

        observation["request"] = self.raise_hand(
            observation
        )


        return observation



    def raise_hand(
        self,
        observation
    ):
        """
        Generate compute request.

        Only report demand.
        Does not allocate.
        """


        delta = observation["delta"]

        age = observation["age"]

        activity = observation["activity"]



        #
        # normalize age
        #

        age_norm = (

            age /

            max(
                np.max(age),
                1.0
            )

        )



        score = (

            self.w_delta * delta

            +

            self.w_age * age_norm

            +

            self.w_activity * activity

        )



        return {


            "type":

                "compute_request",



            "source":

                "internal_dynamics_observer",



            "score":

                score.astype(
                    np.float32
                ),



            "shape":

                score.shape

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


            state = planet.get(
                "field"
            )



        #
        # legacy
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
        
        if not isinstance(
            array,
            np.ndarray
        ):

            return None

        return {
        
            #
            # packet identity
            #


            "type":
                "field",


            "source":
                source,



            #
            # field identity
            #

            "field_type":
                "planet_state",


            "representation":
                "scalar_field",


            "channels":
                1,


            "color_space":
                None,



            #
            # raw data
            #

            "bytes":
                array.astype(
                    np.float32
                ).tobytes(),


            "shape":
                array.shape,


            "dtype":
                "float32"

        }