import os
import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.function_base import copy
# import imutils
import cv2
import argparse
import pandas as pd

from numpy.lib.npyio import save


BLURRINESS_THRESHOLD = 10

def get_mask_generator(mask_generator):
    if args.mask_generator == "rectangular":
        return rectangular_mask
    elif args.mask_generator == "circular":
        return circular_mask
    else:
        raise ValueError("Mask generator (-m/--mask-generator) must be either 'rectangular' or 'circular'.")


def run_single(args):
    filtered_image = get_filtered_image(args.image, args.filter_threshold, get_mask_generator(args.mask_generator), args.visualize)
    if args.save_reconstructed:
        reconstructed_image_name = save_image_name(args.image)
        reconstructed_image = 255-np.abs(filtered_image)
        plt.imsave(reconstructed_image_name, reconstructed_image, cmap="gray")


def run_batch(args):
    images_names = [os.path.join(args.folder, f) for f in os.listdir(args.folder) if os.path.isfile(os.path.join(args.folder, f))]
    get_and_save_detect_blur_data(images_names, args.filter_threshold, get_mask_generator(args.mask_generator))


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

parser_batch = subparsers.add_parser('batch')
parser_batch.add_argument("-f", "--folder", type=str, required=True)
parser_batch.add_argument("-t", "--filter-threshold", dest="filter_threshold", type=int, nargs="+")
parser_batch.add_argument("-m", "--mask-generator", dest="mask_generator", type=str, default="rectangular")
parser_batch.set_defaults(func=run_batch)

parser_single = subparsers.add_parser('single')
parser_single.add_argument("-i", "--image", type=str, required=True)
parser_single.add_argument("-v", "--visualize", action="store_true")
parser_single.add_argument("-t", "--filter-threshold", dest="filter_threshold", type=int, default=60)
parser_single.add_argument("-m", "--mask-generator", dest="mask_generator", type=str, default="rectangular")
parser_single.add_argument("-s", "--save-reconstructed", dest="save_reconstructed", action="store_true")
parser_single.set_defaults(func=run_single)

def circular_mask(height, width, r):
    mask = np.ones((height, width))
    center = (int(height/2), int(width/2))
    x, y = np.ogrid[:height,:width]
    mask_area = (x - center[0])**2 + (y - center[1])**2 <= r**2
    mask[mask_area] = 0
    return mask


def rectangular_mask(height, width, side):
    mask = np.ones((height, width))
    center = (int(height/2), int(width/2))
    mask[center[0]-side:center[0]+side, center[1]-side:center[1]+side] = 0
    return mask


def show_image(ax, image, title):
    ax.imshow(image, cmap="gray")
    ax.set_title(title)
    ax.set_xticks([])
    ax.set_yticks([])


def visualize_high_pass_filter(image, transformed_image, transformed_and_shifted_image, transformed_and_shifted_image_filtered, transformed_image_filtered, reconstructed_image):
    # compute the magnitude spectrum of the transform
    magnitude = 20 * np.log(np.abs(transformed_image))
    shifted_magnitude = 20 * np.log(np.abs(transformed_and_shifted_image))
    # display the original input image
    (fig, ax) = plt.subplots(2, 3, )
    show_image(ax[0,0], image, "Input")
    show_image(ax[0,1], magnitude, "Magnitude Spectrum")
    show_image(ax[0,2], shifted_magnitude, "Shifted Magnitude Spectrum")

    magnitude = 20 * np.log(np.abs(transformed_image_filtered))
    shifted_magnitude = 20 * np.log(np.abs(transformed_and_shifted_image_filtered))

    show_image(ax[1,0], shifted_magnitude, "Shifted Magnitude Spectrum")
    show_image(ax[1,1], magnitude, "Magnitude Spectrum")
    show_image(ax[1,2], 255-np.abs(reconstructed_image), "Reconstructed Input")

    plt.show()


def apply_high_pass_filter(image, frequency_threshold, mask_generator=rectangular_mask, visualize=False):
    height, width = image.shape
    cX, cY = (int(width/2.0), int(height/2.0))

    transformed_image = np.fft.fft2(image)
    transformed_and_shifted_image = np.fft.fftshift(transformed_image)

    mask = mask_generator(height, width, frequency_threshold)

    transformed_and_shifted_image_filtered = transformed_and_shifted_image * mask
    transformed_image_filtered = np.fft.ifftshift(transformed_and_shifted_image_filtered)
    reconstructed_image = np.fft.ifft2(transformed_image_filtered)

    if visualize:
        visualize_high_pass_filter(image, transformed_image, transformed_and_shifted_image, transformed_and_shifted_image_filtered, transformed_image_filtered, reconstructed_image)

    return reconstructed_image


def detect_blur(filtered_image):
    magnitude = np.abs(filtered_image)
    mean = np.mean(magnitude)

    return mean, mean <= BLURRINESS_THRESHOLD


def save_image_name(image_name):
    split_name = image_name.split('.')
    first_name = ''.join(split_name[:-1])
    first_name += '-high-filter'
    first_name = first_name[0].upper() + first_name[1:]
    extension = split_name[-1]
    return '.'.join(['reconstructed' + first_name, extension])


def get_filtered_image(image, filter_threshold, mask_generator, visualize):
    original_image = cv2.imread(image)
    gray_scale_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    filtered_image = apply_high_pass_filter(gray_scale_image, filter_threshold, mask_generator, visualize=visualize)
    return filtered_image


def get_and_save_detect_blur_data(images_names, filter_thresholds, mask_generator):
    is_image_blur = ['blur' in image_name for image_name in images_names]
    detect_blur_data = {
        'name': images_names,
        'is_image_blur': is_image_blur,
    }
    for filter_threshold in filter_thresholds:
        images_score = []
        wc_column_name = f'wc={filter_threshold}'
        for image_name in images_names:
            filtered_image = get_filtered_image(image_name, filter_threshold, mask_generator, False)
            score, is_blur = detect_blur(filtered_image)
            images_score.append(score)
        detect_blur_data[wc_column_name] = images_score
    blur_detection_df = pd.DataFrame(data=detect_blur_data)
    blur_detection_df.to_csv('blur_detection_data.csv')


args = parser.parse_args()
args.func(args)