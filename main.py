import os, sys
from PIL import Image
import numpy as np

programDir = os.path.dirname(os.path.abspath(__file__))
print(programDir)
exts = [".png", ".jpg", ".jpeg", ".bmp", ".gif"]
imageFile = ""
validFileFounded = False

for filename in os.listdir(programDir):
    if any(filename.endswith(ext) for ext in exts):
        imageFile = os.path.join(programDir, filename)
        validFileFounded = True
        break

if not validFileFounded:
    print("No supported file format or there is no file.")
    os.system("pause")
    exit(1)

try:
    image = Image.open(imageFile)
    print(f"Original image mode: {image.mode}")
    image = image.convert("RGBA")
    print(f"Converted image mode: {image.mode}")
except Exception as e:
    print(f"Cannot load image file: {imageFile}\nError: {e}")
    os.system("pause")
    exit(1)

width, height = image.size[0], image.size[1]

aspectRatio = height / width
newSize = 300, int(300 * aspectRatio)

image = image.resize(newSize, Image.LANCZOS)

LmodeImage = np.array(image.convert("L"))
arrImage = np.array(image)

gray_image = np.zeros_like(image)
gray_map = []
gray_symbols = ['＃', '＠', '＆', '％', '！', '？', '＜', '＞', '　']

for i in range(image.size[1]):
        gray_map.append([])
        for j in range(image.size[0]):
            a = arrImage[i, j][3]
            Y = LmodeImage[i, j]
            if a >= 128:
                if Y < 33:
                    gray_map[i].append(gray_symbols[0])
                elif Y < 65:
                    gray_map[i].append(gray_symbols[1])
                elif Y < 97:
                    gray_map[i].append(gray_symbols[2])
                elif Y < 129:
                    gray_map[i].append(gray_symbols[3])
                elif Y < 161:
                    gray_map[i].append(gray_symbols[4])
                elif Y < 193:
                    gray_map[i].append(gray_symbols[5])
                elif Y < 225:
                    gray_map[i].append(gray_symbols[6])
                elif Y < 256:
                    gray_map[i].append(gray_symbols[7])
            else:
                gray_map[i].append(gray_symbols[8])

with open('output.txt', 'w', encoding='utf-8') as file:
    for k in range(len(gray_map)):
        for l in range(len(gray_map[k])):
            file.write(gray_map[k][l])
        file.write("\n")
print("output successful")
