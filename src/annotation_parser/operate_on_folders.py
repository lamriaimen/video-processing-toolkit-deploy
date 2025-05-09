from utils.basic_operation import *
from annotation_parser.utils.file_processing import ProcessFile


class OperateOnFolders:

    def __init__(self):
        print(" I am inside init function")

    @staticmethod
    def modify_folders_for_second_time_change(dataset_folder_path):
        """
            Function to modify the folder names as following :
            train->labels_original := train->labels
            train->labels:= Delete

            test->labels_original := test->labels
            test->labels:= Delete

            valid->labels_original := valid->labels
            valid->labels:= Delete

            Args:

            Returns:

        """
        # Because this folder is a modified folder and it should be deleted
        labels_dir_path_train_1 = os.path.join(dataset_folder_path, 'train', 'labels')
        shutil.rmtree(labels_dir_path_train_1)  # delete this directory

        labels_dir_path_train_2 = os.path.join(dataset_folder_path, 'train', 'labels_mod')
        labels_dir_path_train_2_mod = os.path.join(dataset_folder_path, 'train', 'labels')
        os.rename(labels_dir_path_train_2, labels_dir_path_train_2_mod)

        # Because this folder is a modified folder and it should be deleted
        labels_dir_path_test_1 = os.path.join(dataset_folder_path, 'test', 'labels')
        shutil.rmtree(labels_dir_path_test_1)

        labels_dir_path_test_2 = os.path.join(dataset_folder_path, 'test', 'labels_mod')
        labels_dir_path_test_2_mod = os.path.join(dataset_folder_path, 'test', 'labels')
        os.rename(labels_dir_path_test_2, labels_dir_path_test_2_mod)

        # Because this folder is a modified folder and it should be deleted
        labels_dir_path_valid_1 = os.path.join(dataset_folder_path, 'valid', 'labels')
        shutil.rmtree(labels_dir_path_valid_1)

        labels_dir_path_valid_2 = os.path.join(dataset_folder_path, 'valid', 'labels_mod')
        labels_dir_path_valid_2_mod = os.path.join(dataset_folder_path, 'valid', 'labels')
        os.rename(labels_dir_path_valid_2, labels_dir_path_valid_2_mod)

        print("The modified labeling is complete")

    @staticmethod
    def modify_and_delete_folders_to_reset(dataset_folder_path):
        """
            Function to modify the folder names as following :
            train->labels_original := train->labels
            train->labels:= Delete

            test->labels_original := test->labels
            test->labels:= Delete

            valid->labels_original := valid->labels
            valid->labels:= Delete

            Args:

            Returns:

        """
        # Because this folder is a modified folder and it should be deleted
        labels_dir_path_train_1 = os.path.join(dataset_folder_path, 'train', 'labels')
        shutil.rmtree(labels_dir_path_train_1)  # delete this directory

        labels_dir_path_train_2 = os.path.join(dataset_folder_path, 'train', 'labels_original')
        labels_dir_path_train_2_mod = os.path.join(dataset_folder_path, 'train', 'labels')
        os.rename(labels_dir_path_train_2, labels_dir_path_train_2_mod)

        # Because this folder is a modified folder and it should be deleted
        labels_dir_path_test_1 = os.path.join(dataset_folder_path, 'test', 'labels')
        shutil.rmtree(labels_dir_path_test_1)

        labels_dir_path_test_2 = os.path.join(dataset_folder_path, 'test', 'labels_original')
        labels_dir_path_test_2_mod = os.path.join(dataset_folder_path, 'test', 'labels')
        os.rename(labels_dir_path_test_2, labels_dir_path_test_2_mod)

        # Because this folder is a modified folder and it should be deleted
        labels_dir_path_valid_1 = os.path.join(dataset_folder_path, 'valid', 'labels')
        shutil.rmtree(labels_dir_path_valid_1)

        labels_dir_path_valid_2 = os.path.join(dataset_folder_path, 'valid', 'labels_original')
        labels_dir_path_valid_2_mod = os.path.join(dataset_folder_path, 'valid', 'labels')
        os.rename(labels_dir_path_valid_2, labels_dir_path_valid_2_mod)

        print("The modified labeling is complete")

    @staticmethod
    def modify_folder_names(dataset_folder_path):
        """
            Function to modify the folder names as following :
            train->labels := train->labels_original
            train->labels_mod := train->labels

            test->labels := test->labels_original
            test->labels_mod := test->labels

            valid->labels := valid->labels_original
            valid->labels_mod := valid->labels

            Args:

            Returns:

        """
        labels_dir_path_train_1 = os.path.join(dataset_folder_path, 'train', 'labels')
        labels_dir_path_train_1_mod = os.path.join(dataset_folder_path, 'train', 'labels_original')
        shutil.move(labels_dir_path_train_1, labels_dir_path_train_1_mod)

        # if not os.path.exists(labels_dir_path_train_1_mod):
        #     os.makedirs(labels_dir_path_train_1_mod)
        # DataDescription.move_all_files_from_one_folder_to_another\
        #     (labels_dir_path_train_1, labels_dir_path_train_1_mod)

        labels_dir_path_train_2 = os.path.join(dataset_folder_path, 'train', 'labels_mod')
        labels_dir_path_train_2_mod = os.path.join(dataset_folder_path, 'train', 'labels')
        shutil.move(labels_dir_path_train_2, labels_dir_path_train_2_mod)

        labels_dir_path_test_1 = os.path.join(dataset_folder_path, 'test', 'labels')
        labels_dir_path_test_1_mod = os.path.join(dataset_folder_path, 'test', 'labels_original')
        shutil.move(labels_dir_path_test_1, labels_dir_path_test_1_mod)

        labels_dir_path_test_2 = os.path.join(dataset_folder_path, 'test', 'labels_mod')
        labels_dir_path_test_2_mod = os.path.join(dataset_folder_path, 'test', 'labels')
        shutil.move(labels_dir_path_test_2, labels_dir_path_test_2_mod)

        labels_dir_path_valid_1 = os.path.join(dataset_folder_path, 'valid', 'labels')
        labels_dir_path_valid_1_mod = os.path.join(dataset_folder_path, 'valid', 'labels_original')
        shutil.move(labels_dir_path_valid_1, labels_dir_path_valid_1_mod)

        labels_dir_path_valid_2 = os.path.join(dataset_folder_path, 'valid', 'labels_mod')
        labels_dir_path_valid_2_mod = os.path.join(dataset_folder_path, 'valid', 'labels')
        shutil.move(labels_dir_path_valid_2, labels_dir_path_valid_2_mod)

        print("The modified labeling is complete")

    @staticmethod
    def modify_and_delete_folder_names(dataset_folder_path):
        """
            Function to modify the folder names as following :
            train->labels := train->labels_original
            train->labels_mod := train->labels

            test->labels := test->labels_original
            test->labels_mod := test->labels

            valid->labels := valid->labels_original
            valid->labels_mod := valid->labels

            Args:

            Returns:

        """
        labels_dir_path_train_1 = os.path.join(dataset_folder_path, 'train', 'labels')
        shutil.rmtree(labels_dir_path_train_1)  # delete this directory

        labels_dir_path_train_2 = os.path.join(dataset_folder_path, 'train', 'labels_mod')
        labels_dir_path_train_2_mod = os.path.join(dataset_folder_path, 'train', 'labels')
        os.rename(labels_dir_path_train_2, labels_dir_path_train_2_mod)

        labels_dir_path_test_1 = os.path.join(dataset_folder_path, 'test', 'labels')
        shutil.rmtree(labels_dir_path_test_1)

        labels_dir_path_test_2 = os.path.join(dataset_folder_path, 'test', 'labels_mod')
        labels_dir_path_test_2_mod = os.path.join(dataset_folder_path, 'test', 'labels')
        os.rename(labels_dir_path_test_2, labels_dir_path_test_2_mod)

        labels_dir_path_valid_1 = os.path.join(dataset_folder_path, 'valid', 'labels')
        shutil.rmtree(labels_dir_path_valid_1)

        labels_dir_path_valid_2 = os.path.join(dataset_folder_path, 'valid', 'labels_mod')
        labels_dir_path_valid_2_mod = os.path.join(dataset_folder_path, 'valid', 'labels')
        os.rename(labels_dir_path_valid_2, labels_dir_path_valid_2_mod)

        print("The modified labeling is complete")

    @staticmethod
    def modify_folder_names_only_train(dataset_folder_path):
        """
            Function to modify the folder names of "Train" folder only as following :
            train->labels := train->labels_original
            train->labels_mod := train->labels
            Args:

            Returns:

        """
        labels_dir_path_train_1 = os.path.join(dataset_folder_path, 'train', 'labels')
        labels_dir_path_train_1_mod = os.path.join(dataset_folder_path, 'train', 'labels_original')
        os.rename(labels_dir_path_train_1, labels_dir_path_train_1_mod)

        labels_dir_path_train_2 = os.path.join(dataset_folder_path, 'train', 'labels_mod')
        labels_dir_path_train_2_mod = os.path.join(dataset_folder_path, 'train', 'labels')
        os.rename(labels_dir_path_train_2, labels_dir_path_train_2_mod)

        print("The modified labeling is complete")

    @staticmethod
    def move_all_files_from_one_folder_to_another(source_folder, destination_folder):
        """
            Function to move all the files from one folder to another:

            Args:
                source_folder = The files to move from
                destination_folder = The files to move to
            Returns:

        """
        # fetch all files
        for file_name in os.listdir(source_folder):
            # construct full file path
            source = source_folder + file_name
            destination = destination_folder + file_name
            # move only files
            if os.path.isfile(source):
                shutil.copy2(source, destination)
                # print('Moved:', file_name)

    def modify_list_of_folders(self):
        """
            Function to modify the dataset folders, which are containing several subdirectories. Hence, we will modify
            all these subdirectories
            Args:

            Returns:

        """
        dataset_path_1 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/BACKUP/ball-11/"
        self.modify_folder_names(dataset_path_1)

        # dataset_path_2 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/BACKUP/ball-12/"
        # modify_folder_names(dataset_path_2)

        # dataset_path_3 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/BACKUP/CA_Proj_Group4-1/"
        # modify_folder_names(dataset_path_3)

        # dataset_path_4 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/BACKUP/CA_Proj_Group4-2/"
        # modify_folder_names(dataset_path_4)

        # dataset_path_5 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/BACKUP/coba-10/"
        # modify_folder_names(dataset_path_5)

        # dataset_path_7 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/BACKUP/MBS4542-4/"
        # modify_folder_names(dataset_path_7)

        # dataset_path_8 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/BACKUP/MBS4542-5/"
        # modify_folder_names(dataset_path_8)

        # dataset_path_9 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/FootBall_Data/ball-8/"
        # modify_folder_names(dataset_path_9)

        # dataset_path_10 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/FootBall_Data/football-4/"
        # modify_folder_names(dataset_path_10)

        # dataset_path_11 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/FootBall_Data/football-8/"
        # modify_folder_names(dataset_path_11)

        # dataset_path_12 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/FootBall_Data/football-9/"
        # modify_folder_names(dataset_path_12)

        # dataset_path_13 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/" \
        #                   "FootBall_Data/football-11/"
        # modify_folder_names(dataset_path_13)

        # dataset_path_14 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/" \
        #                   "FootBall_Data/football-13/"
        # modify_folder_names(dataset_path_14)

        # dataset_path_15 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/" \
        #                   "FootBall_Data/Football-1"
        # modify_folder_names_only_train(dataset_path_15)

        # dataset_path_16 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/FootBall_Data/Football-4"
        # modify_folder_names_only_train(dataset_path_16)

        # dataset_path_17 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/FootBall_Data/Football-6"
        # modify_folder_names(dataset_path_17)

        # dataset_path_18 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/" \
        #                   "FootBall_Data/Soccer-Players-1"
        # modify_folder_names(dataset_path_18)

        # dataset_path_19 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/" \
        #                   "FootBall_Data/Soccer-Players-2"
        # modify_folder_names(dataset_path_19)

        # dataset_path_20 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/" \
        #                   "FootBall_Data/Soccer-Players-3"
        # modify_folder_names(dataset_path_20)
        #
        # dataset_path_21 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/" \
        #                   "FootBall_Data/Soccer-Players-4"
        # modify_folder_names(dataset_path_21)
        #
        # dataset_path_22 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/" \
        #                   "FootBall_Data/Soccer-Players-5"
        # modify_folder_names(dataset_path_22)
        #
        # dataset_path_23 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/" \
        #                   "FootBall_Data/Soccer-Players-6"
        # modify_folder_names(dataset_path_23)
        #
        # dataset_path_24 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/" \
        #                   "FootBall_Data/Soccer-Players-8"
        # modify_folder_names(dataset_path_24)
        #
        # dataset_path_25 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/" \
        #                   "FootBall_Data/Soccer-Players-9"
        # modify_folder_names(dataset_path_25)
        #
        # dataset_path_26 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/" \
        #                   "FootBall_Data/Soccer-Players-10"
        # modify_folder_names(dataset_path_26)
        #
        # dataset_path_27 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/" \
        #                   "FootBall_Data/Soccer-Players-11"
        # modify_folder_names(dataset_path_27)
        #
        # dataset_path_28 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/" \
        #                   "FootBall_Data/Soccer-Players-12"
        # modify_folder_names(dataset_path_28)
        #
        # dataset_path_29 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/" \
        #                   "FootBall_Data/Soccer-Players-13"
        # modify_folder_names(dataset_path_29)
        #
        # dataset_path_30 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/" \
        #                   "FootBall_Data/Soccer-Players-14"
        # modify_folder_names(dataset_path_30)
        #
        # dataset_path_31 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/" \
        #                   "FootBall_Data/Soccer-Players-15"
        # modify_folder_names(dataset_path_31)
        #
        # dataset_path_32 = "/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/" \
        #                   "FootBall_Data/Soccer-Players-16"
        # modify_folder_names(dataset_path_32)

    @staticmethod
    def organize_data_into_same_folder_based_folder_name(file_path_for_folder, rootdir, dst_dir):

        """
            Function to get all the folders or dataset folders, exist in "rootdir". Then for each dataset folder, we
            obtain the subdirectories i.e. "train", "test" and "valid" folders.

            Now, in the "dst_dir", we will combine
            all these folders into a single folder, which will contain "train", "test" and "valid" directories

            file_path_for_folder : This is a text file, which will contain the name of the folders to choose from
            "rootdir" and then these folders are combined to obtain a single folder in "dst_dir"

            Args:

            Returns:

        """

        # Get the folder names from the text file; consider only the folders which are not preceded by #.

        with open(file_path_for_folder) as fp:
            Lines = fp.readlines()

            pick_good_folder_names = []

            for line in Lines:
                line = line.rstrip()  # removing all the unnecessary characters
                words = line.split(' ')

                if words[0] != '#':
                    pick_good_folder_names.append(words[0].rstrip())

        dst_train_image_dir = os.path.join(dst_dir, 'train', 'images')
        dst_train_label_dir = os.path.join(dst_dir, 'train', 'labels')
        ProcessFile.create_dir_if_not_exists(dst_train_image_dir)
        ProcessFile.create_dir_if_not_exists(dst_train_label_dir)

        dst_valid_image_dir = os.path.join(dst_dir, 'valid', 'images')
        dst_valid_label_dir = os.path.join(dst_dir, 'valid', 'labels')
        ProcessFile.create_dir_if_not_exists(dst_valid_image_dir)
        ProcessFile.create_dir_if_not_exists(dst_valid_label_dir)

        dst_test_image_dir = os.path.join(dst_dir, 'test', 'images')
        dst_test_label_dir = os.path.join(dst_dir, 'test', 'labels')
        ProcessFile.create_dir_if_not_exists(dst_test_image_dir)
        ProcessFile.create_dir_if_not_exists(dst_test_label_dir)

        for folder_name in pick_good_folder_names:
            full_folder_path = os.path.join(rootdir, folder_name)

            get_train_image_paths = os.path.join(full_folder_path, 'train', 'images')
            get_train_label_paths = os.path.join(full_folder_path, 'train', 'labels')

            get_valid_image_paths = os.path.join(full_folder_path, 'valid', 'images')
            get_valid_label_paths = os.path.join(full_folder_path, 'valid', 'labels')

            get_test_image_paths = os.path.join(full_folder_path, 'test', 'images')
            get_test_label_paths = os.path.join(full_folder_path, 'test', 'labels')

            copy_images_from_dir(get_train_image_paths, dst_train_image_dir)
            copy_images_from_dir(get_train_label_paths, dst_train_label_dir)

            copy_images_from_dir(get_valid_image_paths, dst_valid_image_dir)
            copy_images_from_dir(get_valid_label_paths, dst_valid_label_dir)

            copy_images_from_dir(get_test_image_paths, dst_test_image_dir)
            copy_images_from_dir(get_test_label_paths, dst_test_label_dir)

        print('show me')

    @staticmethod
    def organize_data_into_same_folder_vogo_roboflow(rootdir_vogo, rootdir_roboflow, dst_dir):

        """
            Function to combine the data from "RoboFlow combined dataset" and "VOGO annotated dataset" together; Note
            that both the dataset folder, follow the same folder structure

            Args:

            Returns:

        """

        # Get the folder names from the text file; consider only the folders which are not preceded by

        dst_train_image_dir = os.path.join(dst_dir, 'train', 'images')
        dst_train_label_dir = os.path.join(dst_dir, 'train', 'labels')
        ProcessFile.create_dir_if_not_exists(dst_train_image_dir)
        ProcessFile.create_dir_if_not_exists(dst_train_label_dir)

        dst_test_image_dir = os.path.join(dst_dir, 'test', 'images')
        dst_test_label_dir = os.path.join(dst_dir, 'test', 'labels')
        ProcessFile.create_dir_if_not_exists(dst_test_image_dir)
        ProcessFile.create_dir_if_not_exists(dst_test_label_dir)

        # Roboflow dataset has only training images and there is no validation and testing images
        get_train_image_paths_roboflow = os.path.join(rootdir_roboflow, 'train', 'images')
        get_train_label_paths_roboflow = os.path.join(rootdir_roboflow, 'train', 'labels')

        # VOGO dataset has the training and testing dataset and there is no validation images in this dataset
        get_train_image_paths_vogo = os.path.join(rootdir_vogo, 'train', 'images')
        get_train_label_paths_vogo = os.path.join(rootdir_vogo, 'train', 'labels')

        get_test_image_paths_vogo = os.path.join(rootdir_vogo, 'test', 'images')
        get_test_label_paths_vogo = os.path.join(rootdir_vogo, 'test', 'labels')

        copy_images_from_dir(get_train_image_paths_roboflow, dst_train_image_dir)
        copy_images_from_dir(get_train_label_paths_roboflow, dst_train_label_dir)

        copy_images_from_dir(get_train_image_paths_vogo, dst_train_image_dir)
        copy_images_from_dir(get_train_label_paths_vogo, dst_train_label_dir)

        copy_images_from_dir(get_test_image_paths_vogo, dst_test_image_dir)
        copy_images_from_dir(get_test_label_paths_vogo, dst_test_label_dir)

        print('show me')

    @staticmethod
    def organize_data_from_test_valid_to_train_folder(file_path_for_folder):
        """
            Function to merge the contents from "test" and "valid" folders into the "train" folder

            test->labels := train->labels
            test->images := train->images

            valid->labels := train->labels
            valid->images := train->labels

            Args:

            Returns:

        """
        get_train_image_paths_dest = os.path.join(file_path_for_folder, 'train', 'images')
        get_train_label_paths_dest = os.path.join(file_path_for_folder, 'train', 'labels')

        get_test_image_paths = os.path.join(file_path_for_folder, 'test', 'images')
        get_test_label_paths = os.path.join(file_path_for_folder, 'test', 'labels')

        get_valid_image_paths = os.path.join(file_path_for_folder, 'valid', 'images')
        get_valid_label_paths = os.path.join(file_path_for_folder, 'valid', 'labels')

        copy_images_from_dir(get_test_image_paths, get_train_image_paths_dest)  # copy images from test and valid
        copy_images_from_dir(get_valid_image_paths, get_train_image_paths_dest)

        copy_images_from_dir(get_test_label_paths, get_train_label_paths_dest)
        copy_images_from_dir(get_valid_label_paths, get_train_label_paths_dest)

        # Then delete these folders
        shutil.rmtree(os.path.join(file_path_for_folder, 'test'))
        shutil.rmtree(os.path.join(file_path_for_folder, 'valid'))

        print('show me')

    @staticmethod
    def organize_data_into_same_folder():
        """
            Function to get all the folders or dataset folders, exist in "rootdir". Then for each dataset folder, we
            obtain the subdirectories i.e. "train", "test" and "valid" folders.

            Now, in the "dst_dir", we will combine
            all these folders into a single folder, which will contain "train", "test" and "valid" directories

            Args:

            Returns:

        """

        rootdir = '/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/FootBall_Data/'
        dst_dir = '/home/tanmoymondal/PycharmProjects/LearnPytorch/YOLO_V7/Datasets/Combined_FootBall_Data/'

        dst_train_image_dir = os.path.join(dst_dir, 'train', 'images')
        dst_train_label_dir = os.path.join(dst_dir, 'train', 'labels')

        dst_valid_image_dir = os.path.join(dst_dir, 'valid', 'images')
        dst_valid_label_dir = os.path.join(dst_dir, 'valid', 'labels')

        dst_test_image_dir = os.path.join(dst_dir, 'test', 'images')
        dst_test_label_dir = os.path.join(dst_dir, 'test', 'labels')

        keep_all_data_class_info = []

        for path in glob.glob(f'{rootdir}/*/'):
            get_train_image_paths = os.path.join(path, 'train', 'images')
            get_train_label_paths = os.path.join(path, 'train', 'labels')

            get_valid_image_paths = os.path.join(path, 'valid', 'images')
            get_valid_label_paths = os.path.join(path, 'valid', 'labels')

            get_test_image_paths = os.path.join(path, 'test', 'images')
            get_test_label_paths = os.path.join(path, 'test', 'labels')

            # copy_images_from_dir(get_train_image_paths, dst_train_image_dir)
            # copy_images_from_dir(get_train_label_paths, dst_train_label_dir)

            # copy_images_from_dir(get_valid_image_paths, dst_valid_image_dir)
            # copy_images_from_dir(get_valid_label_paths, dst_valid_label_dir)

            # copy_images_from_dir(get_test_image_paths, dst_test_image_dir)
            # copy_images_from_dir(get_test_label_paths, dst_test_label_dir)

            # dataset_name = path.split('/')
            # dataset_name = dataset_name[-2]
            # yaml_path = os.path.join(path, 'data.yaml')
            # get_num_of_class, pick_class_names = read_yaml_files(yaml_path)

            # For each dataset, we create a instance of the class to have the data structure
            # temp_instance = DataDescription()
            # temp_instance.num_of_classes = get_num_of_class
            # temp_instance.name_of_classes = pick_class_names
            # temp_instance.dataset_name = dataset_name

            # keep_all_data_class_info.append(temp_instance)

            # print("{}".format(dataset_name))
            # print(pick_class_names)

        print('show me')
