import os
import sys
import re
from skimage import io
from scipy.ndimage import imread
from PIL import Image
import random
from tqdm import tqdm

def main():
    VAL_RATIO = 0.2 #max 1
    N_PICS = 5000
    DENSITY_VALUE = 3
    bg = Image.open("cells_models/bg.png")
    print bg.size
    schisto = Image.open("cells_models/sample1.png")
    white = Image.open("cells_models/white.png")
    count_white_px = len([x for x in white.getdata()])

    print dir(schisto)
    print len([x for x in schisto.getdata() if sum(x)!= 0]), len([x for x in schisto.getdata()])



    for n in tqdm(range(1, N_PICS + 1)):

        # ratio of validantion flag
        if random.randint(1, 10) <= (VAL_RATIO  * 10):
            type_sample = "validation"
        else:
            type_sample = "train"


        density_generator = random.randint(1, DENSITY_VALUE)
        bg_frame = bg.copy()
        density_in_field = 0
        for x in range(density_generator):

            schisto_r = schisto.copy() # essa parte devera captuar um schisto sample aleatorio
            schisto_r = schisto_r.rotate(random.randint(0, 360))

            w_to_subtract = white.copy()

            x_coor = random.randint(-10, 140)
            y_coor = random.randint(-10, 140)

            w_to_subtract.paste(schisto_r, (x_coor, y_coor), schisto_r)

            sub_value = len([ s for s in w_to_subtract.getdata() if sum(s) != 255 * 4])

            schisto_real_size = len ([ px_schisto for px_schisto in schisto_r.getdata() if sum (px_schisto)])

            density = float(sub_value)/schisto_real_size

            density_in_field += density

            bg_frame.paste(schisto_r, (x_coor, y_coor), schisto_r)
        bg_frame.save("pics/{}_image_{}_|{}|.png".format(type_sample ,str(n), str(round(density_in_field, ndigits=3))))
        #print "Density in  field: ", density_in_field
        #bg.show()
        #
        # io.imsave('merge.png', bg)
        # io.imshow(schisto)
        # io.show()


if __name__ == '__main__':
    sys.exit(main())
