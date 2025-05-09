import argparse
import os
import cv2
import time
import ffmpy
import numpy as np
import subprocess

def get_frame_types(video_file):
    """
    Function to extract the type of each frame in a video using ffprobe
    The frame types are typically:
    - 'I' (Intra-coded): A full image.
    - 'P'(Predicted): Stores only the difference from the previous frame.
    - 'B' (Bidirectional): Stores differences using both previous and next frames.
    Args:
        video_file (str): Path to the input video file.
    Returns:
        Zip: A zip object containing tuples of (frame_index, frame_type),
             where frame_index is an integer and frame_type is a string ('I', 'P', 'B').
    """
    command = 'ffprobe -v error -show_entries frame=pict_type -of default=noprint_wrappers=1'.split()
    out = subprocess.check_output(command + [video_file]).decode()
    frame_types = out.replace('pict_type=', '').split()
    return zip(range(len(frame_types)), frame_types)


def save_all_i_keyframes(video_file, path_out):
    """Function to extract and save all I-frames of a complete video as image files.
    Args:
        video_file(str): Path to the input video file.
        path_out(str): Directory where the extracted frames will be saved.
    Returns: 
        None
    """
    frame_types = get_frame_types(video_file)
    i_frames = [x[0] for x in frame_types if x[1] == 'I']

    if i_frames:
        # basename = os.path.splitext(os.path.basename(video_file))[0]
        cap = cv2.VideoCapture(video_file)

        blank_cnt = 0
        for frame_no in i_frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
            ret, frame = cap.read()

            create_img_name = "/" + str(blank_cnt) + "frame_" + str(frame_no) + ".jpg"

            full_frame_saving_path = path_out + create_img_name
            cv2.imwrite(full_frame_saving_path, frame)

            print('Saved: ' + full_frame_saving_path)

            blank_cnt = blank_cnt + 1
        cap.release()
        print("Done extracting frames.\n%d frames extracted" % blank_cnt)
    else:
        print('No I-frames in ' + video_file)


def save_all_i_keyframes_between_two_timestamps(video_file, path_out, hh_mm_ss_start, hh_mm_ss_end):
    """Function to extract and save all the I-frames of a complete video as image files between two timestamps.
    Args:
        video_file(str): Path to the input video file.
        path_out(str): The output folder to save all the output frames
        hh_mm_ss_start(str): the time starting time stamp
        hh_mm_ss_end(str): the time ending time stamp
    Returns:
        None
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

    frame_types = get_frame_types(video_file)
    i_frames = [x[0] for x in frame_types if x[1] == 'I']
    if i_frames:

        blank_cnt = 0
        for frame_no in i_frames:
            if first_available_frame_index <= frame_no <= last_available_frame_index:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
                ret, frame = cap.read()

                create_img_name = "/" + str(blank_cnt) + "frame_" + str(frame_no) + ".jpg"

                full_frame_saving_path = path_out + "/" + create_img_name
                cv2.imwrite(full_frame_saving_path, frame)

                # print('Saved: ' + full_frame_saving_path)

                blank_cnt = blank_cnt + 1
        cap.release()
        print("Done extracting frames.\n%d frames extracted" % blank_cnt)
    else:
        print('No I-frames in ' + video_file)


def save_all_p_keyframes(video_file, path_out):
    """Function to extract all P-frames from a complete video as image files.
    Args:
        video_file(str): Path to the input video file.
        path_out(str): Directory where the extracted frames will be saved.

    Returns:
        None
    """
    frame_types = get_frame_types(video_file)
    i_frames = [x[0] for x in frame_types if x[1] == 'P']
    if i_frames:
        # basename = os.path.splitext(os.path.basename(video_file))[0]
        cap = cv2.VideoCapture(video_file)

        blank_cnt = 0
        for frame_no in i_frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
            ret, frame = cap.read()

            create_img_name = "/" + str(blank_cnt) +"frame_" + str(frame_no) + ".jpg"

            full_frame_saving_path = path_out + "/" + create_img_name
            cv2.imwrite(full_frame_saving_path, frame)

            # print('Saved: ' + full_frame_saving_path)

            blank_cnt = blank_cnt + 1
        cap.release()
        print("Done extracting frames.\n%d frames extracted" % blank_cnt)
    else:
        print('No P-frames in ' + video_file)


def save_all_p_keyframes_between_two_timestamps(video_file, path_out, hh_mm_ss_start, hh_mm_ss_end):
    """Function to extract  and save all the p-key frames of a complete video
    Args:
        video_file(str): Path to the input video file.
        path_out(str): Directory where the extracted frames will be saved.
        hh_mm_ss_start(str): the time starting time stamp
        hh_mm_ss_end(str): the time ending time stamp
    Returns:
        None
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

    frame_types = get_frame_types(video_file)
    i_frames = [x[0] for x in frame_types if x[1] == 'P']
    if i_frames:

        blank_cnt = 0
        for frame_no in i_frames:
            if first_available_frame_index <= frame_no <= last_available_frame_index:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
                ret, frame = cap.read()

                create_img_name = "/" + str(blank_cnt) + "frame_" + str(frame_no) + ".jpg"

                full_frame_saving_path = path_out + "/" + create_img_name
                cv2.imwrite(full_frame_saving_path, frame)

                # print('Saved: ' + full_frame_saving_path)

                blank_cnt = blank_cnt + 1
        cap.release()
        print("Done extracting frames.\n%d frames extracted" % blank_cnt)
    else:
        print('No P-frames in ' + video_file)


