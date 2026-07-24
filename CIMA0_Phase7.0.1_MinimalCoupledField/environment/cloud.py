import numpy as np



class CloudField:


    def __init__(self,n):

        self.field=np.zeros(n)

        self.memory=np.zeros(n)



    def update(self,observer):


        # 长期记忆

        self.memory*=0.9999


        self.memory += (

            observer*0.0001

        )


        noise=np.random.randn(

            len(self.field)

        )*0.00001



        self.field += (

            self.memory

            +

            noise

        )


        # 防止成为隐藏控制器

        self.field*=0.99999



    def get(self):

        return self.field