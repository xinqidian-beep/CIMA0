from core.cell import Cell


class World:


    def __init__(self,n):

        self.cells=[

            Cell(i)

            for i in range(n)

        ]


        self.time=0



    def step(self,environment):


        self.time+=1


        cloud=environment.cloud()


        for c in self.cells:


            # 每个人只收到世界扰动

            c.step(
                cloud
            )



    def snapshot(self):


        energy=[

            c.energy

            for c in self.cells

        ]


        x=[

            c.x

            for c in self.cells

        ]


        return {

            "time":
                self.time,

            "energy_mean":
                sum(energy)
                /
                len(energy),

            "x_std":
                __import__(
                    "numpy"
                ).std(x)

        }