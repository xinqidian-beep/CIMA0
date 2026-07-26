import numpy as np


class CloudMatrix:


    def __init__(self,size):

        self.size=size

        self.field=np.full(
            size,
            np.nan
        )


    def clear(self):

        self.field[:] = np.nan



    def deposit_random(
        self,
        count=4,
        strength=1.0
    ):


        for _ in range(count):

            idx=np.random.randint(
                0,
                self.size
            )


            value=np.random.uniform(
                -strength,
                strength
            )


            self.field[idx]=value



    def contact(self,cid):

        value=self.field[cid]


        if np.isnan(value):

            return None


        return float(value)



    def decay(self,rate=0.995):

        mask=~np.isnan(self.field)


        self.field[mask]*=rate


        dead=(
            np.abs(self.field)<1e-4
        )


        self.field[dead]=np.nan