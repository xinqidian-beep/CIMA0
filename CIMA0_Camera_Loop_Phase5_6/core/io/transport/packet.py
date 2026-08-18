from .envelope import PacketEnvelope


class BitPacket:
    """
    Universal information packet.

    Carries:

        identity
        structure
        bytes payload

    Does not interpret meaning.
    """


    def __init__(
        self,
        source,
        tag,
        data=None,
        shape=None,
        dtype=None,
        schema="raw",
        meta=None
    ):


        self.envelope = PacketEnvelope(
            source=source,
            tag=tag,
            schema=schema
        )


        self.data = data

        self.shape = shape

        self.dtype = dtype

        self.meta = meta or {}



    @property
    def source(self):

        return self.envelope.source



    @property
    def tag(self):

        return self.envelope.tag



    def view(
        self,
        fields
    ):

        from .view import PacketView

        return PacketView(
            self,
            fields
        )
