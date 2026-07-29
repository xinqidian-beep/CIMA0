from core.planet import KinEngine
from core.cloud import CloudField
from core.input_field import IOField
from core.observer import Observer
from core.compute import ComputeSystem



def main():

    print(
        "=== CIMA0 Core ==="
    )


    kin = KinEngine()

    cloud = CloudField(
        cloud_size=64
    )

    io = IOField()

    observer = Observer()

    compute = ComputeSystem()



    for step in range(100000):


        #
        # IO receives raw bytes
        #

        if step % 100 == 0:

            io.receive_io_ephemeral_bytes(
                bytes(
                    [step % 256]
                )
            )


            #
            # byte existence becomes
            # disturbance only
            #

            byte_data = (
                io.project_io_ephemeral_bytes()
            )


            if len(byte_data):

                cloud.receive_cloud_ephemeral_disturbance(
                    byte_data[0] - 128
                )



        #
        # cloud evolves itself
        #

        cloud.step_cloud_dynamics()



        #
        # kinetic system evolves itself
        #

        kin.step_kin_dynamics()



        #
        # observer samples
        #

        observer.sample_ephemeral_state(
            kin.kin_x
        )


        result = (
            observer.evaluate_ephemeral_raised()
        )


        #
        # compute reacts only to load
        #

        if result["raised"]:

            compute.receive_compute_ephemeral_load(
                0.1
            )


        compute.step_compute_dynamics()



        if step % 1000 == 0:

            print(
                {
                    "step": step,
                    "kin_x": round(
                        kin.kin_x,
                        4
                    ),
                    "cloud_act": float(
                        cloud.cloud_state_act.sum()
                    ),
                    "raised":
                        result["raised"],
                    "compute":
                        compute.compute_capacity
                }
            )



if __name__ == "__main__":

    main()