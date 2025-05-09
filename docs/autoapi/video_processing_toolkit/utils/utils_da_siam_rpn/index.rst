video_processing_toolkit.utils.utils_da_siam_rpn
================================================

.. py:module:: video_processing_toolkit.utils.utils_da_siam_rpn




Module Contents
---------------

.. py:class:: UtilsDaSiamRPN

   .. py:method:: get_subwindow_tracking(im, pos, model_sz, original_sz, avg_chans, out_mode='torch', new=False)
      :staticmethod:


      img  -- original image
      pos  -- [c_x, c_y]
      model_sz 127  The final size that need to be resized
      original s_ -> sqrt(w_ * h_)  size after target operation
      avg
      template must be a square
      detection is not square



   .. py:method:: cxy_wh_2_rect(pos, sz)
      :staticmethod:



   .. py:method:: rect_2_cxy_wh(rect)
      :staticmethod:



   .. py:method:: get_axis_aligned_bbox(region)
      :staticmethod:



