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



    def acceleration(
        self,
        force
    ):

        return (

            -self.omega *
            self.omega *
            self.x

            +

            force

        )



    def step(
        self,
        force
    ):


        dt=self.dt


        # 当前加速度

        a0=self.acceleration(
            force
        )


        # 半步速度

        self.v += (

            0.5 *
            a0 *
            dt

        )


        # 位置更新

        self.x += (

            self.v *
            dt

        )


        # 新位置内部力

        a1=self.acceleration(
            force
        )


        # 再半步速度

        self.v += (

            0.5 *
            a1 *
            dt

        )