import numpy as np


class Projection:
    """
    Internal projection layer.

    Responsibility:

        transform temporary internal samples
        into display space

    No:

        prediction
        generation
        semantic completion
        memory
        control
    """


    def __init__(self):
        pass



    def project_ephemeral_frame(
        self,
        base_frame,
        sample_ephemeral
    ):

        """
        Reconstruct temporary display frame.

        Unobserved area:

            keep original state


        Sampled area:

            replace with current sampled state
        """


        display_ephemeral_frame = (
            base_frame.copy()
        )


        if sample_ephemeral is None:

            return display_ephemeral_frame



        height, width, channel = (
            display_ephemeral_frame.shape
        )


        for sample in sample_ephemeral:

            x, y = (
                sample["position"]
            )


            if (
                0 <= x < width
                and
                0 <= y < height
            ):

                pixel = np.asarray(
                    sample[
                        "sample_ephemeral_state"
                    ],
                    dtype=np.float32
                )


                display_ephemeral_frame[y, x] = (
                    pixel
                )



        return display_ephemeral_frame