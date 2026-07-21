import random


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

        self.clock=0



    def tick(self):

        self.clock+=1


        active=[]


        for _ in range(
            self.budget
        ):

            if not self.queue:

                self.queue=list(
                    range(self.n)
                )


            idx=self.queue.pop(0)

            active.append(idx)


        return active