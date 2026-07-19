import numpy as np


class ByteFieldMapper:


    """
    byte -> 云扰动场

    没有语义。
    只是物理映射。
    """


    def __init__(
        self,
        dim=512
    ):

        self.dim=dim



    def map(
        self,
        data:bytes
    ):

        field=np.zeros(
            self.dim
        )


        for i,b in enumerate(data):

            idx=i % self.dim

            field[idx]+=(
                b/255.0
            )


        return field