"""
simple reader of HTML tables scraped from https://polskawliczbach.pl
"""

import os
from bs4 import BeautifulSoup

folder_path = ''

filter_words = ['leśna']

def get_html_files(folder_path):
    return [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.html')]

place_names = []

for file_path in get_html_files(folder_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    table_rows = soup.find_all('tr')
    
    for row in table_rows:
        place_name = row.find('a').text.strip()

        if os.path.basename(file_path) != 'miasta.html':
            place_name = ' '.join(place_name.split()[1:])
            
        if not any(word in place_name for word in filter_words):
            place_names.append(place_name)

place_names = list(set(place_names))
place_names.sort()

with open('miejscowosci.txt', 'w', encoding='utf-8') as output_file:
    for name in place_names:
        output_file.write(name + '\n')

def analyze_and_write_results(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    total_instances = len(lines)
    one_word_count = 0
    two_word_count = 0
    three_or_more_word_count = 0
    hyphenated_count = 0

    one_word_names = []
    two_word_names = []
    three_or_more_word_names = []
    hyphenated_names = []

    for line in lines:
        location_name = line.strip()
        words = location_name.split()
        word_count = len(words)

        if word_count == 1 and '-' not in location_name:
            one_word_count += 1
            one_word_names.append(location_name)
        elif word_count == 2 and '-' not in location_name:
            two_word_count += 1
            two_word_names.append(location_name)
        elif word_count >= 3 and '-' not in location_name:
            three_or_more_word_count += 1
            three_or_more_word_names.append(location_name)

        if '-' in location_name:
            hyphenated_count += 1
            hyphenated_names.append(location_name)

    def calculate_percentage(count):
        return (count / total_instances) * 100

    with open('miejscowosci_sorted.txt', 'w', encoding='utf-8') as result_file:
        result_file.write(f"One-word location names: {one_word_count} / {total_instances}, {calculate_percentage(one_word_count):.2f}%\n")
        print(f"One-word location names: {one_word_count} / {total_instances}, {calculate_percentage(one_word_count):.2f}%")
        for name in sorted(one_word_names):
            result_file.write(name + "\n")

        result_file.write(f"\nTwo-word location names: {two_word_count} / {total_instances}, {calculate_percentage(two_word_count):.2f}%\n")
        print(f"Two-word location names: {two_word_count} / {total_instances}, {calculate_percentage(two_word_count):.2f}%")
        for name in sorted(two_word_names):
            result_file.write(name + "\n")

        result_file.write(f"\nThree-or-more-word location names: {three_or_more_word_count} / {total_instances}, {calculate_percentage(three_or_more_word_count):.2f}%\n")
        print(f"Three-or-more-word location names: {three_or_more_word_count} / {total_instances}, {calculate_percentage(three_or_more_word_count):.2f}%")
        for name in sorted(three_or_more_word_names):
            result_file.write(name + "\n")

        result_file.write(f"\nHyphenated location names: {hyphenated_count} / {total_instances}, {calculate_percentage(hyphenated_count):.2f}%\n")
        print(f"Hyphenated location names: {hyphenated_count} / {total_instances}, {calculate_percentage(hyphenated_count):.2f}%")
        for name in sorted(hyphenated_names):
            result_file.write(name + "\n")

analyze_and_write_results('\miejscowosci.txt')