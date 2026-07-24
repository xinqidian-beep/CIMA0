from core.universe import Universe
from observer.observer import Observer
from compute.sparse import SparseCompute



def main():


    print(
        "=== CIMA0 Phase7.0.3 EvolutionField ==="
    )


    u=Universe(
        4096,
        degree=4
    )


    observer=Observer(64)

    compute=SparseCompute(64)



    for t in range(
        10000000
    ):


        # 动力事件

        u.event()



        # 观察不是连续的

        if t % 100 == 0:


            obs=observer.sample(
                u
            )


            compute.compress(
                obs
            )



        if t % 10000==0:


            print(
                u.snapshot()
            )



if __name__=="__main__":

    main()