from annotation_parser.modify_annotations_files import ModifyAnnotationFiles
from utils.basic_operation import *
from annotation_parser.utils.file_processing import ProcessFile
from annotation_parser.draw_annotations import DrawAnnotations
from annotation_parser.custom_dict import roboflow_football_data_dict as foot_data_dict
from pathlib import Path


class TransformOutputClasses(ModifyAnnotationFiles):

    def __init__(self):
        super().__init__()
        print(" I am inside init function")

    @staticmethod
    def class_id_to_name_mapping_five_class(get_obj_label, player_blur_val, player_crop_val, ball_blur_val):
        class_id = 0
        if get_obj_label == "player" and player_blur_val == "false" and player_crop_val == "false":
            class_id = 0
        elif get_obj_label == "player" and player_blur_val == "false" and player_crop_val == "true":
            class_id = 1
        elif get_obj_label == "player" and player_blur_val == "true" and player_crop_val == "false":
            class_id = 2
        elif get_obj_label == "ball" and ball_blur_val == "false":
            class_id = 3
        elif get_obj_label == "ball" and ball_blur_val == "true":
            class_id = 4
        else:
            assert "Invalid class. The class must be from the list of of 5 classes"
        return class_id

    @staticmethod
    def class_id_to_name_mapping_two_class(get_obj_label, player_blur_val, player_crop_val, ball_blur_val):
        class_id = 0
        if get_obj_label == "player" and player_blur_val == "false" and player_crop_val == "false":
            class_id = 0
        elif get_obj_label == "player" and player_blur_val == "false" and player_crop_val == "true":
            class_id = 0
        elif get_obj_label == "player" and player_blur_val == "true" and player_crop_val == "false":
            class_id = 0
        elif get_obj_label == "ball" and ball_blur_val == "false":
            class_id = 1
        elif get_obj_label == "ball" and ball_blur_val == "true":
            class_id = 1
        else:
            assert "Invalid class. The class must be from the list of of 5 classes"
        return class_id

    @staticmethod
    def transform_cvat_xml_dict_update_class(info_dict_all_imgs):
        """
            After receiving the CVAT XML processed by using "parse_cvat_xml()" function in analyze_xml_files.py file
            and the information extracted in dictionary format, this dictionary is passed in this function to modify the
            number of classes i.e. to create more output classes

            Args:
                info_dict_all_imgs: The dictionary, which contains the classes to remove

            Returns:

        """
        get_obj_draw_annotation = DrawAnnotations()

        for item_in_info_dict in info_dict_all_imgs:

            img_path = item_in_info_dict["full_path"]
            get_file_name_only = ProcessFile.get_file_name(img_path)
            get_file_ext_only = ProcessFile.get_file_extension(img_path)

            get_all_bbox_yolo_coods = item_in_info_dict["all_bbox_yolo_coords"]
            get_all_bbox_attributes_info = item_in_info_dict["all_bbox_attributes_info"]

            print_buffer = []
            # Now iterate over all the bounding boxes, exists in the image
            for ii in range(len(get_all_bbox_yolo_coods['yolo_coords'])):
                each_bbox_yolo_coords = get_all_bbox_yolo_coods['yolo_coords'][ii]
                get_obj_label = each_bbox_yolo_coords[0]

                yolo_coord_x = each_bbox_yolo_coords[1]
                yolo_coord_y = each_bbox_yolo_coords[2]
                yolo_coord_width = each_bbox_yolo_coords[3]
                yolo_coord_height = each_bbox_yolo_coords[4]

                player_blur_val = 'false'
                player_crop_val = 'false'
                ball_blur_val = 'false'

                if get_obj_label == "player":
                    # if the bbox is player then it will have 2 attributes
                    player_blur_val = get_all_bbox_attributes_info['bbox_attrib'][ii]['blurred']
                    player_crop_val = get_all_bbox_attributes_info['bbox_attrib'][ii]['cropped']
                elif get_obj_label == "ball":
                    # if the bbox is ball then it will have 1 attribute
                    ball_blur_val = get_all_bbox_attributes_info['bbox_attrib'][ii]['blurred']

                # In case of 5 classes to transform
                # class_id = TransformOutputClasses.class_id_to_name_mapping_five_class(get_obj_label, player_blur_val,
                #                                                                       player_crop_val, ball_blur_val)

                # In case of 2 classes to transform
                class_id = TransformOutputClasses.class_id_to_name_mapping_two_class(get_obj_label, player_blur_val,
                                                                                     player_crop_val, ball_blur_val)

                # Write the bbox details to the file
                print_buffer.append(
                    "{} {:.3f} {:.3f} {:.3f} {:.3f}".format(class_id, yolo_coord_x, yolo_coord_y, yolo_coord_width,
                                                            yolo_coord_height))

            dir_name = os.path.dirname(img_path)
            base_name = os.path.basename(img_path)

            get_dir_one_level_up = str(Path(dir_name).parents[0])  # get one level up in the directory

            dst_label_path_dir = os.path.join("/home/tanmoymondal/Videos/fooball_keyframe/obj_train_data/",
                                              get_dir_one_level_up, 'cvat_converted_yolo_annotations_2_classes')
            if not os.path.exists(dst_label_path_dir):
                os.makedirs(dst_label_path_dir)

            # Name of the file which we have to save
            save_file_name = os.path.join(dst_label_path_dir, base_name.replace("jpg", "txt"))
            src_img_path = os.path.join("/home/tanmoymondal/Videos/fooball_keyframe/obj_train_data/", img_path)

            # Save the annotation to disk
            print("\n".join(print_buffer), file=open(save_file_name, "w"))

            get_class_name_to_id_mapping = foot_data_dict.class_name_to_id_mapping_annotation_football_mod_2

            get_obj_draw_annotation.draw_bounding_box_football_annotation(save_file_name, src_img_path,
                                                                          get_file_name_only, get_file_ext_only,
                                                                          get_class_name_to_id_mapping)

    # @staticmethod
    def transform_class_by_removing_one_class(self, dataset_folder_path, remove_dict=None):
        """
            Function to modify the annotation files of any particular dataset, they are
            modified by removing one class i.e. we modify the annotation files so that any specific class (mentioned in
            "remove_dict" dictionary) will get removed. Hence, all the annotations, related to this specific class will
            be deleted

            Args:
                remove_dict: The dictionary, which contains the classes to remove
                dataset_folder_path: The directory of the dataset
            Returns:
        """
        ModifyAnnotationFiles()

        if remove_dict is None:
            remove_dict = {'1': "some nonsense, not needed"}

        labels_dir_path_train = os.path.join(dataset_folder_path, 'train', 'labels')
        get_all_file_paths_train = get_files_in_dir(labels_dir_path_train)

        labels_dir_path_test = os.path.join(dataset_folder_path, 'test', 'labels')
        get_all_file_paths_test = get_files_in_dir(labels_dir_path_test)

        labels_dir_path_valid = os.path.join(dataset_folder_path, 'valid', 'labels')
        get_all_file_paths_valid = get_files_in_dir(labels_dir_path_valid)

        super().modify_annotations_into_files_by_removing(get_all_file_paths_train, labels_dir_path_train,
                                                          remove_dict)
        super().modify_annotations_into_files_by_removing(get_all_file_paths_test, labels_dir_path_test,
                                                          remove_dict)
        super().modify_annotations_into_files_by_removing(get_all_file_paths_valid, labels_dir_path_valid,
                                                          remove_dict)

        print("The modified labeling is complete")

    def transform_class_by_removing_big_annotations(self, dataset_folder_path, thresh):
        """
            Function to modify the annotation files of any particular dataset, they are
            modified by removing one class i.e. we modify the annotation files so that any specific class
            will get removed. Hence, all the annotations, related to this specific class will
            be deleted
            Hence the annotations, which are of bigger size will be removed

            Args:
                thresh: The threshold to apply
                dataset_folder_path: The directory of the dataset
            Returns:
        """
        ModifyAnnotationFiles()

        labels_dir_path_train = os.path.join(dataset_folder_path, 'train', 'labels')
        get_all_file_paths_train = get_files_in_dir(labels_dir_path_train)

        # labels_dir_path_test = os.path.join(dataset_folder_path, 'test', 'labels')
        # get_all_file_paths_test = get_files_in_dir(labels_dir_path_test)
        #
        # labels_dir_path_valid = os.path.join(dataset_folder_path, 'valid', 'labels')
        # get_all_file_paths_valid = get_files_in_dir(labels_dir_path_valid)

        super().remove_big_annotations_objects_records(get_all_file_paths_train, labels_dir_path_train,
                                                       thresh)
        # super().remove_big_annotations_objects_records(get_all_file_paths_test, labels_dir_path_test,
        #                                                remove_dict)
        # super().remove_big_annotations_objects_records(get_all_file_paths_valid, labels_dir_path_valid,
        #                                                remove_dict)

        print("The modified labeling is complete")

    # @staticmethod
    def transform_three_classes_into_one(self, dataset_folder_path):
        """
            Function to modify the annotation files of any particular dataset which originally has 3 classes, they are
            modified into the dataset of only 1 class i.e. we modify the annotation files so that only one class
            (class 0) remains. Hence, all the annotations, related to class 1 and 2 are replaced with class 0
            Args:
                dataset_folder_path: The directory of the dataset
            Returns:

        """
        ModifyAnnotationFiles()

        labels_dir_path_train = os.path.join(dataset_folder_path, 'train', 'labels')
        get_all_file_paths_train = get_files_in_dir(labels_dir_path_train)

        labels_dir_path_test = os.path.join(dataset_folder_path, 'test', 'labels')
        get_all_file_paths_test = get_files_in_dir(labels_dir_path_test)

        labels_dir_path_valid = os.path.join(dataset_folder_path, 'valid', 'labels')
        get_all_file_paths_valid = get_files_in_dir(labels_dir_path_valid)

        update_dict = {'1': 0, '2': 0}
        super().modify_annotations_into_files(get_all_file_paths_train, labels_dir_path_train, update_dict)
        super().modify_annotations_into_files(get_all_file_paths_test, labels_dir_path_test, update_dict)
        super().modify_annotations_into_files(get_all_file_paths_valid, labels_dir_path_valid, update_dict)

        print("The modified labeling is complete")

    # @staticmethod
    def transform_two_classes_into_one(self, dataset_folder_path):
        """
            Function to modify the annotation files of any particular dataset which originally has 2 classes, they are
            modified into the dataset of only 1 class i.e. we modify the annotation files so that only one class
            (class 0) remains. Hence, all the annotations, related to class 1 are replaced with class 0
            Args:
                dataset_folder_path: The directory of the dataset
            Returns:

        """
        ModifyAnnotationFiles()

        labels_dir_path_train = os.path.join(dataset_folder_path, 'train', 'labels')
        get_all_file_paths_train = get_files_in_dir(labels_dir_path_train)

        labels_dir_path_test = os.path.join(dataset_folder_path, 'test', 'labels')
        get_all_file_paths_test = get_files_in_dir(labels_dir_path_test)

        labels_dir_path_valid = os.path.join(dataset_folder_path, 'valid', 'labels')
        get_all_file_paths_valid = get_files_in_dir(labels_dir_path_valid)

        update_dict = {'1': 0}
        super().modify_annotations_into_files(get_all_file_paths_train, labels_dir_path_train, update_dict)
        super().modify_annotations_into_files(get_all_file_paths_test, labels_dir_path_test, update_dict)
        super().modify_annotations_into_files(get_all_file_paths_valid, labels_dir_path_valid, update_dict)

        print("The modified labeling is complete")

    # @staticmethod
    def transform_two_classes_into_one_only_train_folder(self, dataset_folder_path):
        """
            Function to modify the annotation files of any particular dataset which originally has 2 classes, they are
            modified into the dataset of only 1 class i.e. we modify the annotation files so that only one class
            (class 0) remains. Hence, all the annotations, related to class 1 are replaced with class 0

            This function is exactly same as the above function "transform_two_classes_into_one()", but this function
            will only function on "Train" folder

            Args:
                dataset_folder_path: The directory of the dataset
            Returns:

        """

        labels_dir_path_train = os.path.join(dataset_folder_path, 'train', 'labels')
        get_all_file_paths_train = get_files_in_dir(labels_dir_path_train)

        # update_dict = {'1': 0}
        update_dict = {'0': 1, '1': 0}
        super().modify_annotations_into_files(get_all_file_paths_train, labels_dir_path_train, update_dict)

        print("The modified labeling is complete")

    # @staticmethod
    def transform_variable_classes_into_variable(self, dataset_folder_path, update_dict):
        """
            Function to modify the annotation files of any particular dataset which originally has n classes, they are
            modified into the dataset of only p (p < n) class i.e. we modify the annotation files so that only p classes
            remains.
            Args:
                dataset_folder_path: The directory of the dataset
                update_dict : This is an updated dictionary, which will contain the updated class indexes i.e. for
            example :
                update_dict = {'1': 0, '2': 0} means that class '1' will be updated as class '0'
                                                          class '2' will be updated as class '0'
            Returns:

        """
        ModifyAnnotationFiles()

        labels_dir_path_train = os.path.join(dataset_folder_path, 'train', 'labels')
        get_all_file_paths_train = get_files_in_dir(labels_dir_path_train)

        labels_dir_path_test = os.path.join(dataset_folder_path, 'test', 'labels')
        get_all_file_paths_test = get_files_in_dir(labels_dir_path_test)

        labels_dir_path_valid = os.path.join(dataset_folder_path, 'valid', 'labels')
        get_all_file_paths_valid = get_files_in_dir(labels_dir_path_valid)

        # update_dict = {'1': 0}
        super().modify_annotations_into_files(get_all_file_paths_train, labels_dir_path_train, update_dict)
        super().modify_annotations_into_files(get_all_file_paths_test, labels_dir_path_test, update_dict)
        super().modify_annotations_into_files(get_all_file_paths_valid, labels_dir_path_valid, update_dict)

        print("The modified labeling is complete")

    def transform_variable_classes_into_variable_given_folder(self, dataset_folder_path, update_dict):
        """
            Function to modify the annotation files of any particular dataset which originally has n classes, they are
            modified into the dataset of only p (p < n) class i.e. we modify the annotation files so that only p classes
            remains.

            Only difference here is, we are looking to modify the annotation files in a folder
            Args:
                dataset_folder_path: The directory of the dataset
                update_dict : This is an updated dictionary, which will contain the updated class indexes i.e. for
            example :
                update_dict = {'1': 0, '2': 0} means that class '1' will be updated as class '0'
                                                          class '2' will be updated as class '0'
            Returns:

        """
        ModifyAnnotationFiles()

        labels_dir_path = os.path.join(dataset_folder_path, 'labels')
        get_all_file_paths_actual = get_files_in_dir(labels_dir_path)

        # update_dict = {'1': 0}
        super().modify_annotations_into_files(get_all_file_paths_actual, labels_dir_path, update_dict)

        print("The modified labeling is complete")