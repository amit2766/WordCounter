import re
import threading
import timeit
from concurrent.futures import ThreadPoolExecutor
from threading import Thread


def count_words(line):
    local_count = {}
    words = re.findall(r'\w+', line.rstrip("\n").lower())
    for counter in range(words.__len__()):
        word = words[counter]
        if word in local_count:
            local_count[word] += 1
        else:
            local_count[word] = 1

    with lock:
        for word, count in local_count.items():
            if word in word_count:
                word_count[word] += count
            else:
                word_count[word] = count

def count_word_occurrences(file_path):
    executor = ThreadPoolExecutor(max_workers=4)
    try:
        with open(file_path, 'r') as file:
            for line in file:
                executor.submit(count_words,line)

        return word_count
    except FileNotFoundError:
        print("File not found.")
    except IOError:
        print("An error occurred while reading the file.")

file_path = 'gnu_license.txt'
word_count = {}
lock = threading.Lock()

word_occurrences = count_word_occurrences(file_path)
for word, count in word_occurrences.items():
    print(word, " : ", count)

