import numpy as np



class AttractorGraph:


    def __init__(
        self,
        size=128,
        dim=512
    ):

        self.nodes=[]

        for i in range(size):

            self.nodes.append(
                np.random.normal(
                    0,
                    0.1,
                    dim
                )
            )


        self.last_index=0
        self.last_score=0



    def update(self,vector):


        scores=[]


        for node in self.nodes:

            s=(
                np.dot(node,vector)
                /
                (
                np.linalg.norm(node)
                *
                np.linalg.norm(vector)
                +
                1e-8
                )
            )

            scores.append(s)



        idx=int(
            np.argmax(scores)
        )


        score=scores[idx]


        # 微弱形成吸引子

        self.nodes[idx]+=(
            vector*0.001
        )


        self.last_index=idx
        self.last_score=float(score)



        return idx,score