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
        candidates,
        budget=1
    ):


        scores=[]


        for c in candidates:


            state=self.priority(c)

            if score is None:

                score=0


            scores=float(
                np.mean(score)
            )



        scores.append(
            scores
        )



        if scores.size==0:

            return np.array(
                [],
                dtype=np.int64
            )


        index=np.argpartition(
            scores,
            -budget
        )[-budget:]


        return index