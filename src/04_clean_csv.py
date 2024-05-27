"""Clean the raw CSV file.

Strip whitespaces and newlines.
"""

import os

import pandas as pd
from utils.constants import CLEANED_WORDLIST_CSV_PATH, WORDLIST_CSV_PATH
from utils.logger import logger

if not os.path.exists(WORDLIST_CSV_PATH):
    logger.error('Wordlist CSV file not found. Did you run "03_parse_txt.py"?')
    logger.error(f'{WORDLIST_CSV_PATH} does not exist')
    raise SystemExit('Aborting')

df = pd.read_csv(WORDLIST_CSV_PATH)

# Ensure that there are no cells with null values.
null_count: int = df.isnull().sum().sum()
if null_count > 0:
    null_mask = df.isnull().any(axis=1)
    null_rows = df[null_mask]

    logger.error(f'Found {null_count} cells with null values')
    logger.error(
        'Cleaning/Preprocessing/Parsing of the TXT file must '
        'have gone wrong. Null rows are:'
        f'{null_rows}'
    )
    raise SystemExit('Aborting')

# Strip leading whitespaces and trailing newlines.
df['word'] = df['word'].str.strip()
df['examples'] = df['examples'].str.strip()

# Certain words are transferred over with a hyphen + newline. Undo that.
df['word'] = df['word'].str.replace('-\n', '')
df['examples'] = df['examples'].str.replace('-\n', '')

# If word isn't transferred but there is a word after, it's a newline.
# Make that a whitespace.
df['word'] = df['word'].str.replace('\n', ' ')
df['examples'] = df['examples'].str.replace('\n', ' ')

df.to_csv(CLEANED_WORDLIST_CSV_PATH, index=False)
logger.info('Successfully cleaned CSV')
logger.info(f'Saved cleaned CSV wordlist at {CLEANED_WORDLIST_CSV_PATH}')
