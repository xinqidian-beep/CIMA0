import numpy as np



class CloudField:


    def __init__(
        self,
        n,
        strength=0.02,
        radius=8,
        seed=None
    ):


        self.n=n

        self.strength=strength

        self.radius=radius


        self.rng=np.random.default_rng(
            seed
        )


        self.field=np.zeros(
            n
        )



    def evolve(self):


        new=np.zeros(
            self.n
        )


        for i in range(self.n):


            left=max(
                0,
                i-self.radius
            )


            right=min(
                self.n,
                i+self.radius
            )


            local=self.field[
                left:right
            ]


            if len(local)>0:

                background=np.mean(
                    local
                )

            else:

                background=0



            noise=self.rng.normal(
                0,
                self.strength
            )


            # 空位

            if self.rng.random()<0.1:

                noise=0



            new[i]=(
                0.95*background
                +
                noise
            )



        self.field=new



    def sample(
        self,
        i
    ):

        return self.field[i]