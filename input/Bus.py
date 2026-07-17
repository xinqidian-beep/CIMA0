import time
import random
import numpy as np


class Stimulus:
    """
    外部刺激统一格式

    vision:
        512维

    audio:
        384维

    text:
        384维

    keyboard:
        128维
    """

    def __init__(
        self,
        kind,
        vector,
        intensity=1.0
    ):

        self.kind = kind
        self.vector = vector
        self.intensity = intensity
        self.timestamp = time.time()



class InputBus:


    def __init__(self):

        self.queue=[]


    def push(self, stimulus):

        self.queue.append(stimulus)



    def poll(self):

        """
        当前先模拟输入

        后面替换:
        
        camera.py
        whisper.py
        keyboard.py

        """

        if random.random()<0.2:

            kind=random.choice(
                [
                    "vision",
                    "audio",
                    "text"
                ]
            )


            vector=np.random.normal(
                0,
                1,
                512
            )


            return Stimulus(
                kind,
                vector,
                random.random()
            )


        return None