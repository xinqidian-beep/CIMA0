import numpy as np


class InputField:


    """
    原始输入边界

    不理解内容
    """

    def generate(self):

        x = np.random.randint(
            0,
            128
        )

        y = np.random.randint(
            0,
            128
        )

        value = np.random.randn()*0.5


        return {
            "position":(x,y),
            "value":value
        }