import numpy as np


class Sampler:
    """
    CIMA0 Adaptive Attention Sampler.


    Responsibility:

        local state field

              |

              v

        priority field

              |

              v

        selected positions



    Input state:

        {
            "age",
            "activity",
            "delta"
        }


    Does NOT know:


        organ

        source

        meaning

        compute

        semantics



    It only selects.
    """



    def __init__(
        self
    ):

        #
        # local selection weights
        #

        self.w_age = 0.25

        self.w_activity = 0.35

        self.w_delta = 0.40



    #
    # calculate selection pressure
    #

    def priority(
        self,
        state
    ):


        if state is None:

            return None



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

            self.w_age
            *
            np.asarray(
                age
            )

            +

            self.w_activity
            *
            np.asarray(
                activity
            )

            +

            self.w_delta
            *
            np.abs(
                np.asarray(
                    delta
                )
            )

        )


        return score



    #
    # select positions
    #

    def select(
        self,
        state,
        budget=1
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



        if count == 0:

            return np.array(
                [],
                dtype=np.int64
            )



        budget = int(
            budget
        )


        if budget <= 0:

            return np.array(
                [],
                dtype=np.int64
            )



        #
        # all selected
        #

        if budget >= count:

            return np.arange(
                count,
                dtype=np.int64
            )



        #
        # highest pressure
        #

        index = np.argpartition(
            flat,
            -budget
        )[-budget:]



        return index.astype(
            np.int64
        )