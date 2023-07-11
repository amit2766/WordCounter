import re
import threading
from threading import Thread


def count_word_occurrences(file_path):
    try:
        with open(file_path, 'r') as file:
            contents = file.read()
            words = re.findall(r'\w+', contents.lower())

            word_count = {}
            lock = threading.Lock()

            def count_words(start, end):
                local_count = {}
                for i in range(start, end):
                    word = words[i]
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

            num_threads = 4  # Set the number of threads
            chunk_size = len(words) // num_threads
            threads = []

            for i in range(num_threads):
                start = i * chunk_size
                end = start + chunk_size if i < num_threads - 1 else len(words)
                thread = Thread(target=count_words, args=(start, end))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

            return word_count
    except FileNotFoundError:
        print("File not found.")
    except IOError:
        print("An error occurred while reading the file.")


# Example usage
file_path = 'gnu_license.txt'  # Replace with your file path
word_occurrences = count_word_occurrences(file_path)
for word, count in word_occurrences.items():
    print(word, count)
