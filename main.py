import os, sys
from PIL import Image
import numpy as np
from colorama import init

init(autoreset=True)

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
    exit(1)

try:
    image = Image.open(imageFile)
    print(f"Original image mode: {image.mode}")
    image = image.convert("RGBA")
    print(f"Converted image mode: {image.mode}")
except Exception as e:
    print(f"Cannot load image file: {imageFile}\nError: {e}")
    exit(1)

print(f"Converting Image: {imageFile}")
width, height = image.size[0], image.size[1]

aspectRatio = height / width
while True:
    newWidth = input("Please enter width that you want(min:12, max:300): ")
    if newWidth.isdigit():
        break
    print("Please enter a valid integer.")

printOutput = input("Do you wanna print output after conversion? Y/N(Default N): ")
printOutput = True if printOutput.upper() == "Y" else False

newWidth = int(newWidth)
newWidth = min(max(12, newWidth), 300)
newSize = newWidth, int(newWidth * aspectRatio)

image = image.resize(newSize, Image.LANCZOS)

LmodeImage = np.array(image.convert("L"))
arrImage = np.array(image)

gray_image = np.zeros_like(image)
gray_map = []
gray_symbols = ['＃', '＠', '＆', '％', '！', '？', '＜', '＞', '　']

for i in range(image.size[1]):
        gray_map.append([])
        for j in range(image.size[0]):
            Y = int(LmodeImage[i, j])
            r, g, b, a = arrImage[i, j]
            if a >= 128:
                index = min(Y * (len(gray_symbols)-1) // 256, len(gray_symbols)-2)
                char = gray_symbols[index]
                ansi_char = f"\033[38;2;{r};{g};{b}m{char}\033[0m"
                gray_map[i].append(ansi_char)
            else:
                gray_map[i].append(gray_symbols[8])

with open('output.txt', 'w', encoding='utf-8') as file:
    for k in range(len(gray_map)):
        for l in range(len(gray_map[k])):
            file.write(gray_map[k][l])
        file.write("\n")

if printOutput:
    for row in gray_map:
        print("".join(row))
    

    

print("output successful")
