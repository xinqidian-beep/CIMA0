import numpy as np



class Sampler:
    """
    CIMA0 Universal Sampler.


    Input:


        score field

        budget



    Output:


        selected indices



    Knows only:


        numerical priority



    Does NOT know:


        field meaning

        data source

        semantics

        update rule

    """



    def __init__(
        self,
        minimum=0
    ):

        self.minimum = minimum



    def select(
        self,
        score,
        budget
    ):
        """
        Select high priority locations.


        score:

            ndarray



        budget:

            maximum selected count

        """


        if score is None:

            return np.array(
                [],
                dtype=np.int64
            )



        if not isinstance(
            score,
            np.ndarray
        ):

            return np.array(
                [],
                dtype=np.int64
            )



        flat = np.abs(
            score.reshape(-1)
        )



        count = flat.size



        if budget is None:

            budget = count



        budget = int(
            budget
        )


        if budget <= 0:

            return np.array(
                [],
                dtype=np.int64
            )



        if budget >= count:

            return np.arange(
                count,
                dtype=np.int64
            )



        #
        # highest response first
        #

        indices = np.argpartition(

            flat,

            -budget

        )[-budget:]



        #
        # optional stable ordering
        #

        indices = indices[
            np.argsort(
                flat[indices]
            )[::-1]
        ]



        return indices



    def select_mask(
        self,
        score,
        budget
    ):
        """
        Return field shaped mask.
        """

        selected = self.select(
            score,
            budget
        )


        mask = np.zeros(

            score.size,

            dtype=bool

        )


        mask[selected] = True



        return mask.reshape(
            score.shape
        )