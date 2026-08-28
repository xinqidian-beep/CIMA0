class TransportRouter:
    """
    Information flow router.

    No meaning.
    No control.
    """


    def __init__(self):

        self.subscribers = {}



    def subscribe(
        self,
        tag,
        receiver
    ):

        if tag not in self.subscribers:

            self.subscribers[tag] = []


        self.subscribers[tag].append(
            receiver
        )



    def publish(
        self,
        packet
    ):
        print(
            "ROUTER:",
            packet.source,
            packet.tag,
            packet.schema
        )
        receivers = self.subscribers.get(
            packet.tag,
            []
        )


        for receiver in receivers:

            receiver.receive(
                packet
            )