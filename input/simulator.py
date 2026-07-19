import numpy as np

from core.stimulus import Stimulus


class WorldSimulator:


    def __init__(self):

        self.step=0


    def poll(self):

        self.step += 1

        stimuli=[]


        # 模拟声音一直存在
        if self.step % 5 == 0:

            vector=np.random.rand(512)

            stimuli.append(
                Stimulus(
                    "audio",
                    vector,
                    1.0
                )
            )


        # 模拟视觉稍晚出现
        if self.step > 500 and self.step % 10 == 0:

            vector=np.random.rand(512)

            stimuli.append(
                Stimulus(
                    "vision",
                    vector,
                    1.0
                )
            )


        # 模拟文字更晚出现
        if self.step > 1000 and self.step % 20 == 0:

            vector=np.random.rand(512)

            stimuli.append(
                Stimulus(
                    "text",
                    vector,
                    1.0
                )
            )


        return stimuli