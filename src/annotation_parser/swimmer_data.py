# To download the football detection dataset from RoboFlow
import argparse

from utils.basic_operation import *
from roboflow import Roboflow
from annotation_parser.process_roboflow_datasets import DataDescription

from annotation_parser.custom_dict import roboflow_swimmer_data_dict as swim_data
from annotation_parser.modify_annotations_files import ModifyAnnotationFiles
from annotation_parser.transform_output_classes import TransformOutputClasses
from annotation_parser.operate_on_folders import OperateOnFolders
from annotation_parser.draw_annotations import DrawAnnotations

rf = Roboflow(api_key="4DdMFkEJifnbrhsTW79E")


def check_any_unwanted_class_and_correct(dataset_folder_path):
    # Get all the files from the directory

    labels_dir_path = os.path.join(dataset_folder_path, 'valid', 'labels')
    get_all_file_paths = get_files_in_dir(labels_dir_path)

    bad_cnt = 0
    for annotation_file_path in get_all_file_paths:
        full_file_path = os.path.join(labels_dir_path, annotation_file_path)

        # Now iterate through the all modified annotation and then create a new file to write it
        get_file_name_with_ext = os.path.basename(annotation_file_path)
        make_saving_path_complete = os.path.join(labels_dir_path, get_file_name_with_ext)

        with open(full_file_path, "r") as fp:

            all_lines = fp.readlines()
            mod_keep_all_annotations = []  # keeping all the annotation of a single file
            mod_class_flag = False
            for line in all_lines:  # loop through all the annotation lines, written in a file
                annotation_list = line.split(" ")  # get the single line of annotation

                if '\n' in annotation_list:
                    annotation_list.remove('\n')

                if len(annotation_list) < 6:  # that means there are 5 elements
                    annotation_list_float = []
                    mod_annotation_list_float = []

                    for x in annotation_list:
                        annotation_list_float.append(float(x))
                        mod_annotation_list_float.append(float(x))

                    class_indx = int(annotation_list_float[0])
                    if class_indx > 2:
                        mod_annotation_list_float[0] = float(2)
                        mod_class_flag = True

                    mod_keep_all_annotations.append(mod_annotation_list_float)

            if len(mod_keep_all_annotations) > 0 and mod_class_flag:
                file_handle_to_write = create_file_if_not_exists(make_saving_path_complete)
                file_handle_to_write.seek(0)
                for get_line_annotation in mod_keep_all_annotations:
                    for get_vals in get_line_annotation:
                        file_handle_to_write.write(str(get_vals))
                        file_handle_to_write.write(" ")
                    file_handle_to_write.write("\n")

                file_handle_to_write.truncate()
                file_handle_to_write.close()

                print("stop here")


def cleaning_operation_swim_dataset(dataset_path_1, remove_dict, update_dict, class_id_mapping):

    # Delete all the bad files from the folder
    ModifyAnnotationFiles.delete_bad_files_and_images_dataset(dataset_path_1)

    # First the remove the labels which are not needed from the annotation files
    TransformOutputClasses.transform_class_by_removing_one_class(dataset_path_1, remove_dict)

    # Modify the name of the folders:
    #  train->labels := train->labels_original
    #  train->labels_mod := train->labels
    OperateOnFolders.modify_folder_names(dataset_path_1)

    # check the number of classes exists. The class 0 and class 6 should get removed
    DrawAnnotations.draw_bounding_box_for_each_class_separately(dataset_path_1, class_id_mapping)

    # Hence after manually seeing the classes, we decided that class "Body: original class 1",
    # "BodySurface: original class 2" are valid classes. Then the class "BodyUnder: original class 3", "Swimmer:
    # original class 4" and "Umpire: original class 5" are merged into the single class i.e. "BodyUnder"

    # The following operation will be performed on "labels" folder which is actually modified labels, after the
    # modification by removing few class labels

    TransformOutputClasses.transform_variable_classes_into_variable(dataset_path_1, update_dict)

    # Modify the name of the folders:
    #  train->labels := delete the folder
    #  train->labels_mod := train->labels
    OperateOnFolders.modify_and_delete_folder_names(dataset_path_1)

    # Now check by drawing the annotations on the images
    DrawAnnotations.draw_bounding_box_for_each_class_separately(dataset_path_1, class_id_mapping)


def main():
    # The url to download is : https://universe.roboflow.com/a-s/uwh/dataset/3
    # project = rf.workspace("a-s").project("uwh")
    # dataset_1 = project.version(3).download("yolov8")

    # The url to download is : https://universe.roboflow.com/a-s/uwh/dataset/4
    # project = rf.workspace("a-s").project("uwh")
    # dataset_2 = project.version(4).download("yolov8")

    # The url to download is : https://universe.roboflow.com/a-s/uwh/dataset/5
    # project = rf.workspace("a-s").project("uwh")
    # dataset_3 = project.version(5).download("yolov8")

    # The url to download is : https://universe.roboflow.com/a-s/uwh/dataset/6
    # project = rf.workspace("a-s").project("uwh")
    # dataset_4 = project.version(6).download("yolov8")

    # All the classes to be taken as they are actually represent the football, soccer. Even the class others also
    dataset_path_1 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/Swimmer_Data/UWH-3/"
    remove_dict = {'0': "nonsense_1", '6': "nonsense_2"}
    update_dict = {'1': 0, '2': 1, '3': 2, '4': 2, '5': 2, '6': 2}
    class_id_mapping_dataset_1 = swim_data.class_id_to_name_mapping_UWH_3
    # cleaning_operation_swim_dataset(dataset_path_1, remove_dict, update_dict, class_id_mapping_dataset_1)

    dataset_path_2 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/Swimmer_Data/UWH-4/"
    remove_dict = {'0': "nonsense_1", '6': "nonsense_2"}
    update_dict = {'1': 0, '2': 1, '3': 2, '4': 2, '5': 2, '6': 2}
    class_id_mapping_dataset_2 = swim_data.class_id_to_name_mapping__UWH_4
    # cleaning_operation_swim_dataset(dataset_path_2, remove_dict, update_dict, class_id_mapping_dataset_2)

    dataset_path_3 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/Swimmer_Data/UWH-6/"
    remove_dict = {'0': "nonsense_1", '6': "nonsense_2"}
    update_dict = {'1': 0, '2': 1, '3': 2, '4': 2, '5': 2, '6': 2}
    class_id_mapping_dataset_3 = swim_data.class_id_to_name_mapping__UWH_6
    # cleaning_operation_swim_dataset(dataset_path_3, remove_dict, update_dict, class_id_mapping_dataset_3)

    dataset_path_4 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/Swimmer_Data/UWH-5/"
    remove_dict = {'0': "nonsense_1", '4': "nonsense_2"}
    update_dict = {'3': 2}
    class_id_mapping_dataset_4 = swim_data.class_id_to_name_mapping__UWH_5
    # cleaning_operation_swim_dataset(dataset_path_4, remove_dict, update_dict, class_id_mapping_dataset_4)

    dataset_path_5 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/Combined_Swimmer_1/"
    check_any_unwanted_class_and_correct(dataset_path_5)

    get_obj_data_descrip = DataDescription()
    file_path_for_folder = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/swimmer_combined_1.txt"
    rootdir = '/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/Swimmer_Data/'
    dst_dir = '/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/Combined_Swimmer_1/'

    # OperateOnFolders.organize_data_into_same_folder_based_folder_name(file_path_for_folder, rootdir, dst_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PyTorch Template')

    args = parser.parse_args()
    main()
