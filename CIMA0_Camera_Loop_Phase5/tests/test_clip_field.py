
import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
import cv2
import time


from core.clip_field import CLIPField



CLIP_WEIGHT = (
    r"C:\CIMA0\models"
    r"\open_clip_pytorch_model.bin"
)



def main():


    print("=" * 60)
    print("CIMA0 Phase5 CLIPField Test")
    print("")
    print("ESC : exit")
    print("=" * 60)



    #
    # CLIP visual cloud
    #

    clip_field = CLIPField(
        weight_path=CLIP_WEIGHT,
        device="cpu"
    )



    #
    # camera
    #

    camera = cv2.VideoCapture(0)



    if not camera.isOpened():

        print(
            "Camera open failed"
        )

        return



    counter = 0



    while True:


        ok, frame = camera.read()


        if not ok:

            continue



        #
        # same byte boundary
        # as CameraPlanet
        #

        packet = {

            "bytes":
                frame.tobytes(),

            "shape":
                frame.shape,

            "dtype":
                str(frame.dtype)

        }



        #
        # external collision
        #

        clip_field.receive(
            packet
        )



        #
        # CLIP cloud evolution
        #

        clip_field.step()



        counter += 1



        #
        # low frequency snapshot
        #

        if counter % 30 == 0:


            state = clip_field.snapshot()



            print()
            print(
                "time:",
                counter
            )


            print(
                state
            )



        #
        # display original camera
        #

        cv2.imshow(
            "Phase5 Camera Input",
            frame
        )



        key = cv2.waitKey(1) & 0xff


        if key == 27:

            break



    camera.release()

    cv2.destroyAllWindows()



if __name__ == "__main__":

    main()