import numpy as np


class Cell:

    """
    Autonomous local entity.

    Only knows:
        own state
        local field

    Does not know:
        other cells
        universe
        global state
    """

    def __init__(self, cid):

        self.cid = cid

        # Lorenz state
        self.state = np.random.uniform(
            -1,
            1,
            3
        )

        self.sigma = 10.0
        self.rho = 28.0
        self.beta = 8.0 / 3.0

        self.dt = 0.005


    def step(self, local_field):

        x,y,z = self.state


        dx = (
            self.sigma *
            (y-x)
        )

        dy = (
            x *
            (self.rho-z)
            -
            y
        )

        dz = (
            x*y
            -
            self.beta*z
        )


        # local environment only
        perturb = local_field * 0.001


        self.state += np.array(
            [
                dx,
                dy,
                dz
            ]
        ) * self.dt


        self.state += perturb



        return self.state.copy()



    def activity(self):

        return float(
            np.linalg.norm(
                self.state
            )
        )