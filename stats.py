
import requests
import re
import collections
from bs4 import BeautifulSoup
from sys import argv
from string import ascii_uppercase
from operator import itemgetter


def letter_distribution(text):
    letter_occurences = []
    text = text.upper()
    letter_catalog = list(ascii_uppercase)
    all_letters = str(''.join(re.findall('[a-zA-Z]', text)))

    # highest count
    max_letter = collections.Counter(all_letters).most_common(1)[0][0]

    total_letters = len(all_letters)

    print 'Total letters: {0}'.format(total_letters)
    print 'Most common letter: {0}'.format(max_letter)
    print

    for letter in letter_catalog:
        letter_count = text.count(letter)
        letter_occurences.append(letter_count)
        letter_percentage = (float(letter_count) / total_letters) * 100
        print '{0} - {1:>5} ({2:>5.2f}%): {3}'.format(
            letter, letter_count, letter_percentage, '=' * int(letter_percentage) * 10)

    combined_list = zip(letter_catalog, letter_occurences)  # list of tuples with (letter, occurences) for the sake of sorting and saving

    print
    print 'Sorted: '
    print

    for k, v in sorted(combined_list, key=itemgetter(1), reverse=True):
        letter_percentage = (float(v) / total_letters) * 100
        print '{0} - {1:>5} ({2:>5.2f}%): {3}'.format(
            k, v, letter_percentage, '=' * int(letter_percentage) * 10)

    return combined_list


def main(url_list):
    cumulative_values = []

    for url in url_list:
        if not url.startswith('http'):
            url = 'http://' + url

        r = requests.get(url, headers={'User-agent': 'Mozilla'})
        soup = BeautifulSoup(r.text, 'html.parser')
        [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
        visible_text = soup.getText()

        #print 'VERBOSE: {}\n\nEND VERBOSE'.format(visible_text.encode('ascii', 'ignore'))
        print 'Source: {0}'.format(url)
        cumulative_values.append(letter_distribution(visible_text))

    #TODO: take the cumulative results and graph a histogram of avergae of placement by source
    # E - 1 (80%): ========
    # T - 2 (70%): =======
    # ...


if __name__ == '__main__':
    main(argv[1:])
