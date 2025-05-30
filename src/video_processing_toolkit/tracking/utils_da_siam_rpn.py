import numpy as np
import torch
import cv2
from video_processing_toolkit.transforms.convert_file_format import ConvertFileFormat


class UtilsDaSiamRPN:

    def __init__(self):
        print(" I am inside init function of test file ")

    @staticmethod
    def get_subwindow_tracking(im, pos, model_sz, original_sz, avg_chans, out_mode='torch', new=False):

        """
          img  -- original image
          pos  -- [c_x, c_y]
          model_sz 127  The final size that need to be resized
          original s_ -> sqrt(w_ * h_)  size after target operation
          avg
          template must be a square
          detection is not square
          """
        # example Preventing overflow after zooming in
        if isinstance(pos, float):
            pos = [pos, pos]
        sz = original_sz
        im_sz = im.shape
        c = (original_sz + 1) / 2

        # context_xmin/xmax represents the coordinates of the changed template (possibly negative)

        context_x_min = round(pos[0] - c)  # floor(pos(2) - sz(2) / 2);
        context_x_max = context_x_min + sz - 1
        context_y_min = round(pos[1] - c)  # floor(pos(1) - sz(1) / 2);
        context_y_max = context_y_min + sz - 1

        # If greater than 0, no pad
        # If it overflows, pad a certain size distance

        left_pad = int(max(0., -context_x_min))
        top_pad = int(max(0., -context_y_min))
        right_pad = int(max(0., context_x_max - im_sz[1] + 1))
        bottom_pad = int(max(0., context_y_max - im_sz[0] + 1))

        # Relabel the template information on the original image after the padding
        context_xmin = context_x_min + left_pad
        context_xmax = context_x_max + left_pad
        context_ymin = context_y_min + top_pad
        context_ymax = context_y_max + top_pad

        # zzp: a more easy speed version
        # Use avg to fill the boundary part
        r, c, k = im.shape
        if any([top_pad, bottom_pad, left_pad, right_pad]):
            te_im = np.zeros((r + top_pad + bottom_pad, c + left_pad + right_pad, k),
                             np.uint8)  # 0 is better than 1 initialization
            te_im[top_pad:top_pad + r, left_pad:left_pad + c, :] = im
            if top_pad:
                te_im[0:top_pad, left_pad:left_pad + c, :] = avg_chans
            if bottom_pad:
                te_im[r + top_pad:, left_pad:left_pad + c, :] = avg_chans
            if left_pad:
                te_im[:, 0:left_pad, :] = avg_chans
            if right_pad:
                te_im[:, c + left_pad:, :] = avg_chans
            im_patch_original = te_im[int(context_ymin):int(context_ymax + 1), int(context_xmin):int(context_xmax + 1),
                                :]
        else:
            im_patch_original = im[int(context_ymin):int(context_ymax + 1), int(context_xmin):int(context_xmax + 1), :]

        if not np.array_equal(model_sz, original_sz):
            im_patch = cv2.resize(im_patch_original, (model_sz, model_sz))  # zzp: use cv to get a better speed
        else:
            im_patch = im_patch_original

        return ConvertFileFormat.im_to_torch(im_patch) if out_mode in 'torch' else im_patch

    @staticmethod
    def cxy_wh_2_rect(pos, sz):
        return np.array([pos[0] - sz[0] / 2, pos[1] - sz[1] / 2, sz[0], sz[1]])  # 0-index

    @staticmethod
    def rect_2_cxy_wh(rect):
        return np.array([rect[0] + rect[2] / 2, rect[1] + rect[3] / 2]), np.array([rect[2], rect[3]])  # 0-index

    @staticmethod
    def get_axis_aligned_bbox(region):
        try:
            region = np.array([region[0][0][0], region[0][0][1], region[0][1][0], region[0][1][1],
                               region[0][2][0], region[0][2][1], region[0][3][0], region[0][3][1]])
        except:
            region = np.array(region)
        cx = np.mean(region[0::2])
        cy = np.mean(region[1::2])
        x1 = min(region[0::2])
        x2 = max(region[0::2])
        y1 = min(region[1::2])
        y2 = max(region[1::2])
        A1 = np.linalg.norm(region[0:2] - region[2:4]) * np.linalg.norm(region[2:4] - region[4:6])
        A2 = (x2 - x1) * (y2 - y1)
        s = np.sqrt(A1 / A2)
        w = s * (x2 - x1) + 1
        h = s * (y2 - y1) + 1
        return cx, cy, w, h
