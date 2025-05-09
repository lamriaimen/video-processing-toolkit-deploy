from utils.basic_operation import *
import xml.etree.ElementTree as EleTree
from pathlib import Path
from annotation_parser.custom_dict import roboflow_football_data_dict as foot_data_dict
from annotation_parser.analyze_annotation_files import AnalyzeAnnotationFiles


class AnalyzeXMLFiles:

    def __init__(self):
        print(" I am inside init function")

    # Function to get the data from CVAT formatted XML annotation file
    @staticmethod
    def parse_cvat_xml(xml_file):
        """
            Function to read the XML file and extract the information in dictionary format:
            Args:
                xml_file: The path of the XML file
            Returns:
        """
        root = EleTree.parse(xml_file).getroot()

        keep_all_valid_imag_info_together = []
        get_meta_data = root.findall("image")

        # Parse the XML Tree
        for elem in get_meta_data:

            image_whole_info = {}

            image_id = int(elem.attrib["id"])
            image_full_path = elem.attrib["name"]
            image_width = int(elem.attrib["width"])
            image_height = int(elem.attrib["height"])

            image_whole_info["image_id"] = image_id
            image_whole_info["full_path"] = image_full_path
            image_whole_info["image_width"] = image_width
            image_whole_info["image_height"] = image_height

            imag_id_valid_flag = AnalyzeAnnotationFiles.verify_annotation_image_ids_range(image_id)
            if not imag_id_valid_flag:  # if the image id flag is not valid i.e. the image is out of required range
                continue

            image_tag_meta = elem.findall("tag")

            unvalid_flag = False
            if any(True for _ in image_tag_meta):

                for get_tag in image_tag_meta:
                    obtain_tag = get_tag.attrib["label"]
                    if obtain_tag == "unvalid":
                        unvalid_flag = True
                        break

            if unvalid_flag:
                continue

            image_level_all_bbox_yolo_coords = {'yolo_coords': []}
            image_level_all_bbox_attrib = {'bbox_attrib': []}

            object_metas = elem.findall("box")
            for bbox in object_metas:

                box_label = bbox.attrib["label"]
                xtl = float(bbox.attrib["xtl"])
                ytl = float(bbox.attrib["ytl"])
                xbr = float(bbox.attrib["xbr"])
                ybr = float(bbox.attrib["ybr"])

                # CVAT to yolo
                yolo_x = round(((xtl + xbr) / 2) / image_width, 6)
                yolo_y = round(((ytl + ybr) / 2) / image_height, 6)
                yolo_w = round((xbr - xtl) / image_width, 6)
                yolo_h = round((ybr - ytl) / image_height, 6)

                # Keeping all the yolo coords
                image_level_all_bbox_yolo_coords['yolo_coords'].append([box_label, yolo_x, yolo_y, yolo_w, yolo_h])

                bbox_metas = bbox.findall("attribute")

                keep_each_attribute = {}
                for attr in bbox_metas:
                    attribute_name = attr.attrib["name"]
                    attribute_value = attr.text

                    keep_each_attribute[attribute_name] = attribute_value

                image_level_all_bbox_attrib['bbox_attrib'].append(keep_each_attribute)

            # keeping all the bbox yolo coordinates info of the image
            image_whole_info["all_bbox_yolo_coords"] = image_level_all_bbox_yolo_coords

            # keeping all the bbox attribute info of the image
            image_whole_info["all_bbox_attributes_info"] = image_level_all_bbox_attrib

            keep_all_valid_imag_info_together.append(image_whole_info)

        return keep_all_valid_imag_info_together

    # Function to get the data from XML Annotation of annotated football dataset
    @staticmethod
    def extract_info_from_xml_football(xml_file):
        """
            Function to read the XML file and extract the information in dictionary format:
            Args:
                xml_file: The path of the XML file
            Returns:
        """
        root = EleTree.parse(xml_file).getroot()

        # Initialise the info dict
        info_dict = {'bboxes': []}
        attribute_dict = {'attributes': []}

        # Parse the XML Tree
        for elem in root:
            # Get the file name
            if elem.tag == "filename":
                info_dict['filename'] = elem.text

            # Get the image size
            elif elem.tag == "size":
                image_size = {}
                for sub_elem in elem:
                    if sub_elem.tag == 'width':
                        image_size['width'] = int(sub_elem.text)
                    elif sub_elem.tag == 'height':
                        image_size['height'] = int(sub_elem.text)

                    # image_size.append(int(sub_elem.text))

                info_dict['image_size'] = image_size

            # Get details of the bounding box
            elif elem.tag == "object":
                bbox = {}
                keep_all_attributes = {}

                for sub_elem in elem:
                    if sub_elem.tag == "name":
                        bbox["class"] = sub_elem.text

                    elif sub_elem.tag == "bndbox":
                        for sub_sub_elem in sub_elem:
                            if sub_sub_elem.tag == 'xmin':
                                bbox[sub_sub_elem.tag] = float(sub_sub_elem.text)
                            elif sub_sub_elem.tag == 'xmax':
                                bbox[sub_sub_elem.tag] = float(sub_sub_elem.text)
                            elif sub_sub_elem.tag == 'ymin':
                                bbox[sub_sub_elem.tag] = float(sub_sub_elem.text)
                            elif sub_sub_elem.tag == 'ymax':
                                bbox[sub_sub_elem.tag] = float(sub_sub_elem.text)

                    elif sub_elem.tag == "attributes":
                        keep_all_attributes = {sub_elem.tag: []}

                        for sub_sub_elem in sub_elem:
                            if sub_sub_elem.tag == "attribute":
                                keep_each_attribute = {}

                                for sub_sub_sub_elem in sub_sub_elem:
                                    if sub_sub_sub_elem.tag == 'name':

                                        keep_each_attribute[sub_sub_sub_elem.tag] = sub_sub_sub_elem.text
                                    elif sub_sub_sub_elem.tag == 'value':
                                        keep_each_attribute[sub_sub_sub_elem.tag] = sub_sub_sub_elem.text

                                keep_all_attributes[sub_elem.tag].append(keep_each_attribute)

                info_dict['bboxes'].append(bbox)
                attribute_dict['attributes'].append(keep_all_attributes)

        return info_dict, attribute_dict

    # Function to get the data from XML Annotation
    @staticmethod
    def extract_info_from_xml(xml_file):
        """
            Function to read the XML file and extract the information in dictionary format:
            Args:
                xml_file: The path of the XML file
            Returns:
        """
        root = EleTree.parse(xml_file).getroot()

        # Initialise the info dict
        info_dict = {'bboxes': []}

        # Parse the XML Tree
        for elem in root:
            # Get the file name
            if elem.tag == "filename":
                info_dict['filename'] = elem.text

            # Get the image size
            elif elem.tag == "size":
                image_size = []
                for sub_elem in elem:
                    image_size.append(int(sub_elem.text))

                info_dict['image_size'] = tuple(image_size)

            # Get details of the bounding box
            elif elem.tag == "object":
                bbox = {}
                for sub_elem in elem:
                    if sub_elem.tag == "name":
                        bbox["class"] = sub_elem.text

                    elif sub_elem.tag == "bndbox":
                        for sub_sub_elem in sub_elem:
                            bbox[sub_sub_elem.tag] = int(sub_sub_elem.text)
                info_dict['bboxes'].append(bbox)

        return info_dict

    # Convert the info dict to the required yolo format and write it to disk
    @staticmethod
    def convert_xml_dict_to_yolov5(info_dict):
        """
            Function to read the dictionary which is created from the XML file. By using this dictionary, we can convert
            into the read able text files
            Args:
                info_dict: The dictionary where the information is stored
            Returns:
        """

        get_no_of_bounding_box_in_dict = len(info_dict[0]["bboxes"])
        get_no_of_attributes_in_dict = len(info_dict[1]["attributes"])

        get_img_name = info_dict[0]["filename"]
        get_img_height = info_dict[0]["image_size"]["height"]
        get_img_width = info_dict[0]["image_size"]["width"]

        keep_all_blur_crop_values = []
        if get_no_of_attributes_in_dict == get_no_of_bounding_box_in_dict:
            for ii in range(get_no_of_bounding_box_in_dict):

                bbox = info_dict[0]["bboxes"][ii]
                obj_class = bbox["class"]
                obj_xmin = bbox["xmin"]
                obj_ymin = bbox["ymin"]
                obj_xmax = bbox["xmax"]
                obj_ymax = bbox["ymax"]

                get_all_attributes = info_dict[1]["attributes"][ii]["attributes"]

                # Loop through all the attributes
                blurred_value = False  # initialize the variables
                cropped_value = False  # initialize the variables
                for each_attrib in get_all_attributes:
                    if each_attrib["name"] == "blurred":  # then we will get to know the blurred property of this
                        # attribute
                        blurred_value = (each_attrib["value"])

                    elif each_attrib["name"] == "cropped":  # then we will get to know the cropped property of this
                        # attribute
                        cropped_value = (each_attrib["value"])

                keep_all_blur_crop_values.append([obj_class, obj_xmin, obj_ymin, obj_xmax, obj_ymax,
                                                  blurred_value, cropped_value])
        else:
            assert "The two dictionaries are not of the same size"

        print_buffer = []

        # For each bounding box

        for item_in_keep_all in keep_all_blur_crop_values:
            class_name = item_in_keep_all[0]
            obj_xmin = item_in_keep_all[1]
            obj_ymin = item_in_keep_all[2]
            obj_xmax = item_in_keep_all[3]
            obj_ymax = item_in_keep_all[4]
            blurred_value = item_in_keep_all[5]
            cropped_value = item_in_keep_all[6]

            class_id = 0
            if class_name == "player" and blurred_value == "False" and cropped_value == "False":
                class_id = 0
            elif class_name == "player" and blurred_value == "False" and cropped_value == "True":
                class_id = 1
            elif class_name == "player" and blurred_value == "True" and cropped_value == "False":
                class_id = 2
            elif class_name == "ball" and blurred_value == "False":
                class_id = 3
            elif class_name == "ball" and blurred_value == "True":
                class_id = 4
            else:
                assert "Invalid class. The class must be from the list of of 5 classes"

            # Transform the bbox co-ordinates as per the format required by YOLO v5
            b_center_x = (obj_xmin + obj_xmax) / 2
            b_center_y = (obj_ymin + obj_ymax) / 2
            b_width = (obj_xmax - obj_xmin)
            b_height = (obj_ymax - obj_ymin)

            # Normalise the co-ordinates by the dimensions of the image
            image_w = get_img_width
            image_h = get_img_height

            b_center_x /= image_w
            b_center_y /= image_h
            b_width /= image_w
            b_height /= image_h

            # Write the bbox details to the file
            print_buffer.append(
                "{} {:.3f} {:.3f} {:.3f} {:.3f}".format(class_id, b_center_x, b_center_y, b_width, b_height))

        dir_name = os.path.dirname(get_img_name)
        base_name = os.path.basename(get_img_name)

        get_dir_one_level_up = str(Path(dir_name).parents[0])  # get one level up in the directory

        dst_label_path_dir = os.path.join("/home/tanmoymondal/Downloads/fooball_keyframe/obj_train_data/",
                                          get_dir_one_level_up, 'converted_yolo_annotations')
        if not os.path.exists(dst_label_path_dir):
            os.makedirs(dst_label_path_dir)

        # Name of the file which we have to save
        save_file_name = os.path.join(dst_label_path_dir, base_name.replace("jpg", "txt"))

        # if not os.path.exists(save_file_name):
        #     open(save_file_name, "w")

        # Save the annotation to disk
        print("\n".join(print_buffer), file=open(save_file_name, "w"))

    # Convert the info dict to the required yolo format and write it to disk
    @staticmethod
    def convert_to_yolov5(info_dict):
        """
            Function to read the XML file and extract the information in dictionary format:
            Args:
                info_dict: The dictionary where the information is stored
            Returns:
        """

        print_buffer = []
        class_id = 0
        # For each bounding box
        for b in info_dict["bboxes"]:
            try:
                class_id = foot_data_dict.class_name_to_id_mapping_traffic[b["class"]]
            except KeyError:
                print("Invalid Class. Must be one from ", foot_data_dict.class_name_to_id_mapping_traffic.keys())

            # Transform the bbox co-ordinates as per the format required by YOLO v5
            b_center_x = (b["xmin"] + b["xmax"]) / 2
            b_center_y = (b["ymin"] + b["ymax"]) / 2
            b_width = (b["xmax"] - b["xmin"])
            b_height = (b["ymax"] - b["ymin"])

            # Normalise the co-ordinates by the dimensions of the image
            image_w, image_h, image_c = info_dict["image_size"]
            b_center_x /= image_w
            b_center_y /= image_h
            b_width /= image_w
            b_height /= image_h

            # Write the bbox details to the file
            print_buffer.append(
                "{} {:.3f} {:.3f} {:.3f} {:.3f}".format(class_id, b_center_x, b_center_y, b_width, b_height))

        # Name of the file which we have to save
        save_file_name = os.path.join("Datasets/Road_Sign_Dataset/all_annotations",
                                      info_dict["filename"].replace("png", "txt"))

        # Save the annotation to disk
        print("\n".join(print_buffer), file=open(save_file_name, "w"))
