video_processing_toolkit.utils.convert_file_format
==================================================

.. py:module:: video_processing_toolkit.utils.convert_file_format




Module Contents
---------------

.. py:class:: ConvertFileFormat

   .. py:method:: to_numpy(tensor)
      :staticmethod:



   .. py:method:: torch_var_to_numpy(tensor_var)
      :staticmethod:


      Converts Tensor from a Pytorch tensor to a numpy array.

      :param tensor_var: (torch.Tensor) A Pytorch tensor. Normally a batch of 3D (Ch x Height x Width) images

      :returns: (numpy.ndarray) The same tensor as a numpy array.
      :rtype: np_tensor



   .. py:method:: numpy_to_torch_var(np_tensor, device)
      :staticmethod:


      Converts Tensor from a numpy array to a Pytorch tensor.

      :param np_tensor: (numpy.ndarray) The same tensor as a numpy array.

      :returns: (torch.Tensor) A Pytorch tensor.
      :rtype: var



   .. py:method:: permute_tensor_dims(input_var)
      :staticmethod:


      This function implements the ToTensor class, without scaling the pixel values to the [0,1] range.
          H x W x C -> C x H x W

      :param input_var: (numpy.ndarray) The same tensor as a numpy array.

      :returns: (torch.Tensor) A Pytorch tensor.
      :rtype: var



   .. py:method:: to_torch(ndarray)
      :staticmethod:



   .. py:method:: im_to_numpy(img)
      :staticmethod:



   .. py:method:: im_to_torch(img)
      :staticmethod:


      cv img [h, w, c]
      torch  [c, h, w]



   .. py:method:: torch_to_img(img)
      :staticmethod:



