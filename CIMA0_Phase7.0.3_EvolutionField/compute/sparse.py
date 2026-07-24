import random



class SparseCompute:


    def __init__(
        self,
        capacity=64
    ):

        self.capacity = capacity

        self.field = {}



    def compress(
        self,
        observations
    ):


        """
        只保存有限局部趋势

        不保存整个世界
        """


        for idx,state in observations:


            self.field[idx] = {

                "activity":
                state["activity"],

                "energy":
                state["energy"],

                "life":10

            }



        # 容量限制

        if len(self.field)>self.capacity:


            remove=list(self.field.keys())


            while len(remove)>self.capacity:

                k=random.choice(remove)

                remove.remove(k)


            for k in remove:

                del self.field[k]



    def perturbation(self):


        """
        产生短暂影响

        不改变动力参数
        """


        result={}


        for idx,data in self.field.items():


            strength=(

                data["activity"]

                *

                0.00001

            )


            result[idx]=strength



            data["life"]-=1



        # 自然消散

        dead=[

            k for k,v in self.field.items()

            if v["life"]<=0

        ]


        for k in dead:

            del self.field[k]



        return result