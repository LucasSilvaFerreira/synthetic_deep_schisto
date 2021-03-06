import os
import sys
import re
from skimage import io
from scipy.ndimage import imread
import Image
import random
from tqdm import tqdm
import numpy as np

def check_distance(value, distance_factor=50):

    if sum(value) > distance_factor:
        return True
    else:
        return False

def main():
    VAL_RATIO = 0.2 #max 1
    N_PICS = 100
    DENSITY_VALUE = 3
    DISTANCE_TUNE = 50
    bg = Image.open("/home/lucas/PycharmProjects/synthetic_deep_schisto/cells_models/bg.png")
    print bg.size
    schisto = Image.open("/home/lucas/PycharmProjects/synthetic_deep_schisto/cells_models/sample1.png")
    white = Image.open("/home/lucas/PycharmProjects/synthetic_deep_schisto/cells_models/white.png")
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
        density_generator_history = []
        bg_frame = bg.copy()
        density_in_field = 0
        for x in range(density_generator):

            if len(density_generator_history) != 0 :
                result =  density_generator_history[0]
                #print list(set([ check_distance(map(abs, np.array(x_random) - result)) for x_random in density_generator_history]))
                while False in list(set([check_distance(map(abs, np.array(x_random) - result), distance_factor=DISTANCE_TUNE) for x_random in density_generator_history]))  :
                    print  np.array(x_random), result, 'teste'
                    x_coor = random.randint(-10, 140)
                    y_coor = random.randint(-10, 140)
                    result = np.array([x_coor, y_coor])
                    print result
                    #print set([check_distance(map(abs, np.array(x_random) - result)) for x_random in density_generator_history])


            else:

                x_coor = random.randint(-10, 140)
                y_coor = random.randint(-10, 140)
                np.array([x_coor, y_coor])

            schisto_r = schisto.copy() # essa parte devera captuar um schisto sample aleatorio
            schisto_r = schisto_r.rotate(random.randint(0, 360))

            w_to_subtract = white.copy()

            density_generator_history.append(np.array([x_coor,y_coor ]))

            w_to_subtract.paste(schisto_r, (x_coor, y_coor), schisto_r)

            sub_value = len([ s for s in w_to_subtract.getdata() if sum(s) != 255 * 4])

            schisto_real_size = len ([ px_schisto for px_schisto in schisto_r.getdata() if sum (px_schisto)])

            density = float(sub_value)/schisto_real_size

            density_in_field += density

            bg_frame.paste(schisto_r, (x_coor, y_coor), schisto_r)
        bg_frame.save("/home/lucas/PycharmProjects/synthetic_deep_schisto/pics/{}_image_{}_|{}|.png".format(type_sample ,str(n), str(round(density_in_field, ndigits=3))))
        #print "Density in  field: ", density_in_field
        #bg.show()
        #
        # io.imsave('merge.png', bg)
        # io.imshow(schisto)
        # io.show()


if __name__ == '__main__':
    sys.exit(main())