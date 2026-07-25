from core.cell import Cell
from core.environment import Environment


class World:


    def __init__(self, n):

        self.time = 0

        self.environment = Environment(n)


        self.cells = [
            Cell(i)
            for i in range(n)
        ]



    def step(self):

        """
        世界没有逻辑

        只是让每个个体活一次
        """

        for cell in self.cells:

            cell.step(
                self.environment
            )


        self.environment.decay()


        self.time += 1



    def sample(self, ids):

        return [
            self.cells[i].state()
            for i in ids
        ]