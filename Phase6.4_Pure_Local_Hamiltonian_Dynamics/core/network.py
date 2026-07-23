import numpy as np
from core.body import Body



class LocalHamiltonianNetwork:


    def __init__(
        self,
        n=1024,
        degree=4,
        k=0.02,
        dt=0.01
    ):


        np.random.seed(42)


        self.n=n
        self.k=k
        self.dt=dt


        self.time=0


        self.bodies=[]


        for i in range(n):

            self.bodies.append(

                Body(

                    x=np.random.uniform(
                        -1,
                        1
                    ),

                    v=np.random.uniform(
                        -0.1,
                        0.1
                    )

                )

            )



        self.edges=[]


        self.build_local_graph(
            degree
        )



    def build_local_graph(
        self,
        degree
    ):


        for i in range(self.n):

            neighbors=np.random.choice(

                [
                    j for j in range(self.n)
                    if j!=i
                ],

                degree,

                replace=False

            )


            for j in neighbors:

                if i<j:

                    self.edges.append(
                        (i,j)
                    )




    def force(self,i):


        """
        only local force

        no global information
        """


        f=0.0


        xi=self.bodies[i].x


        for a,b in self.edges:


            if a==i:

                xj=self.bodies[b].x

                f += -self.k*(xi-xj)


            elif b==i:

                xj=self.bodies[a].x

                f += -self.k*(xi-xj)


        return f




    def step(self):


        dt=self.dt


        # half velocity

        acc=[]


        for i,b in enumerate(self.bodies):

            acc.append(
                self.force(i)/b.mass
            )



        for i,b in enumerate(self.bodies):

            b.v += (
                0.5*
                dt*
                acc[i]
            )



        # position update


        for b in self.bodies:

            b.x += (
                dt*
                b.v
            )



        # second force


        acc2=[]


        for i,b in enumerate(self.bodies):

            acc2.append(
                self.force(i)/b.mass
            )



        for i,b in enumerate(self.bodies):

            b.v += (
                0.5*
                dt*
                acc2[i]
            )



        self.time+=1




    def snapshot(self):


        x=np.array(
            [
                b.x
                for b in self.bodies
            ]
        )


        energy=np.array(

            [
                b.kinetic()
                for b in self.bodies
            ]

        )


        return {


            "time":
                self.time,


            "cells":
                self.n,


            "x_std":
                float(x.std()),


            "kinetic_mean":
                float(
                    energy.mean()
                ),


            "kinetic_std":
                float(
                    energy.std()
                )

        }