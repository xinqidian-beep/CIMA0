import time

from core.cell import Cell
from core.cloud import Cloud
from core.observer import ObserverSystem



def main():

    print(
        "=== Phase8.3 Minimal World Loop ==="
    )


    N = 4096


    cells=[
        Cell(i)
        for i in range(N)
    ]


    cloud = Cloud(N)


    observer = ObserverSystem(
        min_sample=16,
        max_sample=128,
        observation_probability=1.0
    )


    steps=500000


    start=time.time()


    for t in range(steps):


        # =================
        # 世界推进
        # =================

        for c in cells:
            c.step()



        # =================
        # 云碰撞
        # =================

        if t % 100000 == 0:


            ids, values = cloud.collide()


            for cid,value in zip(ids,values):

                cells[cid].local_perturb(
                    value
                )


                print(
                    {
                        "cloud_collision":True,
                        "cell":int(cid),
                        "value":float(value),
                        "time":t
                    }
                )



        # =================
        # 快照
        # =================

        if t % 1000 == 0:


            snapshot = observer.sample(
                cells,
                t
            )


            print(
                {
                    "time":t,
                    "snapshot":snapshot
                }
            )



    print(
        "finished",
        time.time()-start
    )



if __name__=="__main__":
    main()
