#!/usr/bin/env python

# Dictionary that maps class names to IDs
class_name_to_id_mapping_traffic = {"trafficlight": 0,
                                    "stop": 1,
                                    "speedlimit": 2,
                                    "crosswalk": 3}

class_name_to_id_mapping_ball_11 = {0: "football",
                                    1: "others",
                                    2: "soccer"}

class_name_to_id_mapping_ball_12 = {0: "Ball",
                                    1: "football",
                                    2: "others"}

class_name_to_id_mapping_annotation_football = {0: "Ball",
                                                1: "Player",
                                                2: "Others"}

class_name_to_id_mapping_annotation_football_mod_1 = {0: "Player",
                                                      1: "Player_Cropped",
                                                      2: "Player_Blurred",
                                                      3: "Ball",
                                                      4: "Ball_Blurred"}

class_name_to_id_mapping_annotation_football_mod_2 = {0: "Player",
                                                      1: "Ball"}

class_name_to_id_mapping_CA_Proj_Group4_1 = {0: "football",
                                             1: "otherball",
                                             2: "soccer"}

class_name_to_id_mapping_CA_Proj_Group4_2 = {0: "football",
                                             1: "otherball",
                                             2: "soccer"}

class_name_to_id_mapping_coba_10 = {0: "ball",
                                    1: "goal"}

class_name_to_id_mapping_football_5 = {0: "football",
                                       1: "football2"}

class_name_to_id_mapping_MBS4542_4 = {0: "ball_2",
                                      1: "ball"}

class_name_to_id_mapping_MBS4542_5 = {0: "ball_2",
                                      1: "ball"}

class_name_to_id_mapping_ball_8 = {0: "football",
                                   1: "others"}

class_name_to_id_mapping_football_4 = {0: "football",
                                       1: "other"}

class_name_to_id_mapping_football_8 = {0: "football",
                                       1: "other"}

class_name_to_id_mapping_football_9 = {0: "football",
                                       1: "other"}

class_name_to_id_mapping_football_11 = {0: "football",
                                        1: "other"}

class_name_to_id_mapping_football_13 = {0: "football",
                                        1: "other"}

class_name_to_id_mapping_Football_1 = {0: "football",
                                       1: "other"}

class_name_to_id_mapping_Football_4 = {0: "football",
                                       1: "other"}

class_name_to_id_mapping_Football_6 = {"football": 0,
                                       "other": 1}

class_name_to_id_mapping_Soccer_Players_1 = {"Ball": 0,
                                             "NED": 1,
                                             "Ref": 2,
                                             "USA": 3}

class_name_to_id_mapping_Soccer_Players_2 = {"Ball": 0,
                                             "NED": 1,
                                             "Ref": 2,
                                             "USA": 3}

class_name_to_id_mapping_Soccer_Players_3 = {"Ball": 0,
                                             "Ref": 1,
                                             "Team1": 2,
                                             "Team2": 3}

class_name_to_id_mapping_Soccer_Players_4 = {"Ball": 0,
                                             "NED": 1,
                                             "Team1": 2,
                                             "Team2": 3}

class_name_to_id_mapping_Soccer_Players_5 = {"Ball": 0,
                                             "Player": 1,
                                             "Ref": 2}

class_name_to_id_mapping_Soccer_Players_6 = {"Ball": 0,
                                             "Player": 1,
                                             "Ref": 2}

class_name_to_id_mapping_Soccer_Players_8 = {"Ball": 0,
                                             "Player": 1,
                                             "Ref": 2}

class_name_to_id_mapping_Soccer_Players_9 = {"Ball": 0,
                                             "NED": 1,
                                             "Ref": 2,
                                             "USA": 3}

class_name_to_id_mapping_Soccer_Players_10 = {"Ball": 0,
                                              "GOAL": 1,
                                              "Goalie": 2,
                                              "NED": 3,
                                              "Ref": 4,
                                              "USA": 5}

class_name_to_id_mapping_Soccer_Players_11 = {"Ball": 0,
                                              "GOAL": 1,
                                              "Goalie": 2,
                                              "NED": 3,
                                              "Ref": 4,
                                              "USA": 5}

