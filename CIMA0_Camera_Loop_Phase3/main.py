from archive.planet import Planet
from archive.observer import Observer
from archive.compute import ComputeSystem
from archive.io import InputField

from hardware.usb_camera import USBCamera
from core.clip_region import ClipRegion


CLIP_WEIGHT = r"C:\CIMA0\models\open_clip_pytorch_model.bin"


def main():

    #
    # Hardware
    #
    camera = USBCamera()


    #
    # Internal structure
    #
    clip = ClipRegion(
        CLIP_WEIGHT
    )


    #
    # Internal Dynamics
    #
    planet = Planet(
        clip_region=clip
    )


    #
    # Observation
    #
    observer = Observer()


    #
    # Computation resource
    #
    compute = ComputeSystem()


    #
    # IO boundary
    #
    io = InputField()



    print("=" * 60)
    print("CIMA0 Camera Loop Phase3")
    print("camera -> planet -> observer -> display")
    print("ClipRegion inside Internal Dynamics")
    print("=" * 60)



    try:

        while True:


            #
            # external state
            #
            frame = camera.read()


            if frame is None:
                continue



            #
            # IO only transfers
            #
            external_state = io.receive(
                frame
            )



            #
            # Internal Dynamics
            #
            planet.update(
                external_state
            )



            #
            # Compute resource recovery
            #
            compute.step()



            #
            # Observer reads state
            #
            snapshot = observer.read(
                planet
            )


            #
            # Temporary output
            #
            print(snapshot)



    except KeyboardInterrupt:

        print("\nStopping...")


    finally:

        camera.release()



if __name__ == "__main__":

    main()