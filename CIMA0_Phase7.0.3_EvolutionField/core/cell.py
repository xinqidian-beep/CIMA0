class Cell:
    """
    CIMA0 动力核心单元

    内部:
        harmonic oscillator

    外部:
        local_force
        perturb

    外部不能修改:
        omega
    """

    __slots__ = (
        "_x",
        "_v",
        "_omega",
        "time",
        "activity"
    )


    def __init__(
        self,
        x,
        v,
        omega
    ):

        self._x = float(x)
        self._v = float(v)
        self._omega = float(omega)

        self.time = 0

        self.activity = 0.0



    @property
    def x(self):

        return self._x



    @property
    def v(self):

        return self._v



    @property
    def omega(self):

        return self._omega



    def acceleration(
        self,
        force
    ):

        return force



    def step(
        self,
        local_force=0.0,
        perturb=0.0,
        dt=0.01
    ):


        """
        Velocity Verlet

        不改变动力规则
        只改变积分方式
        """


        # 当前力

        force = (

            -self._omega *
            self._omega *
            self._x

            +

            local_force

            +

            perturb

        )


        # 半步位置更新

        self._x += (

            self._v * dt

            +

            0.5 *
            force *
            dt *
            dt

        )


        # 新位置后的新力

        new_force = (

            -self._omega *
            self._omega *
            self._x

            +

            local_force

            +

            perturb

        )


        # 速度更新

        self._v += (

            0.5 *
            (force + new_force)
            *
            dt

        )


        self.time += 1


        self.activity = (

            abs(self._x)

            +

            abs(self._v)

        )



    def energy(self):

        return (

            0.5 *
            self._v *
            self._v

            +

            0.5 *
            self._omega *
            self._omega *
            self._x *
            self._x

        )



    def observe(self):

        return {

            "x":
            self._x,

            "v":
            self._v,

            "energy":
            self.energy(),

            "activity":
            self.activity,

            "time":
            self.time

        }