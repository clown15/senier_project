import os
from pathlib import Path
from PIL import Image

def convert_to_webp(source):
    destination = source.with_suffix(".webp")

    image = Image.open(source)  
    image.save(destination, format="webp")  

    return destination

def main():

    paths = Path("static").glob("**/*.png")
    for path in paths:
        webp_path = convert_to_webp(path)
        #print(webp_path)

main()