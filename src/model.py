from src.nodes.generate_img__node import GenerateImg
from src.nodes.generate_img_clean_arrays__node import GenerateImgCleanArrays
from src.nodes.normalize_img_array__node import NormalizeImgArray
from src.nodes.predict_groups__node import PredictGroups
from src.nodes.save_file__node import SaveFile
from src.nodes.train_kmeans__node import TrainKMeans
from src.nodes.pixel_formater__node import PixelFormater


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
        data = { # Set up dictionary for the node chain.
            "X": self.pixel_rgbs,
            "y": self.groups,
            "image_path": image_path
        }

        # Instantiate node chain.
        train_kmeans = TrainKMeans()
        normalize_img_array = NormalizeImgArray()
        predict_groups = PredictGroups()
        generate_img_clean_arrays = GenerateImgCleanArrays()
        generate_img = GenerateImg()
        save_file = SaveFile()

        # Set next nodes for each one of the nodes
        train_kmeans.set_next_node(normalize_img_array)
        normalize_img_array.set_next_node(predict_groups)
        predict_groups.set_next_node(generate_img_clean_arrays)
        generate_img_clean_arrays.set_next_node(generate_img)
        generate_img.set_next_node(save_file)

        # Run the chain of nodes
        train_kmeans.run(data)

        self.controller.show_images(["output/background.jpeg", "output/object.jpeg"])

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
                    object_img[y, x] = (0, 0, 0)
                else: # Object
                    background_img[y, x] = (0, 0, 0)
                    object_img[y, x] = pixels[x, y]
                x+=1
            y+=1
        '''
        