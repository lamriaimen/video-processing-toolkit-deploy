video_processing_toolkit.utils.perform_image_operation
======================================================

.. py:module:: video_processing_toolkit.utils.perform_image_operation

.. autoapi-nested-parse::

   This module exposes the image processing methods as module level global
   variables, that are loaded based on user defined flags.

   Since there are multiple different implementations and libraries available for each
   of the image tasks we want to perform (e.g 'load jpeg' and 'resize'), we give the
   user the choice of using different versions of each function without changing
   the rest of the code. One example in which one would use a 'safe' flag is if
   there are non jpeg images in the dataset, as imageio.imread can read them,
   but not jpeg4py.

   The basic changes introduced here are the libjpeg-turbo which is a instruction
   level parallel (SSE, AVX, etc) implementation of the default C++ jpeg lib
   libjpeg. Morover we also switched the default Pillow for a fork called PIL-SIMD,
   which is identical in terms of the API but uses vectorized instructions as well
   as heavy loop unrolling to optimize some of Pillows functions (particularly the
   resize function). Since the PIL-SIMD is a drop-in replacement for Pillow, even
   if the SIMD version is not installed the program should work just as fine with
   the default Pillow (without the massive speed gains, though).







Module Contents
---------------

.. py:data:: LIBJPEG_TURBO_PRESENT
   :value: False


.. py:data:: VALID_FLAGS
   :value: ['fast', 'safe']


.. py:data:: PIL_FLAGS

