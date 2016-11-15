# Title: main.py
# Authors: Shaun, Junsheng, Samuel
# Description: Uses python 3. TODO: more detail
# NOTE: PLEASE REFORMAT CODE (CTRL+ALT+L) BEFORE PUSHING

# imports
import os

# CHANGE THIS TO FIT YOUR PC
SG_folder = "D:\My Stuff\Downloads\SG\SG"
CN_folder = "D:\My Stuff\Downloads\CN(1)\CN"
ES_folder = "D:\My Stuff\Downloads\ES\ES"
EN_folder = "D:\My Stuff\Downloads\EN\EN"


def get_index(x, list_of_x):
    """
    Function to get the index of x (str) from list of x (list).
    :param x:
    :param list_of_x:
    :return: index (int)
    """
    for index, name in enumerate(list_of_x):
        if x == name:
            return index


def increment_label(line, array, list_of_x):
    """
    Given a line from the file (list of x and y), increments array (list) given index in list_of_x (list).
    Labels in this order (0-6): O, I-positive, B-positive, I-neutral, B-neutral, I-negative, B-negative
    :param line:
    :param array:
    :param list_of_x:
    """
    index = get_index(line[0], list_of_x)
    if line[1] == "O":
        array[0][index] += 1
    elif line[1] == "I-positive":
        array[1][index] += 1
    elif line[1] == "B-positive":
        array[2][index] += 1
    elif line[1] == "I-neutral":
        array[3][index] += 1
    elif line[1] == "B-neutral":
        array[4][index] += 1
    elif line[1] == "I-negative":
        array[5][index] += 1
    elif line[1] == "B-negative":
        array[6][index] += 1


def parse_data(folder_path, filename):
    """
    Parses in the training file, returns 2d int array, list of x.
    Requires filename (str) to be in the folder_path (str) stated.
    :param filename:
    :param folder_path:
    :return: 2d int array, list_of_x
    """
    list_of_x = []
    array = [[], [], [], [], [], [], []]
    with open(os.path.join(folder_path, filename), 'r', encoding="utf8") as infile:
        for line in infile:
            if line.strip() != "":
                proc_line = line.strip().split(" ")
                x = proc_line[0]
                if x not in list_of_x:
                    list_of_x.append(x)
                    for label in array:
                        label.append(0)
                increment_label(proc_line, array, list_of_x)
    return list_of_x, array


# We parse in the training data
SG_X, SG_2d = parse_data(SG_folder, "train")
# CN_X, CN_2d = parse_data(CN_folder, "train")
# ES_X, ES_2d = parse_data(ES_folder, "train")
# EN_X, EN_2d = parse_data(EN_folder, "train")

print(SG_X)
for row in SG_2d:
    print(row)
