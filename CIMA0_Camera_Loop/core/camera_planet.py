import numpy as np


class CameraPlanet:
    """
    External camera planet.

    Responsibility:

        map external camera frame
        into external numerical state


    No:

        observation
        temporal comparison
        sampling
        computation allocation
        semantic understanding
        memory
    """


    def __init__(self):
        pass



    def step_planet(
        self,
        frame
    ):
        """
        Convert raw camera frame
        into external numerical state.

        Only numeric normalization.

        No interpretation.
        """

        if frame is None:
            return None


        external_state = np.asarray(
            frame,
            
        )


        #
        # normalize camera value range
        #

        


        return external_state



    def snapshot(
        self
    ):
        """
        Read-only placeholder.

        No internal state.
        """

        return {

            "module":
                "CameraPlanet",

            "state":
                "stateless"

        }