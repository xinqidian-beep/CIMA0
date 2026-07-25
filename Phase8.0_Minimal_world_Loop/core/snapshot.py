class Snapshot:
    """
    Immutable observation snapshot.

    Only stores observed information.

    Never affects dynamics.
    """

    def __init__(self, time, states):

        self.time = time

        self.states = states


    def get(self, cid):

        return self.states.get(cid)


    def ids(self):

        return self.states.keys()