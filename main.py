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

#-----------------------------------------------------------------------------------------------------------------------
#------  Part II: Emission Parameters  ---------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------

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
            else:
                testing_x_list.append('BLANK')
    d = collections.OrderedDict()
    for index, testing_x in enumerate(testing_x_list):
        if testing_x == "BLANK":
            d["BLANK"+str(index)]=[]
        elif testing_x not in training_x_list:
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

#-----------------------------------------------------------------------------------------------------------------------
#------  Sub-methods  --------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------

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

def compute_sum_list(data_2d):
    sum_list = []
    for row in data_2d:
        sum = 0
        for n in row:
            sum += n
        sum_list.append(sum)
    return sum_list

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
                elif (proc_line[1].startswith("B") or proc_line[1].startswith("I")) and not within_entity:
                    within_entity = True
                    sentiment = proc_line[1].split("-")[1]
                    current_index = index
                    entity_dict[current_index] = [proc_line[1].split("-")[1]]
                elif proc_line[1].startswith("B") and within_entity:
                    sentiment = proc_line[1].split("-")[1]
                    current_index = index
                    entity_dict[current_index] = [proc_line[1].split("-")[1]]
                elif proc_line[1].startswith("I") and within_entity:
                    if sentiment == proc_line[1].split("-")[1]:
                        entity_dict[current_index].append(proc_line[1].split("-")[1])
                    else:
                        sentiment = proc_line[1].split("-")[1]
                        current_index = index
                        entity_dict[current_index] = [proc_line[1].split("-")[1]]
    return entity_dict

#-----------------------------------------------------------------------------------------------------------------------
#------  Part III: Transmission/Viterbi  -------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------

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
                increment_label_labels(previous, array, current)
                previous = current
            else:
                current = "End"
                increment_label_labels(previous, array, current)
                previous = "Start"
    return array

def transmission(data_2d):
    """
    Given filepath of input (string) and data_2d (2d int array), return d (dictionary of initial label and the count of the resulting labels).
    Labels in this order (0-7): O, I-positive, B-positive, I-neutral, B-neutral, I-negative, B-negative, Start/End.
    :param data_2d:
    :return: d (OrderedDict)
    """
    count_y = compute_sum_list(data_2d)
    d = collections.OrderedDict()
    for a in range(0, 8):
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

