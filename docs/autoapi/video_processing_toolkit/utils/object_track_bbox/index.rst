video_processing_toolkit.utils.object_track_bbox
================================================

.. py:module:: video_processing_toolkit.utils.object_track_bbox




Module Contents
---------------

.. py:function:: region_to_bbox(region, center=True)

   Transforms the ground-truth annotation to the convenient format. The
   annotations come in different formats depending on the dataset of origin
   (see README, --Dataset--, for details), some use 4 numbers and some use 8
   numbers to describe the bounding boxes.


.. py:function:: rect(region, center)

   Calculate the center if center=True, otherwise the 4 number annotations
   used in the TempleColor and VOT13 datasets are already in the correct
   format.
   (cx, cy) is the center and w, h are the width and height of the target
   When center is False it returns region, which is a 4 tuple containing the
   (x, y) coordinates of the LowerLeft corner and its width and height.


.. py:function:: poly(region, center)

   Calculates the center, width and height of the bounding box when the
   annotations are 8 number rotated bounding boxes (used in VOT14 and VOT16).
   Since the Tracker does not try to estimate the rotation of the target, this
   function returns a upright bounding box with the same center width and
   height of the original one.
   The 8 numbers correspond to the (x,y) coordinates of the each of the 4
   corner points of the bounding box.


