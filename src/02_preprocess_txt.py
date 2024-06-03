"""Preprocess the cleaned TXT file.

Expand all the pages into a single-column super-long page.

Reason for preprocessing is to allow parsing of the file.
"""

import os.path
import re
from collections import Counter

from utils.constants import (
    PAGE_BREAK,
    WORDLIST_CLEANED_TXT_PATH,
    WORDLIST_PREPROCESSED_TXT_PATH,
)
from utils.logger import logger

if not os.path.exists(WORDLIST_CLEANED_TXT_PATH):
    logger.error(
        'Cleaned wordlist TXT file not found. Did you run "01_clean_txt.py"?'
    )
    logger.error(f'{WORDLIST_CLEANED_TXT_PATH} does not exist')
    raise SystemExit('Aborting')

with open(WORDLIST_CLEANED_TXT_PATH, 'r', encoding='utf-8') as file:
    contents = file.read()

pages = contents.split(f'\n{PAGE_BREAK}\n')

# Holds final result. Will be saved to a file.
preprocessed_lines = []

# Do the actual preprocessing.
for page in pages:
    lines = page.split('\n')

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

# Convert to string, so we can use Regex to reduce amount of newlines.
preprocessed_content = '\n'.join(preprocessed_lines).strip()

# Convert 3 or more newlines into 2 newlines.
preprocessed_content = re.sub(r'\n{3,}', '\n\n', preprocessed_content)

with open(WORDLIST_PREPROCESSED_TXT_PATH, 'w', encoding='utf-8') as file:
    file.write(preprocessed_content)

logger.info('Successfully preprocessed TXT')
logger.info(
    f'Saved preprocessed TXT wordlist at {WORDLIST_PREPROCESSED_TXT_PATH}'
)
