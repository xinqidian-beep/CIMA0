class PacketEnvelope:
    """
    Immutable identity layer.

    Always travels with packet.

    Never remove.
    """

    def __init__(
        self,
        source,
        tag,
        schema="raw",
        version=1
    ):

        self.source = source
        self.tag = tag
        self.schema = schema
        self.version = version


    def copy(self):

        return PacketEnvelope(
            source=self.source,
            tag=self.tag,
            schema=self.schema,
            version=self.version
        )