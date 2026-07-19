from core.cloud import Cloud
from core.stimulus import Stimulus
import time
import numpy as np

cloud = Cloud(
    cells=1000
)


while True:


    stimulus = Stimulus(

        kind="test",

        vector=np.random.rand(512),

        intensity=1.0

    )


    cloud.receive(
        stimulus
    )


    cloud.step()


    print(
        cloud.snapshot()
    )


    time.sleep(0.05)