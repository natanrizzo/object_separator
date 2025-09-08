class Controller:
    def __init__(self):
        self.view = None
        self.model = None
    
    def set_view(self, view):
        self.view = view
    
    def set_model(self, model):
        self.model = model
    
    def save_pixel(self, pixel_rgb: list, group: int):
        self.model.save_pixel(pixel_rgb, group)