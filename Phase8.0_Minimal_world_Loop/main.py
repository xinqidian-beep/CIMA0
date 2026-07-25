import time

from core.cell import Cell
from core.observer import ObserverSystem
from core.cloud import CloudCollision


def main():

    print(
        "=== Phase8.3 Minimal World Loop + Cloud Collision ==="
    )


    N = 4096


    cells = [
        Cell(i)
        for i in range(N)
    ]


    observer = ObserverSystem(
        min_sample=16,
        max_sample=128,
        observation_probability=0.01
    )


    cloud = CloudCollision()


    steps = 500000


    collision_time = 100000
    collision_id = 123
    collision_value = 0.8


    start = time.time()


    for t in range(steps):


        # =========================
        # L1 动力世界
        # =========================

        for cell in cells:

            cell.step()



        # =========================
        # L4 云碰撞
        # =========================

        if t == collision_time:

            result = cloud.collide(
                cells[collision_id],
                collision_value
            )

            print(
                {
                    "cloud_collision": result,
                    "cell": collision_id,
                    "value": collision_value,
                    "time": t
                }
            )



        # =========================
        # L2 Observer
        # =========================

        if observer.should_observe(t):

            snapshot = observer.sample(
                cells,
                t
            )

            print(
                {
                    "snapshot": snapshot
                }
            )



    print(
        "finished",
        time.time()-start
    )



if __name__ == "__main__":

    main()