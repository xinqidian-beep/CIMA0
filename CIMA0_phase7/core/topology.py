import random


class AdaptiveTopology:


    def __init__(
        self,
        n
    ):

        self.n=n

        self.edges={}

        self.weights={}


        for i in range(n):

            self.edges[i]=set()



        for i in range(n):

            for _ in range(4):

                j=random.randrange(n)

                if j!=i:

                    self.edges[i].add(j)

                    self.weights[
                        (i,j)
                    ]=0.5




    def neighbors(
        self,
        i
    ):

        return self.edges[i]



    def weight(
        self,
        i,
        j
    ):

        return self.weights.get(
            (i,j),
            0.0
        )



    def edge_count(self):

        return sum(
            len(v)
            for v in self.edges.values()
        )//2