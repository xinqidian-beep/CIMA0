import cv2
import time


from core.internal_dynamics import InternalDynamics
from core.internal_dynamics_observer import InternalDynamicsObserver
from core.compute_system import ComputeSystem
from core.display_io import DisplayIO

from core.camera_planet import CameraPlanet
from core.clip_field import CLIPField


CLIP_WEIGHT = (
    r"C:\CIMA0\models\open_clip_pytorch_model.bin"
)



class LocalClock:

    def __init__(
        self,
        interval
    ):

        self.interval = interval
        self.last = time.perf_counter()



    def due(self):

        now = time.perf_counter()

        if now - self.last >= self.interval:

            self.last = now

            return True

        return False




def main():


    print("="*60)

    print(
        "CIMA0 Phase5.1 Camera Loop"
    )

    print(
        "ESC : exit"
    )

    print("="*60)



    #
    # internal system
    #

    internal = InternalDynamics()



    clip = CLIPField(
        weight_path=CLIP_WEIGHT,
        device="cpu"
    )



    internal.register(
        "clip",
        clip
    )



    #
    # camera boundary
    #

    camera = cv2.VideoCapture(0)


    camera_planet = CameraPlanet()



    #
    # observer
    #

    observer = InternalDynamicsObserver()


    compute = ComputeSystem(
        capacity=100
    )



    display = DisplayIO()



    #
    # clocks
    #

    camera_clock = LocalClock(
        1/30
    )


    internal_clock = LocalClock(
        0.01
    )


    observer_clock = LocalClock(
        0.1
    )


    display_clock = LocalClock(
        0.1
    )



    if not camera.isOpened():

        print(
            "camera open failed"
        )

        return



    while True:



        #
        # Camera
        #

        if camera_clock.due():


            ret, frame = camera.read()


            if ret:


                camera_planet.step(
                    frame
                )


                raw = camera_planet.state()


                if raw is not None:


                    #
                    # byte broadcast
                    #

                    internal.receive(
                        raw
                    )




        #
        # Internal evolution
        #

        if internal_clock.due():


            internal.step()



        #
        # Observer
        #

        if observer_clock.due():


            snapshot = internal.snapshot()


            request = observer.observe(
                snapshot
            )


            allocation = compute.allocate(
                request
            )


            observer.read(
                snapshot,
                allocation
            )




        #
        # Display only
        #

        if display_clock.due():


            clip = internal.organs.get(
                "clip"
            )


            if clip is not None:


                field = clip.display_field()


                if field is not None:


                    print(
                        "field:",
                        field.shape,
                        field.min(),
                        field.max()
                    )


                    frame_out = display.encode(
                        field
                    )


                    cv2.imshow(
                        "CIMA0",
                        frame_out
                    )




        key = cv2.waitKey(1) & 0xff


        if key == 27:

            break



    camera.release()

    cv2.destroyAllWindows()



if __name__ == "__main__":

    main()