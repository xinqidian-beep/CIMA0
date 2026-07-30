import numpy as np


class CameraPlanet:
    """
    External camera planet.

    Represents:

        external optical world mapping


    Responsibility:

        receive raw camera state
        normalize external state
        provide temporary sampled output


    No:

        internal dynamics
        observation
        computation allocation
        semantic understanding
        long-term memory
    """



    def __init__(self):

        pass



    def step_planet(
        self,
        frame
    ):
        """
        Map external camera frame
        into numerical external state.

        No interpretation.
        """

        if frame is None:

            return None



        external_state = np.asarray(
            frame,
            dtype=np.float32
        )


        #
        # normalize only numeric range
        #

        external_state = (
            external_state / 255.0
        )


        return external_state



    def sample_ephemeral(
        self,
        external_state,
        delta_ephemeral,
        compute_slots_ephemeral
    ):
        """
        Produce temporary sampled projection.

        Compute permission comes externally.

        CameraPlanet does not decide:

            importance
            priority
            budget

        """

        if (
            external_state is None
            or
            delta_ephemeral is None
        ):

            return []



        height, width, channel = (
            external_state.shape
        )


        total_points = (
            height * width
        )


        sample_count = min(
            int(compute_slots_ephemeral),
            total_points
        )


        if sample_count <= 0:

            return []



        #
        # local variation only
        #

        variation_ephemeral = (
            np.abs(
                delta_ephemeral
            )
            .mean(axis=2)
        )


        flat_variation = (
            variation_ephemeral.reshape(-1)
        )



        if sample_count >= total_points:

            indices = np.arange(
                total_points
            )

        else:

            indices = np.argpartition(
                flat_variation,
                -sample_count
            )[-sample_count:]



        sampled_ephemeral = []


        for index in indices:

            y = index // width
            x = index % width


            sampled_ephemeral.append(

                {

                    "position":
                        (
                            int(x),
                            int(y)
                        ),


                    "state_ephemeral":
                        external_state[y, x].copy(),


                    "variation_ephemeral":
                        float(
                            flat_variation[index]
                        )

                }

            )


        return sampled_ephemeral