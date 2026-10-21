import cv2
import numpy as np


class DisplayDevice:
    """
    External display hardware.

    Responsibility:

        send frame to physical display


    No:

        computation
        observation
        interpretation
    """


    def __init__(
        self,
        window_name="CIMA0"
    ):

        self.window_name = window_name

        cv2.namedWindow(
            self.window_name,
            cv2.WINDOW_NORMAL
        )


    def show(
        self,
        frame
    ):

        if frame is None:
            return


        display_frame = np.asarray(
            frame,
            dtype=np.uint8
        )


        cv2.imshow(
            self.window_name,
            display_frame
        )


    def step_display(
        self
    ):

        return cv2.waitKey(1)


    def close(
        self
    ):

        cv2.destroyAllWindows()