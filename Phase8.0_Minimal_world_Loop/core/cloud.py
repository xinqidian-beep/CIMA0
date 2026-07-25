class CloudCollision:
    """
    External perturbation.

    No control.
    No target optimization.

    Just collision.
    """

    def __init__(self):
        self.used = False


    def collide(self, cell, value):

        if self.used:
            return False

        cell.local_perturb(value)

        self.used = True

        return True