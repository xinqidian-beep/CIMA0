class LocalInteraction:


    def __init__(
        self,
        coupling=0.02
    ):

        self.coupling=coupling



    def force(
        self,
        cell,
        neighbors
    ):


        total=0


        for n in neighbors:

            total += (
                n.x-cell.x
            )


        return (
            self.coupling*
            total
        )