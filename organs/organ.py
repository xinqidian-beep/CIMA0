class Organ:
    """
    CIMA0 器官基类

    器官不是控制器。
    只接收场状态，产生局部响应。
    """

    def __init__(self, name="organ"):
        self.name = name
        self.activity = 0

    def receive(self, field):
        """
        接收 CIMA0 场状态
        """
        self.activity += 1

    def step(self):
        """
        器官自身演化
        """
        pass

    def emit(self):
        """
        返回反馈
        """
        return None