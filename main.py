# Title: main.py
# Authors: Shaun, Junsheng, Samuel
# Description: Uses python 3. TODO: more detail
# NOTE: PLEASE REFORMAT CODE (CTRL+ALT+L) BEFORE PUSHING

# imports
import os
import collections

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


def convert_label(label):
    """
    Converts labels from str to int form, or vice versa.
    Labels in this order (0-6): O, I-positive, B-positive, I-neutral, B-neutral, I-negative, B-negative
    :param label:
    :return:
    """
    if type(label) is str:
        if label == "O":
            return 0
        elif label == "I-positive":
            return 1
        elif label == "B-positive":
            return 2
        elif label == "I-neutral":
            return 3
        elif label == "B-neutral":
            return 4
        elif label == "I-negative":
            return 5
        elif label == "B-negative":
            return 6
    else:
        if label == 0:
            return "O"
        elif label == 1:
            return "I-positive"
        elif label == 2:
            return "B-positive"
        elif label == 3:
            return "I-neutral"
        elif label == 4:
            return "B-neutral"
        elif label == 5:
            return "I-negative"
        elif label == 6:
            return "B-negative"


def increment_label(line, array, list_of_x):
    """
    Given a line from the file (list of x and y), increments array (list) given index in list_of_x (list).
    Labels in this order (0-6): O, I-positive, B-positive, I-neutral, B-neutral, I-negative, B-negative
    :param line:
    :param array:
    :param list_of_x:
    """
    index = get_index(line[0], list_of_x)
    array[convert_label(line[1])][index] += 1


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


def emission(file_path_input_x, training_x_list, data_2d):
    """
    Given filepath of input (string), along with training_x_list (list of x) and data_2d (2d int array), return testing_x_list (list of x in testing set) and d (ordereddictionary of word and 7 label emission parameters).
    Labels in this order (0-6): O, I-positive, B-positive, I-neutral, B-neutral, I-negative, B-negative.
    :param filename_input_x:
    :param training_x_list:
    :param data_2d:
    :return: testing_x_list (list), d (OrderedDict)
    """
    testing_x_list = []
    count_y = compute_sum_list(data_2d)
    with open(file_path_input_x, 'r', encoding="utf8") as infile:
        for line in infile:
            x = line.strip()
            if x != "":
                if x not in testing_x_list:
                    testing_x_list.append(x)
    d = collections.OrderedDict()
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


def parse_entities(tagged_file):
    """
    Given a tagged file (filepath), produce entity_dict (dict).
    Entities are explained in the 2nd page of the project document.
    :param tagged_file:
    :return: entity_dict (dict)
    """
    within_entity = False
    entity_dict = dict()
    current_index = -1
    with open(tagged_file, 'r', encoding="utf8") as infile:
        for index, line in enumerate(infile):
            if line.strip() != "":
                proc_line = line.strip().split(" ")
                if proc_line[1] == "O" and within_entity:
                    within_entity = False
                elif proc_line[1].startswith("B") and not within_entity:
                    within_entity = True
                    current_index = index
                    entity_dict[current_index] = [proc_line[1]]
                elif proc_line[1].startswith("I") and not within_entity:
                    current_index = index
                    entity_dict[current_index] = [proc_line[1]]
                elif proc_line[1] != "O" and within_entity:
                    entity_dict[current_index].append(proc_line[1])
    return entity_dict


def part2(folder_name):
    """
    Given the relevant foldername, with dev.in, dev.out, and train;
    1. parses in and trains on "train" file
    2. generates emission parameters using dev.in
    3. writes predicted labels into dev.p2.out
    4. parse entities of dev.out and dev.p2.out
    5. compares the two to get number of correctly predicted entities
    6. calculates and prints Precision, Recall, F Score.
    :param folder_name:
    """
    print("Parsing in data of {0}".format(folder_name))
    p2_X, p2_2d = parse_labeled_data(folder_name, "train")

    print("Generate emission parameters using dev.in")
    p2_testing_x_list, emission_array = (emission(os.path.join(folder_name, "dev.in"), p2_X, p2_2d))

    print("Write predicted labels into dev.p2.out")
    with open(os.path.join(folder_name, "dev.p2.out"), 'w', encoding="utf8") as outfile:
        for key in emission_array:
            outfile.write(key + " " + convert_label(emission_array[key].index(max(emission_array[key]))) + "\n")

    print("Parse entities of dev.out and dev.p2.out")
    dev_entity_dict = parse_entities(os.path.join(folder_name, "dev.out"))
    dev_p2_entity_dict = parse_entities(os.path.join(folder_name, "dev.p2.out"))

    print("Comparing entities..")
    correctly_predicted = 0
    for key in dev_entity_dict:
        if key in dev_p2_entity_dict:
            if dev_entity_dict[key] == dev_p2_entity_dict[key]:
                correctly_predicted += 1
    precision = correctly_predicted / len(dev_p2_entity_dict)
    recall = correctly_predicted / len(dev_entity_dict)

    print("Precision: {0}".format(precision))
    print("Recall: {0}".format(recall))
    try:
        print("F-Score: {0}".format(2 / ((1 / precision) + (1 / recall))))
    except:
        print("Your precision and recall seem to be zero. Check for errors.")


part2(SG_folder)
part2(EN_folder)
part2(CN_folder)
part2(ES_folder)
