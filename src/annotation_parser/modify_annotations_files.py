from pathlib import Path

from sklearn.model_selection import train_test_split
from PIL import Image

from annotation_parser.analyze_annotation_files import AnalyzeAnnotationFiles
from utils.basic_operation import *
from results_stats.analyze_annotation_files import AnalyzeAnnotation


class ModifyAnnotationFiles:

    def __init__(self):
        print(" I am inside init function")

    @staticmethod
    def delete_blank_annotations_files_and_imgs(get_all_file_paths, labels_dir_path):
        """
            Function to detect the void or blank annotation files delete it
            Args:
                get_all_file_paths: The complete path of all the annotation text files, exist in a directory
                labels_dir_path: The new directory path of all the annotations

            Returns:

        """
        bad_file_deleted = 0

        for annotation_file_path in get_all_file_paths:
            full_file_path = os.path.join(labels_dir_path, annotation_file_path)
            if os.path.getsize(full_file_path) == 0:

                # that means all the annotations of the image is badly formatted and there are no good annotation
                get_dir_only = os.path.dirname(full_file_path)
                get_dir_only = str(Path(get_dir_only).parents[0])  # get one level up in the directory
                get_dir_only = os.path.join(get_dir_only, "images")

                img_file_name_with_ext = os.path.basename(full_file_path)
                img_file_name_no_ext = os.path.splitext(img_file_name_with_ext)[0]

                make_img_file_name_only = img_file_name_no_ext + ".jpg"

                full_img_path_to_delete = os.path.join(get_dir_only, make_img_file_name_only)

                # delete the image file from the folder
                if os.path.isfile(full_img_path_to_delete):
                    os.remove(full_img_path_to_delete)

                # delete the text file
                if os.path.isfile(full_file_path):
                    os.remove(full_file_path)

                bad_file_deleted = bad_file_deleted + 1
        print("Total bad files are deleted : ", bad_file_deleted)

    @staticmethod
    def modify_annotations_into_files_by_removing(get_all_file_paths, labels_dir_path, conversion_list_dict):

        """
            Function to modify the annotation text files of any particular dataset, we will
            Args:
                get_all_file_paths: The complete path of all the annotation text files, exist in a directory
                labels_dir_path: The new directory path of all the annotations
                conversion_list_dict: This dict will have the dictionary which contains the classes to modify

                Hence, if we see that there is any image, containing only the annotations, which are deleted or removed
                then there is no meaning to keep this image as this image doesn't contain any annotations. Hence, we
                also remove the image
            Returns:
        """

        get_one_level_up = str(Path(labels_dir_path).parents[0])  # get the directory one level up
        new_dir_path = os.path.join(get_one_level_up, "labels_mod")
        create_dir_if_not_exists(new_dir_path)
        mod_file_cnt = 0
        for annotation_file_path in get_all_file_paths:
            full_file_path = os.path.join(labels_dir_path, annotation_file_path)

            mod_keep_all_annotations = AnalyzeAnnotationFiles.read_file_del_cls_get_needed_contents \
                (full_file_path, conversion_list_dict)

            # Now iterate through the all modified annotation and then create a new file to write it
            get_file_name_with_ext = os.path.basename(annotation_file_path)
            make_saving_path_complete = os.path.join(new_dir_path, get_file_name_with_ext)

            if len(mod_keep_all_annotations) > 0:
                file_handle_to_write = create_file_if_not_exists(make_saving_path_complete)
                for get_line_annotation in mod_keep_all_annotations:
                    for get_vals in get_line_annotation:
                        file_handle_to_write.write(str(get_vals))
                        file_handle_to_write.write(" ")
                    file_handle_to_write.write("\n")
                file_handle_to_write.close()
                mod_file_cnt = mod_file_cnt + 1

            else:
                # that means all the annotations of the image is badly formatted and there are no good annotation
                get_dir_only = os.path.dirname(full_file_path)
                get_dir_only = str(Path(get_dir_only).parents[0])  # get one level up in the directory
                get_dir_only = os.path.join(get_dir_only, "images")

                img_file_name_with_ext = os.path.basename(full_file_path)
                img_file_name_no_ext = os.path.splitext(img_file_name_with_ext)[0]

                make_img_file_name_only = img_file_name_no_ext + ".jpg"

                full_img_path_to_delete = os.path.join(get_dir_only, make_img_file_name_only)

                # delete the image file from the folder
                if os.path.isfile(full_img_path_to_delete):
                    os.remove(full_img_path_to_delete)

        print("check me at the end")

    @staticmethod
    def modify_annotations_into_files(get_all_file_paths, labels_dir_path, conversion_list_dict):
        """
            Function to modify the annotation text files of any particular dataset
            Args:
                get_all_file_paths: The complete path of all the annotation text files, exist in a directory
                labels_dir_path: The new directory path where we will save the modified annotations
                conversion_list_dict: This dict will have the dictionary which contains the classes to modify

            Returns:

        """
        get_one_level_up = str(Path(labels_dir_path).parents[0])  # get the directory one level up
        new_dir_path = os.path.join(get_one_level_up, "labels_mod")
        create_dir_if_not_exists(new_dir_path)

        for annotation_file_path in get_all_file_paths:
            full_file_path = os.path.join(labels_dir_path, annotation_file_path)

            mod_keep_all_annotations = AnalyzeAnnotationFiles. \
                read_file_mod_cls_get_needed_contents(full_file_path, conversion_list_dict)

            # Now iterate through the all modified annotation and then create a new file to write it
            get_file_name_with_ext = os.path.basename(annotation_file_path)
            make_saving_path_complete = os.path.join(new_dir_path, get_file_name_with_ext)

            if len(mod_keep_all_annotations) > 0:
                file_handle_to_write = create_file_if_not_exists(make_saving_path_complete)
                for get_line_annotation in mod_keep_all_annotations:
                    for get_vals in get_line_annotation:
                        file_handle_to_write.write(str(get_vals))
                        file_handle_to_write.write(" ")
                    file_handle_to_write.write("\n")
                file_handle_to_write.close()
            else:
                # that means all the annotations of the image is badly formatted and there are no good annotation
                get_dir_only = os.path.dirname(full_file_path)
                get_dir_only = str(Path(get_dir_only).parents[0])  # get one level up in the directory
                get_dir_only = os.path.join(get_dir_only, "images")

                img_file_name_with_ext = os.path.basename(full_file_path)
                img_file_name_no_ext = os.path.splitext(img_file_name_with_ext)[0]

                make_img_file_name_only = img_file_name_no_ext + ".jpg"

                full_img_path_to_delete = os.path.join(get_dir_only, make_img_file_name_only)

                # delete the image file from the folder
                if os.path.isfile(full_img_path_to_delete):
                    os.remove(full_img_path_to_delete)

    def delete_bad_files_and_images_dataset(self, dataset_folder_path):
        """
            Function to modify the annotation files of any particular dataset which originally has n classes, they are
            modified into the dataset of only p (p < n) class i.e. we modify the annotation files so that only p classes
            remains.
            Args:
                dataset_folder_path: The directory of the dataset
            Returns:

        """
        labels_dir_path_train = os.path.join(dataset_folder_path, 'train', 'labels')
        get_all_file_paths_train = get_files_in_dir(labels_dir_path_train)

        labels_dir_path_test = os.path.join(dataset_folder_path, 'test', 'labels')
        get_all_file_paths_test = get_files_in_dir(labels_dir_path_test)

        labels_dir_path_valid = os.path.join(dataset_folder_path, 'valid', 'labels')
        get_all_file_paths_valid = get_files_in_dir(labels_dir_path_valid)

        # update_dict = {'1': 0}
        self.delete_blank_annotations_files_and_imgs(get_all_file_paths_train, labels_dir_path_train)
        self.delete_blank_annotations_files_and_imgs(get_all_file_paths_test, labels_dir_path_test)
        self.delete_blank_annotations_files_and_imgs(get_all_file_paths_valid, labels_dir_path_valid)

        print("The modified labeling is complete")

    @staticmethod
    def partition_dataset_and_move_files():
        """
            Function to partition the dataset into "train", "valid" and "test" sub-folders
            Args:

            Returns:
        """
        # Read images and annotations
        images = [os.path.join('Road_Sign_Dataset/images', x) for x in os.listdir('Road_Sign_Dataset/images')]
        annotations = [os.path.join('Road_Sign_Dataset/annotations', x) for x in
                       os.listdir('Road_Sign_Dataset/annotations') if x[-3:] == "txt"]

        images.sort()
        annotations.sort()

        # Split the dataset into train-valid-test splits
        train_images, val_images, train_annotations, val_annotations = train_test_split(images, annotations,
                                                                                        test_size=0.2,
                                                                                        random_state=1)
        # Now from the validation images, actually divide it into test and validation set
        val_images, test_images, val_annotations, test_annotations = train_test_split(val_images, val_annotations,
                                                                                      test_size=0.5, random_state=1)

        # Move the splits into their folders
        move_files_to_folder(train_images, 'Road_Sign_Dataset/split_dataset/train/')
        move_files_to_folder(val_images, 'Road_Sign_Dataset/split_dataset/val/')
        move_files_to_folder(test_images, 'Road_Sign_Dataset/split_dataset/test/')

        move_files_to_folder(train_annotations, 'Road_Sign_Dataset/split_labels/train/')
        move_files_to_folder(val_annotations, 'Road_Sign_Dataset/split_labels/val/')
        move_files_to_folder(test_annotations, 'Road_Sign_Dataset/split_labels/test/')

    @staticmethod
    def remove_big_annotations_objects_records(get_all_file_paths, labels_dir_path, sz_thresh):

        """
            Function to remove annotations which are big
            Args:
                get_all_file_paths: The complete path of all the annotation text files, exist in a directory
                labels_dir_path: The new directory path of all the annotations
                sz_thresh: This threshold value will be divided by the image area to get the real threshold to
                identify the big bboxes

                Hence, if we see that there is any image, containing only the annotations, which are deleted or removed
                then there is no meaning to keep this image as this image doesn't contain any annotations. Hence, we
                also remove the image
            Returns:
        """

        get_one_level_up = str(Path(labels_dir_path).parents[0])  # get the directory one level up
        new_dir_path = os.path.join(get_one_level_up, "labels_mod")
        create_dir_if_not_exists(new_dir_path)
        mod_file_cnt = 0
        for annotation_file_path in get_all_file_paths:
            full_file_path = os.path.join(labels_dir_path, annotation_file_path)
            img_dir_path = labels_dir_path.replace('labels', 'images')
            img_file_name = annotation_file_path.replace('.txt', '.jpg')
            full_img_path = os.path.join(img_dir_path, img_file_name)

            image = Image.open(full_img_path)
            img_width, img_height = image.size
            img_area = img_height * img_width

            # For each annotation text file, we will get the list of annotations bbox and these annotations will be
            # stored in the list named as "mod_keep_all_annotations"

            with open(full_file_path, "r") as fp:

                all_lines = fp.readlines()
                mod_keep_all_annotations = []

                for line in all_lines:

                    line = line.rstrip()
                    annotation_list = line.split(" ")

                    if len(annotation_list) < 6:  # that means there are 5 elements in the list
                        annotation_list_float = []
                        mod_annotation_list_float = []

                        for x in annotation_list:
                            annotation_list_float.append(float(x))
                            mod_annotation_list_float.append(float(x))

                        _, bbox_format = AnalyzeAnnotation.convert_annotation_from_yolo_to_cartesian\
                            ([annotation_list_float], img_width, img_height)

                        get_bbox_height = bbox_format[0]['h'] - bbox_format[0]['y']
                        get_bbox_width = bbox_format[0]['w'] - bbox_format[0]['x']

                        get_bbox_area = get_bbox_height * get_bbox_width

                        if get_bbox_area < (img_area/sz_thresh):  # this annotation is a small annotation and are kept
                            mod_keep_all_annotations.append(mod_annotation_list_float)
                fp.seek(0)
                fp.close()

            # Now iterate through the all modified annotation and then create a new file to write it
            get_file_name_with_ext = os.path.basename(annotation_file_path)
            make_saving_path_complete = os.path.join(new_dir_path, get_file_name_with_ext)

            if len(mod_keep_all_annotations) > 0:
                file_handle_to_write = create_file_if_not_exists(make_saving_path_complete)
                for get_line_annotation in mod_keep_all_annotations:
                    for get_vals in get_line_annotation:
                        file_handle_to_write.write(str(get_vals))
                        file_handle_to_write.write(" ")
                    file_handle_to_write.write("\n")
                file_handle_to_write.close()
                mod_file_cnt = mod_file_cnt + 1

            else:
                # that means all the annotations of the image is badly formatted and there are no good annotation
                get_dir_only = os.path.dirname(full_file_path)
                get_dir_only = str(Path(get_dir_only).parents[0])  # get one level up in the directory
                get_dir_only = os.path.join(get_dir_only, "images")

                img_file_name_with_ext = os.path.basename(full_file_path)
                img_file_name_no_ext = os.path.splitext(img_file_name_with_ext)[0]

                make_img_file_name_only = img_file_name_no_ext + ".jpg"

                full_img_path_to_delete = os.path.join(get_dir_only, make_img_file_name_only)

                # delete the image file from the folder
                if os.path.isfile(full_img_path_to_delete):
                    os.remove(full_img_path_to_delete)

        print("check me at the end")
