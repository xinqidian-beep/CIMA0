import numpy as np

from core.cell import Cell



class World:

    """
    World is only a container.

    It does NOT calculate global meaning.

    It only provides existence.
    """


    def __init__(self, n=4096):

        self.time = 0

        self.cells = [

            Cell(
                cid=i,
                seed=i
            )

            for i in range(n)

        ]


    def step(self):

        """
        Each individual evolves.

        No global coupling.
        """

        for c in self.cells:


            # rare environmental noise
            # not intelligence
            perturb = np.random.normal(
                0,
                0.001
            )


            c.step(
                perturb
            )


        self.time += 1



    def observe_local(self):

        """
        Observer only takes a sample.

        No god view.
        """

        sample = np.random.choice(
            self.cells,
            size=32,
            replace=False
        )


        xs = np.array(
            [
                c.x
                for c in sample
            ]
        )


        energies = np.array(
            [
                c.state()["energy"]
                for c in sample
            ]
        )


        return {

            "sample":
                len(sample),

            "x_std":
                float(
                    np.std(xs)
                ),

            "energy_mean":
                float(
                    np.mean(energies)
                )

        }




def main():


    print(
        "=== CIMA0 Phase8.0 Minimal_world_Loop ==="
    )


    world = World(
        n=4096
    )


    TEST_TIME = 10_000_000


    CHECK = 100_000



    for step in range(TEST_TIME):


        world.step()



        if step % CHECK == 0:


            obs = world.observe_local()


            # only validation
            alive = sum(

                1
                for c in world.cells

                if abs(c.x)<20

            )


            print(
                {

                    "time":
                        world.time,

                    "alive":
                        alive,

                    "observer":
                        obs

                }
            )



    print(
        "finished"
    )




if __name__ == "__main__":

    main()