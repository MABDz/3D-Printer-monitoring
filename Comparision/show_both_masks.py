import os
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import keyboard
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk


def order_images_by_name(directory):
    image_files = [f for f in os.listdir(
        directory) if f.endswith('.jpg') or f.endswith('.png')]
    sorted_images = sorted(image_files)
    return [os.path.join(directory, img) for img in sorted_images]


def display_images(images_mask, images_scene):
    num_images = len(images_mask)
    index = 0

    fig, axes = plt.subplots(1, 2)

    def update_plot():
        nonlocal index

        # Load images
        img_mask = cv2.imread(images_mask[index], cv2.IMREAD_GRAYSCALE)
        img_scene = cv2.imread(images_scene[index])

        # Display images side by side
        axes[0].clear()
        axes[0].imshow(img_mask, cmap='gray')
        axes[0].set_title('Mask Image')

        axes[1].clear()
        axes[1].imshow(cv2.cvtColor(img_scene, cv2.COLOR_BGR2RGB))
        axes[1].set_title('Scene Image')

        plt.draw()

        # Increment index and loop back to the beginning if necessary
        index = (index + 1) % num_images

    # Schedule the first update
    update_plot()

    # Schedule periodic updates with a timer
    plt.gcf().canvas.mpl_connect('key_press_event', lambda event: update_plot())
    plt.show()


if __name__ == "__main__":
    calculated_from_mask_directory = r'.\Dataset\Difference\calculated_from_mask'
    calculated_from_scene_directory = r'.\Dataset\Difference\calculated_from_scene'

    # Order images by name
    images_mask = order_images_by_name(calculated_from_mask_directory)
    images_scene = order_images_by_name(calculated_from_scene_directory)

    # Display images side by side
    display_images(images_mask, images_scene)
