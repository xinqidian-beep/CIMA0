class Scheduler:


    def __init__(
        self,
        n,
        budget=100
    ):

        self.n=n
        self.budget=budget

        self.queue=list(
            range(n)
        )


    def tick(self):

        active=[]


        for _ in range(self.budget):

            if not self.queue:

                self.queue=list(
                    range(self.n)
                )


            active.append(
                self.queue.pop(0)
            )


        return active