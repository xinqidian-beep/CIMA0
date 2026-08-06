import cv2
import numpy as np

from core.internal_dynamics import InternalDynamics
from core.internal_dynamics_observer import InternalDynamicsObserver
from core.compute_system import ComputeSystem
from core.display_io import DisplayIO


from core.camera_planet import CameraPlanet
from core.camera_io import CameraIO
from core.camera_observer import CameraObserver


from archive.planet import Planet
from core.clip_region import ClipRegion


from core.camera_compute import CameraComputeSystem


import time
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
    print("CIMA0 Phase4 Internal Clock Loop")
    print("")
    print("ESC : exit")
    print("=" * 60)



    #
    # internal world
    #

    planet = Planet()

    clip = ClipRegion(
        64,
        64,
        3
    )


    internal = InternalDynamics(
        planet,
        clip
    )



    #
    # camera input
    #

    camera = cv2.VideoCapture(0)


    camera_planet = CameraPlanet()

    camera_io = CameraIO()

    camera_observer = CameraObserver()

    camera_compute = CameraComputeSystem()



    #
    # observers
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
    # independent module clocks
    #

    camera_clock = LocalClock(
        1 / 30
    )


    planet_clock = LocalClock(
        0.01
    )


    observer_clock = LocalClock(
        0.1
    )


    display_clock = LocalClock(
        1 / 60
    )




    if not camera.isOpened():

        print(
            "Camera open failed"
        )
        
    while True:


        #
        # camera own time
        #

        if camera_clock.due():

            ret, frame = camera.read()

            if ret:

                camera_state = camera_planet.step_planet(
                    frame
                )


                data = camera_io.encode(
                    camera_state["frame"]
                )


                data = camera_observer.observe(
                    data,
                    camera_compute.step()
                )


                internal.receive(
                    data
                )



        #
        # planet/internal own time
        #

        if planet_clock.due():

            internal.step()



        #
        # observer own time
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
        # display own time
        #

        if display_clock.due():

            snapshot = internal.snapshot()


            frame_out = display.encode(
                snapshot["clip"]
            )


            if frame_out is not None:

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