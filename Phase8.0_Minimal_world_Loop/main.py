import time

from core.cell import Cell
from core.observer import ObserverSystem
from core.cloud import CloudCollision


def main():

    print(
        "=== Phase8.2 Minimal World Loop + Cloud Collision ==="
    )


    N = 4096


    cells = [
        Cell(i)
        for i in range(N)
    ]


    observer = ObserverSystem(
        sample_size=64,
        history_size=8,
        threshold=0.5,
        decay=0.90,
        spread=0.15,
        exploration=0.1,
        window_size=32
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

        if t % 1000 == 0:


            observer.sample(
                cells,
                t
            )


            summary = observer.summary()


            print(
                {
                    "time": t,
                    "snapshot": summary
                }
            )



    print(
        "finished",
        time.time()-start
    )



if __name__ == "__main__":

    main()