def viterbi(emission_array, transmission_array, file_path_input_x):
    """
    Given filepath of input, emission and transmission arrays, return a 3D array of number of sequences X number of words X number of labels
    and the sequence of labels.
    :param emission_array:
    :param transmission_array:
    :param file_path_input_x:
    :return:
    """
    input_array = []
    with open(file_path_input_x, 'r', encoding="utf8") as infile:
        sub_array = []
        for line in infile:
            x = line.strip()
            if x != "":
                sub_array.append(x)
            else:
                input_array.append(sub_array)
                sub_array = []

    score = []
    label_sequence = []
    for a in range(0, len(input_array)):
        sequence_score = []
        label_sequence_2 = ["Start"]
        sequence_labels = []
        for b in range(0, len(input_array[a])+1):
            word_score = []
            word_labels = []

            # Handles the very first word of the sequence. Appends "Start" as the beginning of the sequence and then
            # calculates the score for each label of layer i = 1, where score = transmission(start -> label) *
            # emission(label -> x).
            #
            # Appends the scores as an array of 7 scores for each label.

            if len(sequence_score) < 1:
                for label in range(0, 7):
                    transmission_score = transmission_array["Start"][label]
                    emission_score = emission_array[input_array[a][0]][label]
                    word_score.append(transmission_score * emission_score)
                    # word_score.append(emission_score)


            # Handles the very last word of the sequence. Calculates the end score and the label of layer i = n.
            # Calculates the score for each label where score = transmission(label -> end).
            #
            # Appends the scores as an array of 7 scores for each label.
            # Appends the label that gives the maximum score for layer i = n

            elif len(sequence_score) == len(input_array[a]):
                max = 0
                for prev_label in range(0, 7):

                    if prev_label == 0:
                        current = "O"
                    elif prev_label == 1:
                        current = "I-positive"
                    elif prev_label == 2:
                        current = "B-positive"
                    elif prev_label == 3:
                        current = "I-neutral"
                    elif prev_label == 4:
                        current = "B-neutral"
                    elif prev_label == 5:
                        current = "I-negative"
                    elif prev_label == 6:
                        current = "B-negative"

                    total_score = transmission_array[current][7] * sequence_score[b-1][prev_label]
                    if total_score > max:
                        max = total_score
                        max_label = current

                    word_score.append(transmission_score)
                word_labels.append(max_label)

            # Handles all other layers from i = 1 to n. Calculates 7 score per label in layer i. For example, at label
            # "O" at layer i, calculate 7 scores where score = transmission(label[i-1] -> label[i]) * score(label[i-1])
            # * emimission(label[i] -> x).
            #
            # Then take the maximum score of the 7 as well as the maximum corresponding
            # label of layer i-1 and stores it in the node of layer i.
            #
            # We then calculate the max of all the scores of layer i and append the corresponding maximum label of layer
            # i-1.

            else:
                for label in range(0, 7):
                    word_score_2 = []
                    for prev_label_index in range(0, 7):
                        prev_layer_max_trans = sequence_score[b - 1][prev_label_index]

                        if prev_label_index == 0:
                            prev_label = "O"
                        elif prev_label_index == 1:
                            prev_label = "I-positive"
                        elif prev_label_index == 2:
                            prev_label = "B-positive"
                        elif prev_label_index == 3:
                            prev_label = "I-neutral"
                        elif prev_label_index == 4:
                            prev_label = "B-neutral"
                        elif prev_label_index == 5:
                            prev_label = "I-negative"
                        elif prev_label_index == 6:
                            prev_label = "B-negative"

                        transmission_score = transmission_array[prev_label][label] * prev_layer_max_trans
                        emission_score = emission_array[input_array[a][b]][label]
                        word_score_2.append(transmission_score * emission_score)

                    max = 0
                    for index, c in enumerate(word_score_2):
                        if c > max:
                            max = c
                            if index == 0:
                                max_prev_2 = "O"
                            elif index == 1:
                                max_prev_2 = "I-positive"
                            elif index == 2:
                                max_prev_2 = "B-positive"
                            elif index == 3:
                                max_prev_2 = "I-neutral"
                            elif index == 4:
                                max_prev_2 = "B-neutral"
                            elif index == 5:
                                max_prev_2 = "I-negative"
                            elif index == 6:
                                max_prev_2 = "B-negative"
                    word_score.append(max)
                    word_labels.append(max_prev_2)

                # word_max = 0
                # for index, c in enumerate(word_score):
                #     if c > word_max:
                #         word_max = c
                #         max_index = index
                # label_sequence_2.append(max_prev_label[max_index])

            sequence_score.append(word_score)
            sequence_labels.append(word_labels)

        score.append(sequence_score)

        invert_sequence_labels = ["End"]
        for d in range(len(sequence_labels)-1):
            if d == 0:
                invert_sequence_labels.append(sequence_labels[len(sequence_labels)-(d+1)][0])
            else:
                if invert_sequence_labels[d] == "O":
                    invert_sequence_labels.append(sequence_labels[len(sequence_labels)-(d+1)][0])
                elif invert_sequence_labels[d] == "I-positive":
                    invert_sequence_labels.append(sequence_labels[len(sequence_labels)-(d+1)][1])
                elif invert_sequence_labels[d] == "B-positive":
                    invert_sequence_labels.append(sequence_labels[len(sequence_labels)-(d+1)][2])
                elif invert_sequence_labels[d] == "I-neutral":
                    invert_sequence_labels.append(sequence_labels[len(sequence_labels)-(d+1)][3])
                elif invert_sequence_labels[d] == "B-neutral":
                    invert_sequence_labels.append(sequence_labels[len(sequence_labels)-(d+1)][4])
                elif invert_sequence_labels[d] == "I-negative":
                    invert_sequence_labels.append(sequence_labels[len(sequence_labels)-(d+1)][5])
                elif invert_sequence_labels[d] == "B-negative":
                    invert_sequence_labels.append(sequence_labels[len(sequence_labels)-(d+1)][6])
        invert_sequence_labels.append("Start")

        for e in range(len(invert_sequence_labels)):
            label_sequence_2.append(invert_sequence_labels[len(invert_sequence_labels)-(d+1)])

        label_sequence_2.append("End")
        label_sequence.append(label_sequence_2)


    return score, label_sequence, input_array

