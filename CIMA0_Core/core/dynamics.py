import numpy as np


def local_interaction(
        values
):

    """
    公共局部规则

    没有：
        特殊区域
        特殊节点
        分类器
    """

    mean = np.mean(values)

    return np.tanh(
        mean
    )