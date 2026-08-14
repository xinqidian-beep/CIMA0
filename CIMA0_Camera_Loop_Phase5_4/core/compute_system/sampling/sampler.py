import numpy as np


class Sampler:
    """
    CIMA0 Adaptive Sampler.


    Responsibility:


        state field

            |

            v

        adaptive priority

            |

            v

        selected positions



    State:


        age

        activity

        delta

        weight



    Does NOT know:


        cloud meaning

        planet meaning

        CLIP meaning

        field semantics

    """



    def __init__(
        self,
        minimum=0
    ):

        self.minimum = minimum


        #
        # adaptive coefficients
        #

        self.w_age = 0.25
        self.w_activity = 0.35
        self.w_delta = 0.40



    def priority(
        self,
        state
    ):
        """
        Calculate selection pressure.


        state:

        {
            age,
            activity,
            delta
        }

        """


        age = state.get(
            "age"
        )


        activity = state.get(
            "activity"
        )


        delta = state.get(
            "delta"
        )


        if (
            age is None
            or
            activity is None
            or
            delta is None
        ):

            return None



        score = (

            self.w_age * age

            +

            self.w_activity * activity

            +

            self.w_delta * np.abs(delta)

        )


        return score



    def select(
        self,
        state,
        budget
    ):


        score = self.priority(
            state
        )


        if score is None:

            return np.array(
                [],
                dtype=np.int64
            )



        flat = score.reshape(
            -1
        )


        count = flat.size


        budget = int(
            budget
        )


        if budget >= count:

            return np.arange(
                count
            )



        indices = np.argpartition(

            flat,

            -budget

        )[-budget:]



        return indices



    def update(
        self,
        reward,
        state
    ):
        """
        Adaptive weight evolution.


        """



        age = np.mean(
            state["age"]
        )


        activity = np.mean(
            state["activity"]
        )


        delta = np.mean(
            np.abs(
                state["delta"]
            )
        )



        self.w_delta += (

            reward *

            (
                age
                +
                activity
            )

            *

            0.001

        )


        self.w_age += (

            reward *

            (
                delta
                +
                activity
            )

            *

            0.001

        )


        self.w_activity += (

            reward *

            (
                delta
                +
                age
            )

            *

            0.001

        )



        #
        # normalize
        #

        total = (

            self.w_age

            +

            self.w_activity

            +

            self.w_delta

        )


        if total > 0:

            self.w_age /= total

            self.w_activity /= total

            self.w_delta /= total
