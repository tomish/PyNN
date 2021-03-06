from registry import register

from pyNN.random import RandomDistribution as rnd


@register()
def issue274(sim):
    sim.setup(min_delay=0.5)

    p0 = sim.Population(13, sim.IF_cond_exp())
    p1 = sim.Population(1000, sim.IF_cond_exp())
    p2 = sim.Population(252, sim.IF_cond_exp())

    connector = sim.DistanceDependentProbabilityConnector("exp(-d/100)")

    prj = sim.Projection(p1, p2, connector)

    w_dist = rnd("uniform", [1e-6, 2e-6])
    delay_dist = rnd("uniform", [0.5, 1.0])
    prj.set(weight=w_dist, delay=delay_dist)


if __name__ == '__main__':
    from pyNN.utility import get_simulator
    sim, args = get_simulator()
    issue274(sim)
