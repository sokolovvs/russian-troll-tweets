import csv
import os
import re
import unicodedata
from _csv import reader
from typing import Tuple, List

from nltk.corpus import stopwords

http_pattern = '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'
tag_pattern = '(?:(?<=\s)|^)#(\w*[A-Za-z_]+\w*)'


def iterate_data(path):
    total_data = 0
    total_en_ru = 0
    total_en = 0
    total_ru = 0

    for filename in os.listdir(path):
        if filename.endswith(".csv"):
            with open(path + "/" + filename, 'r') as read_obj:
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    total_data += 1

                    content = row[2]
                    language = row[4]
                    pured_content = pure_content(content)

                    if language == 'English' or language == 'Russian':
                        pured_content = clean_stop_words(pured_content)

                        hasTags, hashtags = extract_hashtags(pured_content)

                        if hasTags:
                            print_row(content, language, pured_content, hashtags)

                            if language == 'English' or language == 'Russian':

                                total_en_ru += 1

                                with open("./data/after/en_ru.csv", mode='a+') as writer:
                                    csv_writer = csv.writer(writer, delimiter=',', quotechar='"',
                                                            quoting=csv.QUOTE_MINIMAL)

                                    csv_writer.writerow([pured_content, hashtags, language])

                                if language == 'English':
                                    total_en += 1

                                    with open("./data/after/en.csv", mode='a+') as writer:
                                        csv_writer = csv.writer(writer, delimiter=',', quotechar='"',
                                                                quoting=csv.QUOTE_MINIMAL)

                                        csv_writer.writerow([pured_content, hashtags, language])

                                if language == 'Russian':
                                    total_ru += 1

                                    with open("./data/after/ru.csv", mode='a+') as writer:
                                        csv_writer = csv.writer(writer, delimiter=',', quotechar='"',
                                                                quoting=csv.QUOTE_MINIMAL)

                                        csv_writer.writerow([pured_content, hashtags, language])

    print_total(total_data, total_en_ru, total_en, total_ru)


def unicode_to_ascii(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def pure_content(content: str) -> str:
    content = content.lower().strip()
    content = re.sub(http_pattern, '', content)
    content = unicode_to_ascii(content)
    content = re.sub(r"([@\'\",.`:;\^\?\.\+\-!,¿%$&*~|\\])", '', content)
    content = re.sub(r'@\w+', '', content)
    content = re.sub(r'@\d+', '', content)

    return content


def clean_stop_words(content: str) -> str:
    stopwords_list = stopwords.words(['english', 'russian'])
    words = content.split()
    clean_words = [word for word in words if (word not in stopwords_list) and len(word) > 2]
    return " ".join(clean_words)


def extract_hashtags(content: str) -> Tuple[bool, List[str]]:
    tags = re.findall(tag_pattern, content)

    return len(tags) != 0, re.findall(tag_pattern, content)


def print_row(content: str, language: str, pured_content: str, hashtags: List[str]) -> None:
    print("Content: {0} \nLanguage: {1} \nPured_content: {2} \nHashtags: {3} \n\n".format(content,
                                                                                          language,
                                                                                          pured_content,
                                                                                          hashtags)
          )


def print_total(total_data, total_en_ru, total_en, total_ru) -> None:
    print("Total tweets: {0} \nTotal selected EN_RU: {1} \nTotal selected EN: {2} \nTotal selected RU: {3}".format(
        total_data, total_en_ru, total_en, total_ru))


if __name__ == "__main__":
    iterate_data(path="./data/before")
