class Cell:
    """
    最小动力单元

    自己负责存在。
    外部只能提供 perturb。

    omega 不可修改。
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

        self._x = x
        self._v = v
        self._omega = omega

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



    def step(
        self,
        local_force=0.0,
        perturb=0.0,
        dt=0.01
    ):

        """
        动力核心

        内生振荡
        +
        局部耦合
        +
        微弱扰动
        """

        force = (

            -self._omega *
            self._omega *
            self._x

            +

            local_force

            +

            perturb
        )


        self._v += force * dt

        self._x += self._v * dt


        self.time += 1


        self.activity = (
            abs(self._x)
            +
            abs(self._v)
        )



    def observe(self):

        energy = (

            0.5*self._v*self._v

            +

            0.5*
            self._omega*
            self._omega*
            self._x*self._x

        )


        return {
            "x":self._x,
            "v":self._v,
            "energy":energy,
            "activity":self.activity
        }