"""Generate the anki deck from the post-processed list."""

import ast
import os
import re
import sys

import pandas as pd
from rich.progress import track
from utils.constants import ANKI_DECK_TXT_PATH, POSTPROCESSED_WORDLIST_CSV_PATH
from utils.logger import logger

if not os.path.exists(POSTPROCESSED_WORDLIST_CSV_PATH):
    logger.error(f'{POSTPROCESSED_WORDLIST_CSV_PATH} not found')
    sys.exit()

logger.info('Generating deck')

df = pd.read_csv(POSTPROCESSED_WORDLIST_CSV_PATH)

escaped_double_quote = '\\"'
separator = '|'
headers = f"""\
#separator:{separator}
#html:true\n\n"""

# Use a list for contents and do ''.join(contents) later.
# This is for performance reasons. String concatenation gets slow here.
contents = [headers]


def build_gender_square(gender: str) -> str:
    """Create HTML for a small 16x16 square with a color representing the gender of a word."""
    gender_to_color_mapping = {
        'der': '#4D94FF',  # Blue
        'die': '#FF66B2',  # Pink
        'das': '#808080',  # Gray
        'pl': '#66FF99',  # Green
    }
    color = gender_to_color_mapping[gender]
    result = f"""\
<span
    style='
         display: inline-block;
         width: 16px;
         height: 16px;
         margin-right: 5px;
         background-color: {color};'>
</span>
"""
    result = result.replace('\n', '')
    result = re.sub(r'\s+', ' ', result)
    return result


def build_front_side(word: str, word_hash: str) -> str:
    """Build the front side of a card."""
    gender_square = ''
    gendered_word_pattern = re.compile(r'(der|die|das)\s[\wÄÖÜäöü\-]+')
    if match := gendered_word_pattern.match(word):
        gender_square = build_gender_square(gender=match.group(1))

    word = word.replace('(CH', '(🇨🇭')
    word = word.replace('(D', '(🇩🇪')
    word = word.replace('(A', '(🇦🇹')

    result = f"""\
"<div
    style='font-size: 16px;'>
    {gender_square}{word} [sound:{word_hash}.wav]
</div>\""""
    result = result.replace('\n', '')
    result = re.sub(r'\s+', ' ', result)
    return result


def build_back_side(
    examples: list[str], word_translation: str, example_translation: list[str]
) -> str:
    """Build the back side of a card."""
    word_translation = '<br>'.join(ast.literal_eval(word_translation))
    back_side = [
        '"',
        f"""\
<div
    style='font-size: 16px;'>
    {word_translation}
</div>   
""",
        '<br>',
    ]
    for idx in range(len(examples)):
        back_side.append(f"""\
<div
    style='font-size: 16px;'>
    🇩🇪 {examples[idx].replace('"', escaped_double_quote)}
    <br>
    🇧🇬 {example_translation[idx].replace('"', escaped_double_quote)}
</div>
<br>
""")
    back_side.append('"')
    result = ''.join(back_side)
    result = result.replace('\n', '')
    result = re.sub(r'\s+', ' ', result)
    return result


for _, row in track(
    df.iterrows(),
    total=df.shape[0],
    description='Generating deck...',
    update_period=10,
    auto_refresh=False,
):
    contents.append(
        build_front_side(word=row['word'], word_hash=row['word_hash'])
    )
    contents.append(separator)
    contents.append(
        build_back_side(
            examples=ast.literal_eval(row['example']),
            word_translation=row['word_translation'],
            example_translation=ast.literal_eval(row['example_translation']),
        )
    )
    contents.append('\n\n\n')

with open(ANKI_DECK_TXT_PATH, 'w') as file:
    file.write(''.join(contents))

logger.info(f'Saved anki deck at {ANKI_DECK_TXT_PATH}')
