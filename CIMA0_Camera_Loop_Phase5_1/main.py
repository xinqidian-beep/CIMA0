import cv2
import numpy as np
import time

from core.internal_dynamics_observer import InternalDynamicsObserver
from core.display_io import DisplayIO



class FakeInternalDynamics:
    """
    模拟 InternalDynamics 输出

    只有内部状态。
    不知道 display。
    """

    def __init__(self):

        self.age = 0

        self.field = np.zeros(
            (32,32,3),
            dtype=np.float32
        )


    def step(self):

        self.age += 1


        #
        # 每5秒移动一次
        #

        x = (self.age // 150) % 32


        self.field *= 0


        #
        # 红色方块
        #

        self.field[5:10,x:x+5,0] = 1.0


        #
        # 绿色跟随残影
        #

        if x > 3:

            self.field[5:10,x-3:x+2,1] = 0.5


        #
        # 蓝色远处状态
        #

        if x > 8:

            self.field[5:10,x-8:x-3,2] = 0.3



    def snapshot(self):

        return {

            "visual":

                self.field.copy()

        }




def main():


    print(
        "CIMA0 packet stream test"
    )


    dynamics = FakeInternalDynamics()


    observer = InternalDynamicsObserver()


    display = DisplayIO(
        height=320,
        width=320
    )



    while True:


        #
        # internal evolution
        #

        dynamics.step()



        #
        # snapshot
        #

        snapshot = dynamics.snapshot()



        #
        # observer read only
        #

        sampled = observer.read(
            snapshot,
            {
                "visual":1024
            }
        )



        #
        # same structure packet
        #

        packet = observer.pack(
            sampled,
            source="visual",
            timestamp=dynamics.age
        )



        #
        # display decode
        #

        frame = display.encode(
            packet["visual"]
        )



        if frame is not None:

            cv2.imshow(
                "CIMA0",
                frame
            )



        if cv2.waitKey(30)==27:

            break



    cv2.destroyAllWindows()



if __name__=="__main__":

    main()