import numpy as np

from .cloud import Cloud


class LayeredCloud:
    """
    多模态分层云

    设计原则：最小打扰，最大自由
    - 每种模态各自一层，层内部就是一个独立的 Cell 云（复用现有 Cloud）
    - 刺激按 stimulus.kind 自动路由到对应层，不做别的判断
    - 层与层之间没有人为设定的 AND/OR 规则，只有一张会自己
      增长/衰减的连接权重表：
        两层这一刻同时活跃 -> 连接权重轻轻加强
        没有同时活跃       -> 连接权重自然衰减
      权重高低本身就是 AND / OR 的连续过渡：
        权重被反复喂到很高 -> 表现得像"必须同时出现才算数"（AND）
        权重一直很低       -> 各层各自独立响应就够了（OR）
      没有阈值需要人来指定，习惯是被"喂"出来的，不是被写死的。
    """

    def __init__(
        self,
        kinds=("vision", "audio", "text"),
        cells_per_layer=200,
        dim=512,
        grow_rate=0.02,
        decay_rate=0.01
    ):

        self.kinds = list(kinds)

        self.layers = {
            k: Cloud(cells=cells_per_layer, dim=dim)
            for k in self.kinds
        }

        n = len(self.kinds)

        # 层间连接权重，初始几乎为0，完全靠后天共同经历自己长出来
        self.link_weight = np.zeros((n, n))

        # 每层此刻的活跃度，连续值（活跃细胞占比），不做二值化判断
        self.activity = {k: 0.0 for k in self.kinds}

        self.grow_rate = grow_rate
        self.decay_rate = decay_rate

        self.step_count = 0



    def receive(self, stimulus):

        # 自动路由：只看 kind，扔进对应层，没有任何筛选或打分逻辑
        layer = self.layers.get(stimulus.kind)

        if layer is not None:
            layer.receive(stimulus)



    def step(self):

        # 每层各自独立演化，互不打扰
        for cloud in self.layers.values():
            cloud.step()

        # 用每层细胞的平均能量作为这一刻的活跃度（连续值，会随时间自然起伏）
        # 用 energy 而不是 activity 计数，是因为 energy 本身会自然衰减，
        # 能反映"最近有没有被持续唤起"，而不是"历史上有没有被摸过一次"
        for k, cloud in self.layers.items():

            n_cells = len(cloud.cells)

            mean_energy = sum(
                c.energy
                for c in cloud.cells
            ) / n_cells if n_cells else 0.0

            self.activity[k] = mean_energy

        self._update_links()

        self.step_count += 1



    def _update_links(self):

        n = len(self.kinds)

        for i in range(n):
            for j in range(n):

                if i == j:
                    continue

                a_i = self.activity[self.kinds[i]]
                a_j = self.activity[self.kinds[j]]

                # 同时活跃 -> 连接自己长粗一点（类似Hebbian：一起放电的神经元连接会加强）
                co_activation = a_i * a_j

                self.link_weight[i][j] += co_activation * self.grow_rate

                # 无论是否共同活跃，连接都会自然衰减，不喂就会慢慢淡忘
                self.link_weight[i][j] *= (1 - self.decay_rate)

                # 防止无限增长，给个软上限
                if self.link_weight[i][j] > 1.0:
                    self.link_weight[i][j] = 1.0

                if self.link_weight[i][j] < 0.0:
                    self.link_weight[i][j] = 0.0



    def snapshot(self):

        n = len(self.kinds)

        links = {}

        for i in range(n):
            for j in range(i + 1, n):

                key = f"{self.kinds[i]}-{self.kinds[j]}"

                # 双向权重取平均，展示成一个数
                w = (
                    self.link_weight[i][j]
                    +
                    self.link_weight[j][i]
                ) / 2

                links[key] = round(float(w), 4)

        return {
            "step": self.step_count,
            "activity": {
                k: round(v, 3)
                for k, v in self.activity.items()
            },
            "links": links
        }
