import numpy as np
from scipy.linalg import norm


class FCM:
    def __init__(self, n_clusters=4, max_iter=100, m=2, error=1e-6):
        super().__init__()
        self.u, self.centers = None, None
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.m = m
        self.error = error

    def fit(self, X):
        N = X.shape[0]
        C = self.n_clusters
        centers = []

        u = np.random.dirichlet(np.ones(C), size=N)

        iteration = 0
        while iteration < self.max_iter:
            u2 = u.copy()

            centers = self.next_centers(X, u)
            u = self.next_u(X, centers)
            iteration += 1

            # Stopping rule
            if norm(u - u2) < self.error:
                break

        self.u = u
        self.centers = centers
        return centers

    def next_centers(self, X, u):
        um = u ** self.m
        return (X.T @ um / np.sum(um, axis=0)).transpose()

    def next_u(self, X, centers):
        return np.apply_along_axis(self._predict, 1, X, centers)

    def _predict(self, X, centers):
        power = float(2 / (self.m - 1))
        temp = norm(X - centers, axis=1) ** power
        denominator_ = temp.reshape((1, -1)).repeat(temp.shape[0], axis=0)
        denominator_ = temp[:, None] / denominator_

        return 1 / denominator_.sum(1)

    def predict(self, X):
        if len(X.shape) == 1:
            X = np.expand_dims(X, axis=0)

        u = np.apply_along_axis(self._predict, 1, X, self.centers)
        return np.argmax(u)