#-----------------------------------------------------------------------------------------------------------------------
#------  Sub-methods  --------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------

def increment_label_labels(previous, array, current):
    """
    Given a line from the file (list of x and y), increments array (list) given previous and current label.
    Labels in this order (0-7): O, I-positive, B-positive, I-neutral, B-neutral, I-negative, B-negative, Start/End
    :param current:
    :param previous:
    :param array:
    """
    current_index = get_index_labels(current)
    previous_index = get_index_labels(previous)
    array[current_index][previous_index] += 1

def get_index_labels(label):
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

# -----------------------------------------------------------------------------------------------------------------------
# ------  Part IV: Top K Viterbi  -------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------

def TopKViterbi(emission_array, transmission_array, file_path_input_x, K):
    """
    Given filepath of input, emission and transmission arrays, return a 3D array of number of sequences X number of words X number of labels
    and the sequence of labels.
    :param emission_array:
    :param transmission_array:
    :param file_path_input_x:
    :param K:
    :return:
    """
    input_array = []
    with open(file_path_input_x, 'r', encoding="utf8") as infile:
        sub_array = []
        for line in infile:
            x = line.strip()
            if x != "":
                # it is a word, add it to sub_array
                sub_array.append(x)
            else:
                # it is a blank add the subarray to input array and empty subarray
                input_array.append(sub_array)
                sub_array = []

    # score contains sequencescores which contains
    score = []
    label_sequence = []
    #traversing though the 2d input array
    for a in range(0, len(input_array)):
        # TODO: initialize a 2d Score array with the inner array having length equal to K
        # TODO: initialize a 2d Sequence array with the inner array having length equal to K
        # Through 'a' we can access each sequence (input_array[a]), initialize a sequence_score and label_sequence_2
        sequence_score = []
        label_sequence_2 = []
        for b in range(0, len(input_array[a])+1):
            # Traversing through the sequence
            word_score = []

            # it is beginning of the sequence, add Start state
            if len(sequence_score) < 1:
                label_sequence_2.append("Start")
                for nextState in range(0, 7):
                    # transmission_array[u][v], u -> v
                    transmission_score = transmission_array["Start"][nextState]
                    # emission_array[emitted word][state], state -> word
                    emission_score = emission_array[input_array[a][0]][nextState]
                    word_score.append(transmission_score * emission_score)
                    # word_score.append(emission_score)

            # If Last word of the seq enters this if block, difference is that emission is not included in the score
            elif len(sequence_score) == len(input_array[a]):
                # TODO: find the top K scores computed from each state of the prev layer
                # prev_layer_max_trans is use to keep track of the maximum score of the previous layer
                prev_layer_max_trans = 0
                # iterate through the previous layer of scores
                for index, c in enumerate(sequence_score[b - 1]):
                    if c > prev_layer_max_trans:
                        prev_layer_max_trans = c
                        if index == 0:
                            current = "O"
                        elif index == 1:
                            current = "I-positive"
                        elif index == 2:
                            current = "B-positive"
                        elif index == 3:
                            current = "I-neutral"
                        elif index == 4:
                            current = "B-neutral"
                        elif index == 5:
                            current = "I-negative"
                        elif index == 6:
                            current = "B-negative"
                # transmission_array[current][7 = STOP]
                transmission_score = transmission_array[current][7] * prev_layer_max_trans
                word_score.append(transmission_score)
                # label_sequence_2.append(current)

            # If General Case enters this if block
            else:
                # TODO: find the top K scores computed from each state of the prev layer
                # prev_layer_max_trans is use to keep track of the maximum score of the previous layer
                prev_layer_max_trans = 0
                # iterate through the previous layer of scores
                for index, c in enumerate(sequence_score[b - 1]):
                    if c > prev_layer_max_trans:
                        prev_layer_max_trans = c
                        if index == 0:
                            current = "O"
                        elif index == 1:
                            current = "I-positive"
                        elif index == 2:
                            current = "B-positive"
                        elif index == 3:
                            current = "I-neutral"
                        elif index == 4:
                            current = "B-neutral"
                        elif index == 5:
                            current = "I-negative"
                        elif index == 6:
                            current = "B-negative"

                for nextState in range(0, 7):
                    transmission_score = transmission_array[current][nextState] * prev_layer_max_trans
                    emission_score = emission_array[input_array[a][b]][nextState]
                    word_score.append(transmission_score * emission_score)
                    # word_score.append(emission_score)
                label_sequence_2.append(current)

            # After exiting any of the conditional block, append the word score to the sequence_score
            sequence_score.append(word_score)
        label_sequence_2.append("End")
        score.append(sequence_score)
        label_sequence.append(label_sequence_2)
    return score, label_sequence, input_array

