import os
import random
import shutil

from annotation_parser.utils.file_processing import ProcessFile
from annotation_parser.modify_annotations_files import ModifyAnnotationFiles


def generate_random_numbers(st_indx, end_indx, num_vals):
    get_vals_arr = []
    try:
        get_vals_arr = random.sample(range(st_indx, end_indx), num_vals)
    except ValueError:
        print('Sample size exceeded population size.')

    return get_vals_arr


def generate_cross_validation_set(base_path_orig_img, folder_path, good_file_path):
    train_file_path = folder_path + "/training.txt"
    test_file_path = folder_path + "/testing.txt"

    f_train = open(train_file_path, 'w+')  # open file in write mode
    f_test = open(test_file_path, 'w+')  # open file in write mode

    with open(good_file_path, "r") as fp:
        file_list = fp.readlines()

        lenCnt = len(file_list)
        cnt1 = 0
        cnt2 = int(lenCnt * 0.7)  # take 70 % as the training set

        get_indx_train = generate_random_numbers(cnt1, lenCnt, cnt2)  # the list of non-redundant values

        list_total = [*range(0, lenCnt, 1)]  # keep all the values in the list

        # get only the values which does not exist in "get_indx_train"
        additional_list = []
        for i in list_total:
            if i not in get_indx_train:
                additional_list.append(i)

        # writing in training file
        for i_train in get_indx_train:
            temp_file_path = file_list[i_train].replace("\n", "")

            if "Nils_backgd_removed_images" in temp_file_path:
                temp_file_path = temp_file_path.replace("Nils_backgd_removed_images", "i_frames")
            elif "backgd_removed_images" in temp_file_path:
                temp_file_path = temp_file_path.replace("backgd_removed_images", "i_frames")

            temp_file_path = os.path.join(base_path_orig_img, temp_file_path)

            f_train.write(temp_file_path)
            f_train.write('\n')

        # writing in testing file
        for i_test in additional_list:
            temp_file_path = file_list[i_test].replace("\n", "")

            if "Nils_backgd_removed_images" in temp_file_path:
                temp_file_path = temp_file_path.replace("Nils_backgd_removed_images", "i_frames")
            elif "backgd_removed_images" in temp_file_path:
                temp_file_path = temp_file_path.replace("backgd_removed_images", "i_frames")

            temp_file_path = os.path.join(base_path_orig_img, temp_file_path)

            f_test.write(temp_file_path)
            f_test.write('\n')

        f_train.close()
        f_test.close()


def only_testing_folder_image_correction(cross_valid_path, num_cross_validation):
    """
    This function is for correcting the image in testing folder. Before, it was background removed images. Now, we make
    it no background removed images
    Returns:

    """

    for i_folder in range(0, num_cross_validation):
        folder_path = cross_valid_path + "Folder_" + str(i_folder)

        test_imgs_path = folder_path + "/test/images"
        test_file_path = folder_path + "/testing.txt"
        f_test = open(test_file_path, 'r')  # open file in read mode
        all_lines_test = f_test.readlines()

        for test_line in all_lines_test:
            test_img_path_complete = test_line.replace("\n", "")

            if "Nils_backgd_removed_images" in test_img_path_complete:
                test_img_path_complete = test_img_path_complete.replace("Nils_backgd_removed_images", "i_frames")
            elif "backgd_removed_images" in test_img_path_complete:
                test_img_path_complete = test_img_path_complete.replace("backgd_removed_images", "i_frames")

            file_name_with_ext = os.path.basename(test_img_path_complete)

            dest_test_img_file_path = os.path.join(test_imgs_path, file_name_with_ext)
            test_img_path_complete = test_img_path_complete.replace("Downloads", "Videos")
            shutil.copy(test_img_path_complete, dest_test_img_file_path)


