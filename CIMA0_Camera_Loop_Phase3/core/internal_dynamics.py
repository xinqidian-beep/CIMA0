class InternalDynamics:
    """
    Internal lifecycle container.

    Only:
        receive()
        step()
        snapshot()

    No:
        byte interpretation
        sampling decision
        resource allocation
        state modification
    """

    def __init__(self, planet, clip):
        self.planet = planet
        self.clip = clip

    def receive(self, data):
        """
        外部字节流只作为扰动进入 clip。
        planet 完全不接触外部数据，保持自驱动、不与外界沟通。
        """
        self.clip.update(data)

    def step(self):
        """
        只推进 planet 自己的演化。
        clip 已经在 receive() 的 update() 里演化过了，这里不再重复。
        """
        self.planet.step()

    def snapshot(self):
        """
        只读快照，不修改任何内部状态。
        对 planet.state 做拷贝，避免下游任何操作反向污染它。
        """
        return {
            "planet": {
                "state": self.planet.state.copy()
            },
            "clip": self.clip.state()
        }