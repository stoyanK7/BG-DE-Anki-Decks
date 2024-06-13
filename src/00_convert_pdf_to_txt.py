"""Convert the wordlist PDF file to TXT file.

Reason for conversion is so that the TXT file can later be parsed
and words and translations can be extracted.

Note: This script was used only once during the beginning of the project.
The exported TXT file has since been manually edited to fix parsing
errors.
"""

import os
import subprocess

from utils.constants import WORDLIST_PDF_PATH, WORDLIST_TXT_PATH
from utils.logger import logger

if not os.path.exists(WORDLIST_PDF_PATH):
    logger.error('PDF file not found')
    logger.error(f'{WORDLIST_PDF_PATH} does not exist')
    raise SystemExit('Aborting')

logger.info('Converting PDF to TXT')

completed_process = subprocess.run(
    [
        'pdftotext',
        '-layout',  # Maintains the original physical layout of the file.
        '-f',  # Specifies the first page to convert.
        '16',
        '-l',  # Specifies the last page to convert.
        '102',
        WORDLIST_PDF_PATH,
        WORDLIST_TXT_PATH,
    ],
    capture_output=True,
)

if completed_process.returncode != 0:
    logger.error(
        f'pdftotext returned non-zero exit status '
        f'{completed_process.returncode}'
    )
    logger.error(completed_process.stderr)
    raise SystemExit('Aborting')

logger.info('Successfully converted PDF to TXT')
logger.info(f'Saved raw TXT wordlist at {WORDLIST_TXT_PATH}')
