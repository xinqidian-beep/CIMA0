class AdaptiveTopology:


    def __init__(
        self,
        n,
        initial_edges
    ):

        self.weights={}

        for e in initial_edges:

            self.weights[e]=0.01



    def weight(
        self,
        a,
        b
    ):

        if a>b:
            a,b=b,a

        return self.weights.get(
            (a,b),
            0.01
        )



    def update(
        self,
        states
    ):

        # Phase7.2:
        # topology only observes
        pass