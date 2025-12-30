import os
from src.data_preparation import prepare_data
import pandas as pd


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, 'src')
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')
DATA_DIR = os.path.join(BASE_DIR, 'data')
DOC_DIR = os.path.join(BASE_DIR, 'docs', 'index.html')


RAW_DATA_PATH = os.path.join(DATA_DIR, 'raw', "dataset.csv")
PROCESSED_DATA_PATH = os.path.join(DATA_DIR, 'processed', "processed.csv")

DATA_PREPARATION_PATH = os.path.join(SRC_DIR, 'data_preparation.py',)
FEATURE_ENGINEERING_PATH = os.path.join(SRC_DIR, 'feature_engineering.py',)
CHURN_ANALYSIS_PATH = os.path.join(SRC_DIR, 'churn_analysis.py',)
VISUALIZATION_PATH = os.path.join(SRC_DIR, 'visualization.py',)

FIGURE_PATH = os.path.join( OUTPUT_DIR, 'figures')

def main():
    prepare_data(RAW_DATA_PATH, PROCESSED_DATA_PATH)


if __name__ == "__main__":
    main()