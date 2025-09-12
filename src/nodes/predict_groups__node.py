from src.node import Node


class PredictGroups(Node):
    def process(self, data):
        flat_pixels = data["flat_pixels"]
        height = data["height"]
        width = data["width"]
        kmeans = data["kmeans"]
        
        groups = kmeans.predict(flat_pixels)
        mask = groups.reshape(height, width)

        data["mask"] = mask

        return data
