import time


from input.bus import InputBus

from core.cloud import Cloud

from core.memory import Memory




def main():


    print(
        "===================="
    )

    print(
        " CIMA0 v0.1 Runtime "
    )

    print(
        "===================="
    )



    bus=InputBus()

    cloud=Cloud(
        cells=128
    )

    memory=Memory()



    while True:



        stimulus=bus.poll()



        if stimulus:


            cloud.receive(
                stimulus
            )


        cloud.step()



        state=cloud.snapshot()



        memory.record(
            state
        )



        print(
            state
        )



        time.sleep(
            0.1
        )





if __name__=="__main__":

    main()