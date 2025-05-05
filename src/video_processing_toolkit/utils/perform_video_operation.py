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

time_stamp_start = ['00:16:50', '00:19:20', '00:20:08', '00:21:15', '00:23:26', '00:25:40', '00:25:45', '00:25:56',
                    '00:26:17', '00:27:50', '00:31:42', '00:32:09', '00:33:05', '00:33:26', '00:35:22', '00:36:17',
                    '00:36:24', '00:38:47', '00:42:10', '00:42:38', '00:44:46', '00:45:40', '00:45:54', '00:47:30',
                    '00:48:50', '00:49:54', '00:50:00', '00:52:20', '00:52:24', '01:10:27', '01:10:55', '01:13:27',
                    '01:20:00', '01:22:05', '01:25:28', '01:25:40', '01:25:48', '01:25:56', '01:26:04', '01:26:11',
                    '01:26:17', '01:26:23', '01:27:25', '01:27:30', '01:29:17', '01:34:09', '01:37:52', '01:38:02',
                    '01:38:08', '01:38:21', '01:41:07', '01:41:13', '01:43:42', '01:45:40', '01:47:10', '01:50:15',
                    '01:53:00', '01:53:06', '01:56:48', '01:57:08', '01:59:20']

time_stamp_end = ['00:16:55', '00:19:30', '00:20:11', '00:21:21', '00:23:32', '00:25:44', '00:25:48', '00:25:59',
                  '00:26:20', '00:27:55', '00:31:50', '00:32:15', '00:33:12', '00:33:32', '00:35:30', '00:36:24',
                  '00:36:28', '00:38:58', '00:42:15', '00:42:49', '00:44:52', '00:45:50', '00:45:60', '00:47:40',
                  '00:48:55', '00:49:58', '00:50:03', '00:52:24', '00:52:27', '01:10:33', '01:11:03', '01:13:34',
                  '01:20:05', '01:22:12', '01:25:34', '01:25:45', '01:25:52', '01:26:03', '01:26:07', '01:26:14',
                  '01:26:20', '01:26:27', '01:27:28', '01:27:32', '01:29:22', '01:34:14', '01:37:58', '01:38:06',
                  '01:38:11', '01:38:24', '01:41:10', '01:41:17', '01:43:47', '01:45:43', '01:47:15', '01:50:20',
                  '01:53:05', '01:53:14', '01:56:56', '01:57:14', '01:59:25']

time_stamp_start_swim_1 = ['00:07:38', '00:22:09', '00:31:01', '01:04:44', '01:22:50', '01:34:42', '01:29:04',
                           '01:48:47', '02:03:45', '02:07:24', '02:23:56', '02:40:17']

time_stamp_end_swim_1 = ['00:18:17', '00:32:15', '00:41:40', '01:14:11', '01:32:55', '01:44:50', '01:40:04',
                         '01:58:50', '02:13:40', '02:17:30', '02:35:59', '02:50:20']


