import time
import numpy as np

from core.universe import Universe
from observer.observer import Observer


# ============================
# 云扰动
# ============================

class CloudPerturbation:

    def __init__(
        self,
        strength=0.001,
        count=64,
        seed=42
    ):
        self.strength = strength
        self.count = count
        self.rng = np.random.default_rng(seed)


    def inject(self, universe):

        n = len(universe.cells)

        ids = self.rng.choice(
            n,
            size=self.count,
            replace=False
        )


        field = {}

        for i in ids:

            field[int(i)] = (
                self.rng.uniform(
                    -self.strength,
                    self.strength
                )
            )

        return field



# ============================
# 主程序
# ============================

def main():


    print(
        "=== CIMA0 Phase7.0.3 EvolutionField ==="
    )


    # ------------------------
    # 动力系统
    # ------------------------

    universe = Universe(
        n=4096,
        degree=8,
        seed=42
    )


    # ------------------------
    # Observer
    # ------------------------

    observer = Observer()


    # ------------------------
    # Compute
    # ------------------------

    cloud = CloudPerturbation(
        strength=0.001,
        count=64
    )


    total_steps = 100_000_000


    report_interval = 1_000_000


    last_response = None



    start=time.time()


    while universe.time < total_steps:


        # ====================
        # 云扰动
        # ====================

        perturb = None


        if universe.time % report_interval == 0:

            before = np.array(
                [
                    c.x
                    for c in universe.cells
                ]
            )


            perturb = cloud.inject(
                universe
            )


        # ====================
        # 动力事件
        # ====================

        universe.event(
            perturb=perturb
        )


        # ====================
        # 记录响应
        # ====================

        if (
            universe.time % report_interval
            == report_interval - 1
        ):


            after = np.array(
                [
                    c.x
                    for c in universe.cells
                ]
            )


            response = (
                after-before
            )


            observer.record(
                response
            )


            stats = universe.snapshot()


            print(
                {
                    "time":
                        universe.time,

                    "energy_mean":
                        stats["energy_mean"],

                    "x_std":
                        stats["x_std"],

                    "response_std":
                        float(
                            np.std(
                                response
                            )
                        ),

                    "response_active":
                        int(
                            np.sum(
                                np.abs(response)
                                >
                                1e-8
                            )
                        )
                }
            )


    print(
        "finished",
        time.time()-start
    )



if __name__ == "__main__":

    main()