#-----------------------------------------------------------------------------------------------------------------------
#------  Main Function  ------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------

def main(folder_name):
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
    p3_2d = parse_labeled_data_labels(folder_name, "train")

    print("Generate emission and transmission parameters using dev.in")
    p2_testing_x_list, emission_array = (emission(os.path.join(folder_name, "dev.in"), p2_X, p2_2d))
    transmission_array = (transmission(p3_2d))

    print("Generating forward scores for Viterbi")

    # print(emission_array)
    # print("NEXT")
    # print(transmission_array)
    # print("NEXT")
    # print(os.path.join(folder_name, "dev.in"))

    score, sequence, original_array = viterbi(emission_array, transmission_array, os.path.join(folder_name, "dev.in"))

    print("Writing predicted labels")
    with open(os.path.join(folder_name, "dev.p2.out"), 'w', encoding="utf8") as outfile:
        for key in emission_array:
            if key.startswith("BLANK"):
                outfile.write("\n")
            else:
                outfile.write(key + " " + convert_label(emission_array[key].index(max(emission_array[key]))) + "\n")
    with open(os.path.join(folder_name, "dev.p3.out"), 'w', encoding="utf8") as outfile:
        for index_1 in range(0, len(original_array)):
            for index_2 in range(0, len(original_array[index_1])):
                outfile.write(original_array[index_1][index_2] + " " + sequence[index_1][index_2 + 1] + "\n")
            outfile.write("\n")
    #
    # print("Parse entities")
    # dev_entity_dict = parse_entities(os.path.join(folder_name, "dev.out"))
    # dev_p2_entity_dict = parse_entities(os.path.join(folder_name, "dev.p2.out"))
    # dev_p3_entity_dict = parse_entities(os.path.join(folder_name, "dev.p3.out"))
    #
    # print("Comparing entities..")
    # correctly_predicted_p2 = 0
    # for key in dev_entity_dict:
    #     if key in dev_p2_entity_dict:
    #         if dev_entity_dict[key] == dev_p2_entity_dict[key]:
    #             correctly_predicted_p2 += 1
    # precision_p2 = correctly_predicted_p2 / len(dev_p2_entity_dict)
    # recall_p2 = correctly_predicted_p2 / len(dev_entity_dict)
    #
    # correctly_predicted_p3 = 0
    # for key in dev_entity_dict:
    #     if key in dev_p3_entity_dict:
    #         if dev_entity_dict[key] == dev_p3_entity_dict[key]:
    #             correctly_predicted_p3 += 1
    # precision_p3 = correctly_predicted_p3 / len(dev_p3_entity_dict)
    # recall_p3 = correctly_predicted_p3 / len(dev_entity_dict)
    #
    # print("Precision: {0}".format(precision_p2))
    # print("Recall: {0}".format(recall_p2))
    # print("Precision: {0}".format(precision_p3))
    # print("Recall: {0}".format(recall_p3))
    # try:
    #     print("F-Score: {0}".format(2 / ((1 / precision_p2) + (1 / recall_p2))))
    #     print("F-Score: {0}".format(2 / ((1 / precision_p3) + (1 / recall_p3))))
    # except:
    #     print("Your precision and recall seem to be zero. Check for errors.")

# print(parse_entities("C:\\Users\\redbe\\OneDrive\\Documents\\ml-project\\testfile.out"))
# print(parse_entities("C:\\Users\\redbe\\OneDrive\\Documents\\ml-project\\testfile.gold.out"))

main(SG_folder)
main(EN_folder)
main(CN_folder)
main(ES_folder)
