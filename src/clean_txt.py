"""Clean the TXT file - remove useless strings and strip margins."""

import os.path
import re
import sys

from utils.constants import (
    CLEANED_WORDLIST_TXT_PATH,
    PAGE_BREAK,
    WORDLIST_TXT_PATH,
)
from utils.logger import logger

if not os.path.exists(WORDLIST_TXT_PATH):
    logger.error(f'{WORDLIST_TXT_PATH} not found')
    sys.exit()

with open(WORDLIST_TXT_PATH, 'r') as file:
    txt_lines: list[str] = file.readlines()

# Lines containing the following can be removed:
#   - 'd+ WORTLISTE'
#   - 'WORTLISTE d+'
#   - 'VS_03'
#   - 'ZERTIFIKAT B1'
page_num_before_pattern = re.compile(r'\s+\d+\s+WORTLISTE')
page_num_after_pattern = re.compile(r'\s+WORTLISTE\s+\d+')
vs_03 = 'VS_03'
zertifikat_b1 = 'ZERTIFIKAT B1'

# Holds final result which will be saved to a file for preprocessing later.
cleaned_lines = []

for line in txt_lines:
    # All page break lines have text after, this way we strip it.
    if line.startswith(PAGE_BREAK):
        cleaned_lines.append(PAGE_BREAK)
        continue
    if (
        page_num_before_pattern.search(line)
        or page_num_after_pattern.search(line)
        or vs_03 in line
        or zertifikat_b1 in line
    ):
        continue
    # All left margins are 8 whitespaces.
    if len(line) > 8:
        line = line[8:]
    cleaned_lines.append(line)

# Convert to string, so we can use Regex to strip out top and bottom margins.
# Also strip leading and trailing newlines, it's safe to do so.
cleaned_contents: str = ''.join(cleaned_lines).strip()
# Remove top margins - all newlines after a page break except first one.
cleaned_contents: str = re.sub(
    rf'{PAGE_BREAK}\n+', rf'{PAGE_BREAK}\n', cleaned_contents
)
# Remove bottom margins - all newlines before a page break except the last one.
cleaned_contents: str = re.sub(
    rf'\n+{PAGE_BREAK}', rf'\n{PAGE_BREAK}', cleaned_contents
)


with open(CLEANED_WORDLIST_TXT_PATH, 'w') as file:
    file.write(cleaned_contents)
    logger.info(f'Saved cleaned TXT at {CLEANED_WORDLIST_TXT_PATH}')
