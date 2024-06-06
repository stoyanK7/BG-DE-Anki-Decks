#!/bin/bash

python3 src/01_clean_txt.py \
    && python3 src/02_preprocess_txt.py \
    && python3 src/03_parse_txt.py \
    && python3 src/04_clean_csv.py \
    && python3 src/05_preprocess_csv.py \
    && python3 src/07_translate.py \
    && python3 src/06_create_audio.py \
    && python3 src/08_postprocess_csv.py \
    && python3 src/09_generate_deck.py
