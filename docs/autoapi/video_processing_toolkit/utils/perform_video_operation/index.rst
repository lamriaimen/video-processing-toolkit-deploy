video_processing_toolkit.utils.perform_video_operation
======================================================

.. py:module:: video_processing_toolkit.utils.perform_video_operation








Module Contents
---------------

.. py:data:: time_stamp_start
   :value: ['00:16:50', '00:19:20', '00:20:08', '00:21:15', '00:23:26', '00:25:40', '00:25:45', '00:25:56',...


.. py:data:: time_stamp_end
   :value: ['00:16:55', '00:19:30', '00:20:11', '00:21:21', '00:23:32', '00:25:44', '00:25:48', '00:25:59',...


.. py:data:: time_stamp_start_swim_1
   :value: ['00:07:38', '00:22:09', '00:31:01', '01:04:44', '01:22:50', '01:34:42', '01:29:04', '01:48:47',...


.. py:data:: time_stamp_end_swim_1
   :value: ['00:18:17', '00:32:15', '00:41:40', '01:14:11', '01:32:55', '01:44:50', '01:40:04', '01:58:50',...


.. py:class:: VideoOperation

   .. py:method:: get_frame_types(video_file)
      :staticmethod:


      Function to get the type of video
      :param video_file: Path of the input video file. We need this function to get the i-frames and p-frames

      Returns:




   .. py:method:: get_clip(input_filename, output_filename, start_time, end_time)
      :staticmethod:


      Function to actually cut the video clips
      :param input_filename: Path of the input video file
      :param output_filename: The path of the output file clip
      :param start_time: The start time stamp
      :param end_time: The end time stamp

      Returns:




   .. py:method:: cut_video_clips(input_filename, output_file_path, time_stamp_start_1, time_stamp_end_1)
      :staticmethod:


      Function to read several start and end time stamps, mentioned in two vectors; "time_stamp_start_1" and
      "time_stamp_end_1", to crop the video clips based on these start and end time stamps
      :param input_filename: Path of the input video file
      :param output_file_path: The path of the output file clip
      :param time_stamp_start_1: The list of start time in HH:MM:SS format
      :param time_stamp_end_1: The list of end time in HH:MM:SS format

      Returns:




   .. py:method:: convert_video(inputted_file)
      :staticmethod:


      Function to convert the video file into .avi format and save it into current project directory
      :param inputted_file: Path of the input video file

      :returns: The name of the output video file, which automatically takes the name from current time and
                save the file into current project folder
      :rtype: video_name



   .. py:method:: compute_frame_per_sec_rate(video_file)
      :staticmethod:


      Function to compute the frame per seconds or pfs
      :param video_file: Path of the video file

      :returns: The Frame rate of the created video stream
      :rtype: fps



   .. py:method:: frames_to_video(input_path, output_path, fps)
      :staticmethod:


      Function reads all the individual frames, saved in a directory and then use them to create a video
      :param input_path: Path of the directory where the images or frames are saved
      :param fps: The Frame rate of the created video stream.
      :param output_path: The path where the constructed video will be saved

      :returns: None



   .. py:method:: video_to_all_frames(input_loc, output_loc)
      :staticmethod:


      Function to extract all the frames from input video file
      and save them as separate frames in an output directory.
      :param input_loc: Input video file.
      :param output_loc: Output directory to save the frames.

      :returns: None



   .. py:method:: extract_images_regular_interval(path_in, path_out, time_interval_in_sec)
      :staticmethod:


      Function to extract the frames in every given "time_interval" e.g. 1 sec, 5 sec etc. from input video file
      and save them as separate frames in an output directory.
      :param path_in: Input video file.
      :param time_interval_in_sec: the time interval of the sampling, mention in seconds; we convert it into milliseconds
      :param path_out: Output directory to save the frames.

      :returns: None

      Resources:
             https://www.futurelearn.com/info/courses/introduction-to-image-analysis-for-plant-phenotyping/0/steps/305359



   .. py:method:: extract_images_at_particular_timestamp(path_in, path_out, hh_mm_ss)
      :staticmethod:


      Function to extract the frame at a particular time stamp; Need to know the number of frames per second and the
      timestamp in the video , we want to take frame from, we can easily calculate the frame number we want
      :param path_in: Input video file.
      :param hh_mm_ss: the time
      :param path_out: Output directory to save the frames.

      :returns: None



   .. py:method:: extract_images_between_two_timestamps(path_in, path_out, hh_mm_ss_start, hh_mm_ss_end)
      :staticmethod:


      Function to extract all the frames within two timestamps; Need to know the number of frames per second and the
      start and end timestamp in the video
      :param path_in: Input video file.
      :param hh_mm_ss_start: the time starting time stamp
      :param hh_mm_ss_end: the time ending time stamp
      :param path_out: Output directory to save the frames.

      :returns: None



   .. py:method:: extract_regular_interval_images_between_two_timestamps(path_in, path_out, hh_mm_ss_start, hh_mm_ss_end, time_interval_in_sec)
      :staticmethod:


      Function to extract frames after given regular intervals within two timestamps; Need to know the number of
      frames per second and the start and end timestamp in the video
      :param path_in: Input video file.
      :param hh_mm_ss_start: the time starting time stamp
      :param hh_mm_ss_end: the time ending time stamp
      :param time_interval_in_sec: The regular time interval
      :param path_out: Output directory to save the frames.

      :returns: None



   .. py:method:: save_all_i_keyframes(video_file, path_out)
      :staticmethod:


      Function to extract  and save all the i-key frames of a complete video
      :param video_file: Input video file.
      :param path_out: The output folder to save all the output frames

      :returns: None

      Resources:
          URL: https://stackoverflow.com/questions/42798634/extracting-keyframes-python-opencv
          URL: https://stackoverflow.com/questions/33311153/python-extracting-and-saving-video-frames



   .. py:method:: save_all_i_keyframes_between_two_timestamps(video_file, path_out, hh_mm_ss_start, hh_mm_ss_end)
      :staticmethod:


      Function to extract  and save all the i-key frames of a complete video
      :param video_file: Input video file.
      :param path_out: The output folder to save all the output frames
      :param hh_mm_ss_start: the time starting time stamp
      :param hh_mm_ss_end: the time ending time stamp

      :returns: None

      Resources:
          URL : https://stackoverflow.com/questions/42798634/extracting-keyframes-python-opencv
          URL: https://stackoverflow.com/questions/33311153/python-extracting-and-saving-video-frames



   .. py:method:: save_all_p_keyframes(video_file, path_out)
      :staticmethod:


      Function to extract  and save all the p-key frames of a complete video
      :param video_file: Input video file.
      :param path_out: The output folder to save all the output frames

      :returns: None

      Resources:
          URL: https://stackoverflow.com/questions/42798634/extracting-keyframes-python-opencv
          URL: https://stackoverflow.com/questions/33311153/python-extracting-and-saving-video-frames



   .. py:method:: save_all_p_keyframes_between_two_timestamps(video_file, path_out, hh_mm_ss_start, hh_mm_ss_end)
      :staticmethod:


      Function to extract  and save all the p-key frames of a complete video
      :param video_file: Input video file.
      :param path_out: The output folder to save all the output frames
      :param hh_mm_ss_start: the time starting time stamp
      :param hh_mm_ss_end: the time ending time stamp

      :returns: None

      Resources:
          URL: https://stackoverflow.com/questions/42798634/extracting-keyframes-python-opencv
          URL: https://stackoverflow.com/questions/33311153/python-extracting-and-saving-video-frames



   .. py:method:: handlle_nils_field_segmentation(frame)
      :staticmethod:



   .. py:method:: process_input_video_give_video_output(input_loc, output_loc, function_to_apply)
      :staticmethod:


      Function to apply the processing on each frames from input video file
      and create another video
      :param input_loc: Input video file.
      :param output_loc: The path of output video file
      :param function_to_apply: The function in which the processing will be applied. Remember, this function should
      :param take opencv frame i.e. a numpy array:
      :type take opencv frame i.e. a numpy array: nd.array

      Example usage :
          process_input_video_give_video_output("input_video_path", "output_video_path",
          handlle_nils_field_segmentation)


      :returns: None



.. py:function:: main()

.. py:data:: start_time