class VideoOperation:

    def __init__(self):
        print(" I am inside init function of test file ")

    @staticmethod
    def get_frame_types(video_file):
        """
        Function to get the type of video
        Args:
            video_file: Path of the input video file. We need this function to get the i-frames and p-frames
        Returns:

        """
        command = 'ffprobe -v error -show_entries frame=pict_type -of default=noprint_wrappers=1'.split()
        out = subprocess.check_output(command + [video_file]).decode()
        frame_types = out.replace('pict_type=', '').split()
        return zip(range(len(frame_types)), frame_types)

    @staticmethod
    def get_clip(input_filename, output_filename, start_time, end_time):
        """
        Function to actually cut the video clips
        Args:
            input_filename: Path of the input video file
            output_filename: The path of the output file clip
            start_time: The start time stamp
            end_time: The end time stamp
        Returns:

        """
        ffmpeg_extract_subclip(input_filename, start_time, end_time, targetname=output_filename)

    @staticmethod
    def cut_video_clips(input_filename, output_file_path, time_stamp_start_1, time_stamp_end_1):

        """
        Function to read several start and end time stamps, mentioned in two vectors; "time_stamp_start_1" and
        "time_stamp_end_1", to crop the video clips based on these start and end time stamps
        Args:
            input_filename: Path of the input video file
            output_file_path: The path of the output file clip
            time_stamp_start_1 : The list of start time in HH:MM:SS format
            time_stamp_end_1 : The list of end time in HH:MM:SS format
        Returns:

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
    def convert_video(inputted_file):
        """Function to convert the video file into .avi format and save it into current project directory
        Args:
            inputted_file: Path of the input video file

        Returns:
            video_name: The name of the output video file, which automatically takes the name from current time and
            save the file into current project folder
        """
        current_time = time.strftime("%Y%m%d-%H%M%S")
        video_name = str(current_time) + ".avi"
        ff = ffmpy.FFmpeg(inputs={inputted_file: None}, outputs={video_name: ' -c:a mp3 -c:v mpeg4'})
        ff.cmd
        ff.run()
        return video_name

    @staticmethod
    def compute_frame_per_sec_rate(video_file):
        """Function to compute the frame per seconds or pfs
        Args:
            video_file: Path of the video file

        Returns:
            fps: The Frame rate of the created video stream
        """
        # Find OpenCV version
        (major_ver, minor_ver, subminor_ver) = cv2.__version__.split('.')

        if int(major_ver) < 3:
            fps = video_file.get(cv2.cv.CV_CAP_PROP_FPS)
            print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
        else:
            fps = video_file.get(cv2.CAP_PROP_FPS)
            print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
        # video_file.release()

        return fps

    @staticmethod
    def frames_to_video(input_path, output_path, fps):
        """Function reads all the individual frames, saved in a directory and then use them to create a video
        Args:
            input_path: Path of the directory where the images or frames are saved
            fps: The Frame rate of the created video stream.
            output_path: The path where the constructed video will be saved
        Returns:
            None
        """
        image_array = []
        files = [f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f))]
        files.sort(key=lambda x: int(x[5:-4]))

        for i in range(len(files)):
            img = cv2.imread(input_path + files[i])
            size = (img.shape[1], img.shape[0])

            img = cv2.resize(img, size)
            image_array.append(img)

        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        out = cv2.VideoWriter(output_path, fourcc, fps, size)

        for i in range(len(image_array)):
            out.write(image_array[i])
        out.release()

    @staticmethod
    def video_to_all_frames(input_loc, output_loc):
        """Function to extract all the frames from input video file
        and save them as separate frames in an output directory.
        Args:
            input_loc: Input video file.
            output_loc: Output directory to save the frames.
        Returns:
            None
        """
        try:
            os.mkdir(output_loc)
        except OSError:
            pass
        # Log the time
        time_start = time.time()

        # Start capturing the feed
        cap = cv2.VideoCapture(input_loc)

        # Find the number of frames
        video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
        print("Number of frames: ", video_length)
        count = 0
        print("Converting video..\n")

        # Start converting the video
        while cap.isOpened():
            # Extract the frame
            ret, frame = cap.read()
            if not ret:
                continue

            cv2.imwrite(output_loc + "/%#05d.jpg" % (count + 1), frame)  # Write the results back to output location.
            count = count + 1

            # If there are no more frames left
            if count > (video_length - 1):
                time_end = time.time()  # Log the time again
                cap.release()  # Release the feed

                print("Done extracting frames.\n%d frames extracted" % count)
                print("It took %d seconds for conversion." % (time_end - time_start))
                break

    @staticmethod
    def extract_images_regular_interval(path_in, path_out, time_interval_in_sec):
        """Function to extract the frames in every given "time_interval" e.g. 1 sec, 5 sec etc. from input video file
        and save them as separate frames in an output directory.
        Args:
            path_in: Input video file.
            time_interval_in_sec: the time interval of the sampling, mention in seconds; we convert it into milliseconds
            path_out: Output directory to save the frames.
        Returns:
            None
        Resources:
               https://www.futurelearn.com/info/courses/introduction-to-image-analysis-for-plant-phenotyping/0/steps/305359
        """
        count = 0
        vidcap = cv2.VideoCapture(path_in)
        success = True
        time_interval_in_millisec = time_interval_in_sec * 1000  # converting it into milliseconds

        # Another way to extract the frame, without finding the frame number,
        # is by using the time in milliseconds directly using CAP_PROP_POS_MSEC instead
        while success:
            vidcap.set(cv2.CAP_PROP_POS_MSEC, (count * time_interval_in_millisec))
            success, image = vidcap.read()
            if not success:
                continue
            else:
                print('Read a new frame: ', success)

            cv2.imwrite(path_out + "/%#05d.jpg" % (count + 1), image)  # save frame as JPEG file
            count = count + 1
        vidcap.release()

    @staticmethod
    def extract_images_at_particular_timestamp(path_in, path_out, hh_mm_ss):
        """Function to extract the frame at a particular time stamp; Need to know the number of frames per second and the
        timestamp in the video , we want to take frame from, we can easily calculate the frame number we want
        Args:
            path_in: Input video file.
            hh_mm_ss: the time
            path_out: Output directory to save the frames.
        Returns:
            None
        """
        # video_avi = convert_video(path_in)  # convert into video_avi first to facilitate the reading of video file
        vidcap = cv2.VideoCapture(path_in)  # read the video

        time_data_split = hh_mm_ss.split(":")
        get_hours = int(time_data_split[0])
        get_mins = int(time_data_split[1])
        get_secs = int(time_data_split[2])

        time_in_millisec = (get_hours * 60 * 60 + get_mins * 60 + get_secs) * 1000
        time_in_sec = (get_hours * 60 * 60 + get_mins * 60 + get_secs)
        get_fps = int(VideoOperation.compute_frame_per_sec_rate(vidcap))

        # See carefully, the following multiplication will give the last frame of time stamp 'time_in_sec'. Because
        # on second 1, we will have 30 frames (e.g. FPS = 30), on second 2, we will have 2*30 = 60 frames then on
        # 'time_in_sec' we will have time_in_sec*30 frames. So the following multiplication will give the last frame
        # of the `time_in_sec`
        frame_id = int(get_fps * time_in_sec)
        count = 0

        while vidcap.isOpened():
            vidcap.set(cv2.CAP_PROP_POS_MSEC, time_in_millisec)
            success, image = vidcap.read()
            if not success:
                count = count + 1
                continue
            else:
                print('Read a new frame: ', success)
                cv2.imwrite(path_out + "/%#05d.jpg" % (frame_id + count), image)  # save frame as JPEG file
                break

        vidcap.release()

    @staticmethod
    def extract_images_between_two_timestamps(path_in, path_out, hh_mm_ss_start, hh_mm_ss_end):
        """Function to extract all the frames within two timestamps; Need to know the number of frames per second and the
        start and end timestamp in the video
        Args:
            path_in: Input video file.
            hh_mm_ss_start: the time starting time stamp
            hh_mm_ss_end: the time ending time stamp
            path_out: Output directory to save the frames.

        Returns:
            None
        """
        vidcap = cv2.VideoCapture(path_in)  # read the video

        time_data_split_start = hh_mm_ss_start.split(":")
        get_hours_start = int(time_data_split_start[0])
        get_mins_start = int(time_data_split_start[1])
        get_secs_start = int(time_data_split_start[2])

        time_in_millisec_start = (get_hours_start * 60 * 60 + get_mins_start * 60 + get_secs_start) * 1000
        time_in_sec_start = (get_hours_start * 60 * 60 + get_mins_start * 60 + get_secs_start)

        time_data_split_end = hh_mm_ss_end.split(":")
        get_hours_end = int(time_data_split_end[0])
        get_mins_end = int(time_data_split_end[1])
        get_secs_end = int(time_data_split_end[2])

        # time_in_millisec_end = (get_hours_end * 60 * 60 + get_mins_end*60 + get_secs_end)*1000
        time_in_sec_end = (get_hours_end * 60 * 60 + get_mins_end * 60 + get_secs_end)

        fps = int(vidcap.get(cv2.CAP_PROP_FPS))  # get the frame per seconds
        vidcap.set(cv2.CAP_PROP_POS_MSEC, time_in_millisec_start)  # setting the pointer to read from this time stamp

        success = True

        # let's say, we need to compute from 17th sec of the video. Hence, the number of frames will be traversed
        # after 17th sec  is completed is 17 * 30 = 510 (by taking an example of 30  fps video) Hence, at the end of
        # 16th sec, we wil traverse 16 * 30 = 480 frames. So, the 17th sec frame counting will start from 481 th frame
        count = ((time_in_sec_start * fps) - fps) + 1
        last_available_frame = time_in_sec_end * fps

        # at each time stamp, we have fps number of frames. Hence, at the last time stamp, we will have :
        # (time_in_sec_end * fps) number of frames
        while success:
            # Extract the frames
            success, frame = vidcap.read()
            if not success:
                continue
            print('Read a new frame: ', success)
            cv2.imwrite(path_out + "/%#05d.jpg" % (count + 1), frame)  # save frame as JPEG file
            count = count + 1

            # If there are no more frames left
            if count > last_available_frame:
                vidcap.release()  # Release the feed
                print("Done extracting frames.\n%d frames extracted" % count)
                break

    @staticmethod
    def extract_regular_interval_images_between_two_timestamps(path_in, path_out, hh_mm_ss_start, hh_mm_ss_end,
                                                               time_interval_in_sec):
        """Function to extract frames after given regular intervals within two timestamps; Need to know the number of
        frames per second and the start and end timestamp in the video
        Args:
            path_in: Input video file.
            hh_mm_ss_start: the time starting time stamp
            hh_mm_ss_end: the time ending time stamp
            time_interval_in_sec: The regular time interval
            path_out: Output directory to save the frames.
        Returns:
            None
        """
        vidcap = cv2.VideoCapture(path_in)  # read the video

        time_data_split_start = hh_mm_ss_start.split(":")
        get_hours_start = int(time_data_split_start[0])
        get_mins_start = int(time_data_split_start[1])
        get_secs_start = int(time_data_split_start[2])

        time_in_millisec_start = (get_hours_start * 60 * 60 + get_mins_start * 60 + get_secs_start) * 1000
        time_in_sec_start = (get_hours_start * 60 * 60 + get_mins_start * 60 + get_secs_start)

        time_data_split_end = hh_mm_ss_end.split(":")
        get_hours_end = int(time_data_split_end[0])
        get_mins_end = int(time_data_split_end[1])
        get_secs_end = int(time_data_split_end[2])

        time_in_millisec_end = (get_hours_end * 60 * 60 + get_mins_end * 60 + get_secs_end) * 1000
        time_in_sec_end = (get_hours_end * 60 * 60 + get_mins_end * 60 + get_secs_end)
        fps = int(vidcap.get(cv2.CAP_PROP_FPS))  # get the frame per seconds

        success = True

        # let's say, we need to compute from 17th sec of the video. Hence, the number of frames will be traversed
        # after 17th sec  is completed is 17 * 30 = 510 (by taking an example of 30  fps video) Hence, at the end of
        # 16th sec, we wil traverse 16 * 30 = 480 frames. So, the 17th sec frame counting will start from 481 th frame
        count = ((time_in_sec_start * fps) - fps) + 1
        last_available_frame = time_in_sec_end * fps

        # at each time stamp, we have fps number of frames. Hence, at the last time stamp, we will have :
        # (time_in_sec_end * fps) number of frames

        time_interval_in_millisec = time_interval_in_sec * 1000

        blank_cnt = 0
        while success:

            frame_pointer = time_in_millisec_start + (blank_cnt * time_interval_in_millisec)

            # setting the pointer to read from this time stamp
            vidcap.set(cv2.CAP_PROP_POS_MSEC, frame_pointer)
            # Extract the frames
            success, frame = vidcap.read()
            if not success:
                continue
            print('Read a new frame: ', success)

            # convert from millisecond to seconds and then into HH:MM:SS format
            time_format = str(timedelta(seconds=int(frame_pointer / 1000)))

            # create_img_name = str(blank_cnt) + "::" + str(get_hours_start) + "_" + str(get_mins_start) + "_" + \
            #     str(get_secs_start) + "-" + str(get_hours_end) + "_" + str(get_mins_end) + "_" + str(get_secs_end) + \
            #     "-frame_1.jpg"

            create_img_name = str(blank_cnt) + "::" + time_format + "-frame_1.jpg"

            full_frame_saving_path = path_out + "/" + create_img_name

            cv2.imwrite(full_frame_saving_path, frame)  # save frame as JPEG file

            count = count + 1
            blank_cnt = blank_cnt + 1

            # If there are no more frames left
            if frame_pointer > time_in_millisec_end:
                break

        vidcap.release()  # Release the feed
        print("Done extracting frames.\n%d frames extracted" % count)
        # break

    @staticmethod
    def save_all_i_keyframes(video_file, path_out):
        """Function to extract  and save all the i-key frames of a complete video
        Args:
            video_file: Input video file.
            path_out: The output folder to save all the output frames
        Returns:
            None
        Resources:
            URL: https://stackoverflow.com/questions/42798634/extracting-keyframes-python-opencv
            URL: https://stackoverflow.com/questions/33311153/python-extracting-and-saving-video-frames
        """
        frame_types = VideoOperation.get_frame_types(video_file)
        i_frames = [x[0] for x in frame_types if x[1] == 'I']
        if i_frames:
            # basename = os.path.splitext(os.path.basename(video_file))[0]
            cap = cv2.VideoCapture(video_file)

            blank_cnt = 0
            for frame_no in i_frames:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
                ret, frame = cap.read()

                create_img_name = str(blank_cnt) + "::" + "-frame_" + str(frame_no) + ".jpg"

                full_frame_saving_path = path_out + "/" + create_img_name
                cv2.imwrite(full_frame_saving_path, frame)

                # print('Saved: ' + full_frame_saving_path)

                blank_cnt = blank_cnt + 1
            cap.release()
            print("Done extracting frames.\n%d frames extracted" % blank_cnt)
        else:
            print('No I-frames in ' + video_file)

    @staticmethod
    def save_all_i_keyframes_between_two_timestamps(video_file, path_out, hh_mm_ss_start, hh_mm_ss_end):
        """Function to extract  and save all the i-key frames of a complete video
        Args:
            video_file: Input video file.
            path_out: The output folder to save all the output frames
            hh_mm_ss_start: the time starting time stamp
            hh_mm_ss_end: the time ending time stamp
        Returns:
            None
        Resources:
            URL : https://stackoverflow.com/questions/42798634/extracting-keyframes-python-opencv
            URL: https://stackoverflow.com/questions/33311153/python-extracting-and-saving-video-frames
        """
        # basename = os.path.splitext(os.path.basename(video_file))[0]
        cap = cv2.VideoCapture(video_file)

        time_data_split_start = hh_mm_ss_start.split(":")
        get_hours_start = int(time_data_split_start[0])
        get_mins_start = int(time_data_split_start[1])
        get_secs_start = int(time_data_split_start[2])

        time_in_millisec_start = (get_hours_start * 60 * 60 + get_mins_start * 60 + get_secs_start) * 1000
        time_in_sec_start = (get_hours_start * 60 * 60 + get_mins_start * 60 + get_secs_start)

        time_data_split_end = hh_mm_ss_end.split(":")
        get_hours_end = int(time_data_split_end[0])
        get_mins_end = int(time_data_split_end[1])
        get_secs_end = int(time_data_split_end[2])

        time_in_millisec_end = (get_hours_end * 60 * 60 + get_mins_end * 60 + get_secs_end) * 1000
        time_in_sec_end = (get_hours_end * 60 * 60 + get_mins_end * 60 + get_secs_end)
        fps = int(cap.get(cv2.CAP_PROP_FPS))  # get the frame per seconds

        # number of frames in video
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # let's say, we need to compute from 17th sec of the video. Hence, the number of frames will be traversed
        # after 17th sec  is completed is 17 * 30 = 510 (by taking an example of 30  fps video) Hence, at the end of
        # 16th sec, we wil traverse 16 * 30 = 480 frames. So, the 17th sec frame counting will start from 481 th frame
        first_available_frame_index = ((time_in_sec_start * fps) - fps) + 1
        last_available_frame_index = time_in_sec_end * fps

        frame_types = VideoOperation.get_frame_types(video_file)
        i_frames = [x[0] for x in frame_types if x[1] == 'I']
        if i_frames:

            blank_cnt = 0
            for frame_no in i_frames:
                if first_available_frame_index <= frame_no <= last_available_frame_index:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
                    ret, frame = cap.read()

                    create_img_name = str(blank_cnt) + "::" + "-frame_" + str(frame_no) + ".jpg"

                    full_frame_saving_path = path_out + "/" + create_img_name
                    cv2.imwrite(full_frame_saving_path, frame)

                    # print('Saved: ' + full_frame_saving_path)

                    blank_cnt = blank_cnt + 1
            cap.release()
            print("Done extracting frames.\n%d frames extracted" % blank_cnt)
        else:
            print('No I-frames in ' + video_file)

    @staticmethod
    def save_all_p_keyframes(video_file, path_out):
        """Function to extract  and save all the p-key frames of a complete video
        Args:
            video_file: Input video file.
            path_out: The output folder to save all the output frames

        Returns:
            None
        Resources:
            URL: https://stackoverflow.com/questions/42798634/extracting-keyframes-python-opencv
            URL: https://stackoverflow.com/questions/33311153/python-extracting-and-saving-video-frames
        """
        frame_types = VideoOperation.get_frame_types(video_file)
        i_frames = [x[0] for x in frame_types if x[1] == 'P']
        if i_frames:
            # basename = os.path.splitext(os.path.basename(video_file))[0]
            cap = cv2.VideoCapture(video_file)

            blank_cnt = 0
            for frame_no in i_frames:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
                ret, frame = cap.read()

                create_img_name = str(blank_cnt) + "::" + "-frame_" + str(frame_no) + ".jpg"

                full_frame_saving_path = path_out + "/" + create_img_name
                cv2.imwrite(full_frame_saving_path, frame)

                # print('Saved: ' + full_frame_saving_path)

                blank_cnt = blank_cnt + 1
            cap.release()
            print("Done extracting frames.\n%d frames extracted" % blank_cnt)
        else:
            print('No P-frames in ' + video_file)

    @staticmethod
    def save_all_p_keyframes_between_two_timestamps(video_file, path_out, hh_mm_ss_start, hh_mm_ss_end):
        """Function to extract  and save all the p-key frames of a complete video
        Args:
            video_file: Input video file.
            path_out: The output folder to save all the output frames
            hh_mm_ss_start: the time starting time stamp
            hh_mm_ss_end: the time ending time stamp
        Returns:
            None
        Resources:
            URL: https://stackoverflow.com/questions/42798634/extracting-keyframes-python-opencv
            URL: https://stackoverflow.com/questions/33311153/python-extracting-and-saving-video-frames
        """
        # basename = os.path.splitext(os.path.basename(video_file))[0]
        cap = cv2.VideoCapture(video_file)

        time_data_split_start = hh_mm_ss_start.split(":")
        get_hours_start = int(time_data_split_start[0])
        get_mins_start = int(time_data_split_start[1])
        get_secs_start = int(time_data_split_start[2])

        time_in_millisec_start = (get_hours_start * 60 * 60 + get_mins_start * 60 + get_secs_start) * 1000
        time_in_sec_start = (get_hours_start * 60 * 60 + get_mins_start * 60 + get_secs_start)

        time_data_split_end = hh_mm_ss_end.split(":")
        get_hours_end = int(time_data_split_end[0])
        get_mins_end = int(time_data_split_end[1])
        get_secs_end = int(time_data_split_end[2])

        time_in_millisec_end = (get_hours_end * 60 * 60 + get_mins_end * 60 + get_secs_end) * 1000
        time_in_sec_end = (get_hours_end * 60 * 60 + get_mins_end * 60 + get_secs_end)
        fps = int(cap.get(cv2.CAP_PROP_FPS))  # get the frame per seconds

        # number of frames in video
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # let's say, we need to compute from 17th sec of the video. Hence, the number of frames will be traversed
        # after 17th sec  is completed is 17 * 30 = 510 (by taking an example of 30  fps video) Hence, at the end of
        # 16th sec, we wil traverse 16 * 30 = 480 frames. So, the 17th sec frame counting will start from 481 th frame
        first_available_frame_index = ((time_in_sec_start * fps) - fps) + 1
        last_available_frame_index = time_in_sec_end * fps

        frame_types = VideoOperation.get_frame_types(video_file)
        i_frames = [x[0] for x in frame_types if x[1] == 'P']
        if i_frames:

            blank_cnt = 0
            for frame_no in i_frames:
                if first_available_frame_index <= frame_no <= last_available_frame_index:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
                    ret, frame = cap.read()

                    create_img_name = str(blank_cnt) + "::" + "-frame_" + str(frame_no) + ".jpg"

                    full_frame_saving_path = path_out + "/" + create_img_name
                    cv2.imwrite(full_frame_saving_path, frame)

                    # print('Saved: ' + full_frame_saving_path)

                    blank_cnt = blank_cnt + 1
            cap.release()
            print("Done extracting frames.\n%d frames extracted" % blank_cnt)
        else:
            print('No P-frames in ' + video_file)

    @staticmethod
    def handlle_nils_field_segmentation(frame):

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
        """Function to apply the processing on each frames from input video file
        and create another video
        Args:
            input_loc: Input video file.
            output_loc: The path of output video file

            function_to_apply : The function in which the processing will be applied. Remember, this function should
            take opencv frame i.e. a numpy array (nd.array) as the input and will return the same i.e. a numpy array

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


