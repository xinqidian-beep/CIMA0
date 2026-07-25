import time

from core.cell import Cell
from core.compute import ComputeSystem
from core.observer import ObserverSystem


def main():

    print(
        "=== Phase8.1 Minimal World Loop ==="
    )


    N = 4096


    cells = [
        Cell(i)
        for i in range(N)
    ]


    # 注意：
    # 这里如果 Cell 未来有邻居关系，
    # Observer 只读取。
    #
    # 当前没有邻居时，
    # observation_field 仍然可以工作。


    observer = ObserverSystem(
        sample_size=64,
        # 时间观察窗口
        history_size=32,
        threshold=0.5,
        decay=0.90,
        spread=0.15,
        exploration=0.1
    )


    steps = 500000


    start = time.time()


    for t in range(steps):


        # =========================
        # L1 动力世界
        # =========================

        for cell in cells:

            cell.step()



        # =========================
        # L2 观察世界
        # =========================

        if t % 1000 == 0:


            observer.sample(
                cells,
                t
            )


            summary = (
                observer.summary()
            )


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