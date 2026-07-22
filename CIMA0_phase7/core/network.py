import numpy as np
import heapq


from core.cell import Cell
from core.coupling import LocalCoupling
from core.topology import AdaptiveTopology



class CellNetwork:



    def __init__(
        self,
        n=128,
        degree=4,
        coupling_strength=0.01,
        active_ratio=0.25,
        seed=42
    ):


        np.random.seed(seed)


        self.n=n

        self.active_ratio=active_ratio


        self.cells=[]

        self.edges=[]


        self.coupling=LocalCoupling(
            strength=coupling_strength
        )


        for _ in range(n):

            self.cells.append(

                Cell(
                    x=np.random.uniform(-1,1),
                    v=np.random.uniform(-0.5,0.5)
                )

            )



        self._create_graph(
            degree
        )


        self.topology=AdaptiveTopology(

            n=self.n,

            initial_edges=self.edges

        )



        self.active_queue=[]



    def _create_graph(
        self,
        degree
    ):


        for i in range(self.n):


            neighbors=np.random.choice(

                [
                    j
                    for j in range(self.n)
                    if j!=i
                ],

                size=degree,

                replace=False

            )


            for j in neighbors:


                if i<j:

                    self.edges.append(
                        (i,j)
                    )



    #
    # observer only
    #

    def active_cells(self):


        queue=[]


        for i,c in enumerate(self.cells):


            activity=(

                abs(c.x)
                +
                0.1*abs(c.v)

            )


            heapq.heappush(

                queue,

                (
                    -activity,
                    i
                )

            )



        result=[]


        count=max(

            1,

            int(
                self.n*self.active_ratio
            )

        )


        for _ in range(count):


            if queue:

                _,idx=heapq.heappop(queue)

                result.append(idx)



        return result



    def step(
        self,
        step_count
    ):



        active=self.active_cells()



        #
        # small natural exploration
        #

        random_count=max(

            1,

            self.n//20

        )


        random_cells=np.random.choice(

            self.n,

            random_count,

            replace=False

        )


        update_set=set(active)

        update_set.update(
            random_cells
        )



        #
        # local coupling
        #

        for a,b in self.edges:


            if (

                a in update_set
                or
                b in update_set

            ):


                w=self.topology.get_weight(
                    a,b
                )


                self.coupling.connect(

                    self.cells[a],

                    self.cells[b],

                    strength=w

                )



        self.coupling.apply()



        #
        # evolve selected cells
        #

        for idx in update_set:


            self.cells[idx].step()



        #
        # very slow topology observation
        #

        if step_count % 5000 == 0:


            self.topology.update(

                [
                    c.x
                    for c in self.cells
                ]

            )



    def snapshot(self):


        xs=np.array(

            [
                c.x
                for c in self.cells
            ]

        )


        gs=np.array(

            [
                c.g
                for c in self.cells
            ]

        )


        fs=np.array(

            [
                c.fatigue
                for c in self.cells
            ]

        )


        energy=np.array(

            [
                c.energy
                for c in self.cells
            ]

        )


        top_id=int(
            np.argmax(
                np.abs(xs)
            )
        )


        return {


            "cells":
                self.n,


            "edges":
                len(self.edges),


            "x_std":
                float(xs.std()),


            "g_mean":
                float(gs.mean()),


            "energy_mean":
                float(energy.mean()),


            "fatigue_mean":
                float(fs.mean()),


            "fatigue_std":
                float(fs.std()),


            "top_cell":
                top_id,


            "top_activity":
                float(
                    abs(xs[top_id])
                )

        }