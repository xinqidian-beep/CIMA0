import random
import numpy as np

from core.cell import Cell


def build_symmetric_neighbors(n, degree, seed):
    """
    无向图：保证 j in neighbors[i] 当且仅当 i in neighbors[j]，且每个节点度数恰好为 degree
    （n*degree 为奇数时，允许极少数节点相差 1）。

    用配置模型（configuration model）的思路：每个节点先领 degree 个"接口"，
    把全部接口打乱后两两配对成边；遇到自环或重复边就和后面的接口交换位置重试，
    避免像"每个节点各自独立随机采样邻居"那样产生大量单向边（之前实测过 98% 不对称）。
    """
    rng = random.Random(seed)
    stubs = []
    for i in range(n):
        stubs.extend([i] * degree)
    rng.shuffle(stubs)
    if len(stubs) % 2 == 1:
        stubs.pop()

    neighbors = {i: set() for i in range(n)}
    i = 0
    pass_count = 0
    max_passes = 10
    while i < len(stubs) - 1 and pass_count < max_passes:
        a, b = stubs[i], stubs[i + 1]
        if a == b or b in neighbors[a]:
            # 找后面一个可以交换的位置，避免自环/重复边
            swapped = False
            for k in range(i + 2, len(stubs)):
                c = stubs[k]
                if c != a and c not in neighbors[a]:
                    stubs[i + 1], stubs[k] = stubs[k], stubs[i + 1]
                    b = stubs[i + 1]
                    swapped = True
                    break
            if not swapped:
                i += 2
                continue
        neighbors[a].add(b)
        neighbors[b].add(a)
        i += 2
        if i >= len(stubs) - 1:
            pass_count += 1

    # 兜底：极少数节点如果还是孤立（理论上概率很低），直接和随机节点连一条边
    for i in range(n):
        while len(neighbors[i]) == 0:
            j = rng.randrange(n)
            if j != i and j not in neighbors[i]:
                neighbors[i].add(j)
                neighbors[j].add(i)

    return {i: list(s) for i, s in neighbors.items()}


class Universe:
    """
    Dynamics 层。没有任何一个函数会在同一时刻遍历全部 cell。
    唯一的推进方式是 event()：随机抽一个 cell，读它的邻居，推进它一步。
    """

    def __init__(self, n=4096, degree=4, omega_lo=0.97, omega_hi=1.03,
                 coupling_strength=0.02, seed=42):
        rng = np.random.RandomState(seed)
        self.time = 0
        self.coupling_strength = coupling_strength
        self.cells = [
            Cell(x=rng.normal(0, 0.01), v=rng.normal(0, 0.01),
                 omega=rng.uniform(omega_lo, omega_hi))
            for _ in range(n)
        ]
        self.neighbors = build_symmetric_neighbors(n, degree, seed)

    def _local_coupling(self, idx):
        cell = self.cells[idx]
        force = 0.0
        for j in self.neighbors[idx]:
            force += (self.cells[j].x - cell.x) * self.coupling_strength
        return force

    def event(self, perturb_map=None):
        idx = random.randrange(len(self.cells))
        coupling = self._local_coupling(idx)
        p = 0.0
        if perturb_map is not None:
            p = perturb_map.get(idx, 0.0)
        self.cells[idx].step(coupling=coupling, perturb=p)
        self.time += 1
        return idx

    def touch(self, idx):
        """给外部只读访问单个 cell 用，不允许批量遍历全部使用这个方法。"""
        return self.cells[idx]

    def sample(self, ids):
        """只读采样，供 Observer 使用，一次只应传入一个有界大小的 ids 列表。"""
        return [(i, self.cells[i].x, self.cells[i].v) for i in ids]
