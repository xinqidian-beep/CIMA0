
class Cell:
    """
    Minimal transient internal state slot.

    Responsibility:

        hold one internal state
        expose local change
        support natural release

    Does NOT:

        interpret
        select
        attend
        decide
        map external coordinates
        define semantic identity
    """

    def __init__(self):

        #
        # current internal state
        #

        self.value = None


        #
        # previous state
        #
        # Used only to measure local change.
        #

        self.previous = None


        #
        # local change magnitude
        #

        self.delta = 0.0


        #
        # age of current state
        #

        self.age = 0


        #
        # current activity
        #

        self.activity = 0.0


    @property
    def empty(self):

        return self.value is None


    def occupy(
        self,
        value
    ):

        value = float(value)


        #
        # preserve previous state
        #

        self.previous = self.value


        #
        # install new state
        #

        self.value = value


        #
        # new state
        #

        self.age = 0


        #
        # local change
        #

        if self.previous is None:

            self.delta = abs(
                value
            )

        else:

            self.delta = abs(
                value
                -
                self.previous
            )


        #
        # activity follows actual change
        #

        self.activity = self.delta


    def release(self):

        #
        # state disappears
        #

        self.value = None


        #
        # previous state is no longer
        # a live comparison target
        #

        self.previous = None


        #
        # reset transient quantities
        #

        self.delta = 0.0

        self.age = 0

        self.activity = 0.0