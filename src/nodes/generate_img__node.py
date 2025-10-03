from src.node import Node


class GenerateImg(Node):
    def process(self, data):
        object_img = data["object_img"]
        background_img = data["background_img"]
        morphed_img = data["morphed_img"]
        mask = data["mask"]
        morphed_mask = data["morphed_mask"]
        img_array = data["img_array"]
        

        object_img[mask == 0] = img_array[mask == 0]
        object_img[mask == 1] = (0, 0, 0)
        
        background_img[mask == 1] = img_array[mask == 1]
        background_img[mask == 0] = (0, 0, 0)

        morphed_img[morphed_mask == 1] = img_array[morphed_mask == 1]
        morphed_img[morphed_mask == 0] = (0, 0, 0)

        data["object_img"] = object_img
        data["background_img"] = background_img
        data["morphed_img"] = morphed_img

        return data