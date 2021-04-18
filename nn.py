from numpy import array, zeros, ones, exp, average, newaxis
from numpy.random import randn


def A(x):
    return 1 / (1 + exp(-x))


X = array([
    [0, 0, 1, 0, 1, 0],
    [1, 1, 0, 1, 0, 0],
    [1, 0, 1, 0, 0, 0],
    [1, 1, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 0],
    [0, 0, 0, 1, 1, 0],
    [1, 0, 1, 0, 1, 0],
    [1, 1, 0, 1, 0, 1]
])


Y = array([[1, 0, 1, 0, 1, 0, 0, 0]]).T


class nn:
    def __init__(self, *shape):
        self.edges = array(list(map(randn, shape[:-1], shape[1:])), dtype=object)


    def forward(self, x):
        net = [ x ]

        for i, edges in enumerate(self.edges):
            net.append(A(net[i] @ edges))

        return net


    def back(self, net, y):
        loss = net[-1] - y
        yield average(net[-2][:, :, newaxis] * loss[:, newaxis, :], axis=0)

        for i, layer in reversed(list(enumerate(net))[1:-1]):

            loss = layer * (1 - layer) * (loss @ self.edges[i].T)
            prev = net[i - 1]

            yield average(prev[:, :, newaxis] * loss[:, newaxis, :], axis=0)


    def fit(self, x, y, time):

        for i in range(time):
          self.edges += -0.5 * array(list(reversed(list(self.back(self.forward(x), y)))), dtype=object)


    def predict(self, x):
        return self.forward(x)[-1]
