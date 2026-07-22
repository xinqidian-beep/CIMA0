class Edge:


    def __init__(
        self,
        a,
        b,
        weight=0.5
    ):

        self.a = a
        self.b = b

        self.weight = weight

        self.age = 0



    def activity(
        self,
        cells
    ):

        ca = cells[self.a]
        cb = cells[self.b]

        return ca.x * cb.x



    def step(
        self,
        cells
    ):

        corr = self.activity(cells)


        # 相关增强
        self.weight += (
            0.00001 *
            corr
        )


        # 自然消耗
        self.weight *= 0.999995


        if self.weight < 0:
            self.weight = 0


        self.age += 1



    def alive(self):

        return self.weight > 0.01