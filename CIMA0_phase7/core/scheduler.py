import heapq


class DualTimeScheduler:


    def __init__(
        self,
        cells
    ):

        self.cells = cells

        self.fast = []

        self.medium = []

        self.slow = []



    def activity(
        self,
        cell
    ):

        return (
            abs(cell.x)
            +
            abs(cell.v)
            +
            0.5 * abs(cell.g)
        )



    def update(self):

        self.fast=[]
        self.medium=[]
        self.slow=[]


        values=[]


        for i,c in enumerate(self.cells):

            values.append(
                (
                    self.activity(c),
                    i
                )
            )


        values.sort(
            reverse=True
        )


        if len(values)==0:
            return



        high = values[0][0]

        low = values[-1][0]


        span = high-low+1e-9



        for score,i in values:


            norm=(score-low)/span



            if norm>0.66:

                self.fast.append(i)


            elif norm>0.25:

                self.medium.append(i)


            else:

                self.slow.append(i)



    def fast_ids(self):

        return self.fast



    def medium_ids(self):

        return self.medium



    def slow_ids(self):

        return self.slow



    def stats(self):

        return {

            "fast":
                len(self.fast),

            "medium":
                len(self.medium),

            "slow":
                len(self.slow)

        }