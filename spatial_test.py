import numpy as np

from organs.oscillator_organ import OscillatorOrgan
from field.spatial_field import SpatialField


np.random.seed(42)



NUM=64



organs=[
    OscillatorOrgan(
        f"organ_{i}",
        16
    )
    for i in range(NUM)
]



field=SpatialField(
    organs,
    radius=1.0,
    coupling=0.0001
)



for step in range(200000):


    field.step()


    for o in organs:
        o.step()



    if step % 20000==0:


        distances=[]


        for i in range(NUM):

            for j in range(i+1,NUM):

                d=np.linalg.norm(
                    organs[i].position-
                    organs[j].position
                )

                distances.append(d)



        print(
            {
            "step":step,

            "mean_distance":
            np.mean(distances),

            "close_pairs":
            sum(
                d<1.0
                for d in distances
            )
            }
        )



print("DONE")