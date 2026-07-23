import random


class AdaptiveTopology:


    def __init__(
        self,
        n,
        avg_degree=4
    ):

        self.n = n


        self.edges = {}

        self.weights = {}


        for i in range(n):

            self.edges[i] = set()


        # 初始局部网络

        for i in range(n):

            targets = random.sample(
                range(n),
                min(
                    avg_degree,
                    n-1
                )
            )


            for j in targets:

                if j != i:

                    self.edges[i].add(j)

                    self.weights[
                        (i,j)
                    ] = random.uniform(
                        0.1,
                        1.0
                    )



    def neighbors(self,i):

        return self.edges[i]



    def weight(self,i,j):

        return self.weights.get(
            (i,j),
            0.1
        )



    def edge_count(self):

        return sum(
            len(v)
            for v in self.edges.values()
        )