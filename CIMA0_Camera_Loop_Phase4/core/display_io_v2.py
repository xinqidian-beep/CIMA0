class DisplayIO:

    def __init__(self):
        self.frame = None


    def receive(
        self,
        data,
        shape,
        dtype
    ):

        self.frame = np.frombuffer(
            data,
            dtype=dtype
        ).reshape(shape)


    def show(self):

        cv2.imshow(
            "CIMA0",
            self.frame
        )