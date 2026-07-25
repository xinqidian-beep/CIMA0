import random
from collections import deque


class AttentionField:
    """
    方案二：局部传播（谣言扩散），用于发现"簇"而不是单点。

    规则：
      1. 一个 cell 在被 event() 正常推进之后，检查自己这次的变化有没有超过
         "自己历史波动幅度"算出来的阈值（local_threshold，只依赖自己的历史）。
         这是二元判断（超过/没超过），不是打分排序。
      2. 超过阈值 -> 以概率 p 把信号传给它的邻居（度数有限，比如 4-8 个），
         不会传到图上不相邻的地方，也不会一次性触达很多 cell。
      3. 邻居收到信号后，不是立刻被"精算"，而是被放进一个有上限大小的
         pending 队列，真正处理时还要经过 MIN_DELAY 个 event 的延迟，
         防止瞬时闭环（观测和响应同步咬合，变成隐藏的实时控制器）。
      4. 从 pending 队列取任务给 Compute 层处理时，是先进先出 + 队列内随机抽样，
         不是按"谁的信号最强"排序后只挑前几名。

    关键的架构约束：
      - 任何一次 flare/propagate 调用，触达的 cell 数量严格有界（1 + 度数），
        不会在任何一个时间点访问全部 N 个 cell。
      - AttentionField 本身不修改任何 cell 的状态，只读 x/v，只写自己的队列。
    """

    def __init__(self, max_queue=256, propagate_prob=0.15, min_delay=200):
        self.pending = deque()          # (idx, enqueued_at)
        self.pending_set = set()        # 防止同一个 idx 重复入队
        self.max_queue = max_queue
        self.propagate_prob = propagate_prob
        self.min_delay = min_delay
        self.max_touch_per_call = 0     # 用于自检：记录单次调用最多摸过几个 cell

    def _enqueue(self, idx, now):
        if idx in self.pending_set:
            return
        if len(self.pending) >= self.max_queue:
            old_idx, _ = self.pending.popleft()
            self.pending_set.discard(old_idx)
        self.pending.append((idx, now))
        self.pending_set.add(idx)

    def observe_after_step(self, universe, idx, rng=random):
        """
        在 universe.event() 正常推进了 idx 这个 cell 之后调用。
        只读这一个 cell + 它的邻居列表(不读邻居的具体状态，只用于传播判断的对象)。
        """
        touched = 1
        cell = universe.cells[idx]
        # cell 自己已经在 step() 内部判断过"这一步是否明显异于我的背景水平"
        if cell.is_flaring():
            self._enqueue(idx, universe.time)
            for j in universe.neighbors[idx]:
                touched += 1
                if rng.random() < self.propagate_prob:
                    self._enqueue(j, universe.time)
        self.max_touch_per_call = max(self.max_touch_per_call, touched)
        return touched

    def pop_ready(self, now, k):
        """
        取出最多 k 个"延迟已满足、可以被精算"的任务。
        先进先出，不按信号强度排序，避免变成隐藏的排序择优机制。
        """
        ready = []
        remaining = deque()
        while self.pending:
            idx, enqueued_at = self.pending.popleft()
            if len(ready) < k and now - enqueued_at >= self.min_delay:
                ready.append(idx)
                self.pending_set.discard(idx)
            else:
                remaining.append((idx, enqueued_at))
        self.pending = remaining
        return ready
