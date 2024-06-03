"""Shared constants such as filenames and directory paths."""

import os

# Common constants
PAGE_BREAK = '\x0c'

# Common paths
ROOT_DIR_PATH = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
)
DATA_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'data')

# 00_convert_pdf_to_text.py
WORDLIST_PDF_PATH = os.path.join(DATA_DIR_PATH, '00_Wordlist.pdf')
WORDLIST_TXT_PATH = os.path.join(DATA_DIR_PATH, '00_Wordlist_Raw.txt')

# 01_clean_txt.py
WORDLIST_CLEANED_TXT_PATH = os.path.join(
    DATA_DIR_PATH, '01_Wordlist_Cleaned.txt'
)

# 02_preprocess_txt.py
WORDLIST_PREPROCESSED_TXT_PATH = os.path.join(
    DATA_DIR_PATH, '02_Wordlist_Preprocessed.txt'
)

# 03_parse_txt.py
WORDLIST_CSV_PATH = os.path.join(DATA_DIR_PATH, '03_Wordlist_Raw.csv')

# 04_clean_csv.py
WORDLIST_CLEANED_CSV_PATH = os.path.join(
    DATA_DIR_PATH, '04_Wordlist_Cleaned.csv'
)

# 05_preprocess_csv.py
WORDLIST_PREPROCESSED_CSV_PATH = os.path.join(
    DATA_DIR_PATH, '05_Wordlist_Preprocessed.csv'
)

# 06_create_audio.py
AUDIO_RECORDINGS_DIR_PATH = os.path.join(DATA_DIR_PATH, 'audio')

# 07_translate.py
TRANSLATIONS_DIR_PATH = os.path.join(DATA_DIR_PATH, 'translations')

# 08_postprocess_csv.py
DECK_DATA_JSON_PATH = os.path.join(DATA_DIR_PATH, '08_Deck_Data.json')

# 09_generate_deck.py
ANKI_DECK_TXT_PATH = os.path.join(DATA_DIR_PATH, 'Anki_Deck.txt')
