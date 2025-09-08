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
        list_pixel_rgb = pixel_formatter.run({ 'pixel_rgb': pixel_rgb }, True)
        self.pixel_rgbs.append(list_pixel_rgb)

        self.groups.append(group)
        print(f"Model:\nPixels: {self.pixel_rgbs}\nGroups: {self.groups}")