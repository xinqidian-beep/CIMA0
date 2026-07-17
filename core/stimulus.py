import time


class Stimulus:
    """
    外部刺激统一格式（全项目唯一定义，input/bus.py 等其他模块统一从这里 import）

    不同模态目前约定的向量维度（后续接入真实 encoder 时以此为准）:
        vision:   512维 (OpenCLIP)
        audio:    512维 (Whisper embedding，具体以接入模型为准)
        text:     512维
        keyboard: 512维
    """

    def __init__(
        self,
        kind,
        vector,
        intensity=1.0
    ):

        self.kind = kind

        self.vector = vector

        self.intensity = intensity

        self.timestamp = time.time()