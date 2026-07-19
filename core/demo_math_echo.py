import time
import numpy as np

from core.cloud import Cloud
from core.stimulus import Stimulus


class MathEchoDemo:
    def __init__(self, dim=512, cells=256):
        self.dim = dim
        self.cloud = Cloud(cells=cells, dim=dim)

        # 固定的 readout 向量组（镜子），不训练不更新
        self.num_readout = 4
        self.readout_vectors = self._init_readout_vectors()

        # 回声混入系数
        self.echo_alpha = 0.9  # 0 表示纯噪声驱动，1 接近“自己对自己说话”

        # 初始回声（全零）
        self.last_echo = np.zeros(self.dim, dtype=np.float32)

        self.step_count = 0

    def _init_readout_vectors(self):
        """固定随机 readout basis，用来从 Cloud 状态中抽取回声向量。"""
        # 这里简单用标准正态，然后正则化
        vecs = np.random.normal(0, 1.0, (self.num_readout, self.dim))
        norms = np.linalg.norm(vecs, axis=1, keepdims=True) + 1e-8
        return (vecs / norms).astype(np.float32)

    def _readout_from_cloud(self):
        """
        从 Cloud 当前状态读出一个 echo 向量：
        - 先把所有 cell 的 state 做平均（只是一个简单聚合方式）
        - 再投影到若干 readout 向量上，做线性组合
        """
        # 所有 cell 的平均状态
        states = np.array([c.state for c in self.cloud.cells])  # shape: [cells, dim]
        avg_state = states.mean(axis=0)  # [dim]

        # 投影到 readout basis 上
        coeffs = self.readout_vectors @ avg_state  # [num_readout]
        echo = coeffs @ self.readout_vectors      # 回到 [dim]

        return echo.astype(np.float32)

    def _generate_stimulus_vector(self):
        """
        生成这一步要送给 Cloud 的扰动向量：
        - 外部噪声 + 上一步的 echo（衰减后）
        """
        # 外部噪声
        noise = np.random.normal(0, 0.3, self.dim).astype(np.float32)

        # 当前刺激 = 噪声 + 衰减回声
        vector = noise + self.echo_alpha * self.last_echo

        # 适当正则化为一个比较稳定的范数
        norm = np.linalg.norm(vector) + 1e-8
        vector = vector / norm

        return vector

    def step(self):
        # 1. 构造刺激向量
        vec = self._generate_stimulus_vector()

        # 2. 封装为 Stimulus（kind 在 Cloud 内不用，随便给个 'echo'）
        stim = Stimulus(kind="echo", vector=vec, intensity=1.0)

        # 3. 投入 Cloud
        self.cloud.receive(stim)

        # 4. 让 Cloud 演化一步
        self.cloud.step()

        # 5. 从 Cloud 当前状态读出新的 echo
        self.last_echo = self._readout_from_cloud()

        # 6. 打印一点简单观测
        snap = self.cloud.snapshot()
        if self.step_count % 50 == 0:
            echo_norm = float(np.linalg.norm(self.last_echo))
            attractor_score = snap.get("attractor_score", 0.0)
            avg_energy = snap.get("avg_energy", 0.0)
            active_fraction = snap.get("active_fraction", 0.0)
            print(
                f"step={self.step_count:5d} "
                f"attractor_score={snap['attractor_score']:.4f} "
                f"avg_energy={snap['avg_energy']:.4f} "
                f"active_fraction={snap['active_fraction']:.3f} "
                f"echo_norm={echo_norm:.3f}"
            )

        self.step_count += 1

    def run(self, max_steps=5000, sleep=0.0):
        print("=== CIMA0 Math Echo Demo Start ===")
        while self.step_count < max_steps:
            self.step()
            if sleep > 0:
                time.sleep(sleep)
        print("=== CIMA0 Math Echo Demo End ===")


if __name__ == "__main__":
    demo = MathEchoDemo(dim=512, cells=256)
    demo.run(max_steps=2000, sleep=0.0)