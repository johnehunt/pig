import cv2
import numpy as np
from PIL import ImageOps, Image


def highlight_color_element(pil_image,
                            lower_1_boundary,
                            upper_1_boundary,
                            lower_2_boundary=None,
                            upper_2_boundary=None):
    im = np.array(pil_image)
    # Convert RGB to BGR
    im = im[:, :, ::-1].copy()
    result = im.copy()
    image = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    lower_mask = cv2.inRange(image, lower_1_boundary, upper_1_boundary)
    if lower_2_boundary is None:
        full_mask = lower_mask
    else:
        upper_mask = cv2.inRange(image, lower_2_boundary, upper_2_boundary)
        full_mask = lower_mask + upper_mask

    result = cv2.bitwise_and(result, result, mask=full_mask)
    mask_image = Image.fromarray(full_mask)

    image2 = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
    color_image = Image.fromarray(image2)

    grey_scale_image = ImageOps.grayscale(pil_image).convert('RGBA')

    merged_image = Image.new("RGBA", grey_scale_image.size)
    merged_image.paste(grey_scale_image, (0, 0))

    # Image.merge('RGB', (grey_scale_image, color_image))
    merged_image.paste(color_image, (0, 0), mask_image)

    return merged_image


def highlight_red_elements(pil_image):
    # lower boundary RED color range values; Hue (0 - 10)
    lower1 = np.array([125, 5, 5])
    upper1 = np.array([180, 255, 255])
    new_image = highlight_color_element(pil_image, lower1, upper1)
    return new_image


def highlight_green_elements(pil_image):
    # lower boundary GREEN color range values; Hue (12-86)
    lower1 = np.array([20, 25, 25])
    upper1 = np.array([70, 255, 255])
    new_image = highlight_color_element(pil_image, lower1, upper1)
    return new_image


def highlight_blue_elements(pil_image):
    # lower boundary GREEN color range values; Hue (12-86)
    lower1 = np.array([100, 45, 45])
    upper1 = np.array([135, 255, 255])
    new_image = highlight_color_element(pil_image, lower1, upper1)
    return new_image

def highlight_yellow_elements(pil_image):
    lower1 = np.array([15, 75, 70])
    upper1 = np.array([90, 255, 255])
    new_image = highlight_color_element(pil_image, lower1, upper1)
    return new_image