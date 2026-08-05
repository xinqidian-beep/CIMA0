import numpy as np


class CameraObserver:
    """
    Dynamic BGR byte observer.

    Input:
        BGR byte stream

    Output:
        complete BGR byte stream


    Rule:

        delta
          +
        age
          +
        compute budget

        ->
        select update positions

        ->
        keep complete field


    No:

        image understanding
        semantic extraction
        feature generation
        packet generation
    """


    def __init__(
        self,
        pixel_size=3
    ):

        self.pixel_size = pixel_size

        self.previous = None

        # current maintained field
        self.field = None

        # refresh age
        self.age = None



    def observe(
        self,
        data,
        compute_state=None
    ):

        if data is None:
            return b""


        raw = np.frombuffer(
            data,
            dtype=np.uint8
        )


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


            return self.field.reshape(
                -1
            ).tobytes()



        #
        # delta
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
        # age update
        #

        self.age += 1



        #
        # compute resource
        #

        available = 0.1


        if isinstance(
            compute_state,
            dict
        ):

            available = compute_state.get(
                "available",
                0.1
            )


        available = float(
            np.clip(
                available,
                0.01,
                1.0
            )
        )



        #
        # dynamic precision budget
        #

        budget = int(
            count *
            available
        )


        budget = max(
            1,
            min(
                count,
                budget
            )
        )



        #
        # local raise score
        #

        score = (
            delta
            +
            self.age.astype(
                np.float32
            ) * 0.02
        )



        #
        # choose update positions
        #

        if budget >= count:

            selected = np.arange(
                count
            )

        else:

            selected = np.argpartition(
                score,
                -budget
            )[-budget:]



        #
        # focus precision update
        #

        self.field[
            selected
        ] = pixels[
            selected
        ]



        #
        # refreshed areas reset age
        #

        self.age[
            selected
        ] = 0



        #
        # output full BGR field
        #

        return self.field.reshape(
            -1
        ).tobytes()



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