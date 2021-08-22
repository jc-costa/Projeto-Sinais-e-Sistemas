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
parser.add_argument("-f", "--filter-threshold", dest="filterThreshold", type=int, default=60)
parser.add_argument("-v", "--visualize", action="store_true")
parser.add_argument("-s", "--save-reconstructed", dest="saveReconstructed", action="store_true")

def applyHighPassFilter(image, frequencyThreshold, visualize=False):
    height, width = image.shape
    cX, cY = (int(width/2.0), int(height/2.0))

    transformedImage = np.fft.fft2(image)
    transformedAndShiftedImage = np.fft.fftshift(transformedImage)

    transformedAndShiftedImageFiltered = copy(transformedAndShiftedImage)
    transformedAndShiftedImageFiltered[cY - frequencyThreshold:cY + frequencyThreshold, cX - frequencyThreshold:cX + frequencyThreshold] = 0
    transformedImageFiltered = np.fft.ifftshift(transformedAndShiftedImageFiltered)
    reconstructedImage = np.fft.ifft2(transformedImageFiltered)

    if visualize:
        # compute the magnitude spectrum of the transform
        magnitude = 20 * np.log(np.abs(transformedImage))
        shiftedMagnitude = 20 * np.log(np.abs(transformedAndShiftedImage))
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
        ax[0,2].imshow(shiftedMagnitude, cmap="gray")
        ax[0,2].set_title("Shifted Magnitude Spectrum")
        ax[0,2].set_xticks([])
        ax[0,2].set_yticks([])
        # compute the magnitude spectrum of the transform
        magnitude = 20 * np.log(np.abs(transformedImageFiltered))
        shiftedMagnitude = 20 * np.log(np.abs(transformedAndShiftedImageFiltered))

        ax[1,0].imshow(shiftedMagnitude, cmap="gray")
        ax[1,0].set_title("Shifted Magnitude Spectrum")
        ax[1,0].set_xticks([])
        ax[1,0].set_yticks([])
        # d1splay the magnitude image
        ax[1,1].imshow(magnitude, cmap="gray")
        ax[1,1].set_title("Magnitude Spectrum")
        ax[1,1].set_xticks([])
        ax[1,1].set_yticks([])
        # d1splay the magnitude image
        ax[1,2].imshow(255-np.abs(reconstructedImage), cmap="gray")
        ax[1,2].set_title("Reconstructed Input")
        ax[1,2].set_xticks([])
        ax[1,2].set_yticks([])
        # show our plots
        plt.show()

    return reconstructedImage

def detectBlur(filteredImage, blurrinessThreshold):
    magnitude = 20 * np.log(np.abs(filteredImage))
    mean = np.mean(magnitude)

    return mean, mean <= blurrinessThreshold


args = parser.parse_args()
originalImage = cv2.imread(args.image)
#originalImage = imutils.resize(originalImage, width=500)
grayScaleImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)

filteredImage = applyHighPassFilter(grayScaleImage, frequencyThreshold=args.filterThreshold, visualize=args.visualize)

if args.saveReconstructed:
    plt.imsave(f"reconstructedImage/{os.path.basename(args.image)}", 255-np.abs(filteredImage), cmap="gray")

print(detectBlur(filteredImage, blurrinessThreshold=10))