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
        
    @property
    def source(self):
        return self._source


    @property
    def tag(self):
        return self._tag


    @property
    def schema(self):
        return self._schema


    @property
    def version(self):
        return self._version
    
    def copy(self):

        return PacketEnvelope(
            source=self.source,
            tag=self.tag,
            schema=self.schema,
            version=self.version
        )