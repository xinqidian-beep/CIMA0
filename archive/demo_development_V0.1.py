"""
最小可跑演示：按自然发展顺序（听觉 -> 视觉 -> 文字）逐层解锁

三种模态的刺激其实一直都在发生（模拟外部世界一直存在），
但一开始只有听觉层是"醒着"能收的，视觉和文字层的刺激会被
直接丢弃——不是它们不存在，是系统还没长到能处理它们的阶段。

什么时候解锁下一层，不是数步数，是看当前层最近的状态波动
是不是比它自己以前明显更平静了。平静下来，才解锁下一层。
"""

import time
import numpy as np

from core.layered_cloud import LayeredCloud
from core.development import DevelopmentController
from core.stimulus import Stimulus


DIM = 512

ORDER = ("audio", "vision", "text")

cloud = LayeredCloud(
    kinds=ORDER,
    cells_per_layer=150,
    dim=DIM
)

dev = DevelopmentController(
    order=ORDER,
    window=40,
    settle_ratio=0.5,
    min_steps_before_check=80
)


print("========================================")
print(" 发展阶段控制器 · 最小演示")
print(" 初始只有 audio 层醒着，其余层的刺激先被丢弃")
print("========================================")


step = 0

while True:

    step += 1

    # 模拟外部世界：三种模态的刺激其实一直都在发生
    kind = np.random.choice(ORDER)

    vector = np.random.rand(DIM)

    stimulus = Stimulus(kind, vector, 1.0)

    # 只有已解锁的层才真的收下这个刺激，没解锁的层直接丢弃
    if dev.is_unlocked(kind):
        cloud.receive(stimulus)

    cloud.step()

    # 把"当前正在成长"的那一层的稳定度喂给发展控制器
    growing_layer = dev.current_layer()

    if growing_layer is not None:

        stability = cloud.layers[growing_layer].attractor.last_score

        dev.record(growing_layer, stability)

    event = dev.step()

    if event:
        print(
            f"\n>>> 第{step}步：{event['settled']} 层已趋于稳定，"
            f"解锁下一层：{event['unlocked']}\n"
        )

    if step % 50 == 0:
        print(step, dev.snapshot())

    time.sleep(0.005)
