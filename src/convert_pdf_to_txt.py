"""Convert the wordlist PDF file to TXT file.

Note: This script was used only once during the beginning of the project.
The exported .TXT file has since been manually edited to fix parsing
errors. See the following commits for the manual changes:
 - ae73703527e53d52634e05f85625258605e19761
 - 811d2298acb3ac9a466143ed2562a31faaff3054
 - 6fc67be7d450372be5bbe4dcf249ffef39c4c93e
"""

import subprocess

from utils.constants import WORDLIST_PDF_PATH, WORDLIST_TXT_PATH

wordlist_first_page = '16'
wordlist_last_page = '102'

command = [
    'pdftotext',
    '-layout',  # Maintain the original physical layout of the text.
    '-f',  # Specifies the first page to convert.
    wordlist_first_page,
    '-l',  # Specifies the last page to convert.
    wordlist_last_page,
    WORDLIST_PDF_PATH,
    WORDLIST_TXT_PATH,
]
subprocess.run(command, stdout=subprocess.PIPE)
