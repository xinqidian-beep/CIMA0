import numpy as np


class CloudPerturbation:


    def __init__(
        self,
        strength=0.5,
        radius=50,
        probability=0.001
    ):

        self.strength = strength
        self.radius = radius
        self.probability = probability

        self.total_events = 0

    def apply(
        self,
        network
    ):

        # 没有扰动事件
        if np.random.random() > self.probability:
            return None
        self.total_events += 1

        center=np.random.randint(
            network.n
        )


        ids=np.arange(
            network.n
        )


        distance=np.abs(
            ids-center
        )


        mask = (
            distance < self.radius
        )


        selected=np.where(
            mask
        )[0]


        noise=np.random.normal(
            0,
            self.strength,
            len(selected)
        )


        for idx,n in zip(
            selected,
            noise
        ):
            network.cells[idx].v += n


        return {
            "center": int(center),
            "affected": int(len(selected))
        }