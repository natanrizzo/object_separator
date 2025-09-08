from src.node import Node

class PixelFormater(Node):
    '''
        params:
            data: (dict)\n
                - pixel_rgb: (tuple)
        returns:
            - 0: pixel_rgb: (list)
    '''
    def process(self, data):
        print(data)
        r, g, b = data['pixel_rgb']
        
        data = [r, g, b]

        return data