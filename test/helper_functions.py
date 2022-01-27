from PIL import Image
import numpy as np
from pathlib import Path


def generate_random_image(filename: Path):
    random_array = np.random.randint(low=0, high=255, size=(1500, 1500), dtype=np.uint8)
    random_array = random_array.astype(np.uint8)
    random_im = Image.fromarray(random_array)
    random_im.save(filename)
