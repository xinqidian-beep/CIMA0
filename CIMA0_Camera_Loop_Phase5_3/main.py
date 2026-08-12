import cv2


from core.terminal.camera import (
    CameraPlanet,
    CameraObserver
)
from core.internal_dynamics import InternalDynamics
from core.internal_dynamics import InternalDynamicsObserver
from core.display_io import DisplayIO

from core.compute_system import ComputeSystem

from core.internal_dynamics.cloud import CloudField



def main():


    print("=" * 60)
    print("CIMA0 Phase5_3 Internal Dynamics Loop")
    print("=" * 60)



    #
    # dynamics container
    #

    dynamics = InternalDynamics()



    #
    # cloud organ
    #

    cloud = CloudField(
        capacity=32
    )


    dynamics.register(
        "cloud",
        cloud
    )



    #
    # compute
    #

    compute = ComputeSystem()



    #
    # observer
    #

    observer = InternalDynamicsObserver()



    #
    # display
    #

    display = DisplayIO()



    #
    # camera
    #

    cap = cv2.VideoCapture(0)


    if not cap.isOpened():

        print(
            "camera open failed"
        )

        return



    camera_planet = CameraPlanet()
    camera_observer = CameraObserver()



    while True:

        key = cv2.waitKey(1) & 0xff

        if key == 27:
            break


        ret, frame = cap.read()

        if not ret:
            continue


        packet = camera_planet.step(frame)


        #
        # visual path
        #

        camera_display_packet = camera_observer.observe(
            packet,
            budget=5000
        )


        frame_out = display.encode(
            camera_display_packet
        )


        if frame_out is not None:

            cv2.imshow(
                "CIMA0",
                frame_out
            )


        #
        # internal path
        #

        dynamics.receive(packet)

        request = dynamics.request_compute()

        allocation = compute.allocate(request)

        dynamics.execute_compute(allocation)

        dynamics.step()



if __name__ == "__main__":

    main()