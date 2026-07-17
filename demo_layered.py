"""
最小可跑演示：分层云 + 自适应层间连接

模拟场景：
    - 视觉和听觉经常"同时"出现（比如看到一个东西、同时听到它发出的声音）
    - 文本则是独立、随机出现的，跟视觉/听觉没有关联

没有写任何阈值去"判断"这三者该怎么关联。
只是让它们反复共同经历，然后观察 vision-audio 之间的连接权重，
是否会自己比 vision-text / audio-text 长得更高。

跑起来看 link 数值随时间的变化就知道了。
"""

import time
import numpy as np

from core.layered_cloud import LayeredCloud
from core.stimulus import Stimulus


DIM = 512

cloud = LayeredCloud(
    kinds=("vision", "audio", "text"),
    cells_per_layer=200,
    dim=DIM
)

# 视觉和听觉共享的一个"关联模式"，代表"同一件事"在两种模态上的样子
# 每次用的时候加一点随机噪声，不是完全一样的向量
shared_pattern = np.random.rand(DIM)


step = 0

print("========================================")
print(" 分层云自适应连接 · 最小演示")
print(" 观察 vision-audio 的连接权重是否自己长起来")
print("========================================")

while True:

    step += 1

    if step % 3 != 0:

        # 三次里有两次：视觉和听觉一起出现（模拟“看到+听到同一件事”）
        cloud.receive(
            Stimulus(
                "vision",
                shared_pattern + np.random.normal(0, 0.05, DIM),
                1.0
            )
        )

        cloud.receive(
            Stimulus(
                "audio",
                shared_pattern + np.random.normal(0, 0.05, DIM),
                1.0
            )
        )

    else:

        # 三次里有一次：只有文本单独出现，跟视觉听觉没有任何关系
        cloud.receive(
            Stimulus(
                "text",
                np.random.rand(DIM),
                1.0
            )
        )

    cloud.step()

    if step % 20 == 0:
        print(step, cloud.snapshot())

    time.sleep(0.01)
