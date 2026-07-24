import numpy as np

from core.cell import Cell



class Universe:


    def __init__(
        self,
        n,
        avg_neighbors,
        dt,
        omega_min,
        omega_max,
        seed
    ):


        np.random.seed(seed)


        self.time = 0


        self.cells=[]


        for i in range(n):

            self.cells.append(

                Cell(

                    x=np.random.uniform(
                        -1,
                        1
                    ),

                    v=np.random.uniform(
                        -0.5,
                        0.5
                    ),

                    omega=np.random.uniform(
                        omega_min,
                        omega_max
                    ),

                    dt=dt
                )
            )


        self.neighbors={}


        self.build_network(
            avg_neighbors
        )



    def build_network(
        self,
        degree
    ):


        n=len(
            self.cells
        )


        for i in range(n):

            choices=np.delete(
                np.arange(n),
                i
            )


            self.neighbors[i]=list(

                np.random.choice(

                    choices,

                    degree,

                    replace=False

                )

            )



    def local_force(
        self,
        i
    ):


        force=0.0


        xi=self.cells[i].x


        for j in self.neighbors[i]:


            xj=self.cells[j].x


            force += (
                0.02 *
                np.sin(
                    xj-xi
                )
            )


        return force



    def event(self):


        i=np.random.randint(

            len(self.cells)

        )


        force=self.local_force(
            i
        )


        self.cells[i].step(
            force
        )


        self.time += 1



    def step(
        self,
        events
    ):


        for _ in range(events):

            self.event()