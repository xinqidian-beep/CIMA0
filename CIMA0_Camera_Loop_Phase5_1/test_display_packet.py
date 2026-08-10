import cv2
import numpy as np

from core.display_io import DisplayIO


def make_packet():

    #
    # 模拟 planet 彩色视频
    #
    h = 240
    w = 320


    img = np.zeros(
        (h,w,3),
        dtype=np.uint8
    )


    #
    # 移动彩色方块
    #

    x = 100
    y = 80


    img[
        y:y+40,
        x:x+40,
        0
    ] = 255


    img[
        y:y+40,
        x:x+40,
        1
    ] = 100



    return {

        "bytes":
            img.tobytes(),

        "shape":
            img.shape,

        "dtype":
            "uint8"

    }



def main():

    print(
        "Display packet test"
    )


    display = DisplayIO()


    while True:


        packet = make_packet()


        frame = display.encode(
            packet
        )


        print(
            frame.shape,
            frame.dtype
        )


        cv2.imshow(
            "test",
            frame
        )


        if cv2.waitKey(30)==27:
            break



if __name__=="__main__":

    main()