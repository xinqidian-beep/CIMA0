from .cell import Cell
from .dynamics import local_update


class Cloud:


    def __init__(self, size=128):

        self.cells=[
            Cell(i)
            for i in range(size)
        ]


    def step(self):

        for c in self.cells:

            neighbors = self.get_neighbors(c)

            local_update(
                c,
                neighbors
            )


    def get_neighbors(self,cell):

        i=cell.id

        ids=[
            (i-1)%len(self.cells),
            (i+1)%len(self.cells)
        ]

        return [
            self.cells[x]
            for x in ids
        ]


    def statistics(self):

        energy=[
            c.energy
            for c in self.cells
        ]

        return {

            "mean_energy":
            sum(energy)/len(energy),

            "active":
            sum(
                1
                for e in energy
                if e>0.1
            )

        }
        
    def phase_coherence(self):

        import numpy as np

        phases = np.array(
            [
                c.phase
                for c in self.cells
            ]
        )

        return abs(
            np.mean(
                np.exp(1j*phases)
            )
        )