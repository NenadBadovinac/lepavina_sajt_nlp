from sklearn import datasets
from matplotlib import pyplot as plt

X, y = datasets.make_blobs(
    n_samples=150, n_features=2, centers=2, cluster_std=1.05, random_state=2
    )

plt.scatter(X[:, 0], X[:, 1], marker="o", c=y)

print(y)

plt.show()
