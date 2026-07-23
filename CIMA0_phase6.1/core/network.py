import numpy as np

from core.oscillator import Oscillator


class OscillatorNetwork:


    def __init__(
        self,
        n=128,
        avg_degree=4,
        coupling=0.08
    ):


        np.random.seed(42)


        self.n=n

        self.time=0

        self.coupling=coupling



        self.cells=[]


        for i in range(n):

            self.cells.append(

                Oscillator(

                    x=np.random.uniform(
                        -1.8,
                        1.8
                    ),

                    v=np.random.uniform(
                        -0.8,
                        0.8
                    ),

                    omega=np.random.uniform(
                        0.97,
                        1.03
                    )
                )

            )


        self.neighbors=[
            []
            for _ in range(n)
        ]


        self.build_network(avg_degree)



    def build_network(
        self,
        degree
    ):


        for i in range(self.n):

            targets=np.random.choice(

                [
                    j
                    for j in range(self.n)
                    if j!=i
                ],

                degree,

                replace=False
            )


            for j in targets:

                if j not in self.neighbors[i]:

                    self.neighbors[i].append(j)


                if i not in self.neighbors[j]:

                    self.neighbors[j].append(i)



    def local_field(
        self,
        i
    ):

        x=self.cells[i].x


        total=0.0


        for j in self.neighbors[i]:

            other=self.cells[j].x


            total += np.sin(
                other-x
            )


        if len(self.neighbors[i]):

            total /= len(
                self.neighbors[i]
            )


        return (
            self.coupling
            *
            total
        )



    def step(
        self,
        events=1
    ):


        for _ in range(events):


            # asynchronous

            i=np.random.randint(
                self.n
            )


            field=self.local_field(i)


            self.cells[i].step(
                field
            )


            self.time += 1