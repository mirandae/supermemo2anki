#!/usr/bin/python

import os, re, sys, time

DEFAULT_NUM_ARGS = 2

FILES_TO_IGNORE = [".DS_Store"]

USAGE = "Usage: supermemo2anki path/to/bkup_folder"
CLOZE_PATTERN = '.*(?<=<SPAN class=clozed>)(.*)(<\/SPAN>).*'
TAG_STRIPPER_PATTERN = '<[^<]+?>'
ANKI_BACKUPS = 'anki_cards_{}.txt'


def process_folder(foldername):
    regex = re.compile(CLOZE_PATTERN)
    cards = []
    for root, directories, filenames in os.walk(foldername):
        for file in filenames:
            if file not in FILES_TO_IGNORE:
                cards.extend(extract_cloze_card(os.path.join(root, file), regex))

    # identify out with current time
    out_filename = ANKI_BACKUPS.format(int(round(time.time() * 1000)))
    # remove cards that have already been backed up
    cards = delete_imported_cards(cards)
    if len(cards) != 0:
        export_cards(out_filename, cards)
    print "Processed {} cards!".format(len(cards))

def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]

def delete_imported_cards(cards):
    anki_backups = ANKI_BACKUPS.format('.*')
    regex = re.compile(anki_backups)
    for root, directories, filenames in os.walk(os.getcwd()):
        for file in filenames:
            if regex.match(file) is not None:
                with open(file) as f:
                    content = f.readlines()
                    # print content
                    cards = diff(cards, content)
    return cards


def export_cards(output_name, cards):
    file = open(output_name, 'w')
    for card in cards:
        file.write(card)
    file.close()

def remove_html_tags(string):
    return re.sub(TAG_STRIPPER_PATTERN, '', string)

def extract_cloze_card(filename, regex):
    cards = []
    with open(filename) as f:
        content = f.readlines()
        content = [x.strip() for x in content]
        for line in content:
            if regex.match(line) is not None:
                replacement_word = remove_html_tags(re.search(CLOZE_PATTERN, line).group(1))
                subbed =  remove_html_tags(re.sub(re.search(CLOZE_PATTERN, line).group(1), '{{c1::' + replacement_word + '}} ', line)) + '\n'
                cards.append(subbed)
    return cards

def main():
    if len(sys.argv) is not DEFAULT_NUM_ARGS:
        print(USAGE)
        exit(1)

    base_folder = sys.argv[1]
    process_folder(base_folder+"/elements")


if __name__ == '__main__':
    main()
