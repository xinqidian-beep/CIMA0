"""
最小可跑演示：按更细致的自然发展顺序逐层解锁

单声道 -> 双声道 -> 视觉 -> 语言（说话的声音）-> 文字符号体系

顺序背后的逻辑：
- 单声道到双声道是质变，不是同一件事的两个版本——双声道需要
  同时整合两只耳朵的时间差/强度差来定位声源，必须踩在单声道
  成熟的基础上才能长出来
- 语言（说话的声音）不是泛泛的听觉，是从听觉这个原始通道里
  进一步抽出来的结构化模式（音素、词），排在视觉之后单独成一层
- 文字符号体系最后、最抽象，踩在口语基础上

五种"刺激"其实一直都在发生（模拟外部世界一直存在），
但只有已解锁的层才会真的收下，没解锁的层直接丢弃这次刺激。
"""

import time
import numpy as np

from core.layered_cloud import LayeredCloud
from core.development import DevelopmentController
from core.stimulus import Stimulus


DIM = 512

ORDER = ("mono", "stereo", "vision", "language", "text")

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
print(" 发展阶段控制器 · 五级顺序演示")
print(" 单声道 -> 双声道 -> 视觉 -> 语言 -> 文字")
print(" 初始只有 mono 层醒着，其余层的刺激先被丢弃")
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