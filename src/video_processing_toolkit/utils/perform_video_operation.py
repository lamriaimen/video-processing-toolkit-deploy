from __future__ import print_function, division
import argparse
import os
import cv2
import time
import ffmpy
import numpy as np
import torch
import torch.nn as nn
import time
import sys
import os
import subprocess
from datetime import timedelta
import copy
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from src.utils.perform_color_processing import ColorProcessing
from videoanalyst.nodes.operators import FieldSegmentation, Mask
from videoanalyst.engine.types import Image
from PIL import Image as PILImage

class VideoOperation:

    def __init__(self):
        print(" Video Operation class ")

    @staticmethod
    def get_clip(input_filename, output_filename, start_time, end_time):
        """
        Function to actually cut the video clips.

        Args:
            input_filename: Path of the input video file
            output_filename: The path of the output file clip
            start_time: The start time stamp
            end_time: The end time stamp.
        Returns:
            None
        """
        ffmpeg_extract_subclip(input_filename, start_time, end_time, targetname=output_filename)

    @staticmethod
    def cut_video_clips(input_filename, output_file_path, time_stamp_start_1, time_stamp_end_1):
        """
        Function to read several start and end time stamps, mentioned in two vectors; "time_stamp_start_1" and
        "time_stamp_end_1", to crop the video clips based on these start and end time stamps.

        Args:
            input_filename: Path of the input video file
            output_file_path: The path of the output file clip
            time_stamp_start_1 : The list of start time in HH:MM:SS format
            time_stamp_end_1 : The list of end time in HH:MM:SS format.
        Returns:
            None
        """
        for ii in range(0, len(time_stamp_start_1)):
            get_clip_start_time = time_stamp_start_1[ii]
            get_clip_start_time = get_clip_start_time.split(':')

            get_clip_end_time = time_stamp_end_1[ii]
            get_clip_end_time = get_clip_end_time.split(':')

            start_time_hr = int(get_clip_start_time[0])
            start_time_min = int(get_clip_start_time[1])
            start_time_sec = int(get_clip_start_time[2])

            end_time_hr = int(get_clip_end_time[0])
            end_time_min = int(get_clip_end_time[1])
            end_time_sec = int(get_clip_end_time[2])

            create_output_file_name = str(start_time_hr) + '_' + str(start_time_min) + '_' + str(start_time_sec) + '-' \
                                      + str(end_time_hr) + '_' + str(end_time_min) + '_' + str(end_time_sec) + '.mp4'
            output_file_path_complete = output_file_path + create_output_file_name

            total_start_time_in_sec = start_time_hr * 3600 + start_time_min * 60 + start_time_sec
            total_end_time_in_sec = end_time_hr * 3600 + end_time_min * 60 + end_time_sec

            VideoOperation.get_clip(input_filename, output_file_path_complete, total_start_time_in_sec,
                                    total_end_time_in_sec)

    @staticmethod
    def handlle_nils_field_segmentation(frame):
        """
        Performs field segmentation on the given image frame, applying a color-based mask
        to isolate regions with specific hue values, typically representing green field areas.

        Args:
            frame (np.ndarray): The input image as a NumPy array in BGR color format.
        Returns:
            np.ndarray: A NumPy array representing the masked image where only the segmented
                    field regions are preserved, and the rest is filtered out.
        """
        segmentation_node = FieldSegmentation()
        segmentation_node.border_size.value = 0
        segmentation_node.blur_size.value = 0
        segmentation_node.min_hue.value = 78
        segmentation_node.max_hue.value = 108

        image_frame = Image(array=frame, mode="BGR")

        segmentation_node(image=image_frame)

        result_img = segmentation_node.output.value
        # pil_result_image = ColorProcessing.plot_img(result_img)

        my_mask = Mask()
        my_mask(image_frame, result_img)
        merged_imag = my_mask.output.value.array

        # pil_masked_image = ColorProcessing.plot_img(merged_imag)

        return merged_imag  # ndarray of numpy

    @staticmethod
    def process_input_video_give_video_output(input_loc, output_loc, function_to_apply):
        """Function to apply the processing on each frames from input video file and create another video.

        Args:
            input_loc: Input video file
            output_loc: The path of output video file
            function_to_apply : The function in which the processing will be applied. Remember, this function should
            take opencv frame i.e. a numpy array (nd.array) as the input and will return the same i.e. a numpy array.
        Example usage :
            process_input_video_give_video_output("input_video_path", "output_video_path",
            handlle_nils_field_segmentation)
        Returns:
            None
        """

        vidcap = cv2.VideoCapture(input_loc)  # read the video
        get_fps = VideoOperation.compute_frame_per_sec_rate(vidcap)

        # Log the time
        time_start = time.time()

        # Start capturing the feed
        cap = cv2.VideoCapture(input_loc)

        # Find the number of frames
        video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
        print("Number of frames: ", video_length)
        count = 0
        print("Converting video..\n")

        # Just to get the size of image frames
        size = (0, 0)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                continue
            else:
                size = (frame.shape[1], frame.shape[0])
                # cap.release()  # Release the feed
                break

        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        out = cv2.VideoWriter(output_loc, fourcc, get_fps, size)

        # Start converting the video
        while cap.isOpened():
            # Extract the frame
            ret, frame = cap.read()
            if not ret:
                print("Done processing the BAD frame %d" % count)

                if count > (video_length - 1):
                    time_end = time.time()  # Log the time again
                    cap.release()  # Release the feed

                    print("It took %d seconds for conversion and last frame was BAD" % (time_end - time_start))
                    break
                count = count + 1
                continue

            # get_mask_2 = ColorProcessing.compute_field_mask_cvprw_2018(frame, "threshold_approximation")
            # masked_2 = cv2.bitwise_and(frame, frame, mask=get_mask_2)

            masked_2 = function_to_apply(frame)
            out.write(masked_2)
            print("Done processing the GOOD frame %d" % count)

            count = count + 1

            # If there are no more frames left
            if count > (video_length - 1):
                time_end = time.time()  # Log the time again
                cap.release()  # Release the feed

                print("Done extracting frames.\n%d frames extracted" % count)
                print("It took %d seconds for conversion." % (time_end - time_start))
                break

        out.release()
