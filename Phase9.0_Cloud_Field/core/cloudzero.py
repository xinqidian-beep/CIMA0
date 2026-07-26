import numpy as np


class CloudMatrix:
    """
    Minimal external cloud field.

    不控制 Cell
    不保存 Cell 状态

    只提供:
        空
        正扰动
        负扰动
        零扰动

    """

    def __init__(self, size):

        self.size = size

        # NaN = 没有云
        # 0   = 云存在但值为0
        # +/- = 扰动
        self.field = np.full(
            size,
            np.nan
        )


    def clear(self):

        self.field.fill(
            np.nan
        )


    def deposit_random(
        self,
        count=4,
        strength=1.0
    ):

        """
        生成云事件

        不固定位置
        不跟 Cell 耦合
        """

        self.clear()


        ids = np.random.choice(
            self.size,
            count,
            replace=False
        )


        for cid in ids:

            value = np.random.uniform(
                -strength,
                strength
            )

            self.field[cid] = value


    def contact(self, cid):

        """
        Cell读取接口

        返回:
            None:
                无云

            float:
                云值
        """

        value = self.field[cid]


        if np.isnan(value):

            return None
        # 一次接触后消失
        self.field[cid] = np.nan    


        return float(value)