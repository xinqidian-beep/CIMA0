import cv2


class CameraIO:
    """
    Pure camera acquisition port.


    Output:

        {
            bytes,
            shape,
            dtype
        }


    No:

        image processing
        resize
        color conversion
        interpretation
    """



    def __init__(
        self,
        index=0
    ):

        self.cap = cv2.VideoCapture(
            index
        )

        self.current_state = None



    def step(
        self
    ):

        packet = self._read()


        self.current_state = packet


        return packet



    def _read(
        self
    ):

        ok, frame = self.cap.read()


        if not ok:

            return None



        return {

            "bytes":
                frame.tobytes(),


            "shape":
                frame.shape,


            "dtype":
                str(frame.dtype)

        }



    def state(
        self
    ):

        return self.current_state