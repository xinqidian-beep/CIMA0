import numpy as np


class DisplayIO:
    """
    Structural display adapter.

    internal read result -> display frame

    Does NOT:
        analyze
        interpret
        fuse
        control
        modify internal state

    只认三种类型：dict / ndarray / scalar，不认字段名。
    """

    def __init__(self, height=240, width=320):
        self.height = height
        self.width = width

    def encode(self, read_result):
        if not read_result:
            return None

        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self._render(read_result, frame, 0, 0, self.width, self.height)
        return frame

    def _render(self, obj, frame, x, y, w, h):
        if obj is None or w <= 0 or h <= 0:
            return

        if isinstance(obj, dict):
            items = [(k, v) for k, v in obj.items() if v is not None]
            if not items:
                return
            step = max(1, h // len(items))
            for i, (_, value) in enumerate(items):
                self._render(value, frame, x, y + i * step, w, step)
            return

        if isinstance(obj, np.ndarray):
            if obj.size == 0:
                return
            arr = np.nan_to_num(np.abs(obj.astype(np.float32)))
            mx = arr.max()
            if mx > 0:
                arr = arr / mx
            # read() 返回的是一维稀疏序列，不保留原始二维形状，
            # 这里按顺序把它铺成一条横向强度带，不是真正的二维空间重建
            strip = (arr * 255).astype(np.uint8)
            strip = np.repeat(strip, max(1, w // max(1, len(strip)) + 1))[:w]
            if len(strip) < w:
                strip = np.pad(strip, (0, w - len(strip)))
            band_h = max(1, h)
            frame[y:y + band_h, x:x + w, 0] = strip[np.newaxis, :]
            return

        if isinstance(obj, (int, float)):
            value = min(1.0, abs(float(obj)))
            length = int(w * value)
            bar_h = max(1, min(6, h))
            frame[y:y + bar_h, x:x + length, 1] = 255
            return