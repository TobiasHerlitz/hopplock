from pathlib import Path
import math
import re

def load_texts():
    x = Path("texts")
    texts = {}

    for path in x.iterdir():  # Iterating over filepaths in texts
        with open(path, 'r', encoding='utf-8') as file:  # Open and read file
            text = file.read()

        text = re.sub('[().,]', '', text).lower()  # Remove some non-text chars

        curr_dict = {}
        text_list = text.split(' ')
        for word in text_list:
            curr_dict[word] = text_list.count(word)

        texts[path._str.split('\\')[1]] = curr_dict

    collection = {}
    for i in texts:
        for j in texts[i]:
            if j in collection:
                collection[j][0] += texts[i][j]
            else:
                collection[j] = [texts[i][j], 0]

    doc_num = len(texts)
    for word in collection:
        for text in texts:
            if word in texts[text]:
                collection[word][1] += 1
        collection[word].append(math.log((doc_num/collection[word][1]), 10))



    return texts, collection


def binary_weighting(texts, filename):
    matches = {x: 0 for x in texts.keys()}
    for i in texts:
        for j in texts[filename]:
            if j in texts[i]:
                matches[i] += 1

    return matches


def tf_idf_weighting(texts, collection, filename):
    # tf definition used is raw count. Simply number of occurences
    # idf is the log of (number of docs / docs that contain term)
    matches = {x: 0 for x in texts.keys()}
    matches_words = {x: [] for x in texts.keys()}
    for i in texts:
        for j in texts[filename]:
            if j in texts[i]:
                matches[i] += texts[i][j] * collection[j][2]
                matches_words[i].append(j)

    return matches, matches_words


def print_result(answ_dict):
    my_list = [(k, v) for k, v in sorted(
        answ_dict.items(), key=lambda item: item[1])][::-1]
    print('MATCHES\t\tTEXT')
    [print(f'{i[1]}\t\t\t{i[0]}') for i in my_list]


def length_norm(text_dict):
    # square items -> sum -> square root
    text_sum = 0
    for i in text_dict:
        text_sum = text_dict[i] ** 2

    text_sum = text_sum ** 0.5

    return text_sum



texts, collection = load_texts()
res, matches_words = tf_idf_weighting(texts, collection, 'bananas.txt')
# [print(i) for i in collection.items()]
# print_result(res)

print_result(res)


for i in matches_words['parrots.txt']:
    print(i, round(collection[i][2], 2))