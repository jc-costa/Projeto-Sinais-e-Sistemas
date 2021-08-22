import os
import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.function_base import copy
import imutils
import cv2
import argparse

from numpy.lib.npyio import save

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image", type=str, required=True)
parser.add_argument("-f", "--filter-threshold", dest="filter_threshold", type=int, default=60)
parser.add_argument("-v", "--visualize", action="store_true")
parser.add_argument("-s", "--save-reconstructed", dest="save_reconstructed", action="store_true")

def apply_high_pass_filter(image, frequency_threshold, visualize=False):
    height, width = image.shape
    cX, cY = (int(width/2.0), int(height/2.0))

    transformed_image = np.fft.fft2(image)
    transformed_and_shifted_image = np.fft.fftshift(transformed_image)

    transformed_and_shifted_image_filtered = copy(transformed_and_shifted_image)
    transformed_and_shifted_image_filtered[cY - frequency_threshold:cY + frequency_threshold, cX - frequency_threshold:cX + frequency_threshold] = 0
    transformed_image_filtered = np.fft.ifftshift(transformed_and_shifted_image_filtered)
    reconstructed_image = np.fft.ifft2(transformed_image_filtered)

    if visualize:
        # compute the magnitude spectrum of the transform
        magnitude = 20 * np.log(np.abs(transformed_image))
        shifted_magnitude = 20 * np.log(np.abs(transformed_and_shifted_image))
        # display the original input image
        (fig, ax) = plt.subplots(2, 3, )
        ax[0,0].imshow(image, cmap="gray")
        ax[0,0].set_title("Input")
        ax[0,0].set_xticks([])
        ax[0,0].set_yticks([])
        # display the magnitude image
        ax[0,1].imshow(magnitude, cmap="gray")
        ax[0,1].set_title("Magnitude Spectrum")
        ax[0,1].set_xticks([])
        ax[0,1].set_yticks([])
        # display the magnitude image
        ax[0,2].imshow(shifted_magnitude, cmap="gray")
        ax[0,2].set_title("Shifted Magnitude Spectrum")
        ax[0,2].set_xticks([])
        ax[0,2].set_yticks([])
        # compute the magnitude spectrum of the transform
        magnitude = 20 * np.log(np.abs(transformed_image_filtered))
        shifted_magnitude = 20 * np.log(np.abs(transformed_and_shifted_image_filtered))

        ax[1,0].imshow(shifted_magnitude, cmap="gray")
        ax[1,0].set_title("Shifted Magnitude Spectrum")
        ax[1,0].set_xticks([])
        ax[1,0].set_yticks([])
        # d1splay the magnitude image
        ax[1,1].imshow(magnitude, cmap="gray")
        ax[1,1].set_title("Magnitude Spectrum")
        ax[1,1].set_xticks([])
        ax[1,1].set_yticks([])
        # d1splay the magnitude image
        ax[1,2].imshow(255-np.abs(reconstructed_image), cmap="gray")
        ax[1,2].set_title("Reconstructed Input")
        ax[1,2].set_xticks([])
        ax[1,2].set_yticks([])
        # show our plots
        plt.show()

    return reconstructed_image

def detect_blur(filtered_image, blurriness_threshold):
    magnitude = 20 * np.log(np.abs(filtered_image))
    mean = np.mean(magnitude)

    return mean, mean <= blurriness_threshold

def save_image_name(image_name):
    split_name = image_name.split('.')
    first_name = ''.join(split_name[:-1])
    first_name += '-high-filter'
    first_name_capitalize = first_name[0].upper() + first_name[1:]
    extension = split_name[-1]
    return '.'.join(['reconstructed' + first_name_capitalize, extension])

args = parser.parse_args()
original_image = cv2.imread(args.image)
#originalImage = imutils.resize(originalImage, width=500)
gray_scale_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

filtered_image = apply_high_pass_filter(gray_scale_image, args.filter_threshold, visualize=args.visualize)

mean, is_blurred= detect_blur(filtered_image, blurriness_threshold=10)
print(mean, is_blurred)

if args.save_reconstructed:
    reconstructed_image_name = save_image_name(args.image)
    print(reconstructed_image_name)
    reconstructed_image = 255-np.abs(filtered_image)
    plt.imsave(reconstructed_image_name, reconstructed_image, cmap="gray")