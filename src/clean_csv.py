"""Clean the CSV file - strip whitespaces and newlines."""

import os
import sys

import pandas as pd
from utils.constants import CLEANED_WORDLIST_CSV_PATH, WORDLIST_CSV_PATH
from utils.logger import logger

if not os.path.exists(WORDLIST_CSV_PATH):
    logger.error(f'{WORDLIST_CSV_PATH} not found')
    sys.exit()

df = pd.read_csv(WORDLIST_CSV_PATH)

null_count: int = df.isnull().sum().sum()
if null_count > 0:
    null_mask = df.isnull().any(axis=1)
    null_rows = df[null_mask]
    logger.error(f"""\
Found {null_count} null values. Cleaning/Preprocessing
/Parsing of the TXT file must have gone wrong. Null rows are:

{null_rows}
""")
    sys.exit()

# Strip leading whitespaces and trailing newlines.
df['word'] = df['word'].str.strip()
df['example'] = df['example'].str.strip()

# Certain words are transferred over with a hyphen + newline.
df['word'] = df['word'].str.replace('-\n', '')
df['example'] = df['example'].str.replace('-\n', '')

# If word isn't transferred but there is a word after, it's a newline - strip.
df['word'] = df['word'].str.replace('\n', ' ')
df['example'] = df['example'].str.replace('\n', ' ')

df.to_csv(CLEANED_WORDLIST_CSV_PATH, index=False)
logger.info(f'Saved cleaned CSV at {CLEANED_WORDLIST_CSV_PATH}')
