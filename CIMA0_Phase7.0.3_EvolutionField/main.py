import time

from core.universe import Universe
from observer.observer import Observer
from compute.sparse import SparseCompute


def main():

    print(
        "=== CIMA0 Phase7.0.3 EvolutionField ==="
    )


    # ==========================
    # Dynamics
    # ==========================

    universe = Universe(
        n=4096,
        degree=4,
        coupling=0.01,
        seed=42
    )


    # ==========================
    # Observer
    # ==========================

    observer = Observer(
        sample_size=64
    )


    # ==========================
    # Compute
    # ==========================

    compute = SparseCompute(
        capacity=64
    )


    TOTAL_EVENTS = 10_000_000


    OBSERVE_INTERVAL = 100


    REPORT_INTERVAL = 100_000



    start=time.time()


    for step in range(
        TOTAL_EVENTS
    ):


        # ----------------------
        # 1.
        # Compute提供短暂扰动
        #
        # 不是控制
        # ----------------------

        perturb = compute.perturbation()



        # ----------------------
        # 2.
        # Dynamics自行推进
        #
        # 局部事件
        # 局部耦合
        # ----------------------

        universe.event(
            perturb
        )



        # ----------------------
        # 3.
        # Observer偶尔观察
        #
        # 不扫描全局
        # ----------------------

        if step % OBSERVE_INTERVAL == 0:


            observations = observer.sample(
                universe
            )


            compute.compress(
                observations
            )



        # ----------------------
        # 4.
        # 外部观察输出
        # ----------------------

        if step % REPORT_INTERVAL == 0:


            snap = universe.snapshot()


            print(
                snap,
                "compute_field=",
                len(compute.field)
            )



    print(
        "finished",
        "time=",
        time.time()-start
    )



if __name__=="__main__":

    main()