class_name_to_id_mapping_Soccer_Players_12 = {"Ball": 0,
                                              "NED": 1,
                                              "Ref": 2,
                                              "USA": 3}

class_name_to_id_mapping_Soccer_Players_13 = {"Ball": 0,
                                              "NED": 1,
                                              "Ref": 2,
                                              "USA": 3}

class_name_to_id_mapping_Soccer_Players_14 = {"Ball": 0,
                                              "NED": 1,
                                              "Ref": 2,
                                              "USA": 3}

class_name_to_id_mapping_Soccer_Players_15 = {"Ball": 0,
                                              "Player": 1,
                                              "Ref": 2}

class_name_to_id_mapping_Soccer_Players_16 = {"Ball": 0,
                                              "Player": 1,
                                              "Ref": 2}

class_name_to_id_mapping_Soccer_Players_17 = {"Player": 0,
                                              "Ball": 1}

class_name_to_id_mapping_Soccer_Players_18 = {"Ball": 0,
                                              "Player": 1}


class_id_to_name_mapping_traffic = dict(zip(class_name_to_id_mapping_traffic.values(),
                                            class_name_to_id_mapping_traffic.keys()))

class_id_to_name_mapping_ball_11 = dict(zip(class_name_to_id_mapping_ball_11.values(),
                                            class_name_to_id_mapping_ball_11.keys()))
class_id_to_name_mapping_ball_12 = dict(
    zip(class_name_to_id_mapping_ball_12.values(), class_name_to_id_mapping_ball_12.keys()))
class_id_to_name_mapping_CA_Proj_Group4_1 = dict(zip(class_name_to_id_mapping_CA_Proj_Group4_1.values(),
                                                     class_name_to_id_mapping_CA_Proj_Group4_1.keys()))

class_id_to_name_mapping_CA_Proj_Group4_2 = dict(zip(class_name_to_id_mapping_CA_Proj_Group4_2.values(),
                                                     class_name_to_id_mapping_CA_Proj_Group4_2.keys()))
class_id_to_name_mapping_coba_10 = dict(zip(class_name_to_id_mapping_coba_10.values(),
                                            class_name_to_id_mapping_coba_10.keys()))

class_id_to_name_mapping_football_5 = dict(zip(class_name_to_id_mapping_football_5.values(),
                                               class_name_to_id_mapping_football_5.keys()))
class_id_to_name_mapping_MBS4542_4 = dict(zip(class_name_to_id_mapping_MBS4542_4.values(),
                                              class_name_to_id_mapping_MBS4542_4.keys()))

class_id_to_name_mapping_MBS4542_5 = dict(zip(class_name_to_id_mapping_MBS4542_5.values(),
                                              class_name_to_id_mapping_MBS4542_5.keys()))

class_id_to_name_mapping_ball_8 = dict(zip(class_name_to_id_mapping_ball_8.values(),
                                           class_name_to_id_mapping_ball_8.keys()))

class_id_to_name_mapping_football_4 = dict(zip(class_name_to_id_mapping_football_4.values(),
                                               class_name_to_id_mapping_football_4.keys()))

class_id_to_name_mapping_football_8 = dict(zip(class_name_to_id_mapping_football_8.values(),
                                               class_name_to_id_mapping_football_8.keys()))

class_id_to_name_mapping_football_9 = dict(zip(class_name_to_id_mapping_football_9.values(),
                                               class_name_to_id_mapping_football_9.keys()))

class_id_to_name_mapping_football_11 = dict(zip(class_name_to_id_mapping_football_11.values(),
                                                class_name_to_id_mapping_football_11.keys()))

class_id_to_name_mapping_football_13 = dict(zip(class_name_to_id_mapping_football_13.values(),
                                                class_name_to_id_mapping_football_13.keys()))

class_id_to_name_mapping_Football_1 = dict(zip(class_name_to_id_mapping_Football_1.values(),
                                               class_name_to_id_mapping_Football_1.keys()))