def main():
    all_dir_path = "/home/tanmoymondal/Videos/FootBall_Video_Data_Server/"

    # VideoOperation.cut_video_clips("/home/tanmoymondal/Videos/Swimming/piscine strasbourg.MP4",
    #                                "/home/tanmoymondal/Videos/Swimming/clip_video/", time_stamp_start_swim_1,
    #                                time_stamp_end_swim_1)

    # VideoOperation.cut_video_clips("/home/tanmoymondal/Videos/Swimming/piscine strasbourg.MP4",
    #                                "/home/tanmoymondal/Videos/Swimming/small_clip_video/", ['00:02:00'], ['00:02:40'])

    VideoOperation.process_all_video_frames_to_output_video(
        "/home/tanmoymondal/Videos/Swimming/small_clip_video/0_2_0-0_2_40.mp4",
        "/home/tanmoymondal/Videos/Swimming/small_clip_video/0_2_0-0_2_40_bgd_removed.mp4", VideoOperation.
        handlle_nils_field_segmentation)

    # img_file_path = "/home/tanmoymondal/Videos/FootBall_Video_Data_Server/5299/i_frames/58::-frame_8820.jpg"
    # ColorProcessing.apply_nils_background_removal_on_image(img_file_path)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print(f'Done...Take {(time.time() - start_time):.4f} (sec)')
