import time

import numpy as np


from core.universe import Universe
from observer.observer import Observer
from compute.compute import Compute
from cloud.cloud import Cloud



# =========================
# 参数
# =========================

N = 4096

TOTAL_EVENTS = 20_000_000

REPORT_INTERVAL = 100_000


# 云参数

CLOUD_TIME = 2_000_000

CLOUD_DURATION = 500_000

CLOUD_CENTER = 2048

CLOUD_RADIUS = 5

CLOUD_STRENGTH = 0.05



# =========================
# 主程序
# =========================

def main():


    print(
        "=== CIMA0 Phase7.0.4 CloudPerturbation ==="
    )


    universe = Universe(
        n=N
    )


    observer = Observer()


    compute = Compute(
        sample_size=64
    )


    cloud = None


    start = time.time()



    for step in range(
        TOTAL_EVENTS
    ):


        #
        # 默认无扰动
        #
        perturb = {}



        #
        # 云进入
        #
        if (
            universe.time >= CLOUD_TIME
            and universe.time <
            CLOUD_TIME + CLOUD_DURATION
        ):


            if cloud is None:

                cloud = Cloud(
                    center=CLOUD_CENTER,
                    radius=CLOUD_RADIUS,
                    strength=CLOUD_STRENGTH
                )


                print(
                    "\n[CLOUD ENTER]"
                )


            perturb = cloud.contact()



        #
        # 世界自行运行
        #
        universe.event(
            perturb
        )



        #
        # 观察
        #
        if (
            universe.time %
            REPORT_INTERVAL
            == 0
        ):


            obs = observer.observe(
                universe
            )


            result = compute.process(
                universe,
                obs
            )


            stats = universe.stats()



            changed = 0


            if perturb:

                changed = len(
                    perturb
                )



            print(
                {
                    "time":
                        universe.time,


                    "energy_mean":
                        stats["energy_mean"],


                    "energy_std":
                        stats["energy_std"],


                    "x_std":
                        stats["x_std"],


                    "cloud_cells":
                        changed,


                    "observer":
                        obs,


                    "compute":
                        result
                }
            )



    print(
        "finished",
        time.time()-start
    )



if __name__ == "__main__":

    main()