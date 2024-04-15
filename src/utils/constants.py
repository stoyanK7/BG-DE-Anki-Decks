"""Shared constants such as filenames and directory paths."""

import os

ROOT_DIR_PATH: str = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
)
DATA_DIR_PATH: str = os.path.join(ROOT_DIR_PATH, 'data')
INPUT_DATA_DIR_PATH: str = os.path.join(DATA_DIR_PATH, 'input')
OUTPUT_DATA_DIR_PATH: str = os.path.join(DATA_DIR_PATH, 'output')
RAW_DATA_DIR_PATH: str = os.path.join(OUTPUT_DATA_DIR_PATH, 'raw')
CLEANED_DATA_DIR_PATH: str = os.path.join(OUTPUT_DATA_DIR_PATH, 'cleaned')
PREPROCESSED_DATA_DIR_PATH: str = os.path.join(
    OUTPUT_DATA_DIR_PATH, 'preprocessed'
)
AUDIO_RECORDINGS_DIR_PATH: str = os.path.join(OUTPUT_DATA_DIR_PATH, 'audio')
TRANSLATIONS_DIR_PATH: str = os.path.join(OUTPUT_DATA_DIR_PATH, 'translations')

WORDLIST_PDF_FILENAME = 'Goethe-Zertifikat_B1_Wortliste.pdf'
WORDLIST_PDF_PATH: str = os.path.join(
    INPUT_DATA_DIR_PATH, WORDLIST_PDF_FILENAME
)

WORDLIST_TXT_FILENAME = 'Goethe-Zertifikat_B1_Wortliste.txt'
WORDLIST_TXT_PATH: str = os.path.join(
    RAW_DATA_DIR_PATH, WORDLIST_TXT_FILENAME
)

CLEANED_WORDLIST_TXT_PATH: str = os.path.join(
    CLEANED_DATA_DIR_PATH, WORDLIST_TXT_FILENAME
)

PREPROCESSED_WORDLIST_TXT_PATH: str = os.path.join(
    PREPROCESSED_DATA_DIR_PATH, WORDLIST_TXT_FILENAME
)

WORDLIST_CSV_FILENAME = 'Goethe-Zertifikat_B1_Wortliste.csv'
WORDLIST_CSV_PATH: str = os.path.join(
    RAW_DATA_DIR_PATH, WORDLIST_CSV_FILENAME
)

CLEANED_WORDLIST_CSV_PATH: str = os.path.join(
    CLEANED_DATA_DIR_PATH, WORDLIST_CSV_FILENAME
)

PREPROCESSED_WORDLIST_CSV_PATH: str = os.path.join(
    PREPROCESSED_DATA_DIR_PATH, WORDLIST_CSV_FILENAME
)


PAGE_BREAK = '\x0c'
