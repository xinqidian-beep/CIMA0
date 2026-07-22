import numpy as np


class AdaptiveTopology:

    def __init__(
        self,
        n,
        initial_edges,
        max_edges=None,
        seed=42
    ):

        np.random.seed(seed)

        self.n = n

        self.edges = set(
            tuple(sorted(e))
            for e in initial_edges
        )

        self.max_edges = (
            max_edges
            if max_edges
            else n * 6
        )

        self.weights = {}

        for e in self.edges:
            self.weights[e] = 1.0



    def weight(
        self,
        a,
        b
    ):

        key = tuple(sorted((a,b)))

        return self.weights.get(
            key,
            0.0
        )



    def update(
        self,
        states
    ):

        """
        Local topology evolution.

        states:
        [
            [x,v,g,energy],
            ...
        ]

        no target
        no reward
        """

        remove = []

        # ---- edge weakening ----

        for e,w in list(self.weights.items()):

            a,b=e

            sa=states[a]
            sb=states[b]


            distance=np.linalg.norm(
                sa-sb
            )


            if distance > 3.0:

                self.weights[e] *= 0.995


            else:

                self.weights[e] *= 1.001



            if self.weights[e] < 0.2:

                remove.append(e)



        for e in remove:

            self.edges.remove(e)

            del self.weights[e]



        # ---- local reconnection ----

        while len(self.edges)<self.max_edges:

            a=np.random.randint(
                0,self.n
            )

            b=np.random.randint(
                0,self.n
            )


            if a==b:
                continue


            e=tuple(sorted((a,b)))


            if e not in self.edges:

                self.edges.add(e)

                self.weights[e]=0.5

                break



    def edge_list(self):

        return list(self.edges)



    def stats(self):

        degree=np.zeros(
            self.n
        )

        for a,b in self.edges:

            degree[a]+=1
            degree[b]+=1


        return {

            "edges":
                len(self.edges),

            "degree_mean":
                float(
                    degree.mean()
                ),

            "degree_std":
                float(
                    degree.std()
                )

        }