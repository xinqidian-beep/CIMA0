import numpy as np


class ComputeScheduler:


    def __init__(
        self,
        organs,
        active_slots=8
    ):

        self.organs = organs

        self.active_slots = active_slots

        self.time = 0



    def rank(self):

        scores=[]

        for i,o in enumerate(self.organs):

            score = (
                np.std(o.state)
                +
                abs(np.mean(o.state))
            )

            scores.append(
                (score,i)
            )


        scores.sort(
            reverse=True
        )

        return [
            i
            for _,i in scores
        ]



    def step(self):


        self.time += 1


        ranking = self.rank()


        active = ranking[
            :self.active_slots
        ]


        for i,o in enumerate(self.organs):


            if i in active:


                # 补齐等待时间

                gap = (
                    self.time
                    -
                    o.last_compute_time
                )


                o.fast_forward(
                    gap
                )


                # 高精度计算

                o.receive(
                    np.concatenate(
                        [
                            x.emit()
                            for x in self.organs
                        ]
                    )
                )


                o.step()


                o.last_compute_time = (
                    self.time
                )


            else:

                # 不计算

                pass