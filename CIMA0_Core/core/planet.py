class KinEngine:

    def __init__(
        self,
        kin_x=1.0,
        kin_v=0.0,
        kin_omega=1.0,
        kin_dt=0.01
    ):

        self.kin_x = kin_x
        self.kin_v = kin_v
        self.kin_omega = kin_omega
        self.kin_dt = kin_dt


        self.kin_ephemeral_force = 0.0



    def receive_kin_ephemeral_force(
        self,
        force
    ):

        self.kin_ephemeral_force = force



    def step_kin_dynamics(
        self
    ):

        acceleration = (
            -self.kin_omega**2
            *
            self.kin_x
            +
            self.kin_ephemeral_force
        )


        self.kin_v += (
            acceleration
            *
            self.kin_dt
        )


        self.kin_x += (
            self.kin_v
            *
            self.kin_dt
        )


        self.kin_ephemeral_force = 0.0