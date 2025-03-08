import cv2, os
from PIL import Image
import numpy as np

program_dir = os.path.dirname(os.path.abspath(__file__))
image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
image_file = ""

for filename in os.listdir(program_dir):
    if any(filename.endswith(ext) for ext in image_extensions):
        image_file = os.path.join(program_dir, filename)
        break
    elif not any(filename.endswith(ext) for ext in image_extensions):
        print("No supported format or there is no file.")
        exit(1)
if image_file.endswith(".gif"):
    image = Image.open(image_file)
    image.save("image.png")
    image_file = os.path.join("image.png")
    image = cv2.imread(image_file, cv2.IMREAD_UNCHANGED)
else:
    image = cv2.imread(image_file, cv2.IMREAD_UNCHANGED)

if image is None:
    print(f"Error:Cannot load image {image_file}.")
    exit(1)

height, width, channels = image.shape

if channels not in [3, 4]:
    print("Error:Channels other than 3 or 4 are not supported.")

new_width = 300
aspect_ratio = height / width
new_height = int(new_width * aspect_ratio)
resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)

sharpen_kernel = np.array([[0, -1, 0],
                           [-1, 5,-1],
                           [0, -1, 0]])

image = cv2.filter2D(resized_image, -1, sharpen_kernel)


gray_image = np.zeros_like(image)
gray_map = []
gray_symbols = ['＃', '＠', '＆', '％', '！', '？', '＜', '＞', '　']

for i in range(new_height):
        gray_map.append([])
        for j in range(new_width):
            if channels == 3:
                b, g, r = image[i, j]
            if channels == 4:
                b, g, r, a = image[i, j]
            Y = 0.299 * r + 0.587 * g + 0.114 * b
            if channels == 4:
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
            else:
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

with open('output.txt', 'w', encoding='utf-8') as file:
    for k in range(len(gray_map)):
        for l in range(len(gray_map[k])):
            file.write(gray_map[k][l])
        file.write("\n")
