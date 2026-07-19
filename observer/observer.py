import numpy as np


class Observer:


    def __init__(self):
        pass



    def measure(self, cloud):

        phases = []

        xs = []


        for c in cloud.cells:

            phase = np.arctan2(
                np.mean(c.v),
                np.mean(c.x)
            )

            phases.append(
                phase
            )

            xs.append(
                np.mean(c.x)
            )


        phases=np.array(phases)
        xs=np.array(xs)



        return {

            "phase_std":
                round(
                    float(np.std(phases)),
                    5
                ),


            "phase_coherence":
                round(
                    float(
                        abs(
                            np.mean(
                                np.exp(
                                    1j*phases
                                )
                            )
                        )
                    ),
                    5
                ),


            "avg_x":
                round(
                    float(
                        np.mean(xs)
                    ),
                    5
                ),


            "cells":

                len(cloud.cells)

        }
        
    def cluster(self, cloud):

        phases=[]

        for c in cloud.cells:

            p=np.arctan2(
                np.mean(c.v),
                np.mean(c.x)
            )

            phases.append(p)


        clusters=[]

        used=set()


        for i,p in enumerate(phases):

            if i in used:
                continue


            group=[]


            for j,q in enumerate(phases):

                diff=abs(
                    np.angle(
                        np.exp(1j*(p-q))
                    )
                )


                if diff<0.5:

                    group.append(j)
                    used.add(j)


            clusters.append(
                len(group)
            )


        return {

            "clusters":
                len(clusters),

            "max_cluster":
                max(clusters),

            "avg_cluster":
                sum(clusters)/len(clusters)

        }