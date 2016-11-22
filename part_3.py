import os
import collections

SG_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/SG")
CN_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/CN")
ES_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/ES")
EN_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/EN")

def parse_labeled_data_labels(folder_path, filename):
    """
    Parses in the training file, returns 2d int array.
    Requires filename (str) to be in the folder_path (str) stated.
    :param filename:
    :param folder_path:
    :return: 2d int array
    """

    # Rows(next label): O, I-positive, B-positive, I-neutral, B-neutral, I-negative, B-negative, End
    # Columns(previous label): O, I-positive, B-positive, I-neutral, B-neutral, I-negative, B-negative, Start
    array = [[0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0]]
    previous = "Start"
    with open(os.path.join(folder_path, filename), 'r', encoding="utf8") as infile:
        for line in infile:
            if line.strip() != "":
                proc_line = line.strip().split(" ")
                current = proc_line[1]
                increment_label(previous, array, current)
                previous = current
            else:
                current = "End"
                increment_label(previous, array, current)
                previous = "Start"
    return array

def increment_label(previous, array, current):
    """
    Given a line from the file (list of x and y), increments array (list) given previous and current label.
    Labels in this order (0-7): O, I-positive, B-positive, I-neutral, B-neutral, I-negative, B-negative, Start/End
    :param current:
    :param previous:
    :param array:
    """
    current_index = get_index(current)
    previous_index = get_index(previous)
    array[current_index][previous_index] += 1

def get_index(label):
    """
    Function to get the index of label.
    :param label:
    :return: index (int)
    """
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
    elif label == "Start":
        return 7
    elif label == "End":
        return 7

def compute_sum_list(data_2d):
    sum_list = []
    for row in data_2d:
        sum = 0
        for n in row:
            sum += n
        sum_list.append(sum)
    return sum_list

def transmission(file_path_input_x, data_2d):
    """
    Given filepath of input (string) and data_2d (2d int array), return d (dictionary of initial label and the count of the resulting labels).
    Labels in this order (0-7): O, I-positive, B-positive, I-neutral, B-neutral, I-negative, B-negative, Start/End.
    :param filename_input_x:
    :param data_2d:
    :return: d (OrderedDict)
    """
    count_y = compute_sum_list(data_2d)
    d = collections.OrderedDict()
    for a in range(0,8):
        if a == 0:
            initial = "O"
        elif a == 1:
            initial = "I-positive"
        elif a == 2:
            initial = "B-positive"
        elif a == 3:
            initial = "I-neutral"
        elif a == 4:
            initial = "B-neutral"
        elif a == 5:
            initial = "I-negative"
        elif a == 6:
            initial = "B-negative"
        elif a == 7:
            initial = "Start"
        d[initial] = [data_2d[a][0] / count_y[a],
                      data_2d[a][1] / count_y[a],
                      data_2d[a][2] / count_y[a],
                      data_2d[a][3] / count_y[a],
                      data_2d[a][4] / count_y[a],
                      data_2d[a][5] / count_y[a],
                      data_2d[a][6] / count_y[a],
                      data_2d[a][7] / count_y[a]]
    return d

def test(folder_name):
    print("Parsing in data of {0}".format(folder_name))
    p2_2d = parse_labeled_data_labels(folder_name, "train")

    print("Generate transmission parameters using dev.in")
    transmission_array = (transmission(os.path.join(folder_name, "dev.in"), p2_2d))

    for n in p2_2d:
        print(n)

    print(transmission_array)

test(SG_folder)