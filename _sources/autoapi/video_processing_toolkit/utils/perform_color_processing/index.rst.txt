video_processing_toolkit.utils.perform_color_processing
=======================================================

.. py:module:: video_processing_toolkit.utils.perform_color_processing








Module Contents
---------------

.. py:class:: ColorProcessing

   .. py:method:: plot_img(image: videoanalyst.engine.types.Image)
      :staticmethod:



   .. py:method:: channel_histogram(img, channel=0)
      :staticmethod:


      Note : 257 bins since bins are divided as [0,1), [1,2), ..., [254,255), [255,256]. If we took
      256 bin, the last bin would have been [254,255] thus concatenating two values.



   .. py:method:: histogram_peak(histogram)
      :staticmethod:



   .. py:method:: morphological_opening(img, morph_size)
      :staticmethod:



   .. py:method:: morphological_closing(img, morph_size)
      :staticmethod:



   .. py:method:: gaussian_blur(img, kernel_size, std)
      :staticmethod:



   .. py:method:: threshold(img, channel=0, threshmin=None, threshmax=None)
      :staticmethod:



   .. py:method:: compute_field_mask_cvprw_2018(frame, str_type)
      :staticmethod:


      Function to generate the mask for field segmentation
      :param frame: Input opencv image
      :param str_type: there are two type of approximation used: "epsilon" and "threshold_approximation"; This operator
      :param helps to smooth the boundary of the image:

      :returns: None

      Resources:
          "A bottom-up approach based on semantics for the interpretation of the main camera stream in soccer games"
          URL: http://www.telecom.ulg.ac.be/publi/publications/anthony/Anthony2018ABottomUp/index.html



   .. py:method:: compute_field_mask_nils(image_path)
      :staticmethod:



   .. py:method:: generate_batch_background_image(all_dir_path)
      :staticmethod:


      Function to generate the mask for field segmentation
      :param all_dir_path: The main directory path where all the subdirectory exist

      :returns: None

      Resources:
          "A bottom-up approach based on semantics for the interpretation of the main camera stream in soccer games"
          URL: http://www.telecom.ulg.ac.be/publi/publications/anthony/Anthony2018ABottomUp/index.html



   .. py:method:: apply_nils_background_removal_on_image(img_file_path)
      :staticmethod:



   .. py:method:: generate_batch_background_image_nils(all_dir_path)
      :staticmethod:


      Function to generate the mask for field segmentation
      :param all_dir_path: The main directory path where all the subdirectory exist

      :returns: None

      Resources:
          "A bottom-up approach based on semantics for the interpretation of the main camera stream in soccer games"
          URL: http://www.telecom.ulg.ac.be/publi/publications/anthony/Anthony2018ABottomUp/index.html



.. py:function:: main()

.. py:data:: start_time

