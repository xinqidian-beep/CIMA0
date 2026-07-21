import numpy as np

from organs.oscillator_organ import OscillatorOrgan



np.random.seed(42)



class CoupledSystem:


    def __init__(
        self,
        coupling=0.001
    ):

        self.a = OscillatorOrgan(
            "A",
            16
        )

        self.b = OscillatorOrgan(
            "B",
            16
        )


        self.coupling = coupling



    def step(self):


        # -------------------------
        # local interaction
        # -------------------------

        diff = (
            self.b.state
            -
            self.a.state
        )


        force_a = (
            self.coupling
            *
            diff
        )


        force_b = (
            -self.coupling
            *
            diff
        )



        # only perturb velocity

        self.a.velocity += force_a

        self.b.velocity += force_b



        # autonomous evolution

        self.a.step()

        self.b.step()



    def snapshot(self):


        phase_distance = np.mean(
            np.abs(
                self.a.state
                -
                self.b.state
            )
        )


        return {

            "A":self.a.snapshot(),

            "B":self.b.snapshot(),

            "relation":
            round(
                float(phase_distance),
                5
            )
        }




system = CoupledSystem(
    coupling=0.001
)



print("INITIAL")


print(
    system.snapshot()
)



for step in range(200000):


    system.step()



    if step % 20000 ==0:

        print(
            step,
            system.snapshot()
        )