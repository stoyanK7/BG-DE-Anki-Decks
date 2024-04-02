import os
import subprocess

wordlist_path = "Goethe-Zertifikat_B1_Wortliste.pdf"
wordlist_first_page = "16"
wordlist_last_page = "102"
wordlist_text_path = "Goethe-Zertifikat_B1_Wortliste.txt"

if not os.path.exists(wordlist_text_path):
    command = [
        "pdftotext",
        "-layout",  # Maintain the original physical layout of the text.
        "-f",  # Specifies the first page to convert.
        wordlist_first_page,
        "-l",  # Specifies the last page to convert.
        wordlist_last_page,
        wordlist_path,  # The path to the PDF file.
        wordlist_text_path,  # The path to the text file.
    ]
    subprocess.run(command, stdout=subprocess.PIPE)
