import random

from core.interaction import local_force


class Universe:


    def __init__(
        self,
        cells,
        topology
    ):

        self.cells=cells

        self.topology=topology

        self.time=0



    def step(
        self,
        events=1000
    ):


        for _ in range(events):

            i=random.randrange(
                len(self.cells)
            )


            cell=self.cells[i]


            neighbors=(
                self.topology
                .neighbors(i)
            )


            force=local_force(
                cell,
                neighbors
            )


            cell.step(
                force,
                0.001
            )


            self.time+=1