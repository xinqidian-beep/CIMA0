class CameraIO:
    """
    Pure byte transport.

    No:

        decoding
        sampling
        interpretation
    """


    def encode(self, data):

        if data is None:
            return b""

        return bytes(data)



    def decode(self, data):

        if data is None:
            return b""

        return bytes(data)