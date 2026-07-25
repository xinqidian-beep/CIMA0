import numpy as np


class Environment:


    """
    Local world memory.

    No global intelligence.

    Only:
        decay
        local residue
    """


    def __init__(self,n):

        self.field=np.zeros(n)



    def update(self,cell_id,value):

        self.field[cell_id]*=0.999


        self.field[cell_id]+=(
            value*0.001
        )



    def get(self,cell_id):

        return self.field[cell_id]