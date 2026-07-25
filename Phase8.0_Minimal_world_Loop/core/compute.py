from core.cell import Cell


class ComputeSystem:
    """
    Compute system.

    Only advances dynamics.

    Does not know:
        observer
        user
        meaning
    """

    def __init__(self, cells):
        self.cells = cells
        self.time = 0


    def step(self):

        for cell in self.cells:
            cell.step()

        self.time += 1


    def get_cells(self):

        return self.cells