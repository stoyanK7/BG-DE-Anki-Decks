"""Postprocess the CSV file - prepare for deck generation."""

import ast
import os
import sys

import pandas as pd
from utils.constants import (
    POSTPROCESSED_WORDLIST_CSV_PATH,
    PREPROCESSED_WORDLIST_CSV_PATH,
    TRANSLATIONS_DIR_PATH,
)
from utils.logger import logger

if not os.path.exists(PREPROCESSED_WORDLIST_CSV_PATH):
    logger.error(f'{PREPROCESSED_WORDLIST_CSV_PATH} not found')
    sys.exit()

df = pd.read_csv(PREPROCESSED_WORDLIST_CSV_PATH)

for _, row in df.iterrows():
    wh: str = row['word_hash']
    if not os.path.exists(os.path.join(TRANSLATIONS_DIR_PATH, wh)):
        logger.error(f'Translation directory for word hash {wh} does not exist')
        sys.exit()

    if not os.path.exists(
        os.path.join(TRANSLATIONS_DIR_PATH, wh, 'translation.txt')
    ):
        logger.error(f'Translation file for word hash {wh} does not exist')
        sys.exit()


def extract_word_translation(word_hash: str) -> str:
    """Extract word translation from saved DeepL response."""
    path_to_translation_txt: str = os.path.join(
        TRANSLATIONS_DIR_PATH,
        word_hash,
        'translation.txt',
    )

    with open(path_to_translation_txt, 'r') as file:
        contents = file.read()

    split_contents: list[str] = contents.split('---')
    word_translation = split_contents[0].strip()
    return word_translation


df['word_translation'] = df['word_hash'].apply(extract_word_translation)


def extract_example_translation(word_hash: str) -> str:
    """Extract example translation from saved DeepL response."""
    path_to_translation_txt: str = os.path.join(
        TRANSLATIONS_DIR_PATH,
        word_hash,
        'translation.txt',
    )

    with open(path_to_translation_txt, 'r') as file:
        contents = file.read()

    split_contents: list[str] = contents.split('---\n')
    translated_examples = []
    for example in split_contents[1:]:
        translated_examples.append(example.strip())

    return str(translated_examples)


df['example_translation'] = df['word_hash'].apply(extract_example_translation)

for _, row in df.iterrows():
    examples: list[str] = ast.literal_eval(row['example'])
    example_translation: list[str] = ast.literal_eval(
        row['example_translation']
    )
    if len(examples) != len(example_translation):
        logger.error(
            f'Mismatch in translations for word hash {row["word_hash"]}'
        )
        sys.exit()

df.to_csv(POSTPROCESSED_WORDLIST_CSV_PATH, index=False)
logger.info(f'Saved postprocessed CSV at {POSTPROCESSED_WORDLIST_CSV_PATH}')
