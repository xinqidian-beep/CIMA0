import cv2


class CameraIO:

    def __init__(self, index=0):
        self.cap = cv2.VideoCapture(index)

        self.previous_state = None
        self.current_state = None


    def step(self):
        frame = self._read()

        self.previous_state = self.current_state
        self.current_state = frame


    def _read(self):

        ok, frame = self.cap.read()

        if not ok:
            return None

        return {
            "frame": frame,
            "shape": frame.shape,
            "dtype": str(frame.dtype)
        }


    def state(self):
        return self.current_state