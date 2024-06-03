"""Clean the TXT file.

Remove unnecessary strings and strip margins - left,
top and bottom margins.
"""

import os.path
import re

from utils.constants import (
    PAGE_BREAK,
    WORDLIST_CLEANED_TXT_PATH,
    WORDLIST_TXT_PATH,
)
from utils.logger import logger

if not os.path.exists(WORDLIST_TXT_PATH):
    logger.error(
        'Wordlist TXT file not found. Did you run "00_convert_pdf_to_txt.py"?'
    )
    logger.error(f'{WORDLIST_TXT_PATH} does not exist')
    raise SystemExit('Aborting')

with open(WORDLIST_TXT_PATH, 'r', encoding='utf-8') as file:
    txt_lines = file.readlines()

# Lines containing the following can be removed:
#   - 'd+ WORTLISTE'
#   - 'WORTLISTE d+'
#   - 'VS_03'
#   - 'ZERTIFIKAT B1'
page_num_before_pattern = re.compile(r'\s+\d+\s+WORTLISTE')
page_num_after_pattern = re.compile(r'\s+WORTLISTE\s+\d+')
vs_03 = 'VS_03'
zertifikat_b1 = 'ZERTIFIKAT B1'

# Holds final result. Will be saved to a file.
cleaned_lines = []

# Do the actual cleaning.
for line in txt_lines:
    # All page break lines have text on them, strip it.
    if line.startswith(PAGE_BREAK):
        cleaned_lines.append(PAGE_BREAK)
        continue

    # Remove the following lines.
    if (
        page_num_before_pattern.search(line)
        or page_num_after_pattern.search(line)
        or vs_03 in line
        or zertifikat_b1 in line
    ):
        continue

    # All left margins are 8 whitespaces, strip them.
    if len(line) > 8:
        line = line[8:]

    cleaned_lines.append(line)

# Convert to string, so we can use Regex to strip out top and bottom margins.
# Also strip leading and trailing newlines, it's safe to do so.
cleaned_contents = ''.join(cleaned_lines).strip()

# Remove top margins (all newlines after a page break except one).
cleaned_contents = re.sub(
    rf'{PAGE_BREAK}\n+', rf'{PAGE_BREAK}\n', cleaned_contents
)

# Remove bottom margins (all newlines before a page break except one).
cleaned_contents = re.sub(
    rf'\n+{PAGE_BREAK}', rf'\n{PAGE_BREAK}', cleaned_contents
)

with open(WORDLIST_CLEANED_TXT_PATH, 'w', encoding='utf-8') as file:
    file.write(cleaned_contents)

logger.info('Successfully cleaned TXT')
logger.info(f'Saved cleaned TXT wordlist at {WORDLIST_CLEANED_TXT_PATH}')
