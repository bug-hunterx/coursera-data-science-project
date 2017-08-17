from skimage import data, io
from PIL import Image
import numpy
import csv



image = numpy.array(Image.open('VHP.G04.C07.NC.P1981035.SM.SMN.tif'))

print(image.shape)

red_points = {}

for i in range(1000, 1140):
    for j in range(8483, 8611):
        if image[i][j][0] >= 40 and image[i][j][1] <= 10 and image[i][j][2] <= 10 and image[i][j][3] == 255:
            red_points[j] = [i, j]

pixel_indexes = {}
for i in range(1000, 1140):
    for j in range(8483, 8611):
        value = image[i][j][0] == 0 and image[i][j][1] == 0 and image[i][j][2] == 0
        if j in red_points:
            red_point = red_points[j]
            if value == False and i > red_point[0] and (
                (image[i][j][0] >= 10 and image[i][j][1] <= 8 and image[i][j][2] <= 8) == False):
                pixel_indexes[(i, j)] = image
        else:
            print(str(j))
file = open('indexes.csv', 'w')

csv_writer = csv.writer(file, delimiter=',')
for (i, j) in pixel_indexes.keys():
    csv_writer.writerow([i, j])

for i in range(1000, 1140):
    for j in range(8483, 8611):
        if (i, j) in pixel_indexes:
            image[i][j][1] = 255
image_sk_raw = image[1000:1140, 8483:8611]
io.imshow(image_sk_raw)
io.show()
