video_processing_toolkit
========================

.. py:module:: video_processing_toolkit

.. autoapi-nested-parse::

   Top-level package for Video Processing Toolkit.



Submodules
----------

.. toctree::
   :maxdepth: 1

   /autoapi/video_processing_toolkit/cli/index
   /autoapi/video_processing_toolkit/core/index
   /autoapi/video_processing_toolkit/utils/index
   /autoapi/video_processing_toolkit/visualization/index






Package Contents
----------------

.. py:function:: get_frame_types(video_file)

   Function to extract the type of each frame in a video using ffprobe
   The frame types are typically:
   - 'I' (Intra-coded): A full image.
   - 'P'(Predicted): Stores only the difference from the previous frame.
   - 'B' (Bidirectional): Stores differences using both previous and next frames.
   :param video_file: Path to the input video file.
   :type video_file: str

   :returns:

             A zip object containing tuples of (frame_index, frame_type),
                  where frame_index is an integer and frame_type is a string ('I', 'P', 'B').
   :rtype: zip


.. py:function:: save_all_i_keyframes(video_file, path_out)

   Function to extract and save all I-frames of a complete video as image files.
   :param video_file: Path to the input video file.
   :type video_file: str
   :param path_out: The output folder to save all the extracted frames.
   :type path_out: str

   :returns: None


.. py:function:: save_all_i_keyframes_between_two_timestamps(video_file, path_out, hh_mm_ss_start, hh_mm_ss_end)

   Function to extract and save all the all I-frames of a complete video as image files between two timestamps.
   :param video_file: Path to the input video file.
   :type video_file: str
   :param path_out: The output folder to save all the output frames
   :param hh_mm_ss_start: the time starting time stamp
   :param hh_mm_ss_end: the time ending time stamp

   :returns: None


.. py:function:: save_all_p_keyframes(video_file, path_out)

   Function to extract all P-frames from a complete video as image files.
   :param video_file: Path to the input video file.
   :type video_file: str
   :param path_out: The output folder to save all the output frames

   :returns: None


.. py:function:: save_all_p_keyframes_between_two_timestamps(video_file, path_out, hh_mm_ss_start, hh_mm_ss_end)

   Function to extract  and save all the p-key frames of a complete video
   :param video_file: Input video file.
   :param path_out: The output folder to save all the output frames
   :param hh_mm_ss_start: the time starting time stamp
   :param hh_mm_ss_end: the time ending time stamp

   :returns: None


.. py:function:: convert_video(inputed_file)

   Function to convert the video file into .avi format and save it into current project directory
   :param inputed_file: Path of the input video file

   :returns: The name of the output video file, which automatically takes the name from current time and save the
             file into current project folder
   :rtype: video_name


.. py:function:: compute_frame_per_sec_rate(video_file)

   Function to compute the frame per seconds or pfs
   :param video_file: Path of the video file

   :returns: The Frame rate of the created video stream
   :rtype: fps


.. py:function:: frames_to_video(input_path, output_path, fps)

   Function reads all the individual frames, saved in a directory and then use them to create a video
   :param input_path: Path of the directory where the images or frames are saved
   :param fps: The Frame rate of the created video stream.
   :param output_path: The path where the constructed video will be saved

   :returns: None


.. py:function:: video_to_all_frames(input_loc, output_loc)

   Function to extract all the frames from input video file
   and save them as separate frames in an output directory.
   :param input_loc: Input video file.
   :param output_loc: Output directory to save the frames.

   :returns: None


.. py:function:: extract_images_regular_interval(path_in, path_out, time_interval_in_sec)

   Function to extract the frames in every given "time_interval" e.g. 1 sec, 5 sec etc. from input video file
   and save them as separate frames in an output directory.
   :param path_in: Input video file.
   :param time_interval_in_sec: the time interval of the sampling, mention in seconds; we convert it into milliseconds
   :param path_out: Output directory to save the frames.

   :returns: None

   Resources:
          https://www.futurelearn.com/info/courses/introduction-to-image-analysis-for-plant-phenotyping/0/steps/305359


.. py:function:: extract_images_at_particular_timestamp(path_in, path_out, hh_mm_ss)

   Function to extract the frame at a particular time stamp; Need to know the number of frames per second and the
   timestamp in the video , we want to take frame from, we can easily calculate the frame number we want
   :param path_in: Input video file.
   :param hh_mm_ss: the time
   :param path_out: Output directory to save the frames.

   :returns: None


.. py:function:: extract_images_between_two_timestamps(path_in, path_out, hh_mm_ss_start, hh_mm_ss_end)

   Function to extract all the frames within two timestamps; Need to know the number of frames per second and the
   start and end timestamp in the video
   :param path_in: Input video file.
   :param hh_mm_ss_start: the time starting time stamp
   :param hh_mm_ss_end: the time ending time stamp
   :param path_out: Output directory to save the frames.

   :returns: None


.. py:function:: extract_regular_interval_images_between_two_timestamps(path_in, path_out, hh_mm_ss_start, hh_mm_ss_end, time_interval_in_sec)

   Function to extract frames after given regular intervals within two timestamps; Need to know the number of
   frames per second and the start and end timestamp in the video
   :param path_in: Input video file.
   :param hh_mm_ss_start: the time starting time stamp
   :param hh_mm_ss_end: the time ending time stamp
   :param time_interval_in_sec: The regular time interval
   :param path_out: Output directory to save the frames.

   :returns: None


.. py:function:: main()

.. py:data:: parser

