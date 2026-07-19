import numpy as np

from .cell import Cell


class Cloud:

    def __init__(
        self,
        cells=64,
        dim=512,
        coupling=0.12,
        avg_degree=6
    ):

        self.dim = dim

        self.cells = [
            Cell(
                i,
                dim=dim
            )
            for i in range(cells)
        ]


        self.step_count = 0

        self.last_kind = "none"

        self.coupling = coupling


        # 简单邻接关系
        self.edges = []

        rng = np.random.default_rng(42)

        for i in range(cells):

            others = [
                x for x in range(cells)
                if x != i
            ]

            neighbors = rng.choice(
                others,
                size=min(avg_degree, len(others)),
                replace=False
            )

            for j in neighbors:

                if i < j:

                    self.edges.append(
                        (i, j)
                    )


        self.edges = np.array(
            self.edges
        )


    def receive(self, stimulus):

        """
        接收外部 IO field

        支持:
        1. Stimulus对象
        2. numpy field
        """

        # 判断输入类型

        if hasattr(stimulus, "vector"):

            vector = stimulus.vector

            self.last_kind = getattr(
                stimulus,
                "kind",
                "unknown"
            )

            strength = getattr(
                stimulus,
                "intensity",
                1.0
            )

        else:

            # 直接 numpy array

            vector = stimulus

            self.last_kind = "byte"

            strength = 1.0



        for cell in self.cells:

            cell.stimulate(
                vector,
                strength
            )


    def step(self):

        """
        CIMA0内部动力
        """

        # 局部耦合

        forces = np.zeros(
            len(self.cells)
        )


        if len(self.edges)>0:

            for a,b in self.edges:

                ca = self.cells[a]
                cb = self.cells[b]


                diff = (
                    ca.x
                    -
                    cb.x
                )


                f = (
                    self.coupling
                    *
                    np.sin(diff)
                )


                forces[a]+=f
                forces[b]-=f



        # 每个cell自身演化

        for i,c in enumerate(self.cells):

            c.step(
                forces[i]
                if i < len(forces)
                else 0
            )


        self.step_count += 1




    def get_field(self):

        """
        提供给器官/IO的场状态

        不改变动力
        """

        x = []
        v = []


        for c in self.cells:

            if hasattr(c,"x"):

                x.append(
                    c.x
                )

            if hasattr(c,"v"):

                v.append(
                    c.v
                )


        return np.array(
            x + v,
            dtype=np.float32
        )




    def snapshot(self):

        """
        Observer读取
        """

        xs = []
        vs = []


        activity = 0


        for c in self.cells:

            if hasattr(c,"x"):

                xs.append(
                    c.x
                )

            if hasattr(c,"v"):

                vs.append(
                    c.v
                )


            if getattr(
                c,
                "activity",
                0
            ) > 0:

                activity += 1



        phase_std = 0.0


        if len(xs)>0:

            phases = np.arctan2(
                np.array(vs),
                np.array(xs)
            )

            phase_std = np.std(
                phases
            )



        return {

            "step":
            self.step_count,


            "phase_std":
            round(
                float(phase_std),
                5
            ),


            "avg_x":
            round(
                float(np.mean(xs))
                if xs else 0,
                5
            ),


            "cells":
            len(self.cells),


            "activity":
            activity
        }