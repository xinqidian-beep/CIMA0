import cv2
import numpy as np


class DisplayIO:
    """
    Display boundary IO.


    Responsibility:

        transfer output frame
        to display hardware


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



    def output_frame(
        self,
        frame
    ):

        if frame is None:
            return


        display_frame = frame

            

        cv2.imshow(
            self.window_name,
            frame
        )



    def step_display(
        self
    ):

        return cv2.waitKey(1)