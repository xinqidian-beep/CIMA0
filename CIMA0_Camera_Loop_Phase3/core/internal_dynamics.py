from archive.planet import Planet
from core.clip_region import ClipRegion



class InternalDynamics:
    """
    Internal Dynamics composition layer.


    Contains local dynamic regions:

        Planet
            |
            state
            local relation
            evolution


        ClipRegion
            |
            visual local state
            local relation
            evolution



    This layer does not:

        interpret
        classify
        control
        select


    It only allows local dynamics
    to coexist.
    """



    def __init__(
        self,
        clip_weight,
        planet_size=128
    ):


        #
        # pure internal dynamics
        #

        self.planet = Planet(
            size=planet_size
        )



        #
        # local visual basin
        #

        self.clip = ClipRegion(
            clip_weight
        )





    def update(
        self,
        external_state=None
    ):
        """
        One internal evolution step.


        External information:

            only enters local state evolution.


        Does not modify:

            dynamics rule
        """



        #
        # Planet original dynamics
        #
        # no input
        # no modification
        #

        self.planet.step()



        #
        # Clip local dynamics
        #

        if external_state is not None:

            self.clip.update(
                external_state
            )






    def snapshot(self):
        """
        Raw internal snapshot.


        Observer reads this.

        No semantic interpretation.
        """

        return {


            "planet":

                {

                    "state":

                        self.planet.state.copy(),

                    "mean":

                        float(
                            self.planet.state.mean()
                        ),

                    "std":

                        float(
                            self.planet.state.std()
                        )

                },



            "clip":

                self.clip.state()

        }
        
    def observation_state(self):
        """
        Provide raw local state for Observer.

        No interpretation.
        """

        return self.planet.state.copy()    