from PIL import Image
from pathlib import Path
import numpy as np

if __name__ == "__main__":
    for img_path in sorted(Path("./static/reverse_img_store").glob("*.jpg")):
        print(img_path)