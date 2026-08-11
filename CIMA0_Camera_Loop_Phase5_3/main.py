import cv2


from core.camera_planet import CameraPlanet
from core.internal_dynamics import InternalDynamics
from core.internal_dynamics_observer import InternalDynamicsObserver
from core.display_io import DisplayIO

from core.compute_system import ComputeSystem

from core.internal_dynamics.cloud.cloud_field import CloudField



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



    while True:



        #
        # camera packet
        #

        ret, frame = cap.read()


        if not ret:

            continue



        packet = camera_planet.step(
            frame
        )


        if packet is None:

            continue



        #
        # input
        #

        dynamics.receive(
            packet
        )



        #
        # compute request
        #

        request = dynamics.request_compute()



        #
        # allocation
        #

        allocation = compute.allocate(
            request
        )



        #
        # execute budget
        #

        dynamics.execute_compute(
            allocation
        )



        #
        # local evolution
        #

        dynamics.step()



        #
        # snapshot
        #

        snapshot = dynamics.snapshot()



        #
        # observer activity
        #

        request = observer.observe(
            snapshot                       
        )
        
        
        
        #
        # compute allocation
        #

        allocation = compute.allocate(
            request
        )
        
        #
        # sparse read
        #


        read_state = observer.read(
            snapshot,
            allocation
        )



        #
        # internal state -> IO byte packet
        #

        display_packet = observer.encode_field(
            read_state,
            source="internal"
        )
        
        print(
            "[DISPLAY PACKET]",
            None if display_packet is None
            else display_packet.keys()
        )
        
        #
        # display only receives field packet
        #

        frame_out = display.encode(
            display_packet
        )
        
        if frame_out is not None:

            cv2.imshow(
                "CIMA0",
                frame_out
            )
            
        key = cv2.waitKey(1) & 0xff


        if key == 27:

            break



if __name__ == "__main__":

    main()