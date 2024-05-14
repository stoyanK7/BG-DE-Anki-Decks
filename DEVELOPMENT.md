# Development

This document describes the process for running this application on your local computer.

## Getting started

> [!NOTE]  
> The software ran smoothly on Ubuntu 22.04. However, there's no guarantee it will work on Windows, despite using adaptable modules.

You need [`pdftotext`](https://www.xpdfreader.com/pdftotext-man.html) to run the conversion script([convert_pdf_to_txt.py](src/convert_pdf_to_txt.py)). `pdftotext` is included with [the `poppler` library](https://poppler.freedesktop.org/).

```shell
git clone https://github.com/stoyanK7/BG-DE-anki-decks.git
cd BG-DE-anki-decks
pipenv sync --dev
```

## Run the whole pipeline

```shell
python3 src/clean_txt.py \
    && python3 src/preprocess_txt.py \
    && python3 src/parse_txt.py \
    && python3 src/clean_csv.py \
    && python3 src/preprocess_csv.py \
    && python3 src/translate.py \
    && python3 src/create_audio.py \
    && python3 src/postprocess_csv.py \
    && python3 src/generate_deck.py
```

## Process

```mermaid
flowchart LR
    inputPdfFile["`**data/input/Goethe-Zertifikat_B1_Wortliste.pdf**
    -----------
    Input file. Downloaded from Goethe Institut's website.`"]
    
    convertPdfToTxtScript[["`**convert_pdf_to_txt.py**
    -----------
    Convert *data/input/\*.pdf* to a text file - *data/output/raw/\*.txt*`"]]
    
    rawTxtFile["`**data/output/raw/Goethe-Zertifikat_B1_Wortliste.txt**
    -----------
    Text representation of the input PDF file.`"]
    
    manuallyEdit["`**Manually edit data/output/raw/\*.txt**
    -----------
    This step is inevitable. It's faster to catch edge cases and fix them manually than trying to come up with an algorithm.
    This step can occur during any of the steps below.`"]

    cleanTxtScript[["`**clean_txt.py**
    -----------
    Clean *data/output/raw/\*.txt*`"]]
    cleanedTxtFile["Cleaned TXT file"]
    preprocessTxtScript[["Preprocess Txt"]]
    preprocessedTxtFile["preprocessed TXT file"]
    parseTxtScript[["Parse TXT"]]
    rawCsvFile[("Raw CSV file")]
    cleanCsvScript[["Clean CSV"]]
    cleanedCsvFile[("Cleaned CSV file")]
    preprocessCsvScript[["Preprocess CSV"]]
    preprocessedCsvFile[("Preprocessed CSV file")]

    convertPdfToTxtScript -->|Reads| inputPdfFile
    convertPdfToTxtScript -->|Writes| rawTxtFile
    manuallyEdit -->|Edits| rawTxtFile
    cleanTxtScript -->|Reads| rawTxtFile
    cleanTxtScript -->|Writes| cleanedTxtFile
    preprocessTxtScript -->|Reads| cleanedTxtFile
    preprocessTxtScript -->|Writes| preprocessedTxtFile
    
    parseTxtScript -->|Reads| preprocessedTxtFile
    parseTxtScript -->|Writes| rawCsvFile
    
    cleanCsvScript -->|Reads| rawCsvFile
    cleanCsvScript -->|Writes| cleanedCsvFile
    
    preprocessCsvScript -->|Reads| cleanedCsvFile
    preprocessCsvScript -->|Writes| preprocessedCsvFile
    
```
