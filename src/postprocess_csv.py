"""Postprocess the CSV file - prepare for deck generation."""

import ast
import json
import os
import sys

import pandas as pd
from utils.constants import (
    EXAMPLE_TRANSLATIONS_FIX_PATH,
    POSTPROCESSED_WORDLIST_CSV_PATH,
    PREPROCESSED_WORDLIST_CSV_PATH,
    TRANSLATIONS_DIR_PATH,
    WORD_TRANSLATIONS_FIX_JSON_PATH,
)
from utils.logger import logger

if not os.path.exists(PREPROCESSED_WORDLIST_CSV_PATH):
    logger.error(f'{PREPROCESSED_WORDLIST_CSV_PATH} not found')
    sys.exit()

if not os.path.exists(WORD_TRANSLATIONS_FIX_JSON_PATH):
    logger.error(f'{WORD_TRANSLATIONS_FIX_JSON_PATH} not found')
    sys.exit()

if not os.path.exists(EXAMPLE_TRANSLATIONS_FIX_PATH):
    logger.error(f'{EXAMPLE_TRANSLATIONS_FIX_PATH} not found')
    sys.exit()

df = pd.read_csv(PREPROCESSED_WORDLIST_CSV_PATH)
with open(WORD_TRANSLATIONS_FIX_JSON_PATH, 'r') as file:
    word_translations_fix = json.load(file)
with open(EXAMPLE_TRANSLATIONS_FIX_PATH, 'r') as file:
    example_translations_fix = json.load(file)

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
    return str([word_translation])


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


# Apply word translation fix.
word_fix_mask = df['word'].isin(word_translations_fix.keys())
df_word_fix = df[word_fix_mask]

if df_word_fix.shape[0] != len(word_translations_fix):
    logger.error('Not all word fixes were applied. Mismatch in keys.')
    logger.error(
        f'{df_word_fix.shape[0]} rows caught in mask, {len(word_translations_fix)} expected'
    )
    logger.error('The following keys were not found:')
    logger.error(
        set(word_translations_fix.keys()) - set(df_word_fix['word'].to_list())
    )
    sys.exit()

df.loc[word_fix_mask, 'word_translation'] = (
    df.loc[word_fix_mask, 'word'].map(word_translations_fix).apply(str)
)

# Apply example translation fix.
for _, row in df.iterrows():
    for key, value in example_translations_fix.items():
        if row['word'] == key:
            result = ast.literal_eval(row['example_translation'])
            for idx, de_sentence in enumerate(ast.literal_eval(row['example'])):
                if de_sentence not in value.keys():
                    continue
                result[idx] = value[de_sentence]
            row['example_translation'] = str(result)


# Sanity check.
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
