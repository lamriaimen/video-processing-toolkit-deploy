import subprocess
from .video_processing import compute_frame_per_sec_rate

def get_clip(input_filename, output_filename, start_time, end_time):
    """
    Cuts a video using ffmpeg while preserving the original framerate and 
    forcing one I-frame per second for clean frame extraction.

    Args:
        input_filename (str): Path to the input video.
        output_filename (str): Path to save the output video.
        start_time (float): Start time in seconds.
        end_time (float): End time in seconds.
    """
    framerate = compute_frame_per_sec_rate(input_filename)
    gop_size = int(framerate)

    command = [
        "ffmpeg",
        "-y",                           # Overwrite output file without asking
        "-ss", str(start_time),        # Start time of the clip (in seconds)
        "-to", str(end_time),          # End time of the clip
        "-i", input_filename,          # Input video file
        "-r", str(framerate),          # Set output video framerate
        "-c:v", "libx264",             # Encode video using H.264 codec
        "-crf", "23",                  # Constant Rate Factor (quality setting, lower is better quality)
        "-g", str(gop_size),           # Group of Pictures size (distance between I-frames)
        "-keyint_min", str(gop_size), # Minimum interval between I-frames (set equal to GOP size for forced I-frame interval)
        "-sc_threshold", "0",         # Scene change threshold (0 disables scene detection for I-frames)
        "-preset", "slow",            # Compression efficiency vs. speed
        "-movflags", "+faststart",    # Optimize MP4 for web streaming
        "-c:a", "aac",                # Encode audio using AAC codec
        output_filename               # Output video file path
    ]

    subprocess.run(command, check=True)

def cut_video_clips(input_filename, output_file_path, time_stamp_start_1, time_stamp_end_1):
        """
        Function to read several start and end time stamps, mentioned in two vectors; "time_stamp_start_1" and
        "time_stamp_end_1", to crop the video clips based on these start and end time stamps.

        Args:
            input_filename (str): Path of the input video file
            output_file_path (str): The path of the output file clip
            time_stamp_start_1 (List[str]): The list of start time in HH:MM:SS format
            time_stamp_end_1 (List[str]): The list of end time in HH:MM:SS format.
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