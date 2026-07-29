import cv2


class USBCamera:
    """
    USB camera hardware.

    External physical boundary.

    Responsible:

        acquire raw frame

    Does not:

        interpret image
        analyze content
        control CIMA
    """


    def __init__(
        self,
        device_id=0
    ):

        self.camera = cv2.VideoCapture(
            device_id
        )


    def read(self):

        ok, frame = self.camera.read()

        if not ok:
            return None

        return frame



    def close(self):

        self.camera.release()