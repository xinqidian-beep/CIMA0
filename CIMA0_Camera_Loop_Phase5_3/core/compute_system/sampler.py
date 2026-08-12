import numpy as np

from .raise_score import raise_score



class Sampler:


    def __init__(
        self,
        budget_ratio=0.1
    ):

        self.budget_ratio = budget_ratio



    def select(
        self,
        delta,
        age,
        activity=None,
        budget=None
    ):


        delta = np.asarray(
            delta,
            dtype=np.float32
        )


        age = np.asarray(
            age,
            dtype=np.float32
        )


        if activity is None:

            activity = np.zeros_like(
                delta
            )

        else:

            activity = np.asarray(
                activity,
                dtype=np.float32
            )



        if not (
            len(delta)
            ==
            len(age)
            ==
            len(activity)
        ):

            raise ValueError(
                "Sampler input size mismatch"
            )



        score = raise_score(
            delta,
            age,
            activity
        )


        count = len(score)



        if budget is None:

            budget = int(
                count *
                self.budget_ratio
            )



        budget = max(
            1,
            min(
                count,
                int(budget)
            )
        )



        if budget >= count:

            return np.arange(
                count
            )



        return np.argpartition(
            score,
            -budget
        )[-budget:]