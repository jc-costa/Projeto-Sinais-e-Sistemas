import matplotlib.pyplot as plt
import numpy as np
import imutils
import cv2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image", type=str, required=True)

def detectBlur(image, frequencyThreshold, blurrinessThreshold, visualize=False):
    height, width = image.shape
    cX, cY = (int(width/2.0), int(height/2.0))

    transformedImage = np.fft.fft2(image)
    transformedAndShiftedImage = np.fft.fftshift(transformedImage)

    if visualize:
        # compute the magnitude spectrum of the transform
        magnitude = 20 * np.log(np.abs(transformedAndShiftedImage))
        # display the original input image
        (fig, ax) = plt.subplots(1, 2, )
        ax[0].imshow(image, cmap="gray")
        ax[0].set_title("Input")
        ax[0].set_xticks([])
        ax[0].set_yticks([])
        # display the magnitude image
        ax[1].imshow(magnitude, cmap="gray")
        ax[1].set_title("Magnitude Spectrum")
        ax[1].set_xticks([])
        ax[1].set_yticks([])
        # show our plots
        plt.show()

    transformedAndShiftedImage[cY - frequencyThreshold:cY + frequencyThreshold, cX - frequencyThreshold:cX + frequencyThreshold] = 0
    transformedImage = np.fft.ifftshift(transformedAndShiftedImage)
    reconstructedImage = np.fft.ifft2(transformedImage)

    magnitude = 20 * np.log(np.abs(reconstructedImage))
    mean = np.mean(magnitude)

    return mean, mean <= blurrinessThreshold


args = parser.parse_args()
originalImage = cv2.imread(args.image)
originalImage = imutils.resize(originalImage, width=500)
grayScaleImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)

print(detectBlur(grayScaleImage, frequencyThreshold=60, blurrinessThreshold=10))