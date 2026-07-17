import time


from input.bus import InputBus  # 注意：文件名统一为小写 bus.py（原 Bus.py，Windows不区分大小写掩盖了这个问题，Linux/云端会报 ModuleNotFoundError）

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