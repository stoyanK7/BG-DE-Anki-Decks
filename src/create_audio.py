"""Create audio files for word and examples."""

import ast
import os
import sys

import pandas as pd
import torch
from rich.progress import track
from TTS.api import TTS
from utils.constants import (
    AUDIO_RECORDINGS_DIR_PATH,
    PREPROCESSED_WORDLIST_CSV_PATH,
)
from utils.logger import logger

if not os.path.exists(PREPROCESSED_WORDLIST_CSV_PATH):
    logger.error(f'{PREPROCESSED_WORDLIST_CSV_PATH} not found')
    sys.exit()

device = 'cuda' if torch.cuda.is_available() else 'cpu'

tts = TTS(
    model_name='tts_models/de/thorsten/tacotron2-DDC', progress_bar=False
).to(device)

df = pd.read_csv(PREPROCESSED_WORDLIST_CSV_PATH)

for _, row in track(
    df.iterrows(),
    total=df.shape[0],
    description='Creating...',
    update_period=10,
    auto_refresh=False,
):
    word_hash = row['word_hash']
    path_to_audio_dir: str = os.path.join(AUDIO_RECORDINGS_DIR_PATH, word_hash)
    if not os.path.exists(path_to_audio_dir):
        os.makedirs(path_to_audio_dir)

    path_to_word_audio_file: str = os.path.join(path_to_audio_dir, 'word.wav')
    if not os.path.exists(path_to_word_audio_file):
        tts.tts_to_file(
            text=row['word_audio'], file_path=path_to_word_audio_file
        )

    examples: list[str] = ast.literal_eval(row['example'])
    for idx, example in enumerate(examples):
        path_to_example_audio_file = os.path.join(
            path_to_audio_dir, f'example{idx + 1}.wav'
        )
        if not os.path.exists(path_to_example_audio_file):
            tts.tts_to_file(text=example, file_path=path_to_example_audio_file)
