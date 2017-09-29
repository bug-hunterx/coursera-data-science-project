from skimage import data, io
from PIL import Image
import numpy as np
import csv


def load_indexes():
    file = open('indexes.csv', 'r')
    reader = csv.reader(file)
    indexes = []
    for row in reader:
        x = int(row[0])
        y = int(row[1])
        indexes.append((x, y))
    return indexes


image = np.array(Image.open('VHP.G04.C07.NC.P1981035.SM.SMN.tif'))


indexes = load_indexes()
coeff = np.load('coeff.npz')['coeff']
max_coeff = np.max(coeff)
min_coeff = np.min(coeff)
length = max_coeff - min_coeff
for i in range(0, len(indexes)):
    index = indexes[i]
    coeff_pixel = coeff[i]
    color = (coeff_pixel - min_coeff) * 255 / length
    image[index[0], index[1]][1] = color

image_sk_raw = image[1000:1140, 8483:8611]
io.imshow(image_sk_raw)
io.show()
