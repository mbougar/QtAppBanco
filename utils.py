import sys
import os

#Gestiona las rutas de lso recursos para que funcionen con pyInstaller
def resource_path(relative_path):
    try:
        
        base_path = sys._MEIPASS
    except Exception:
        
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)