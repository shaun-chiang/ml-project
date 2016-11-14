# Title: main.py
# Authors: Shaun, Junsheng, Samuel
# Description: Uses python 3. TODO: more detail
#

# imports
import os

# CHANGE THIS TO FIT YOUR PC
SG_folder = "D:\My Stuff\Downloads\SG\SG"
CN_folder = "D:\My Stuff\Downloads\CN(1)\CN"
ES_folder = "D:\My Stuff\Downloads\ES\ES"
EN_folder = "D:\My Stuff\Downloads\EN\EN"

def get_index(x, list_of_x):
    # gets the index of x from list
    i=0
    for name in list_of_x:
        if x == name:
            return i
        i+=1


def increment_label(line, array, list_of_x):
    index = get_index(line[0].lower(), list_of_x)
    # labels in this order: O, I-positive, B-positive, I-neutral, B-neutral, I-negative, B-negative
    if line[1] == "O":
        array[0][index]+=1
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


def parse_training_data(folder_path):
    # parses in the training file, returns 2d int array, list of x
    list_of_x = []
    array = [[],[],[],[],[],[],[]]
    with open(os.path.join(folder_path, "train"), 'r', encoding="utf8") as infile:
        for line in infile:
            if line.strip() != "":
                proc_line= line.strip().split(" ")
                x = proc_line[0].lower()
                if x not in list_of_x:
                    list_of_x.append(x)
                    for label in array:
                        label.append(0)
                increment_label(proc_line,array,list_of_x)

    return list_of_x, array


SG_X, SG_2d = parse_training_data(SG_folder)
# parse_training_data(CN_folder)
# parse_training_data(ES_folder)
# parse_training_data(EN_folder)

print(SG_X)
for row in SG_2d:
    print(row)