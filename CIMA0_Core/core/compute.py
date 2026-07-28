class ComputeSystem:
    """
    Local computation system.

    Responsibility:

        allocate calculation effort
        refine current observation


    Does not:

        control dynamics
        store world model
        understand meaning
        manage objects

    """


    def __init__(
        self,
        base_steps=1,
        max_steps=100
    ):

        self.base_steps = base_steps

        self.max_steps = max_steps



    def allocate(
        self,
        raised
    ):

        """
        Decide current calculation amount.

        Only based on observation signal.

        No global knowledge.
        """


        if raised:

            return self.max_steps


        return self.base_steps



    def compute(
        self,
        state,
        steps
    ):

        """
        Refine current local calculation.

        State meaning is unknown here.

        """

        result = state


        for _ in range(steps):

            result = self._local_process(
                result
            )


        return result



    def _local_process(
        self,
        value
    ):

        """
        Placeholder local calculation.

        No semantic processing.
        """

        return value