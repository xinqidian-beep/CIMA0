import sys
import os
import numpy as np


# 保证可以导入 core
ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(ROOT)


from core.oscillator import Oscillator



# ==========================
# experiment parameters
# ==========================

STEPS = 100_000

WINDOW = 20_000


INITIAL_AMPLITUDES = [
    0.01,
    0.1,
    0.5,
    1.0,
    1.5,
    2.0,
    3.0
]



def run_case(x0):

    organ = Oscillator(
        x=x0,
        v=0.0,
        

        

        omega=1.0,
        mu=0.6,

        dt=0.02

        
    )


    radius_history = []


    for step in range(STEPS):

        organ.step()


        if step >= STEPS - WINDOW:

            r = np.sqrt(
                organ.x * organ.x
                +
                organ.v * organ.v
            )

            radius_history.append(r)



    radius_history = np.array(
        radius_history
    )


    return {

        "x0": x0,

        "final_x": organ.x,

        "final_v": organ.v,

        "mean_radius":
            float(
                np.mean(radius_history)
            ),

        "std_radius":
            float(
                np.std(radius_history)
            ),

        "min_radius":
            float(
                np.min(radius_history)
            ),

        "max_radius":
            float(
                np.max(radius_history)
            )
    }




def classify(result):

    r = result["mean_radius"]
    std = result["std_radius"]


    if r < 1e-3:
        return "origin"


    if std / r < 0.05:
        return "stable_orbit"


    return "complex"



def main():

    print(
        "=== Phase5 Fast Dynamics Sweep ==="
    )


    results = []


    for x0 in INITIAL_AMPLITUDES:

        print(
            "\nRunning x0 =",
            x0
        )


        result = run_case(x0)

        result["class"] = classify(
            result
        )

        results.append(result)


        print(result)



    print(
        "\n=== SUMMARY ==="
    )


    for r in results:

        print(
            f"x0={r['x0']:>4} "
            f""
            f"radius={r['mean_radius']:.6f} "
            f""
            f"std={r['std_radius']:.6f} "
            f""
            f"{r['class']}"
        )



if __name__ == "__main__":
    main()