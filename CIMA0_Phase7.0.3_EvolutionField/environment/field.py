import numpy as np


class EvolutionField:


    def __init__(self,n):

        self.field=np.zeros(n)



    def update(
        self,
        region,
        state
    ):


        if len(region)==0:
            return


        for i in region:

            self.field[i] *= 0.99999


            # 非目标，只留下历史痕迹

            self.field[i]+=(
                state[i]*0.000001
            )



    def get(self):

        return self.field.copy()