.. py:function:: decode_jpeg_fast(img_path)

   Jpeg decoding method implemented by jpeg4py, available in
   https://github.com/ajkxyz/jpeg4py . This library binds the libjpeg-turbo
   C++ library (available in
   https://github.com/libjpeg-turbo/libjpeg-turbo/blob/master/BUILDING.md),
   and can be up to 9 times faster than the non SIMD implementation.
   Requires libjpeg-turbo, built and installed correctly.


.. py:function:: get_decode_jpeg_fcn(flag='fast')

   Yields the function demanded by the user based on the flags given and
   the system responses to imports. If the demanded function is not
   available an exception is raised and the user is informed it should try
   using another flag.


.. py:function:: resize_fast(img, size_tup, interp='bilinear')

   Implements the PIL resize method from a numpy image input, using the
   same interface as the scipy imresize method.
   OBS: if concerned with the resizing of the correlation score map, the
   default behavior of the PIL resize is to align the corners, so we can
   simply use resize(img, (129,129)) without any problems. The center pixel
   is kept in the center (at least for the 4x upscale) and the corner pixels
   aligned.

   :param img: (numpy.ndarray) A numpy RGB image.
   :param size_tup: (tuple) A 2D tuple containing the height and weight of the
                    resized image.
   :param interp: (str) The flag indicating the interpolation method. Available
                  methods include 'bilinear', 'bicubic' and 'nearest'.

   :returns: (numpy.ndarray) The resized image
   :rtype: img_res


.. py:function:: get_resize_fcn(flag='fast')

   Yields the resize function demanded by the user based on the flags given
   and the system responses to imports. If the demanded function is not
   available an exception is raised and the user is informed it should try
   using another flag.


.. py:function:: pad_image()

   Factory function to generate pads dictionaries with the placeholders for
   the amount of padding in each direction of an image. Note: the 'up' direction
   is up in relation to the displayed image, thus it represent the negative
   direction of the y indices.

   :returns: (dictionary) The padding in each direction.
   :rtype: pads


.. py:function:: crop_img(img, cy, cx, reg_s)

   Crops an image given its center and the side of the crop region.
   If the crop exceeds the size of the image, it calculates how much padding
   it should have in each one of the four sides. In the case that the bounding
   box has an even number of pixels in either dimension we approach the center
   of the bounding box as the floor in each dimension, which may displace the
   actual center half a pixel in each dimension. This way we always deal with
   bounding boxes of odd size in each dimension. Furthermore, we add the same
   amount of context region in every direction, which makes the effective
   region size always an odd integer as well, so to enforce this approach we
   require the region size to be an odd integer.


   :param img: (numpy.ndarray) The image to be cropped. Must be of dimensions
               [height, width, channels]
   :param cy: (int) The y coordinate of the center of the target.
   :param cx: (int) The x coordinate of the center of the target.
   :param reg_s: The side of the square region around the target, in pixels. Must
                 be an odd integer.

   :returns: (numpy.ndarray) The cropped image.
             pads: (dictionary) A dictionary with the amount of padding in pixels in
                 each side. The order is: up, down, left, right, or it can be
                 accessed by their names, e.g.: pads['up']
   :rtype: cropped_img


.. py:function:: resize_and_pad(cropped_img, out_sz, pads, reg_s=None, use_avg=True, resize_fcn=resize)

   Resizes and pads the cropped image.

   :param cropped_img: (numpy.ndarray) The cropped image.
   :param out_sz: (int) Output size, the desired size of the output.
   :param pads: (dictionary) A dictionary of the amount of pad in each side of the
                cropped image. They can be accessed by their names, e.g.: pads['up']
   :param reg_s: (int) Optional: The region side, used to check that the crop size
                 plus the padding amount is equal to the region side in each axis.
   :param use_avg: (bool) Indicates the mode of padding employed. If True, the
                   image is padded with the mean value, else it is padded with zeroes.
   :param resize_fcn: The image resize function

   :returns:

             (numpy.ndarray) The output image, resized and padded. Has size
                 (out_sz, out_sz).
   :rtype: out_img


.. py:function:: crop_and_resize(img, center, size, out_size, border_type=cv2.BORDER_CONSTANT, border_value=(0, 0, 0), interp=cv2.INTER_LINEAR)

.. py:function:: pad_frame(im, frame_sz, pos_x, pos_y, patch_sz, use_avg=True)

   Pads a frame equally on all sides, enough to fit a region of size
   patch_sz centered in (pos_x, pos_y). If the region is already inside the
   frame, it doesn't do anything.

   :param im: (numpy.ndarray) The image to be padded.
   :param frame_sz: (tuple) The width and height of the frame in pixels.
   :param pos_x: (int) The x coordinate of the center of the target in the frame.
   :param pos_y: (int) The y coordinate of the center of the target in the frame.
   :param path_sz: (int) The size of the patch corresponding to the context
                   region around the bounding box.
   :param use_avg: (bool) Indicates if we should pad with the mean value of the
                   pixels in the image (True) or zero (False).

   :returns: (numpy.ndarray) The image after the padding.
             npad: (int) the amount of padding applied
   :rtype: im_padded


.. py:function:: extract_crops_z(im, npad, pos_x, pos_y, sz_src, sz_dst)

   Extracts the reference patch from the image.

   :param im: (numpy.ndarray) The padded image.
   :param npad: (int) The amount of padding added to each side.
   :param pos_x: (int) The x coordinate of the center of the reference in the
                 original frame, not considering the padding.
   :param pos_y: (int) The y coordinate of the center of the reference in the
                 original frame, not considering the padding.
   :param sz_src: (int) The original size of the reference patch.
   :param sz_dst: (int) The final size of the patch (usually 127)

   :returns:

             (numpy.ndarray) The cropped image containing the reference with its
                 context region.
   :rtype: crop


.. py:function:: extract_crops_x(im, npad, pos_x, pos_y, sz_src0, sz_src1, sz_src2, sz_dst)

   Extracts the 3 scaled crops of the search patch from the image.

   :param im: (numpy.ndarray) The padded image.
   :param npad: (int) The amount of padding added to each side.
   :param pos_x: (int) The x coordinate of the center of the bounding box in the
                 original frame, not considering the padding.
   :param pos_y: (int) The y coordinate of the center of the bounding box in the
                 original frame, not considering the padding.
   :param sz_src0: (int) The downscaled size of the search region.
   :param sz_src1: (int) The original size of the search region.
   :param sz_src2: (int) The upscaled size of the search region.
   :param sz_dst: (int) The final size for each crop (usually 255)

   :returns: (numpy.ndarray) The 3 cropped images containing the search region
             in 3 different scales.
   :rtype: crops


.. py:function:: read_image(img_file, cvt_code=cv2.COLOR_BGR2RGB)

.. py:function:: show_image(img, boxes=None, box_fmt='ltwh', colors=None, thickness=3, fig_n=1, delay=1, visualize=True, cvt_code=cv2.COLOR_RGB2BGR)

