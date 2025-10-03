import numpy as np
import cv2

from src.node import Node


class MorphologialOperations(Node):
    def process(self, data):
        mask = data["mask"]

        # Convert mask to uint8 format
        binary_mask = np.uint8(mask * 255)

        # Define a kernel for operations
        kernel = np.ones((5, 5), np.uint8)

        # Apply erosion
        eroded_mask = cv2.erode(binary_mask, kernel, iterations=2)
        # Apply dilation
        dilated_mask = cv2.dilate(eroded_mask, kernel, iterations=2)

        # Convert final mask back
        morphed_mask = (dilated_mask / 255).astype(int)

        data["morphed_mask"] = morphed_mask

        return data