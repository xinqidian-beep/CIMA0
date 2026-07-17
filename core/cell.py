import numpy as np



class Cell:


    def __init__(self,id,dim=512):

        self.id=id

        self.state=np.random.normal(
            0,
            0.1,
            dim
        )

        self.energy=1.0

        self.activity=0



    def stimulate(
        self,
        vector,
        strength
    ):

        self.state += (
            vector
            *
            strength
            *
            0.05
        )

        self.energy += strength*0.01

        self.activity+=1



    def step(self):

        # 自然衰减

        self.state*=0.999

        self.energy*=0.999



    def similarity(self,vector):

        a=self.state
        b=vector


        return (
            np.dot(a,b)
            /
            (
            np.linalg.norm(a)
            *
            np.linalg.norm(b)
            +
            1e-8
            )
        )