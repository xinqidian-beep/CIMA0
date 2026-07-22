import numpy as np


from core.cell import Cell
from core.coupling import LocalCoupling
from core.topology import AdaptiveTopology
from core.scheduler import DualTimeScheduler



class CellNetwork:


    def __init__(
        self,
        n=128,
        degree=4,
        coupling_strength=0.01,
        seed=42
    ):

        np.random.seed(seed)


        self.n = n


        self.cells = []

        self.edges = []



        # -----------------
        # create cells
        # -----------------

        for _ in range(n):

            self.cells.append(

                Cell(

                    x=np.random.uniform(
                        -1,
                        1
                    ),

                    v=np.random.uniform(
                        -0.5,
                        0.5
                    )

                )

            )



        # -----------------
        # initial topology
        # -----------------

        self._create_graph(
            degree
        )



        self.coupling = LocalCoupling(

            strength=coupling_strength

        )



        self.topology = AdaptiveTopology(

            n=self.n,

            initial_edges=self.edges

        )



        # -----------------
        # dual time scheduler
        # -----------------

        self.scheduler = DualTimeScheduler(

            self.cells

        )



        self.scheduler.update()



    # ==================================================
    # random initial graph
    # ==================================================

    def _create_graph(
        self,
        degree
    ):


        for i in range(self.n):


            neighbors = np.random.choice(

                [

                    j

                    for j in range(self.n)

                    if j != i

                ],

                size=degree,

                replace=False

            )



            for j in neighbors:


                if i < j:

                    self.edges.append(

                        (
                            i,
                            j
                        )

                    )



    # ==================================================
    # one evolution step
    # ==================================================

    def step(
        self,
        step_count
    ):


        # -----------------
        # refresh time structure
        # -----------------

        if step_count % 100 == 0:

            self.scheduler.update()



        fast = set(

            self.scheduler.fast_ids()

        )


        medium = set(

            self.scheduler.medium_ids()

        )


        slow = set(

            self.scheduler.slow_ids()

        )



        active = (

            fast
            |
            medium
            |
            slow

        )



        # -----------------
        # local coupling
        # -----------------

        self.coupling.clear()



        for a,b in self.edges:


            if (

                a in active

                or

                b in active

            ):


                self.coupling.connect(

                    self.cells[a],

                    self.cells[b]

                )



        self.coupling.apply()



        # -----------------
        # multi-timescale update
        # -----------------


        # fast cells

        for i in fast:

            self.cells[i].step()



        # medium cells

        if step_count % 10 == 0:


            for i in medium:

                self.cells[i].step()



        # slow cells

        if step_count % 1000 == 0:


            for i in slow:

                self.cells[i].step()



        # -----------------
        # slow topology evolution
        # -----------------

        if step_count % 1000 == 0:


            self.topology.update(

                [

                    c.x

                    for c in self.cells

                ]

            )



    # ==================================================
    # observation
    # ==================================================

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



        data = {


            "cells":

                self.n,


            "edges":

                len(self.edges),



            "x_std":

                float(
                    xs.std()
                ),



            "g_mean":

                float(
                    gs.mean()
                ),



            "g_std":

                float(
                    gs.std()
                ),



            "energy_mean":

                float(

                    np.mean(

                        [

                            c.energy

                            for c in self.cells

                        ]

                    )

                )

        }



        data.update(

            self.scheduler.stats()

        )


        data.update(

            self.topology.stats()

        )


        return data