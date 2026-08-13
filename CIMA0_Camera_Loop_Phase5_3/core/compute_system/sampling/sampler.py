import numpy as np



class Sampler:
    """
    Universal sampling rule.

    Input:

        delta
        age
        activity
        budget


    Output:

        selected indices


    Knows:

        numerical sampling rule
        internal weights


    Does NOT know:

        camera
        cloud
        clip
        planet
        meaning


    Dynamics:

        w_delta
        w_age
        w_activity

    are internal slow variables.

    They can evolve through reward feedback.
    """



    def __init__(
        self,
        budget_ratio=0.1,

        w_delta=1.0,
        w_age=0.01,
        w_activity=0.1
    ):

        self.budget_ratio = budget_ratio


        #
        # internal sampling state
        #

        self.w_delta = float(
            w_delta
        )

        self.w_age = float(
            w_age
        )

        self.w_activity = float(
            w_activity
        )



    def _score(
        self,
        delta,
        age,
        activity
    ):

        return (

            delta * self.w_delta

            +

            age * self.w_age

            +

            activity * self.w_activity

        )



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



        score = self._score(
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



    def update(
        self,
        reward,
        delta,
        age,
        activity,

        learning_rate=0.001,
        decay=0.0001
    ):
        """
        Internal weight evolution.

        Reward source is external.

        Sampler does not know:

            where reward comes from

        It only updates its own state.
        """



        delta = np.asarray(
            delta,
            dtype=np.float32
        )

        age = np.asarray(
            age,
            dtype=np.float32
        )

        activity = np.asarray(
            activity,
            dtype=np.float32
        )



        #
        # natural decay
        #

        self.w_delta *= (
            1.0 - decay
        )

        self.w_age *= (
            1.0 - decay
        )

        self.w_activity *= (
            1.0 - decay
        )



        #
        # cross coupling dynamics
        #
        # delta weight influenced by age
        #

        self.w_delta += (

            learning_rate
            *
            reward
            *
            float(
                np.mean(age)
            )

        )



        #
        # age weight influenced by activity
        #

        self.w_age += (

            learning_rate
            *
            reward
            *
            float(
                np.mean(activity)
            )

        )



        #
        # activity weight influenced by delta
        #

        self.w_activity += (

            learning_rate
            *
            reward
            *
            float(
                np.mean(delta)
            )

        )



    def state(
        self
    ):
        """
        Expose sampler internal state.
        """

        return {

            "w_delta":
                self.w_delta,

            "w_age":
                self.w_age,

            "w_activity":
                self.w_activity

        }