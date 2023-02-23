import os
import json

import game_state

FILE = "scores.json"


def create_score_file():
    try:
        file = open(FILE, "w")
        json.dump({"profiles": [{}], "last_profile": game_state.profile_name, "last_second_profile": game_state.second_profile_name}, file, indent=4)
        file.close()
    except IOError as e:
        print(e)


def open_score_file(access_type="r"):
    if os.path.exists(FILE):
        try:
            return open(FILE, access_type)
        except IOError as e:
            print(e)
            return None
    else:
        create_score_file()


def get_JSON(file):
    try:
        return json.load(file)
    except Exception as e:
        print(e)
        return dict()


def write_to_file(json_dict: dict):
    over_file = open_score_file("w")
    json.dump(json_dict, over_file, indent=4)
    over_file.close()


def set_last_profile(profile: str):
    file = open_score_file()
    json_dict = get_JSON(file)
    file.close()
    json_dict["last_profile"] = profile
    write_to_file(json_dict)


def set_last_second_profile(profile: str):
    file = open_score_file()
    json_dict = get_JSON(file)
    file.close()
    json_dict["last_second_profile"] = profile
    write_to_file(json_dict)


def get_last_profile():
    last_profile = game_state.profile_name
    file = open_score_file()
    if file is not None:
        json_dict: dict = get_JSON(file)
        if json_dict is not None:
            if "last_profile" in json_dict:
                last_profile = json_dict["last_profile"]
    if file is not None:
        file.close()
    return last_profile


def get_last_second_profile():
    last_second_profile = game_state.second_profile_name
    file = open_score_file()
    if file is not None:
        json_dict: dict = get_JSON(file)
        if json_dict is not None:
            if "last_second_profile" in json_dict:
                last_second_profile = json_dict["last_second_profile"]
    if file is not None:
        file.close()
    return last_second_profile


def get_profiles():
    profile_list = []
    file = open_score_file()
    if file is not None:
        json_dict: dict = get_JSON(file)
        if json_dict is not None:
            if "profiles" in json_dict:
                if type(json_dict["profiles"]) == list:
                    for i in range(len(json_dict["profiles"])):
                        if "name" in json_dict["profiles"][i]:
                            profile_list.append(json_dict["profiles"][i]["name"])
    if file is not None:
        file.close()
    return profile_list


def get_score(profile: str, gamemode: int):
    score = -1
    file = open_score_file()
    if file is not None:
        json_dict: dict = get_JSON(file)
        file.close()
        if json_dict is not None:
            if "profiles" in json_dict:
                if type(json_dict["profiles"]) == list:
                    for i in range(len(json_dict["profiles"])):
                        if "name" in json_dict["profiles"][i] and json_dict["profiles"][i]["name"] == profile and "scores" in json_dict["profiles"][i] and type(json_dict["profiles"][i]["scores"]) == list:
                            score = json_dict["profiles"][i]["scores"][gamemode]
    return score


def append_profile(profile: str, gamemode, score):
    file = open_score_file()
    json_dict = get_JSON(file)
    file.close()
    if "profiles" in json_dict:
        if type(json_dict["profiles"]) == list:
            scores = [-1, -1, -1]
            scores[gamemode] = score
            json_dict["profiles"].append({"name": profile, "scores": scores})
            write_to_file(json_dict)


def add_score(profile: str, gamemode, score):
    file = open_score_file()
    json_dict = get_JSON(file)
    file.close()
    if "profiles" in json_dict:
        if type(json_dict["profiles"]) == list:
            profile_found = False
            for i in range(len(json_dict["profiles"])):
                if "name" in json_dict["profiles"][i] and json_dict["profiles"][i]["name"] == profile:
                    profile_found = True
                    json_dict["profiles"][i]["scores"][gamemode] = score
                    write_to_file(json_dict)
                    break
            if not profile_found:
                append_profile(profile, gamemode, score)
    else:
        create_score_file()
        append_profile(profile, gamemode, score)
