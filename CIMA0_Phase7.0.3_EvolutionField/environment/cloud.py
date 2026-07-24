from memory.trace import TraceMemory



class CloudField:


    def __init__(
        self,
        n
    ):

        self.memory=TraceMemory(n)



    def disturb(
        self,
        ids,
        universe
    ):

        for i in ids:

            x=universe.cells[i].x


            # 只记录

            self.memory.add(
                i,
                abs(x)*0.001
            )



    def evolve(self):

        self.memory.decay()



    def field(self):

        return self.memory.trace