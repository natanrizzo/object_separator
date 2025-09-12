from src.node import Node
from PIL import Image
import os


class SaveFile(Node):
    def process(self, data):
        background_img = data["background_img"]
        object_img = data["object_img"]
        
        os.makedirs("output", exist_ok=True)

        Image.fromarray(background_img).save("output/background.jpeg")
        Image.fromarray(object_img).save("output/object.jpeg")