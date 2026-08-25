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
        # selection weights
        #

        self.w_age = 0.25

        self.w_activity = 0.35

        self.w_delta = 0.40
        
        self.memory = None

    def attach_memory(
        self,
        memory
    ):

        self.memory = memory

    #
    # calculate priority
    #

    def priority(
        self,
        state
    ):
        
        memory_pressure = None


        if self.memory is not None:

            memory_pressure = (
                self.memory.pressure()
            )
        print(
            "MEMORY PRESSURE:",
            memory_pressure
        )
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
            or activity is None
            or delta is None
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

    def adapt_weights(
        self
    ):

        if self.memory is None:
            return


        pressure = self.memory.pressure()


        if pressure > 0.8:

            self.w_delta *= 0.99

            self.w_activity *= 1.01

    #
    # select top priority
    #

    def select(
        self,
        candidates,
        budget=1
    ):


        if candidates is None:

            return np.array(
                [],
                dtype=np.int64
            )


        if len(candidates)==0:

            return np.array(
                [],
                dtype=np.int64
            )



        scores=[]



        for candidate in candidates:


            score = self.priority(
                candidate
            )


            if score is None:

                score_value = 0.0


            else:

                score_value = float(
                    np.mean(
                        score
                    )
                )


            scores.append(
                score_value
            )



        scores=np.asarray(
            scores,
            dtype=np.float32
        )



        budget=min(
            int(budget),
            len(scores)
        )



        if budget <= 0:

            return np.array(
                [],
                dtype=np.int64
            )



        index=np.argpartition(

            scores,

            -budget

        )[-budget:]



        #
        # highest priority first
        #

        index=index[
            np.argsort(
                scores[index]
            )[::-1]
        ]



        return index
        
