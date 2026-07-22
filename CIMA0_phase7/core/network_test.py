import numpy as np

from core.cell import Cell
from core.coupling import LocalCoupling



class CellNetwork:


    def __init__(
        self,
        n=32,
        degree=4,
        coupling_strength=0.01,
        seed=42
    ):

        np.random.seed(seed)

        self.n = n

        self.cells = []

        self.edges = []

        self.coupling = LocalCoupling(
            strength=coupling_strength
        )


        #
        # create independent cells
        #
        for i in range(n):

            self.cells.append(

                Cell(
                    x=np.random.uniform(-1,1),
                    v=np.random.uniform(-0.5,0.5)
                )

            )


        #
        # sparse local graph
        #
        self.create_graph(
            degree
        )



    def create_graph(
        self,
        degree
    ):

        """
        random local topology

        no global optimization
        """

        for i in range(self.n):

            neighbors = np.random.choice(
                [
                    j for j in range(self.n)
                    if j != i
                ],
                size=degree,
                replace=False
            )


            for j in neighbors:

                if i < j:

                    self.edges.append(
                        (i,j)
                    )



    def step(self):


        #
        # local interactions
        #
        for a,b in self.edges:

            self.coupling.connect(
                self.cells[a],
                self.cells[b]
            )



        #
        # local evolution
        #
        for c in self.cells:

            c.step()



    def snapshot(self):

        xs = np.array(
            [
                c.x
                for c in self.cells
            ]
        )


        gs = np.array(
            [
                c.g
                for c in self.cells
            ]
        )


        return {

            "mean_x":
                float(xs.mean()),

            "std_x":
                float(xs.std()),

            "active":
                int(
                    np.sum(
                        np.abs(xs)>0.1
                    )
                ),

            "mean_g":
                float(gs.mean()),

            "std_g":
                float(gs.std()),

            "edges":
                len(self.edges)
        }