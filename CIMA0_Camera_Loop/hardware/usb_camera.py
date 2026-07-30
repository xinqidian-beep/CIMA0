import cv2


class USBCamera:
    """
    USB camera hardware adapter.


    Responsibility:

        hardware access only


    No:

        image processing
        sampling
        computation
        interpretation
    """



    def __init__(
        self,
        device_id=0
    ):

        self.camera = cv2.VideoCapture(
            device_id
        )



    def read(self):

        """
        Read raw camera frame.

        Return:

            raw frame
            None if failed
        """


        ok, frame = (
            self.camera.read()
        )


        if not ok:

            return None


        return frame



    def release(self):

        """
        Release hardware resource.
        """


        self.camera.release()