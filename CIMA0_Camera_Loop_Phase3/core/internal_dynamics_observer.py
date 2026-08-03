import numpy as np


class InternalDynamicsObserver:
    """
    Read only observer.

    Does NOT:
        modify state
        allocate resource
        control modules
    """

    def __init__(self):
        self.previous = {}

    # ------------------------------------------------------------
    # 原有 observe()/_measure()/_extract()/_collect() 保持不变
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
    # 新增：read() —— 按 allocate() 给出的预算做稀疏读取
    # ------------------------------------------------------------

    @staticmethod
    def _sparse_array(arr, budget):
        arr = np.asarray(arr, dtype=np.float32).reshape(-1)
        total = arr.size
        if total == 0:
            return arr
        if budget <= 0:
            return arr[:0]
        if budget >= total:
            return arr
        stride = max(1, total // int(budget))
        return arr[::stride]

    def _read_value(self, value, budget):
        """
        通用递归读取，不认字段名：
            dict   -> 子项均分预算，递归处理
            array  -> 稀疏抽取
            scalar -> 原样返回（预算对标量没有意义）
        """
        if isinstance(value, dict):
            if not value or budget <= 0:
                return {}
            share = budget / len(value)
            return {k: self._read_value(v, share) for k, v in value.items()}

        if isinstance(value, np.ndarray):
            return self._sparse_array(value, budget)

        if isinstance(value, (int, float)):
            return value

        return None

    def read(self, snapshot, allocation):
        """
        snapshot   -- 与 observe() 收到的同一份原始快照
        allocation -- compute.allocate(request) 的返回值 {key: budget}
        """
        result = {}
        for key, value in snapshot.items():
            budget = allocation.get(key, 0)
            result[key] = self._read_value(value, budget)
        return result