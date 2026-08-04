import cv2
import time


from core.internal_dynamics import InternalDynamics
from core.internal_dynamics_observer import InternalDynamicsObserver
from core.compute_system import ComputeSystem
from core.display_io import DisplayIO


from core.camera_planet import CameraPlanet
from core.camera_io import CameraIO
from core.camera_observer import CameraObserver


from archive.planet import Planet
from core.clip_region import ClipRegion


CLIP_WEIGHT = r"C:\CIMA0\models\open_clip_pytorch_model.bin"



def main():

    print("=" * 60)
    print("CIMA0 Internal Dynamics Loop")
    print("")
    print("ESC : exit")
    print("=" * 60)



    #
    # internal world
    #

    planet = Planet()


    clip = ClipRegion(
        CLIP_WEIGHT
    )


    internal = InternalDynamics(
        planet,
        clip
    )



    #
    # camera chain
    #

    camera = cv2.VideoCapture(0)


    camera_planet = CameraPlanet()

    camera_io = CameraIO()

    camera_observer = CameraObserver()



    #
    # observer
    #

    observer = InternalDynamicsObserver()



    #
    # compute
    #

    compute = ComputeSystem(
        capacity=100
    )


    #
    # camera compute
    #
    # camera自身资源状态
    #

    from core.camera_compute import CameraComputeSystem

    camera_compute = CameraComputeSystem()



    #
    # output
    #

    display = DisplayIO()



    if not camera.isOpened():

        print(
            "Camera open failed"
        )



    while True:


        #
        # ============================
        # camera input chain
        # ============================
        #

        ret, frame = camera.read()


        if ret:


            #
            # hardware fact
            #

            camera_state = camera_planet.step_planet(
                frame
            )


            #
            # BGR -> bytes
            #

            data = camera_io.encode(
                camera_state["frame"]
            )


            #
            # camera computation state
            #

            camera_state_compute = camera_compute.step()



            #
            # sparse focus update
            #

            data = camera_observer.observe(
                data,
                camera_state_compute
            )


            #
            # byte stream enters internal
            #

            internal.receive(
                data
            )



        #
        # ============================
        # internal dynamics
        # ============================
        #

        internal.step()



        #
        # snapshot
        #

        snapshot = internal.snapshot()



        #
        # readonly observation
        #

        request = observer.observe(
            snapshot
        )



        #
        # resource allocation
        #

        allocation = compute.allocate(
            request
        )



        #
        # sparse read
        #

        observed = observer.read(
            snapshot,
            allocation
        )



        #
        # display
        #
        # only once
        #

        frame_out = display.encode(
            observed["planet"]["state"]
        )



        if frame_out is not None:

            cv2.imshow(
                "CIMA0",
                frame_out
            )



        #
        # ESC
        #

        key = cv2.waitKey(1) & 0xff


        if key == 27:

            print(
                "CIMA0 stopped"
            )

            break



        time.sleep(
            0.03
        )



    camera.release()

    cv2.destroyAllWindows()



if __name__ == "__main__":

    main()