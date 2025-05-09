#!/usr/bin/env python

# Dictionary that maps class names to IDs


"""
This is the dictionary of the classes of each dataset, regarding the football
"""

class_name_to_id_mapping_UWH_3 = {"black-hat": 0,
                                  "body": 1,
                                  "bodysurface": 2,
                                  "bodyunder": 3,
                                  "swimmer": 4,
                                  "umpire": 5,
                                  "white-hat": 6}

class_name_to_id_mapping_UWH_4 = {"black-hat": 0,
                                  "body": 1,
                                  "bodysurface": 2,
                                  "bodyunder": 3,
                                  "swimmer": 4,
                                  "umpire": 5,
                                  "white-hat": 6}

class_name_to_id_mapping_UWH_5 = {"black-hat": 0,
                                  "bodysurface": 1,
                                  "bodyunder": 2,
                                  "umpire": 3,
                                  "white-hat": 4}

class_name_to_id_mapping_UWH_6 = {"black-hat": 0,
                                  "body": 1,
                                  "bodysurface": 2,
                                  "bodyunder": 3,
                                  "swimmer": 4,
                                  "umpire": 5,
                                  "white-hat": 6}

class_name_to_id_mapping_combined_1 = {"body": 0,
                                       "bodysurface": 1,
                                       "bodyunder": 2}

class_id_to_name_mapping_UWH_3 = dict(zip(class_name_to_id_mapping_UWH_3.values(),
                                          class_name_to_id_mapping_UWH_3.keys()))

class_id_to_name_mapping__UWH_4 = dict(zip(class_name_to_id_mapping_UWH_4.values(),
                                           class_name_to_id_mapping_UWH_4.keys()))

class_id_to_name_mapping__UWH_5 = dict(zip(class_name_to_id_mapping_UWH_5.values(),
                                           class_name_to_id_mapping_UWH_5.keys()))

class_id_to_name_mapping__UWH_6 = dict(zip(class_name_to_id_mapping_UWH_6.values(),
                                           class_name_to_id_mapping_UWH_6.keys()))

class_id_to_name_mapping_combined_1 = dict(zip(class_name_to_id_mapping_combined_1.values(),
                                           class_name_to_id_mapping_combined_1.keys()))
