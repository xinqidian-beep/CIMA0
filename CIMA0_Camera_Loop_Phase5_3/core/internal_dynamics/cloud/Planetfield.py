import numpy as np


class PlanetField:
    """
    CIMA0 Phase5_3

    The one true dynamical core.

    Same equations as archive/planet.py (four-neighbor
    diffusion + a small sin nonlinearity), rewritten as
    vectorized numpy slicing instead of a python double
    loop, so it can run once per camera frame without
    stalling the main loop. The math is unchanged: every
    read in a step comes from a copy of the previous state
    ("old"), so vectorizing does not change the result.

    step() is unconditional. It is never budget-gated and
    never skipped. That is the whole point: nothing except
    this organ can be "the thing that keeps going even with
    no camera, no compute allocation, no observer reading
    it at all". CloudField's problem, several iterations
    ago, was that it had no source of persistence of its
    own — every property it had came from outside (receive)
    or shrank towards nothing (decay). This organ is built
    the other way around: state evolves from itself first,
    and external input only perturbs an already-running
    process.

    Knows only:
        state
        local interaction
        evolution

    Does NOT know:
        camera byte format
        compute budgets
        display
    """

    def __init__(
        self,
        size=128,
        diffusion_rate=0.05,
        nonlinear_rate=0.001,
        impact_scale=0.02
    ):

        self.size = size

        self.diffusion_rate = diffusion_rate

        self.nonlinear_rate = nonlinear_rate

        # how strongly one incoming camera frame can perturb
        # the field per receive() call. Kept small on purpose:
        # camera input is meant to be an impact on an already
        # -running process, not a replacement for it. This
        # number is a placeholder, not a derived constant —
        # flagging it the same way capacity/threshold constants
        # were flagged earlier in this project.
        self.impact_scale = impact_scale

        self.state = np.random.randn(
            size,
            size
        ).astype(np.float32) * 0.01



    #
    # external perturbation only — never a reset, never an
    # overwrite. The field keeps whatever it already is and
    # this just nudges it.
    #

    def receive(
        self,
        raw
    ):

        if raw is None:

            return


        try:

            data = np.frombuffer(
                raw["bytes"],
                dtype=np.dtype(raw["dtype"])
            )

            data = data.reshape(
                raw["shape"]
            )

        except Exception:

            return



        if data.ndim == 3:

            gray = data.astype(np.float32).mean(axis=2)

        elif data.ndim == 2:

            gray = data.astype(np.float32)

        else:

            return



        impact = self._resize(
            gray,
            self.size,
            self.size
        )


        # map raw byte-ish magnitude down into a small
        # perturbation range instead of dumping ~0-255
        # straight into a field that is meant to stay near
        # unit scale.
        impact = (impact / 255.0 - 0.5) * self.impact_scale


        self.state += impact



    def _resize(
        self,
        array,
        out_h,
        out_w
    ):

        in_h, in_w = array.shape

        ys = np.linspace(
            0,
            in_h - 1,
            out_h
        ).astype(np.int32)

        xs = np.linspace(
            0,
            in_w - 1,
            out_w
        ).astype(np.int32)

        return array[np.ix_(ys, xs)]



    #
    # unconditional evolution. No budget parameter anywhere
    # in this method on purpose — see class docstring.
    #

    def step(
        self
    ):

        old = self.state.copy()


        neighbor = (
            old[2:, 1:-1] +
            old[:-2, 1:-1] +
            old[1:-1, 2:] +
            old[1:-1, :-2]
        ) / 4.0


        self.state[1:-1, 1:-1] += (
            self.diffusion_rate *
            (neighbor - old[1:-1, 1:-1])
        )

        self.state[1:-1, 1:-1] += (
            self.nonlinear_rate *
            np.sin(old[1:-1, 1:-1])
        )



    def snapshot(
        self
    ):

        return self.state.copy()


    #
    # intentionally no request_compute / execute_compute.
    #
    # step() above always runs in full, every call, so
    # there is nothing here for a compute budget to gate.
    # InternalDynamics.execute_compute() already skips any
    # organ without this method (hasattr check), so simply
    # not defining it is enough to opt this organ out of
    # the compute-budget economy entirely, rather than
    # defining a no-op that would be misleading about what
    # actually happens.
    #