# Development

This document describes the process for running this application on your local machine.

> [!IMPORTANT]
> This software was developed and tested only on Ubuntu 22.04.

<!-- TOC -->
* [Development](#development)
  * [Getting started](#getting-started)
  * [Activating the environment](#activating-the-environment)
  * [Running the whole pipeline](#running-the-whole-pipeline)
  * [Running an individual step](#running-an-individual-step)
  * [Running the linter](#running-the-linter)
  * [Pipeline explanations](#pipeline-explanations)
<!-- TOC -->

## Getting started

```shell
git clone https://github.com/stoyanK7/BG-DE-anki-decks.git
cd BG-DE-anki-decks
pipenv sync --dev
```

## Activating the environment

```shell
pipenv shell
```

## Running the whole pipeline

```shell
./run.sh
```

## Running an individual step

```shell
python3 src/XX_step_you_want_to_run.py
```

## Running the linter

```shell
ruff format . && ruff check . --fix .
```

## Pipeline explanations

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