def convert_video(inputed_file):
    """Function to convert the video file into .avi format and save it into current project directory
    Args:
        inputed_file(str): Path of the input video file

    Returns:
        str: The name of the output video file, which automatically takes the name from current time and save the
        file into current project folder
    """
    current_time = time.strftime("%Y%m%d-%H%M%S")
    video_name = str(current_time) + ".avi"
    ff = ffmpy.FFmpeg(inputs={inputed_file: None}, outputs={video_name: ' -c:a mp3 -c:v mpeg4'})
    ff.cmd
    ff.run()
    return video_name


def compute_frame_per_sec_rate(video_file: str) -> int:
    """Function to compute the frame per seconds or pfs
    Args:
        video_file (str): Path of the video file

    Returns:
        int : The Frame rate of the created video stream
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


def frames_to_video(input_path, output_path, fps):
    """Function reads all the individual frames, saved in a directory and then use them to create a video
    Args:
        input_path(str): Path of the directory where the images or frames are saved
        fps(int): The Frame rate of the created video stream.
        output_path(str): The path where the constructed video will be saved
    Returns:
        None
    """
    image_array = []
    files = [f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f))]
    files.sort(key=lambda x: int(x.split("_")[1].split(".")[0])) 
       
    for i in range(len(files)):
        img = cv2.imread(input_path + files[i])
        size = (img.shape[1], img.shape[0])

        img = cv2.resize(img, size)
        image_array.append(img)

    fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
    out = cv2.VideoWriter(output_path, fourcc, fps, size)

    for i in range(len(image_array)):
        out.write(image_array[i])
    out.release()


def video_to_all_frames(input_loc, output_loc):
    """Function to extract all the frames from input video file
    and save them as separate frames in an output directory.

    Args:
        input_loc (str): Path to the input video file.
        output_loc (str): Directory where the frames will be saved.

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


def extract_images_regular_interval(path_in, path_out, time_interval_in_sec):
    """Function to extract the frames in every given "time_interval" e.g. 1 sec, 5 sec etc. from input video file
    and save them as separate frames in an output directory.
    Args:
        path_in(str): Input video file.
        path_out(str): Directory where the extracted frames will be saved.
        time_interval_in_sec(int): the time interval of the sampling, mention in seconds; we convert it into milliseconds
        
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


def extract_images_at_particular_timestamp(path_in, path_out, hh_mm_ss):
    """Function to extract the frame at a particular time stamp; Need to know the number of frames per second and the
    timestamp in the video , we want to take frame from, we can easily calculate the frame number we want
    Args:
        path_in(str): Input video file.
        path_out (str): Directory where the extracted frame will be saved.
        hh_mm_ss(str): The timestamp in "HH:MM:SS" format where the frame should be extracted.
        
    Returns:
        None
    """
    # video_avi = convert_video(path_in)  # convert into video_avi file first to facilitate the reading of video file
    vidcap = cv2.VideoCapture(path_in)  # read the video

    time_data_split = hh_mm_ss.split(":")
    get_hours = int(time_data_split[0])
    get_mins = int(time_data_split[1])
    get_secs = int(time_data_split[2])

    time_in_millisec = (get_hours * 60 * 60 + get_mins * 60 + get_secs) * 1000
    time_in_sec = (get_hours * 60 * 60 + get_mins * 60 + get_secs)
    get_fps = int(compute_frame_per_sec_rate(vidcap))

    # See carefully, the following multiplication will give the last frame of time stamp 'time_in_sec'. Because on
    # second 1, we will have 30 frames (e.g. FPS = 30), on second 2, we will have 2*30 = 60 frames then on 'time_in_sec'
    # we will have time_in_sec*30 frames. So the following multiplication will give the last frame of the `time_in_sec`
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


def extract_images_between_two_timestamps(path_in, path_out, hh_mm_ss_start, hh_mm_ss_end):
    """Function to extract all the frames within two timestamps; Need to know the number of frames per second and the
    start and end timestamp in the video
    Args:
        path_in(str): Path to the input video file.
        path_out(str): Directory where the extracted frames will be saved.
        hh_mm_ss_start (str): The start timestamp in "HH:MM:SS" format.
        hh_mm_ss_end (str): The end timestamp in "HH:MM:SS" format.
        

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
    # after 17th sec  is completed is 17 * 30 = 510 (by taking an example of 30  fps video)
    # Hence, at the end of 16th sec, we wil traverse 16 * 30 = 480 frames. So, the 17th sec frame counting will start
    # from 481 th frame
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


