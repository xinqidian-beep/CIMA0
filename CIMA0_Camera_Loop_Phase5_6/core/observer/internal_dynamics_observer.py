import numpy as np


class InternalDynamicsObserver:


    def __init__(self):

        self.previous = None
        self.current = None



    def _trigger(
        self,
        snapshot
    ):

        fields = (
            snapshot
            .get(
                "fields",
                {}
            )
        )


        clip = fields.get(
            "clip"
        )


        if clip is not None:

            return True


        return False



    def observe(
        self,
        snapshot
    ):

        #
        # keep current attention logic
        #

        if self._trigger(snapshot):

            self.previous = self.current

            self.current = snapshot


        return {

            "state":
                self.current,

            "delta":
                self._compare()

        }




    def _compare(
        self
    ):


        if self.previous is None:

            return None



        delta = {}



        #
        # planet
        #

        old_planet = (
            self.previous
            .get(
                "planet"
            )
        )


        new_planet = (
            self.current
            .get(
                "planet"
            )
        )



        if (
            old_planet is not None
            and
            new_planet is not None
        ):


            delta["planet"] = (
                new_planet
                -
                old_planet
            )


            print(
                "OBSERVER PLANET DELTA:",
                float(
                    np.mean(
                        np.abs(
                            delta["planet"]
                        )
                    )
                )
            )




        #
        # organs
        #

        delta["organs"] = {}


        old_organs = (
            self.previous
            .get(
                "organs",
                {}
            )
        )


        new_organs = (
            self.current
            .get(
                "organs",
                {}
            )
        )



        for name,new in new_organs.items():


            old = old_organs.get(
                name
            )


            if old is None:

                delta["organs"][name] = None


            else:

                delta["organs"][name] = {

                    "changed":
                        True

                }



        return delta




    def read(
        self
    ):

        return self.current