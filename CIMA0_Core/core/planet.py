class PlanetEngine:
    """
    Minimal dynamic engine.

    State:

        x
        v
        omega

    """

    def __init__(
        self,
        x=1.0,
        v=0.0,
        omega=1.0,
        dt=0.01
    ):

        self.x = float(x)
        self.v = float(v)
        self.omega = float(omega)
        self.dt = float(dt)


    def step(
        self,
        external_force=0.0
    ):

        acceleration = (
            -self.omega
            *
            self.omega
            *
            self.x
            +
            external_force
        )


        self.v += (
            acceleration
            *
            self.dt
        )


        self.x += (
            self.v
            *
            self.dt
        )


    def sample(self):

        return {
            "x": self.x,
            "v": self.v,
            "omega": self.omega
        }