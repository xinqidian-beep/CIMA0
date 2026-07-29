from core.planet import PlanetEngine


p = PlanetEngine()


for i in range(100000):

    p.step()

    if i % 1000 == 0:

        print(
            i,
            p.sample()
        )