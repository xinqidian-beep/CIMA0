class PacketView:
    """
    Partial view of packet.

    Keeps identity.
    """

    def __init__(
        self,
        packet,
        fields
    ):

        self.envelope = packet.envelope.copy()

        self.data = {}

        for field in fields:

            if hasattr(packet, field):

                self.data[field] = getattr(
                    packet,
                    field
                )


    @property
    def source(self):

        return self.envelope.source


    @property
    def tag(self):

        return self.envelope.tag