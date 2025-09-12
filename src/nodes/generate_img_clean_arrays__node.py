from src.node import Node
import numpy as np


class GenerateImgCleanArrays(Node):
    def process(self, data):
        img_array = data["img_array"]

        data["background_img"] = np.zeros_like(img_array)
        data["object_img"] = np.zeros_like(img_array)

        return data