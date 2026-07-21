import numpy as np


class OscillatorOrgan:

    def __init__(self, name, dim=16):

        self.name = name
        self.dim = dim


        # =========================
        # Core oscillator state
        # =========================

        self.state = np.random.randn(dim) * 0.01

        self.velocity = np.zeros(dim)

        self.phase = np.random.random() * np.pi * 2


        self.activity = 0


        # prediction system

        self.prediction = self.state.copy()

        self.prediction_error = 0.0

        self.error = 0.0


        # uncertainty

        self.uncertainty = 0.01


        # =========================
        # Metabolism
        # =========================

        self.fatigue = 0.0

        self.energy = 1.0

        self.energy_max = 1.0


        self.consume_rate = 0.00005

        self.recovery_rate = 0.00003

        self.fatigue_gain = 0.0001

        self.fatigue_decay = 0.99995



        # oscillator parameters

        self.omega = 0.05

        self.damping = 0.001



    # =========================
    # local metabolism
    # =========================

    def metabolic_step(self):

        # activity consumes energy

        if self.activity > 0:

            self.energy -= self.consume_rate

            self.fatigue += self.fatigue_gain



        # natural recovery

        self.energy += (
            self.recovery_rate *
            np.exp(-self.fatigue)
        )


        # fatigue naturally decays

        self.fatigue *= self.fatigue_decay



        # only physical boundary

        self.energy = np.clip(
            self.energy,
            -1.0,
            self.energy_max
        )



    # =========================
    # oscillator evolution
    # =========================

    def step(self):

        old = self.state.copy()


        # local oscillator

        acceleration = (
            -self.omega * self.state
            -self.damping * self.velocity
        )


        self.velocity += acceleration


        self.state += self.velocity



        # prediction

        self.prediction = (
            0.99 * self.prediction
            + 0.01 * self.state
        )


        self.prediction_error = float(
            np.mean(
                np.abs(
                    self.state -
                    self.prediction
                )
            )
        )


        self.error = self.prediction_error



        # activity

        delta = np.mean(
            np.abs(
                self.state-old
            )
        )


        if delta > 0.001:

            self.activity += 1



        # uncertainty

        self.uncertainty = (
            0.99*self.uncertainty
            +
            0.01*self.prediction_error
        )


        # metabolism

        self.metabolic_step()



    # =========================
    # interface for ComputeField
    # =========================

    def snapshot(self):

        return {

            "name": self.name,

            "std": round(
                float(np.std(self.state)),
                5
            ),

            "activity": self.activity,


            "error": round(
                float(self.error),
                5
            ),


            "prediction_error": round(
                float(self.prediction_error),
                5
            ),


            "uncertainty": round(
                float(self.uncertainty),
                5
            ),


            "fatigue": round(
                float(self.fatigue),
                5
            ),


            "energy": round(
                float(self.energy),
                5
            )
        }