class Cell:


    def __init__(
        self,
        x,
        v,
        omega,
        dt
    ):

        self.x = x
        self.v = v

        self.omega = omega

        self.dt = dt



    def step(
        self,
        force
    ):

        acceleration = (

            -self.omega *
            self.omega *
            self.x

            +

            force
        )


        self.v += (
            acceleration *
            self.dt
        )


        self.x += (
            self.v *
            self.dt
        )