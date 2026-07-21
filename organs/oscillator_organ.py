import numpy as np



class OscillatorOrgan:


    """
    Minimal autonomous organism.

    No:
        reward
        target
        supervision
        external control


    Internal closure:

        energy
          |
          v
    nonlinear oscillator
          |
          v
       activity
          |
          v
     metabolism


    External input in future:
        only perturbation
        never state replacement

    """



    def __init__(
        self,
        name,
        dim=16
    ):


        self.name=name

        self.dim=dim



        # --------------------
        # local state
        # --------------------

        self.state=np.random.randn(dim)*0.1

        self.velocity=np.random.randn(dim)*0.01


        self.phase=np.random.random()*np.pi*2
        self.position = np.random.randn(3)


        # --------------------
        # internal prediction
        # --------------------

        self.prediction=self.state.copy()

        self.prediction_error=0.0

        self.uncertainty=0.05



        self.error=0.0



        # --------------------
        # metabolism
        # --------------------

        self.energy=1.0

        self.energy_max=1.0


        self.fatigue=0.0



        self.activity=0



        # --------------------
        # internal physics
        # --------------------

        self.omega=0.05


        # nonlinear strength
        self.mu=0.8


        self.damping=0.02



        self.dt=0.05



    # =================================
    # internal metabolism
    # =================================


    def metabolic_step(self):


        activity_cost = (
            np.mean(
                np.abs(self.velocity)
            )
            *
            0.0005
        )


        self.energy -= activity_cost



        # internal recovery
        # not a goal
        # just metabolism

        self.energy += (
            0.0003
            *
            (1.0-self.energy)
        )


        self.energy=np.clip(
            self.energy,
            0.0,
            self.energy_max
        )



        self.fatigue += (
            activity_cost
        )


        self.fatigue*=0.9999



    # =================================
    # autonomous dynamics
    # =================================


    def step(self):


        old=self.state.copy()



        # ---------------------------------
        # Van der Pol like local dynamics
        # ---------------------------------

        amplitude=np.mean(
            self.state*self.state
        )


        nonlinear = (

            self.mu
            *
            (
                1.0-amplitude
            )
            *
            self.velocity

        )



        acceleration=(

            nonlinear

            -

            self.omega*self.omega*self.state

            -

            self.damping*self.velocity

        )



        self.velocity += (
            acceleration
            *
            self.dt
        )


        self.state += (
            self.velocity
            *
            self.dt
        )

        

        # -------------------------------
        # prediction
        # -------------------------------

        self.prediction=(

            0.98*self.prediction

            +

            0.02*self.state

        )


        self.prediction_error=float(

            np.mean(

                np.abs(
                    self.state
                    -
                    self.prediction
                )

            )

        )


        self.error=self.prediction_error



        self.uncertainty=(

            0.99*self.uncertainty

            +

            0.01*self.prediction_error

        )



        # -------------------------------
        # activity
        # -------------------------------

        delta=np.mean(
            np.abs(
                self.state-old
            )
        )


        if delta>1e-5:

            self.activity+=1



        self.metabolic_step()

        self.position += (
            np.random.randn(3)
            *
            0.0001
        )

    def snapshot(self):
        

        return {

            "name":self.name,
            "position":
            [
                round(float(x),3)
                for x in self.position
            ],

            "std":round(
                float(np.std(self.state)),
                5
            ),


            "activity":self.activity,


            "prediction_error":round(
                self.prediction_error,
                5
            ),


            "uncertainty":round(
                self.uncertainty,
                5
            ),


            "energy":round(
                self.energy,
                5
            ),


            "fatigue":round(
                self.fatigue,
                5
            )

        }