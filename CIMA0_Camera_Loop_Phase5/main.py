import cv2
import time

from core.internal_dynamics import InternalDynamics
from core.internal_dynamics_observer import InternalDynamicsObserver
from core.compute_system import ComputeSystem
from core.display_io import DisplayIO

from core.camera_planet import CameraPlanet
from core.camera_observer import CameraObserver
from core.camera_compute import CameraComputeSystem

from archive.planet import Planet
from core.clip_field import CLIPField


CLIP_WEIGHT = r"C:\CIMA0\models\open_clip_pytorch_model.bin"



class LocalClock:
    """
    Independent module clock.
    """

    def __init__(self, interval):

        self.interval = interval
        self.last = time.perf_counter()



    def due(self):

        now = time.perf_counter()

        if now - self.last >= self.interval:

            self.last = now
            return True

        return False




def main():

    print("=" * 60)
    print("CIMA0 Phase5 Internal Clock Loop")
    print()
    print("ESC : exit")
    print("=" * 60)



    #
    # internal world
    #

    internal = InternalDynamics()



    planet = Planet()


    clip = CLIPField(
        weight_path=CLIP_WEIGHT,
        device="cpu"
    )



    internal.register(
        "planet",
        planet
    )


    internal.register(
        "clip",
        clip
    )



    #
    # camera
    #

    camera = cv2.VideoCapture(0)


    camera_planet = CameraPlanet()

    camera_observer = CameraObserver()

    camera_compute = CameraComputeSystem()



    #
    # observer
    #

    observer = InternalDynamicsObserver()


    compute = ComputeSystem(
        capacity=100
    )



    #
    # display
    #

    display = DisplayIO()



    #
    # clocks
    #

    camera_clock = LocalClock(
        1 / 30
    )


    internal_clock = LocalClock(
        0.01
    )


    observer_clock = LocalClock(
        0.1
    )


    display_clock = LocalClock(
        1 / 30
    )



    #
    # observer cache
    #

    latest_snapshot = None

    latest_sample = None



    if not camera.isOpened():

        print(
            "Camera open failed"
        )



    while True:



        #
        # camera input
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
                    # byte stream boundary
                    #

                    internal.receive(
                        raw
                    )



        #
        # internal evolution
        #

        if internal_clock.due():

            internal.step()



        #
        # observer sampling
        #

        if observer_clock.due():


            latest_snapshot = internal.snapshot()



            request = observer.observe(
                latest_snapshot
            )


            allocation = compute.allocate(
                request
            )


            latest_sample = observer.read(
                latest_snapshot,
                allocation
            )



        #
        # display
        #

        if display_clock.due():


            if latest_sample is not None:


                field = latest_sample.get(
                    "planet"
                )


                if field is not None:


                    print(
                        "display:",
                        field.shape,
                        field.min(),
                        field.max()
                    )


                    frame_out = display.encode(
                        field
                    )


                    if frame_out is not None:

                        cv2.imshow(
                            "CIMA0",
                            frame_out
                        )



        #
        # exit
        #

        key = cv2.waitKey(1) & 0xff


        if key == 27:

            print(
                "CIMA0 stopped"
            )

            break



    camera.release()

    cv2.destroyAllWindows()




if __name__ == "__main__":

    main()