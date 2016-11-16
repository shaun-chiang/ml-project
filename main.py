# Title: main.py
# Authors: Shaun, Junsheng, Samuel
# Description: Uses python 3. TODO: more detail
# NOTE: PLEASE REFORMAT CODE (CTRL+ALT+L) BEFORE PUSHING

# imports
import os

SG_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/SG")
CN_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/CN")
ES_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/ES")
EN_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/EN")


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


def parse_labeled_data(folder_path, filename):
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


def compute_sum_list(data_2d):
    sum_list = []
    for row in data_2d:
        sum = 0
        for n in row:
            sum += n
        sum_list.append(sum)
    return sum_list


def emission(folder_path, filename_input_x, training_x_list, data_2d):
    testing_x_list = []
    count_y = compute_sum_list(data_2d)
    with open(os.path.join(folder_path, filename_input_x), 'r', encoding="utf8") as infile:
        for line in infile:
            x = line.strip()
            if x != "":
                if x not in testing_x_list:
                    testing_x_list.append(x)
    d = dict()
    for testing_x in testing_x_list:
        if testing_x not in training_x_list:
            d[testing_x] = [1 / (count_y[0] + 1), 1 / (count_y[1] + 1), 1 / (count_y[2] + 1), 1 / (count_y[3] + 1),
                            1 / (count_y[4] + 1), 1 / (count_y[5] + 1), 1 / (count_y[6] + 1)]
        else:
            training_index = get_index(testing_x, training_x_list)
            d[testing_x] = [data_2d[0][training_index] / (count_y[0] + 1),
                            data_2d[1][training_index] / (count_y[1] + 1),
                            data_2d[2][training_index] / (count_y[2] + 1),
                            data_2d[3][training_index] / (count_y[3] + 1),
                            data_2d[4][training_index] / (count_y[4] + 1),
                            data_2d[5][training_index] / (count_y[5] + 1),
                            data_2d[6][training_index] / (count_y[6] + 1)]
    return testing_x_list, d


# We parse in the training data
SG_X, SG_2d = parse_labeled_data(SG_folder, "train")
# CN_X, CN_2d = parse_labeled_data(CN_folder, "train")
# ES_X, ES_2d = parse_labeled_data(ES_folder, "train")
# EN_X, EN_2d = parse_labeled_data(EN_folder, "train")

print(SG_X)
for row in SG_2d:
    print(row)
SG_testing_x_list, emission_array = (emission(SG_folder, "dev.in", SG_X, SG_2d))
with open("dev.p2.out", 'w') as outfile:
    for key in emission_array:
        outfile.write(key + " : " + str(emission_array[key])+ "\n")
