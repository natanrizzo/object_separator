from src.node import Node
from PIL import Image
import numpy as np

class NormalizeImgArray(Node):
    def process(self, data):
        image_path = data["image_path"]
        image = Image.open(image_path).convert("RGB")
        img_array = np.array(image)
        h, w, c = img_array.shape
        flat_pixels = img_array.reshape(-1, 3)
        
        data["img_array"] = img_array
        data["height"] = h
        data["width"] = w
        data["flat_pixels"] = flat_pixels

        return data