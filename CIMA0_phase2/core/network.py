import numpy as np
from core.oscillator import Oscillator



class OscillatorNetwork:


    def __init__(
        self,
        n=1000,
        degree=6,
        coupling=0.12
    ):

        self.n=n
        self.coupling=coupling


        self.nodes=[
            Oscillator(i)
            for i in range(n)
        ]


        self.edges=[]


        rng=np.random.default_rng(42)


        for i in range(n):

            neighbors=rng.choice(
                [
                    j for j in range(n)
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


        self.edges=np.array(
            self.edges
        )


    def step(self, active):


        forces=np.zeros(self.n)


        x=np.array(
            [
                node.x
                for node in self.nodes
            ]
        )


        for a,b in self.edges:

            diff=x[a]-x[b]

            f=self.coupling*np.sin(diff)

            forces[a]-=f
            forces[b]+=f



        for i in active:

            self.nodes[i].step(
                forces[i]
            )