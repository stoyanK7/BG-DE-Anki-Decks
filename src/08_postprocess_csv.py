"""Postprocess the CSV file.

Prepare JSON file for deck generation.
"""

import ast
import json
import os

import pandas as pd
from utils.constants import (
    DECK_DATA_JSON_PATH,
    TRANSLATIONS_DIR_PATH,
    WORDLIST_PREPROCESSED_CSV_PATH,
)
from utils.logger import logger

if not os.path.exists(WORDLIST_PREPROCESSED_CSV_PATH):
    logger.error(
        'Preprocessed wordlist CSV file not found. Did you run "05_preprocess_csv.py"?'
    )
    logger.error(f'{WORDLIST_PREPROCESSED_CSV_PATH} does not exist')
    raise SystemExit('Aborting')

logger.info('Postprocessing CSV')

df = pd.read_csv(WORDLIST_PREPROCESSED_CSV_PATH)

# Assert that all translations are in place.
for row in df.itertuples():
    if not os.path.exists(
        os.path.join(TRANSLATIONS_DIR_PATH, row.word, 'translation.txt')
    ):
        logger.error(f'Translation TXT file for word {row.word} does not exist')
        logger.error('Try running "07_translate.py"')
        raise SystemExit('Aborting')


def extract_word_translation(word: str) -> str:
    """Extract word translation from saved DeepL response."""
    path_to_translation_txt = os.path.join(
        TRANSLATIONS_DIR_PATH,
        word,
        'translation.txt',
    )

    with open(path_to_translation_txt, 'r', encoding='utf-8') as file:
        contents = file.read()

    split_contents = contents.split('---')
    # First item is a word
    word_translation = split_contents[0].strip()
    return str([word_translation])


df['word_translation'] = df['word'].apply(extract_word_translation)


def extract_examples_translations(word: str) -> str:
    """Extract examples translations from saved DeepL response."""
    path_to_translation_txt = os.path.join(
        TRANSLATIONS_DIR_PATH,
        word,
        'translation.txt',
    )

    with open(path_to_translation_txt, 'r', encoding='utf-8') as file:
        contents = file.read()

    split_contents = contents.split('---\n')
    translated_examples = []
    # First item is word, everything else is examples
    for example in split_contents[1:]:
        translated_examples.append(example.strip())

    return str(translated_examples)


df['examples_translations'] = df['word'].apply(extract_examples_translations)

# Get list of objects that have been manually verified.
manually_verified_words = set()
word_to_object = dict()
if os.path.exists(DECK_DATA_JSON_PATH):
    with open(DECK_DATA_JSON_PATH, 'r', encoding='utf-8') as file:
        objects = json.load(file)

    for obj in objects:
        word_to_object[obj['word_de']] = obj
        if obj['manually_verified']:
            manually_verified_words.add(obj['word_de'])

# Prepare JSON file.
data = []
for row in df.itertuples():
    # If word has already been manually verified, don't touch it.
    if row.word in manually_verified_words:
        data.append(word_to_object[row.word])
        continue

    examples_de = ast.literal_eval(row.examples)
    examples_bg = ast.literal_eval(row.examples_translations)
    examples_list = []
    for de, bg in zip(examples_de, examples_bg):
        examples_list.append({'example_de': de, 'example_bg': bg})

    data.append(
        {
            'manually_verified': False,
            'word_de': row.word,
            'word_bg': ast.literal_eval(row.word_translation),
            'examples': examples_list,
        }
    )


with open(DECK_DATA_JSON_PATH, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
