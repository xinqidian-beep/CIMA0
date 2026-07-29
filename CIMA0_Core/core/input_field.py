class IOField:
    """
    Pure boundary.

    byte enters.
    byte leaves.

    No semantic interpretation.
    """

    def __init__(self):

        self.io_ephemeral_input_bytes = b""

        self.io_ephemeral_output_bytes = b""


    def receive_io_ephemeral_bytes(
        self,
        io_bytes
    ):

        self.io_ephemeral_input_bytes = bytes(
            io_bytes
        )


    def project_io_ephemeral_bytes(
        self
    ):

        """
        Internal system may read
        raw bytes.

        IO does not transform.
        """

        return self.io_ephemeral_input_bytes



    def receive_io_ephemeral_output(
        self,
        io_bytes
    ):

        self.io_ephemeral_output_bytes = bytes(
            io_bytes
        )


    def emit_io_ephemeral_bytes(
        self
    ):

        io_result = self.io_ephemeral_output_bytes

        self.io_ephemeral_output_bytes = b""

        return io_result