class AnalyzeAnnotationFiles:

    def __init__(self):
        print(" I am inside init function")

    @staticmethod
    def read_file_del_cls_get_needed_contents(full_file_path, conversion_list_dict):
        """
        Function to read the annotation file and extract only the entries of the classes which are mentioned in
        conversion_list_dict

        Args:
            conversion_list_dict: The dictionary which contain the required classes
            full_file_path: The complete path of the file
        Returns:
            mod_keep_all_annotations: The filtered list, containing only the needed annotations
        """

        with open(full_file_path, "r") as fp:

            all_lines = fp.readlines()
            mod_keep_all_annotations = []

            for line in all_lines:
                annotation_list = line.split(" ")

                if len(annotation_list) < 6:  # that means there are 5 elements in the list
                    annotation_list_float = []
                    mod_annotation_list_float = []

                    for x in annotation_list:
                        annotation_list_float.append(float(x))
                        mod_annotation_list_float.append(float(x))

                    # here you change the 1st entry of the list i.e. annotation_list_float; which represent class
                    # index
                    class_indx = str(int(annotation_list_float[0]))
                    if class_indx not in conversion_list_dict:  # if this class name exists in the
                        # conversion_list_dict
                        mod_keep_all_annotations.append(mod_annotation_list_float)
            fp.seek(0)
            fp.close()

            return mod_keep_all_annotations

    @staticmethod
    def read_file_mod_cls_get_needed_contents(full_file_path, conversion_list_dict):
        """
        Function to read the annotation file and extract only the entries of the classes which are mentioned in
        conversion_list_dict

        Args:
            conversion_list_dict: The dictionary which contain the required classes
            full_file_path: The complete path of the file
        Returns:
            mod_keep_all_annotations: The filtered list, containing only the needed annotations
        """

        with open(full_file_path, "r") as fp:

            all_lines = fp.readlines()
            mod_keep_all_annotations = []

            for line in all_lines:
                annotation_list = line.split(" ")

                if '\n' in annotation_list:
                    annotation_list.remove('\n')

                if len(annotation_list) < 6:  # that means there are 5 elements in the list
                    annotation_list_float = []
                    mod_annotation_list_float = []

                    for x in annotation_list:
                        annotation_list_float.append(float(x))
                        mod_annotation_list_float.append(float(x))
                    #
                    # here you change the 1st entry of the list i.e. annotation_list_float; which represent class
                    # index
                    class_indx = str(int(annotation_list_float[0]))
                    if class_indx in conversion_list_dict:  # if this class name exists in the conversion_list_dict
                        get_mod_class = conversion_list_dict.get(class_indx)
                        mod_annotation_list_float[0] = int(get_mod_class)

                    mod_keep_all_annotations.append(mod_annotation_list_float)
            fp.seek(0)
            fp.close()

            return mod_keep_all_annotations

    @staticmethod
    def read_folder_path_annotated_football_data(txt_file_path):
        """
            Function to read the .txt file of the manual annotation done for football dataset. We read each image
            path from the textfile and then get only the image file name and accept only certain number of images (the
            one which are corrected manually, and we can get the range of image names/numbers from the CVAT interface)
            Args:
                txt_file_path: The .yaml file path

            Returns:
                list_valid_img_paths: The list of image paths which are valid i.e. whose annotation are manually
                corrected
        """
        start_indx_imgs = [38000, 37500, 37000, 36500, 36000, 35500]
        end_indx_imgs = [38302, 37999, 37499, 36999, 36499, 35999]

        with open(txt_file_path, "r") as fp:

            all_lines = fp.readlines()
            keep_filtered_imgs_paths = []

            line_cnt = 1
            for line in all_lines:

                if (start_indx_imgs[0] <= line_cnt <= end_indx_imgs[0]) or \
                        (start_indx_imgs[1] <= line_cnt <= end_indx_imgs[1]) or \
                        (start_indx_imgs[2] <= line_cnt <= end_indx_imgs[2]) or \
                        (start_indx_imgs[3] <= line_cnt <= end_indx_imgs[3]) or \
                        (start_indx_imgs[4] <= line_cnt <= end_indx_imgs[4]) or \
                        (start_indx_imgs[5] <= line_cnt <= end_indx_imgs[5]):
                    line = line.replace('\n', '')
                    keep_filtered_imgs_paths.append(line)

                line_cnt = line_cnt + 1
            fp.seek(0)
            fp.close()

            return keep_filtered_imgs_paths

    @staticmethod
    def read_yaml_files(file_path):
        """
            Function to read the .yaml file and extract the information
            Args:
                file_path: The .yaml file path

            Returns:
                get_num_of_class: The number of classes, mentioned in the .yaml file
                pick_class_names: The class names, mentioned in the .yaml file
        """

        count = 0
        with open(file_path) as fp:
            Lines = fp.readlines()

            pick_class_flag = False
            pick_class_names = []

            for line in Lines:
                words = line.split(' ')

                if words[0] == 'nc:':
                    pick_class_flag = False  # end of picking of class names
                    get_num_of_class = int(words[1])
                    # pick_class_names.clear()

                if pick_class_flag:
                    pick_class_names.append(words[1].rstrip())

                if words[0].rstrip() == 'names:':
                    pick_class_flag = True

                count += 1

        return get_num_of_class, pick_class_names

    @staticmethod
    def verify_annotation_image_ids_range(individual_img_id):
        """
        This function will verify whether the image id is within the given range image ids or not

        Args:
            individual_img_id: The individual images id

        Returns:

        """
        imag_id_valid_flag = False

        start_indx_imgs = [38000, 37500, 37000, 36500, 36000, 35500]
        end_indx_imgs = [38302, 37999, 37499, 36999, 36499, 35999]

        if (start_indx_imgs[0] <= individual_img_id <= end_indx_imgs[0]) or \
                (start_indx_imgs[1] <= individual_img_id <= end_indx_imgs[1]) or \
                (start_indx_imgs[2] <= individual_img_id <= end_indx_imgs[2]) or \
                (start_indx_imgs[3] <= individual_img_id <= end_indx_imgs[3]) or \
                (start_indx_imgs[4] <= individual_img_id <= end_indx_imgs[4]) or \
                (start_indx_imgs[5] <= individual_img_id <= end_indx_imgs[5]):
            imag_id_valid_flag = True

        return imag_id_valid_flag
