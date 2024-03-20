import os
import cv2
import numpy as np
from datetime import datetime
import random

random.seed()


def order_images_by_creation_date(directory):
    image_files = [f for f in os.listdir(
        directory) if f.endswith('.jpg') or f.endswith('.png')]
    images_with_timestamp = [(f, os.path.getctime(
        os.path.join(directory, f))) for f in image_files]
    sorted_images = sorted(images_with_timestamp, key=lambda x: x[1])
    return [img[0] for img in sorted_images]


def compute_and_save_mog2_difference(images, output_directory, mog2):
    # Create a MOG2 background subtractor

    # Initialize an accumulator for combined difference
    combined_difference = None

    # Iterate through all pairs of images in the array
    for image_path in images:
        # Read the image
        img = cv2.imread(image_path)

        # Ensure the image was successfully read
        if img is not None:
            # Apply MOG2 background subtraction
            foreground_mask = mog2.apply(img)

            # If it's the first image, initialize the accumulator
            if combined_difference is None:
                combined_difference = np.zeros_like(
                    img, dtype=np.uint8)[:, :, 1]

            # Accumulate the differences
            combined_difference += foreground_mask
        else:
            print(f"Error reading image: {image_path}")

    # Save the combined difference image
    output_filename = os.path.join(
        output_directory, f"{os.path.basename(images[0])} - {os.path.basename(images[-1])}.jpg")
    cv2.imwrite(output_filename, combined_difference)


def main():
    skip = 1
    mog2 = cv2.createBackgroundSubtractorMOG2(history=skip)
    dataset_directory = r'.\Dataset\Scene'
    difference_directory = r'.\Dataset\Difference\calculated_from_scene'

    # Ensure the output directory exists
    os.makedirs(difference_directory, exist_ok=True)

    # Order the images in the dataset directory by creation date
    sorted_images = order_images_by_creation_date(dataset_directory)

    # Process subsequent pairs of images, skipping eight images in between
    # Increment by 8 to skip seven images in between

    for i in range(0, len(sorted_images) - skip, skip):
        image1_index = i
        image2_index = i + skip

        # Ensure image2_index is within the range of sorted_images
        if image2_index >= len(sorted_images):
            break

        # Create an array of image paths from image1 to image2 (inclusive)
        image_paths = [os.path.join(dataset_directory, sorted_images[j])
                       for j in range(image1_index, image2_index + 1)]

        # Compute and save the MOG2 difference between images
        compute_and_save_mog2_difference(
            image_paths, difference_directory, mog2)


if __name__ == "__main__":
    main()
