import numpy as np


class CameraIO:
    """
    Camera IO interface.

    Responsibility:

        camera sampled state
            |
            v
        byte stream
            |
            v
        InternalDynamics


    No:

        sampling
        computation
        interpretation
        filtering
    """


    def __init__(self):
        pass


    def encode(
        self,
        state
    ):
        """
        Convert camera state
        into byte stream.

        Same structure.
        No meaning added.
        """

        if state is None:
            return b""


        array = np.asarray(
            state,
            dtype=np.float32
        )


        return array.tobytes()



    def decode(
        self,
        data,
        shape
    ):
        """
        Restore byte stream
        into camera state.

        Used for IO symmetry.
        """

        if data is None:
            return None


        array = np.frombuffer(
            data,
            dtype=np.float32
        )


        return array.reshape(
            shape
        )