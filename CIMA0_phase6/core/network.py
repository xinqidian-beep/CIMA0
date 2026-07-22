import numpy as np

from core.oscillator import Oscillator
from core.field import LocalField


class OscillatorNetwork:


    def __init__(
        self,
        n=1000,
        avg_degree=6,
        coupling=0.12,
        field_strength=0.05
    ):

        np.random.seed(42)


        self.n=n

        self.dt=0.02

        self.coupling=coupling

        self.field_strength=field_strength


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


        self.build_edges(
            avg_degree
        )


        self.field=LocalField(n)



    def build_edges(
        self,
        avg_degree
    ):

        edges_from=[]
        edges_to=[]


        for i in range(self.n):

            others=np.delete(
                np.arange(self.n),
                i
            )


            neighbors=np.random.choice(
                others,
                size=avg_degree,
                replace=False
            )


            for j in neighbors:

                if j>i:

                    edges_from.append(i)
                    edges_to.append(j)



        self.edges_from=np.array(
            edges_from
        )

        self.edges_to=np.array(
            edges_to
        )



    def state_arrays(self):

        x=np.array(
            [
                c.x
                for c in self.cells
            ]
        )


        return x



    def step(
        self,
        active_ids
    ):


        x=self.state_arrays()


        local_field=self.field.update(
            x,
            self.edges_from,
            self.edges_to
        )


        forces=np.zeros(
            self.n
        )


        diff=(
            x[self.edges_from]
            -
            x[self.edges_to]
        )


        f=(
            self.coupling *
            np.sin(diff)
        )


        np.add.at(
            forces,
            self.edges_from,
            f
        )

        np.add.at(
            forces,
            self.edges_to,
            -f
        )


        for i in active_ids:


            total_field=(
                forces[i]
                +
                self.field_strength *
                local_field[i]
            )


            self.cells[i].step(
                total_field
            )



    def snapshot(self):

        energy=np.array(
            [
                c.energy
                for c in self.cells
            ]
        )


        x=np.array(
            [
                c.x
                for c in self.cells
            ]
        )


        v=np.array(
            [
                c.v
                for c in self.cells
            ]
        )


        phase=np.arctan2(
            v,
            x
        )


        return {

            "mean_energy":
                float(
                    energy.mean()
                ),

            "energy_std":
                float(
                    energy.std()
                ),

            "max_energy":
                float(
                    energy.max()
                ),

            "phase_std":
                float(
                    phase.std()
                ),

            "field_std":
                float(
                    self.field.field.std()
                )
        }