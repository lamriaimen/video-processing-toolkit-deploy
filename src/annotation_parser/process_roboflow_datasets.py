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
        print(" I am inside init function of test file ")
        self.num_of_classes = 0
        self.name_of_classes = None  # this list cannot be initialized here!
        self.dataset_name = None

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

    @staticmethod
    def load_data_convert_txt_road_sign_dataset():
        """
            Function to read the XML file and to convert into text files (yolo formatting)
            Args:

            Returns:
        """

        # This is just an example about how to convert from XML file into the text file for the annotation
        print(AnalyzeXMLFiles.extract_info_from_xml('Datasets/Road_Sign_Dataset/all_annotations/road4.xml'))

        # Get the annotations
        annotations = [os.path.join('Datasets/Road_Sign_Dataset/all_annotations', x) for x in
                       os.listdir('Datasets/Road_Sign_Dataset/all_annotations')
                       if x[-3:] == "xml"]
        annotations.sort()

        # Convert and save the annotations
        for ann in tqdm(annotations):
            info_dict = AnalyzeXMLFiles.extract_info_from_xml(ann)
            AnalyzeXMLFiles.convert_to_yolov5(info_dict)
        annotations = [os.path.join('Datasets/Road_Sign_Dataset/all_annotations', x) for x in
                       os.listdir('Datasets/Road_Sign_Dataset/all_annotations')
                       if x[-3:] == "txt"]

        return annotations

    @staticmethod
    def my_test_performance_result():
        detections_dir = "../runs/detect/yolov7_road_test_detect/"
        detection_images = [os.path.join(detections_dir, x) for x in os.listdir(detections_dir)]

        random_detection_image = Image.open(random.choice(detection_images))
        plt.imshow(np.array(random_detection_image))

        print('show me')


