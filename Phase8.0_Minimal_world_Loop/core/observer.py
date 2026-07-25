import numpy as np

from core.snapshot import Snapshot


class ObserverSystem:
    """
    Observer only.

    It observes.

    It does not:
        change Cell
        inject force
        control dynamics


    Observation field:
        temporary
        decaying
        local propagation

    It is not part of the world.
    """

    def __init__(
        self,
        sample_size=64,
        history_size=8,
        threshold=0.5,
        decay=0.90,
        spread=0.15,
        exploration=0.1
    ):

        self.sample_size = sample_size

        self.history_size = history_size

        self.threshold = threshold

        self.decay = decay

        self.spread = spread

        self.exploration = exploration


        self.snapshots = []


        # 观察场
        # cid -> strength
        self.observation_field = {}



    def choose_samples(self, cells):

        n = len(cells)

        budget = self.sample_size


        chosen = set()


        # --------------------------------
        # 1. 利用已有观察场
        # --------------------------------

        if self.observation_field:


            ids = list(
                self.observation_field.keys()
            )


            weights = np.array(
                [
                    self.observation_field[i]
                    for i in ids
                ],
                dtype=float
            )


            if weights.sum() > 0:

                weights /= weights.sum()


                count = int(
                    budget *
                    (1.0-self.exploration)
                )


                selected = np.random.choice(
                    ids,
                    size=min(
                        count,
                        len(ids)
                    ),
                    replace=False,
                    p=weights
                )


                chosen.update(
                    selected
                )



        # --------------------------------
        # 2. 随机探索
        # --------------------------------

        remain = budget - len(chosen)


        if remain > 0:

            candidates = list(
                set(range(n))
                -
                chosen
            )


            if candidates:

                extra = np.random.choice(
                    candidates,
                    size=min(
                        remain,
                        len(candidates)
                    ),
                    replace=False
                )


                chosen.update(extra)



        return list(chosen)



    def sample(self, cells, time):

        ids = self.choose_samples(
            cells
        )


        states = {}


        for i in ids:

            s = cells[i].state()

            states[i] = {

                "x": s["x"],
                "v": s["v"]

            }


        snapshot = Snapshot(
            time,
            states
        )


        self.snapshots.append(
            snapshot
        )


        if len(self.snapshots) > self.history_size:

            self.snapshots.pop(0)



        self.update_observation_field(
            cells
        )


        return snapshot



    def temporal_activity(self):


        if len(self.snapshots) < 2:

            return {}


        old = self.snapshots[-2]

        new = self.snapshots[-1]


        activity = {}


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


            activity[cid] = (
                abs(dx)
                +
                abs(dv)
            )


        return activity



    def update_observation_field(
        self,
        cells
    ):


        # ----------------------------
        # 1. 衰减旧观察
        # ----------------------------

        remove = []


        for cid in self.observation_field:

            self.observation_field[cid] *= self.decay


            if self.observation_field[cid] < 0.01:

                remove.append(cid)



        for cid in remove:

            del self.observation_field[cid]



        # ----------------------------
        # 2. 当前举手
        # ----------------------------

        activity = self.temporal_activity()


        for cid, value in activity.items():

            if value > self.threshold:

                self.observation_field[cid] = 1.0



        # ----------------------------
        # 3. 局部传播
        # ----------------------------

        new_signal = {}


        for cid, strength in self.observation_field.items():

            if strength <= 0:

                continue


            neighbors = getattr(
                cells[cid],
                "neighbors",
                []
            )


            for nid in neighbors:

                new_signal[nid] = (
                    new_signal.get(nid,0)
                    +
                    strength*self.spread
                )



        for nid,value in new_signal.items():

            self.observation_field[nid] = max(

                self.observation_field.get(
                    nid,
                    0
                ),

                value

            )



    def summary(self):

        activity = self.temporal_activity()


        return {

            "observed":
                len(activity),

            "activity_mean":
                float(
                    np.mean(
                        list(activity.values())
                    )
                )
                if activity else 0.0,


            "observation_field_size":
                len(self.observation_field),


            "observation_strength":
                float(
                    sum(
                        self.observation_field.values()
                    )
                )

        }