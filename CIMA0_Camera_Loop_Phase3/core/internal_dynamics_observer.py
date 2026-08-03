import numpy as np


class InternalDynamicsObserver:
    """
    Read only observer.

    Does NOT:
        modify state
        allocate resource
        control modules
    """

    def __init__(self, coarse_ratio=0.15):
        self.previous = {}          # observe() 用：每个顶层 key 的活跃度历史
        self.previous_arrays = {}   # read() 用：每个数组各自的上一次读数，用来求 δ
        self.coarse_ratio = coarse_ratio  # 粗算基线保留多大比例，暂定值，见下方说明

    # ------------------------------------------------------------
    # observe()：产生资源需求，逻辑不变
    # ------------------------------------------------------------

    def observe(self, snapshot):
        requests = {}
        for name, state in snapshot.items():
            requests[name] = self._measure(name, state)
        return requests

    def _measure(self, name, state):
        current = self._extract(state)
        if current is None:
            return 0.0
        previous = self.previous.get(name, current)
        delta = abs(current - previous)
        self.previous[name] = current
        return float(min(1.0, 0.7 * current + 0.3 * delta))

    def _extract(self, obj):
        values = []
        self._collect(obj, values)
        if values:
            return np.mean(np.abs(values))
        return None

    def _collect(self, obj, out):
        if isinstance(obj, dict):
            for v in obj.values():
                self._collect(v, out)
        elif isinstance(obj, np.ndarray):
            if obj.size:
                out.append(float(np.mean(np.abs(obj))))
        elif isinstance(obj, (int, float)):
            out.append(float(obj))

    # ------------------------------------------------------------
    # read()：按预算做举手竞争 + 粗算基线 + 焦点精算
    # ------------------------------------------------------------

    def read(self, snapshot, allocation):
        result = {}
        for key, value in snapshot.items():
            budget = allocation.get(key, 0)
            result[key] = self._read_value(value, budget, path=key)
        return result

    def _read_value(self, value, budget, path):
        if isinstance(value, dict):
            if not value or budget <= 0:
                return {}
            share = budget / len(value)
            return {
                k: self._read_value(v, share, f"{path}.{k}")
                for k, v in value.items()
            }

        if isinstance(value, np.ndarray):
            return self._hand_raise_read(value, budget, path)

        if isinstance(value, (int, float)):
            return value

        return None

    def _hand_raise_read(self, arr, budget, path):
        """
        粗算基线：永远覆盖全数组，压缩比例固定，
                  保证任何区域都不会被彻底漏看（这是这次要修的核心问题）。
        焦点精算：与自身历史求 δ，举手竞争，δ 最大的位置在预算内获得精确读数。
        """
        flat = arr.reshape(-1).astype(np.float32)
        total = flat.size

        # 粗算：固定比例压缩，不管预算多少、不管这次谁举手，永远存在
        coarse_n = max(1, int(total * self.coarse_ratio))
        coarse_stride = max(1, total // coarse_n)
        coarse = flat[::coarse_stride]

        # 自比较求 delta：这一步就是让"活跃区域"真正被找到，而不是瞎抽
        prev = self.previous_arrays.get(path)
        if prev is None or prev.shape != flat.shape:
            delta = np.zeros_like(flat)
        else:
            delta = np.abs(flat - prev)
        self.previous_arrays[path] = flat.copy()

        # 精算名额：预算换算成这次能精确读取几个位置
        n_precise = max(0, min(total, int(budget)))

        if n_precise > 0:
            winners = np.argsort(delta)[::-1][:n_precise]
            precise_values = flat[winners]
            precise_indices = winners
        else:
            precise_values = np.zeros(0, dtype=np.float32)
            precise_indices = np.zeros(0, dtype=np.int64)

        return {
            "coarse": coarse,
            "precise_values": precise_values,
            "precise_indices": precise_indices,
        }