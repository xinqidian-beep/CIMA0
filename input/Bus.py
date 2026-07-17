import random
import numpy as np

from core.stimulus import Stimulus


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