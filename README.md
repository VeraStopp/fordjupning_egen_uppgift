# SCB Income Analysis Pipeline

En modular Python data pipeline for analyzing income data from Statistics Sweden (SCB)

---

## Installation and Enviroment Setup
python version: 3.13.7

### 1. Clon repository and navigate to the project root
```bash
git clone https://github.com/VeraStopp/fordjupning_egen_uppgift.git
cd Vera_Stopp_fordjupning_python 
```
### 2. Create and activate a virtual enviroment
```bash
python -m venv -venv
source -venv/Scripts/activate
```
### 3. Install dependencies and the package
```bash
python -m pip install --upgrade pip
python -m pip install -e .
```
## Usage
To execute the full pipeline from the terminal:
```bash
python -m income_report
```
## Running tests
To execute all unit tests located in the `test/` directory:
```bash
pytest
```

## Data Requirements
The pipeline expects a specific raw CSV dataset from `https://www.statistikdatabasen.scb.se/pxweb/sv/ssd/START__HE__HE0110__HE0110A/SamForvInk1c/` 
Raw export files should be places in `data/raw` prior to running the pipeline

If you wish to update the input data, esure the file matches the following structure:
* **File Format:** CSV (`.csv`) with UTF-8 encoding
* **Required columns:** 
    * `kön` - Gender (`män`, `kvinnor` or `total`)
    * `utbildningsnivå` - Educational level categories
    * `år` / `year` - Observation year
    * `inkomst_tkr` / `medelinkomst` - Average income in thousands of SEK

## License & author
Author: Vera Stopp
Data Source: Statistiska Centralbyrån (SCB)