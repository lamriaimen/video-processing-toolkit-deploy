import subprocess

def get_clip(input_filename, output_filename, start_time, end_time):
    """
    Cuts a video using ffmpeg with re-encoding to ensure clean playback.

    Args:
        input_filename (str): Path to the input video.
        output_filename (str): Path to save the output video.
        start_time (float): Start time in seconds.
        end_time (float): End time in seconds.
    """
    command = [
        "ffmpeg",
        "-y",  # Overwrite without asking
        "-ss", str(start_time),
        "-to", str(end_time),
        "-i", input_filename,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-strict", "experimental",
        output_filename
    ]
    subprocess.run(command, check=True)

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

            get_clip(input_filename, output_file_path_complete, total_start_time_in_sec,
                                    total_end_time_in_sec)