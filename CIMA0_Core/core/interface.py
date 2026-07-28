class ByteInterface:
    """
    Pure byte IO interface.

    Responsibility:

        bytes in
        bytes out


    Does not:

        understand content
        extract features
        interpret meaning
        control internal state

    """


    def __init__(self):

        self.input_buffer = bytearray()

        self.output_buffer = bytearray()



    def push(
        self,
        data: bytes
    ):

        """
        Receive external byte stream.
        """

        self.input_buffer.extend(
            data
        )



    def read(
        self
    ):

        """
        Provide raw bytes.

        No decoding.
        """

        data = bytes(
            self.input_buffer
        )


        self.input_buffer.clear()


        return data



    def write(
        self,
        data: bytes
    ):

        """
        Output raw bytes.
        """

        self.output_buffer.extend(
            data
        )



    def flush_output(
        self
    ):

        """
        Return outgoing bytes.
        """

        data = bytes(
            self.output_buffer
        )


        self.output_buffer.clear()


        return data