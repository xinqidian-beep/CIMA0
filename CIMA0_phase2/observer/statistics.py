import numpy as np



def snapshot(network):


    energy=np.array(
        [
            n.energy
            for n in network.nodes
        ]
    )


    return {

        "mean_energy":
            float(np.mean(energy)),

        "energy_std":
            float(np.std(energy)),

        "max_energy":
            float(np.max(energy))

    }