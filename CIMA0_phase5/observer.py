import numpy as np


class Observer:


    def record(
        self,
        network,
        scheduler,
        step
    ):

        x=np.array(
            [
                c.x
                for c in network.cells
            ]
        )


        v=np.array(
            [
                c.v
                for c in network.cells
            ]
        )


        energy=np.array(
            [
                c.energy
                for c in network.cells
            ]
        )


        phase=np.arctan2(
            v,
            x
        )


        return {

            "step": step,

            "mean_energy":
                float(
                    energy.mean()
                ),

            "energy_std":
                float(
                    energy.std()
                ),

            "phase_std":
                float(
                    phase.std()
                ),

            "active_count":
                len(
                    getattr(
                        scheduler,
                        "active_ids",
                        []
                    )
                )
        }