from pathlib import Path
import numpy as np
from utils.basic_operation import *
from PIL import ImageDraw, Image
import matplotlib.pyplot as plt
import random

from annotation_parser.analyze_xml_files import AnalyzeXMLFiles


class DrawAnnotations:

    def __init__(self):
        print(" I am inside init function")

    @staticmethod
    def plot_bounding_box(image, annotation_list, image_annotation_path, class_id_to_name_mapping):

        """
            Function to actually draw the annotation on the image

            Args:
                image: The numpy array of the image
                annotation_list: The list which contains the coordinate of four corners of each annotation
                image_annotation_path: The path where the annotated image will be stored, after drawing the annotation

                class_id_to_name_mapping: The dictionary which contains the class name : class index, which need to be
                drawn or written on the image

            Returns:

        """
        flag_pass = True

        dir_name_only = os.path.dirname(image_annotation_path)
        file_name_with_ext = os.path.basename(image_annotation_path)

        annotations = np.array(annotation_list)
        w, h = image.size

        transformed_annotations = np.copy(annotations)
        transformed_annotations[:, [1, 3]] = annotations[:, [1, 3]] * w
        transformed_annotations[:, [2, 4]] = annotations[:, [2, 4]] * h

        transformed_annotations[:, 1] = transformed_annotations[:, 1] - (transformed_annotations[:, 3] / 2)
        transformed_annotations[:, 2] = transformed_annotations[:, 2] - (transformed_annotations[:, 4] / 2)
        transformed_annotations[:, 3] = transformed_annotations[:, 1] + transformed_annotations[:, 3]
        transformed_annotations[:, 4] = transformed_annotations[:, 2] + transformed_annotations[:, 4]

        # Creating an empty dictionary
        unique_class_dict = {}
        annotation_cnt = 0
        for ann in transformed_annotations:
            obj_cls = 0.0
            x0 = 0.0
            y0 = 0.0
            x1 = 0.0
            y1 = 0.0
            try:
                obj_cls, x0, y0, x1, y1 = ann
            except:
                print("An exception occurred")

                flag_pass = False
                # return flag_pass

            temp_keep_annotation_coords = [x0, y0, x1, y1]
            # for the very first time only
            if annotation_cnt == 0:
                unique_class_dict[str(obj_cls)] = list()
                unique_class_dict[str(obj_cls)].append(temp_keep_annotation_coords)
            else:
                add_values_in_dict(unique_class_dict, str(obj_cls), temp_keep_annotation_coords)
            annotation_cnt = annotation_cnt + 1

        for key, value in unique_class_dict.items():
            im_draw = image.copy()
            plotted_image = ImageDraw.Draw(im_draw)
            obj_cls = int(float(key))

            folder_name = "/class" + "_" + str(obj_cls) + "/"
            dir_name_only_1 = dir_name_only + folder_name
            if not os.path.exists(os.path.dirname(dir_name_only_1)):
                os.makedirs(os.path.dirname(dir_name_only_1))

            full_file_path_to_save = dir_name_only_1 + file_name_with_ext

            # Iterate for the number of entries i.e. the number of boxes for this class; to be plotted on the image
            for annot in value:
                x0, y0, x1, y1 = annot
                plotted_image.rectangle(((x0, y0), (x1, y1)))
                plotted_image.text((x0, y0 - 10), class_id_to_name_mapping[(int(obj_cls))])

            plt.imsave(full_file_path_to_save, np.array(im_draw))  # save each image separately

        return flag_pass

    def draw_bounding_box(self, annotations):

        """
            Function to draw the annotations on the image

            Args:
                annotations: The list which contains coordinates of four corners of all the annotations, to draw

            Returns:

        """
        # Get any random annotation file
        get_rand_num = random.randint(0, len(annotations))
        annotation_file = annotations[get_rand_num]  # random.choice(annotations)
        with open(annotation_file, "r") as file:
            annotation_list = file.read().split("\n")[:-1]
            annotation_list = [x.split(" ") for x in annotation_list]
            annotation_list = [[float(y) for y in x] for x in annotation_list]

        # Get the corresponding image file
        image_file = annotation_file.replace("annotations", "images").replace("txt", "png")
        assert os.path.exists(image_file)

        # Load the image
        image = Image.open(image_file)

        # Plot the Bounding Box
        self.plot_bounding_box(image, annotation_list)

    # This code is only to understand the bounding boxes for each labels

    def draw_bounding_box_for_each_class_separately(self, dataset_folder_path, class_id_to_name_mapping):

        """
            Function to draw the bounding boxes around each object classes which are mentioned in
            "class_id_to_name_mapping"

            Args:
                dataset_folder_path: The path of the specific dataset
                class_id_to_name_mapping: The dictionary which contains the class name : class index, so that we can use
                it to write the class name in the image

            Returns:

        """
        # Get all the files from the directory

        labels_dir_path = os.path.join(dataset_folder_path, 'train', 'labels')
        get_all_file_paths = get_files_in_dir(labels_dir_path)

        bad_cnt = 0
        for annotation_file_path in get_all_file_paths:
            full_file_path = os.path.join(labels_dir_path, annotation_file_path)

            with open(full_file_path, "r") as fp:

                all_lines = fp.readlines()
                keep_all_annotations = []
                for line in all_lines:
                    annotation_list = line.split(" ")

                    if '\n' in annotation_list:
                        annotation_list.remove('\n')

                    if len(annotation_list) < 6:  # that means there are 5 elements
                        annotation_list_float = []
                        for x in annotation_list:
                            annotation_list_float.append(float(x))

                        keep_all_annotations.append(annotation_list_float)

            # Get the corresponding image file
            image_file = full_file_path.replace("labels", "images").replace("txt", "jpg")

            image_annotation_path = image_file.replace("images", "image_annotation")
            image_annotation_path = image_annotation_path.replace("train/", "train_")

            if not os.path.exists(os.path.dirname(image_annotation_path)):
                os.makedirs(os.path.dirname(image_annotation_path))

            # The list is empty and the corresponding image doesn't exist then delete the annotation text file
            if (len(keep_all_annotations) == 0) & (not os.path.exists(image_file)):
                os.remove(full_file_path)
                bad_cnt = bad_cnt + 1
                print("The bad image count is : \n", bad_cnt)
                continue
            else:
                if not os.path.exists(image_file):  # ideally we shouldn't enter here
                    assert os.path.exists(image_file)

            # Load the image
            image = Image.open(image_file)

            if len(keep_all_annotations) > 0:  # the size is at least 1
                flag_pass = self.plot_bounding_box(image, keep_all_annotations, image_annotation_path,
                                                   class_id_to_name_mapping)

            # Plot the Bounding Box
            # if not flag_pass:
            #     print("An exception occurred")

    @staticmethod
    def call_draw_bounding_box_football_annotation(list_img_paths):
        """

        Args:
            list_img_paths:

        Returns:

        """
        # Get all the files from the directory

        # labels_dir_path = os.path.join(dataset_folder_path, 'train', 'labels')
        # get_all_file_paths = get_files_in_dir(labels_dir_path)

        for img_file_path in list_img_paths:
            img_file_name_only, _ = os.path.splitext(os.path.basename(img_file_path))

            # Get the corresponding image file
            img_file_path.replace("jpg", "txt")
            label_path_xml = img_file_path.replace('FootBall_Video_Data_Server', 'Annnotation_XML')
            label_path_xml = label_path_xml.replace('.jpg', '.xml')

            # here we obtain the dictionary, which stores the data read from .XML file
            get_meta_data = AnalyzeXMLFiles.extract_info_from_xml_football(label_path_xml)

            AnalyzeXMLFiles.convert_xml_dict_to_yolov5(get_meta_data)
            # DrawAnnotations.draw_bounding_box_football_annotation(label_path, img_file_path, img_file_name_only,
            #                                                       img_file_extension_only)

    def draw_bounding_box_football_annotation(self, label_path, img_file_path, img_file_name_only,
                                              img_file_extension_only, get_class_name_to_id_mapping):
        convert_label_path = Path(label_path)
        label_path_one_level_up = str(convert_label_path.parent.parent)

        dst_label_path_dir = os.path.join(label_path_one_level_up, 'annotated_imgs')
        if not os.path.exists(os.path.dirname(dst_label_path_dir)):
            os.makedirs(os.path.dirname(dst_label_path_dir))

        # Load the image
        image = Image.open(img_file_path)

        with open(label_path, "r") as fp:

            all_lines = fp.readlines()
            keep_all_annotations = []
            for line in all_lines:
                annotation_list = line.split(" ")

                if '\n' in annotation_list:
                    annotation_list.remove('\n')

                if len(annotation_list) < 6:  # that means there are 5 elements
                    annotation_list_float = []
                    for x in annotation_list:
                        annotation_list_float.append(float(x))

                    keep_all_annotations.append(annotation_list_float)

        if len(keep_all_annotations) > 0:  # the size is at least 1
            complete_path_img_save = os.path.join(dst_label_path_dir, img_file_name_only + img_file_extension_only)
            flag_pass = self.plot_bounding_box(image, keep_all_annotations, complete_path_img_save,
                                               get_class_name_to_id_mapping)

        # Plot the Bounding Box
        # if not flag_pass:
        #     print("An exception occurred")
