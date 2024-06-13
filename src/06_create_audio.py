"""Create audio files for DE word and DE examples."""

import ast
import io
import os
from contextlib import redirect_stdout

import pandas as pd
import torch
from rich.progress import track
from TTS.api import TTS
from utils.constants import (
    AUDIO_RECORDINGS_DIR_PATH,
    WORDLIST_PREPROCESSED_CSV_PATH,
)
from utils.logger import logger

if not os.path.exists(WORDLIST_PREPROCESSED_CSV_PATH):
    logger.error(
        'Cleaned wordlist CSV file not found. Did you run "05_preprocess_csv.py"?'
    )
    logger.error(f'{WORDLIST_PREPROCESSED_CSV_PATH} does not exist')
    raise SystemExit('Aborting')

logger.info('Creating audio')

stdout_capture = io.StringIO()
with redirect_stdout(stdout_capture):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    tts = TTS(
        model_name='tts_models/de/thorsten/tacotron2-DDC', progress_bar=False
    ).to(device)

df = pd.read_csv(WORDLIST_PREPROCESSED_CSV_PATH)

for row in track(
    df.itertuples(),
    total=df.shape[0],
    description='Creating audio...',
    update_period=10,
    auto_refresh=False,
):
    path_to_audio_dir = os.path.join(AUDIO_RECORDINGS_DIR_PATH, row.word)
    if not os.path.exists(path_to_audio_dir):
        os.makedirs(path_to_audio_dir)

    path_to_word_audio_file = os.path.join(path_to_audio_dir, 'word.wav')
    if not os.path.exists(path_to_word_audio_file):
        tts.tts_to_file(text=row.word_audio, file_path=path_to_word_audio_file)

    examples: list[str] = ast.literal_eval(row.examples)
    for idx, example in enumerate(examples):
        path_to_example_audio_file = os.path.join(
            path_to_audio_dir, f'example{idx + 1}.wav'
        )
        if not os.path.exists(path_to_example_audio_file):
            with redirect_stdout(stdout_capture):
                tts.tts_to_file(
                    text=example, file_path=path_to_example_audio_file
                )

logger.info('Successfully created audio files')
logger.info(f'Saved audio files at {AUDIO_RECORDINGS_DIR_PATH}')
