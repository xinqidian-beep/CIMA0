class CameraIO:
    """
    Camera input boundary.


    Responsibility:

        transfer external frame


    No:

        interpretation
        compression
        sampling
        feature extraction
        state evaluation
    """



    def __init__(self):

        pass



    def input_frame(
        self,
        frame
    ):
        """
        Receive raw camera frame.

        Return unchanged frame.
        """


        return frame



    def output_frame(
        self,
        frame
    ):
        """
        Output boundary.

        Current stage:

            transparent pass-through
        """


        return frame