import numpy as np


class Observer:


    def measure(self, network):

        phases = np.array(
            [
                node.phase()
                for node in network.nodes
            ]
        )


        energy = np.array(
            [
                node.energy
                for node in network.nodes
            ]
        )


        return {

            "phase_std":
                float(np.std(phases)),

            "mean_energy":
                float(np.mean(energy)),

            "energy_std":
                float(np.std(energy))
        }