class_id_to_name_mapping_Football_4 = dict(zip(class_name_to_id_mapping_Football_4.values(),
                                               class_name_to_id_mapping_Football_4.keys()))

class_id_to_name_mapping_Football_6 = dict(zip(class_name_to_id_mapping_Football_6.values(),
                                               class_name_to_id_mapping_Football_6.keys()))

class_id_to_name_mapping_Soccer_Players_1 = dict(zip(class_name_to_id_mapping_Soccer_Players_1.values(),
                                                     class_name_to_id_mapping_Soccer_Players_1.keys()))

class_id_to_name_mapping_Soccer_Players_2 = dict(zip(class_name_to_id_mapping_Soccer_Players_2.values(),
                                                     class_name_to_id_mapping_Soccer_Players_2.keys()))

class_id_to_name_mapping_Soccer_Players_3 = dict(zip(class_name_to_id_mapping_Soccer_Players_3.values(),
                                                     class_name_to_id_mapping_Soccer_Players_3.keys()))

class_id_to_name_mapping_Soccer_Players_4 = dict(zip(class_name_to_id_mapping_Soccer_Players_4.values(),
                                                     class_name_to_id_mapping_Soccer_Players_4.keys()))

class_id_to_name_mapping_Soccer_Players_5 = dict(zip(class_name_to_id_mapping_Soccer_Players_5.values(),
                                                     class_name_to_id_mapping_Soccer_Players_5.keys()))

class_id_to_name_mapping_Soccer_Players_6 = dict(zip(class_name_to_id_mapping_Soccer_Players_6.values(),
                                                     class_name_to_id_mapping_Soccer_Players_6.keys()))

class_id_to_name_mapping_Soccer_Players_8 = dict(zip(class_name_to_id_mapping_Soccer_Players_8.values(),
                                                     class_name_to_id_mapping_Soccer_Players_8.keys()))

class_id_to_name_mapping_Soccer_Players_9 = dict(zip(class_name_to_id_mapping_Soccer_Players_9.values(),
                                                     class_name_to_id_mapping_Soccer_Players_9.keys()))

class_id_to_name_mapping_Soccer_Players_10 = dict(zip(class_name_to_id_mapping_Soccer_Players_10.values(),
                                                      class_name_to_id_mapping_Soccer_Players_10.keys()))

class_id_to_name_mapping_Soccer_Players_11 = dict(zip(class_name_to_id_mapping_Soccer_Players_11.values(),
                                                      class_name_to_id_mapping_Soccer_Players_11.keys()))

class_id_to_name_mapping_Soccer_Players_12 = dict(zip(class_name_to_id_mapping_Soccer_Players_12.values(),
                                                      class_name_to_id_mapping_Soccer_Players_12.keys()))

class_id_to_name_mapping_Soccer_Players_13 = dict(zip(class_name_to_id_mapping_Soccer_Players_13.values(),
                                                      class_name_to_id_mapping_Soccer_Players_13.keys()))

class_id_to_name_mapping_Soccer_Players_14 = dict(zip(class_name_to_id_mapping_Soccer_Players_14.values(),
                                                      class_name_to_id_mapping_Soccer_Players_14.keys()))

class_id_to_name_mapping_Soccer_Players_15 = dict(zip(class_name_to_id_mapping_Soccer_Players_15.values(),
                                                      class_name_to_id_mapping_Soccer_Players_15.keys()))

class_id_to_name_mapping_Soccer_Players_16 = dict(zip(class_name_to_id_mapping_Soccer_Players_16.values(),
                                                      class_name_to_id_mapping_Soccer_Players_16.keys()))

class_id_to_name_mapping_Soccer_Players_17 = dict(zip(class_name_to_id_mapping_Soccer_Players_17.values(),
                                                      class_name_to_id_mapping_Soccer_Players_17.keys()))

class_id_to_name_mapping_Soccer_Players_18 = dict(zip(class_name_to_id_mapping_Soccer_Players_18.values(),
                                                      class_name_to_id_mapping_Soccer_Players_18.keys()))