def extract_regular_interval_images_between_two_timestamps(path_in, path_out, hh_mm_ss_start, hh_mm_ss_end,
                                                           time_interval_in_sec):
    """Function to extract frames after given regular intervals within two timestamps; Need to know the number of
    frames per second and the start and end timestamp in the video
    Args:
        path_in (str): Path to the input video file.
        path_out (str): Directory where the extracted frames will be saved.
        hh_mm_ss_start (str): The start timestamp in "HH:MM:SS" format.
        hh_mm_ss_end (str): The end timestamp in "HH:MM:SS" format.
        time_interval_in_sec (int): The time interval (in seconds) between each frame extraction.
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

    # time_in_millisec_end = (get_hours_end * 60 * 60 + get_mins_end * 60 + get_secs_end)*1000
    time_in_sec_end = (get_hours_end * 60 * 60 + get_mins_end * 60 + get_secs_end)
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))  # get the frame per seconds

    success = True

    # let's say, we need to compute from 17th sec of the video. Hence, the number of frames will be traversed
    # after 17th sec  is completed is 17 * 30 = 510 (by taking an example of 30  fps video)
    # Hence, at the end of 16th sec, we wil traverse 16 * 30 = 480 frames. So, the 17th sec frame counting will start
    # from 481 th frame
    count = ((time_in_sec_start * fps) - fps) + 1
    last_available_frame = time_in_sec_end * fps

    # at each time stamp, we have fps number of frames. Hence, at the last time stamp, we will have :
    # (time_in_sec_end * fps) number of frames

    time_interval_in_millisec = time_interval_in_sec * 1000

    blank_cnt = 0
    while success:

        frame_pointer = time_in_millisec_start + (blank_cnt * time_interval_in_millisec)

        if frame_pointer > (time_in_sec_end * 1000):
            break
        # setting the pointer to read from this time stamp
        vidcap.set(cv2.CAP_PROP_POS_MSEC, frame_pointer)
        # Extract the frames
        success, frame = vidcap.read()
        if not success:
            continue

        print('Read a new frame: ', success)
        cv2.imwrite(path_out + "/%#05d.jpg" % count, frame)  # save frame as JPEG file

        count = count + 1
        blank_cnt = blank_cnt + 1

        # If there are no more frames left
        # if count > last_available_frame:
    vidcap.release()  # Release the feed
    print("Done extracting frames.\n%d frames extracted" % count)
    # break


def main():
    print("This is only a test")
    input_loc = '/home/tanmoymondal/Videos/FootBall_Video_Data/669/clips/0_37_56-0_52_0.mp4'
    output_loc_1 = '/home/tanmoymondal/Videos/FootBall_Video_Data/669/clips/save_all_frames/'

    output_loc_2 = '/home/tanmoymondal/Videos/FootBall_Video_Data/669/clips/save_frames_regular_time_interval/'
    output_loc_3 = '/home/tanmoymondal/Videos/FootBall_Video_Data/669/clips/save_image_particular_timestamp/'
    output_loc_4 = "/home/tanmoymondal/Videos/FootBall_Video_Data/669/clips/save_frames_between_timestamps/"
    output_loc_5 = "/home/tanmoymondal/Videos/FootBall_Video_Data/669/clips/save_frames_bet_tstamps_regular_interval/"
    output_loc_6 = "/home/tanmoymondal/Videos/FootBall_Video_Data/669/clips/save_all_i_frames/"
    output_loc_7 = "/home/tanmoymondal/Videos/FootBall_Video_Data/669/clips/save_all_p_frames/"

    # video_to_all_frames(input_loc, output_loc_1)  # WORKING
    # extract_images_regular_interval(input_loc, output_loc_2, 5)  # WORKING
    # extract_images_at_particular_timestamp(input_loc, output_loc_3, "00:09:40")  # WORKING
    # extract_images_between_two_timestamps(input_loc, output_loc_4, "00:05:30", "00:09:40")  # WORKING
    # extract_regular_interval_images_between_two_timestamps(input_loc, output_loc_5, "00:05:30", "00:09:40", 5)
    # frames_to_video(input_loc, output_loc)

    # save_all_i_keyframes(input_loc, output_loc_6)
    save_all_i_keyframes_between_two_timestamps(input_loc, output_loc_6, "00:05:30", "00:09:40")

    # save_all_p_keyframes(input_loc, output_loc_7)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PyTorch Template')

    args = parser.parse_args()
    main()
