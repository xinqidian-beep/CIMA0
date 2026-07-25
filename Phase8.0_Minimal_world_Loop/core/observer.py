import numpy as np

from core.snapshot import Snapshot



class ObserverSystem:
    """
    Observer only.

    Does not control.
    Does not modify Cell.

    It creates temporary descriptions
    from snapshots.
    """

    def __init__(
        self,
        sample_size=64,
        history_size=8
    ):

        self.sample_size = sample_size

        self.history_size = history_size

        self.snapshots = []

        self.observe_ids = None



    def sample(self, cells, time):

        n = len(cells)


        if self.observe_ids is None:

            ids = np.random.choice(
                n,
                size=min(
                    self.sample_size,
                    n
                ),
                replace=False
            )

            self.observe_ids = set(ids)



        states = {}

        for i in self.observe_ids:

            s = cells[i].state()

            states[i] = {

                "x": s["x"],
                "v": s["v"]

            }



        snapshot = Snapshot(
            time,
            states
        )


        self.snapshots.append(snapshot)


        if len(self.snapshots) > self.history_size:

            self.snapshots.pop(0)


        return snapshot



    def activity(self):

        """
        Snapshot difference only.

        Not a Cell variable.
        """

        if len(self.snapshots) < 2:

            return {}


        old = self.snapshots[-2]

        new = self.snapshots[-1]


        result = {}


        for cid in new.ids():

            if cid not in old.states:
                continue


            dx = (
                new.states[cid]["x"]
                -
                old.states[cid]["x"]
            )

            dv = (
                new.states[cid]["v"]
                -
                old.states[cid]["v"]
            )


            result[cid] = abs(dx) + abs(dv)


        return result



    def summary(self):

        act = self.activity()


        if not act:

            return {}


        values = list(act.values())


        return {

            "observed":
                len(values),

            "activity_mean":
                float(np.mean(values)),

            "activity_max":
                float(np.max(values))

        }