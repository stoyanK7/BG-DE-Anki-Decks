"""Parse the TXT file - extract words ane examples in a CSV file."""

import os.path
import re
import sys

import pandas as pd
from utils.constants import PREPROCESSED_WORDLIST_TXT_PATH, WORDLIST_CSV_PATH
from utils.logger import logger

if not os.path.exists(PREPROCESSED_WORDLIST_TXT_PATH):
    logger.error(f'{PREPROCESSED_WORDLIST_TXT_PATH} not found')
    sys.exit()

with open(PREPROCESSED_WORDLIST_TXT_PATH, 'r') as file:
    lines: list[str] = file.readlines()

# Remove lines with single letters A B C D E F G ...
# as those mess with the parsing.F
letter_regex = r'^[A-Z]$'
for line in lines:
    if re.match(letter_regex, line.strip()):
        lines.remove(line)

current_word: str | None = None
current_example: str | None = None
# Hold the final result which will be exported to CSV.
words = []
examples = []
# Pattern matching ' 1. ' or ' 2. ' etc...
example_start_pattern = r'\s*(\s\s\d+\.\s).+'


def is_word_letter(char: str) -> bool:
    """Check whether the given character is a word letter.

    Words consist of alphanumeric characters, umlauts and a few special
    characters such as parentheses, dashes or arrows.
    """
    return char.isalpha() or char.lower() in [
        'ä',
        'ö',
        'ü',
        '→',
        '„',
        '–',
        '(',
        '/',
        '-',
        '&',
    ]


for line in lines:
    # If line is a newline and there is a current_word, save.
    # Another word almost always comes after a newline.
    is_newline = len(line.strip()) == 0
    if is_newline and current_word:
        words.append(current_word)
        examples.append(current_example)
        current_word = None
        current_example = None
        continue
    elif is_newline:
        continue

    # Else the line is longer. We have parsing to do...

    # '  1. ' always indicates a new word.
    if '  1. ' in line:
        # If there was a word previously, save it first.
        if current_word:
            words.append(current_word)
            examples.append(current_example)

        line_sections: list[str] = line.split('  1. ')
        # First section is word.
        current_word = line_sections[0].strip() + '\n'
        # Second section is example.
        current_example = '1. ' + line_sections[1].strip() + '\n'

    # If there is a ' 2. ' or ' 3. ', ... then we definitely have
    # a second/third/... example.
    elif re.search(example_start_pattern, line):
        search = re.search(example_start_pattern, line)
        example_start: str = search.group(1)
        # Get index of '  2. '
        idx_example_start: int = line.find(example_start)
        # Before the index is a word. There could be nothing, but we
        # append it anyway.
        word: str = line[:idx_example_start].strip() + '\n'
        # After the index is the example.
        example: str = line[idx_example_start - 1 :].strip() + '\n'

        # If there is a word, append to it, else append to last inserted word.
        # The latter are common cases where a word spans over multiple columns.
        if current_word and current_example:
            current_word += word
            current_example += example
        else:
            words[-1] += word
            examples[-1] += example

    # First char being a word letter and having a current_word could mean 3 things:
    #    1. Continuation of current_word and example.
    #    2. Just continuation of current_word.
    #    3. Just continuation of example.
    elif is_word_letter(line.lstrip()[0]) and current_word:
        # Reduce all 2 or more whitespaces to just 2, so we can split the line.
        line: str = re.sub(r'\s{2,}', '  ', line)
        line_sections: list[str] = line.split('  ')
        # Remove empty strings.
        line_sections = [x for x in line_sections if x]
        if len(line_sections) == 2:
            # We have a word and an example.
            current_word += line_sections[0].strip() + '\n'
            current_example += line_sections[1].strip() + '\n'
        elif len(line_sections) == 1:
            # It could be a word or an example. If first char of line is a
            # letter, then we consider it a word, otherwise an example.
            if is_word_letter(line[0]):
                current_word += line_sections[0].strip() + '\n'
            else:
                current_example += line_sections[0].strip() + '\n'
        else:
            # Anything other than 1 or 2 shouldn't happen.
            logger.error(f'Weird edge case at line "{line}"')
            sys.exit()

    # Same as above, however, this time it would be a new word/example or both.
    elif is_word_letter(line.lstrip()[0]) and not current_word:
        # Reduce all 2 or more whitespaces to just 2, so we can split the line.
        line: str = re.sub(r'\s{2,}', '  ', line)
        line_sections: list[str] = line.split('  ')
        # Remove empty strings.
        line_sections = [x for x in line_sections if x]
        if len(line_sections) == 2:
            # We have a word and an example.
            current_word = line_sections[0].strip() + '\n'
            current_example = line_sections[1].strip() + '\n'
        elif len(line_sections) == 1:
            # It could be a word or an example. If first char of line is a
            # letter, then we consider it a word, otherwise an example.
            if is_word_letter(line[0]):
                current_word = line_sections[0].strip() + '\n'
            else:
                current_example = line_sections[0].strip() + '\n'
        else:
            # Anything other than 1 or 2 shouldn't happen.
            logger.error(f'Weird edge case at line "{line}"')
            sys.exit()

    # Else we have something that isn't a word letter - most likely a digit.
    # Add it to example.
    else:
        line = line.strip()
        if current_example:
            current_example += line + '\n'
        else:
            # Usually a new page-column.
            examples[-1] += line + '\n'


df = pd.DataFrame({'word': words, 'example': examples})
logger.info(f'Parsed {df.shape[0]} words')

df.to_csv(WORDLIST_CSV_PATH, index=False)
logger.info(f'Saved raw CSV wordlist {WORDLIST_CSV_PATH}')
