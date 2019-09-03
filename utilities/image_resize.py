import argparse
import os

from PIL import Image


def rescale_image(directory, size):
    for img in os.listdir(directory):
        print(directory + img)
        im = Image.open(directory + img)
        im_resized = im.resize(size, Image.ANTIALIAS)
        im_resized.save(directory + img)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rescale images')
    parser.add_argument("-d", '--directory', type=str, required=True, help='Directory ')
    parser.add_argument("-s", "--size", type=int, nargs=2, required=True
                        , metavar=('width', 'height'), help='Image size')
    args = parser.parse_args()
    rescale_image(args.directory, args.size)
