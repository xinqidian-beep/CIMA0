from core.cloud import Cloud
import time


cloud=Cloud(1000)


while True:

    cloud.step(
        input_field=0.1
    )


    print(
        cloud.cells[0].phase,
        cloud.cells[0].memory
    )


    time.sleep(0.05)