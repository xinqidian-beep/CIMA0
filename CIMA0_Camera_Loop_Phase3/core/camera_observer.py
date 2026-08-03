import numpy as np


class CameraObserver:
    """
    Byte stream dynamic gate.

    Input:
        bytes

    Output:
        bytes

    Internal:
        local history
        delta
        age
    """

    def __init__(
        self,
        threshold=0.01,
        max_output=4096
    ):

        self.previous = None
        self.age = None

        self.threshold = threshold
        self.max_output = max_output



    def observe(
        self,
        data
    ):

        if data is None:
            return b""


        current = np.frombuffer(
            data,
            dtype=np.uint8
        )


        size = current.size


        if self.previous is None:

            self.previous = current.copy()

            self.age = np.zeros(
                size,
                dtype=np.int32
            )

            return data[:self.max_output]



        delta = np.abs(
            current.astype(np.int16)
            -
            self.previous.astype(np.int16)
        )


        self.previous = current.copy()



        self.age += 1


        active = delta > self.threshold


        self.age[
            active
        ] = 0



        score = (
            delta.astype(np.float32)
            +
            self.age * 0.05
        )



        count = min(
            self.max_output,
            size
        )


        index = np.argpartition(
            score,
            -count
        )[-count:]



        index.sort()


        output = current[
            index
        ]


        return output.tobytes()