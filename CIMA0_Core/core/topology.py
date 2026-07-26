import random


class Topology:


    def __init__(
        self,
        size,
        degree=4,
        seed=1
    ):

        self.size=size
        self.degree=degree

        self.neighbors = {

            i:set()

            for i in range(size)

        }


        self._build(seed)



    def _build(self,seed):

        rng=random.Random(seed)


        while True:

            for i in range(self.size):

                self.neighbors[i].clear()


            edges=0


            while edges < self.size*self.degree//2:


                a=rng.randrange(self.size)
                b=rng.randrange(self.size)


                if a==b:
                    continue


                if b in self.neighbors[a]:
                    continue


                if (
                    len(self.neighbors[a])>=self.degree
                    or
                    len(self.neighbors[b])>=self.degree
                ):
                    continue


                self.neighbors[a].add(b)
                self.neighbors[b].add(a)

                edges+=1



            if all(
                len(self.neighbors[i])>0
                for i in range(self.size)
            ):
                break



        self.neighbors={

            k:list(v)

            for k,v in self.neighbors.items()

        }



    def get(self,cid):

        return self.neighbors[cid]