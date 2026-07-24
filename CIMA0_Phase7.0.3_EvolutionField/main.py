from core.universe import Universe
from observer.observer import Observer
from compute.sparse import SparseCompute



def main():


    print(
        "=== CIMA0 Phase7.0.3 Sparse Evolution ==="
    )


    u=Universe(
        4096
    )


    observer=Observer(
        64
    )


    compute=SparseCompute()



    for t in range(100000):


        # 观察
        obs=observer.sample(u)



        # 计算系统吸收
        compute.receive(obs)



        # 计算系统决定展开
        ids=compute.select_precision()



        # 动力推进
        u.evolve_cells(ids)



        u.time+=1



        if t%10000==0:

            print(
                u.snapshot()
            )



if __name__=="__main__":

    main()