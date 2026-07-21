import numpy as np
from oscillator import Oscillator


class OscillatorNetwork:

    def __init__(
        self,
        n=1000,
        coupling=0.12,
        avg_degree=6
    ):

        self.n = n
        self.dt = 0.02
        self.coupling = coupling


        self.nodes = [
            Oscillator(
                omega=np.random.uniform(
                    0.97,
                    1.03
                )
            )
            for _ in range(n)
        ]


        self.edges_from = []
        self.edges_to = []


        self.build_graph(avg_degree)


    def build_graph(self, avg_degree):

        for i in range(self.n):

            others = np.delete(
                np.arange(self.n),
                i
            )

            neighbors = np.random.choice(
                others,
                size=avg_degree,
                replace=False
            )


            for j in neighbors:

                if j > i:
                    self.edges_from.append(i)
                    self.edges_to.append(j)



        self.edges_from = np.array(
            self.edges_from
        )

        self.edges_to = np.array(
            self.edges_to
        )



    def step(self):

        forces = np.zeros(self.n)


        phase_i = np.array(
            [
                self.nodes[i].phase()
                for i in self.edges_from
            ]
        )

        phase_j = np.array(
            [
                self.nodes[j].phase()
                for j in self.edges_to
            ]
        )


        interaction = (
            self.coupling *
            np.sin(
                phase_j-phase_i
            )
        )


        np.add.at(
            forces,
            self.edges_from,
            interaction
        )

        np.add.at(
            forces,
            self.edges_to,
            -interaction
        )


        for i,node in enumerate(self.nodes):

            node.step(
                forces[i],
                self.dt
            )