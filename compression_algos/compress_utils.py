import cv2
import numpy as np

def apply_dct_compression(image, block_size=8, threshold=10):
    height, width, _ = image.shape
    compressed = np.zeros_like(image, dtype=np.float32)

    for channel in range(3):
        for i in range(0, height, block_size):
            for j in range(0, width, block_size):
                block = image[i:i+block_size, j:j+block_size, channel].astype(np.float32)
                if block.shape[0] != block_size or block.shape[1] != block_size:
                    continue

                dct_block = cv2.dct(block)
                dct_block[np.abs(dct_block) < threshold] = 0
                idct_block = cv2.idct(dct_block)

                compressed[i:i+block_size, j:j+block_size, channel] = idct_block

    return np.clip(compressed, 0, 255).astype(np.uint8)
