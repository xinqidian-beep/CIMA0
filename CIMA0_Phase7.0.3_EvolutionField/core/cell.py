import math


class Cell:

    def __init__(
        self,
        x,
        v,
        omega
    ):

        self.x = x
        self.v = v

        # 固定动力参数
        self.omega = omega


    def step(
        self,
        force=0.0,
        perturb=0.0,
        dt=0.01
    ):

        """
        最小动力核心

        外界只能通过:
            force
            perturb

        不能改变:
            omega

        """

        acceleration = (

            -self.omega *
            self.omega *
            self.x

            +

            force

            +

            perturb

        )


        self.v += acceleration * dt

        self.x += self.v * dt



    def energy(self):

        return (

            0.5 *
            self.v *
            self.v

            +

            0.5 *
            self.omega *
            self.omega *
            self.x *
            self.x

        )


    def observe(self):

        return {

            "x": self.x,

            "v": self.v,

            "energy": self.energy()

        }