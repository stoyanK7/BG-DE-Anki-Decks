"""Preprocess the CSV file - prepare for translation and creation of audio and images."""

import hashlib
import os
import re
import sys

import pandas as pd
from utils.constants import (
    CLEANED_WORDLIST_CSV_PATH,
    PREPROCESSED_WORDLIST_CSV_PATH,
)
from utils.logger import logger

if not os.path.exists(CLEANED_WORDLIST_CSV_PATH):
    logger.error(f'{CLEANED_WORDLIST_CSV_PATH} not found')
    sys.exit()

df = pd.read_csv(CLEANED_WORDLIST_CSV_PATH)

# Catch strings such as '1. ' or '2. ' or '13. '.
example_number_pattern = re.compile(r'(\d+)\.\s\w+')


def split_example(example: str) -> list[str]:
    """Split example string into a list of examples if many are found."""
    is_only_one_example = not example.startswith('1. ')
    if is_only_one_example:
        return [example]

    # Else we have multiple examples.

    # Find actual delimiters by ensuring each one is bigger than
    # the previous delimiter by 1.
    # For example [1, 2, 3, 200, 4, 5] -> [1, 2, 3, 4, 5]
    matches: list[str] = re.findall(example_number_pattern, example)
    actual_numeric_delimiters = []
    last_num = 0
    for str_num in matches:
        int_num = int(str_num)
        if int_num == last_num + 1:
            actual_numeric_delimiters.append(f'{str_num}. ')
            last_num += 1

    # To split with multiple delimiters, we have to create a regex pattern.
    pattern = '|'.join(map(re.escape, actual_numeric_delimiters))
    pattern = re.compile(pattern)
    examples: list[str] = pattern.split(example)
    examples = [example.strip() for example in examples if example.strip()]

    return examples


df['example'] = df['example'].apply(split_example)

verb_pattern = re.compile(r'^([^,]+),([^,]+),([^,]+), (hat|ist).+')
der_die_pattern = re.compile(r'^(der\s[\wÄÖÜäöü]+),.*\s(die\s[\wÄÖÜäöü]+), .+')
normal_word_pattern = re.compile(r'((der|die|das)\s[\wÄÖÜäöü\-]+)')


def determine_audio_text(word: str) -> str:
    """Determine which part of the words has to be converted to an audio file."""
    if match := verb_pattern.match(word):
        return (
            match.group(1)
            .strip()
            .replace('(sich etwas)', 'sich etwas')
            .replace('(sich)', 'sich')
        )

    if match := der_die_pattern.match(word):
        return f'{match.group(1).strip()}, {match.group(2).strip()}'

    if match := normal_word_pattern.match(word):
        return match.group(1).strip()

    if '(Pl.)' in word:
        return word.split('(Pl.)')[0].strip()

    if '(D' in word:
        return word.split('(D')[0].strip()

    if '(A' in word:
        return word.split('(A')[0].strip()

    if '(CH' in word:
        return word.split('(CH')[0].strip()

    if '/' in word:
        return word.split('/')[0].strip()

    if word.startswith('-'):
        return word.lstrip('-')

    return word


df['word_audio'] = df['word'].apply(determine_audio_text)


just_word_pattern = re.compile(r'(der|die|das)\s([\wÄÖÜäöü\-]+)')


def determine_word_search(word: str) -> str:
    """Determine which word to put into PONS dictionary for translation."""
    if match := just_word_pattern.match(word):
        return match.group(2).strip()

    if word.startswith('sich etwas'):
        return word.split('sich etwas')[1].strip()

    if word.startswith('sich'):
        return word.split('sich')[1].strip()

    if word.startswith('jdn.'):
        return word.split('jdn.')[1].strip()

    if ',' in word:
        return word.split(',')[0].strip()

    return word


df['word_search'] = df['word_audio'].apply(determine_word_search)


def hash_word(word: str) -> str:
    """Generate unique word hash to use as identifier for folder names."""
    return hashlib.sha256(word.encode('utf-8')).hexdigest()


df['word_hash'] = df['word'].apply(hash_word)


df.to_csv(PREPROCESSED_WORDLIST_CSV_PATH, index=False)
logger.info(f'Saved preprocessed CSV at {PREPROCESSED_WORDLIST_CSV_PATH}')
