import time

from core.cloud import Cloud



print("================")
print(" CIMA-0 START ")
print("================")


cloud=Cloud(
    size=128
)


step=0


while True:


    cloud.step()


    if step%100==0:

        print(
            step,
            cloud.statistics()
            "coherence=",
            cloud.phase_coherence()
        )


    step+=1

    time.sleep(0.01)