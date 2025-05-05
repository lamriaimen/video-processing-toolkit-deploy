from __future__ import print_function, division
import argparse
import os
import cv2
import time
# import ffmpy
import numpy as np
import torch
import torch.nn as nn
import time
import sys
import os
from pathlib import Path
from videoanalyst.nodes.sources import ImageFile
import subprocess
from datetime import timedelta
from videoanalyst.nodes.operators import FieldSegmentation, Mask
from videoanalyst.engine.types import Image
from PIL import Image as PILImage


class ColorProcessing:

    def __init__(self):
        print(" I am inside init function of test file ")

    @staticmethod
    def plot_img(image: Image):

        img_rgb = image.to_color_mode("RGB").array
        return PILImage.fromarray(img_rgb)

    @staticmethod
    def channel_histogram(img, channel=0):
        """
            Note : 257 bins since bins are divided as [0,1), [1,2), ..., [254,255), [255,256]. If we took
            256 bin, the last bin would have been [254,255] thus concatenating two values.
        """
        histogram = np.histogram(img[:, :, channel], np.arange(257))
        histogram_list = [histogram[0], np.arange(256)]
        return histogram_list

    @staticmethod
    def histogram_peak(histogram):
        return histogram[1][np.argmax(histogram[0])]

    @staticmethod
    def morphological_opening(img, morph_size):
        kernel = np.ones((morph_size, morph_size), np.uint8)
        return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

    @staticmethod
    def morphological_closing(img, morph_size):
        kernel = np.ones((morph_size, morph_size), np.uint8)
        return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    @staticmethod
    def gaussian_blur(img, kernel_size, std):
        return cv2.GaussianBlur(img, (kernel_size, kernel_size), std)

    @staticmethod
    def threshold(img, channel=0, threshmin=None, threshmax=None):
        mask_1 = np.where(img[:, :, channel] > threshmin, 1, 0)
        mask_2 = np.where(img[:, :, channel] < threshmax, 1, 0)
        mask = (mask_1 == 1) & (mask_2 == 1)
        mask = mask.astype("uint8")
        mask[mask == 1] = 255
        return mask

    @staticmethod
    def compute_field_mask_cvprw_2018(frame, str_type):
        """Function to generate the mask for field segmentation
        Args:
            frame: Input opencv image
            str_type: there are two type of approximation used: "epsilon" and "threshold_approximation"; This operator
            helps to smooth the boundary of the image

        Returns:
            None
        Resources:
            "A bottom-up approach based on semantics for the interpretation of the main camera stream in soccer games"
            URL: http://www.telecom.ulg.ac.be/publi/publications/anthony/Anthony2018ABottomUp/index.html
        """
        # Parameters
        threshold_width = 10
        gaussian_blur_size = 9
        gaussian_blur_std = 1
        max_number_of_contour_edges = 20

        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        frame_hsv_filtered = ColorProcessing.gaussian_blur(frame_hsv, gaussian_blur_size, gaussian_blur_std)

        histogram = ColorProcessing.channel_histogram(frame_hsv_filtered, channel=0)
        histogram_peak = ColorProcessing.histogram_peak(histogram)

        thresholded_mask = ColorProcessing.threshold(frame_hsv_filtered, channel=0,
                                                     threshmin=histogram_peak - threshold_width,
                                                     threshmax=histogram_peak + threshold_width)

        filtered_mask = ColorProcessing.morphological_opening(thresholded_mask, 15)
        filtered_mask = ColorProcessing.morphological_closing(filtered_mask, 17)

        kernel_dilation = np.ones((13, 13), np.uint8)
        filtered_mask = cv2.dilate(filtered_mask, kernel_dilation, iterations=3)

        contours, hierarchy = cv2.findContours(filtered_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        areas = []

        for contour in contours:
            areas.append(cv2.contourArea(contour))

        max_index = np.argmax(areas)

        # Approximation and convex Hull
        field_contour = contours[max_index]
        threshold_contour_approximation = 0

        if str_type == "epsilon":
            epsilon = 0.01 * cv2.arcLength(field_contour, True)
            field_contour = cv2.approxPolyDP(field_contour, epsilon, True)

        if str_type == "threshold_approximation":
            while len(field_contour) > max_number_of_contour_edges:
                threshold_contour_approximation = threshold_contour_approximation + 1
                field_contour = cv2.approxPolyDP(field_contour, threshold_contour_approximation, True)

        field_contour = cv2.convexHull(field_contour)

        filtered_mask.fill(0)
        cv2.drawContours(filtered_mask, [field_contour], 0, 255, -1)

        # cv2.imshow("image", filtered_mask)
        # cv2.waitKey(0)

        return filtered_mask

    @staticmethod
    def compute_field_mask_nils(image_path):

        # path = Path("/home/tanmoymondal/Videos/FootBall_Video_Data/669/clips/"
        #             "save_frames_regular_time_interval/00043.jpg")

        path = Path(image_path)

        image_source = ImageFile(path)

        segmentation_node = FieldSegmentation()
        image_source()
        segmentation_node(image=image_source.output.value)

        result_img = segmentation_node.output.value
        pil_image = ColorProcessing.plot_img(result_img)
        pil_image.show()

        my_mask = Mask()
        my_mask(image_source.output.value, result_img)
        merged_imag = my_mask.output.value

        pil_image = ColorProcessing.plot_img(merged_imag)
        pil_image.show()

        return pil_image

    @staticmethod
    def generate_batch_background_image(all_dir_path):
        """Function to generate the mask for field segmentation
        Args:
            all_dir_path: The main directory path where all the subdirectory exist

        Returns:
            None
        Resources:
            "A bottom-up approach based on semantics for the interpretation of the main camera stream in soccer games"
            URL: http://www.telecom.ulg.ac.be/publi/publications/anthony/Anthony2018ABottomUp/index.html
        """

        # list file and directories
        all_sub_dirs = os.listdir(all_dir_path)
        for sub_dir in all_sub_dirs:
            make_full_dir_path = os.path.join(all_dir_path, sub_dir, "i_frames")
            make_full_dir_masked = os.path.join(all_dir_path, sub_dir, "backgd_removed_images")

            if not os.path.exists(make_full_dir_masked):  # if the masked directory doesn't exist
                os.makedirs(make_full_dir_masked)  # create a new directory

            jpg_files = Path(make_full_dir_path).glob('*.jpg')

            for get_files in jpg_files:
                with get_files.open(mode='r') as spec_image_files:
                    img_file_name_with_ext = os.path.basename(str(get_files))
                    img_frame = cv2.imread(str(get_files), cv2.IMREAD_COLOR)

                    # get_mask_1 = ColorProcessing.compute_field_mask_cvprw_2018(img_frame, "epsilon")
                    get_mask_2 = ColorProcessing.compute_field_mask_cvprw_2018(img_frame, "threshold_approximation")

                    # masked_1 = cv2.bitwise_and(img_frame, img_frame, mask=get_mask_1)
                    masked_2 = cv2.bitwise_and(img_frame, img_frame, mask=get_mask_2)

                    full_dir_path_masked_img = os.path.join(make_full_dir_masked, img_file_name_with_ext)
                    cv2.imwrite(full_dir_path_masked_img, masked_2)

    @staticmethod
    def apply_nils_background_removal_on_image(img_file_path):

        img_file_path = Path(img_file_path)
        image_source = ImageFile(img_file_path)

        segmentation_node = FieldSegmentation()
        segmentation_node.border_size.value = 25
        image_source()

        segmentation_node(image=image_source.output.value)

        result_img = segmentation_node.output.value
        # pil_result_image = ColorProcessing.plot_img(result_img)

        my_mask = Mask()
        my_mask(image_source.output.value, result_img)
        merged_imag = my_mask.output.value

        pil_masked_image = ColorProcessing.plot_img(merged_imag)
        pil_masked_image.show()

    @staticmethod
    def generate_batch_background_image_nils(all_dir_path):
        """Function to generate the mask for field segmentation
        Args:
            all_dir_path: The main directory path where all the subdirectory exist

        Returns:
            None
        Resources:
            "A bottom-up approach based on semantics for the interpretation of the main camera stream in soccer games"
            URL: http://www.telecom.ulg.ac.be/publi/publications/anthony/Anthony2018ABottomUp/index.html
        """

        # list file and directories
        all_sub_dirs = os.listdir(all_dir_path)
        for sub_dir in all_sub_dirs:
            make_full_dir_path = os.path.join(all_dir_path, sub_dir, "i_frames")
            make_full_dir_masked = os.path.join(all_dir_path, sub_dir, "Nils_backgd_removed_images")

            if not os.path.exists(make_full_dir_masked):  # if the masked directory doesn't exist
                os.makedirs(make_full_dir_masked)  # create a new directory

            jpg_files = Path(make_full_dir_path).glob('*.jpg')

            for get_files in jpg_files:
                with get_files.open(mode='r') as spec_image_files:
                    img_file_name_with_ext = os.path.basename(str(get_files))

                    img_file_path = Path(get_files)
                    image_source = ImageFile(img_file_path)

                    segmentation_node = FieldSegmentation()
                    segmentation_node.border_size.value = 80
                    image_source()

                    segmentation_node(image=image_source.output.value)

                    result_img = segmentation_node.output.value
                    # pil_result_image = ColorProcessing.plot_img(result_img)

                    my_mask = Mask()
                    my_mask(image_source.output.value, result_img)
                    merged_imag = my_mask.output.value

                    pil_masked_image = ColorProcessing.plot_img(merged_imag)

                    full_dir_path_masked_img = os.path.join(make_full_dir_masked, img_file_name_with_ext)
                    pil_masked_image.save(full_dir_path_masked_img)


def main():
    all_dir_path = "/home/tanmoymondal/Videos/FootBall_Video_Data_Server/"
    # ColorProcessing.generate_batch_background_image(all_dir_path)
    ColorProcessing.generate_batch_background_image_nils(all_dir_path)

    # img_file_path = "/home/tanmoymondal/Videos/FootBall_Video_Data_Server/5299/i_frames/58::-frame_8820.jpg"
    # ColorProcessing.apply_nils_background_removal_on_image(img_file_path)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print(f'Done...Take {(time.time() - start_time):.4f} (sec)')
