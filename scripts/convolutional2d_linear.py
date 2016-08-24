import os
import sys
import re
import numpy
from skimage import io, img_as_int
from skimage.transform import resize
from glob import glob
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D

class images_parse():
    def __init__(self, path_of_directory, train=True):

        if train:
            self.data_type = 'train'
        else:
            self.data_type = 'validation'

        self.path_png = path_of_directory + '/{}*png'.format(self.data_type)
        self.path_png = self.path_png.replace("//", "/")
        self.images = glob(self.path_png)
        self.images_number = len(self.images)
        self.item_counted = 0
        self.class_values = [float(re.search("\|(\S+)\|" , value).group(1)) for value in self.images]


    def __iter__(self):
        return self

    def __len__(self):
        return len(self.class_values)

    def next(self):
        if self.item_counted < self.images_number:



            img_opened = io.imread(self.images[self.item_counted])

            # print self.images[self.item_counted]
            # io.imshow(img_opened)
            # io.show()
            # exit()


            array_image =  resize(img_opened,(50, 50)).transpose()

            # io.imshow(array_image)
            # io.show()
            # exit()
            #arary_image = array_image
            self.item_counted += 1
            return array_image
        else:
            raise StopIteration()


    def get_density_list(self):
        return self.class_values



def convolution_training(train_input, validation_input):

    model = Sequential()
    model.add(Convolution2D(20, 6, 6, input_shape=(3, 50, 50)))
    model.add(Activation('relu'))
    model.add(Convolution2D(30, 3, 3))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(3, 3)))

    model.add(Convolution2D(30, 2, 2))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(3, 3)))

    model.add(Flatten())
    model.add(Dense(100))
    model.add(Activation('relu'))
    model.add(Dropout(0.1))
    # model.add(Dense(100))
    # model.add(Activation('relu'))
    # model.add(Dropout(0.1))
    # model.add(Dense(20))
    # model.add(Activation('relu'))
    # model.add(Dropout(0.1))
    model.add(Dense(output_dim=1))
    #model.add(Dense(output_dim=1, init='uniform', activation='linear'))

    model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['accuracy'])  # Using mse loss results in faster convergence
    #
    # print numpy.array(train_input.get_density_list()).shape
    # print len(train_input.get_density_list())
    # print train_input.get_density_list()
    # numpy.array([t for t in train_input])
    # print train_input.get_density_list()
    X_train, y_train, X_test, y_test = numpy.array([t for t in train_input]), numpy.array(train_input.get_density_list()), numpy.array([t for t in validation_input]), numpy.array(validation_input.get_density_list())

    model.fit(X_train, y_train, nb_epoch=2000, batch_size=16, verbose=1 , validation_data=(X_test, y_test))
    #score = model.evaluate(X_test, y_test, batch_size=16)



def main():
    dir_pics_data = '/home/lucas/PycharmProjects/synthetic_deep_schisto/pics'
    train_imgs = images_parse(dir_pics_data, train=True)
    validation_imgs = images_parse(dir_pics_data, train=False)


    #print train_imgs.next().shape, len(train_imgs), len(train_imgs.get_density_list())

    convolution_training(train_imgs, validation_imgs)
    #main session


if __name__ == '__main__':
    sys.exit(main())
