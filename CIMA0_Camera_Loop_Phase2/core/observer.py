import numpy as np


class Observer:
    """
    Internal observer.

    Not controller.
    Not sampler.
    Not decision maker.

    Responsibility:

        read current internal state
        read local structures
        generate snapshot

    """

    def __init__(self):

        self.last_snapshot = None



    def observe(
        self,
        field_state=None,
        clip_state=None
    ):

        snapshot = {}


        if field_state is not None:

            field_array = np.asarray(
                field_state,
                dtype=np.float32
            )

            snapshot["field_mean"] = float(
                field_array.mean()
            )

            snapshot["field_std"] = float(
                field_array.std()
            )

            snapshot["field_activity"] = float(
                np.abs(field_array).mean()
            )


        if clip_state is not None:

            snapshot["clip"] = clip_state



        self.last_snapshot = snapshot


        return snapshot



    def read(self):

        return self.last_snapshot