import os
import cv2
import random
import numpy as np

random.seed()


def order_images_by_creation_date(directory):
    image_files = [f for f in os.listdir(
        directory) if f.endswith('.jpg') or f.endswith('.png')]
    images_with_timestamp = [(f, os.path.getctime(
        os.path.join(directory, f))) for f in image_files]
    sorted_images = sorted(images_with_timestamp, key=lambda x: x[1])
    return [img[0] for img in sorted_images]


def accumulate_masks(images, output_directory, skip):
    # Initialize an accumulator for combined masks
    combined_mask = None

    # Iterate through all images in the array with skipping
    for i in range(0, len(images), skip):
        image_path = images[i]

        # Read the mask image
        mask = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # Ensure the image was successfully read
        if mask is not None:
            # If it's the first mask, initialize the accumulator
            if combined_mask is None:
                combined_mask = np.zeros_like(mask, dtype=np.uint8)

            # Accumulate the masks
            combined_mask += mask
        else:
            print(f"Error reading mask: {image_path}")

    # Save the combined mask image
    output_filename = os.path.join(
        output_directory, f"{os.path.basename(images[0])} - {os.path.basename(images[-1])}.jpg")
    print(output_filename)
    cv2.imwrite(output_filename, combined_mask)


def main():
    dataset_directory = r'.\Dataset\Mask'
    combined_mask_directory = r'.\Dataset\Difference\calculated_from_mask'

    # Ensure the output directory exists
    os.makedirs(combined_mask_directory, exist_ok=True)

    # Order the mask images by creation date
    sorted_masks = order_images_by_creation_date(dataset_directory)

    # Set the skip value
    skip = 1  # Change this value as needed
    for i in range(0, len(sorted_masks) - skip, skip):
        image1_index = i
        image2_index = i + skip

        # Ensure image2_index is within the range of sorted_masks
        if image2_index >= len(sorted_masks):
            break

        # Create an array of image paths from image1 to image2 (inclusive)
        image_paths = [os.path.join(dataset_directory, sorted_masks[j])
                       for j in range(image1_index, image2_index + 1)]

        # Accumulate masks with skipping
        accumulate_masks(image_paths, combined_mask_directory, skip)


if __name__ == "__main__":
    main()
