class Cloud:

    def __init__(self, center, radius, strength):
        self.center = center
        self.radius = radius
        self.strength = strength


    def contact(self):

        result = {}

        for i in range(
            self.center-self.radius,
            self.center+self.radius+1
        ):
            if i >= 0:
                result[i] = self.strength

        return result