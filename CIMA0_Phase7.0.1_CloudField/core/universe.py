import random
from core.cell import Cell
from core.cloud import Cloud


class Universe:


    def __init__(
        self,
        n=4096,
        neighbors=4
    ):


        self.cells=[
            Cell()
            for _ in range(n)
        ]


        self.links=[]


        for i in range(n):

            ns=random.sample(
                range(n),
                neighbors
            )

            self.links.append(ns)


        self.cloud=Cloud()

        self.time=0



    def event(self):


        i=random.randrange(
            len(self.cells)
        )


        cell=self.cells[i]


        coupling=0


        for j in self.links[i]:

            other=self.cells[j]

            coupling+=(
                other.x-cell.x
            )*0.01



        disturbance=self.cloud.perturb()



        cell.step(
            coupling,
            disturbance
        )


        self.time+=1



    def step(self,n):

        for _ in range(n):

            self.event()