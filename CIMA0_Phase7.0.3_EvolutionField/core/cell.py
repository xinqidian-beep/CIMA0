class Cell:

    """
    动力核心单元

    外部只能提供 perturb
    不允许修改 omega
    不允许修改内部规则
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
        perturb=0.0,
        dt=0.01
    ):

        """
        核心动力

        F = intrinsic + perturb

        perturb只能是外部微扰
        """

        force = (
            -self._omega *
            self._omega *
            self._x
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
            0.5*self._omega*self._omega*self._x*self._x
        )


        return {

            "x":self._x,

            "v":self._v,

            "energy":energy,

            "activity":self.activity,

            "time":self.time

        }