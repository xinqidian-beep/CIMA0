class Snapshot:
    """
    Read-only snapshot.

    Only records observed state.

    Does not affect dynamics.
    """

    def __init__(self, time, states):

        self.time = time

        self.states = states


    def get(self, cid):

        return self.states.get(cid)


    def ids(self):

        return self.states.keys()