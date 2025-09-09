from src.nodes.train_kmeans__node import TrainKMeans
from src.nodes.pixel_formater__node import PixelFormater
from PIL import Image

class Model:
    def __init__(self):
        self.controller = None
        self.pixel_rgbs = []
        self.groups = []
    
    def set_controller(self, controller):
        self.controller = controller
    

    def save_pixel(self, pixel_rgb, group):
        pixel_formatter = PixelFormater()
        list_pixel_rgb = pixel_formatter.run({ 'pixel_rgb': pixel_rgb })
        self.pixel_rgbs.append(list_pixel_rgb)

        self.groups.append(group)
        print(f"Model:\nPixels: {self.pixel_rgbs}\nGroups: {self.groups}")
    
    def separate_object(self, image_path):
        data = {
            "X": self.pixel_rgbs,
            "y": self.groups
        }

        train_kmeans = TrainKMeans()
        kmeans = train_kmeans.run(data, True)['kmeans']

        image = Image.open(image_path)
        image = image.convert("RGB")
        pixels = image.load()
        width, height = image.size

        pixel_formatter = PixelFormater()
        # Run image.

        y=0
        while y < height:
            x=0
            while x < width:
                form_pixel = pixel_formatter.run({ 'pixel_rgb': pixels[x, y] }),
                group = kmeans.predict(form_pixel)

                print(group)

                x+=1
            y+=1