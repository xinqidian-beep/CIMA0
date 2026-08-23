import numpy as np


class Planet:

    """
    Pure local dynamics.

    Knows only:

        state
        local interaction
        evolution


    Organ interface:

        receive()
        step()
        snapshot()
    """



    def __init__(
        self,
        size=128
    ):

        self.size = size


        self.state = np.random.randn(
            size,
            size
        ) * 0.01



    def receive(
        self,
        raw
    ):
        """
        Ignore external disturbance.

        Local planet owns
        its own dynamics.
        """

        pass



    def step(
        self
    ):

        old = self.state.copy()


        for x in range(
            1,
            self.size-1
        ):

            for y in range(
                1,
                self.size-1
            ):


                neighbor = (

                    old[x+1,y] +
                    old[x-1,y] +
                    old[x,y+1] +
                    old[x,y-1]

                ) / 4



                self.state[x,y] += (

                    0.05 *
                    (
                        neighbor -
                        old[x,y]
                    )

                )


                self.state[x,y] += (

                    0.001 *
                    np.sin(
                        old[x,y]
                    )

                )



    def snapshot(
        self
    ):

        return self.state.copy()