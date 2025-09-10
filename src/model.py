from src.nodes.train_kmeans__node import TrainKMeans
from src.nodes.pixel_formater__node import PixelFormater
from PIL import Image
import numpy as np
import os

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
        kmeans = train_kmeans.run(data)['kmeans']

        image = Image.open(image_path).convert("RGB")
        ''' Old code
        pixels = image.load()
        width, height = image.size

        pixel_formatter = PixelFormater()
        # Run image.
        
        img_shape = (height, width, 3)

        background_img=np.zeros(shape=img_shape, dtype=np.uint8)
        object_img=np.zeros(shape=img_shape, dtype=np.uint8)

        y=0
        while y < height:
            x=0
            while x < width:
                form_pixel = pixel_formatter.run({ 'pixel_rgb': pixels[x, y] }),
                group = kmeans.predict(form_pixel)
                if (group == 0): # Background
                    background_img[y, x] = pixels[x, y]
                    object_img[y, x] = (0, 0, 255)
                else: # Object
                    background_img[y, x] = (0, 0, 255)
                    object_img[y, x] = pixels[x, y]
                x+=1
            y+=1
        '''
        
        img_array = np.array(image)
        h, w, c = img_array.shape

        flat_pixels = img_array.reshape(-1, 3)

        groups = kmeans.predict(flat_pixels)
        mask = groups.reshape(h, w)

        background_img = np.zeros_like(img_array)
        object_img = np.zeros_like(img_array)

        object_img[mask == 0] = img_array[mask == 0]
        object_img[mask == 1] = (255, 0, 0)

        background_img[mask == 1] = img_array[mask == 1]
        background_img[mask == 0] = (255, 0, 0)
        
        os.makedirs("output", exist_ok=True)
        Image.fromarray(background_img).save("output/background.jpeg")
        Image.fromarray(object_img).save("output/object.jpeg")
