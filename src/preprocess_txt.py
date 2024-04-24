"""Preprocess the TXT file - combine all pages in one long one-column file."""

import os.path
import re
import sys
from collections import Counter

from utils.constants import (
    CLEANED_WORDLIST_TXT_PATH,
    PAGE_BREAK,
    PREPROCESSED_WORDLIST_TXT_PATH,
)
from utils.logger import logger

if not os.path.exists(CLEANED_WORDLIST_TXT_PATH):
    logger.error(f'{CLEANED_WORDLIST_TXT_PATH} not found')
    sys.exit()

with open(CLEANED_WORDLIST_TXT_PATH, 'r') as file:
    contents: str = file.read()

pages: list[str] = contents.split(f'\n{PAGE_BREAK}\n')

# Holds final result which will be saved to a file for parsing later.
preprocessed_lines = []

for page in pages:
    lines: list[str] = page.split('\n')

    # Count occurrences of '  [A-Za-z]' in the middle of the page.
    # The most common index will correspond to the middle of the page.
    indices_occurrences = []
    for line in lines:
        # Skip lines shorter than 100 to avoid errors.
        if len(line) < 100:
            continue
        # All middles are somewhere between 68 and 88. This is an observation.
        for i in range(68, 88):
            if line[i - 1] == ' ' and line[i] == ' ' and line[i + 1].isalpha():
                indices_occurrences.append(i)

    # Find the most common index.
    counter = Counter(indices_occurrences)
    most_common_idx: tuple[int, int] = counter.most_common(1)[0]
    # First int is index, second is frequency.
    most_common_idx: int = most_common_idx[0]

    # Everything before most_common_idx is considered left column.
    # Everything after most_common_idx is considered right column.
    left_page_column_content = ''
    right_page_column_content = ''

    for line in lines:
        if len(line) >= most_common_idx:
            left_page_column_content += f'{line[:most_common_idx]}\n'
            # most_common_idx + 1 so we don't grab the space before the letter
            right_page_column_content += f'{line[most_common_idx + 1:]}\n'
        else:
            left_page_column_content += f'{line}\n'
            # Even though there is no content in right column, there is
            # a newline which will most-likely indicate a new word.
            right_page_column_content += '\n'

    preprocessed_lines.append(left_page_column_content)
    preprocessed_lines.append(right_page_column_content)

preprocessed_content: str = '\n'.join(preprocessed_lines).strip()
# Convert 3 or more newlines into 2 newlines.
preprocessed_content = re.sub(r'\n{3,}', '\n\n', preprocessed_content)

with open(PREPROCESSED_WORDLIST_TXT_PATH, 'w') as file:
    file.write(preprocessed_content)
    logger.info(f'Saved preprocessed TXT at {PREPROCESSED_WORDLIST_TXT_PATH}')
