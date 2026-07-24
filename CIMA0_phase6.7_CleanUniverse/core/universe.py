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

        self.dt = dt

        self.cells=[]


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
                    ),

                    omega=np.random.uniform(
                        omega_min,
                        omega_max
                    ),

                    dt=dt
                )
            )


        self.edges={}


        ids=np.arange(n)


        for i in ids:

            others=np.delete(
                ids,
                i
            )

            self.edges[i]=list(

                np.random.choice(
                    others,
                    size=avg_neighbors,
                    replace=False
                )

            )



    def local_force(
        self,
        i
    ):

        cell=self.cells[i]


        force=0.0


        for j in self.edges[i]:

            other=self.cells[j]


            # weak local coupling

            force += (
                0.01 *
                np.sin(
                    other.x-cell.x
                )
            )


        return force



    def event(self):


        i=np.random.randint(
            len(self.cells)
        )


        f=self.local_force(i)


        self.cells[i].step(
            f
        )


        self.time += 1



    def step(
        self,
        events
    ):

        for _ in range(events):

            self.event()



    def raw_state_sample(
        self,
        count=256
    ):

        ids=np.random.choice(
            len(self.cells),
            size=count,
            replace=False
        )


        xs=[]

        vs=[]


        for i in ids:

            c=self.cells[i]

            xs.append(c.x)

            vs.append(c.v)


        return np.array(xs),np.array(vs)