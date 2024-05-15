"""Translate from DE to BG using selenium."""

import ast
import os
import random
import sys
from time import sleep

import pandas as pd
from rich.progress import track
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from utils.constants import (
    PREPROCESSED_WORDLIST_CSV_PATH,
    TRANSLATIONS_DIR_PATH,
)
from utils.logger import logger

if not os.path.exists(PREPROCESSED_WORDLIST_CSV_PATH):
    logger.error(f'{PREPROCESSED_WORDLIST_CSV_PATH} not found')
    sys.exit()

df = pd.read_csv(PREPROCESSED_WORDLIST_CSV_PATH)

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

driver.get('https://www.deepl.com/translator')
sleep(3)
if 'DeepL Translate' not in driver.title:
    logger.error()
    sys.exit()


accept_cookies = wait.until(
    ec.visibility_of_element_located(
        (By.XPATH, '/html/body/div[1]/div[1]/div[1]/div/div[3]/button[2]')
    )
)
accept_cookies.click()

extension_suggestion_close = wait.until(
    ec.visibility_of_element_located(
        (
            By.XPATH,
            '/html/body/div[1]/div[1]/div[2]/div/div[1]/div/main/div[3]/div/div/div[2]/button',
        )
    )
)
extension_suggestion_close.click()

translate_from_button = driver.find_element(
    By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/div[1]/div/main/div[2]/nav/div/div[2]/div/div/div[1]/section/div/div[1]/div/div[1]/div/div[1]/span/span/span/button/span/div/div/span/span'
)
translate_from_button.click()

translate_from_input = wait.until(
    ec.visibility_of_element_located(
        (
            By.XPATH,
            '/html/body/div[1]/div[1]/div[2]/div[2]/div[1]/div/main/div[2]/nav/div/div[2]/div/div/div[1]/section/div/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div/input',
        )
    )
)
translate_from_input.click()
sleep(2)
translate_from_input.send_keys('German')
sleep(2)
translate_from_input.send_keys(Keys.RETURN)
sleep(2)

translate_to_button = driver.find_element(
    By.XPATH, '//*[@id="headlessui-popover-button-34"]/span/div/div/span/span'
)
translate_to_button.click()

translate_to_input = wait.until(
    ec.visibility_of_element_located(
        (
            By.XPATH,
            '/html/body/div[1]/div[1]/div[2]/div[2]/div[1]/div/main/div[2]/nav/div/div[2]/div/div/div[1]/section/div/div[1]/div/div[3]/div[1]/div[1]/div/div/div[1]/div/input',
        )
    )
)
translate_to_input.click()
sleep(2)
translate_to_input.send_keys('Bulgarian')
sleep(2)
translate_to_input.send_keys(Keys.RETURN)
sleep(2)

def get_translation(text_to_translate: str) -> str:
    """Get translation for a piece of text."""
    input_textbox = driver.find_element(
        By.XPATH,
        '//*[@id="textareasContainer"]/div[1]/section/div/div[1]/d-textarea',
    )
    input_textbox.click()
    sleep(1)
    input_textbox.send_keys(text_to_translate)
    sleep(5)
    output_textbox = driver.find_element(
        By.XPATH,
        '/html/body/div[1]/div[1]/div[2]/div/div[1]/div/main/div[2]/nav/div/div[2]/div/div/div[1]/section/div/div[2]/div[3]/section/div[1]/d-textarea/div',
    )

    translation: str = output_textbox.text

    input_textbox.send_keys(Keys.CONTROL + 'a')
    input_textbox.send_keys(Keys.DELETE)

    return translation


for _, row in track(
    df.iterrows(),
    total=df.shape[0],
    description='Scraping...',
    update_period=12,
    auto_refresh=False,
):
    word_hash: str = row['word_hash']
    path_to_translation_dir: str = os.path.join(
        TRANSLATIONS_DIR_PATH, word_hash
    )
    if not os.path.exists(path_to_translation_dir):
        os.mkdir(path_to_translation_dir)

    path_to_translation_txt = os.path.join(
        path_to_translation_dir, 'translation.txt'
    )
    if os.path.exists(path_to_translation_txt):
        continue

    word: str = row['word_search']
    text_to_translate = f'{word}\n'
    examples: list[str] = ast.literal_eval(row['example'])
    for idx, example in enumerate(examples):
        text_to_translate += f'---\n{example}\n'

    # Text_to_translate string should look like:
    # Abschnitt
    # ---
    # Lesen Sie bitte den zweiten Abschnitt.
    # ---
    # Some other example, etc...

    result: str = get_translation(text_to_translate)
    with open(path_to_translation_txt, 'w') as file:
        file.write(result)

    sleep(random.randint(8, 12))

logger.info('Done scraping example translations.')
