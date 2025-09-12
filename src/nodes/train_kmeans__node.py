from src.node import Node
from sklearn.cluster import KMeans

class TrainKMeans(Node):
    def process(self, data):
        caracteristics = data["X"]
        classes = data["y"]

        kmeans = KMeans(n_clusters=2)
        kmeans.fit(caracteristics, classes)
        data["kmeans"] = kmeans

        return data