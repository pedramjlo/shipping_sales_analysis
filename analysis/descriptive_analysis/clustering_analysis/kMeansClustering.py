import numpy as np

class KMeans:
    def __init__(self, data, n_clusters=3, max_iter=100, tol=1e-4, random_state=None):
        self.data = np.array(data)  # Ensure data is a NumPy array
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tol = tol
        self.random_state = random_state
        self.centroids = None
        self.labels_ = None

    def fit(self):
        np.random.seed(self.random_state)

        # Step 1: Initialize centroids by selecting K random data points
        random_idx = np.random.permutation(len(self.data))[:self.n_clusters]
        self.centroids = self.data[random_idx]

        for i in range(self.max_iter):
            # Step 2: Assign each point to the nearest centroid
            distances = self._compute_distances(self.data)
            labels = np.argmin(distances, axis=1)

            # Step 3: Compute new centroids
            new_centroids = np.array([
                self.data[labels == k].mean(axis=0) if np.any(labels == k) else self.centroids[k]
                for k in range(self.n_clusters)
            ])

            # Step 4: Check for convergence
            shift = np.linalg.norm(self.centroids - new_centroids)
            if shift < self.tol:
                break

            self.centroids = new_centroids

        self.labels_ = labels

    def predict(self, X=None):
        X = self.data if X is None else np.array(X)
        distances = self._compute_distances(X)
        return np.argmin(distances, axis=1)

    def transform(self, X=None):
        X = self.data if X is None else np.array(X)
        return self._compute_distances(X)

    def fit_transform(self):
        self.fit()
        return self.transform()

    def _compute_distances(self, X):
        return np.linalg.norm(X[:, np.newaxis] - self.centroids, axis=2)
