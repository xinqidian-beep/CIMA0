import numpy as np

from core.compute_system import Sampler


class CameraObserver:
    """
    Dynamic BGR field observer.


    Input:

        CameraPlanet packet

        {
            bytes,
            shape,
            dtype
        }


    Output:

        complete BGR field packet


    Responsibility:

        maintain visual field
        calculate local change
        maintain refresh age


    Sampling:

        delegated to ComputeSystem.Sampler


    No:

        image understanding
        semantic extraction
        feature generation
        sampling rule
        compute allocation
    """


    def __init__(
        self,
        pixel_size=3
    ):

        self.pixel_size = pixel_size


        # previous input frame

        self.previous = None


        # maintained complete field

        self.field = None


        # refresh age

        self.age = None


        # universal sampler

        self.sampler = Sampler()



    def observe(
        self,
        packet,
        budget=None
    ):

        if packet is None:

            return None



        raw = np.frombuffer(
            packet["bytes"],
            dtype=np.uint8
        )


        shape = packet["shape"]

        dtype = packet["dtype"]



        #
        # keep BGR alignment
        #

        usable = (
            raw.size //
            self.pixel_size
        ) * self.pixel_size


        raw = raw[:usable]


        pixels = raw.reshape(
            -1,
            self.pixel_size
        )


        count = pixels.shape[0]



        #
        # first frame
        #

        if self.previous is None:


            self.previous = pixels.copy()


            self.field = pixels.copy()


            self.age = np.zeros(
                count,
                dtype=np.int32
            )


            return self._packet(
                shape,
                dtype
            )



        #
        # local change
        #

        delta = np.mean(
            np.abs(
                pixels.astype(np.int16)
                -
                self.previous.astype(np.int16)
            ),
            axis=1
        )


        self.previous = pixels.copy()



        #
        # age evolution
        #

        self.age += 1



        #
        # sampling decision
        #

        if budget is None:

            budget = count



        selected = self.sampler.select(
            delta,
            self.age,
            budget=budget
        )



        #
        # update selected positions
        #

        self.field[
            selected
        ] = pixels[
            selected
        ]



        #
        # reset refreshed age
        #

        self.age[
            selected
        ] = 0



        return self._packet(
            shape,
            dtype
        )



    def _packet(
        self,
        shape,
        dtype
    ):

        return {

            "bytes":
                self.field.reshape(
                    -1
                ).tobytes(),


            "shape":
                shape,


            "dtype":
                dtype

        }



    def snapshot(
        self
    ):

        if self.field is None:

            return {

                "active": False

            }



        return {

            "active": True,


            "pixels":
                int(
                    self.field.shape[0]
                ),


            "mean":
                float(
                    np.mean(
                        self.field
                    )
                ),


            "std":
                float(
                    np.std(
                        self.field
                    )
                )

        }