def generate_cross_validation_images(cross_valid_path, all_labels_path_str, num_cross_validation):

    for i_folder in range(0, num_cross_validation):

        folder_path = cross_valid_path + "Folder_" + str(i_folder)

        train_imgs_path = folder_path + "/train/images"
        train_labels_path = folder_path + "/train/labels"

        test_imgs_path = folder_path + "/test/images"
        test_labels_path = folder_path + "/test/labels"

        if not os.path.isdir(train_imgs_path):
            os.makedirs(train_imgs_path)

        if not os.path.isdir(train_labels_path):
            os.makedirs(train_labels_path)

        if not os.path.isdir(test_imgs_path):
            os.makedirs(test_imgs_path)

        if not os.path.isdir(test_labels_path):
            os.makedirs(test_labels_path)

        train_file_path = folder_path + "/training.txt"
        test_file_path = folder_path + "/testing.txt"

        f_train = open(train_file_path, 'r')  # open file in read mode
        f_test = open(test_file_path, 'r')  # open file in read mode

        all_lines_train = f_train.readlines()
        all_lines_test = f_test.readlines()

        for train_line in all_lines_train:
            train_img_path_complete = train_line.replace("\n", "")

            file_name_with_ext = os.path.basename(train_img_path_complete)
            name_only = file_name_with_ext.split('.')[0]
            filename_only = name_only + ".txt"

            source_labels_path = train_img_path_complete.replace("i_frames", all_labels_path_str)
            source_labels_path = os.path.join(ProcessFile.get_directory_only(source_labels_path), filename_only)
            dest_labels_path = os.path.join(train_labels_path, filename_only)

            dest_train_img_file_path = os.path.join(train_imgs_path, file_name_with_ext)

            shutil.copy(train_img_path_complete, dest_train_img_file_path)
            shutil.copy(source_labels_path, dest_labels_path)

        for test_line in all_lines_test:
            test_img_path_complete = test_line.replace("\n", "")

            file_name_with_ext = os.path.basename(test_img_path_complete)
            name_only = file_name_with_ext.split('.')[0]
            filename_only = name_only + ".txt"

            source_labels_path = test_img_path_complete.replace("i_frames", all_labels_path_str)
            source_labels_path = os.path.join(ProcessFile.get_directory_only(source_labels_path), filename_only)
            dest_labels_path = os.path.join(test_labels_path, filename_only)

            dest_test_img_file_path = os.path.join(test_imgs_path, file_name_with_ext)

            shutil.copy(test_img_path_complete, dest_test_img_file_path)
            shutil.copy(source_labels_path, dest_labels_path)


def start_creating_cross_validation(base_path_orig_img, base_path, num_cross_validation, good_file_name):
    """
        In this function, we will create the folders where the cross validation folders will be created

        Args:
            good_file_name: The text file where all good image paths are saved
            num_cross_validation: The number of cross validation folder is required
            base_path_orig_img: The path where the original images are stored

            base_path: The path where I want to have multiple folders which will contain the files for cross validation
        Returns:

    """

    filename = os.path.join(base_path, 'cross_validation/')
    for i_folder in range(0, num_cross_validation):

        folder_path = filename + "Folder_" + str(i_folder)
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)

        generate_cross_validation_set(base_path_orig_img, folder_path, good_file_name)


def main():
    print("initialising...")
    # The base path to append before to obtain the complete path, where the original images are stored
    base_path_orig_img = '/home/tanmoymondal/Videos/fooball_keyframe/obj_train_data/'

    # The path where I want to have multiple folders which will contain the files for cross validation
    base_path = '/home/tanmoymondal/Videos/fooball_keyframe/'
    num_cross_validation = 3
    good_file_name_1 = "/home/tanmoymondal/Videos/fooball_keyframe/exp_dataset_1.txt"

    start_creating_cross_validation(base_path_orig_img, base_path, num_cross_validation, good_file_name_1)

    # The path where I want to have multiple folders which will contain the files for cross validation
    cross_valid_path = '/home/tanmoymondal/Videos/fooball_keyframe/cross_validation/'
    all_labels_path = 'cvat_converted_yolo_annotations_2_classes'

    # generate_cross_validation_images(cross_valid_path, all_labels_path, num_cross_validation)

    """
     This function was needed because, before there was an error that I was taking the testing images from the 
     background removed folder
    """
    # only_testing_folder_image_correction(cross_valid_path, num_cross_validation)

    """
     There were some problems in the annotation files of the testing folder of each cross validation. Hence I modify 
     the class label from 1 to 0 and from 0 to 1
    """
    update_dict = {'1': 0, '0': 1}
    get_all_annot_paths = "/home/tanmoymondal/Videos/fooball_keyframe/cross_validation/Folder_2/test/labels/"
    get_all_file_paths_train = ProcessFile.get_all_text_files_in_dir(get_all_annot_paths)

    ModifyAnnotationFiles.modify_annotations_into_files(get_all_file_paths_train, get_all_annot_paths, update_dict)


if __name__ == '__main__':
    main()
