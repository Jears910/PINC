import os
Addinspath = os.path.dirname(__file__)
allfiles = []
for filename in os.listdir(Addinspath):
    if(filename[:6] == "addin-" and filename[-3:] == ".py" and not filename == "__init__.py" and not filename == "__pycache__"):
        stripName = os.path.splitext(filename)[0]
        allfiles.append(stripName)
__all__ = allfiles
