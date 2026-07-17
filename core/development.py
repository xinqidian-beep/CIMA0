import numpy as np


class DevelopmentController:
    """
    发展阶段控制器

    按给定顺序（比如 听觉 -> 视觉 -> 文字 -> 语言）逐层解锁。
    一开始只有第一层醒着，能接收刺激；其余层保持沉默，
    不是"关掉"，只是还没轮到它，跟婴儿在听觉先成熟、视觉还没跟上是一个道理。

    "什么时候解锁下一层"不是数步数、不是写死的固定阈值，
    而是拿当前层自己最近一段时间的波动幅度，去跟它自己历史上的
    波动幅度比——如果比自己以前明显更平静了，就认为这层大致成熟了，
    可以解锁下一层。标准是每一层自己给自己定的，不是外部强加的。
    """

    def __init__(
        self,
        order=("audio", "vision", "text"),
        window=50,
        settle_ratio=0.5,
        min_steps_before_check=100
    ):

        self.order = list(order)

        # 已解锁到第几层（0-based，包含这一层本身）
        self.unlocked_index = 0

        self.window = window

        # 跟自己历史波动比，降到多少比例算"平静下来了"
        # 这是唯一一个需要人写的数字，但它只影响"多快换挡"，
        # 不影响"该不该有与或关系"这种核心逻辑，本质是个工程旋钮
        self.settle_ratio = settle_ratio

        self.min_steps_before_check = min_steps_before_check

        self.history = {
            k: []
            for k in self.order
        }

        # 每层自己的历史波动基线，用指数滑动平均持续更新，
        # 代表"这一层通常有多不稳定"，是它自己的、会变化的标准
        self.baseline_std = {
            k: None
            for k in self.order
        }

        self.steps_since_unlock = 0



    def is_unlocked(self, kind):

        if kind not in self.order:
            return True  # 不在发展顺序里的层，不受管控，正常收

        return self.order.index(kind) <= self.unlocked_index



    def current_layer(self):

        if self.unlocked_index >= len(self.order):
            return None

        return self.order[self.unlocked_index]



    def all_unlocked(self):

        return self.unlocked_index >= len(self.order) - 1



    def record(self, kind, stability_value):

        if not self.is_unlocked(kind):
            return

        hist = self.history[kind]

        hist.append(stability_value)

        if len(hist) > self.window:
            hist.pop(0)



    def step(self):

        self.steps_since_unlock += 1

        kind = self.current_layer()

        if kind is None:
            return None

        hist = self.history[kind]

        if (
            len(hist) < self.window
            or
            self.steps_since_unlock < self.min_steps_before_check
        ):
            return None

        current_std = float(np.std(hist))

        baseline = self.baseline_std[kind]

        if baseline is None:
            self.baseline_std[kind] = current_std
            return None

        # 持续更新这一层"通常"有多不稳定，标准本身也在跟着走
        self.baseline_std[kind] = (
            baseline * 0.98
            +
            current_std * 0.02
        )

        # 只有比自己历史上明显更平静，才算这一层"稳定下来了"
        if current_std < baseline * self.settle_ratio:

            is_last = (
                self.unlocked_index >= len(self.order) - 1
            )

            next_kind = (
                None
                if is_last
                else self.order[self.unlocked_index + 1]
            )

            # 就算是最后一层，也要记录"它自己稳定下来了"这件事，
            # 只是不再有下一层可以解锁——不能因为没有下一步，
            # 就连这一层本身有没有成熟都不算了
            if not is_last:
                self.unlocked_index += 1

            self.steps_since_unlock = 0

            return {
                "settled": kind,
                "unlocked": next_kind
            }

        return None



    def snapshot(self):

        return {
            "current_layer": self.current_layer(),
            "unlocked_up_to": self.order[:self.unlocked_index + 1],
            "baseline_std": {
                k: (
                    round(v, 5)
                    if v is not None else None
                )
                for k, v in self.baseline_std.items()
            }
        }