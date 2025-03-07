import sys
import os

def resource_path(relative_path):
    try:
        # PyInstaller creates a temporary folder for bundled resources
        base_path = sys._MEIPASS
    except Exception:
        # If not running from a bundle, use the current directory
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# Example of loading an image
image_path = resource_path("assets/your_image.png")