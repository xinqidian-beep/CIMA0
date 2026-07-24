from core.universe import Universe
from observer.observer import Observer
from compute.sparse import SparseCompute



def main():


    print(
        "=== CIMA0 Phase7.0.3 EvolutionField ==="
    )


    universe=Universe(
        4096
    )


    observer=Observer(
        64
    )


    compute=SparseCompute()



    for t in range(100000):


        # 1 动力自己运行

        universe.tick()



        # 2 观察者偶尔看

        if t % 100 == 0:


            obs=observer.sample(
                universe
            )


            # 3 计算形成压缩表示

            compute.compress(
                obs
            )



        if t % 10000 == 0:


            print(

                {
                    "time":
                    universe.time,

                    "observed":
                    len(compute.field)

                }

            )




if __name__=="__main__":

    main()