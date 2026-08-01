import numpy as np


class DisplayIO:
    """
    Display IO interface.

    Responsibility:

        observer snapshot
             |
             v
        display format


    No:

        state interpretation
        sampling
        computation
        resolution decision
    """


    def __init__(self):
        pass



    def encode(
        self,
        snapshot
    ):
        """
        Convert observer output
        into display frame.

        Only format conversion.
        """


        if snapshot is None:

            return None



        state = snapshot.get(
            "delta",
            None
        )


        if state is None:

            state = snapshot.get(
                "state",
                None
            )


        if state is None:

            return None



        array = np.asarray(
            state,
            dtype=np.float32
        )



        #
        # debug only
        #

        print(
            "DISPLAY INPUT",
            array.shape,
            float(np.min(array)),
            float(np.max(array)),
            float(np.mean(array))
        )



        #
        # display normalization only
        #

        value = np.abs(
            array
        )


        max_value = np.max(
            value
        )


        if max_value > 0:

            value = value / max_value



        frame = (

            value * 255

        ).astype(
            np.uint8
        )


        return frame