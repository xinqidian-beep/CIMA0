class Observer:
    """
    Local observer.

    Only:

        receive local signal
        compare with own history
        output raised


    Does not:

        control dynamics
        modify state
        know global structure
    """


    def __init__(
        self,
        decay=0.99
    ):

        self.baseline = None

        self.decay = decay



    def observe(
        self,
        value
    ):

        """
        Observe one local value.

        No global scan.
        No semantic understanding.
        """

        value = float(value)


        # initialize history

        if self.baseline is None:

            self.baseline = value


        else:

            self.baseline = (
                self.decay * self.baseline
                +
                (1.0 - self.decay) * value
            )


        deviation = abs(
            value - self.baseline
        )


        raised = (
            deviation
            >
            self.observed_threshold()
        )


        return {

            "raised": raised,

            "activity": value,

            "baseline": self.baseline,

            "deviation": deviation

        }



    def observed_threshold(
        self
    ):

        """
        Local adaptive threshold.

        Relative to own history.

        No global constant.
        """

        if self.baseline is None:

            return 0.0


        return (
            abs(self.baseline)
            *
            0.5
            +
            1e-9
        )