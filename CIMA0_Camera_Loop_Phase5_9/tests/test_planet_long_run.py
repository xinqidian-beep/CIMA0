import os
import sys
import time
import numpy as np


#
# allow project import
#

ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(
    0,
    ROOT
)


from core.internal_dynamics.cloud.Planetfield import PlanetField
from archive.planet import Planet



LOG_PATH = r"C:\temp\planet_long_run.log"


TOTAL_STEPS = 10000

OBSERVE_INTERVAL = 100



def safe_energy(
    state
):
    if state is None:
        return 0.0

    array = np.asarray(
        state
    )

    if array.size == 0:
        return 0.0

    return float(
        np.mean(
            np.square(
                array
            )
        )
    )



def safe_variance(
    state
):
    if state is None:
        return 0.0

    array = np.asarray(
        state
    )

    if array.size == 0:
        return 0.0

    return float(
        np.var(
            array
        )
    )



def write_log(
    text
):

    with open(
        LOG_PATH,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            text
            +
            "\n"
        )



def main():


    os.makedirs(
        os.path.dirname(
            LOG_PATH
        ),
        exist_ok=True
    )


    #
    # clean old observation
    #

    if os.path.exists(
        LOG_PATH
    ):

        os.remove(
            LOG_PATH
        )


    write_log(
        "CIMA0 Planet long run observation"
    )

    write_log(
        "steps=%d interval=%d"
        %
        (
            TOTAL_STEPS,
            OBSERVE_INTERVAL
        )
    )



    #
    # create endogenous planet
    #

    planet_rule = Planet(
        size=128
    )


    planet_field = PlanetField(
        planet_rule
    )


    start = time.time()


    for step in range(
        TOTAL_STEPS
    ):


        #
        # internal evolution only
        #

        planet_field.step()



        #
        # observer window
        #

        if (
            step %
            OBSERVE_INTERVAL
            ==
            0
        ):


            snapshot = (
                planet_field.snapshot()
            )


            energy = safe_energy(
                snapshot
            )


            variance = safe_variance(
                snapshot
            )


            glimpse = (
                planet_field.glimpse()
            )


            if glimpse is None:

                glimpse_info = "None"

            else:

                observation = (
                    glimpse.get(
                        "observation",
                        {}
                    )
                )

                glimpse_info = str(
                    {
                        "level":
                            observation.get(
                                "level"
                            ),

                        "region":
                            observation.get(
                                "region"
                            ),

                        "age":
                            observation.get(
                                "age"
                            )
                    }
                )


            line = (
                "step=%d "
                "energy=%f "
                "variance=%f "
                "glimpse=%s"
                %
                (
                    step,
                    energy,
                    variance,
                    glimpse_info
                )
            )


            print(
                line
            )


            write_log(
                line
            )



    elapsed = (
        time.time()
        -
        start
    )


    finish = (
        "finished "
        "steps=%d "
        "seconds=%f"
        %
        (
            TOTAL_STEPS,
            elapsed
        )
    )


    print(
        finish
    )


    write_log(
        finish
    )



if __name__ == "__main__":

    main()