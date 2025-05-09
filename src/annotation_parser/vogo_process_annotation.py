import argparse
import random

import matplotlib.pyplot as plt
import numpy as np
from IPython.display import Image  # for displaying images
from PIL import Image

from annotation_parser.custom_dict import roboflow_football_data_dict as foot_data_dict
from tqdm import tqdm
from annotation_parser.analyze_xml_files import AnalyzeXMLFiles
from annotation_parser.draw_annotations import DrawAnnotations

from annotation_parser.modify_annotations_files import ModifyAnnotationFiles
from annotation_parser.operate_on_folders import OperateOnFolders

from annotation_parser.analyze_annotation_files import AnalyzeAnnotationFiles
from annotation_parser.transform_output_classes import TransformOutputClasses

from utils.basic_operation import *


class DataDescription:

    def __init__(self):
        print(" I am inside init function ")

    @staticmethod
    def fast_scandir(dir_name):
        """
        Get all the sub_directories from a directory
        Args:
            dir_name: Path of the directory, from which we want to get sub-direcotries
        Returns:
            sub_folders: The subdirectories within this folder
        """
        subfolders = [f.path for f in os.scandir(dir_name) if f.is_dir()]
        for dirname in list(subfolders):
            subfolders.extend(DataDescription.fast_scandir(dirname))
        return subfolders


def main():

    # create all the objects
    operate_on_folders = OperateOnFolders()
    draw_annotations = DrawAnnotations()
    transform_output_classes = TransformOutputClasses()

    # football_annotation_txt_file = "/home/tanmoymondal/Downloads/fooball_keyframe/train.txt"
    # keep_filtered_imgs_paths = AnalyzeAnnotationFiles.\
    #     read_folder_path_annotated_football_data(football_annotation_txt_file)
    # DrawAnnotations.call_draw_bounding_box_football_annotation(keep_filtered_imgs_paths)

    # Process the CVAT format xml file
    cvat_xml_file_path = "/home/tanmoymondal/Videos/fooball_keyframe/CVAT_Annnotation_XML/annotations.xml"
    keep_all_valid_imag_info_together = AnalyzeXMLFiles.parse_cvat_xml(cvat_xml_file_path)

    # save the good image file paths in a text file
    keep_good_file_name_only = []
    good_file_name_1 = "/home/tanmoymondal/Videos/fooball_keyframe/exp_dataset_1.txt"
    for item_in_info_dict in keep_all_valid_imag_info_together:
        img_path = item_in_info_dict["full_path"]
        keep_good_file_name_only.append("{}".format(img_path))

    # Save the annotation to disk
    print("\n".join(keep_good_file_name_only), file=open(good_file_name_1, "w"))

    TransformOutputClasses.transform_cvat_xml_dict_update_class(keep_all_valid_imag_info_together)

    """
        -----:  How to combine the VOGO annotated dataset and Roboflow dataset :----
        1. Use the cross validation set of VOGO dataset; there you can see that the dataset is arranged in the same 
        manner as it is in the classical YOLO format
        
        2. The same dataset formatting is there also in VOGO annotated dataset
        
        3. Now to combine these two dataset to generate a combined dataset
    """

    """
    ########   Here we combine two individual datasets together to make one  ###############"
    1. Dataset 1: RoboFlow dataset
    2. Dataset 2: Vogo Dataset
    """

    dest_folder = "/home/tanmoymondal/Videos/Vogo_Roboflow/"
    dest_folder_1 = "/home/tanmoymondal/Videos/Soccer-Players-10/"

    # rootdir_vogo = '/home/tanmoymondal/Videos/fooball_keyframe/cross_validation/Folder_0/'

    # rootdir_roboflow = '/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/Datasets
    # /Combined_Players_Data_1/'

    # operate_on_folders.organize_data_into_same_folder_vogo_roboflow(rootdir_vogo, rootdir_roboflow,
    #                                                                 dest_folder)
    # draw_annotations.draw_bounding_box_for_each_class_separately(dest_folder,
    #                                                              foot_data_dict.
    #                                                              class_id_to_name_mapping_Soccer_Players_17)

    """
        -----:  How to remove the annotations which are big that means these annotations are of the zoomed objects :----
        1. The objective here is to identify the objects which are big and then remove the corresponding annotations 
    """
    # transform_output_classes.transform_class_by_removing_big_annotations(dest_folder, 12)
    draw_annotations.draw_bounding_box_for_each_class_separately(dest_folder,
                                                                 foot_data_dict.
                                                                 class_id_to_name_mapping_Soccer_Players_17)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PyTorch Template')

    args = parser.parse_args()
    main()
