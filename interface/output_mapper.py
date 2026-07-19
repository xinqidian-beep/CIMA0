import numpy as np


class OutputMapper:
    """
    CIMA0 内部状态 -> byte

    第一版只做状态压缩。
    不解释意义。
    """

    def __init__(self):
        pass


    def map(self, field):

        # 限制范围
        x = np.asarray(field)

        x = np.tanh(x)


        # [-1,1] -> [0,255]

        data = (
            (x + 1.0)
            *
            127.5
        )


        data = np.clip(
            data,
            0,
            255
        )


        return bytes(
            data.astype(
                np.uint8
            )
        )