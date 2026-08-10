import cv2
import time


from core.internal_dynamics import InternalDynamics
from core.internal_dynamics_observer import InternalDynamicsObserver
from core.display_io import DisplayIO

from core.camera_planet import CameraPlanet
from core.clip_field import CLIPField

from archive.planet import Planet


CLIP_WEIGHT = r"C:\CIMA0\models\open_clip_pytorch_model.bin"



class LocalClock:

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


    print("="*60)
    print("CIMA0 minimal packet loop")
    print("="*60)



    #
    # world
    #

    dynamics = InternalDynamics()



    planet = Planet()



    visual = CLIPField(
        weight_path=CLIP_WEIGHT,
        device="cpu"
    )



    dynamics.register(
        "planet",
        planet
    )


    dynamics.register(
        "visual",
        visual
    )



    #
    # camera
    #

    cap = cv2.VideoCapture(0)


    camera_planet = CameraPlanet()



    #
    # observer
    #

    observer = InternalDynamicsObserver()



    display = DisplayIO()



    #
    # clocks
    #

    camera_clock = LocalClock(
        1/30
    )


    step_clock = LocalClock(
        0.01
    )


    display_clock = LocalClock(
        1/10
    )



    while True:


        #
        # camera packet
        #

        if camera_clock.due():


            ret, frame = cap.read()


            if ret:


                camera_planet.step(
                    frame
                )


                packet = camera_planet.state()
                
                print(
                    packet["shape"],
                    packet["dtype"],
                    len(packet["bytes"])
                )



                print(
                    "[CAMERA]",
                    packet["shape"],
                    packet["dtype"],
                    len(packet["bytes"])
                )



                dynamics.receive(
                    packet
                )



        #
        # internal
        #

        if step_clock.due():


            dynamics.step()



        #
        # observer -> packet
        #

        if display_clock.due():


            display_packet = camera_planet.state()



            frame_out = display.encode(
                display_packet
            )


            if frame_out is not None:

                cv2.imshow(
                    "CIMA0",
                    frame_out
                )




        if cv2.waitKey(1)&0xff == 27:

            break




    cap.release()

    cv2.destroyAllWindows()




if __name__ == "__main__":

    main()