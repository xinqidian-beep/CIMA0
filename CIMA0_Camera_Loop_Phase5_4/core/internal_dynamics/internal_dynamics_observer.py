import numpy as np


class InternalDynamicsObserver:
    """
    Read only internal dynamics observer.

    Phase5_4

    Input:

        InternalDynamics snapshot


        {
            "planet": {},

            "organs":
            {
                "clip": {}
            }
        }


    Output:

        homogeneous observation packet


    Responsibility:

        observe state change

        calculate delta

        calculate activity

        raise computation request


    No:

        modify dynamics

        allocate resource

        understand semantics

    """


    def __init__(
        self,
        w_delta=1.0,
        w_age=0.1,
        w_activity=1.0
    ):


        #
        # multi source memory
        #

        self.previous = {}

        self.age = {}


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


        fields = self._extract_fields(
            snapshot
        )


        if len(fields) == 0:

            return None



        result = {}



        for name, item in fields.items():


            state = item["state"]



            state = state.astype(
                np.float32
            )



            #
            # first observation
            #

            if name not in self.previous:


                self.previous[name] = (
                    state.copy()
                )


                self.age[name] = np.zeros_like(
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
                    self.previous[name]
                )


                self.previous[name] = (
                    state.copy()
                )



                self.age[name] += 1.0



                active = delta > 0


                self.age[name][active] = 0




            #
            # activity
            #

            activity = (

                delta +

                1e-6

            )



            #
            # computation pressure
            #

            score = (

                self.w_delta *

                delta

                +

                self.w_age *

                self.age[name]

                +

                self.w_activity *

                activity

            )




            result[name] = {


                "type":

                    item.get(
                        "type",
                        name
                    ),



                "state":

                    self._field_packet(
                        state,
                        name+"_state"
                    ),



                "delta":

                    self._field_packet(
                        delta,
                        name+"_delta"
                    ),



                "age":

                    self._field_packet(
                        self.age[name],
                        name+"_age"
                    ),



                "activity":

                    self._field_packet(
                        activity,
                        name+"_activity"
                    ),



                #
                # keep structure
                #

                "structure":

                    item.get(
                        "structure"
                    ),



                #
                # hand raising
                #

                "compute_request":
                {

                    "type":

                        "field_request",



                    "source":

                        name,



                    "shape":

                        state.shape,



                    "score":

                        score

                }

            }



        self.last_observation = result


        return result





    def _extract_fields(
        self,
        snapshot
    ):


        fields = {}



        if snapshot is None:

            return fields



        if not isinstance(
            snapshot,
            dict
        ):

            return fields




        #
        # Planet
        #

        planet = snapshot.get(
            "planet"
        )


        if isinstance(
            planet,
            dict
        ):


            state = self._extract_state_value(
                planet
            )


            if state is not None:


                fields["planet"] = {


                    "state":

                        state,


                    "type":

                        "planet",


                    "structure":

                        planet.get(
                            "structure"
                        )

                }





        #
        # Organs
        #

        organs = snapshot.get(
            "organs",
            {}
        )


        if isinstance(
            organs,
            dict
        ):


            for name, organ in organs.items():


                if not isinstance(
                    organ,
                    dict
                ):

                    continue



                state = self._extract_state_value(
                    organ
                )


                if state is None:

                    continue



                fields[name] = {


                    "state":

                        state,


                    "type":

                        organ.get(
                            "type",
                            name
                        ),


                    "structure":

                        organ.get(
                            "structure"
                        )

                }



        return fields




    def _extract_state_value(
        self,
        data
    ):


        #
        # direct ndarray
        #

        for key in (
            "state",
            "cloud"
        ):


            value = data.get(
                key
            )


            if isinstance(
                value,
                np.ndarray
            ):

                return value




        #
        # packet state
        #

        state = data.get(
            "state"
        )


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



        return None





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



            "structure":

                data.get(
                    "structure"
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