def main():
    # create all the objects
    operate_on_folders = OperateOnFolders()
    draw_annotations = DrawAnnotations()
    transform_output_classes = TransformOutputClasses()

    # get_txt_annotations = DataDescription.load_data_convert_txt_road_sign_dataset()
    # DrawAnnotations.draw_bounding_box(get_txt_annotations)

    # ModifyAnnotationFiles.partition_dataset_and_move_files()

    # DataDescription.my_test_performance_result()

    # operate_on_folders.organize_data_into_same_folder()
    # subfolders = [f.path for f in os.scandir("/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/"
    #                                          "Datasets/FootBall_Data/") if f.is_dir()]

    """
    ########   From here onwards, we will combine several individual datasets together to make one  ###############"
    """

    # file_path_for_folder = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/Datasets/" \
    #                        "Folders_Summary_5.txt"
    # rootdir = '/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/Datasets/FootBall_Data/'
    # dst_dir = '/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/Datasets/Combined_FootBall_Data_5/'

    # operate_on_folders.organize_data_into_same_folder_based_folder_name(file_path_for_folder, rootdir, dst_dir)
    # operate_on_folders.modify_list_of_folders()

    """
    ########   From here onwards, we will process only the ball datasets.  ###############"
    """

    # All the classes to be taken as they are actually represent the football, soccer. Even the class others also
    # dataset_path_1 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/Datasets/BACKUP/ball-11/"
    # draw_annotations.draw_bounding_box_for_each_class_separately(dataset_path_1,
    #                                                              foot_data_dict.class_name_to_id_mapping_ball_11)
    # TransformOutputClasses.transform_three_classes_into_one(dataset_path_1)

    # All the classes to be taken as they are actually represent the football, soccer. Even the class others also
    # dataset_path_2 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/Datasets/BACKUP/ball-12/"
    # draw_annotations.draw_bounding_box_for_each_class_separately(dataset_path_2, foot_data_dict.
    #                                                              class_name_to_id_mapping_ball_12)
    # TransformOutputClasses.transform_three_classes_into_one(dataset_path_2)

    # dataset_path_3 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/Datasets/BACKUP
    # /CA_Proj_Group4-1/"
    # draw_annotations.draw_bounding_box_for_each_class_separately(dataset_path_3,
    #                                                              foot_data_dict.
    #                                                              class_name_to_id_mapping_CA_Proj_Group4_1)
    # TransformOutputClasses.transform_three_classes_into_one(dataset_path_3)

    # dataset_path_4 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/Datasets/BACKUP
    # /CA_Proj_Group4-2/"
    # draw_annotations.draw_bounding_box_for_each_class_separately(dataset_path_4,
    #                                                              foot_data_dict.
    #                                                              class_name_to_id_mapping_CA_Proj_Group4_2)
    # TransformOutputClasses.transform_three_classes_into_one(dataset_path_4)

    # dataset_path_5 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/Datasets/BACKUP/coba-10/"
    # draw_annotations.draw_bounding_box_for_each_class_separately(dataset_path_5, foot_data_dict.
    #                                                              class_name_to_id_mapping_coba_10)
    # TransformOutputClasses.transform_class_by_removing_one_class(dataset_path_5)

    # dataset_path_7 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/Datasets/BACKUP/MBS4542-4/"
    # draw_annotations.draw_bounding_box_for_each_class_separately(dataset_path_7, foot_data_dict.
    #                                                              class_name_to_id_mapping_MBS4542_4)
    # TransformOutputClasses.transform_two_classes_into_one(dataset_path_7)

    # dataset_path_8 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/Datasets/BACKUP/MBS4542-5/"
    # draw_annotations.draw_bounding_box_for_each_class_separately(dataset_path_8, foot_data_dict.
    #                                                              class_name_to_id_mapping_MBS4542_5)
    # TransformOutputClasses.transform_two_classes_into_one(dataset_path_8)

    # dataset_path_9 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/Datasets/FootBall_Data
    # /ball-8/"
    # draw_annotations.draw_bounding_box_for_each_class_separately(dataset_path_9, foot_data_dict.
    #                                                              class_name_to_id_mapping_ball_8)
    # TransformOutputClasses.transform_two_classes_into_one(dataset_path_9)

    # dataset_path_10 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/Datasets/FootBall_Data
    # /football-4/"
    # draw_annotations.draw_bounding_box_for_each_class_separately(dataset_path_10, foot_data_dict.
    #                                                              class_name_to_id_mapping_football_4)
    # TransformOutputClasses.transform_two_classes_into_one(dataset_path_10)

    # dataset_path_11 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/Datasets/FootBall_Data
    # /football-8/"
    # draw_annotations.draw_bounding_box_for_each_class_separately(dataset_path_11, foot_data_dict.
    #                                                              class_name_to_id_mapping_football_8)
    # TransformOutputClasses.transform_two_classes_into_one(dataset_path_11)

    # dataset_path_12 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/Datasets/FootBall_Data
    # /football-9/"
    # draw_annotations.draw_bounding_box_for_each_class_separately(dataset_path_12, foot_data_dict.
    #                                                              class_name_to_id_mapping_football_9)
    # TransformOutputClasses.transform_two_classes_into_one(dataset_path_12)

    # dataset_path_13 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/Datasets/FootBall_Data
    # /football-11/"
    # draw_annotations.draw_bounding_box_for_each_class_separately(dataset_path_13, foot_data_dict.
    #                                                              class_name_to_id_mapping_football_11)
    # TransformOutputClasses.transform_two_classes_into_one(dataset_path_13)

    # dataset_path_14 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/Datasets/FootBall_Data
    # /football-13/"
    # draw_annotations.draw_bounding_box_for_each_class_separately(dataset_path_14, foot_data_dict.
    #                                                              class_name_to_id_mapping_football_13)
    # TransformOutputClasses.transform_two_classes_into_one(dataset_path_14)

    # dataset_path_15 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/Datasets/" \
    #                   "FootBall_Data_Test_3/Football-1"
    # draw_annotations.draw_bounding_box_for_each_class_separately(dataset_path_15, foot_data_dict.
    #                                                              class_name_to_id_mapping_Football_1)
    # TransformOutputClasses.transform_two_classes_into_one_only_train_folder(dataset_path_15)

    # dataset_path_16 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/Datasets/" \
    #                   "FootBall_Data_Test_3/Football-4"
    # draw_annotations.draw_bounding_box_for_each_class_separately(dataset_path_16, foot_data_dict.
    #                                                              class_name_to_id_mapping_Football_4)
    # TransformOutputClasses.transform_two_classes_into_one_only_train_folder(dataset_path_16)

    # dataset_path_17 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/Datasets/" \
    #                   "FootBall_Data_Test_3/Football-6"
    # draw_annotations.draw_bounding_box_for_each_class_separately(dataset_path_17, foot_data_dict.
    #                                                              class_id_to_name_mapping_Football_6)
    # TransformOutputClasses.transform_two_classes_into_one(dataset_path_17)

    """
    ########   From here onwards, we will process only the player datasets.  ###############"
    """
    # update_dict = {'2': 1, '3': 1}
    # dataset_path_18 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/Datasets/" \
    #                   "FootBall_Data/Soccer-Players-1"
    # draw_annotations.draw_bounding_box_for_each_class_separately(dataset_path_18,
    #                                                              foot_data_dict.
    #                                                              class_id_to_name_mapping_Soccer_Players_18)
    # transform_output_classes.transform_variable_classes_into_variable(dataset_path_18, update_dict)

    # update_dict = {'2': 1, '3': 1}
    # dataset_path_19 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/Datasets/" \
    #                   "FootBall_Data/Soccer-Players-2"
    # draw_annotations.draw_bounding_box_for_each_class_separately(dataset_path_19,
    #                                                              foot_data_dict.
    #                                                              class_id_to_name_mapping_Soccer_Players_18)
    # transform_output_classes.transform_variable_classes_into_variable(dataset_path_19, update_dict)

    # update_dict = {'2': 1, '3': 1}
    # dataset_path_20 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/Datasets/" \
    #                   "FootBall_Data/Soccer-Players-3"
    # draw_annotations.draw_bounding_box_for_each_class_separately(dataset_path_20,
    #                                                              foot_data_dict.
    #                                                              class_id_to_name_mapping_Soccer_Players_18)
    # transform_output_classes.transform_variable_classes_into_variable(dataset_path_20, update_dict)

    # update_dict = {'2': 1, '3': 1}
    # dataset_path_21 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/Datasets/" \
    #                   "FootBall_Data/Soccer-Players-4"
    # draw_annotations.draw_bounding_box_for_each_class_separately(dataset_path_21,
    #                                                              foot_data_dict.
    #                                                              class_id_to_name_mapping_Soccer_Players_18)
    # transform_output_classes.transform_variable_classes_into_variable(dataset_path_21, update_dict)

    # update_dict = {'2': 1}
    # dataset_path_22 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/" \
    #                   "Datasets/FootBall_Data/Soccer-Players-5"
    # draw_annotations.draw_bounding_box_for_each_class_separately(dataset_path_22,
    #                                                              foot_data_dict.
    #                                                              class_id_to_name_mapping_Soccer_Players_18)
    # transform_output_classes.transform_variable_classes_into_variable(dataset_path_22, update_dict)

    # update_dict = {'2': 1}
    # dataset_path_23 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/Datasets/" \
    #                   "FootBall_Data/Soccer-Players-6"
    # draw_annotations.draw_bounding_box_for_each_class_separately(dataset_path_23,
    #                                                              foot_data_dict.
    #                                                              class_id_to_name_mapping_Soccer_Players_18)
    # transform_output_classes.transform_variable_classes_into_variable(dataset_path_23, update_dict)

    # update_dict = {'2': 1}
    # dataset_path_24 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/" \
    #                   "Datasets/FootBall_Data/Soccer-Players-8"
    # draw_annotations.draw_bounding_box_for_each_class_separately(dataset_path_24,
    #                                                              foot_data_dict.
    #                                                              class_id_to_name_mapping_Soccer_Players_18)
    # transform_output_classes.transform_variable_classes_into_variable(dataset_path_24, update_dict)

    # update_dict = {'2': 1, '3': 1}
    # dataset_path_25 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/" \
    #                   "VOGO/YOLO_V7/Datasets/FootBall_Data/Soccer-Players-9"
    # draw_annotations.draw_bounding_box_for_each_class_separately(dataset_path_25,
    #                                                              foot_data_dict.
    #                                                              class_id_to_name_mapping_Soccer_Players_18)
    # transform_output_classes.transform_variable_classes_into_variable(dataset_path_25, update_dict)

    # update_dict = {'2': 1, '3': 1, '4': 1, '5': 1}
    # remove_dict = {'1': "nonsense_1"}

    # dataset_path_26 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/" \
    #                   "Datasets/FootBall_Data/Soccer-Players-10"
    # transform_output_classes.transform_class_by_removing_one_class(dataset_path_26, remove_dict)
    # transform_output_classes.transform_variable_classes_into_variable(dataset_path_26, update_dict)

    # draw_annotations.draw_bounding_box_for_each_class_separately(dataset_path_26,
    #                                                              foot_data_dict.
    #                                                              class_id_to_name_mapping_Soccer_Players_18)

    # update_dict = {'2': 1, '3': 1, '4': 1, '5': 1}
    # remove_dict = {'1': "nonsense_1"}
    # dataset_path_27 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/" \
    #                   "Datasets/FootBall_Data/Soccer-Players-11"
    # transform_output_classes.transform_class_by_removing_one_class(dataset_path_27, remove_dict)
    # transform_output_classes.transform_variable_classes_into_variable(dataset_path_27, update_dict)
    # draw_annotations.draw_bounding_box_for_each_class_separately(dataset_path_27,
    #                                                              foot_data_dict.
    #                                                              class_id_to_name_mapping_Soccer_Players_11)

    # update_dict = {'2': 1, '3': 1}
    # dataset_path_28 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/" \
    #                   "Datasets/FootBall_Data/Soccer-Players-12"
    # draw_annotations.draw_bounding_box_for_each_class_separately(dataset_path_28,
    #                                                              foot_data_dict.
    #                                                              class_id_to_name_mapping_Soccer_Players_18)
    # transform_output_classes.transform_variable_classes_into_variable(dataset_path_28, update_dict)

    # update_dict = {'2': 1, '3': 1}
    # dataset_path_29 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/" \
    #                   "Datasets/FootBall_Data/Soccer-Players-13"
    # draw_annotations.draw_bounding_box_for_each_class_separately(dataset_path_29,
    #                                                              foot_data_dict.
    #                                                              class_id_to_name_mapping_Soccer_Players_18)
    # transform_output_classes.transform_variable_classes_into_variable(dataset_path_29, update_dict)

    # update_dict = {'2': 1, '3': 1}
    # dataset_path_30 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/" \
    #                   "YOLO_V7/Datasets/FootBall_Data/Soccer-Players-14"
    # draw_annotations.draw_bounding_box_for_each_class_separately(dataset_path_30,
    #                                                              foot_data_dict.
    #                                                              class_id_to_name_mapping_Soccer_Players_18)
    # transform_output_classes.transform_variable_classes_into_variable(dataset_path_30, update_dict)

    # update_dict = {'2': 1}
    # dataset_path_31 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/" \
    #                   "Datasets/FootBall_Data/Soccer-Players-15"
    # draw_annotations.draw_bounding_box_for_each_class_separately(dataset_path_31,
    #                                                              foot_data_dict.
    #                                                              class_id_to_name_mapping_Soccer_Players_18)
    # transform_output_classes.transform_variable_classes_into_variable(dataset_path_31, update_dict)

    # update_dict = {'2': 1}
    # dataset_path_32 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/" \
    #                   "YOLO_V7/Datasets/FootBall_Data/Soccer-Players-16"
    # draw_annotations.draw_bounding_box_for_each_class_separately(dataset_path_32,
    #                                                              foot_data_dict.
    #                                                              class_id_to_name_mapping_Soccer_Players_18)
    # transform_output_classes.transform_variable_classes_into_variable(dataset_path_32, update_dict)

    """
    ########   Here we combine several individual datasets together to make one  ###############"
    """
    # update_dict = {'0': 1, '1': 0}

    # file_path_for_folder = "/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/Datasets/" \
    #                        "football_players_combine_1.txt"
    # rootdir = '/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/Datasets/FootBall_Data/'
    # dst_dir = '/home/tanmoymondal/PycharmProjects/LearnPytorch/VOGO/YOLO_V7/Datasets/Combined_Players_Data_1/'

    # operate_on_folders.organize_data_into_same_folder_based_folder_name(file_path_for_folder, rootdir, dst_dir)
    # transform_output_classes.transform_two_classes_into_one_only_train_folder(dst_dir)
    # draw_annotations.draw_bounding_box_for_each_class_separately(dst_dir,
    #                                                              foot_data_dict.
    #                                                              class_id_to_name_mapping_Soccer_Players_17)

    # operate_on_folders.modify_list_of_folders()

    test_data_path = "/home/tanmoymondal/Videos/fooball_keyframe/cross_validation/Folder_0/"
    draw_annotations.draw_bounding_box_for_each_class_separately(test_data_path,
                                                                 foot_data_dict.
                                                                 class_id_to_name_mapping_Soccer_Players_17)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PyTorch Template')

    args = parser.parse_args()
    main()
